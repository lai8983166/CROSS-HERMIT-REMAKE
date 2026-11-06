"""Bounded actual scene/CRT/TLS/event ownership and native retreat observation.

Only three sourced initializer/scenario/event roots write via original code.
All host process writes are restricted to fresh call-bridge buffers. Inputs are
performed separately through Computer Use, never by writing game input/result.
This native observation is not the frozen terminal fixture's full replay.
"""
from __future__ import annotations
import argparse
import ctypes as C
import ctypes.wintypes as W
import gzip
import hashlib
import json
from pathlib import Path
import struct
import time
import traceback
import types

from tools import school_native_scene as native
from tools.school_native_dialogue import VisibleOwnedRuntime
from tools.school_native_dialogue_desktop import require_unlocked
from tools.school_crt_init_nested import resolve
from devtools.native_observer_guard import require_idle

ROOT = native.ROOT
original, parent = native.original, native.parent
SOURCE_SHA = native.SOURCE_SHA
SOURCE = native.SOURCE
RANGES = native.RANGES + ((0x422360,0x422434),(0x422560,0x42260A),
    (0x56E050,0x56E225),(0x5753B0,0x57555B),(0x458580,0x458929),
    (0x453D00,0x453E5D),(0x451670,0x4519A3),(0x4967B0,0x4968A9),
    (0x45E8D0,0x45EA50),(0x60CB18,0x60CB28))
IAT = tuple(dict.fromkeys(native.IAT+(0x59221C,0x5921A8,0x5921AC,0x5921A4)))


def need(value, message):
    if not value:
        raise ValueError(message)


def word(raw, offset=0):
    return struct.unpack_from('<I', raw, offset)[0]


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def identity(path):
    path = Path(path)
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(1024*1024), b''):
            h.update(block)
    return dict(path=path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path),
                bytes=path.stat().st_size, sha256=h.hexdigest())


class Calls(native.previous.SceneCalls):
    def __init__(self, pid, owned, scenario):
        need(scenario == 4, 'explicit original T0004 scenario only')
        self.scene = scenario
        super().__init__(pid, owned)
        image = C.create_unicode_buffer(32768)
        size = W.DWORD(len(image))
        original.check(native.image_name(self.h,0,image,C.byref(size)), 'actual owned image path')
        need(Path(image.value).resolve() == native.APP.resolve(), 'private original runtime only')
        self.process_image = image.value
        self.standard_code = self.code
        self.cdecl_code = self.reserve(4096)
        self.put(self.cdecl_code, native.cdecl_thunk())
        old = W.DWORD()
        original.check(parent.protect(self.h,self.cdecl_code,4096,0x20,C.byref(old)), 'private bridge RX')
        original.check(parent.flush(self.h,self.cdecl_code,len(native.cdecl_thunk())), 'private bridge instruction cache')
        self.main = word(self.get(0x7A4A00,4))
        need(self.main and word(self.get(self.main,4)) == 0x5986A0, 'actual original MAIN')
        self.phase = 0
        self.scene_construction_authorized = False

    def validate(self, va, receiver, args):
        need(self.pid in self.owned.members(), 'exclusively owned original process')
        need(self.scene_construction_authorized,
             'scene construction requires an empty original scheduler preflight')
        protocol = ((0x4E1B60,0,()),(0x4DA860,0,(4,)),(0x439E30,self.main+0x10,(16,)))
        need(self.phase < len(protocol) and (va,receiver,args) == protocol[self.phase],
             'only initializer, scenario4 and MAIN scene event roots')

    def call(self, va, receiver, args=(), slot=0):
        self.code = self.cdecl_code if va == 0x4DA860 else self.standard_code
        row = super().call(va, receiver, args, slot)
        self.phase += 1
        return row


