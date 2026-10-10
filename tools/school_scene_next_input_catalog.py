"""Independent second scene input, progress and signed cache query provenance."""
import argparse,hashlib,json,struct
from copy import deepcopy
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from tools.school_scene_next_input_emulation import ROOT,SOURCE,SOURCE_SHA256,BASE,UNITCTRL,AUTHORITY,report_text
from tools.school_scene_unit_work_catalog import source_catalog as prefix_catalog,expected_prefix
from tools.school_enemy_records_catalog import source_catalog as record_catalog,expected_record
from tools.school_current_units_catalog import source_catalog as current_catalog,expected_progress

EVIDENCE=ROOT/'analysis/school-scene-next-input-v1-20261010.json'
EVIDENCE_SHA256='b78b913b3d8ffe895a86675f8c77c9b630caafb731d58c40a66adb7262b58276'
CACHE_EVIDENCE=ROOT/'analysis/school-scene-cache-query-v1-20261010.json'
CACHE_SHA256='5de16b7c89e433595a6c103fc26fef82e8bcbb997804b3cfdfbc17740a665995'


def source_catalog():
    raw=SOURCE.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA256:raise ValueError('scene next source identity')
    md=Cs(CS_ARCH_X86,CS_MODE_32);md.detail=True;code=[]
    def ins(va,mnemonic):
        i=next(md.disasm(raw[va-BASE:va-BASE+16],va,count=1))
        if i.mnemonic!=mnemonic:raise ValueError('scene cache instruction identity')
        code.append({'va':hex(va),'mnemonic':i.mnemonic,'operands':i.op_str,'instruction_hex':i.bytes.hex()})
        return i
    count=ins(0x466DCF,'cmp').operands[1].imm
    entry=ins(0x466DDE,'lea').operands[1].mem
    used=ins(0x466DEB,'movsx').operands[1]
    group=ins(0x466DF5,'movsx').operands[1]
    palette=ins(0x466E01,'movsx').operands[1]
    if (count,entry.scale,used.size,group.size,palette.size)!=(512,8,1,2,1):raise ValueError('scene cache field shape')
    for va,name in ((0x466DEE,'test'),(0x466DF9,'cmp'),(0x466E05,'cmp'),(0x466E19,'ret')):ins(va,name)
    prefix,records,current=prefix_catalog(),record_catalog(),current_catalog();keys=[]
    for ordinal,template in enumerate(records['templates']):
        record=bytes.fromhex(expected_record(template,rules=records)['record_hex'])
        role,job=struct.unpack_from('<H',record,2)[0],struct.unpack_from('<H',record,12)[0]
        j=prefix['jobs'][str(job)]
        variant=0 if j['mode']==0 else j['fixed_variant'] if j['mode']==1 else (
            j['palettes_by_character'][role]+1 if j['palettes_by_character'][role] else 0)
        keys.append({'ordinal':ordinal,'role':role,'job':job,'group':j['group'],'palette':variant})
    return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'prefix':prefix,'records':records,
        'progress':current['progress'],'cache':{'count':count,'stride':entry.scale,'offset':entry.disp,
            'used_offset':used.mem.disp,'group_offset':group.mem.disp,'palette_offset':palette.mem.disp,
            'signed_group':True,'signed_palette':True,'nonzero_used':True,'first_match':True},
        'scene_keys':keys,'code_inputs':code,'source_branch_bodies':[{'start':hex(a),'end':hex(b),
            'instruction_hex':raw[a-BASE:b-BASE].hex(),'sha256':hashlib.sha256(raw[a-BASE:b-BASE]).hexdigest()}
            for a,b in ((0x466DA0,0x466E1C),(0x453630,0x453638),(0x451D80,0x451E19))],
        'declared_insertion_inputs':{'used':1,'opaque_token_base':0x1A000000,'opaque_token_stride':96},
        'scope':'Actual second scene input stops before mode0 loading. Separate35 ordered read-only queries use declared insertions; no allocation/binding/remaining constructors/placement/VM.',**AUTHORITY}


