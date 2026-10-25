"""Independent exact work fields, original pause stores and truncating fade rules."""
import copy,struct
from tools.terminal_work_emulation import CTRL,TASK,VM,WORK,SCRIPT,ROOT,SOURCE,need,terminal
from tools.battle_lethal_combat import expand
from tools import battle_live_terminal_model as combat
from tools.school_retained_portrait_catalog import commands


def num(b,offset,fmt='i'):return struct.unpack_from('<'+fmt,b,offset)[0]


def verify_work(row):
 w=row['work'];expected=copy.deepcopy(row['initialization']['before']);key=row['key_writes']
 need(num(bytes.fromhex(expected['task']),0x60,'I')==WORK,'original TASK work owner declared before first root')
 need(bytes.fromhex(expected['work'])==bytes(0x24C0),'declared empty complete work object')
 def store(pc,address,value,n=1):return dict(pc=pc,address=address,bytes=n,value=value&((1<<(n*8))-1))
 def check(step,edits=(),writes=(),result=None):
  nonlocal expected
  need(step['before']==expected,'continuous independent work boundary input')
  for field,offset,value,fmt in edits:
   b=bytearray.fromhex(expected[field]);struct.pack_into('<'+fmt,b,offset,value);expected[field]=b.hex()
  need(step['after']==expected,'entire independent work/VM/task/units/clock state')
  need(key[slice(*step['writes'])]==list(writes),'all exact original work stores and PCs')
  if result is not None:need(step['call']['result']==result,'original work return contract')
 check(row['initialization'],writes=[store(0x49781D,WORK+0x2499,0),store(0x49782A,WORK+0x2490,0,4),store(0x49783A,WORK+0x24A8,0)])
 # The live world/event prefix changes WORK's three protocol bytes and VM binding.
 expected=copy.deepcopy(w['before']);event=expand(row['events'][-1]['after'],row['blobs'])
 need(all(expected[k]==event[k] for k in ('VM','task','units','remaining','elapsed')) and bytes.fromhex(expected['work'])[:3].hex()==event['work'],'actual terminal state enters supplemental pause/work experiment')
 need(num(bytes.fromhex(expected['VM']),0x1C)==0 and bytes.fromhex(expected['VM'])[0x92E0]==0,'bound but unplayed VM input')
 need(bytes.fromhex(expected['work'])[3:]==bytes(0x24C0-3),'remaining work fields not host-initialized later')
 edits=[('gates',i,0,'B') for i in (2,3,4,6,7,8)]+[('gates',9,255,'B'),('gates',10,255,'B')]
 edits += [('owner_flags',i,1,'B') for i in range(4)]+[('work',o,0,'B') for o in (0x20E8,0x216C,0x2230)]
 pause_writes=[store(pc,WORK+o,0) for pc,o in ((0x455406,0x20E8),(0x4558C6,0x216C),(0x455D26,0x2230))]
 pause_writes += [store(pc,CTRL+o,0) for pc,o in ((0x4679A1,0x108B34),(0x4679AB,0x108B35),(0x4679B5,0x108B36),(0x4679BF,0x108B38),(0x4679C9,0x108B39),(0x4679D3,0x108B3A))]
 pause_writes += [store(0x467A7B,CTRL+0x108B3B,255),store(0x467A85,CTRL+0x108B3C,255)]
 check(w['pause'],edits,pause_writes,0)
 def tick(steps):
  need(len(steps)==3,'fade/scroll/query root triple')
  b=bytes.fromhex(expected['work']);active=b[0x2499];direction=b[0x2498];edits=[];writes=[];returned=1
  if active:
   value=num(b,0x2490);delta=num(b,0x2494);value=value+delta if direction==1 else value-delta
   value=min(38912,value) if direction==1 else max(0,value);remaining=num(b,0x249C)-1
   edits=[('work',0x2490,value,'i'),('work',0x249C,remaining,'i')]
   writes=[store(0x497B4D if direction else 0x497B0A,WORK+0x2490,value,4),store(0x497BB7,WORK+0x249C,remaining,4)]
   # For this sourced 60-step corpus no arithmetic clamp occurs.
   need(0<value<38912,'unclamped source fade60 interior, including residual endpoint')
   if remaining==0:
    status=2 if direction else 0;edits += [('work',0x2499,0,'B'),('work',0x249A,status,'B'),('VM',0x92E0,0,'B')]
    writes += [store(0x497BD1,WORK+0x2499,0),store(0x497C0A if direction else 0x497BFB,WORK+0x249A,status),store(0x4977B8,VM+0x92E0,0)]
   else:
    edits += [('work',0x249A,1,'B')];writes += [store(0x497C22,WORK+0x249A,1)];returned=0
  check(steps[0],edits,writes,returned)
  need(bytes.fromhex(expected['work'])[0x24A8]==0,'declared inactive scroll work, never supplied result')
  check(steps[1]);check(steps[2],result=int(bytes.fromhex(expected['work'])[0x249A]!=0))
 tick(w['idle']);need(len(w['experiments'])==2,'both actual terminal work handlers')
 raw=(ROOT/terminal.SCRIPT_PATH).read_bytes();decoded=commands(raw);sub={1:2,4:11}[num(bytes.fromhex(expected['task']),0x174)]
 seg=next(s for s in decoded['segments'] if s['index']==sub);rows=decoded['commands'][seg['first_command']:seg['first_command']+seg['command_count']]
 constant=struct.unpack_from('<f',SOURCE.read_bytes(),0x59E8BC-0x400000)[0];need(constant==38912.0,'original float constant')
 # _ftol forces x87 RC=11 (truncate), then restores the prior control word.
 delta=int(constant/60);need(delta==648,'independent original truncating conversion')
 outcomes=[]
 for op,e in zip((117,118),w['experiments']):
  c=next(c for c in rows if c['opcode']==op);need(e['opcode']==op and e['source_command']==c and c['bytes']==8 and raw[c['offset']+4:c['offset']+8]==struct.pack('<I',0x2000003C),'genuine selected raw command and duration')
  need(e['handler']['call']['args']==[0,SCRIPT+c['offset'],8] and num(bytes.fromhex(expected['VM']),0x10,'I')==SCRIPT+seg['code_start'],'declared handler root references bound source; no VM-PC fabrication')
  direction=int(op==117);edits=[('work',0x2490,0 if direction else 38912,'i'),('work',0x2494,delta,'i'),('work',0x2498,direction,'B'),('work',0x2499,1,'B'),('work',0x249A,1,'B'),('work',0x249C,60,'i'),('VM',0x9250,60,'i'),('VM',0x92E0,1,'B')]
  pcs=(0x49790B,0x49791B,0x497927,0x497937,0x497942,0x497969) if direction else (0x4979CB,0x4979DB,0x4979E7,0x4979F7,0x497A02,0x497A29)
  writes=[store(pc,WORK+off,value,n) for pc,off,value,n in zip(pcs,(0x2490,0x2498,0x249A,0x249C,0x2499,0x2494),(0 if direction else 38912,direction,1,60,1,delta),(4,1,1,4,1,4))]
  wait=store(0x42D9C7 if direction else 0x42DA45,VM+0x92E0,1);writes=writes+[wait] if direction else [wait]+writes
  check(e['handler'],edits,writes,8);need(len(e['ticks'])==61,'sixty real updates plus inactive successor')
  for steps in e['ticks']:tick(steps)
  b=bytes.fromhex(expected['work']);need(num(bytes.fromhex(expected['VM']),0x1C)==0,'VM PC remains bound and unplayed')
  outcomes.append(dict(opcode=op,updates=60,inactive_successors=1,final_value=num(b,0x2490),delta=delta,remaining=num(b,0x249C),status=b[0x249A],VM_wait=bytes.fromhex(expected['VM'])[0x92E0]))
 need(w['after']==expected,'complete work experiment final state')
 return outcomes