selector_entry = original.bind('Wow64GetThreadSelectorEntry', W.BOOL, [W.HANDLE,W.DWORD,C.c_void_p])
get_thread_id = original.bind('GetThreadId', W.DWORD, [W.HANDLE])
get_thread_pid = original.bind('GetProcessIdOfThread', W.DWORD, [W.HANDLE])
ntdll = C.WinDLL('ntdll')
query_object = ntdll.NtQueryObject
query_object.restype = C.c_long
query_object.argtypes = [W.HANDLE,C.c_int,C.c_void_p,W.ULONG,C.POINTER(W.ULONG)]


def parse_selector(raw):
    need(len(raw) == 8, 'complete WOW64_LDT_ENTRY')
    return struct.unpack_from('<H',raw,2)[0] | raw[4]<<16 | raw[7]<<24


def validate_tls(teb, head, slot_index, ptd_pointer, ptd, pid, tid, node):
    need(len(head) == 0x40 and word(head,0x18) == teb, 'TEB self pointer')
    need(word(head,0x20) == pid and word(head,0x24) == tid, 'TEB current process/thread identity')
    need(word(head,8) < word(head,4) and 0 <= slot_index < 1088, 'TEB stack and bounded TLS index')
    need(ptd_pointer != 0 and len(ptd) == 116, 'complete current CRT PTD')
    need(word(ptd) == tid and word(ptd,0x48) == 0x421F50 and word(ptd,0x4C) == node,
         'actual worker TLS belongs to original421F50 and this scene')


def event_identity(c, handle):
    need(handle not in (0,0xFFFFFFFF), 'non-null current event handle')
    local = W.HANDLE()
    original.check(parent.duplicate(c.h,handle,parent.current_process(),C.byref(local),0,False,2),
                   'duplicate current own event for non-consuming query')
    try:
        buffer = C.create_string_buffer(2048)
        used = W.ULONG()
        status = query_object(local,2,buffer,len(buffer),C.byref(used))
        need(status == 0, 'successful actual ObjectTypeInformation')
        length = struct.unpack_from('<H',buffer.raw)[0]
        pointer = C.c_void_p.from_buffer(buffer,8).value
        need(length == 10 and pointer is not None and C.addressof(buffer) <= pointer
             and pointer+length <= C.addressof(buffer)+len(buffer), 'bounded Event type name')
        name = C.string_at(pointer,length).decode('utf-16le')
        need(name == 'Event', 'actual handle is a Windows Event')
        return dict(remote_handle=handle,owner_pid=c.pid,duplicate_succeeded=True,
                    query_status=status,type_name=name,wait_or_signal_called=False)
    finally:
        original.close(local)


def tls_contract(c):
    import pefile
    from capstone import Cs, CS_ARCH_X86, CS_MODE_32
    entry = resolve(c.pid,'kernelbase.dll','TlsGetValue')
    pe = pefile.PE(entry['module_path'])
    raw = pe.get_memory_mapped_image()[entry['RVA']:entry['RVA']+64]
    need(c.get(entry['target'],64) == raw, 'actual current native TlsGetValue code')
    instructions = [(i.mnemonic,i.op_str) for i in Cs(CS_ARCH_X86,CS_MODE_32).disasm(raw,entry['target'])]
    need(any('fs:[0x18]' in op for _,op in instructions)
         and any('0xe10]' in op for _,op in instructions)
         and any('0xf94]' in op for _,op in instructions),
         'current original system implementation independently exposes TEB/TLS offsets')
    return dict(**entry, code_hex=raw.hex(), instructions=instructions,
                fixed_slots_offset=0xE10, expansion_pointer_offset=0xF94,
                method='actual WOW64 FS selector plus verified current TlsGetValue implementation')


