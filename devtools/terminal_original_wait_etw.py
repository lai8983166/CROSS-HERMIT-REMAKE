"""Bounded ETW + read-only suspended-stack observation of the original worker.

Only the qualified dedicated guest may run this. No injected traps, debug object
changes, game memory writes, fake API results or mouse/keyboard actions.
"""
import argparse
from contextlib import contextmanager
import ctypes as C
import gzip
import hashlib
import json
import os
from pathlib import Path
import struct
import time
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
ETL_LIMIT = 4 * 1024 * 1024
TRACE_FLAGS = 0x92  # THREAD | CSWITCH | SYSTEMCALL; no unrelated image/process rundown.


def need(value, message):
    if not value:
        raise ValueError(message)


def identity(path):
    data = Path(path).read_bytes()
    return dict(path=str(path), bytes=len(data), sha256=hashlib.sha256(data).hexdigest())


def kernel_path(name, system_root):
    prefix = '\\SystemRoot\\'
    if name.lower().startswith(prefix.lower()):
        path = Path(system_root) / name[len(prefix):]
    else:
        path = Path(name)
    path = path.resolve()
    need(path == (Path(system_root) / 'System32' / 'ntoskrnl.exe').resolve(),
         'actual kernel image must resolve to dedicated guest System32/ntoskrnl.exe')
    return path


