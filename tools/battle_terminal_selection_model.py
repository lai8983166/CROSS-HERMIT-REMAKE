"""Independent scene-4 branch, five-instruction condition VM and result contracts."""
import struct
from tools.battle_terminal_selection_emulation import (ROOT,SOURCE,CTRL,UNIT,TASK,VM,SCRIPT,SCRIPT_PATH,
 combat,package_offsets,vm_offsets,need)


def num(b,at,f='i'):return struct.unpack_from('<'+f,b,at)[0]


def outcome(c):
 p=combat(c['combat']);r=[bytes.fromhex(next(s for s in p['final'] if s['pointer']==0x11200000)['hex'])[i*256:(i+1)*256] for i in (0,1)]
 hostile=r[0][15]==1 and p['input']['relation']==1
 dead=r[1][15]!=1
 raw=bytes.fromhex(p['final'][0]['hex']);deaths=struct.unpack_from('<b',raw,0x2EF34)[0]
 if not hostile:sub=2 if deaths==0 else 5
 elif c['remaining']==0:sub=11
 elif dead:sub=14
 else:sub=None
 table=SOURCE.read_bytes();selector=0 if sub is None else num(table,0x60CA7C-0x400000+sub*4)
 return dict(sub=sub,selector=selector,no_hostile=not hostile,own_dead=dead,own_deaths=deaths,records=r,
  score=num(raw,0x2EF14,'h'))


def program(sub):
 """Execute the sourced condition path without reading emulator results."""
 raw=(ROOT/SCRIPT_PATH).read_bytes();_,g=package_offsets(raw);_,s=package_offsets(raw,g[0]);start,end=g[0]+s[sub],g[0]+s[sub+1]
 offsets=vm_offsets(raw,start,end);lo,hi=start+offsets[0],start+offsets[1];pc=0;regs=[0]*50;work=[0,0,1];commands=[]
 def operand(v):
  kind,index=v>>28,v&0xFFFFFFF
  if kind==0 and index<50:return regs[index]
  if kind==2:return index
  raise ValueError('unsupported original condition operand')
 for _ in range(8):
  at=lo+pc;need(lo<=at<=hi-4,'condition instruction bounds');op,advance=struct.unpack_from('<HH',raw,at);need(4<=advance<=hi-at,'condition instruction size')
  commands.append(dict(pointer=SCRIPT+at,opcode=op,advance=advance,pc=pc,work=bytes(work).hex()))
  if op==167:
   target=num(raw,at+4,'I');need(target<50 and advance==8,'condition query variable');regs[target]=work[0]
  elif op==8:
   operator,left,right,target=struct.unpack_from('<4I',raw,at+4);need(operator==1 and advance==20,'condition equality');
   if operand(left)==operand(right):pc=target;continue
  elif op==166:need(advance==8,'condition set size');work[1]=int(operand(num(raw,at+4,'I'))!=0)
  elif op==11:need(advance==8,'condition jump size');pc=num(raw,at+4,'I');continue
  elif op==19:need(advance==4,'condition END size');return commands,work[1],(start,end)
  else:raise ValueError('undeclared sourced condition opcode')
  pc+=advance
 raise ValueError('condition instruction bound')