def capture_tls(c, frame, node):
    tid = frame['tid']
    th = original.opent(0x48,False,tid)
    original.check(th,'query actual worker selector')
    try:
        need(get_thread_pid(th) == c.pid and get_thread_id(th) == tid, 'queried worker belongs to current process')
        context = bytes.fromhex(frame['context_hex'])
        selector = word(context,144)
        descriptor = C.create_string_buffer(8)
        original.check(selector_entry(th,selector,descriptor),'current WOW64 FS selector')
        teb = parse_selector(descriptor.raw)
        head = c.get(teb,0x40)
        index = word(c.get(0x761BC0,4))
        need(index < 1088, 'bounded actual CRT TLS index')
        expansion = None
        if index < 64:
            slot = teb+0xE10+index*4
        else:
            expansion = word(c.get(teb+0xF94,4))
            need(expansion != 0, 'current TLS expansion array')
            slot = expansion+(index-64)*4
        ptd_pointer = word(c.get(slot,4))
        ptd = c.get(ptd_pointer,116)
        validate_tls(teb,head,index,ptd_pointer,ptd,c.pid,tid,node)
        need(word(head,8) <= frame['ESP'] < word(head,4), 'sampled ESP in same worker TEB stack')
        worker = next(r for r in frame['chain'] if r['return_va'] == 0x56E183)
        callback = next(r for r in frame['chain'] if r['return_va'] == 0x421F8A)
        ancestry_addresses = dict(worker_argument=worker['bp']+8,
            wrapper_argument=worker['saved_bp']+8,callback_this=callback['bp']-4,
            callback_argument=callback['bp']+8,node_argument=node+0x18)
        ancestry_memory = {name:dict(pointer=p,hex=c.get(p,4).hex())
                           for name,p in ancestry_addresses.items()}
        ancestry = {name:word(bytes.fromhex(row['hex'])) for name,row in ancestry_memory.items()}
        need(ancestry['worker_argument'] == ancestry['callback_this'] == node
             and ancestry['wrapper_argument'] == ptd_pointer
             and ancestry['callback_argument'] == ancestry['node_argument'],
             'actual CRT wrapper, worker, callback and current TLS are one lifetime')
        return dict(owner_pid=c.pid,thread_id=tid,FS=selector,selector_hex=descriptor.raw.hex(),
                    TEB=teb,TEB_head_hex=head.hex(),TLS_index=index,expansion_pointer=expansion,
                    slot=slot,TLS_slot_hex=c.get(slot,4).hex(),PTD=ptd_pointer,PTD_hex=ptd.hex(),
                    ancestry=ancestry,ancestry_memory=ancestry_memory)
    finally:
        original.close(th)


def source_identity(c):
    raw = SOURCE.read_bytes()
    need(sha(raw) == SOURCE_SHA,'original executable source identity')
    ranges = []
    for a,b in RANGES:
        data = c.get(a,b-a)
        need(data == raw[a-0x400000:b-0x400000], 'unchanged actual original code '+hex(a))
        ranges.append(dict(pointer=a,bytes=b-a,sha256=sha(data)))
    return dict(code=ranges,IAT=[dict(slot=p,hex=c.get(p,4).hex()) for p in IAT])


