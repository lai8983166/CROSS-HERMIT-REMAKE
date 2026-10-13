"""Source comparison for real character-name raster and retained parent proof."""
from tools.school_character_name_catalog import *
from tools.school_character_prefix_verification import compare_case as compare_prefix

def compare_parent(case,completed=False):
 first=case['first_live_text'];cleanup=first['COM_process_cleanup'];old=[case['second_live_text']['texture'],first['texture']]
 owned=([case['name_texture']['texture']] if completed else [])+old
 if cleanup['texture_releases']!=[{'pointer':t['pointer'],'unlock_hr':0,'count':0} for t in owned] or not cleanup['all_owned_resources_released']:raise ValueError('actual complete name/parent COM cleanup')
 wanted={'fonts':0 if completed else 1,'bitmaps':0 if completed else 1,'dcs':3 if completed else 4,'all_resources_released':True}
 if first['remaining_GDI_cleanup']!=wanted or not first['process_exited']:raise ValueError('actual complete name/parent GDI cleanup')
 # Verification-only projection of observed cleanup to already proven resources.
 # The immutable native evidence retains the actual full cleanup unchanged.
 view=dict(case);f=dict(first);c=dict(cleanup);c['texture_releases']=cleanup['texture_releases'][-2:]
 f['COM_process_cleanup']=c;f['remaining_GDI_cleanup']={'fonts':0,'bitmaps':0,'dcs':2,'all_resources_released':True};view['first_live_text']=f
 compare_prefix(view)

def compare_raster(case,completed=False):
 compare_parent(case,completed);p=case['name_raster'];prefix=case['character_prefix'];rules=name_rules();api=p['font_api']
 if p['before']!=prefix['after'] or p['inputs']['parent_prefix_sha256']!=PREFIX_SHA:raise ValueError('name complete actual prefix')
 if not api or api[0]['name']!='CreateFontA' or api[0]['args']!=rules['prefix']['font_args'] or api[0]['return_va']!='0x4ca7cb':raise ValueError('name original font request')
 inputs=p['inputs'];first=case['first_live_text']
 if inputs['graphics_context']!=first['raster']['inputs']['graphics_context'] or inputs['device']!=first['binding']['bound'] or inputs['platform']!='real_host_GDI_offscreen_measurement_DC' or inputs['host_ansi_code_page']<=0:raise ValueError('name actual host platform')
 e=expected_raster(p['before'],p['measured'],inputs['graphics_context'],api[0]['result'])
 if p['after']!=e['after'] or p['entry']!=pending_texture(prefix) or p['text_hex']!=rules['prefix']['name']['hex']:raise ValueError('name complete state/stack/source text')
 if p['pending_texture']!={'va':'0x403bd0','receiver':TEXTURE,'args':[inputs['device'],0],'return_va':'0x405779','first_instruction_executed':False,'natural_stack_verified':True}:raise ValueError('name exact natural texture entry')
 r=p['raster'];raw=bytes.fromhex(r['hex'])
 if r['pointer']!=RASTER or r['size']!=e['raster_size'] or len(raw)!=r['size'][0]*r['size'][1]*4 or hashlib.sha256(raw).hexdigest()!=r['sha256']:raise ValueError('name real raster complete buffer')
 dib=next(x for x in api if x['name']=='CreateDIBSection')
 if dib['header_hex']!=e['header_hex'] or dib['virtual_bits_pointer']!=RASTER:raise ValueError('name original DIB geometry')
 copy=p['crt'];f=prefix['pending_font']['frames']['name']
 if copy!=[{'name':'bounded_source_copy','target':f-0x108,'source':rules['prefix']['name']['pointer'],'hex':rules['prefix']['name']['hex'],'return_va':'0x4ca7f0'}]:raise ValueError('name exact original copy')
 if p['prior_actual_readbacks']!=prefix['actual_readbacks'] or not p['retained_ranges_unchanged']:raise ValueError('name full prior resource retention')
 if not p['real_name_font_and_raster_executed'] or any(p[k] is not False for k in ('name_texture_created','image_load_executed','GPU_draw_or_present_executed')):raise ValueError('name raster exact boundary')
 compare_api(p,prefix)
 return {'name':case['name'],'measured':p['measured'],'raster_size':r['size'],'raster_bytes':len(raw),'complete_regions':len(REGIONS),'prior_texture_bytes':[len(bytes.fromhex(x['hex'])) for x in p['prior_actual_readbacks']],
  'retained_bytes':p['retained_bytes'],'name_texture_created':False}