def verify(row):
 c=row['input'];o=outcome(c);before=row['event']['before'];after=row['event']['after'];calls=row['calls']
 expected=bytearray.fromhex(before['task']);need(num(expected,0x174)==0 and expected[0x43]==0,'unselected task input')
 selected=[e for e in calls if e['entry']==0x454AF0];conditions=[e for e in calls if e['entry']==0x4551C0];requests=[e for e in calls if e['entry']==0x4549D0]
 if o['sub'] is None:
  need(not selected and not conditions and not requests and not row['commands'],'no premature terminal request');need(bytes.fromhex(after['work'])==bytes(3),'unused work input remains')
 else:
  sub=o['sub'];need(len(selected)==len(conditions)==len(requests)==1,'one original condition and request')
  need(selected[0]['args']==[sub,sub] and selected[0]['receiver']==TASK and selected[0]['caller']==0x454ADD,'original selected request caller')
  need(conditions[0]['args']==[0,sub] and conditions[0]['caller']==0x454BDD and conditions[0]['result']==1,'original complete condition return')
  commands,result,span=program(sub);need(result==1 and row['commands']==commands,'independent sourced five-instruction condition execution')
  need(requests[0]['args']==[0,0,sub,1,0,1,1] and requests[0]['caller']==0x454BFD and requests[0]['receiver']==TASK,'original request fields')
  expected[0x43]=1;expected[0x44:0x60]=bytes(28)
  struct.pack_into('<4I',expected,0x48,1,1,0,1);expected[0x59]=1
  struct.pack_into('<I',expected,0x174,o['selector']);need(after['work']=='010101','original condition outcome and mode retained')
  binds=[e for e in calls if e['entry']==0x455060]
  need([e['args'] for e in binds]==[[0,sub],[0,sub+1],[0,sub],[0,sub+1]],'original directory accesses for check and binding')
  need([e['result'] for e in binds]==[SCRIPT+span[0],SCRIPT+span[1]]*2,'independent nested directory pointer selection')
 need(bytes.fromhex(after['task'])==expected,'complete independent task prefix after event')
 for k in ('records','counters','remaining','elapsed'):
  need(before[k]==after[k]==row['finalization']['after'][k],'combat-derived input unchanged '+k)
 no_hostile_calls=[e for e in calls if e['entry']==0x4307B0];need(len(no_hostile_calls)==2 and all(e['result']==int(o['no_hostile']) for e in no_hostile_calls),'independent hostile survival predicates in event and finalizer')
 casualties=[e for e in calls if e['entry']==0x430BA0];need([e['result'] for e in casualties]==([int(o['own_deaths']==0)] if o['no_hostile'] else []),'independent own death predicate')
 annihilation=[e for e in calls if e['entry']==0x430DF0];need([e['result'] for e in annihilation]==([int(o['own_dead'])] if not o['no_hostile'] and c['remaining'] else []),'independent all-own incapacitated predicate')
 # VM cleanup initializes these original thread-short fields, including
 # any falling inside the result pages; all remaining event result bytes stay.
 result=bytearray.fromhex(before['result'])
 if o['sub'] is not None:
  for i in range(14,56):
   at=VM+0x446+i*0xAB8
   if 0x7F4000<=at<0x7F6000:struct.pack_into('<H',result,at-0x7F4000,0)
 need(bytes.fromhex(after['result'])==result,'independent result-data bytes across condition VM')
 f=row['finalization'];need(f['before']==after,'same state enters result finalization')
 struct.pack_into('<hhh',result,0x50C,o['selector'],1,2 if o['no_hostile'] else 1);struct.pack_into('<h',result,0x512,o['score'])
 for j in range(20):result[0x518+j*0xB0+0xAA:0x518+j*0xB0+0xAF]=bytes(5)
 record=o['records'][1];need(num(result,0x518+0xB0,'H')==num(record,0,'H') and num(result,0x51A+0xB0,'H')==num(record,2,'H'),'original output slot identity')
 result[0x518+0xB0+0xAA:0x518+0xB0+0xAF]=record[0xAA:0xAF]
 need(bytes.fromhex(f['after']['result'])==result,'independent whole result-data pages from actual selection and combat')
 for k in f['before']:
  if k!='result':need(f['before'][k]==f['after'][k],'result finalizer preserves '+k)
 return dict(sub=o['sub'],selector=o['selector'],no_hostile=o['no_hostile'],own_dead=o['own_dead'],score=o['score'],player_kills=num(record,0xAA,'h'),player_contribution=num(record,0xAC,'h'),player_deaths=record[0xAE])
