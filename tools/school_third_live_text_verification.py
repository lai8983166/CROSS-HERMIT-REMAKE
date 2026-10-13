"""Independent fifth-texture, original GDI/COM and third readiness comparison."""
from copy import deepcopy
from tools.school_third_live_text_catalog import *
from tools.school_character_animation_verification import compare_third

EVIDENCE=ROOT/'analysis/school-third-live-text-v4-20261013.json'
EVIDENCE_SHA256='e14e359274b020d363fefed4f5e0701172312ce967032bfad78ca7574dd8c82b'

def parent_view(case):
 first=case['first_live_text'];cleanup=first['COM_process_cleanup'];third=case['third_live_text'];old=(case['image_live']['texture'],case['name_texture']['texture'],case['second_live_text']['texture'],first['texture'])
 if cleanup['texture_releases']!=[{'pointer':t['pointer'],'unlock_hr':0,'count':0} for t in (third['texture'],*old)] or not cleanup['all_owned_resources_released'] or not first['process_exited']:raise ValueError('third all five actual COM cleanup')
 if first['remaining_GDI_cleanup']!={'fonts':0,'bitmaps':0,'dcs':4,'all_resources_released':True}:raise ValueError('third complete actual GDI cleanup')
 # Comparison-only projection; the native report retains the actual fifth owner.
 view=dict(case);f=dict(first);c=dict(cleanup);c['texture_releases']=cleanup['texture_releases'][1:];f['COM_process_cleanup']=c;f['remaining_GDI_cleanup']={'fonts':0,'bitmaps':0,'dcs':3,'all_resources_released':True};view['first_live_text']=f
 compare_third(view)

def compare_gdi(p,prefix):
 api=p['font_api'];font_frame=prefix['pending_font']['frames']['font'];f=font_frame-0x1DC;text=font_frame-0x110;n=len(bytes.fromhex(prefix['third_text']['hex']));cfg=geometry(p['measured']);pad=cfg['padding'];w,h=cfg['raster_size']
 if len(api)!=23:raise ValueError('third exact GDI sequence length')
 font=api[0]['result'];measure=api[2]['args'][0];old_font=api[2]['result'];dc=api[6]['result'];bitmap=api[7]['result'];brush=api[10]['result']
 if any(type(v)is not int or not 0<v<0xFFFFFFFF for v in (font,measure,old_font,dc,bitmap,brush)):raise ValueError('third actual GDI handles')
 expected=[('CreateFontA','0x4cad09',prefix['pending_font']['args']),('lstrlenA','0x4051ba',[text]),('SelectObject','0x4051ea',[measure,font]),
  ('lstrlenA','0x405230',[text]),('GetTextExtentPoint32A','0x405246',[measure,text,n,f-0x54]),('SelectObject','0x40528a',[measure,old_font]),
  ('CreateCompatibleDC','0x405373',[0]),('CreateDIBSection','0x4053cc',[dc,f-0x38,0,f-0x3C,0,0]),('SelectObject','0x40541b',[dc,bitmap]),
  ('SetMapMode','0x40545d',[dc,1]),('GetStockObject','0x405471',[4]),('SelectObject','0x405485',[dc,brush]),('PatBlt','0x4054ac',[dc,0,0,w,h,0xF00021]),
  ('SelectObject','0x4054c6',[dc,font]),('SetBkMode','0x405508',[dc,1]),('SetBkColor','0x405520',[dc,0]),('SetTextAlign','0x405535',[dc,0]),
  ('SetTextColor','0x405663',[dc,0x80808]),('lstrlenA','0x405676',[text]),('TextOutA','0x40569c',[dc,2*pad,2*pad,text,n]),
  ('SetTextColor','0x4056b4',[dc,0xFFFFFF]),('lstrlenA','0x4056c7',[text]),('TextOutA','0x4056e7',[dc,pad,pad,text,n])]
 if [(x['name'],x['return_va'],x['args']) for x in api]!=expected:raise ValueError('third every original GDI input/caller')
 slots={'CreateFontA':0x5920A0,'lstrlenA':0x5922C4,'SelectObject':0x5920A4,'GetTextExtentPoint32A':0x5920BC,'CreateCompatibleDC':0x592094,'CreateDIBSection':0x592098,'SetMapMode':0x59209C,'GetStockObject':0x592084,'PatBlt':0x592088,'SetBkMode':0x59208C,'SetBkColor':0x5920B4,'SetTextAlign':0x5920B8,'SetTextColor':0x5920B0,'TextOutA':0x592090}
 if any(r['slot']!=hex(slots[r['name']]) for r in api):raise ValueError('third every original GDI import slot')
 bindings=p['inputs']['import_bindings']
 if len(bindings)!=len(slots):raise ValueError('third exact GDI binding count')
 for index,(name,slot) in enumerate(slots.items()):
  target=0xE300000 if index==0 else 0xE300100+16*index;b=bindings[index]
  if b!={'slot':hex(slot),'before':0xE310000 if name=='SelectObject' else target,'bound':target,'name':name}:raise ValueError('third actual declared GDI binding')
 if api[4]['measured']!=p['measured'] or api[4]['selected_face']!=p['selected_face'] or not p['selected_face']:raise ValueError('third actual measurement provenance')
 for r in api:
  if r['name']=='lstrlenA' and r['result']!=n:raise ValueError('third original byte count')
  if r['name'] in ('GetTextExtentPoint32A','PatBlt','TextOutA') and r['result']!=1:raise ValueError('third actual GDI success')
 if api[7]['header_hex']!=cfg['header_hex'] or api[7]['virtual_bits_pointer']!=RASTER:raise ValueError('third original DIB shape/binding')
 if p['crt']!=[{'name':'bounded_source_copy','target':text,'source':prefix['split']['lines'][0]['pointer'],'hex':prefix['third_text']['hex'],'return_va':'0x4cad23'}]:raise ValueError('third exact original stack copy')