def finalization(row,outcome):
 f=row['finalization'];a,b=(expand(f[k],row['blobs']) for k in ('before','after'));last=row['work']['after']
 need(all(a[k]==last[k] for k in ('VM','task','units','remaining','elapsed')) and a['work']==last['work'][:6],'same work end enters explicit original result input root')
 data=bytearray.fromhex(a['result']);record=bytes.fromhex(a['records'][1]);score=num(bytes.fromhex(a['counters']),0,'h')
 need(a['remaining']==outcome['remaining'] and a['elapsed']==outcome['elapsed'],'pause freezes combat clock throughout supplemental work updates')
 selector=num(bytes.fromhex(a['task']),0x174);need(selector==outcome['selector'],'original selection retained')
 elapsed=row['input']['limit']-a['remaining'];t1,t2=num(data,0x4AC),num(data,0x4B0);grade=0 if t1==0 else 1 if elapsed<=t1 else 2 if elapsed<=t2 else 3
 struct.pack_into('<hhhh',data,0x50C,selector,grade,2 if outcome['no_hostile'] else 1,score)
 for j in range(20):data[0x518+j*0xB0+0xAA:0x518+j*0xB0+0xAF]=bytes(5)
 data[0x518+0xB0+0xAA:0x518+0xB0+0xAF]=record[0xAA:0xAF]
 need(bytes.fromhex(b['result'])==data,'independent entire result page after actual pause/work contracts')
 need(all(a[k]==b[k] for k in a if k!='result'),'result input root preserves work-derived end state')
