"""Independent local contracts from explicitly observed function-entry inputs.

This is deliberately not a whole-world predictive model. No expected output is
copied from an original return; records/positions/seeds at ENTRY are the inputs.
"""
import struct
from tools.battle_hit_damage import Random,physical,signed,div
from tools.battle_target_acquisition import choose,candidate,case,inputs as target_inputs
from tools.battle_attack_animation import basic
from tools.battle_region_routing import inputs as map_inputs
from tools.battle_bilateral_combat_emulation import CTRL,UNIT,TARGET,SOURCE,need

UNITS=(UNIT,TARGET)
SOURCE_BYTES=SOURCE.read_bytes()


def number(b,o,fmt='h'):return struct.unpack_from('<'+fmt,b,o)[0]
def bytes_at(s,k,i):return bytes.fromhex(s[k][i])
def cell(u):return div(number(u,0x2EC,'i')>>16,32),div(number(u,0x2F0,'i')>>16,16)


def snapshot(record,unit):
    b=bytearray(44)
    for dst,src,n in ((0,0x3A,2),(2,0x3C,2),(4,0x38,2),(8,0x4C,1),(9,0x4D,1),(10,0x50,1),(11,0x4F,1),(12,0x4E,1),(0x24,0x52,2)):b[dst:dst+n]=record[src:src+n]
    x,y=cell(unit);data=map_inputs();need(0<=x<64 and 0<=y<96,'bounded source terrain cell')
    t=data['logical'][16+(y*64+x)*6];coefs=struct.unpack_from('<3i',data['terrain'],t*76+16+record[0x30]*12)
    struct.pack_into('<3i',b,0x10,*coefs);return b


def hit_contract(e):
    ai,vi=[UNITS.index(u) for u in e['args'][:2]];need(ai!=vi,'two different combat roles')
    s=e['before'];ar,vr=bytes_at(s,'records',ai),bytes_at(s,'records',vi);au,vu=bytes_at(s,'units',ai),bytes_at(s,'units',vi)
    a,d=snapshot(ar,au),snapshot(vr,vu);ev,armor=struct.unpack_from('<2i',d,0x10)
    rng=Random(s['battle_seed']);cfg=dict(power=number(ar,0x3A,'H'),spread=number(ar,0x3C,'H'),accuracy=number(ar,0x38,'H'),evasion=vr[0x4C],armor=vr[0x4D],mental=number(vr,0x52,'H'))
    hit=physical(cfg,ev,armor,rng);struct.pack_into('<i',a,0x28,hit['damage'])
    expected=dict(kind=hit['kind'],attack=a.hex(),defense=d.hex(),seed=rng.seed,draws=s['battle_draws']+rng.count)
    need(e['resolved']==expected,'independent two-sided physical snapshots, damage and RNG')
    result=1 if hit['kind'] and vu[6] else hit['kind'];delta=signed(-hit['damage'],16);skill=basic(number(ar,0xC,'H'))
    packet=bytearray.fromhex(e['input_packet']);need(len(packet)==12 and number(packet,4)==skill and packet[2:4]==bytes([ai,vi]),'original attack packet identity and basic skill')
    packet[6]=result;struct.pack_into('<h',packet,10,delta)
    effect=None
    if result:
        g=number(SOURCE_BYTES,0x213B78+skill*6+{1:2,2:2,3:4,4:0}[result])
        if g in (2001,2007,2012,2018,2023,2029,2052,2057):g+=rng.next()%5
        effect=g
        need(bytes_at(e['after'],'units',vi)[0xE8:0xF4]==packet,'independent victim effect packet')
    need((e['after']['battle_seed'],e['after']['battle_draws'])==(rng.seed,s['battle_draws']+rng.count),'independent physical plus effect-variant random stream')
    return dict(attacker=UNITS[ai],victim=UNITS[vi],frame=e['frame'],kind=hit['kind'],event_kind=result,damage32=hit['damage'],delta16=delta,effect=effect)


def scan_contract(e,c):
    ai=UNITS.index(e['args'][0]);vi=1-ai;s=e['before'];au,vu=bytes_at(s,'units',ai),bytes_at(s,'units',vi);ar,vr=bytes_at(s,'records',ai),bytes_at(s,'records',vi)
    counter=signed(number(au,0x2D4,'i')+1);selected=None
    if counter>=number(au,0x2B8,'i'):
        counter=0;relations=[0]*16;relations[vr[0xA4]]=c['relation']
        p=candidate(vi,cell=list(cell(vu)),faction=vr[0xA4],state=vu[0x290],record_id=number(vr,2,'H'),alive=vr[15],hp=number(vr,0x16),max_hp=number(vr,0x14))
        selected=choose(case('boundary',scope=signed(au[0x2BC],8),policy=signed(au[0x2BD],8),candidates=[p],actor_faction=ar[0xA4],relations=relations),cell(au))
    need(e['result']==(UNITS[vi] if selected else 0),'independent bilateral search result')
    need(number(bytes_at(e['after'],'units',ai),0x2D4,'i')==counter,'independent bilateral scan cadence')
    return bool(selected)


def apply_delta(old,maximum,threshold,delta):
    value=min(32767,signed(old+delta))
    if threshold and value<=0 and delta<0 and old>=threshold and -delta>=threshold:value=1
    return 0 if value<0 else min(maximum,value)