def compare_api(p,prefix):
 api=p['font_api']
 if len(api)!=23:raise ValueError('name bounded original GDI sequence')
 font=api[0]['result'];measure=api[2]['args'][0];old_font=api[2]['result'];dc=api[6]['result'];bitmap=api[7]['result'];brush=api[10]['result']
 if any(type(v)is not int or not 0<v<0xFFFFFFFF for v in (font,measure,old_font,dc,bitmap,brush)):raise ValueError('name actual owned GDI handles')
 f=prefix['pending_font']['frames']['name']-0x1D4;text=prefix['pending_font']['frames']['name']-0x108;n=len(bytes.fromhex(name_rules()['prefix']['name']['hex']));cfg=geometry(p['measured']);pad=cfg['padding'];w,h=cfg['raster_size']
 expected=[('CreateFontA','0x4ca7cb',name_rules()['prefix']['font_args']),('lstrlenA','0x4051ba',[text]),('SelectObject','0x4051ea',[measure,font]),
  ('lstrlenA','0x405230',[text]),('GetTextExtentPoint32A','0x405246',[measure,text,n,f-0x54]),('SelectObject','0x40528a',[measure,old_font]),
  ('CreateCompatibleDC','0x405373',[0]),('CreateDIBSection','0x4053cc',[dc,f-0x38,0,f-0x3C,0,0]),('SelectObject','0x40541b',[dc,bitmap]),
  ('SetMapMode','0x40545d',[dc,1]),('GetStockObject','0x405471',[4]),('SelectObject','0x405485',[dc,brush]),('PatBlt','0x4054ac',[dc,0,0,w,h,0xF00021]),
  ('SelectObject','0x4054c6',[dc,font]),('SetBkMode','0x405508',[dc,1]),('SetBkColor','0x405520',[dc,0]),('SetTextAlign','0x405535',[dc,0]),
  ('SetTextColor','0x405663',[dc,0x80808]),('lstrlenA','0x405676',[text]),('TextOutA','0x40569c',[dc,2*pad,2*pad,text,n]),
  ('SetTextColor','0x4056b4',[dc,0xFFFFFF]),('lstrlenA','0x4056c7',[text]),('TextOutA','0x4056e7',[dc,pad,pad,text,n])]
 if [(x['name'],x['return_va'],x['args']) for x in api]!=expected:raise ValueError('name every original GDI argument/caller')
 if api[4]['measured']!=p['measured'] or api[4]['selected_face']!=p['selected_face']:raise ValueError('name real measurement provenance')
 for x in api:
  if x['name']=='lstrlenA' and x['result']!=n:raise ValueError('name source length')

