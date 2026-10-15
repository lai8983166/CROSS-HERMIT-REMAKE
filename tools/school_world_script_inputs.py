"""Pinned source inputs read from the verified pending184 checkpoint."""
import gzip,hashlib,json
from functools import lru_cache
from tools.school_world_script import ROOT,SOURCE_SHA256,SCRIPT_SHA,SCRIPT,TACT,SCRIPT_REGIONS
from tools.school_world_resume_verification import phase_checked,load_verified_checkpoint,read_memory,REPORTS,SHAS
from tools.school_world_life_codec import unpack

INPUTS=ROOT/'analysis/school-world-script-inputs-v1-20261016.json.gz'
INPUTS_SHA='4f3b733e917a740a7f85e133a06c05110ce866c44284cb5c56ca2ac6fa2182ae'

@lru_cache(maxsize=1)
def source_inputs():
    raw=INPUTS.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=INPUTS_SHA:raise ValueError('world script pinned source inputs')
    d=unpack(json.loads(gzip.decompress(raw)))
    if d['source_sha256']!=SOURCE_SHA256 or d['parent_report']!=REPORTS['entry'].relative_to(ROOT).as_posix() or d['parent_sha256']!=SHAS['entry'] or d['runtime_fixture'] is not False:raise ValueError('world script input provenance')
    return d

@lru_cache(maxsize=3)
def checked_parent(name):
    seed=next((c for c in source_inputs()['cases'] if c['name']==name),None)
    if seed is None:raise ValueError('world script known source case')
    c,state=phase_checked(name,'entry');payload,cp=load_verified_checkpoint(name,'entry')
    before=[dict(pointer=a,bytes=n,hex=read_memory(payload,a,n).hex()) for a,n in SCRIPT_REGIONS]
    if seed['parent_checkpoint']!=cp or cp!=c['continuation_checkpoint'] or seed['before']!=before:raise ValueError('world script full private seed provenance')
    x=seed['inputs']
    for key,at in (('script_pointer',TACT+0x64),('strcmp_import',0x592278),('tick_import',0x592210),('main_owner',0x7A4A00)):
        if x[key]!=int.from_bytes(read_memory(payload,at,4),'little'):raise ValueError('world script private source input '+key)
    if x['script_sha256']!=SCRIPT_SHA or read_memory(payload,x['script_pointer'],SCRIPT.stat().st_size)!=SCRIPT.read_bytes():raise ValueError('world script full private source script')
    return c,state,seed
