"""Finite two-sided ordinary combat declarations; no runtime game writes."""
from copy import deepcopy
from tools.battle_enemy_engagement import corpus as prior_corpus,validate as prior_validate,pages,expand,validate_pages
from tools.battle_pathfinding_emulation import need


def base_input(c):
    r={k:deepcopy(v) for k,v in c.items() if k!='player_active'}
    r['rounds']=2 if c['relation']==1 and c['scope']==0 else 0
    return r


def corpus():
    rows=[]
    for j,c in enumerate(prior_corpus()[:4],1):
        c=deepcopy(c);c.update(name='bilateral_job'+str(j),player_active=True);rows.append(c)
    for name,scope,relation,active in [('mutual_neutral',0,0,True),('both_search_disabled',2,1,True),('passive_player',0,1,False)]:
        c=deepcopy(rows[0]);c.update(name=name,scope=scope,relation=relation,player_active=active,rounds=2 if scope==0 and relation else 0,budget=384 if relation and scope==0 else 96);rows.append(c)
    return rows


def validate(c):
    need(set(c)==set(corpus()[0]),'exact bilateral input')
    prior_validate(base_input(c));need(type(c['player_active']) is bool,'explicit player autonomy')


def declarations(c):
    from tools.battle_enemy_engagement_emulation import CTRL,UNIT,TARGET,RECORD
    result=[(CTRL+0x115AAC+4,c['relation'],'B')]
    for u in (UNIT,TARGET):
        result.extend((u+o,v,f) for o,v,f in [(0x290,2 if u==UNIT or c['player_active'] else 5,'B'),(0x291,0,'B'),(0x292,0,'B'),(0x293,0,'B'),
            (0x4EE,-1,'h'),(0x4F2,-1,'h'),(0x4FA,-1,'h'),(0x4FC,-1,'h'),(0x2BC,c['scope'],'b'),(0x2BD,9,'b'),(0x2BE,0,'b'),(0x2B8,1,'i')])
    # Symmetric physical inputs keep both sides alive for repeated exchanges.
    # These are fresh fixture declarations, before the first original root.
    for r in (RECORD,RECORD+0x100):
        result.extend((r+o,v,f) for o,v,f in [(0x14,1000,'h'),(0x16,1000,'h'),(0x2E,999,'H'),(0x32,3,'h'),(0x34,5,'h'),
            (0x37,5,'B'),(0x38,100,'H'),(0x3A,50,'H'),(0x3C,0,'H'),(0x4C,0,'B'),(0x4D,10,'B'),(0x52,1000,'H')])
    return result