def bounded_sample(c, owned, hwnd, main_tid, worker_tid, node, worker_exited=False):
    tids = [main_tid]+([worker_tid] if worker_tid else [])
    with original.frozen(c.h,c.pid,tids) as frames:
        current = word(c.get(0x7A4174,4))
        sample = dict(elapsed=owned.elapsed(),scene_global=current,frames=frames,
            MAIN_event_hex=c.get(c.main+0x2C,8).hex(),manager_hex=c.get(c.main+0x64,0x120).hex(),
            scenario_hex=c.get(0x7F4488,80).hex(),VM_hex=c.get(native.VM,128).hex(),
            game_exit_flag_hex=c.get(0x5FF720,4).hex())
        manager = bytes.fromhex(sample['manager_hex'])
        registered = []
        seen = set()
        for bucket in range(32):
            pointer = word(manager,bucket*8)
            while pointer:
                need(pointer not in seen and len(seen)<128,'bounded original scheduler graph')
                seen.add(pointer)
                h = c.get(pointer,48)
                registered.append(dict(pointer=pointer,bucket=bucket,head_hex=h.hex()))
                pointer = word(h,12)
        sample['registered_tasks'] = registered
        sample['successor_global'] = word(c.get(0x7A49C8,4))
        sample['scene_registered'] = current in seen
        sample['worker_exited'] = worker_exited
        if current and current in seen and not worker_exited:
            need(not node or current == node, 'same current scene lifetime')
            head = c.get(current,0x200)
            sample['scene_head_hex'] = head.hex()
            need(word(head) == 0x59A430 and word(head,8) == c.main+0x64,
                 'original derived vtable and actual MAIN scheduler')
            sample['controller_task_backpointer'] = word(c.get(current+0x190+0x117C38,4))
            worker = next((f for f in frames if f['tid'] == word(head,0x24)),None)
            returns = [r['return_va'] for r in worker['chain']] if worker else []
            if worker and 0x421F8A in returns and 0x56E183 in returns:
                sample['TLS'] = capture_tls(c,worker,current)
                sample['worker_stack_pointer'] = worker['ESP']
                sample['worker_stack_hex'] = c.get(worker['ESP'],min(128,word(bytes.fromhex(sample['TLS']['TEB_head_hex']),4)-worker['ESP'])).hex()
            # Preserve exact currently generated input, not OS injection guesses.
            game = word(c.get(0x7A49FC,4))
            sample['input'] = dict(game=game,keyboard_edges_hex=c.get(game+0x10B8+0x580,256).hex(),
                                   mouse_pointer=game+0x196C,mouse_hex=c.get(game+0x196C,0x58).hex())
        return sample


def construction_preflight(c):
    """Reject overlapping native owners before initializer/event/input effects.

    Empty scheduler state is necessary, not proof of a natural prior retirement.
    All existing threads are paused for this read; no original task is killed,
    unregistered, masked or resumed through an injected scheduler operation.
    """
    from devtools.terminal_scene_transition_contract import require_empty_scene_preflight
    row=dict(pid=c.pid,main=c.main,all_existing_threads_paused=True,
             original_scene_roots_called=False,authorized=False,error=None)
    try:
        need(c.pid in c.owned.members(),'preflight current process belongs to Job')
        with original.frozen(c.h,c.pid) as frames:
            row['frames']=frames
            row['main_global_hex']=c.get(0x7A4A00,4).hex()
            row['main_vtable_hex']=c.get(c.main,4).hex()
            need(word(bytes.fromhex(row['main_global_hex']))==c.main
                 and word(bytes.fromhex(row['main_vtable_hex']))==0x5986A0,'actual MAIN identity')
            row['manager_hex']=c.get(c.main+0x64,0x120).hex()
            row['MAIN_event_hex']=c.get(c.main+0x2C,8).hex()
            manager=bytes.fromhex(row['manager_hex']);rows=[];seen=set()
            for bucket in range(32):
                pointer=word(manager,bucket*8)
                while pointer:
                    need(pointer not in seen and len(seen)<128,'bounded complete preflight graph')
                    seen.add(pointer);head=c.get(pointer,48)
                    rows.append(dict(pointer=pointer,bucket=bucket,head_hex=head.hex()))
                    pointer=word(head,12)
            row['registered_tasks']=rows
            row['check']=require_empty_scene_preflight(row['manager_hex'],row['MAIN_event_hex'],rows)
            game=word(c.get(0x7A49FC,4));need(game,'actual original game owner')
            renderer=c.get(game+0x1058,56)
            count,table=word(renderer,8),word(renderer,16)
            need(count==4096 and 0x10000<=table<=0xFFFFFFFF-count*8,
                 'bounded original renderer bucket table')
            queue=c.get(table,count*8)
            row['renderer']=dict(pointer=game+0x1058,head_hex=renderer.hex(),
                                 table_pointer=table,table_hex=queue.hex())
            need(queue==bytes(count*8),'all renderer queues must be drained before new scene')
            row['resource_group90_hex']=c.get(game+0xB14,8).hex()
            need(row['resource_group90_hex']=='00'*8,'no prior scene/menu group90 owner')
            # An empty snapshot can be taken between unlink and destruction.
            # It is not a natural handoff certificate, and resuming the threads
            # would otherwise race the subsequent three roots. Until that
            # original handoff is implemented, this entry remains fail-closed.
            raise ValueError('empty snapshot is insufficient: natural retirement and atomic scene handoff are not proved')
    except Exception as exc:
        row['error']=repr(exc)
    return row