def kernel_wait_identity():
    """Current driver base + actual guest PE export; no kernel memory access."""
    from devtools.native_input_isolation import require_qualified_guest
    require_qualified_guest()
    import pefile
    api = C.WinDLL('psapi', use_last_error=True)
    api.EnumDeviceDrivers.argtypes = [C.POINTER(C.c_void_p), C.c_uint32, C.POINTER(C.c_uint32)]
    api.EnumDeviceDrivers.restype = C.c_int
    for name in ('GetDeviceDriverBaseNameW', 'GetDeviceDriverFileNameW'):
        f = getattr(api, name)
        f.argtypes = [C.c_void_p, C.c_wchar_p, C.c_uint32]; f.restype = C.c_uint32
    bases = (C.c_void_p * 2048)(); used = C.c_uint32()
    need(api.EnumDeviceDrivers(bases, C.sizeof(bases), C.byref(used))
         and 0 < used.value < C.sizeof(bases) and used.value % 8 == 0,
         'bounded current driver-base enumeration')
    found = []
    for base in bases[:used.value // 8]:
        need(base, 'driver image bases unavailable; do not infer KASLR base')
        name = C.create_unicode_buffer(512)
        size = api.GetDeviceDriverBaseNameW(base, name, len(name))
        need(0 < size < len(name), 'complete driver basename')
        if name.value.lower() != 'ntoskrnl.exe':
            continue
        filename = C.create_unicode_buffer(32768)
        size = api.GetDeviceDriverFileNameW(base, filename, len(filename))
        need(0 < size < len(filename), 'complete actual kernel filename')
        path = kernel_path(filename.value, os.environ['SystemRoot'])
        pe = pefile.PE(str(path))
        need(pe.FILE_HEADER.Machine == 0x8664, 'guest x64 kernel PE')
        symbols = [s for s in pe.DIRECTORY_ENTRY_EXPORT.symbols if s.name == b'NtWaitForSingleObject']
        need(len(symbols) == 1 and not symbols[0].forwarder, 'actual unforwarded kernel wait export')
        symbol = symbols[0]
        need(0 < symbol.address < pe.OPTIONAL_HEADER.SizeOfImage, 'wait export within kernel image')
        found.append(dict(base=base, symbol='NtWaitForSingleObject', RVA=symbol.address,
            target=base+symbol.address, image_size=pe.OPTIONAL_HEADER.SizeOfImage,
            module=identity(path), enumerated_path=filename.value,
            export_disk_bytes=pe.get_data(symbol.address, 64).hex(),
            method='EnumDeviceDrivers + GetDeviceDriverFileNameW + actual guest PE export',
            live_kernel_code_read=False, kernel_symbol_downloaded=False))
    need(len(found) == 1, 'one current kernel image')
    return found[0]


def utc_now_ns(kernel):
    ticks = C.c_uint64()
    kernel.GetSystemTimePreciseAsFileTime(C.byref(ticks))
    return (ticks.value - 116444736000000000) * 100


def trace_properties(path=None):
    from devtools import terminal_wait_etw_probe as etw
    buf, p = etw.properties(path)
    if path is not None:
        p.EnableFlags = TRACE_FLAGS
    return buf, p


@contextmanager
def owned_frames(c, thread_ids, backend=None):
    """Identity and suspend/context/restore all use the same retained handle.

    A node under construction may still contain a stale thread ID. Never suspend
    by that number before checking the handle's actual owning process/thread.
    """
    if backend is None:
        from devtools import terminal_scene_owner as backend
    original=backend.original; opened=[]; held=[]; frames=[]
    need(len(set(thread_ids))==len(thread_ids) and 0<len(thread_ids)<=2,'bounded distinct owned threads')
    try:
        for tid in thread_ids:
            th=original.opent(0x4A,False,tid)
            original.check(th,'open exact original thread for owned snapshot')
            opened.append(th)
            need(backend.get_thread_pid(th)==c.pid and backend.get_thread_id(th)==tid,
                 'thread handle belongs to the exact current original owner before suspension')
            previous=original.suspend(th)
            need(previous!=0xffffffff,'suspend the verified original thread')
            held.append((th,previous))
            storage=C.create_string_buffer(736);at=(C.addressof(storage)+15)&~15
            C.memset(at,0,716);C.c_uint32.from_address(at).value=0x1003f
            original.check(original.ctx(th,at),'read exact retained original thread context')
            raw=C.string_at(at,716);bp=struct.unpack_from('<I',raw,180)[0];chain=[]
            for _ in range(100):
                link=original.memory(c.h,bp,8)
                if link is None:break
                saved,ret=struct.unpack('<II',link)
                chain.append(dict(bp=bp,saved_bp=saved,return_va=ret))
                if not bp<saved<bp+0x100000:break
                bp=saved
            frames.append(dict(tid=tid,context_hex=raw.hex(),EIP=struct.unpack_from('<I',raw,184)[0],
                EBP=struct.unpack_from('<I',raw,180)[0],ESP=struct.unpack_from('<I',raw,196)[0],
                chain=chain,owner_verified_before_suspend=True,previous_suspend_count=previous))
        yield frames
    finally:
        failures=[]
        for th,previous in reversed(held):
            returned=original.resume(th)
            if returned!=previous+1:failures.append('own suspend increment restore count mismatch')
        for th in reversed(opened):
            if not original.close(th):failures.append('own snapshot handle close failed')
        need(not failures,'; '.join(failures))


def stack_regions(c, frame):
    """Exact small source ranges, including raw frame links and API parameters."""
    ranges = {(r['bp'], r['bp']+8) for r in frame['chain']}
    ranges.add((frame['ESP'], frame['ESP']+128))
    for r in frame['chain']:
        if r['return_va'] == 0x42240D:
            ranges.add((r['bp'], r['bp']+0x10))
            ranges.add((r['saved_bp']-0x60, r['saved_bp']+0x10))
    need(len(ranges) <= 104, 'bounded original frame chain')
    return [dict(pointer=a, hex=c.get(a,b-a).hex()) for a,b in sorted(ranges)]


def startup_candidate(nodes, startup_vtable):
    candidates = [n for n in nodes if struct.unpack_from('<I',bytes.fromhex(n['head_hex']))[0] == startup_vtable]
    need(len(candidates) <= 1, 'no ambiguous original startup owners')
    if not candidates:
        return None
    row = candidates[0]; raw = bytes.fromhex(row['head_hex'])
    values = struct.unpack_from('<III',raw,0x1C)
    if any(x in (0,0xffffffff) for x in values):
        return None
    return row


def await_startup(c, main_tid, result, kernel, seconds=5):
    from devtools import terminal_scene_owner as base, terminal_startup_handoff as startup
    deadline = time.monotonic()+seconds; previous=None
    result['startup_readiness'] = []
    while time.monotonic() < deadline:
        with owned_frames(c,[main_tid]) as frames:
            need(any(f['tid'] == main_tid for f in frames), 'actual scheduler available for readiness')
            manager,nodes = startup.graph(c)
            candidate = startup_candidate(nodes,startup.STARTUP)
            signature = [(n['pointer'],n['head_hex']) for n in nodes]
            if signature != previous:
                need(len(result['startup_readiness']) < 32, 'bounded distinct startup transitions')
                result['startup_readiness'].append(dict(utc_ns=utc_now_ns(kernel),
                    manager_pointer=c.main+0x64,manager_hex=manager.hex(),registered_nodes=nodes))
                previous=signature
        if candidate:
            node=candidate['pointer'];tid=base.word(bytes.fromhex(candidate['head_hex']),0x24)
            if tid != main_tid:
                with owned_frames(c,[tid]) as frames:
                    frame=next((f for f in frames if f['tid']==tid),None)
                    returns={r['return_va']for r in frame['chain']}if frame else set()
                    if {0x421F8A,0x56E183} <= returns:
                        result['startup_readiness_ancestor'] = frame
                        return node,tid
        time.sleep(.010)
    raise ValueError('original startup registration/worker ancestry did not naturally become ready within 5 seconds')


def snapshot(c, main_tid, worker_tid, node, kernel):
    from devtools import terminal_scene_owner as base, terminal_startup_handoff as startup
    # Freeze the scheduler before the worker; neither can publish the next
    # scheduler handshake while the read-only ownership/stack sample is taken.
    with owned_frames(c,[main_tid,worker_tid]) as frames:
        need({x['tid'] for x in frames} == {main_tid,worker_tid}, 'both original scheduler and worker contexts')
        begin = utc_now_ns(kernel)
        frame = next(x for x in frames if x['tid'] == worker_tid)
        manager, nodes = startup.graph(c)
        actual = [x for x in nodes if x['pointer'] == node]
        need(len(actual) == 1, 'same original registered worker during sample')
        head = c.get(node, 0x40)
        need(base.word(head,0x24) == worker_tid and base.word(head,8) == c.main+0x64,
             'current original worker and scheduler owner')
        row = dict(snapshot_begin_ns=begin, node_pointer=node, node_hex=head.hex(),
            manager_pointer=c.main+0x64, manager_hex=manager.hex(), frame=frame,
            scheduler_frame=next(x for x in frames if x['tid'] == main_tid),
            current_TLS=base.capture_tls(c,frame,node), stack_regions=stack_regions(c,frame),
            registered_nodes=nodes, source_memory_written=False, debug_registers_written=False)
        row['snapshot_end_ns'] = utc_now_ns(kernel)
        return row


def run(out):
    from devtools.native_input_isolation import require_qualified_guest
    qualification = require_qualified_guest()  # Before game imports/launch or any tracing API.
    from devtools import terminal_wait_etw_probe as etw, terminal_menu_handoff as menu
    from devtools import terminal_startup_handoff as startup
    from devtools.terminal_scene_resources import clone
    from devtools.isolated_guest_focus import guest_focus_scope, focus_owned_window
    from devtools.isolated_guest_dep_observer import DepObserver
    from tools.school_crt_init_nested import resolve
    import pefile
    base = menu.base
    out = out.resolve()
    need(out.parent == ROOT/'analysis' and out.name.endswith('.json.gz') and not out.exists(),
         'fresh qualified guest source output')
    folder = out.parent/out.name.removesuffix('.json.gz')
    need(not folder.exists(), 'fresh bounded ETL directory')
    folder.mkdir()
    etl = folder/'trace.etl'
    implementations = [identity(Path(__file__)), identity(Path(etw.__file__))]
    kernel_export = kernel_wait_identity()  # Fail before launching game if address identity is unavailable.
    kernel, advapi = etw.bind_windows()
    def observe(pid, owned, progress, duration):
        result = dict(error=None, subject=None, owner_snapshots={}, trace=None,
            host_game_calls=[], host_memory_writes=[], host_input_actions=[],
            source_memory_written=False, general_registers_written=False,
            debug_registers_written=False, debug_object_modified=False,
            debugger_reply_substituted=False, full_instruction_trace=False,
            full_resource_lifetime_proved=False, accepted=False)
        h = None; session = None
        try:
            need(pid in owned.members(), 'original process inside this exclusive Job')
            h = base.original.openp(0x100450, False, pid)
            base.original.check(h, 'read/query/duplicate-only original handle')
            c = SimpleNamespace(pid=pid,h=h,owned=owned,get=lambda p,n:base.original.required(h,p,n))
            c.main = base.word(c.get(0x7A4A00,4))
            hwnd = base.original.findwindow(b'Cross Hermit',None)
            window_pid = C.c_uint32()
            main_tid = base.original.ownerpid(hwnd,C.byref(window_pid))
            need(window_pid.value == pid and main_tid, 'actual original MAIN HWND owner')
            result['guest_activation'] = focus_owned_window(c,hwnd)
            node,tid = await_startup(c,main_tid,result,kernel)
            need(tid != main_tid, 'distinct original scheduler and worker')
            result['subject'] = dict(pid=pid,tid=tid,main_tid=main_tid,main=c.main,node=node)
            raw = base.SOURCE.read_bytes(); need(base.sha(raw) == base.SOURCE_SHA, 'fixed unpacked original image')
            result['original_code'] = []
            for lo,hi in ((0x422360,0x422434),(0x422560,0x4225DA),(0x56CE80,0x56CE98)):
                observed = c.get(lo,hi-lo)
                need(observed == raw[lo-0x400000:hi-0x400000], 'original unmodified wait range')
                result['original_code'].append(dict(pointer=lo,hex=observed.hex()))
            result['API_exports'] = []
            for module,name,slot in (('kernel32.dll','WaitForSingleObject',0x59226C),('ntdll.dll','NtWaitForSingleObject',None)):
                entry = resolve(pid,module,name)
                image = pefile.PE(entry['module_path']).get_memory_mapped_image(ImageBase=entry['base'])
                actual = c.get(entry['target'],64)
                need(actual == image[entry['RVA']:entry['RVA']+64], 'actual relocated x86 OS wait export')
                iat = c.get(slot,4) if slot else None
                need(iat is None or base.word(iat) == entry['target'], 'actual original wait IAT')
                result['API_exports'].append(dict(name=name,slot=slot,IAT_hex=iat.hex()if iat else None,
                    entry_hex=actual.hex(),**entry))
            result['TLS_implementation'] = base.tls_contract(c)
            result['owner_snapshots']['before'] = snapshot(c,main_tid,tid,node,kernel)
            head = bytes.fromhex(result['owner_snapshots']['before']['node_hex'])
            result['event_owners'] = dict(node_event=base.event_identity(c,base.word(head,0x1C)),
                manager_event=base.event_identity(c,base.word(c.get(c.main+0x17C,4))))
            class NativeWaitSession(etw.Session):
                start = clone(etw.Session.start,properties=trace_properties)
            session = NativeWaitSession(advapi,etl)
            session.start()
            result['capture_interval'] = dict(begin_ns=utc_now_ns(kernel))
            # The worker may already be inside a wait when tracing starts.
            # Allow natural handshakes before choosing a sample; an unobserved
            # entry is still rejected by the independent pairing verifier.
            time.sleep(.035)
            # At most 100 ms of sampling and one final natural-resume interval.
            # ETL sequential 4 MiB limit and lost-event checks are never waived.
            deadline = time.monotonic()+.100
            attempts = 0
            while time.monotonic() < deadline:
                row = snapshot(c,main_tid,tid,node,kernel); attempts += 1
                if any(x['return_va'] == 0x42240D for x in row['frame']['chain']):
                    result['owner_snapshots']['observed_wait'] = row
                    break
                time.sleep(.001)
            result['wait_snapshot_attempts'] = attempts
            need('observed_wait' in result['owner_snapshots'], 'actual suspended original wait caller not observed')
            time.sleep(.035)  # Let the original scheduler naturally release the sampled wait.
            result['capture_interval']['end_ns'] = utc_now_ns(kernel)
        except Exception as exc:
            import traceback
            result['error'] = repr(exc); result['traceback'] = traceback.format_exc(limit=8)
        finally:
            if session is not None:
                result['trace'] = session.stop()
                if session.owned:
                    result['trace'] = session.stop()
                if session.owned or result['trace'].get('stop_status') != 0:
                    result['error'] = (result['error'] or '')+'; owned ETW stop unresolved/incomplete'
            if h:
                try:
                    if result['subject']:
                        result['owner_snapshots']['after'] = snapshot(c,main_tid,tid,node,kernel)
                except Exception as exc:
                    result['after_snapshot_error'] = repr(exc)
                    result['error'] = result['error'] or repr(exc)
                base.original.close(h)
        if etl.exists():
            result['ETL'] = identity(etl)
            if not 0 < result['ETL']['bytes'] < ETL_LIMIT:
                result['error'] = (result['error'] or '')+'; complete ETL must be below 4 MiB'
        return result
    with guest_focus_scope(), DepObserver() as dep:
        result = clone(menu.run,continue_menu=observe)(out,30,None,False,0)
    observation = result.pop('probe') or dict(error='original observation callback was not reached')
    result.update(observation)
    result.update(kind='original_worker_ETW_wait',input_isolation=qualification,
        collector_implementations=implementations,kernel_wait_export=kernel_export,
        trace_flags=TRACE_FLAGS,
        actual_process_dep_observations=dep.rows,dep_observer_error=dep.error,
        full_battle_exit_accepted=False,wait_return_proved=False,accepted=False)
    need(implementations == [identity(Path(__file__)),identity(Path(etw.__file__))], 'frozen actual collector implementations')
    need(kernel_export['module'] == identity(Path(kernel_export['module']['path'])), 'actual guest kernel file unchanged')
    return result


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out',type=Path,required=True)
    args = p.parse_args()
    result = run(args.out)
    raw = json.dumps(result,separators=(',',':')).encode()
    need(len(raw) <= 2*1024*1024, 'bounded original wait source')
    with args.out.open('xb') as f:
        f.write(gzip.compress(raw,mtime=0))
    print(json.dumps(dict(error=result['error'],lifecycle_error=result['lifecycle']['error'],
        subject=result.get('subject'),ETL=result.get('ETL'),accepted=False)),flush=True)
    raise SystemExit(1 if result['error'] or result['lifecycle']['error'] else 0)
