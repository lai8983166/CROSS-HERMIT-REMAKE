"""Declared finite complete world-update cases after basic melee HP."""
from copy import deepcopy
from tools.battle_combat_aftermath import corpus as aftermath_corpus,validate as aftermath_validate
from tools.battle_pathfinding_emulation import need


def corpus():
    inputs={c['name']:c for c in aftermath_corpus()};rows=[]
    for name in ('ordinary','ordinary_job2','ordinary_job3','ordinary_job4','stagger','heavy_stagger','lethal','threshold_survival','miss_roll95','block_armor'):
        rows.append(dict(name=name,aftermath=deepcopy(inputs[name]),frames=3,world_enabled=True))
    rows.append(dict(name='world_gate_off',aftermath=deepcopy(inputs['lethal']),frames=2,world_enabled=False))
    return rows


def validate(c):
    need(set(c)=={'name','aftermath','frames','world_enabled'},'exact finite world input')
    aftermath_validate(c['aftermath']);need(type(c['frames']) is int and 1<=c['frames']<=4,'finite world frame budget')
    need(isinstance(c['name'],str) and c['name'] and type(c['world_enabled']) is bool,'world name and total gate')
