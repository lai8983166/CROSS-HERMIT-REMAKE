"""Independent whole original execution and typed native boundary proof.

This module does not label a source accepted merely because it can decode.
Initial inputs, root ABI, native effects, every original instruction/write,
whole mapped memory and the canonical57 CPU are checked by separate rules.
"""
import copy
import ctypes
import hashlib
import json
import struct

from unicorn import UC_HOOK_CODE
from tools import terminal_unit_frontends_emulation as source
from tools.terminal_unit_frontends_retries import RepReplay as Replay
from tools.terminal_unit_frontends_inputs_verification import InitialInputs,Driver,need
from tools.terminal_unit_frontends_other_platform_verification import GDI,OtherLeaves
from tools.terminal_unit_frontends_projection_verification import HistoricalPlatformVerifier
from tools import terminal_last_dialogue_gdi as identity_plan
from tools import terminal_last_dialogue_gdi_verification as GDI_history
from tools import terminal_name_emulation as names
from tools import battle_hit_damage_emulation as combat
from tools.school_retained_name_corpus import source_names
from tools.school_tactical_resources_emulation import original_resource
from tools.terminal_unit_frontends_platform_verification import FILE_SIZES


def file_inputs():
    """Authenticate complete original asset bytes, independently of the row."""
    out={}
    for name in FILE_SIZES:
        if 'DxAnim' in name:
            job=1 if name.endswith('b0a.bin') else 3
            raw=source.images.unit_asset(job)['raw']
        elif name=='data\\Tactics\\common.bin':
            raw=source.previous.common_resource()[0]
        elif name.lower().endswith(('sc001.bin','sc002.bin')):
            catalog,_=source_names()
            role='1' if name.lower().endswith('sc001.bin') else '2'
            identity=catalog['roles'][role]
            raw=(source.ROOT/identity['image_path']).read_bytes()
            need(hashlib.sha256(raw).hexdigest()==identity['image_sha256'],
                 'independent complete original portrait file')
        else:
            raw,_=original_resource(name)
        need(len(raw)==FILE_SIZES[name],'complete independently authenticated original file '+name)
        out[name]=raw
    return out


def audit_GDI(row):
    raw=(source.ROOT/identity_plan.PLAN_PATH).read_bytes()
    need(hashlib.sha256(raw).hexdigest()==identity_plan.PLAN_SHA256,'exact independent GDI identity plan')
    plan=json.loads(raw)
    count=len(next(c for c in plan['cases'] if c['name']==row['input']['name'])['calls'])
    calls=[]
    native_bitmaps={}
    for trace in row['GDI_trace']:
        native=trace['native_result']
        if trace['name']=='CreateDIBSection':
            bits=native.get('native_bits');size=native.get('bitmap_bytes')
            need(type(bits) is int and 0<bits<2**(8*ctypes.sizeof(ctypes.c_void_p))
                 and type(size) is int and size>0
                 and all(not(a<bits+size and bits<a+n) for a,n in native_bitmaps.values()),
                 'actual current native DIB buffer identity and live span ownership')
            native_bitmaps[native['result']]=(bits,size)
        elif trace['name']=='DeleteObject' and native['result']:
            native_bitmaps.pop(trace['native_args'][0],None)
        call=copy.deepcopy(trace['native_result'])
        call.pop('dc_translated_args',None);call.pop('native_bits',None)
        call.update(args=trace['args'],result=trace['logical_result'],actual_API_executed=True)
        calls.append(call)
    need(not native_bitmaps,'all actual DIB buffers retire with their original bitmap owners')
    declared=row['last_dialogue_GDI_lifetimes']
    return GDI_history.audit(calls,row['GDI_trace'],declared,declared['latest_guest_slots'],
                             calls[:count],raw,identity_plan.PLAN_PATH,plan['source'],row['input']['name'])


