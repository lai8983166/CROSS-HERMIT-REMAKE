"""Bounded guest-only hardware observations through the original debug parent.

The child is already debugged by its original protection parent. Attach only to
that owned parent, observe its NtDebugContinue call, and leave its reply intact.
Only debug registers are instrumented; no game memory or general registers.
"""
import ctypes as C
import ctypes.wintypes as W
import struct
import time
import traceback

from tools import school_crt_init_capture as debug
from tools.school_crt_init_nested import instrument, resolve

win = debug.win
need = debug.need
word = debug.word
detach = win.bind('DebugActiveProcessStop', W.BOOL, [W.DWORD])
kill_on_exit = win.bind('DebugSetProcessKillOnExit', W.BOOL, [W.BOOL])
get_thread_id = win.bind('GetThreadId', W.DWORD, [W.HANDLE])
get_process_id = win.bind('GetProcessId', W.DWORD, [W.HANDLE])
current_process = win.bind('GetCurrentProcess', W.HANDLE, [])
duplicate = win.bind('DuplicateHandle', W.BOOL,
    [W.HANDLE,W.HANDLE,W.HANDLE,C.POINTER(W.HANDLE),W.DWORD,W.BOOL,W.DWORD])
class MEMORY(C.Structure):
    _fields_=[('base',C.c_void_p),('allocation',C.c_void_p),('allocation_protect',W.DWORD),
              ('partition',W.WORD),('size',C.c_size_t),('state',W.DWORD),('protect',W.DWORD),('type',W.DWORD)]
query_memory=win.bind('VirtualQueryEx',C.c_size_t,[W.HANDLE,C.c_void_p,C.POINTER(MEMORY),C.c_size_t])


def own_duplicate(handle):
    result=W.HANDLE();process=current_process()
    win.check(duplicate(process,handle,process,C.byref(result),0,False,2),'own debug-event handle duplicate')
    return result.value


def unused_debug_registers(context):
    # DR7 bits 0..7 enable local/global slots; bit13 enables general detect.
    # Reserved/read-as-one control bits do not represent an active breakpoint.
    return len(context)==716 and not(word(context,24)&0x20FF)


def null_execution_slots(context,region):
    return (len(context)==716 and word(context,24)==0x155
            and all(word(context,i)==0 for i in (4,8,12,16))
            and region.get('base')==0 and region.get('state')==0x10000
            and region.get('size',0)>=0x10000)


def own_hardware_stop(context, targets, mask):
    ip=word(context,184);status=word(context,20)
    if status&0xE000 or word(context,24)&0xFF!=mask&0xFF:return False
    return any(target!=0 and ip==target and word(context,4+i*4)==target
               and mask&(1<<(i*2)) and status&(1<<i)
               for i,target in enumerate(targets))


