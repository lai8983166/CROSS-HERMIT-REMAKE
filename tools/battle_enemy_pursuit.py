"""Declared out-of-range targets for original world-driven enemy pursuit."""
from copy import deepcopy
from tools.battle_enemy_engagement import corpus as parent_corpus,validate as parent_validate
from tools.battle_world_combat import pages,expand,validate_pages
from tools.battle_pathfinding_emulation import need,sha


def base_input(c):return {k:v for k,v in c.items() if k!='target_cell'}


def corpus():
    rows=[]
    for j,c in enumerate(parent_corpus()[:4],1):
        c=deepcopy(c);c.update(name='south_job'+str(j),target_cell=[29,13]);rows.append(c)
    c=deepcopy(rows[0]);c.update(name='diagonal_job1',target_cell=[33,12]);rows.append(c)
    c=deepcopy(rows[0]);c.update(name='search_disabled_far',scope=2,rounds=0,budget=96);rows.append(c)
    return rows


def validate(c):
    need(set(c)=={'name','aftermath','scope','relation','budget','rounds','target_cell'},'exact pursuit input')
    parent_validate(base_input(c));need(c['target_cell'] in ([29,13],[33,12]),'declared actual-map far target')


def target_fields(c):
    x,y=c['target_cell'];return [(0x2EC,(x*32+16)*65536,'i'),(0x2F0,(y*16+8)*65536,'i')]+[(o,v,'B') for o,v in ((0x4E7,x),(0x4E8,y),(0x4E9,x),(0x4EA,y))]
