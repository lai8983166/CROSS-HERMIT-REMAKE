"""Independent full-byte comparison of native animation and natural third-text prefix."""
from tools.school_character_animation_catalog import *
from tools.school_character_image_verification import compare_live

EVIDENCE=ROOT/'analysis/school-character-animation-live-v4-20261013.json'
EVIDENCE_SHA256='9b09e8ae8c68d51a81ccf6eeeab65505170f5f5c7b779cff58bf61fac1711b1e'

def compare_animation(case):
 compare_live(case);p=case['character_animation'];image=case['image_live']
 if p['before']!=image['after'] or p['renderer']!=case['image_prefix']['renderer'] or len(p['steps'])!=78:raise ValueError('animation natural image parent/driver')
 before=p['before'];calls=0
 for i,step in enumerate(p['steps']):
  expected=advance(before,i,p['renderer'])
  if step!=expected:raise ValueError('animation every byte/call/predicate/return '+str(i))
  calls+=len(step['presentation'])+len(step['text_draws']);before=step['after']
 if p['after']!=before:raise ValueError('animation final released state')
 pixels=case['name_texture']['prior_actual_readbacks']+[case['name_texture']['actual_readback'],image['actual_readback']]
 if p['actual_readbacks']!=pixels:raise ValueError('animation all four actual pixels')
 if not {0x4CC0D2,0x4CC420,0x4CA1B0,0x4C99E0,0x4CD060,0x4CD120,0x4CA860,0x4077C0}.issubset(p['visited']):raise ValueError('animation required original bodies')
 if any(p[k] is not True for k in ('original_handler_returned','original_animation_executed','original_readiness_executed','retained_ranges_unchanged')) or any(p[k] is not False for k in ('synthetic_readiness','GPU_draw_or_present_executed','world_update_loop_executed')):raise ValueError('animation exact authority/retention')
 return {'name':case['name'],'updates':78,'readiness_calls':154,'terminal_calls':calls,'complete_regions_per_update':len(REGIONS),'four_texture_bytes':[len(bytes.fromhex(r['hex'])) for r in pixels],'released_PC':272}

def compare_third(case):
 result=compare_animation(case);p=case['third_text_prefix']
 if p['before']!=case['character_animation']['after']:raise ValueError('third natural animation parent')
 expected=third_prefix(p['before'],p['script_pointer'])
 if any(p[k]!=v for k,v in expected.items()):raise ValueError('third full source regions/text/calls/split/font stack')
 if p['actual_readbacks']!=case['character_animation']['actual_readbacks']:raise ValueError('third all actual resource pixels')
 if any(p[k] is not True for k in ('original_text_activation_executed','original_lookup_split_executed','retained_ranges_unchanged')) or any(p[k] is not False for k in ('font_API_executed','third_texture_created','GPU_draw_or_present_executed','world_update_loop_executed')):raise ValueError('third exact authority/retention')
 return {**result,'third_text_index':2,'third_layer':5,'pending_PC':280,'third_font_executed':False}

@lru_cache(maxsize=1)
def fixture():
 raw=EVIDENCE.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=EVIDENCE_SHA256:raise ValueError('pinned actual animation evidence')
 return json.loads(raw)

if __name__=='__main__':
 import sys
 sys.stdout.reconfigure(encoding='utf-8');print(report_text({'source_image_sha256':SOURCE_SHA256,'native_report_sha256':EVIDENCE_SHA256,'cases':[compare_third(c) for c in fixture()['cases']]}),end='')