def hp_contract(e):
    i=UNITS.index(e['args'][0]);before=bytes_at(e['before'],'records',i);after=bytes_at(e['after'],'records',i);expected=bytearray(before);stores=[]
    for node in e['before']['queues'][i]:
        data=bytes.fromhex(node['hex']);need(data[0]&128 and data[1]==0,'declared physical HP queue type')
        hp=apply_delta(number(expected,0x16),number(expected,0x14),number(expected,0x54,'H'),number(data,2));struct.pack_into('<h',expected,0x16,hp);stores.append(hp&65535)
    need(after==expected,'independent entire record after HP queue application')
    need(not e['after']['queues'][i] and number(bytes_at(e['after'],'units',i),0x510,'I')==0,'original HP queue fully consumed')
    return stores


def regen_contract(e):
    i=UNITS.index(e['args'][0]);rec=bytearray.fromhex(e['before']['records'][i]);unit=bytes_at(e['before'],'units',i);out=bytes_at(e['after'],'units',i);stores=[]
    for off,cap,interval,counter in ((0x16,0x14,0x18,0x504),(0x1C,0x1A,0x1E,0x506)):
        value,maximum=number(rec,off),number(rec,cap);count=0
        if (off!=0x16 or value!=0) and value<maximum:
            count=signed(number(unit,counter)+1,16);rate=number(rec,interval)
            if count>=max(1 if rate<0 else 0,rate):
                count=0;value=max(0,min(maximum,min(32767,value+1)));struct.pack_into('<h',rec,off,value)
                if off==0x16:stores.append(value&65535)
        need(number(out,counter)==count,'independent per-unit recovery counter')
    need(bytes_at(e['after'],'records',i)==rec,'independent whole regenerated record');return stores


def ai_contract(e):
    i=UNITS.index(e['args'][0]);a=bytes_at(e['before'],'units',i);b=bytes_at(e['after'],'units',i);r=bytes_at(e['before'],'records',i);entry=e['entry']
    if entry==0x475270:
        need(e['caller'] in (0x4763AA,0x47654C,0x4778E2,0x4786C5,0x47CF8A,0x47B9E0),'declared natural ordinary AI request caller')
        need(b[0x292]==e['args'][1] and e['args'][1] in (6,15,19),'original requested command stored')
    elif entry==0x4751F0:
        expected=bytes([a[0x292],a[0x290],0,0]) if a[0x292] else a[0x290:0x294]
        need(b[0x290:0x294]==expected,'independent pending request consumption')
    elif entry==0x476250:
        phase=a[0x293];pending=a[0x292];seed=e['before']['battle_seed'];draws=e['before']['battle_draws']
        if phase==0:phase=2
        elif phase==2:
            threshold=60
            if r[0xA4]>=4:
                rng=Random(seed);threshold=30+20*(rng.next()%10);seed=rng.seed;draws+=1
            if number(a,0xA)>threshold:pending=15;phase=3
        need((b[0x293],b[0x292])==(phase,pending),'independent player/enemy idle decision')
        need((e['after']['battle_seed'],e['after']['battle_draws'])==(seed,draws),'independent idle random threshold')
    elif entry==0x476470:need(b[0x2A7]==1 and b[0x292]==19,'ordinary decision naturally requests scan')
    elif entry==0x47C580:
        j=UNITS.index(e['args'][1]);target=bytes_at(e['before'],'units',j)
        need(number(b,0x4EE)==j and number(b,0x4F2)==basic(number(r,0xC,'H')) and tuple(b[0x4F0:0x4F2])==cell(target),'independent reverse-role target/skill/coordinate binding')
    elif entry==0x477980 and a[0x293]==24:
        if r[0xA4]>=4:need(b[0x292]==15 and number(b,0x4EE)==number(b,0x4F2)==-1,'enemy recovery clears and replans')
        else:
            # The basic type2 re-entry check uses detection range, not the
            # attack range. In this two-faction fixture there are no allied
            # supporters; the second search can only reconsider self.
            j=number(a,0x4EE);target=bytes_at(e['before'],'units',j);x,y=cell(a);tx,ty=cell(target)
            mask=target_inputs()['masks'][r[0x2C]];w,h=mask['width'],mask['height'];dx,dy=abs(tx-x),abs(ty-y);rx,ry=div(w-1,2),div(h-1,2)
            reuse=dx<=rx and dy<=ry and bool(bytes.fromhex(mask['hex'])[(dy+ry)*w+dx+rx])
            if reuse:need(b[0x293]==0 and b[0x292]==0 and b[0x4EE:0x4F4]==a[0x4EE:0x4F4],'player in-detection recovery restarts attack')
            else:need(b[0x292]==15 and number(b,0x4EE)==number(b,0x4F2)==-1,'player outside detection clears and replans')


def damage_contract(e):
    i=UNITS.index(e['args'][0]);a=bytes_at(e['before'],'units',i);b=bytes_at(e['after'],'units',i)
    if not number(a,0xE0,'I'):return None
    p=a[0xE8:0xF4];result=p[6];delta=number(p,10)
    need(not number(b,0xE0,'I'),'natural received damage event consumed')
    need(number(bytes_at(e['after'],'records',i),0xA6,'H')==p[2],'original damage attributed to other unit index')
    if result!=4 or delta>0:
        q=e['after']['queues'][i];need(q and number(bytes.fromhex(q[0]['hex']),2)==delta,'independent effect packet to HP queue delta')
    return dict(victim=UNITS[i],attacker_index=p[2],frame=e['frame'],kind=result,delta=delta)
