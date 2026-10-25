"""Independent live HP/RNG/death ledger, world clock and scene-4 contracts."""
import struct
from tools import battle_lethal_combat_model as combat
from tools.battle_lethal_combat import expand
from tools.battle_terminal_selection_model import program
from tools.battle_live_terminal_emulation import CTRL,UNIT,TARGET,RECORD,TASK,VM,need


def num(b,at,f='i'):return struct.unpack_from('<'+f,b,at)[0]
def ledger(records):return [[combat.number(r,o,f) for o,f in ((0xAA,'h'),(0xAC,'h'),(0xAE,'b'),(15,'B'),(0x24,'i'))] for r in records]


def world_contracts(row):
 c=row['combat_input'];rng=combat.Random(c['aftermath']['combat']['seed']);crt=c['aftermath']['combat']['crt_seed'];crt_draws=0
 hp=[70 if i==c['victim'] else 1000 for i in (0,1)];expected_ledger=[[0,0,0,1,100],[0,0,0,1,100]];stats=bytes(0x30);stores=[];hits=[];received=[]
 by_frame=[[] for _ in row['world_frames']]
 for e in row['contracts']:
  need(type(e['frame']) is int and 0<=e['frame']<len(by_frame) and 'after' in e,'complete natural world contract');by_frame[e['frame']].append(e)
 for i,f in enumerate(row['world_frames']):
  before=expand(f['before'],row['blobs']);need([num(bytes.fromhex(before[k]),0x16,'h') for k in ('record','target_record')]==hp,'continuous pre-world HP from prior contracts')
  for e in by_frame[i]:
   at=e['entry']
   if at==0x467E00:
    need((e['before']['battle_seed'],e['before']['battle_draws'])==(rng.seed,rng.count),'continuous battle RNG input');value=rng.next();need((e['result'],e['after']['battle_seed'],e['after']['battle_draws'])==(value,rng.seed,rng.count),'independent battle RNG')
   elif at==0x570FE0:
    need(e['before']['CRT_seed']==crt,'continuous CRT input');crt=(crt*0x343FD+0x269EC3)&0xFFFFFFFF;crt_draws+=1;need(e['result']==(crt>>16)&32767 and e['after']['CRT_seed']==crt,'independent CRT RNG')
   elif at==0x48AAE0:hits.append(combat.hit_contract(e))
   elif at==0x47A920:combat.scan_contract(e,c)
   elif at in (0x493450,0x472370):
    side=combat.UNITS.index(e['args'][0]);need(combat.number(combat.bytes_at(e['before'],'records',side),0x16)==hp[side],'continuous HP boundary input')
    values=(combat.hp_contract if at==0x493450 else combat.regen_contract)(e)
    stores.extend(dict(frame=i,pc=0x472658,address=RECORD+side*256+0x16,bytes=2,value=v) for v in values)
    if values:hp[side]=combat.signed(values[-1],16)
   elif at==0x4918D0:
    r=combat.damage_contract(e)
    if r:received.append(r)
   elif at in (0x4799C0,0x479F40,0x46BA10,0x472770,0x475370):
    records,st=combat.death_contract(e)
    if at in (0x4799C0,0x479F40):
     need(ledger([bytes.fromhex(r) for r in e['before']['records']])==expected_ledger and bytes.fromhex(e['before']['death_stats'])==stats,'continuous independent death/kill ledger input')
     expected_ledger=ledger(records);stats=bytes(st)
   else:combat.ai_contract(e)
  after=expand(f['after'],row['blobs']);records=[bytes.fromhex(after[k]) for k in ('record','target_record')]
  need([num(r,0x16,'h') for r in records]==hp and ledger(records)==expected_ledger,'whole world HP and kill/death records from original contracts')
  need(bytes.fromhex(after['world_stats'])[0x800:]==stats,'independent whole-frame persistent faction scores')
  need((after['battle_seed'],after['battle_draws'],after['CRT_seed'])==(rng.seed,rng.count,crt),'every original random state connected')
 need(row['both_hp_writes']==stores,'every original HP store derives independently')
 need(len(hits)==len(received),'all hit packets consumed before live frontier')
 for victim in (UNIT,TARGET):
  hs=[h for h in hits if h['victim']==victim];rs=[r for r in received if r['victim']==victim];need(len(hs)==len(rs),'per-victim original hit delivery')
  for h,r in zip(hs,rs):need(r['attacker_index']==combat.UNITS.index(h['attacker']) and r['delta']==h['delta16'] and h['frame']<=r['frame']<=h['frame']+1,'original hit/received identity and delay')
 return dict(HP=hp,hits_by_side=[sum(h['attacker']==u for h in hits) for u in (UNIT,TARGET)],CRT_draws=crt_draws,battle_draws=rng.count)


