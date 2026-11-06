"""Audit redundant Unicorn REP STOSD attempts without changing guest execution.

The original memset's positive iterations decrement ECX and advance EDI by four.
Consecutive code/store callbacks with unchanged architectural state describe one
iteration. Keep their raw trace separately. Only a matched ordinary live-heap
store may be excluded from the canonical instruction/write digest.
"""
import hashlib
import json
import struct

from tools.terminal_unit_frontends_trace import Replay,TraceCount,SLICE


def need(value,message):
    if not value:raise ValueError(message)


class Counts(TraceCount):
    def __init__(self):
        super().__init__()
        self.raw=TraceCount()
        self.repeated=False

    def instruction(self,pc):
        self.raw.instruction(pc)
        if not self.repeated:super().instruction(pc)

    def write(self,pc,address,size,value):
        self.raw.write(pc,address,size,value)
        if not self.repeated:super().write(pc,address,size,value)


class RepReplay(Replay):
    REP=0x56CF01
    MAX_RETRIES=1024

    def __init__(self,*args,heap_owner,quiescent_return=None,**kwargs):
        super().__init__(*args,**kwargs)
        self.count=Counts()
        self.heap_owner=heap_owner
        self.rep=None
        self.retries=[]
        self.rep_boundary=None
        self.quiescent_return=quiescent_return
        self.implicit_return_stops=[]
        self.deferred_stop_hits=0
        self.completing_stop_retry=False

    def stop_selection(self,pc):
        if self.event_index!=len(self.events)-1:return None
        event=self.events[self.event_index]
        if not(event['stop'] is True and event['continues_guest'] is False
               and event['effects']==[] and event['CPU_changes']=={}):return None
        row=self.report['transactions'][len(self.history)-1]
        target=row['after_trace']['instructions']
        need(self.count.instructions<=target,'quiescent stop ordinal cannot be passed')
        if self.count.instructions==target:
            need(pc==event['pc'],'exact original PC at quiescent stop ordinal')
            return 'stop'
        return 'defer' if pc==event['pc'] else None

    def invoke_code(self,uc,pc,size,context):
        if self.stop_selection(pc)!='defer' and not self.completing_stop_retry:
            return super().code(uc,pc,size,context)
        # A budget stop inside a loop belongs to its final recorded ordinal,
        # not every earlier execution of that original instruction address.
        events=self.events
        self.events=()
        self.deferred_stop_hits+=1
        try:super().code(uc,pc,size,context)
        finally:self.events=events

    def complete_attempt(self,cpu):
        previous=self.rep
        if previous is None:return
        expected=dict(previous['CPU'])
        if expected['ECX']:
            need(previous['stores']==1,'one store per positive original REP attempt')
            need(self.read(expected['EDI'],4)==struct.pack('<I',expected['EAX']),
                 'completed original REP store has committed its exact four bytes')
            expected['ECX']-=1
            expected['EDI']+=4
        else:
            need(previous['stores']==0,'zero-count original REP performs no store')
            expected['EIP']=self.REP+2
        need(cpu==expected,'complete original REP architectural progress')

    def code(self,uc,pc,size,context):
        self.completing_stop_retry=False
        if pc==self.quiescent_return and not(
                self.event_index<len(self.events) and self.events[self.event_index]['pc']==pc):
            row=self.report['transactions'][len(self.history)-1]
            actual=self.cpu()
            need(self.event_index==len(self.events) and row['end'] in (0,pc)
                 and row['after_CPU']['EIP']==pc and actual==row['after_CPU'],
                 'natural complete owned root return boundary')
            if self.rep is not None:self.complete_attempt(self.cpu())
            self.rep=None;self.count.repeated=False
            self.implicit_return_stops.append(dict(transaction=len(self.history)-1,
                entry=row['entry'],end=row['end'],actual_return=pc,
                actual_complete_CPU_sha256=hashlib.sha256(
                    json.dumps(actual,sort_keys=True,separators=(',',':')).encode()).hexdigest()))
            uc.emu_stop()
            return
        selection=self.stop_selection(pc)
        if selection=='stop':
            actual=self.cpu()
            if (pc==self.REP and self.rep is not None and self.rep['CPU']['ECX']>0
                    and self.rep['stores']==1 and actual==self.rep['CPU']):
                expected=dict(actual,ECX=actual['ECX']-1,EDI=actual['EDI']+4)
                need(expected==self.events[self.event_index]['before_CPU'],
                     'only the pending REP iteration may finish before its source stop')
                self.completing_stop_retry=True
            else:
                if self.rep is not None:self.complete_attempt(actual)
                self.rep=None;self.count.repeated=False
                return self.invoke_code(uc,pc,size,context)
        boundary=(len(self.history),self.slice_first)
        budget_stop=self.count.instructions-self.slice_first>=SLICE
        is_rep=pc==self.REP
        if not is_rep or budget_stop or boundary!=self.rep_boundary:
            if self.rep is not None:self.complete_attempt(self.cpu())
            self.rep=None
        self.count.repeated=False
        if not is_rep or budget_stop:
            return self.invoke_code(uc,pc,size,context)
        need(size==2 and self.read(pc,2)==b'\xF3\xAB','exact unchanged original REP STOSD')
        need(selection=='defer' or self.completing_stop_retry or not(
             self.event_index<len(self.events) and self.events[self.event_index]['pc']==pc),
             'REP attempts have no host event or effect')
        previous=self.rep
        if previous is None:
            current=self.cpu()
            if (not current['ECX'] or current['EFLAGS']&0x400 or current['EDI']%4
                    or not self.heap_owner(current['EDI'],4)):
                return self.invoke_code(uc,pc,size,context)
        else:
            ecx=uc.reg_read(self.x86.UC_X86_REG_ECX)
            edi=uc.reg_read(self.x86.UC_X86_REG_EDI)
            expected=previous['CPU']
            repeated=ecx==expected['ECX'] and edi==expected['EDI']
            if repeated:
                need(ecx>0 and previous['stores']==1,'only a completed positive REP attempt may repeat')
                current=self.cpu()
                need(current==expected,'entire architectural CPU unchanged at repeated REP attempt')
                need(len(self.retries)<self.MAX_RETRIES,'finite independent raw REP retry budget')
                actual=self.read(edi,4)
                need(self.heap_owner(edi,4) and actual in
                     (previous['before'],struct.pack('<I',current['EAX'])),
                     'aborted or committed repeated store has no unrelated memory change')
                self.count.repeated=True
            else:
                if previous['repeated']:self.complete_attempt(self.cpu())
                need(expected['ECX']>0 and previous['stores']==1
                     and ecx==expected['ECX']-1 and edi==expected['EDI']+4,
                     'each distinct original REP iteration advances ECX and EDI')
                # No other guest instruction or host event has occurred. STOSD
                # changes only ECX/EDI. Verify every register at retries/exits.
                current=dict(expected,ECX=ecx,EDI=edi)
        self.rep=dict(CPU=current,stores=0,repeated=self.count.repeated,
                      before=previous['before'] if self.count.repeated else None)
        self.rep_boundary=boundary
        self.invoke_code(uc,pc,size,context)

    def write(self,uc,access,address,size,value,context):
        pc=uc.reg_read(self.x86.UC_X86_REG_EIP)
        if self.rep is not None:need(pc==self.REP,'active REP cannot hide another instruction write')
        if pc==self.REP and self.rep is not None:
            need(self.rep is not None and self.rep['stores']==0,'REP code and exactly one store are paired')
            cpu=self.rep['CPU']
            need(cpu['ECX']>0 and (address,size,value&0xFFFFFFFF)==(cpu['EDI'],4,cpu['EAX'])
                 and self.heap_owner(address,size),'exact original STOSD store in a live CRT allocation')
            if not self.rep['repeated']:self.rep['before']=self.read(address,4)
            self.rep['stores']=1
            if self.rep['repeated']:
                need(self.cpu()==cpu,'repeated store preserves the entire pre-instruction CPU')
                self.retries.append(dict(transaction=len(self.history)-1,CPU=dict(cpu),
                    write=dict(pc=pc,address=address,bytes=size,value=value&0xFFFFFFFF),
                    memory_before=self.rep['before'].hex(),memory_before_retry=self.read(address,4).hex(),
                    canonical_before=self.count.mark(),raw_before=self.count.raw.mark()))
        super().write(uc,access,address,size,value,context)

    def run(self):
        result=super().run()
        if self.rep is not None:self.complete_attempt(self.cpu())
        raw=self.count.raw.mark()
        need(raw['instructions']-self.count.instructions==len(self.retries)
             and raw['writes']-self.count.writes==len(self.retries),
             'raw differences consist exclusively of paired audited REP retries')
        result.update(raw_original_callback_trace=raw,REP_callback_retries=self.retries,
                      implicit_owned_RETURN_stops=self.implicit_return_stops,
                      quiescent_stop_matching='original_PC_and_canonical_instruction_ordinal',
                      deferred_earlier_stop_PC_hits=self.deferred_stop_hits,
                      REP_retry_rule_version=1,canonical_trace_matches_source=True,
                      raw_trace_matches_source=not self.retries,
                      guest_execution_or_state_modified=False)
        return result