def observe(c, owned, tid, target, capture, seconds=30, maximum_hits=256):
    """capture(context) returns (small evidence, next original instruction VA).

    None ends the requested scope. Returned observations are not full replay.
    Called synchronously by the thread which owns the debugger attachment.
    """
    from devtools.terminal_wait_observer_gate import require_supported_relay
    require_supported_relay()
    from devtools.native_input_isolation import require_qualified_guest
    qualification = require_qualified_guest()
    need(1 <= seconds <= 120 and 1 <= maximum_hits <= 4096, 'bounded debug scope')
    parent = int(owned.pi.pid)
    need(parent != c.pid and {parent, c.pid} <= set(owned.members()), 'exact owned parent and child')
    need(tid in win.threads(c.pid), 'selected current child worker')
    api = resolve(parent, 'ntdll.dll', 'NtDebugContinue')
    entry = api['target']
    attach_break32=resolve(parent,'ntdll.dll','DbgBreakPoint')
    attach_break64=C.cast(C.WinDLL('ntdll').DbgBreakPoint,C.c_void_p).value
    result = dict(parent_pid=parent, child_pid=c.pid, child_tid=tid, qualification=qualification,
        parent_api=api, attach_break32=attach_break32, attach_break64=attach_break64,
        initial_contexts=[], hits=[], instrumentation=[], parent_restores=[], protocol=[],
        original_child_replies=[], error=None,
        source_memory_written=False, general_registers_written=False,
        debugger_reply_substituted=False, accepted=False, full_instruction_trace=False)
    threads = {}; processes = {}; masks = {}; originals = {}; borrowed={}; null_slots=set()
    pending = None; attached = False; child_handle = None
    wanted = target; child_original = None; child_armed = False
    attach_breaks_seen=set(); parent_modified=set()
    last_continuation=None; continuation_returned=False; parent_restored=False
    started = time.monotonic()
    def parent_arm(h, key, targets, mask):
        parent_modified.add(key)  # SetThreadContext can succeed before readback fails.
        actual_targets,actual_mask=targets,mask
        if key in null_slots:
            # Explicit developer observation, not a behavior-equivalence claim:
            # reuse DR0 only, retaining the other three null execution slots.
            active=0 if mask==1 else 1
            actual_targets=(targets[active],0,0,0);actual_mask=0x155
        result['instrumentation'].append(dict(role='parent', pid=key[0], tid=key[1],
            **instrument(h, actual_targets, actual_mask)))
        masks[key] = (targets,mask,actual_targets,actual_mask)
    def restore(h, old, suspended):
        if suspended:
            win.check(win.suspend(h) != 0xffffffff, 'suspend owned instrumentation cleanup')
        try:
            targets = tuple(word(old, i) for i in (4,8,12,16))
            # DR6 is debug status, not architectural application state.
            return instrument(h, targets, word(old,24))
        finally:
            if suspended:win.check(win.resume(h) != 0xffffffff, 'resume owned instrumentation cleanup')
    try:
        child_handle = win.opent(0x5A, False, tid)
        win.check(child_handle, 'selected worker debug context handle')
        win.check(win.suspend(child_handle) != 0xffffffff, 'suspend selected worker')
        try:
            child_original = debug.context(child_handle)
            result['initial_contexts'].append(dict(role='child',tid=tid,context_hex=child_original.hex()))
            need(unused_debug_registers(child_original), 'do not replace preexisting child hardware instrumentation')
        finally:win.check(win.resume(child_handle)!=0xffffffff,'resume initial child context query')
        win.check(debug.attach(parent), 'attach exact owned protection parent')
        attached = True
        win.check(kill_on_exit(False), 'debugger exit must not kill original parent')
        deadline = started + seconds
        events = 0
        while time.monotonic() < deadline and len(result['hits']) < maximum_hits:
            e = debug.EVENT()
            if not debug.wait_event(C.byref(e), 100):
                error = C.get_last_error()
                need(error in (0,121), 'debug wait failed, not a timeout: '+str(error))
                continue
            pending=(e.pid,e.tid);key=pending
            status=0x80010001 if e.code==1 else 0x10002
            events += 1
            need(events <= maximum_hits*8+256, 'bounded parent debug events')
            need(e.pid == parent, 'only explicitly attached owned parent')
            if e.code in (2,3):
                event_h = e.u.create.thread if e.code == 3 else e.u.thread.thread
                borrowed[('thread',e.tid)]=event_h
                h=own_duplicate(event_h)
                threads[key] = h; originals[key] = debug.context(h)
                result['initial_contexts'].append(dict(role='parent',tid=key[1],context_hex=originals[key].hex()))
                if e.code == 3:
                    borrowed[('process',e.pid)]=e.u.create.process
                    processes[e.pid] = own_duplicate(e.u.create.process)
                    if e.u.create.file:win.close(e.u.create.file)
                if not unused_debug_registers(originals[key]):
                    region=MEMORY()
                    need(C.sizeof(region)==48 and query_memory(processes[parent],0,C.byref(region),C.sizeof(region))==48,
                         'actual parent zero-page memory state')
                    view=dict(base=region.base or 0,size=region.size,state=region.state,protect=region.protect)
                    result['initial_contexts'][-1]['null_page_query']=view
                    need(null_execution_slots(originals[key],view),'only exact declared null-slot development experiment')
                    result['initial_contexts'][-1]['one_null_execution_slot_repurposed']=True
                    result['original_debug_behavior_equivalence_proved']=False
                    result['null_slot_caveat']='Unmapped address0 execution can still raise #DB before fetch fault; DR6 hit-bit set may differ. Three original null slots retained. No formal behavior equivalence claimed.'
                    null_slots.add(key)
                parent_arm(h,key,(entry,0,0,0),1)
            elif e.code == 6:
                if e.u.file:win.close(e.u.file)
            elif e.code == 1:
                ex = e.u.exception.record.code; h = threads[key]
                status = 0x80010001
                if ex in (0x80000003,0x4000001F):
                    address=e.u.exception.record.address
                    expected={0x80000003:attach_break64,0x4000001F:attach_break32['target']}[ex]
                    need(ex not in attach_breaks_seen and address==expected and e.u.exception.first==1,
                         'only identified first system attach breakpoint is ours')
                    need(debug.required(processes[parent],address,1)==b'\xcc','actual attach INT3 byte')
                    attach_breaks_seen.add(ex)
                    status = 0x10002
                    parent_arm(h,key,(entry,0,0,0),1)
                    if not child_armed:
                        win.check(win.suspend(child_handle) != 0xffffffff, 'suspend selected child for first arm')
                        try:
                            child_armed = True  # Dirty even if instrumentation readback fails.
                            result['instrumentation'].append(dict(role='child',pid=c.pid,tid=tid,
                                **instrument(child_handle,(wanted,0,0,0),1)))
                        finally:win.check(win.resume(child_handle)!=0xffffffff,'resume instrumented selected child')
                elif ex in (0x80000004,0x4000001E):
                    context = debug.context(h); ip = word(context,184)
                    targets,mask,actual_targets,actual_mask=masks[key]
                    need(own_hardware_stop(context,actual_targets,actual_mask),'only our enabled parent hardware stop')
                    status = 0x10002
                    if ip == entry and word(context,20)&1:
                        stack = debug.required(processes[parent],word(context,196),16)
                        ret,debug_object,client,reply = struct.unpack('<4I',stack)
                        cp,ct = struct.unpack('<2I',debug.required(processes[parent],client,8))
                        need(cp == c.pid, 'original parent continues only its owned child')
                        if ct == tid:
                            cc = debug.context(child_handle)
                            if word(cc,184) == wanted and word(cc,20)&1:
                                result['original_child_replies'].append(dict(parent_pid=e.pid,parent_tid=e.tid,
                                    parent_context_hex=context.hex(),parent_stack_hex=stack.hex(),
                                    child_pid=cp,child_tid=ct,child_context_hex=cc.hex(),original_continue_status=reply))
                                need(reply in (0x10002,0x80010001), 'known original debugger reply, never substituted: '+hex(reply))
                                if reply==0x80010001:
                                    result['original_hardware_exception_forwarded_to_child']=True
                                    # Development-only observation: leave this reply
                                    # untouched and see whether the original child's
                                    # own exception dispatch naturally reaches the
                                    # next boundary. Missing progress must fail.
                                record,next_ip = capture(cc)
                                index = len(result['hits'])
                                result['hits'].append(dict(index=index,elapsed=time.monotonic()-started,
                                    context_hex=cc.hex(),target=wanted,data=record))
                                result['protocol'].append(dict(hit_index=index,parent_context_hex=context.hex(),
                                    parent_stack_hex=stack.hex(),client_id_hex=struct.pack('<2I',cp,ct).hex(),
                                    original_continue_status=reply,debug_object=debug_object))
                                wanted = next_ip
                                if wanted is None:last_continuation=(key,ret)
                                result['instrumentation'].append(dict(role='child',pid=c.pid,tid=tid,
                                    **instrument(child_handle,(wanted or 0,0,0,0),1 if wanted else 0)))
                        parent_arm(h,key,(entry,ret,0,0),4)
                    else:
                        need(ip == targets[1] and mask == 4 and word(context,20)&(1 if key in null_slots else 2),
                             'only original parent continuation entry/return breakpoints')
                        need(word(context,176)==0,'original NtDebugContinue returned STATUS_SUCCESS')
                        if last_continuation==(key,ip):
                            result['last_original_continue_return_context_hex']=context.hex()
                            continuation_returned=True
                            # All parent threads are debug-stopped here. Do not
                            # race a newly queued breakpoint during detach.
                            for held_key,held in threads.items():
                                if held_key in parent_modified:
                                    result['parent_restores'].append(dict(pid=held_key[0],tid=held_key[1],
                                        **restore(held,originals[held_key],False)))
                            parent_restored=True
                        else:parent_arm(h,key,(entry,0,0,0),1)
                else:
                    status = 0x80010001
                    result.setdefault('other_parent_exceptions',[]).append(dict(code=ex,first_chance=e.u.exception.first))
            elif e.code == 4:
                # ContinueDebugEvent closes the original event handle.
                own=threads.pop(key,None)
                if own:win.close(own)
                originals.pop(key,None);parent_modified.discard(key);borrowed.pop(('thread',e.tid),None)
            elif e.code == 5:
                result['parent_exit_during_scope']=int(e.u.exit_code)
                for own in (*threads.values(),*processes.values()):win.close(own)
                threads.clear();originals.clear();processes.clear();parent_modified.clear()
                borrowed.clear()
            win.check(debug.continue_event(*pending,status), 'continue unmodified owned parent event')
            pending = None
            if wanted is None and continuation_returned:
                result['scope_completed']=True;break
            need(e.code != 5, 'parent exited before observation completed')
        result.setdefault('scope_completed',False)
        result['debug_events'] = events
    except Exception as exc:
        result['error']=repr(exc);result['traceback']=traceback.format_exc(limit=6)
    finally:
        cleanup = dict(errors=[], parent_detached=False, child_debug_registers_restored=False)
        if child_handle and child_original is not None and child_armed:
            try:
                cleanup['child_restore']=restore(child_handle,child_original,True)
                cleanup['child_debug_registers_restored']=True
            except Exception as exc:cleanup['errors'].append('child: '+repr(exc))
        for key,h in threads.items():
            if key not in parent_modified or parent_restored:continue
            try:result['parent_restores'].append(dict(pid=key[0],tid=key[1],
                **restore(h,originals[key],pending is None)))
            except Exception as exc:cleanup['errors'].append('parent: '+repr(exc))
        if pending:
            if not debug.continue_event(*pending,status):cleanup['errors'].append('pending event continuation failed')
        if attached:
            cleanup['parent_detached']=bool(detach(parent))
            if not cleanup['parent_detached']:cleanup['errors'].append('detach failed: '+str(C.get_last_error()))
        cleanup['event_handle_cleanup']=[]
        for own in (*threads.values(),*processes.values()):
            if not win.close(own):cleanup['errors'].append('own duplicated event handle close failed')
        for (kind,ident),handle in borrowed.items():
            C.set_last_error(0)
            actual=(get_thread_id if kind=='thread' else get_process_id)(handle)
            error=C.get_last_error() if not actual else 0
            row=dict(kind=kind,original_id=ident,query_id=actual,query_error=error)
            if not actual and error==6:row['already_invalid']=True
            else:
                # Windows documents EXIT-event close, not detach close. Never
                # manually close a potentially recycled borrowed value. The
                # short-lived collector process owns any surviving references.
                row['deferred_to_observer_process_exit']=True
            cleanup['event_handle_cleanup'].append(row)
        cleanup['own_event_handle_duplicates_closed']=not any('duplicated event handle' in e for e in cleanup['errors'])
        cleanup['last_original_continue_return_observed']=continuation_returned
        if child_handle:win.close(child_handle)
        result['cleanup']=cleanup;result['elapsed_seconds']=time.monotonic()-started
    return result