def run_probe(pid, owned, progress, duration):
    c = None
    report = dict(scenario=4,pid=pid,samples=[],
        original_scene_constructor_and_factory=False,source_code_IAT_or_general_registers_written=False,
        old_terminal_fixture_loaded=False,full_instruction_trace=False,wait_API_return_status_sampled=False,
        native_retreat_observed=False,error=None)
    worker_local = None
    try:
        c = Calls.__new__(Calls)
        c.__init__(pid,owned,4)
        report.update(main=c.main,process_image=c.process_image,
                      source_before=source_identity(c),TLS_implementation=tls_contract(c))
        need(word(c.get(0x7A4174,4)) == 0,'fresh unpublished original scene')
        # Startup may still consume its first menu event; observe it becoming idle.
        deadline = time.monotonic()+5
        while word(c.get(c.main+0x2C,4)) and time.monotonic()<deadline:
            time.sleep(.01)
        need(word(c.get(c.main+0x2C,4)) == 0,'original MAIN event idle')
        report['construction_preflight']=construction_preflight(c)
        if not report['construction_preflight']['authorized']:
            report['stop_reason']='unsafe_native_scene_construction_rejected'
            report['source_after']=source_identity(c)
            raise ValueError(report['construction_preflight']['error'])
        c.scene_construction_authorized=True
        c.call(0x4E1B60,0)
        report['scenario_before_hex'] = c.get(0x7F4488,80).hex()
        c.call(0x4DA860,0,(4,))
        report['scenario_selected_hex'] = c.get(0x7F4488,80).hex()
        c.call(0x439E30,c.main+0x10,(16,))
        hwnd = original.findwindow(b'Cross Hermit',None)
        wp = W.DWORD()
        main_tid = original.ownerpid(hwnd,C.byref(wp))
        need(wp.value == pid and pid in owned.members(),'only own original window')
        report['window'] = dict(hwnd=hwnd,pid=pid,main_tid=main_tid)
        deadline = time.monotonic()+duration
        node = tid = None
        last_signature = None
        last_saved = last_progress = 0
        tail_observed = retreat_observed = False
        milestones = set()
        while time.monotonic()<deadline:
            current = word(c.get(0x7A4174,4))
            if current and not node:
                head = c.get(current,48)
                if word(head,4)&1 and word(head,0x20) and word(head,0x24):
                    node,tid = current,word(head,0x24)
                    worker_local = W.HANDLE()
                    original.check(parent.duplicate(c.h,word(head,0x20),parent.current_process(),C.byref(worker_local),0,False,2),'actual scene worker reference')
                    need(get_thread_pid(worker_local) == pid and get_thread_id(worker_local) == tid,
                         'actual worker native process/thread identity')
                    manager_event = word(c.get(c.main+0x64+0x118,4))
                    report['worker'] = dict(node=node,thread_id=tid,remote_handle=word(head,0x20),
                        manager_event=event_identity(c,manager_event),node_event=event_identity(c,word(head,0x1C)))
                    report['derived_object_initial'] = dict(pointer=node,bytes=native.SIZE,
                        hex=c.get(node,native.SIZE).hex())
                    report['original_scene_constructor_and_factory'] = True
            exited = bool(worker_local and original.wait(worker_local,0) == 0)
            sample = bounded_sample(c,owned,hwnd,main_tid,None if exited else tid,node,exited)
            now = time.monotonic()
            head = bytes.fromhex(sample.get('scene_head_hex',''))
            returns = [r['return_va'] for f in sample['frames'] if f['tid'] == tid for r in f['chain']]
            if head:
                retreat_observed |= head[0x31] == 1
            tail_observed |= 0x451758 in returns or 0x451796 in returns
            milestones.update(set(returns)&{0x4516D5,0x453CB5,0x453CD3,0x453CDD,0x451758,0x451796})
            vm = bytes.fromhex(sample['VM_hex'])
            signature = (sample['scene_global'],head[0x30:0x3C],head[0x43:0x45],head[0x59:0x5A],
                         vm[28:32],sample['MAIN_event_hex'],tuple(sorted(milestones)),tail_observed,'TLS' in sample)
            if signature != last_signature or now-last_saved >= .5:
                if len(report['samples']) >= 1600:
                    report['stop_reason'] = 'bounded_observation_budget'
                    break
                sample['index'] = len(report['samples'])
                report['samples'].append(sample)
                last_signature,last_saved = signature,now
            if now-last_progress >= .5:
                state = dict(status='observing',pid=pid,hwnd=hwnd,node=node,worker_tid=tid,
                    scene_state=word(head,0x34) if head else None,scene_selector=word(head,0x38) if head else None,
                    menu_state=head[0x30] if head else None,retreat_flag=head[0x31] if head else None,
                    script_running=bool(head and head[0x43] and head[0x59]),VM_PC=word(vm,28),
                    VM_wait=struct.unpack_from('<H',vm,32)[0],tail_observed=tail_observed,
                    samples=len(report['samples']),elapsed=owned.elapsed())
                progress.write_text(json.dumps(state),encoding='utf8')
                last_progress = now
            if exited:
                code = W.DWORD()
                original.check(parent.exit_thread(worker_local,C.byref(code)),'actual exited original worker')
                report['worker_exit'] = dict(thread_id=tid,exit_code=code.value,wait_status=0,
                    before_WM_CLOSE=True,retreat_flag_observed=retreat_observed,tail_wait_observed=tail_observed)
                # Allow original MAIN to consume its published successor event.
                until = time.monotonic()+3
                while time.monotonic()<until:
                    sample = bounded_sample(c,owned,hwnd,main_tid,None,node,True)
                    sample['index'] = len(report['samples'])
                    report['samples'].append(sample)
                    successor = next((r for r in sample['registered_tasks']
                        if r['pointer'] == sample['successor_global']
                        and word(bytes.fromhex(r['head_hex'])) == 0x59B060),None)
                    consumed = bool(successor and not sample['scene_registered']
                                    and word(bytes.fromhex(sample['MAIN_event_hex'])) == 0)
                    if consumed:
                        report['successor'] = successor
                        break
                    time.sleep(.02)
                report['native_retreat_observed'] = bool(code.value == 0 and retreat_observed and tail_observed
                    and consumed)
                break
            time.sleep(.01)
        need(node and any('TLS' in s for s in report['samples']),'actual derived scene worker/TLS captured')
        report['source_after'] = source_identity(c)
        need(report['source_after'] == report['source_before'],'original code/IAT unchanged throughout')
        report['reached_deadline'] = time.monotonic() >= deadline
        report.setdefault('stop_reason','time_budget' if report['reached_deadline'] else 'worker_exit')
    except BaseException as exc:
        report['error'] = repr(exc)
        report['error_traceback'] = traceback.format_exc(limit=8)
    finally:
        if worker_local:
            original.close(worker_local)
        if c:
            report.update(calls=getattr(c,'calls',[]),host_private_writes=getattr(c,'writes',[]))
            try:
                if hasattr(c,'blocks'):
                    report['private_frees'] = c.close()
                elif getattr(c,'h',None):
                    original.close(c.h)
            except BaseException as exc:
                report['cleanup_error'] = repr(exc)
        report['full_battle_exit_accepted'] = False
    return report


