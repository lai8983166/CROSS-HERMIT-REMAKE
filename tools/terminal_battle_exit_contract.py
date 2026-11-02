"""Independent contracts for the original battle-loop exit prefix.

These checks use the preserved parent binary/report; source execution does not
import this module. Historical acceptance bytes are never rewritten.
"""
import hashlib,json,struct
from functools import lru_cache
from tools import terminal_battle_stage_handoff_emulation as parent
ROOT,CODE,need=parent.ROOT,parent.CODE,parent.need
TASK,INPUT,STACK,RETURN=parent.TASK,parent.INPUT,parent.STACK,parent.RETURN
TASK_PROOF='analysis/terminal-task-completion-proof-v1-20261030.json'
TASK_PROOF_SHA='e17bd23efe9691d7bf6f14ef808500b9d827fd84496c52bb9513b66a6900a3ce'

@lru_cache(maxsize=1)
def accepted_task_counts():
 raw=(ROOT/TASK_PROOF).read_bytes()
 need(hashlib.sha256(raw).hexdigest()==TASK_PROOF_SHA,'fixed accepted task-completion proof for accounting')
 return {r['name']:r['forward_summary']['complete_tasks'] for r in json.loads(raw)['cases']}

def parent_task_accounting(row):
 """Count complete original task roots instead of copying a stale summary."""
 d=row['terminal_battle_stage_handoff'];frames=d['frames'];segments=d['segments']
 tasks=[(i,s) for i,s in enumerate(segments) if s['entry']==0x454CF0]
 need(len(frames)==349 and [f['index'] for f in frames]==list(range(349)),'349 preserved stage frames for task accounting')
 need(len(tasks)==len(frames),'one complete task call in every preserved stage frame')
 for f,(i,s) in zip(frames,tasks):
  need(f['segments'][0]<=i<f['segments'][1],'counted task belongs to its own frame')
  need(s['label']=='task_'+str(f['index']) and s['root']==dict(receiver=TASK,args=[]),'counted original task root identity and ABI')
  need(s['stop']==RETURN and s['CPU']['EIP']==RETURN and s['CPU']['ESP']==STACK+0xF004,'count only naturally completed original task roots')
 base=accepted_task_counts()[row['input']['name']]
 return dict(accepted_task_completion=base,additional_stage_task_calls=len(tasks),complete_tasks=base+len(tasks),previous_stage_summary_omitted_calls=len(tasks),historical_proof_unchanged=True)

def strict_parent_text(row):
 receipts=row['terminal_battle_stage_handoff']['text_APIs']
 need(len(receipts)==698,'one IME and one string query per accepted original stage frame')
 strings=[]
 for i,r in enumerate(receipts):
  need(r['actual_API_executed'] is True,'actual original stage input endpoint')
  if i%2==0:
   need((r['name'],r['entry'],r['import_slot'],r['caller'],r['args'],r['result'],r['segment'])==('ImmGetOpenStatus',0x76182A80,0x5920EC,0x425C99,[0],0,'input_'+str(i//2)),'exact owned null IME endpoint')
  else:
   need((r['name'],r['entry'],r['import_slot'],r['caller'],r['args'],r['result'],r['segment'],r['string_hex'])==('lstrlenA',0x770206E0,0x5922C4,0x425A7E,[INPUT+0x528],0,'task_'+str(i//2),''),'exact original task string caller, owned buffer and empty bytes')
   strings.append(r)
 return dict(original_string_caller=0x425A7E,owned_buffer=INPUT+0x528,string_calls=len(strings),IME_calls=len(receipts)-len(strings),derived_fields_written=False)

def original_exit_contract():
 from capstone import Cs,CS_ARCH_X86,CS_MODE_32
 md=Cs(CS_ARCH_X86,CS_MODE_32)
 expected={0x4539EC:('call','0x454cf0'),0x4539F1:('mov','dword ptr [ebp - 8], 0'),0x4539FB:('call','0x453f10'),0x453A00:('mov','dword ptr [ebp - 8], eax'),0x453A0C:('call','0x46b470'),0x453A1A:('call','0x432100'),0x453A22:('call','0x457aa0'),0x453C3A:('call','0x453e10'),0x453CB0:('call','0x422360'),0x453CB5:('cmp','dword ptr [ebp - 8], 0'),0x453CB9:('je','0x453ce4'),0x453CC4:('call','0x4967b0'),0x453CCE:('call','0x422360'),0x453CD8:('call','0x422360'),0x453CDD:('mov','eax, 1'),0x453CFB:('ret','')}
 for address,want in expected.items():
  decoded=next(md.disasm(CODE[address-0x400000:address-0x400000+16],address))
  need((decoded.mnemonic,decoded.op_str)==want,'original battle exit instruction '+hex(address))
 seq=list(md.disasm(CODE[0x453CA6-0x400000:0x453CB5-0x400000],0x453CA6))
 need([(i.mnemonic,i.op_str) for i in seq]==[('call','0x457c40'),('push','0'),('mov','ecx, dword ptr [ebp - 4]'),('call','0x422360')],'original first cooperative wait argument and receiver')
 # Both stores and the consumer use the same original stack local; the first
 # cooperative call is before the compare, so freezing there cannot prove exit.
 need(0x453A00<0x453CB0<0x453CB5<0x453CDD,'result remains pending across the first original cooperative wait')
 return dict(instruction_checks=len(expected),wait_entry=0x422360,wait_call_site=0x453CB0,wait_return_address=0x453CB5,wait_argument=0,pending_result_local=-8,original_result_consumer=0x453CB5,loop_return_one=0x453CDD,terminal_battle_exit_executed=False)
