"""Bounded no-window qualification of child-only #DB -> VEH -> first read.

This never accepts an arbitrary PID or starts a game. It cannot qualify the
canonical57 state contract or install a handler in the original protected child.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import struct
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'devtools/terminal_wait_child_veh_fixture.cpp'
CONTEXT_SIZE = 716
RECORD_SIZE = 76 + 5 * CONTEXT_SIZE
RECEIPT_SIZE = 280 + 4 * RECORD_SIZE
HEADER = ('magic version bytes context_bytes pid tid gated error rounds handler_calls '
          'handler_removed handles_closed memory_freed peer_signals worker_exit '
          'code_unchanged nt_unchanged code_base consumer nt_wait code_size tls_freed').split()
FIELDS = ('index tid teb tls_index tls_value stack_return stack_event stack_alertable '
          'stack_timeout pre_count post_count status value exception_code exception_address '
          'exception_first_consumer guard_error context_unchanged_except_DR debug_port').split()


def need(value, message):
    if not value:
        raise ValueError(message)


def identity(path):
    path = Path(path)
    raw = path.read_bytes()
    return dict(path=str(path.resolve()), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


def word(raw, offset):
    return struct.unpack_from('<I', raw, offset)[0]


def decode(raw, debugger, gated):
    """Reinterpret fixed binary records; do not trust fixture success booleans alone."""
    need(len(raw) == RECEIPT_SIZE, 'exact bounded v2 receipt')
    h = dict(zip(HEADER, struct.unpack_from('<22I', raw)))
    need((h['magic'], h['version'], h['bytes'], h['context_bytes']) ==
         (0x56454831, 2, RECEIPT_SIZE, 716), 'owned x86 v2 record ABI')
    need(h['gated'] == int(gated) and h['error'] == 0 and h['rounds'] == 4, 'four completed native waits')
    need(h['handler_calls'] == (4 if gated else 0) and h['peer_signals'] == 3,
         'three peer signals and one unsignaled timeout; exact handler count')
    need(h['worker_exit'] == 0 and all(h[k] == 1 for k in (
         'handler_removed', 'handles_closed', 'memory_freed', 'code_unchanged', 'nt_unchanged', 'tls_freed')),
         'normal child cleanup with unchanged code')
    code = raw[88:152][:h['code_size']]
    need(h['code_size'] == 38 and code == raw[152:216][:h['code_size']], 'exact unchanged owned wrapper')
    need(code[:16] == bytes.fromhex('558bec538b5d0cff75106a00ff7508b8') and
         word(code, 16) == h['nt_wait'] and code[20:] == bytes.fromhex('ffd08b13895304894308ff430c5b5dc20c00'),
         'real NtWait call followed immediately by result memory read')
    need(h['consumer'] == h['code_base'] + 22, 'first consumer address')
    nt = raw[216:248]
    need(nt == raw[248:280] and nt[:1] == b'\xb8' and nt[10:15] == bytes.fromhex('ffd2c20c00'),
         'unchanged actual WOW64 NtWait stub')
    need(debugger['child_pid'] == h['pid'] and debugger['exited'] is True and
         debugger['exit_code'] == 0 and debugger['forced'] is False and debugger['handles_closed'] is True and
         debugger['child_signaled'] is True and debugger['continue_error'] == 0 and
         debugger['initial_break'] is True and debugger['ntdll_loaded'] is True,
         'debugger observed normal current child exit')
    creation = [r for r in debugger['events'] if r['type'] == 3]
    initial = [r for r in debugger['events'] if r['type'] == 1 and r['exception'] in (0x80000003, 0x4000001f)]
    need(len(creation) == len(initial) == 1 and initial[0]['tid'] == creation[0]['tid'] and
         initial[0]['first'] == 1 and initial[0]['reply'] == 0x10002 and
         debugger['ntdll_base'] <= initial[0]['address'] < debugger['ntdll_base'] + debugger['ntdll_size'],
         'one current loader breakpoint, never an arbitrary exception override')
    steps = [r for r in debugger['events'] if r['type'] == 1 and r['exception'] in (0x80000004, 0x4000001e)]
    need(len(steps) == (4 if gated else 0) == debugger['single_steps'] and debugger['guards'] == 0,
         'exact child execution exceptions, no page guards')
    need(all(r['pid'] == h['pid'] and r['tid'] == h['tid'] and r['address'] == h['consumer'] and
             r['first'] == 1 and r['reply'] == 0x80010001 for r in steps), 'unaltered first-chance NOT_HANDLED policy')
    need(all(r['pid'] == h['pid'] for r in debugger['events']), 'same debugger child for every event')
    need(sum(r['type'] == 1 for r in debugger['events']) == 1 + len(steps) and
         debugger['unhandled'] == len(steps), 'no hidden or second-chance exception')
    records = []
    for i in range(4):
        start = 280 + i * RECORD_SIZE
        r = dict(zip(FIELDS, struct.unpack_from('<19I', raw, start)))
        ctx = {name: raw[start + 76 + n*716:start + 76 + (n+1)*716]
               for n, name in enumerate(('blocked', 'armed', 'trapped', 'resumed', 'after'))}
        blocked = ctx['blocked']
        need(all(word(ctx[k], 0) & 0x1003f == 0x1003f for k in ('blocked', 'armed', 'after')),
             'requested user-context groups returned')
        need(r['index'] == i and r['tid'] == h['tid'] and r['teb'] >= 0x10000 and
             r['tls_value'] >= 0x10000 and r['debug_port'] == 0xffffffff, 'actual current owner and existing debug port')
        need(word(blocked, 184) == h['nt_wait'] + 12 and r['stack_return'] == h['consumer'] and
             r['stack_event'] != 0 and r['stack_alertable'] == 0 and
             (r['stack_timeout'] != 0) == (i == 3), 'actually pending original nonalertable wait and caller')
        need(not word(blocked, 192) & 0x10100 and not word(blocked, 24) & 255 and
             blocked[4:20] == bytes(16), 'no RF/TF or occupied debug slots at arm')
        need(r['status'] == (258 if i == 3 else 0) and r['value'] == 0x12340000 + i and
             r['post_count'] == 1, 'native return then exactly one real memory consumption')
        need(ctx['after'][4:28] == blocked[4:28], 'actual post-consumption debug state restored')
        armed = ctx['armed']
        need(armed[:4] == blocked[:4] and armed[28:] == blocked[28:], 'arming changes only debug registers')
        if gated:
            need(word(armed, 4) == h['consumer'] and armed[8:20] == blocked[8:20] and
                 word(armed, 20) & 0xe00f == 0 and
                 word(armed, 24) == (word(blocked, 24) & ~0xf0003) | 1,
                 'actual readback of one execution breakpoint')
            trapped, resumed = ctx['trapped'], ctx['resumed']
            need(r['pre_count'] == 0 and r['guard_error'] == 0 and r['context_unchanged_except_DR'] == 1,
                 'held before consumption and bounded ACK')
            need(r['exception_code'] in (0x80000004, 0x4000001e) and
                 r['exception_address'] == r['exception_first_consumer'] == word(trapped, 184) == h['consumer'],
                 'exact fault before first consumer instruction')
            need(word(trapped, 176) == r['status'] and word(trapped, 4) == h['consumer'] and
                 word(trapped, 20) & 0xe00f == 1, 'actual returned EAX and this breakpoint only')
            need(trapped[:4] == resumed[:4] and trapped[28:] == resumed[28:] and
                 resumed[4:28] == blocked[4:28], 'resume preserves all supplied non-DR context including RF')
        else:
            need(armed == blocked, 'uninstrumented control state remains unchanged')
        records.append(dict(index=i, raw_offset=start, thread_id=r['tid'], TEB=r['teb'],
            TLS_index=r['tls_index'], TLS_value=r['tls_value'], native_return=r['status'],
            post_count=r['post_count'], pending_EIP=word(blocked, 184),
            fault_EIP=word(ctx['trapped'], 184) if gated else None,
            exception_EFLAGS=word(ctx['trapped'], 192) if gated else None,
            exception_ContextFlags=word(ctx['trapped'], 0) if gated else None,
            resumed_EFLAGS=word(ctx['resumed'], 192) if gated else None))
    return dict(pid=h['pid'], tid=h['tid'], gated=gated, actual_returns=[r['native_return'] for r in records],
        exact_preconsumer_stops=4 if gated else 0, parent_debug_registers_modified=False,
        supplied_context_unchanged_except_own_DR=True if gated else None,
        RF_modified=False, records=records, code_hex=code.hex(), nt_wait=h['nt_wait'], nt_hex=nt.hex(),
        full57=False, original_game_observed=False, game_acquisition_allowed=False)


def drain_owned_job(owner, maximum_seconds=.5):
    """Record live member identity before bounded natural exit; never change cleanup policy."""
    import ctypes as C
    import ctypes.wintypes as W
    query = owner.w.k.QueryFullProcessImageNameW
    query.argtypes = [W.HANDLE, W.DWORD, W.LPWSTR, C.POINTER(W.DWORD)]
    query.restype = W.BOOL
    rows = []; seen = set(); deadline = time.perf_counter() + maximum_seconds
    while True:
        members = owner.ids()
        for pid in members:
            if pid in seen:
                continue
            seen.add(pid); row = dict(pid=pid, image=None, query_error=None)
            h = owner.w.openp(0x1000, False, pid)
            if h:
                try:
                    buf = C.create_unicode_buffer(32768); n = W.DWORD(len(buf))
                    if query(h, 0, buf, C.byref(n)):
                        row['image'] = buf.value
                    else:
                        row['query_error'] = C.get_last_error()
                finally:
                    owner.w.check(owner.w.close(h), 'close owned Job member image query')
            else:
                row['query_error'] = C.get_last_error()
            rows.append(row)
        if not members or time.perf_counter() >= deadline:
            return dict(observed_members=rows, final_members=members, maximum_seconds=maximum_seconds)
        time.sleep(.01)


def execute(folder, out):
    from devtools.terminal_oplock_probe import Owned
    from devtools.terminal_host_desktop import snapshot, differences, health
    need(folder.is_relative_to(ROOT / '.venv-audit') and not folder.exists(), 'fresh F-drive fixture folder')
    need(out.parent == ROOT / 'analysis' and not out.exists(), 'fresh bounded analysis report')
    deps = [SOURCE, Path(__file__), ROOT/'devtools/terminal_oplock_probe.py',
            ROOT/'devtools/terminal_oplock.py', ROOT/'devtools/terminal_host_desktop.py']
    before = [identity(p) for p in deps]
    folder.mkdir(); (folder/'tmp').mkdir()
    report = dict(kind='owned_child_only_execution_breakpoint_VEH_preflight', accepted=False,
        implementations=before, cases=[], error=None, game_started=False, screenshots=False,
        host_input=False, full57=False, game_acquisition_allowed=False, backups_created=0)
    start = time.perf_counter()
    report['desktop_before'] = snapshot()
    try:
        need(not health(report['desktop_before']), 'healthy read-only desktop baseline')
        vcvars = Path('C:/Program Files/Microsoft Visual Studio/2022/Community/VC/Auxiliary/Build/vcvarsall.bat')
        compiler = Path('C:/Program Files/Microsoft Visual Studio/2022/Community/VC/Tools/MSVC/14.44.35207/bin/Hostx64/x86/cl.exe')
        exe = folder/'wait-child-veh.exe'
        report['compiler'] = identity(compiler)
        # Fixed, quoted compiler setup; all outputs/TEMP are in this owned folder.
        need(not any(c in str(folder) for c in '&|<>%!\r\n"'), 'literal build path without command expansion')
        recipe = ('@echo off\r\ncall "'+str(vcvars)+'" x86 -vcvars_ver=14.44 >nul\r\n'
                  'if errorlevel 1 exit /b %errorlevel%\r\n"'+str(compiler)+
                  '" /nologo /O2 /W4 /MT /EHsc /Fe:"'+str(exe)+'" /Fo:"'+str(folder/'fixture.obj')+
                  '" "'+str(SOURCE)+'" /link /SUBSYSTEM:WINDOWS /ENTRY:wmainCRTStartup\r\nexit /b %errorlevel%\r\n')
        (folder/'build.cmd').write_bytes(recipe.encode('ascii'))
        cmd = ['cmd.exe', '/d', '/c', 'build.cmd']
        build = subprocess.run(cmd, cwd=folder,
            env=dict(os.environ, TEMP=str(folder/'tmp'), TMP=str(folder/'tmp')), capture_output=True,
            timeout=30, creationflags=0x08000000)
        report['build'] = dict(returncode=build.returncode, stdout=build.stdout.decode(errors='replace')[:16000],
                               stderr=build.stderr.decode(errors='replace')[:16000], command=cmd)
        need(build.returncode == 0, 'bounded x86 native build')
        import pefile
        executable = pefile.PE(str(exe))
        need(executable.FILE_HEADER.Machine == 0x14c and executable.OPTIONAL_HEADER.Subsystem == 2,
             'x86 non-console image before any execution')
        report['binary'] = identity(exe)
        for name, gated in (('baseline', False), ('gated', True)):
            case_folder = folder/name; case_folder.mkdir()
            if gated:
                (case_folder/'gated').write_bytes(b'1')
            owner = None
            case = dict(name=name, error=None)
            report['cases'].append(case)
            try:
                owner = Owned(exe, case_folder)
                need(owner.wait(20000) == 0, 'native parent ended within 20 seconds')
                case['natural_job_drain'] = drain_owned_job(owner)
            finally:
                if owner:
                    case['owner'] = owner.finish()
            need(case['owner']['job_empty'] and case['owner']['handles_closed'] and
                 not case['owner']['forced'] and not case['owner']['errors'] and
                 case['owner']['exits'][str(case['owner']['parent_pid'])]['code'] == 0,
                 'own parent exit0, Job and handles clean')
            debugger_path = case_folder/'debugger.json'; binary_path = case_folder/'child.bin'
            need(debugger_path.stat().st_size < 32768 and binary_path.stat().st_size == RECEIPT_SIZE,
                 'bounded source files')
            debugger = json.loads(debugger_path.read_text())
            need(debugger['pid'] == case['owner']['parent_pid'], 'same owned debugger parent')
            case['sources'] = [identity(binary_path), identity(debugger_path)]
            case['verification'] = decode(binary_path.read_bytes(), debugger, gated)
            import pefile
            dll = Path('C:/Windows/SysWOW64/ntdll.dll')
            pe = pefile.PE(str(dll))
            export = next(x for x in pe.DIRECTORY_ENTRY_EXPORT.symbols if x.name == b'NtWaitForSingleObject')
            base = case['verification']['nt_wait'] - export.address
            need(debugger['ntdll_base'] == base and debugger['ntdll_size'] == pe.OPTIONAL_HEADER.SizeOfImage,
                 'same actual host ntdll mapping for loader exception and native wait')
            actual = pe.get_memory_mapped_image(ImageBase=base)[export.address:export.address+32]
            need(actual.hex() == case['verification']['nt_hex'], 'live original NtWait equals relocated actual host DLL')
            case['native_wait_source'] = dict(file=identity(dll), base=base, RVA=export.address,
                                              live_entry_matches_relocated_file=True)
        report['synchronous_entry_preflight_passed'] = True
    except Exception as exc:
        report['error'] = repr(exc)
        report['synchronous_entry_preflight_passed'] = False
    finally:
        report['desktop_after'] = [snapshot()]; time.sleep(.25); report['desktop_after'].append(snapshot())
        report['desktop_differences'] = [differences(report['desktop_before'], r) for r in report['desktop_after']]
        report['implementations_unchanged'] = before == [identity(p) for p in deps]
        if report['desktop_differences'] != [[], []] or not report['implementations_unchanged']:
            report['error'] = report['error'] or 'desktop or frozen implementation mismatch'
            report['synchronous_entry_preflight_passed'] = False
        report['elapsed_seconds'] = time.perf_counter() - start
        report['retained_files'] = [identity(p) for p in sorted(folder.rglob('*')) if p.is_file()]
        need(sum(r['bytes'] for r in report['retained_files']) < 8*1024*1024, 'bounded native evidence')
        with out.open('x', encoding='utf8', newline='\n') as stream:
            json.dump(report, stream, ensure_ascii=False, indent=2)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute', action='store_true')
    parser.add_argument('--folder', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    if not args.execute:
        print(json.dumps(dict(plan='owned baseline then child-only DR/VEH; no game/UI/input',
            build_timeout_seconds=30, per_case_parent_timeout_seconds=20, full57=False)))
        return
    report = execute(args.folder.resolve(), args.out.resolve())
    print(json.dumps(dict(error=report['error'], synchronous_entry=report['synchronous_entry_preflight_passed'],
                         full57=False, game_acquisition_allowed=False, report=identity(args.out))))
    if report['error']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
