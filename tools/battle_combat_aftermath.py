"""Finite basic melee follow-up inputs, all declared before the first root."""
from copy import deepcopy
from tools.battle_hit_damage import corpus as hit_corpus,validate as hit_validate
from tools.battle_pathfinding_emulation import need


def corpus():
    names=('ordinary','ordinary_job2','ordinary_job3','ordinary_job4','stagger','heavy_stagger','forced_critical_roll4',
           'miss_roll95','block_armor','lethal','exact_hp_zero','threshold_survival','threshold_unmet','accuracy_critical','short_wrap_heals')
    hits={r['name']:r for r in hit_corpus()};rows=[]
    for name in names:
        rows.append(dict(name=name,combat=deepcopy(hits[name]),actor_kills=0,actor_points=0,target_deaths=0,score=0,region_count=0,kill_points=20))
    for name,field,value in [('kill_short_saturated','actor_kills',32767),('points_short_saturated','actor_points',32760),
                             ('death_byte_saturated','target_deaths',127),('score_short_saturated','score',32760),('region_short_wrap','region_count',32767),
                             ('kill_short_last_increment','actor_kills',32766),('points_short_last_increment','actor_points',32747),
                             ('death_byte_last_increment','target_deaths',126)]:
        c=deepcopy(rows[9]);c['name']=name;c[field]=value;rows.append(c)
    return rows


def validate(c):
    need(set(c)=={'name','combat','actor_kills','actor_points','target_deaths','score','region_count','kill_points'},'exact aftermath input')
    hit_validate(c['combat']);need(isinstance(c['name'],str) and c['name'],'aftermath name')
    for key in ('actor_kills','actor_points','score','region_count'):need(type(c[key]) is int and 0<=c[key]<=32767,'declared '+key)
    need(type(c['target_deaths']) is int and 0<=c['target_deaths']<=127,'declared target death counter')
    need(type(c['kill_points']) is int and 0<=c['kill_points']<=32767,'declared kill point value')