def run(output, duration):
    require_idle()
    desktop = require_unlocked()
    need(sha(SOURCE.read_bytes()) == SOURCE_SHA,'fixed original source')
    # Reuse the separate runtime; retain mutable bytes in RAM and restore only
    # after its exclusively owned process tree has ended. No new full asset copy.
    runtime = native.runtime_audit()
    mutable = {native.APP.parent/r['path']:(native.APP.parent/r['path']).read_bytes()
               for r in runtime['private_writable_files']}
    owners,probes = [],[]
    progress = Path(str(output)+'.progress.json')
    need(not progress.exists(),'fresh progress output')
    def own():
        o = VisibleOwnedRuntime()
        owners.append(o)
        return o
    def post(hwnd,msg,w,l):
        need(msg == 16 and len(owners) == 1 and not probes,'single owned scene probe before WM_CLOSE')
        pid = W.DWORD()
        original.ownerpid(hwnd,C.byref(pid))
        need(pid.value in owners[0].members(),'own actual window lifetime')
        probes.append(run_probe(pid.value,owners[0],progress,duration))
        return original.post(hwnd,msg,w,l)
    observe = types.FunctionType(original.observe.__code__,
        dict(original.observe.__globals__,OwnedOriginal=own,post=post),
        'actual_same_owner_scene_probe',original.observe.__defaults__)
    started = time.monotonic()
    lifecycle = observe(False)
    restored = []
    need(not lifecycle['lifetime']['members_after_cleanup'],'owned process tree ended before mutable-file comparison')
    for path,before in mutable.items():
        after = path.read_bytes()
        if after != before:
            need(path.resolve().is_relative_to(native.APP.parent.resolve()),'private runtime mutable path only')
            path.write_bytes(before)
        restored.append(dict(path=path.relative_to(ROOT).as_posix(),bytes=len(before),sha256=sha(before),
                             changed_during_probe=after != before,restored_exact=path.read_bytes() == before))
    progress.write_text(json.dumps(dict(status='closed',owned_job_empty=True,
        probe_error=(probes[0] if probes else {}).get('error'),lifecycle_error=lifecycle['error'])),encoding='utf8')
    return dict(schema_version=1,accepted=False,kind='actual_same_owner_scene_and_retreat_observation',
        observer=identity(Path(__file__)),original=identity(SOURCE),desktop=desktop,runtime=runtime,
        mutable_private_runtime_files=restored,lifecycle=lifecycle,probe=probes[0] if probes else None,
        duration_seconds=round(time.monotonic()-started,3),old_terminal_cases_replayed=False,
        full_native_instruction_or_API_trace=False,independent_full_replay=False,
        R3_complete=False,R4_complete=False,R5_complete=False,R6_complete=False)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out',required=True)
    p.add_argument('--seconds',type=int,default=180)
    a = p.parse_args()
    out = Path(a.out).resolve()
    need(out.is_relative_to(ROOT/'analysis') and not out.exists(),'fresh local immutable output')
    need(30 <= a.seconds <= 600,'bounded30..600-second scene observation')
    result = run(out,a.seconds)
    raw = json.dumps(result,separators=(',',':')).encode()
    need(len(raw) <= 32*1024*1024,'bounded source before persistence')
    packed = gzip.compress(raw,mtime=0)
    need(len(packed) <= 8*1024*1024,'bounded compressed evidence')
    with out.open('xb') as stream:
        stream.write(packed)
    print(json.dumps(dict(report=identity(out),lifecycle_error=result['lifecycle']['error'],
        probe_error=(result['probe'] or {}).get('error'),retreat=(result['probe'] or {}).get('native_retreat_observed'))),flush=True)
    if result['lifecycle']['error'] or not result['probe'] or result['probe']['error']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
