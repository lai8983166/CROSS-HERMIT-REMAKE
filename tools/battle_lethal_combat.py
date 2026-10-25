"""Autonomous two-sided lethal exchanges and real result-input declarations."""
from copy import deepcopy
from tools.battle_bilateral_combat import corpus as previous_corpus,validate as previous_validate,pages,expand,validate_pages
from tools.battle_pathfinding_emulation import need


def base_input(c):return {k:deepcopy(v) for k,v in c.items() if k not in ('victim','survival')}


def corpus():
    rows=[]
    for job in (1,3):
        for victim in (0,1):
            c=deepcopy(previous_corpus()[job-1]);c.update(name=('enemy' if victim==0 else 'player')+'_dies_job'+str(job),victim=victim,survival=False);rows.append(c)
    c=deepcopy(rows[1]);c.update(name='player_threshold_survives',survival=True,budget=256);rows.append(c)
    c=deepcopy(previous_corpus()[4]);c.update(name='neutral_living_control',victim=1,survival=False);rows.append(c)
    return rows


def validate(c):
    need(set(c)==set(corpus()[0]),'exact lethal input');previous_validate(base_input(c))
    need(type(c['victim']) is int and c['victim'] in (0,1) and type(c['survival']) is bool,'explicit death role and threshold')


def declarations(c):
    from tools.battle_bilateral_combat_emulation import CTRL,UNIT,TARGET,RECORD
    rows=[(0x7F4491,0,'B'),(0x7F44AC,600,'i'),(0x7F44B0,1200,'i'),(0x7F45CA,11,'H'),(0x7F45C8,1,'H'),(0x12700000+0x174,0,'h')]
    # Output identity uses unit slot1 (not record-ID-as-slot); it is declared
    # before any root and asserted by the original finalization function.
    rows[-3]=(0x7F451A+0xB0,11,'H');rows[-2]=(0x7F4518+0xB0,1,'H')
    rows.extend((0x7F44BE+i,0,'B') for i in range(16))
    for i in (0,1):
        r=RECORD+i*256;hp=70 if i==c['victim'] else 1000
        rows.extend((r+o,v,f) for o,v,f in [(0,i,'H'),(0x14,hp,'h'),(0x16,hp,'h'),(0x18,32767,'h'),(0x24,100,'i'),
            (0x54,1 if c['survival'] and i==c['victim'] else 0,'H'),(0xA6,0,'H'),(0xA8,20,'h'),(0xAA,0,'h'),(0xAC,0,'h'),(0xAE,0,'b')])
    rows.extend((CTRL+0x2EF14+o,0,'B') for o in range(0x31))
    return rows


def done(get,c,index):
    from tools.battle_bilateral_combat_emulation import UNIT,RECORD
    if c['survival'] or c['relation']==0:return index==c['budget']-2
    return get(RECORD+c['victim']*256+0xF,'B')==4 and get(UNIT+c['victim']*0x520+0x290,'B')==11