def compare_live(case):
 parent_view(case);p=case['third_live_text'];prefix=case['third_text_prefix'];r=p['raster'];first=case['first_live_text'];device=first['binding']['bound'];tex=p['texture']['pointer'];old=[t['pointer'] for t in (first['texture'],case['second_live_text']['texture'],case['name_texture']['texture'],case['image_live']['texture'])]
 if tex in old or len(set(old+[tex]))!=5 or r['before']!=prefix['after'] or p['before']!=r['after']:raise ValueError('third fresh fifth texture and full natural parent')
 inputs=r['inputs'];renderer=case['image_prefix']['renderer']
 if inputs['device']!=device or inputs['graphics_context']!=renderer or inputs['parent_text_sha256']!=PREFIX_SHA or inputs['platform']!='real_host_GDI_offscreen_measurement_DC' or type(inputs['host_ansi_code_page'])is not int or inputs['host_ansi_code_page']<=0:raise ValueError('third actual platform binding')
 if r['text_hex']!=prefix['third_text']['hex']:raise ValueError('third source string')
 cfg=raster_state(r['before'],r['measured'],renderer);e=complete_state(p['before'],device,tex)
 if r['after']!=cfg['after']:raise ValueError('third every raster region')
 for k in ('after','text_draws','text_updates','objects','natural_return'):
  if p[k]!=e[k]:raise ValueError('third full source completion '+k)
 if p['presentation']!=presentation(prefix):raise ValueError('third source character/old layer presentation')
 compare_gdi(r,prefix);raw=bytes.fromhex(r['raster']['hex'])
 if r['raster']['pointer']!=RASTER or r['raster']['size']!=cfg['raster_size'] or len(raw)!=cfg['raster_size'][0]*cfg['raster_size'][1]*4 or hashlib.sha256(raw).hexdigest()!=r['raster']['sha256']:raise ValueError('third all real raster bytes')
 wanted={'va':'0x403bd0','receiver':TEXTURE,'args':[device,0],'return_va':'0x405779','first_instruction_executed':False,'natural_stack_verified':True}
 if r['pending_texture']!=wanted:raise ValueError('third natural texture request')
 if any(r[k] is not True for k in ('font_api_executed','original_raster_geometry_executed','real_offscreen_GDI_drawing','platform_resources_live')) or any(r[k] is not False for k in ('original_gpu_executed','texture_creation_executed','text_record_completed','text_readiness_executed','natural_VM_returned','world_update_loop_executed')):raise ValueError('third raster exact execution boundary')
 font=prefix['pending_font']['frames']['font'];f=font-0x1DC;w,h=e['texture_size']
 if p['entry']!={'sp':font-0x2E0,'ebp':f,'return_va':0x405779} or p['accounting_before']!=case['image_live']['accounting_after'] or p['accounting_after']!=p['accounting_before']+w*h*2:raise ValueError('third natural texture stack/accounting')
 if p['cleanup_import_bindings']!=[{'slot':0x5920A4,'before':0xE300120,'bound':0xE310000},{'slot':0x5920C4,'before':0xE310010,'bound':0xE310010},{'slot':0x592060,'before':0xE310020,'bound':0xE310020}]:raise ValueError('third exact original cleanup bindings')
 if not {0x403730,0x403BD0,0x405A80,0x4CAD7C,0x4D1BF0,0x4C4D04,0x4CB220}.issubset(p['visited']):raise ValueError('third original required function bodies')
 calls=p['COM_calls']
 if len(calls)!=4:raise ValueError('third exact COM call count')
 argslist=([device,w,h,1,0,25,1,TEXTURE+0x2C],[tex,0,font-0x318],[tex,0,f-0x84,0,0x800],[tex,0])
 for c,at,offset,args in zip(calls,('0x403c87','0x403cbb','0x40395b','0x4039d0'),(80,56,64,68),argslist):
  identity=first['platform_hello']['device'] if offset==80 else p['texture']
  if c['source_va']!=at or c['offset']!=offset or c['args']!=args or c['vtable']!=identity['vtable'] or c['actual_method']!=identity['methods'][str(offset)] or c['result']['hr']!=0:raise ValueError('third every actual original COM input')
 if calls[0]['result']['texture']!=p['texture'] or struct.unpack('<8I',bytes.fromhex(calls[1]['result']['hex']))!=(25,1,0,1,w*h*2,0,w,h):raise ValueError('third actual COM identity/descriptor')
 lock=p['lock'];pitch=lock['pitch'];out=bytes.fromhex(lock['before_hex'])
 if type(pitch)is not int or not w*2<=pitch<=4096 or pitch%2 or len(out)!=pitch*h or lock['mirror']!=MIRROR:raise ValueError('third bounded full actual lock')
 if (calls[2]['result']['pitch'],calls[2]['result']['bits'],calls[2]['result']['hex'])!=(pitch,lock['host_bits'],lock['before_hex']):raise ValueError('third actual lock provenance')
 conversions=[]
 for b in bands(cfg):
  out=convert_surface(raw,cfg['raster_size'],b['rect'],out,pitch,b['point']);conversions.append({'source_va':'0x405869','args':[RASTER,f-0x84,*cfg['raster_size'],f-0x98,f-0xA8],'lock_hex':struct.pack('<2I',pitch,MIRROR).hex(),**b})
 rb=p['actual_readback']
 if p['conversion_calls']!=conversions or rb['hex']!=out.hex() or lock['after_hex']!=out.hex() or rb['sha256']!=hashlib.sha256(out).hexdigest() or rb['pitch']!=pitch or rb['hr']!=0 or rb['unlock_hr']!=0:raise ValueError('third every original band and complete pixels')
 api=r['font_api'];dc=api[6]['result'];bitmap=api[7]['result'];font_handle=api[0]['result'];old_bitmap=api[8]['result']
 if p['GDI_cleanup_calls']!=[{'name':'SelectObject','args':[dc,old_bitmap],'return_va':'0x4058d8','result':bitmap},{'name':'DeleteObject','args':[bitmap],'return_va':'0x405921','result':1},{'name':'DeleteDC','args':[dc],'return_va':'0x40596a','result':1},{'name':'DeleteObject','args':[font_handle],'return_va':'0x4d1c1b','result':1}]:raise ValueError('third original GDI cleanup order')
 remote=[]
 for at in ('0x403c81','0x403cb8','0x403958','0x4039cd'):
  identity=first['platform_hello']['device'] if at=='0x403c81' else p['texture'];remote.append({'source_va':at,'pointer':identity['pointer'],'vtable':identity['vtable']})
 if p['remote_reads']!=remote or r['prior_actual_readbacks']!=prefix['actual_readbacks'] or p['prior_actual_readbacks']!=prefix['actual_readbacks']:raise ValueError('third actual remote reads/four prior pixels')
 if any(x['retained_ranges_unchanged'] is not True for x in (p,r)) or not p['original_third_font_texture_handler_executed'] or any(p[k] is not False for k in ('GPU_draw_or_present_executed','world_update_loop_executed','dialogue_playback_completed')):raise ValueError('third complete authority/retention')
 return {'name':case['name'],'texture_size':[w,h],'fifth_texture_bytes':len(out),'raster_size':cfg['raster_size'],'band_calls':len(conversions),'GDI_calls':23,'COM_calls':4,'handler_return_PC':286}

