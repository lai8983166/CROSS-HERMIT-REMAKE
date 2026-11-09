"""Preserve native vtable transitions without mistaking them for new owners.

An unclassified transition is evidence, not acceptance. The independent verifier
must prove each transition from raw frames and original code before accepting it.
"""
import ctypes as C
import ctypes.wintypes as W
from devtools import terminal_worker_retention as parent
from devtools.terminal_scene_resources import clone

base=parent.base
need=parent.need
word=parent.word


class WorkerRetention(parent.WorkerRetention):
    def transition(self,row,task,previous,handle):
        c=self.c;b=self.backend
        pid=b.get_thread_pid(handle);tid=b.get_thread_id(handle)
        need(pid==c.pid and tid==task['thread_id'],'same retained transition thread owner')
        status=b.original.wait(handle,0)
        need(status in (0,258),'actual zero-time retained thread query')
        code=W.DWORD()
        b.original.check(b.parent.exit_thread(handle,C.byref(code)),'actual retained transition exit query')
        need(code.value==(0 if status==0 else 259),'normal original thread status or still active')
        main=next(f for f in row['frames']if f['tid']==self.main_tid)
        sched=[f for f in main['chain']if f['return_va']==0x42182F]
        need(len(sched)<=1,'unambiguous original scheduler frame')
        scheduler=None
        if sched:
            bp=sched[0]['bp'];scheduler=dict(bp=bp,return_va=0x42182F,pointer=bp-0x5C,
                hex=c.get(bp-0x5C,0x6C).hex())
        frame=next((f for f in row['frames']if f['tid']==tid),None)
        regions=[]
        for link in frame['chain']if frame else []:
            need(len(regions)<100,'bounded original transition stack')
            pointer=link['bp']-0x90;raw=b.original.memory(c.h,pointer,0xA0)
            regions.append(dict(pointer=pointer,hex=raw.hex()if raw is not None else None))
        return dict(previous_vtable=previous['vtable'],observed_vtable=task['vtable'],
            thread_query=dict(owner_pid=pid,thread_id=tid,wait_status=status,exit_code=code.value,
                zero_timeout=True,observer_duplicate_only=True,original_cleanup_proved=False),
            scheduler_frame=scheduler,worker_stack_regions=regions,
            transition_verified=False,full_resource_PTD_cleanup_proved=False)

    def retain(self,row):
        c=self.c;b=self.backend;receipt=row['worker_retention'];receipt['version']=2;call=None
        try:
            for task in row['tasks']:
                head=bytes.fromhex(task['header_hex']);tid=word(head,0x24)
                need(tid==task['thread_id'],'raw header worker ID')
                key=(task['pointer'],tid);remote=word(head,0x20);event=word(head,0x1C)
                frame=next((f for f in row['frames']if f['tid']==tid),None)
                ancestors={x['return_va']for x in frame['chain']}if frame else set()
                proof=dict(pointer=key[0],thread_id=tid,remote_handle=remote,event=event,
                    observed_context_present=frame is not None,status=None)
                receipt['tasks'].append(proof)
                if key in self.handles:
                    previous=next(w for w in self.workers if(w['pointer'],w['thread_id'])==key)
                    need((previous['original_handle'],previous['event']['remote_handle'])==(remote,event),
                         'retained graph thread handle and event remain exact')
                    if previous['vtable']!=task['vtable']:
                        call=dict(api='transition owner/exit/stack observation',pid=c.pid,pointer=key[0],
                            thread_id=tid,remote_handle=remote,event=event)
                        proof['transition']=self.transition(row,task,previous,self.handles[key])
                        proof['status']='retained_vtable_transition'
                    else:proof['status']='already_retained'
                    continue
                callback={0x421F8A,0x56E183}
                if not callback<=ancestors:
                    need(not callback&ancestors and 'TLS'not in task,
                         'partial original callback ancestry must not become pending')
                    proof['status']='pending_callback_ancestry';continue
                need(remote and tid and 'TLS'in task,'original callback requires actual native handle and TLS')
                handle=W.HANDLE()
                call=dict(api='DuplicateHandle',pid=c.pid,pointer=key[0],thread_id=tid,
                    remote_handle=remote,event=event,options=2,desired_access=0,inherit=False)
                b.original.check(b.parent.duplicate(c.h,remote,b.parent.current_process(),
                    C.byref(handle),0,False,2),'retain same suspended original worker')
                try:
                    need(b.get_thread_pid(handle)==c.pid and b.get_thread_id(handle)==tid,
                         'duplicate belongs to exact original worker')
                    call=dict(api='event_identity',pid=c.pid,pointer=key[0],thread_id=tid,remote_handle=event)
                    identity=b.event_identity(c,event)
                except BaseException:
                    b.original.check(b.original.close(handle),'close failed observer retention');raise
                self.handles[key]=handle
                self.workers.append(dict(pointer=key[0],thread_id=tid,vtable=task['vtable'],
                    original_handle=remote,event=identity,first_elapsed=row['elapsed']))
                proof['status']='retained'
        except BaseException as exc:
            if self.failure is None:self.failure=dict(error=repr(exc),call=call,row=row)
            raise


def progress_signature(row,controller):
    # Save the first retention even if graph/VM/wait-site fields did not change.
    return parent.progress_signature(row,controller),tuple(
        (p['pointer'],p['thread_id'],p['remote_handle'],p['event'],p['status'])
        for p in row['worker_retention']['tasks'])


continue_school=clone(parent.continue_school,WorkerRetention=WorkerRetention,progress_signature=progress_signature)
