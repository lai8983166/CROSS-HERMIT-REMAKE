"""Independent full-memory and live ownership comparison for character prefix."""
from tools.school_character_prefix_catalog import *

def compare_case(case):
 compare_confirmation(case);p=case['character_prefix'];parent=case['confirmation']
 if p['before']!=parent['after']:raise ValueError('character natural confirmation parent')
 e=expected_prefix(p['before'])
 if p['after']!=e['after'] or p['pending_font']!=e['pending_font']:raise ValueError('character complete source state/stack')
 if p['actual_readbacks']!=parent['actual_readbacks'] or not p['resources_retained'] or not p['retained_ranges_unchanged']:raise ValueError('character full texture/memory retention')
 if not p['handler_prefix_executed'] or any(p[k] is not False for k in ('name_font_executed','image_load_executed','animation_executed','GPU_draw_or_present_executed','world_update_loop_executed')):raise ValueError('character exact execution boundary')
 if not {0x4C61C0,0x4CC600,0x4CC0F0,0x4CA770}.issubset(p['visited']):raise ValueError('character original required calls')
 return {'name':case['name'],'layer':5,'PC':252,'complete_regions':len(REGIONS),'pending_font_return':hex(p['pending_font']['return_va']),
  'texture_bytes':[len(bytes.fromhex(r['hex'])) for r in p['actual_readbacks']],'retained_bytes':p['retained_bytes'],'name_font_executed':False,'image_load_executed':False}

if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('report');a=parser.parse_args();path=ROOT/a.report
 raw=path.read_bytes();d=json.loads(raw)
 print(report_text({'source':source_catalog(),'native_report_sha256':hashlib.sha256(raw).hexdigest(),'cases':[compare_case(c) for c in d['cases']]}))