def compare_wait(case):
 result=compare_live(case);p=case['third_text_wait'];live=case['third_live_text'];prefix=case['third_text_prefix']
 if p['before']!=live['after'] or len(p['steps'])!=26:raise ValueError('third wait natural live parent/update count')
 if p['input_binding']!={'before_mouse_words':[0,1,0],'after_mouse_words':[0,0,0],'write_address':TASK+0x1990,'kind':'explicit isolated reset of prior confirmation pulse; no live input capture','space_key':0,'mouse_position':[0,0]}:raise ValueError('third explicit no-input reset')
 before=p['before']
 for i,s in enumerate(p['steps']):
  if s!=advance_wait(before,i,prefix):raise ValueError('third every native wait byte/predicate/input/update '+str(i))
  before=s['after']
 if p['after']!=before or p['actual_readbacks']!=live['prior_actual_readbacks']+[live['actual_readback']]:raise ValueError('third final readiness and all five retained actual pixels')
 if not p['retained_ranges_unchanged'] or not p['original_fade_readiness_executed'] or any(p[k] is not False for k in ('text_skip_executed','confirmation_started','GPU_draw_or_present_executed','world_update_loop_executed')):raise ValueError('third natural wait exact scope')
 return {**result,'wait_updates':26,'object_readiness_calls':250,'original_input_queries':50,'released_PC':290,'confirmation_pending':True,'five_texture_bytes':[len(bytes.fromhex(r['hex'])) for r in p['actual_readbacks']]}

@lru_cache(maxsize=1)
def fixture():
 raw=EVIDENCE.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=EVIDENCE_SHA256:raise ValueError('pinned actual third live evidence')
 return json.loads(raw)

if __name__=='__main__':
 import sys
 sys.stdout.reconfigure(encoding='utf-8');print(report_text({'source_image_sha256':SOURCE_SHA256,'native_report_sha256':EVIDENCE_SHA256,'cases':[compare_wait(c) for c in fixture()['cases']]}),end='')