def expected_lookup(cache_hex,group,palette,receiver=UNITCTRL,rules=None):
    r=source_catalog() if rules is None else rules;c=r['cache']
    try:cache=bytes.fromhex(cache_hex)
    except (TypeError,ValueError) as error:raise ValueError('cache byte encoding') from error
    if len(cache)!=c['count']*c['stride']:raise ValueError('cache byte ownership')
    if any(type(v) is not int or not -2**31<=v<2**31 for v in (group,palette)):
        raise ValueError('cache signed32 query argument')
    if type(receiver) is not int or receiver<=0 or receiver%4 or receiver+c['offset']+len(cache)>2**32:
        raise ValueError('cache receiver bounds/alignment')
    slot=None
    for i in range(c['count']):
        at=i*c['stride']
        if cache[at+c['used_offset']]==0:continue
        g=struct.unpack_from('<h',cache,at+c['group_offset'])[0]
        p=struct.unpack_from('<b',cache,at+c['palette_offset'])[0]
        if (g,p)==(group,palette):slot=i;break
    return {'slot':slot,'return_pointer':0 if slot is None else receiver+c['offset']+slot*c['stride'],
        'cache_after_hex':cache.hex(),'cache_unchanged':True}


def expected_sequence(seed_cache_hex,rules=None):
    r=source_catalog() if rules is None else rules
    try:cache=bytearray.fromhex(seed_cache_hex)
    except (TypeError,ValueError) as error:raise ValueError('cache seed encoding') from error
    outputs=[]
    inputs=r['declared_insertion_inputs']
    for k in r['scene_keys']:
        q=expected_lookup(cache.hex(),k['group'],k['palette'],rules=r)
        insertion=None
        if q['slot'] is None:
            slots=[i for i in range(r['cache']['count']) if cache[i*8]==0]
            if not slots:raise ValueError('declared cache insertion has no free row')
            slot=slots[0];entry=struct.pack('<BBHI',inputs['used'],k['palette'],k['group'],
                inputs['opaque_token_base']+k['ordinal']*inputs['opaque_token_stride'])
            cache[slot*8:slot*8+8]=entry
            insertion={'slot':slot,'entry_hex':entry.hex(),'opaque_controller_token_not_allocation':True}
        outputs.append({**k,**q,'declared_insertion':insertion,'driver_cache_after_hex':cache.hex()})
    return {'queries':outputs,'final_declared_cache_hex':cache.hex(),
        'hits':sum(q['slot'] is not None for q in outputs),'misses':sum(q['slot'] is None for q in outputs)}


def expected_second(p,record_before_prefix,rules=None):
    r=source_catalog() if rules is None else rules
    expected=expected_record(r['records']['templates'][1],rules=r['records'])
    if expected['record_hex']!=record_before_prefix:raise ValueError('second record source mismatch')
    prefix=expected_prefix(record_before_prefix,1,p['cache_before_hex'],p['counter_before'],p['renderer'],
        p['allocation']['pointer'],p['classification_selector'],p['relation_hex'],r['prefix'])
    return {'record':expected,'prefix':prefix}


def native_fixture():
    raw=EVIDENCE.read_bytes();cache=CACHE_EVIDENCE.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=EVIDENCE_SHA256 or hashlib.sha256(cache).hexdigest()!=CACHE_SHA256:
        raise ValueError('frozen next scene evidence identity')
    fields=('name','ready','second_scene_input_prepared','second_scene_record','second_scene_work','scene_progress',
        'stop_reason','persistent_ranges_unchanged','battle_world_constructed')
    return {'schema_version':1,'source_report_sha256':EVIDENCE_SHA256,'cache_report_sha256':CACHE_SHA256,
        'cases':[{k:deepcopy(c[k]) for k in fields if k in c} for c in json.loads(raw)['cases']],
        'declared_cache_diagnostic':json.loads(cache),**AUTHORITY}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--rules-out',required=True);p.add_argument('--fixture-out',required=True);a=p.parse_args()
    for path,data in ((a.rules_out,source_catalog()),(a.fixture_out,native_fixture())):
        (ROOT/path).write_text(report_text(data),encoding='utf-8',newline='\n')
