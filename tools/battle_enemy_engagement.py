"""Finite autonomous ordinary enemy engagements through complete world roots."""
from copy import deepcopy
from tools.battle_world_combat import corpus as parent_corpus,pages,expand,validate_pages
from tools.battle_combat_aftermath import validate as validate_aftermath
from tools.battle_pathfinding_emulation import need,sha


def corpus():
    base=parent_corpus();rows=[]
    for j,c in enumerate(base[:4],1):
        a=deepcopy(c['aftermath']);a['combat'].update(hp=1000,max_hp=1000,evasion=0,mental=1000)
        rows.append(dict(name='enemy_job'+str(j),aftermath=a,scope=0,relation=1,budget=384,rounds=2))
    for name,scope,relation in [('neutral_relation',0,0),('search_disabled',2,1)]:
        c=deepcopy(rows[0]);c.update(name=name,scope=scope,relation=relation,budget=96,rounds=0);rows.append(c)
    return rows


def validate(c):
    need(set(c)=={'name','aftermath','scope','relation','budget','rounds'},'exact enemy engagement input')
    validate_aftermath(c['aftermath'])
    need(type(c['name']) is str and c['name'] and type(c['budget']) is int and 1<=c['budget']<=384,'bounded enemy world frames')
    need(type(c['scope']) is int and c['scope'] in (0,2) and type(c['relation']) is int and c['relation'] in (0,1),'declared search/relation')
    need(type(c['rounds']) is int and c['rounds'] in (0,2) and bool(c['rounds'])==(c['scope']==0 and c['relation']==1),'two rounds or no attack control')
    x=c['aftermath']['combat'];need(x['hp']==x['max_hp']==1000 and x['evasion']==0 and x['mental']==1000,'living passive player target declaration')


def declarations(c):
    from tools.battle_world_combat_emulation import CTRL,UNIT,RECORD
    return [(RECORD+0xA4,4,'B'),(RECORD+0x1A4,0,'B'),(UNIT+0x290,2,'B'),
            (UNIT+0x4EE,-1,'h'),(UNIT+0x4F2,-1,'h'),(UNIT+0x2BC,c['scope'],'b'),
            (CTRL+0x115AAC+4*16,c['relation'],'B')]


def completed_round(get,previous):
    from tools.battle_world_combat_emulation import UNIT
    now=(get(UNIT+0x290,'B'),get(UNIT+0x293,'B'))
    return now,now==(6,24) and previous!=(6,24)
