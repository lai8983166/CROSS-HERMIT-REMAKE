"""Independent original physical hit/damage and declared combat inputs."""
from functools import lru_cache
from tools.battle_pathfinding_emulation import ROOT,SOURCE,need,sha
from tools.dxanim_lib import parse_dxanim,parse_program_blocks
from tools.battle_attack_animation import case as animation_case


@lru_cache(maxsize=1)
def effect_resource():
    p=ROOT/'CROSS HERMIT/CROSS HERMIT/DATA/DXANIM/EFCT.BIN';raw=p.read_bytes();digest='9c0a8896610e8168f324bc0ca91bc7e860024a8e54cf713db8ad33c2f8906106'
    need(sha(raw)==digest,'original EFCT identity');offsets=parse_dxanim(raw)
    return dict(raw=raw[:offsets[6]],offsets=offsets,programs=parse_program_blocks(raw),identity=dict(path=p.relative_to(ROOT).as_posix(),bytes=len(raw),sha256=digest,metadata_bytes=offsets[6]))


def case(name,**kw):
    c=dict(name=name,job=1,power=50,spread=0,accuracy=100,evasion=10,armor=10,mental=100,hp=100,max_hp=100,threshold=0,
           seed=20<<16,crt_seed=1,target_attacking=False)
    c.update(kw);return c


def animation_input(c):return animation_case(c['name'],job=c['job'],consume='early_boundary')


def corpus():
    return [case('ordinary'),case('ordinary_job2',job=2),case('ordinary_job3',job=3),case('ordinary_job4',job=4),
            case('miss_roll95',seed=95<<16),case('miss_residual',accuracy=0),case('forced_critical_roll4',seed=4<<16),case('roll5_normal',seed=5<<16),
            case('accuracy_critical',accuracy=300),case('block_armor',power=1,armor=100),case('zero_evasion_normal',evasion=0),
            case('zero_evasion_critical',evasion=0,accuracy=300),case('power_spread',spread=30),case('stagger',mental=20),case('heavy_stagger',mental=1),
            case('attacking_target',mental=1,target_attacking=True),case('lethal',hp=10),case('threshold_survival',hp=10,threshold=10),
            case('threshold_below_hp',hp=20,threshold=10),case('threshold_unmet',hp=9,threshold=10),case('short_damage_wrap',power=65535,accuracy=500),
            case('short_delta_overflow',power=32768,armor=0,evasion=0,accuracy=100),case('critical_negative_minimum',power=0,armor=100,seed=0),
            case('critical_exact_zero',power=0,armor=0,seed=0),case('short_wrap_heals',power=65535,accuracy=500,max_hp=30000),
            case('exact_hp_zero',hp=39),case('mental_equal',mental=39),case('mental_triple_equal',mental=13),
            case('roll94_hit',seed=94<<16,accuracy=200),case('roll95_high_accuracy_miss',seed=95<<16,accuracy=500),
            case('zero_evasion_roll95_hit',seed=95<<16,evasion=0),case('forced_roll4_low_accuracy',seed=4<<16,accuracy=0),
            case('threshold_unsigned_high',hp=10,threshold=65535),case('hp_above_capacity',max_hp=50)]


def validate(c):
    need(set(c)==set(case('x')),'exact combat fields')
    need(type(c['name']) is str and c['name'] and type(c['target_attacking']) is bool,'combat name/flag')
    for k,lo,hi in [('job',1,4),('power',0,65535),('spread',0,65535),('accuracy',0,65535),('evasion',0,255),('armor',0,255),('mental',0,65535),
                    ('hp',0,32767),('max_hp',1,32767),('threshold',0,65535),('seed',0,0xFFFFFFFF),('crt_seed',0,0xFFFFFFFF)]:
        need(type(c[k]) is int and lo<=c[k]<=hi,'combat '+k)


def signed(v,bits=32):return (v+(1<<(bits-1)))%(1<<bits)-(1<<(bits-1))
def div(a,b):return abs(a)//b*(-1 if a<0 else 1)


class Random:
    def __init__(self,seed):self.seed=seed;self.count=0;self.values=[]
    def next(self):
        v=(self.seed>>16)&32767;self.seed=(self.seed*0x48D159E1+1)&0xFFFFFFFF;self.count+=1;self.values.append(v);return v


def physical(c,evasion_coefficient,armor_coefficient,rng):
    roll=rng.next()%100;residual=c['accuracy']-div(c['evasion']*evasion_coefficient,100)-roll;mult=100
    if c['evasion']==0:
        if residual>=150:mult=residual
    elif roll<5 or residual>=150:
        if roll>=95:return dict(kind=0,damage=0,roll=roll,multiplier=None)
        mult=max(150,residual)
    elif roll>=95 or residual<0:return dict(kind=0,damage=0,roll=roll,multiplier=None)
    power=c['power']+(rng.next()%c['spread'] if c['spread'] else 0)
    damage=signed(div(signed(power*mult),100)-div(c['armor']*armor_coefficient,100))
    if mult==100:
        kind=4 if damage<1 else (3 if damage>c['mental']*3 else (2 if damage>c['mental'] else 1));damage=max(damage,0)
    else:kind=3;damage=1 if damage<0 else damage
    return dict(kind=kind,damage=damage,roll=roll,multiplier=mult)