def compare_texture(case):
 result=compare_raster(case,True);p=case['name_texture'];raster=case['name_raster'];prefix=case['character_prefix'];first=case['first_live_text'];texture=p['texture'];device=first['binding']['bound']
 if p['before']!=raster['after'] or texture['pointer'] in [x['texture']['pointer'] for x in (first,case['second_live_text'])]:raise ValueError('name third independent actual resource')
 e=expected_complete(raster,texture['pointer'],device,p['accounting_before']);width,height=e['texture_size'];f=prefix['pending_font']['frames']['name']-0x1D4
 if p['after']!=e['after'] or p['accounting_after']!=e['accounting_after'] or p['accounting_before']!=case['second_live_text']['accounting_after']:raise ValueError('name full source state/accounting')
 if p['pending_image']!=pending_image(prefix) or p['path']!=e['path']:raise ValueError('name original image entry/path')
 calls=[]
 for at,offset,args in zip(('0x403c87','0x403cbb','0x40395b','0x4039d0'),(80,56,64,68),
  ([device,width,height,1,0,25,1,TEXTURE+0x2C],[texture['pointer'],0,prefix['pending_font']['frames']['name']-0x310],[texture['pointer'],0,f-0x84,0,0x800],[texture['pointer'],0])):
  identity=first['platform_hello']['device'] if offset==80 else texture
  calls.append({'source_va':at,'offset':offset,'args':args,'vtable':identity['vtable'],'actual_method':identity['methods'][str(offset)]})
 if len(p['COM_calls'])!=4:raise ValueError('name original COM count')
 for actual,expected in zip(p['COM_calls'],calls):
  if any(actual[k]!=v for k,v in expected.items()) or actual['result']['hr']!=0:raise ValueError('name every original COM dispatch')
 if p['COM_calls'][0]['result']['texture']!=texture:raise ValueError('name created texture identity')
 if struct.unpack('<8I',bytes.fromhex(p['COM_calls'][1]['result']['hex']))!=(25,1,0,1,width*height*2,0,width,height):raise ValueError('name actual descriptor')
 lock=p['lock'];pitch=lock['pitch'];initial=bytes.fromhex(lock['before_hex']);cfg=geometry(raster['measured']);raw=bytes.fromhex(raster['raster']['hex'])
 if type(pitch)is not int or not width*2<=pitch<=4096 or pitch%2 or len(initial)!=pitch*height or lock['mirror']!=MIRROR:raise ValueError('name bounded actual lock')
 actual_lock=p['COM_calls'][2]['result']
 if (actual_lock['pitch'],actual_lock['bits'],actual_lock['hex'])!=(pitch,lock['host_bits'],lock['before_hex']):raise ValueError('name real lock provenance')
 out=initial;conversions=[]
 for b in bands(cfg):
  out=convert_surface(raw,cfg['raster_size'],b['rect'],out,pitch,b['point'])
  conversions.append({'source_va':'0x405869','args':[RASTER,f-0x84,*cfg['raster_size'],f-0x98,f-0xA8],'lock_hex':struct.pack('<2I',pitch,MIRROR).hex(),**b})
 readback=p['actual_readback']
 if p['conversion_calls']!=conversions or lock['after_hex']!=out.hex() or readback['hex']!=out.hex() or readback['sha256']!=hashlib.sha256(out).hexdigest() or readback['pitch']!=pitch or readback['hr']!=0 or readback['unlock_hr']!=0:raise ValueError('name full original converted texture/readback')
 if p['prior_actual_readbacks']!=prefix['actual_readbacks'] or not p['retained_ranges_unchanged']:raise ValueError('name both prior complete resources retained')
 api=raster['font_api'];dc=api[6]['result'];bitmap=api[7]['result'];font=api[0]['result'];old=api[8]['result']
 if p['GDI_cleanup_calls']!=[{'name':'SelectObject','args':[dc,old],'return_va':'0x4058d8','result':bitmap},{'name':'DeleteObject','args':[bitmap],'return_va':'0x405921','result':1},
  {'name':'DeleteDC','args':[dc],'return_va':'0x40596a','result':1},{'name':'DeleteObject','args':[font],'return_va':'0x4d1c1b','result':1}]:raise ValueError('name original cleanup sequence')
 remote=[]
 for at in ('0x403c81','0x403cb8','0x403958','0x4039cd'):
  identity=first['platform_hello']['device'] if at=='0x403c81' else texture;remote.append({'source_va':at,'pointer':identity['pointer'],'vtable':identity['vtable']})
 if p['remote_reads']!=remote:raise ValueError('name actual remote COM reads')
 if p['path_calls']!=[{'name':'bounded_source_concat','target':PATH,'source':0x5BFD60,'before_hex':b'data\\adv\\bin\\'.hex(),'after_hex':e['path'].encode('ascii').hex(),'return_va':'0x4cd83a'}]:raise ValueError('name declared exact CRT path primitive')
 if not p['original_name_texture_upload_executed'] or not p['original_name_font_cleanup_executed'] or not p['name_handler_completed'] or any(p[k] is not False for k in ('image_loader_executed','layer_handler_completed','GPU_draw_or_present_executed','world_update_loop_executed')):raise ValueError('name exact image boundary')
 return {**result,'name_texture_created':True,'third_texture_bytes':len(out),'texture_size':e['texture_size'],'band_calls':len(conversions),'image_path':p['path'],'image_slot':32,'retained_bytes':p['retained_bytes']}

if __name__=='__main__':
 import sys
 sys.stdout.reconfigure(encoding='utf-8');p=argparse.ArgumentParser();p.add_argument('report');p.add_argument('--texture',action='store_true');a=p.parse_args();path=ROOT/a.report;raw=path.read_bytes();d=json.loads(raw)
 print(report_text({'native_sha256':hashlib.sha256(raw).hexdigest(),'cases':[(compare_texture if a.texture else compare_raster)(c) for c in d['cases']]}),end='')