def event_contract(row,index):
 f=row['world_frames'][index];e=row['events'][index];blobs=row['blobs'];before=expand(e['before'],blobs);after=expand(e['after'],blobs)
 wb,wa=expand(f['before'],blobs),expand(f['after'],blobs);need(wa['terminal_state']==before,'same live world output enters event')
 records=[bytes.fromhex(r) for r in before['records']];previous=[bytes.fromhex(wb[k]) for k in ('record','target_record')]
 need(before['records']==[wa[k] for k in ('record','target_record')],'actual event records bound to world')
 # 46E730 builds active and inactive lists before this world's unit updates.
 expected_active=[u for u,r in zip((UNIT,TARGET),previous) if r[15]==1];raw=bytes.fromhex(wa['world_fields'][hex(CTRL+0xDC30C)])
 n=num(raw,0x5E0,'I');need(n==len(expected_active) and list(struct.unpack_from('<'+str(n)+'I',raw,0x5E4))==expected_active,'independent pre-unit active list')
 expected_inactive=[u for u,r in zip((UNIT,TARGET),previous) if r[15] in (0,2,3,4,5)];n=num(raw,0x9CC,'I')
 need(n==len(expected_inactive) and list(struct.unpack_from('<'+str(n)+'I',raw,0x9D0))==expected_inactive,'independent inactive list from original record-state predicate')
 need(all(records[(u-UNIT)//0x520][15]!=0 for u in expected_inactive),'this corpus inactive records do not represent pending entrants')
 no_hostile=not(UNIT in expected_active and row['combat_input']['relation']==1)
 own_dead=records[1][15] in (0,2,3,4,5);deaths=struct.unpack_from('<b',bytes.fromhex(before['counters']),0x20)[0]
 remaining=max(0,row['input']['limit']-index-1);need(before['remaining']==after['remaining']==remaining and before['elapsed']==after['elapsed']==index+1,'original frame clock decrements/counts without host writes')
 if no_hostile:sub=2 if deaths==0 else 5
 elif remaining==0:sub=11
 elif own_dead:sub=14
 else:sub=None
 selector=0 if sub is None else {2:1,5:2,8:3,11:4,14:5}[sub]
 calls=row['calls'][slice(*e['calls'])];selected=[x for x in calls if x['entry']==0x454AF0];conditions=[x for x in calls if x['entry']==0x4551C0];requests=[x for x in calls if x['entry']==0x4549D0]
 task=bytearray.fromhex(before['task']);need(num(task,0x174)==0 and task[0x43]==0,'unselected fresh task before first terminal event')
 if sub is None:need(not selected and not conditions and not requests,'no premature event request')
 else:
  need(len(selected)==len(conditions)==len(requests)==1,'one natural terminal condition and request')
  need(selected[0]['args']==[sub,sub] and selected[0]['receiver']==TASK and selected[0]['caller']==0x454ADD,'original terminal selected branch')
  need(conditions[0]['args']==[0,sub] and conditions[0]['result']==1,'original condition VM result')
  commands,result,span=program(sub);need(result==1 and row['commands']==commands,'independent sourced condition instructions')
  need(requests[0]['args']==[0,0,sub,1,0,1,1] and requests[0]['receiver']==TASK,'original task request initialization')
  task[0x43]=1;task[0x44:0x60]=bytes(28);struct.pack_into('<4I',task,0x48,1,1,0,1);task[0x59]=1;struct.pack_into('<I',task,0x174,selector)
 need(bytes.fromhex(after['task'])==task,'independent whole task prefix')
 for k in ('records','units','counters'):need(before[k]==after[k],'event preserves actual live combat '+k)
 need([x['result'] for x in calls if x['entry']==0x4307B0]==[int(no_hostile)],'original hostile predicate matches independent list/relations')
 need([x['result'] for x in calls if x['entry']==0x430BA0]==([int(deaths==0)] if no_hostile else []),'original casualty predicate')
 need([x['result'] for x in calls if x['entry']==0x430DF0]==([int(own_dead)] if not no_hostile and remaining else []),'original own annihilation predicate')
 result=bytearray.fromhex(before['result'])
 if sub is not None:
  for j in range(14,56):
   at=VM+0x446+j*0xAB8
   if 0x7F4000<=at<0x7F6000:struct.pack_into('<H',result,at-0x7F4000,0)
 need(bytes.fromhex(after['result'])==result,'independent event result-page preservation and VM thread flags')
 return dict(sub=sub,selector=selector,no_hostile=no_hostile,own_dead=own_dead,remaining=remaining,elapsed=index+1)


def finalization_contract(row,outcome):
 e=row['finalization'];a,b=expand(e['before'],row['blobs']),expand(e['after'],row['blobs']);need(a==expand(row['events'][-1]['after'],row['blobs']),'same final event output enters original result root')
 data=bytearray.fromhex(a['result']);selector=num(bytes.fromhex(a['task']),0x174);need(selector==outcome['selector'],'actual final selector from event')
 elapsed=row['input']['limit']-outcome['remaining'];t1=num(data,0x4AC);t2=num(data,0x4B0);grade=0 if t1==0 else 1 if elapsed<=t1 else 2 if elapsed<=t2 else 3
 record=bytes.fromhex(a['records'][1]);score=num(bytes.fromhex(a['counters']),0,'h')
 struct.pack_into('<hhhh',data,0x50C,selector,grade,2 if outcome['no_hostile'] else 1,score)
 for j in range(20):data[0x518+j*0xB0+0xAA:0x518+j*0xB0+0xAF]=bytes(5)
 need(num(data,0x518+0xB0,'H')==num(record,0,'H') and num(data,0x51A+0xB0,'H')==num(record,2,'H'),'actual player result slot identity')
 data[0x518+0xB0+0xAA:0x518+0xB0+0xAF]=record[0xAA:0xAF];need(bytes.fromhex(b['result'])==data,'independent complete result pages from live battle')
 for k in a:
  if k!='result':need(a[k]==b[k],'result root preserves '+k)
 return dict(time_key=grade,score=score,player_kills=num(record,0xAA,'h'),player_contribution=num(record,0xAC,'h'),player_deaths=record[0xAE],record_liveness=[bytes.fromhex(r)[15] for r in a['records']],commands=[bytes.fromhex(u)[0x290] for u in a['units']])