class CaseVerifier:
    def __init__(self,row):
        self.row=row
        self.driver=Driver(row['input'])
        self.platform=HistoricalPlatformVerifier(row,source.previous.CODE,file_inputs())
        self.other=OtherLeaves(row)
        self.gdi=GDI(row)
        self.wait_seen=False
        self.observed={}
        self.native_result_calls=[]
        self.replay=None

    def original(self,uc,pc,size,context):
        replay=self.replay
        if replay.budget_stop:return
        self.platform.policy.observe(replay,pc)
        if replay.event_index:
            last=replay.events[replay.event_index-1]
            if last['pc']==pc and last['stop']:return
        if pc in (0x46B470,0x432100,0x454CF0,0x473860,0x4539B0,0x40B2EC,0x46D3F4,0x440F00,0x457C40):
            self.observed[hex(pc)]=self.observed.get(hex(pc),0)+1
            if pc==0x473860:
                sp=replay.cpu()['ESP']
                self.native_result_calls.append(struct.unpack('<I',replay.read(sp,4))[0])

    def wait(self,replay):
        row=self.row
        frontier=row.get('frontier') or row['terminal_battle_exit_prefix']['freeze']
        memory=row.get('forward_memory') or row['final']
        cpu=row.get('forward_CPU') or row['pending_CPU']
        need(not self.wait_seen,'first original cooperative wait occurs only once')
        actual=replay.cpu();sp=actual['ESP'];outer=source.previous.STACK+0xF000-4
        need(actual==cpu and actual['EIP']==source.WAIT and actual['ECX']==source.previous.TASK,
             'complete natural wait CPU and receiver')
        need(struct.unpack('<I',replay.read(sp,4))[0]==0x453CB5
             and struct.unpack('<I',replay.read(outer-8,4))[0]==1
             and struct.unpack('<I',replay.read(outer+4,4))[0]==source.previous.RETURN,
             'actual original wait caller and pending outer result1/return')
        regions=list(replay.u.mem_regions())
        need(len(regions)==len(memory),'all forward mapped regions at original wait')
        for (a,b,permission),capture in zip(regions,memory):
            need((capture['pointer'],capture['bytes'])==(a,b-a+1)
                 and replay.read(a,b-a+1).hex()==capture['hex'],
                 'entire independent forward RAM at '+hex(a))
        need(frontier['entry']==source.WAIT and frontier['kind']=='cooperative_wait'
             and frontier['first_instruction_executed'] is False
             and frontier['original_wait_reached'] is True
             and frontier['original_wait_body_executed'] is False
             and frontier['outer_result_consumed'] is False
             and frontier['terminal_battle_exit_executed'] is False,
             'honest first-wait boundary and unresolved full exit')
        need(frontier['stack_hex']==replay.read(source.previous.STACK,0x20000).hex(),
             'entire pending original128KiB stack')
        expected=dict(kind='cooperative_wait',entry=source.WAIT,first_instruction_executed=False,
                      original_wait_reached=True,original_wait_body_executed=False,
                      frame_EBP=actual['EBP'],outer_frame_EBP=outer,caller=0x453CB5,
                      args=[0],local_result=1,root_return_address=source.previous.RETURN,
                      stack_pointer=source.previous.STACK,stack_bytes=0x20000,
                      stack_hex=replay.read(source.previous.STACK,0x20000).hex(),
                      outer_result_consumed=False,terminal_battle_exit_executed=False)
        need(struct.unpack('<I',replay.read(sp+4,4))[0]==0 and frontier==expected,
             'every reported natural wait field independently derived from actual current stack/CPU')
        self.wait_seen=True
        self.driver.frontier_reached=True

    def event(self,replay,event):
        # Pure host observations and quiescent stops may never change guest
        # registers or bytes. Their actual native readbacks are still audited.
        if not event['effects']:
            need(not event['CPU_changes'],'observation/stop cannot change any architectural register')
            wire=event.get('wire')
            if wire is not None:
                need(set(wire)=={'CRT','GPU','GDI','TLS'},'complete observed native channels')
                for name in ('CRT','GPU'):
                    self.platform.observers(replay,name,wire[name][0])
                    self.platform.observers(replay,name,wire[name][1])
                need(wire['GDI'][0]==wire['GDI'][1] and wire['TLS'][0]==wire['TLS'][1],
                     'no unverified GDI/TLS observer operation')
            if event['pc']==source.WAIT:
                need(event['stop'] and not event['continues_guest'],'wait CALL target stays unexecuted')
                self.wait(replay)
            elif event['pc']==self.driver.active_keyboard_stop:
                need(event['stop'] and not event['continues_guest'],
                     'declared captured keyboard fragment stops before its next original instruction')
            else:
                pc=event['pc']
                api=any(struct.unpack('<I',replay.read(slot,4))[0]==pc for slot in source.previous.overlay.crt.IMPORTS)
                api=api or any(struct.unpack('<I',replay.read(slot,4))[0]==pc for slot in names.GDI)
                need(pc in source.ALLOWED or pc==source.previous.RETURN or api,
                     'quiescent stop only at current admitted original/API/root-return PC')
                need(event['stop'] != event['continues_guest'],'stop or side-effect-free original observer')
            return
        if self.platform.handles(replay,event):
            self.platform.validate_event(replay,event)
        elif self.other.handles(replay,event):
            self.foreign_wire(replay,event,'TLS' if event['pc'] in combat.APIS else None)
            self.other.validate_event(replay,event)
        elif self.gdi.handles(replay,event):
            self.foreign_wire(replay,event,'GDI')
            self.gdi.validate_event(replay,event)
        else:
            raise ValueError('unimplemented independent platform boundary '+hex(event['pc']))

    def foreign_wire(self,replay,event,channel):
        wire=event['wire']
        need(set(wire)=={'CRT','GPU','GDI','TLS'},'complete independent native wire channels')
        for name in ('CRT','GPU'):
            need(wire[name][0]==wire[name][1],'Win32/GDI leaf cannot hide another native operation')
            self.platform.observers(replay,name,wire[name][0])
        for name,cursor in (('GDI',self.gdi.ordinal),('TLS',self.other.tls_count)):
            need(wire[name]==[cursor,cursor+int(name==channel)],
                 'exact current independently consumed '+name+' native call ordinal')

    def drive(self,replay,actions,row,history):
        if row is not None and 'wire_before' in row:
            wire=row['wire_before']
            for name in ('CRT','GPU'):
                self.platform.observers(replay,name,wire[name])
            need(wire['GDI']==self.gdi.ordinal and wire['TLS']==self.other.tls_count,
                 'all side-effecting native calls occur at recorded instruction boundaries')
        self.driver(replay,actions,row,history)

    def verify(self):
        try:
            execution=self.row['unit_frontends']['execution']
            need(execution['schema_version']==2 and 'write_PCs' in execution
                 and all('wire_before' in tx and 'wire_after' in tx for tx in execution['transactions']),
                 'complete current trace with actual write-PC set and native observation boundaries')
            replay=Replay(execution,source.previous.CODE,source.RANGES,
                          InitialInputs(self.row),self.drive,self.event,
                          heap_owner=lambda address,size:any(p<=address and address+size<=p+b['bytes']
                              for p,b in self.platform.blocks.items()),
                          quiescent_return=source.previous.RETURN)
            self.replay=replay
            replay.u.hook_add(UC_HOOK_CODE,self.original)
            proof=replay.run()
            need(self.wait_seen,'actual independently executed original wait reached')
            need(self.observed.get('0x4539b0')==1 and self.observed.get('0x40b2ec',0)>0
                 and self.observed.get('0x46d3f4',0)>0,'original scene and both old frontend PCs actually executed')
            need(0x454798 in self.native_result_calls,'original473860 reached from natural454793 CALL')
            need(self.observed.get('0x440f00')==self.observed.get('0x457c40')==1,
                 'natural original minimap and final UI updates executed before wait')
            need(self.other.common_count==119,'all original COMMON no-texture markers executed')
            proof.update(platform=self.platform.finish(replay),other_platform=self.other.finish(),
                         fresh_GDI=self.gdi.finish(),GDI_lifetimes=audit_GDI(self.row),
                         observed_original_entries=self.observed,natural_result_callers=self.native_result_calls,
                         root_calls=self.driver.root_count,keyboard_samples=self.driver.keyboard_count,
                         original_wait_reached=True,wait_body_executed=False,
                         outer_result_consumed=False,complete_battle_exit=False)
            return proof
        except Exception as error:
            # Preserve the first independent difference without a RAM dump.
            cursor=error.__traceback__
            while cursor is not None:
                frame=cursor.tb_frame
                if frame.f_code.co_name=='run' and frame.f_locals.get('self') is self.replay:
                    tx=frame.f_locals.get('row')
                    if tx is not None:
                        actual=self.replay.cpu()
                        error.unit_frontends_context=dict(
                            transaction=frame.f_locals.get('i'),entry=tx['entry'],end=tx['end'],
                            CPU_difference={k:[tx['after_CPU'][k],v] for k,v in actual.items()
                                            if tx['after_CPU'][k]!=v},
                            memory=[tx['after_memory'],self.replay.memory.capture()],
                            trace=[tx['after_trace'],self.replay.count.mark()])
                        if hasattr(self.replay.count,'raw'):
                            error.unit_frontends_context.update(raw_trace=self.replay.count.raw.mark(),
                                retries=self.replay.retries[-3:])
                        break
                cursor=cursor.tb_next
            raise
        finally:
            self.gdi.close()


def verify_case(row):
    return CaseVerifier(row).verify()
