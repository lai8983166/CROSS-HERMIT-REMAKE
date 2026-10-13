"""Independent source current-school combat fields and basic attack snapshots."""
import argparse
import hashlib
import json
import struct
from tools.tactics_exit_emulation import SOURCE, SOURCE_SHA256, BASE, ROOT, report_text
from tools.school_formation_placement_catalog import source_catalog as formation_source

JOBS = {3:10,4:6,9:7}
FIELDS = {'attack_rate':(44,1),'movement_rate':(46,2),'movement_type':(48,1),
    'cast_ticks':(52,2),'attack_range':(55,1),'accuracy':(56,2),'power':(58,2),'power_range':(60,2),
    'evasion':(76,1),'armor':(77,1),'body':(78,1),'magic_body':(79,1),'magic_resist':(80,1),'mental':(82,2)}
FUNCTIONS = [(0x4B93C0,0x4BAA90),(0x4DE930,0x4DEA30),(0x48A260,0x48A380),
    (0x48A380,0x48A730),(0x48A730,0x48ABA0),(0x43B9E0,0x43BB90),
    (0x4824D0,0x4826F0),(0x4826F0,0x482810),(0x46C9F0,0x46CA60),(0x488AF0,0x488BC0)]


def source_rules():
    raw = SOURCE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA256: raise ValueError('attack source identity')
    jobs = {}
    for identity,job in JOBS.items():
        template = raw[0x6F5088-BASE+identity*1184:0x6F5088-BASE+(identity+1)*1184]
        j = raw[0x6B2D88-BASE+job*64:0x6B2D88-BASE+(job+1)*64]
        archetype = struct.unpack_from('<H',j,24)[0]
        w = raw[0x6C2DC8-BASE+archetype*72:0x6C2DC8-BASE+(archetype+1)*72]
        jobs[str(job)] = {'job':job,'job_hex':j.hex(),'archetype':archetype,'attack_hex':w.hex(),
            'family':j[2]-1,'weapon_type':template[0x72],'template_sha256':hashlib.sha256(template).hexdigest()}
    addresses = {'half':0x5A0CC0,'tenth':0x5A0CB8,'fifth':0x5A0CB0,
        'eight_hundredths':0x5A0CA8,'quarter':0x5A0C98,'fifteen_hundredths':0x5A0C90,'twentieth':0x5A0C88}
    coefficients = {k:struct.unpack_from('<d',raw,v-BASE)[0] for k,v in addresses.items()}
    terrain = bytes.fromhex(formation_source()['terrain_hex'])
    # 43B9E0 mode4 uses mode0 terrain modifiers; +10/+14/+18, not +0/+4/+8.
    modifiers = [[list(struct.unpack_from('<3i',terrain,t*76+16+(0 if mode==4 else mode)*16))
        for mode in range(5)] for t in range(len(terrain)//76)]
    return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'supported_roles':{str(k):v for k,v in JOBS.items()},
        'jobs':jobs,'coefficients':coefficients,'coefficient_addresses':{k:hex(v) for k,v in addresses.items()},
        'basic_snapshot_threshold':101,'basic_snapshot_skips_skill_scaling':True,
        'terrain_modifiers':modifiers,'field_layout':{k:list(v) for k,v in FIELDS.items()},
        'function_sha256':{hex(a):hashlib.sha256(raw[a-BASE:b-BASE]).hexdigest() for a,b in FUNCTIONS},
        'scope':'Supported no-item current roles/jobs only. Basic unconditioned snapshot and original scalar damage; not full attack/AI/event/HP application chain.'}


def project(input, rules=None):
    r = source_rules() if rules is None else rules
    identity, job = input.get('character_id'), input.get('job')
    if type(identity) is not int or identity not in JOBS or JOBS[identity] != job \
        or input.get('equipped_items') != [0]*8 or not isinstance(input.get('attributes'),list) \
        or len(input['attributes']) != 7 or any(type(a) is not int or not 0<=a<=255 for a in input['attributes']):
        raise ValueError('unsupported attack role input')
    s = r['jobs'][str(job)]; j = bytes.fromhex(s['job_hex']); w = bytes.fromhex(s['attack_hex']); c = r['coefficients']
    a,b,sense,vital,intellect,body,spirit = [min(135,max(1,v)) for v in input['attributes']]
    def word(raw,off): return struct.unpack_from('<H',raw,off)[0]
    def signed(raw,off): return struct.unpack_from('<h',raw,off)[0]
    def clamp(value,high): return min(high,max(0,int(value)))
    if s['family'] == 2:
        if s['weapon_type'] != 2: raise ValueError('unsupported ranged weapon input')
        stat = sense
        attack_range = clamp(w[18]+sense*c['eight_hundredths'],127)
        accuracy = clamp(w[20]+sense*c['fifth'],999)
    elif s['family'] in (3,4):
        stat = vital if s['family'] == 3 else intellect
        attack_range = clamp(w[18]+stat*c['tenth'],127)
        accuracy = 999
    else: raise ValueError('unsupported current attack family')
    power_range = clamp(int(signed(w,36)*stat/100),999)
    power = clamp(int(signed(w,32)*stat/100)+(power_range>>1),999)
    return {'character_id':identity,'job':job,'attack_id':s['archetype'],
        'attack_class':w[5],'target_filter':w[25],
        'attack_rate':clamp(j[18]+sense*c['tenth'],32),
        'movement_rate':clamp(signed(j,20)+int((word(j,20)>>1)*b/100),999),
        'movement_type':0,'cast_ticks':word(w,14),'attack_range':attack_range,
        'accuracy':accuracy,'power':power,'power_range':power_range,
        'evasion':clamp(j[26]*b//100+b*c['quarter'],255),
        'armor':clamp(j[27]*a//100+a*c['fifteen_hundredths'],255),
        'body':clamp(j[28]+body*c['tenth']+sense*c['twentieth'],99),
        'magic_body':clamp(j[29]+intellect*c['fifteen_hundredths'],255),
        'magic_resist':clamp(j[30]+spirit*c['twentieth']+vital*c['tenth'],99),
        'mental':clamp(min(999,max(1,int((body*3+a+b)*word(j,6)/100)))*c['tenth'],999)}


def from_record(raw):
    if len(raw) != 176: raise ValueError('combat record size')
    return {k:int.from_bytes(raw[off:off+n],'little') for k,(off,n) in FIELDS.items()}


def snapshot(fields, terrain, mode=0, rules=None):
    r = source_rules() if rules is None else rules
    if type(terrain) is not int or not 0<=terrain<len(r['terrain_modifiers']) or mode not in range(5):
        raise ValueError('attack terrain/movement mode')
    if r['basic_snapshot_threshold'] != 101 or not r['basic_snapshot_skips_skill_scaling']:
        raise ValueError('basic snapshot classification source')
    coefficients = r['terrain_modifiers'][terrain][mode]
    # Original46C9F0 identifies basic attacks;488AF0 skips all skill scaling.
    return {'power':fields['power'],'power_range':fields['power_range'],'accuracy':fields['accuracy'],
        'evasion':fields['evasion'],'armor':fields['armor'],'magic_resist':fields['magic_resist'],
        'magic_body':fields['magic_body'],'body':fields['body'],
        'evasion_coefficient':coefficients[0],'armor_coefficient':coefficients[1],
        'body_coefficient':coefficients[2],'magic_modifier':0}


def snapshot_bytes(fields, terrain, mode=0, rules=None):
    value = snapshot(fields,terrain,mode,rules)
    raw = bytearray(44)
    struct.pack_into('<3H',raw,0,value['power'],value['power_range'],value['accuracy'])
    raw[8:13] = bytes(value[k] for k in ('evasion','armor','magic_resist','magic_body','body'))
    struct.pack_into('<3i',raw,16,value['evasion_coefficient'],value['armor_coefficient'],value['body_coefficient'])
    struct.pack_into('<H',raw,36,fields['mental'])
    return bytes(raw)


def scalar_damage(attack, defense, rolls, magic=False):
    rolls = iter(rolls)
    if magic:
        power = attack['power']+(next(rolls)%attack['power_range'] if attack['power_range'] else 0)
        return max(int(power*(100-defense['magic_resist']+defense['magic_modifier'])/100)
            -int(defense['magic_body']*defense['body_coefficient']/100),1)
    roll = next(rolls)%100
    residual = attack['accuracy']-int(defense['evasion']*defense['evasion_coefficient']/100)-roll
    if defense['evasion'] == 0 or roll <= 4 or residual >= 150:
        if defense['evasion'] and roll > 94: return -1
        multiplier = max(residual,150)
    elif roll > 94 or residual < 0: return -1
    else: multiplier = 100
    power = attack['power']+(next(rolls)%attack['power_range'] if attack['power_range'] else 0)
    damage = int(power*multiplier/100)-int(defense['armor']*defense['armor_coefficient']/100)
    return max(damage,0) if multiplier == 100 else (1 if damage < 0 else damage)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument('--out',required=True)
    args=parser.parse_args(); (ROOT/args.out).write_text(report_text(source_rules()),encoding='utf-8',newline='\n')
