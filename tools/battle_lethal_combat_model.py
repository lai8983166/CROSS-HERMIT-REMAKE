"""Independent death/ledger/removal and result-input boundary contracts."""
import struct
from tools import battle_bilateral_combat_model as prior
from tools.battle_bilateral_combat_model import number,bytes_at,cell,UNITS,hit_contract,hp_contract,regen_contract,damage_contract,Random,signed,div
from tools.battle_lethal_combat_emulation import need,UNIT,RECORD,parent


def scan_contract(e,c):
    # Original world work list contains live state1 records. A nonzero state4
    # record must not be fabricated as a candidate merely because bool(4).
    def choose_live(cfg,position):
        cfg=dict(cfg,candidates=[p for p in cfg['candidates'] if p['alive']==1]);return prior.choose(cfg,position)
    import types
    f=types.FunctionType(prior.scan_contract.__code__,dict(prior.scan_contract.__globals__,choose=choose_live));return f(e,c)


def ai_contract(e):
    if e['entry']==0x475270:
        c=e['caller'];raw=parent.parent.CODE;off=c-5-0x400000
        need(raw[off]==0xE8 and c+number(raw,off+1,'i')==0x475270,'actual original direct request caller')
        i=UNITS.index(e['args'][0]);need(e['args'][1] in (2,6,13,15,19) and bytes_at(e['after'],'units',i)[0x292]==e['args'][1],'original natural command request');return
    return prior.ai_contract(e)


def max_add(buf,offset,add,fmt):
    old=number(buf,offset,fmt);bits=8 if fmt=='b' else 16;candidate=signed(old+add,bits)
    if candidate>old:struct.pack_into('<'+fmt,buf,offset,candidate)


def death_contract(e):
    side=UNITS.index(e['args'][0]);a=bytes_at(e['before'],'units',side);b=bytes_at(e['after'],'units',side)
    records=[bytearray.fromhex(r) for r in e['before']['records']];stats=bytearray.fromhex(e['before']['death_stats']);r=records[side];entry=e['entry']
    if entry==0x472770:
        pending=number(r,0x16)<=0 and a[0x290]!=13
        need(e['result']==int(pending),'independent original death-request predicate')
        need(b[0x292]==(13 if pending else a[0x292]),'natural HP0 requests command13')
    elif entry==0x475370:
        need(e['caller']==0x479DDA and e['args'][1:]==[11,0xFFFFFFFF],'natural command11 removal request')
        need(b[0x290:0x294]==bytes((11,0,0,0)),'immediate inactive command transition')
    elif entry==0x46BA10:
        need(e['caller'] in (0x479CEC,0x479D0A),'death removal is nested in command13')
        need(e['after']['occupied'][side]==(e['before']['occupied'][side]-1)&255,'exact single occupancy decrement')
        need(all(b[o]==255 for o in (0x4E5,0x4E6,0x4E9,0x4EA)),'removed unit has inactive grid history')
        need(number(b,0x4FE)==(900 if r[0xA4]<4 else 600),'player/enemy removal timeout differs')
        need(number(b,0x4EE)==number(b,0x4F2)==-1 and number(b,0x510,'I')==0,'removed target/skill/HP queue cleared')
        r[0x9D]=0
    elif entry==0x4799C0:
        phase=a[0x293]
        if phase==0:
            max_add(r,0xAE,1,'b');killer=number(r,0xA6);need(killer in (0,1) and killer!=side,'actual last attacker is other used slot')
            kr=records[killer];max_add(kr,0xAA,1,'h');max_add(kr,0xAC,number(r,0xA8),'h');max_add(stats,kr[0xA4]*2,number(r,0xA8),'h')
            stats[0x20+r[0xA4]]=(stats[0x20+r[0xA4]]+1)&255
            need(b[0x293]==1 and b[6]==b[7]==1,'death phase0 starts animation and flags')
        elif phase==1:
            need(b[0x293]==(2 if a[4] else 1),'death animation completion gates delay')
            if a[4]:need(number(b,0xA)==0,'death delay timer reset after animation')
        elif phase==2:
            remove=number(a,0xA)>70
            need(e['result']==int(remove),'strict greater-than70 death removal gate')
            if remove:
                r[15]=3;r[0x9D]=0
                if r[0xA4]<4 and 1<=number(r,2,'H')<=45:
                    lifetime=number(r,0x24,'i')
                    if lifetime<3600:struct.pack_into('<i',r,0x24,0);r[15]=4
                    else:struct.pack_into('<i',r,0x24,max(0,div(lifetime*50,100)))
                need(b[0x290]==11,'original death completes inactive command')
        else:raise ValueError('undeclared death phase')
    elif entry==0x479F40:
        # Normal hostile IDs10/11 are neither bases nor special death types.
        if r[15]==3 and r[0xA4]>=4:r[15]=4
    need([bytes.fromhex(x) for x in e['after']['records']]==records,'independent complete death/ledger records')
    need(bytes.fromhex(e['after']['death_stats'])==stats,'independent per-faction score/death counters')
    return records,stats


def result_contract(row):
    e=row['finalization'];before=e['before'];after=e['after'];blobs=row['blobs']
    from tools.battle_lethal_combat import expand
    a,b=expand(before,blobs),expand(after,blobs);expected=bytearray.fromhex(a['result_data']);records=[bytes.fromhex(a[k]) for k in ('record','target_record')]
    # Selectors are copied, never inferred from a death. Current task selector
    # remains0; immutable initial timer fields supply the elapsed grade input.
    ctrl=bytes.fromhex(next(r['hex'] for r in row['initial'] if r['pointer']==0x11000000))
    elapsed=number(ctrl,0x2E6FC,'i')-number(ctrl,0x2E6F4,'i');threshold1=number(expected,0x4AC,'i');threshold2=number(expected,0x4B0,'i')
    grade=0 if threshold1==0 else 1 if elapsed<=threshold1 else 2 if elapsed<=threshold2 else 3
    hostile_live=records[0][15]==1 and row['input']['relation']==1
    struct.pack_into('<hhh',expected,0x50C,0,grade,1 if hostile_live else 2)
    # Normal mode clears exactly AA/AC/AE for20 output records; faction0's
    # slot1 counters then come from the actual naturally produced player record.
    for j in range(20):expected[0x518+j*0xB0+0xAA:0x518+j*0xB0+0xAF]=bytes(5)
    r=records[1];need(number(expected,0x518+0xB0,'H')==number(r,0,'H') and number(expected,0x51A+0xB0,'H')==number(r,2,'H'),'original result identity inputs match actual slot1')
    expected[0x518+0xB0+0xAA:0x518+0xB0+0xAF]=r[0xAA:0xAF]
    score=number(bytes.fromhex(a['world_stats']),0x800);struct.pack_into('<h',expected,0x512,score)
    need(bytes.fromhex(b['result_data'])==expected,'independent entire original result-data pages')
    for key in a:
        if key!='result_data':need(a[key]==b[key],'supplemental finalization does not rewrite world state '+key)
    return dict(selector=0,time_key=grade,unit_condition=1 if hostile_live else 2,score=score,player_kills=number(r,0xAA),player_contribution=number(r,0xAC),player_deaths=r[0xAE])
