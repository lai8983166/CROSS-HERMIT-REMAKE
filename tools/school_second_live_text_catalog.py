"""Independent source comparison for the completed second original text."""
import argparse,hashlib,json,struct
from functools import lru_cache
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from tools.school_next_text_catalog import ROOT,SOURCE,SOURCE_SHA256,BASE,VM,OBJECT_OFFSET,NODE_OFFSET,REGIONS,memory_regions,AUTHORITY,report_text,compare_case as compare_prefix,expected_next
from tools.school_font_raster_catalog import geometry,convert_surface,TEXTURE_OFFSET,source_catalog as raster_rules
from tools.school_live_text_catalog import source_catalog as live_rules
from tools.school_text_timing_catalog import expected_update,BYTES,source_catalog as timing_rules
from tools.school_texture_contract import power_of_two

EVIDENCE=ROOT/'analysis/school-second-live-text-v2-20261013.json'
EVIDENCE_SHA256='bbd276d0bbdb8b18809a4395ab57127b41a663c42c48ad4dcd3f76f18f17eaed'
TEXTURE2=TEXTURE_OFFSET+0x110
RASTER2=0x38000000;MIRROR2=0x39000000

@lru_cache(maxsize=1)
def source_catalog():
 raw=SOURCE.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA256:raise ValueError('second original image identity')
 pairs={0x4057B4:('cmp','ecx, dword ptr [ebp - 0x60]'),0x4057C7:('cmp','edx, 0x100'),0x4057CD:('jae','0x40586e'),
  0x4057D6:('shl','eax, 8'),0x4057DC:('sub','ecx, eax'),0x4057DE:('cmp','ecx, 0x100'),
  0x405806:('shl','ecx, 8'),0x40583B:('imul','ecx, dword ptr [ebp - 0x64]'),0x405869:('call','0x405a80')}
 md=Cs(CS_ARCH_X86,CS_MODE_32);proof=[]
 for at,pair in pairs.items():
  ins=next(md.disasm(raw[at-BASE:at-BASE+16],at,count=1))
  if (ins.mnemonic,ins.op_str)!=pair:raise ValueError('second band source instruction differs')
  proof.append({'va':hex(at),'hex':ins.bytes.hex(),'mnemonic':ins.mnemonic,'operands':ins.op_str})
 return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'band_code_inputs':proof,'inherited_raster_code':raster_rules()['code_inputs'],
  'inherited_live_code':live_rules()['code_inputs'],'inherited_timing_code':timing_rules()['code_inputs'],
  'row_stride':0x110,'second_texture_offset':TEXTURE2,'next_PC':244,'draw_body_executed':False,
  'scope':'Original second text/VM completion with real declared platform and exact terminal drawing; no renderer startup/GPU/Present/world/waves.',**AUTHORITY}

def bands(cfg):
 width,height=cfg['raster_size'];result=[]
 for i in range(cfg['bands']):
  if (i+1)*height>=256:continue
  size=min(256,width-i*256)
  if size<=0:raise ValueError('zero-width band unsupported by bounded surface comparison')
  result.append({'rect':[i*256,0,size,height],'point':[0,i*height]})
 return result

def expected(p,first):
 raster=p['raster'];prep=p['preparation'];derived=expected_next(prep['inputs'],first['after'])
 if raster['before']!=derived['after']:raise ValueError('second complete font parent mismatch')
 cfg=geometry(raster['measured']);mem=memory_regions(raster['before']);vm=mem[VM];o=TEXTURE2
 inputs=raster['inputs'];device=first['binding']['bound'];tex=p['texture']['pointer']
 if type(tex)is not int or not 0<tex<0xFFFFFFFF or tex==first['texture']['pointer'] or inputs['device']!=device or inputs['graphics_context']!=first['raster']['inputs']['graphics_context'] or inputs['platform']!='real_host_GDI_offscreen_measurement_DC':raise ValueError('second independent live ownership')
 if raster['text_hex']!=derived['second_text']['hex'] or inputs['parent_text_sha256']!='47e76776fc4eaddf701e99242bccd0968029093ce2faf6056cf3492f0614f69a':raise ValueError('second source string/provenance')
 if struct.unpack_from('<2I',vm,o+0x2C)!=(0,0) or struct.unpack_from('<H',vm,OBJECT_OFFSET+22)[0]!=1:raise ValueError('second empty texture/single completed line required')
 struct.pack_into('<I',vm,o+0x28,0);struct.pack_into('<I',vm,o+0x4C,inputs['graphics_context']);vm[o+0x64:o+0x68]=bytes([255]*4)
 struct.pack_into('<I',vm,o+0x34,25);struct.pack_into('<2H',vm,o+0x38,*cfg['texture_size']);struct.pack_into('<2H',vm,o+0x40,*cfg['raster_size'])
 prefix=[{'pointer':a,'bytes':n,'hex':mem[a].hex()} for a,n in REGIONS]
 if prefix!=raster['after'] or prefix!=p['before']:raise ValueError('second complete raster prefix differs')
 width,height=[power_of_two(v) for v in cfg['texture_size']]
 struct.pack_into('<2I',vm,o+0x28,device,tex);struct.pack_into('<2H',vm,o+0x3C,width,height)
 struct.pack_into('<H',vm,o+0x44,struct.unpack_from('<H',vm,o+0x44)[0]|6);struct.pack_into('<H',vm,OBJECT_OFFSET+22,2)
 update_before=bytes(vm[OBJECT_OFFSET:OBJECT_OFFSET+BYTES]);origin=list(struct.unpack_from('<2H',vm,NODE_OFFSET+30));update=expected_update(update_before,origin,VM+OBJECT_OFFSET)
 vm[OBJECT_OFFSET:OBJECT_OFFSET+BYTES]=bytes.fromhex(update['after_hex']);struct.pack_into('<I',vm,0x1C,244);struct.pack_into('<H',vm,NODE_OFFSET+4,struct.unpack_from('<H',vm,NODE_OFFSET+2)[0])
 lock=p['lock'];pitch=lock['pitch'];before=bytes.fromhex(lock['before_hex']);raw=bytes.fromhex(raster['raster']['hex'])
 if type(pitch)is not int or not width*2<=pitch<=4096 or pitch%2 or len(before)!=pitch*height or raster['raster']['size']!=cfg['raster_size'] or raster['raster']['pointer']!=RASTER2 or lock['mirror']!=MIRROR2:raise ValueError('second full surface geometry/binding')
 out=before
 if hashlib.sha256(raw).hexdigest()!=raster['raster']['sha256']:raise ValueError('second real raster digest')
 for b in bands(cfg):out=convert_surface(raw,cfg['raster_size'],b['rect'],out,pitch,b['point'])
 font=derived['pending_font']['frames']['font'];f=font-0x1DC;pointer=VM+o
 calls=[]
 for at,offset,args in zip(('0x403c87','0x403cbb','0x40395b','0x4039d0'),(80,56,64,68),
   ([device,width,height,1,0,25,1,pointer+0x2C],[tex,0,font-0x318],[tex,0,f-0x84,0,0x800],[tex,0])):
  identity=first['platform_hello']['device'] if offset==80 else p['texture']
  calls.append({'source_va':at,'offset':offset,'args':args,'vtable':identity['vtable'],'actual_method':identity['methods'][str(offset)]})
 conversions=[{'source_va':'0x405869','args':[RASTER2,f-0x84,*cfg['raster_size'],f-0x98,f-0xA8],
  'lock_hex':struct.pack('<2I',pitch,MIRROR2).hex(),**b} for b in bands(cfg)]
 return {'after':[{'pointer':a,'bytes':n,'hex':mem[a].hex()} for a,n in REGIONS],'pixel_hex':out.hex(),'texture_size':[width,height],
  'accounting_after':(p['accounting_before']+width*height*2)&0xFFFFFFFF,'update_before_hex':update_before.hex(),'text_draws':update['draws'],
  'text_updates':[{'args':[(VM+NODE_OFFSET)&0xFFFF0000|origin[0],origin[1]],'return_va':'0x4cd541','receiver':VM+OBJECT_OFFSET}],
  'entry':{'sp':font-0x2E0,'ebp':f,'return_va':0x405779},'COM_calls':calls,'conversion_calls':conversions}

def compare_case(case):
 first=case['first_live_text'];p=case['second_live_text'];compare_prefix({'first_live_text':first,'next_text':p['preparation']});e=expected(p,first)
 for key in ('after','accounting_after','update_before_hex','text_draws','text_updates','entry','conversion_calls'):
  if p[key]!=e[key]:raise ValueError('second independent source differs: '+key)
 if e['pixel_hex']!=p['actual_readback']['hex'] or e['pixel_hex']!=p['lock']['after_hex'] or first['actual_readback']!=p['first_actual_readback']:raise ValueError('second both complete actual textures differ')
 if len(p['COM_calls'])!=4:raise ValueError('second bounded COM count')
 for call,derived in zip(p['COM_calls'],e['COM_calls']):
  if any(call[k]!=v for k,v in derived.items()) or call['result']['hr']!=0:raise ValueError('second original COM dispatch')
 if p['COM_calls'][0]['result']['texture']!=p['texture']:raise ValueError('second created texture identity')
 lock=p['lock'];actual_lock=p['COM_calls'][2]['result']
 if (actual_lock['pitch'],actual_lock['bits'],actual_lock['hex'])!=(lock['pitch'],lock['host_bits'],lock['before_hex']):raise ValueError('second real lock/mirror provenance')
 readback=p['actual_readback']
 if readback['pitch']!=lock['pitch'] or readback['hr']!=0 or readback['unlock_hr']!=0 or readback['sha256']!=hashlib.sha256(bytes.fromhex(e['pixel_hex'])).hexdigest():raise ValueError('second actual complete readback provenance')
 width,height=e['texture_size']
 if struct.unpack('<8I',bytes.fromhex(p['COM_calls'][1]['result']['hex']))!=(25,1,0,1,width*height*2,0,width,height):raise ValueError('second actual texture descriptor')
 api=p['raster']['font_api'];dc=next(r['result'] for r in api if r['name']=='CreateCompatibleDC');bitmap=next(r['result'] for r in api if r['name']=='CreateDIBSection');font=api[0]['result'];old=next(r['result'] for r in api if r['return_va']=='0x40541b')
 dib=next(r for r in api if r['name']=='CreateDIBSection')
 if dib['header_hex']!=geometry(p['raster']['measured'])['header_hex'] or dib['virtual_bits_pointer']!=RASTER2:raise ValueError('second source DIB header')
 wanted=[{'name':'SelectObject','args':[dc,old],'return_va':'0x4058d8','result':bitmap},
  {'name':'DeleteObject','args':[bitmap],'return_va':'0x405921','result':1},{'name':'DeleteDC','args':[dc],'return_va':'0x40596a','result':1},{'name':'DeleteObject','args':[font],'return_va':'0x4d1c1b','result':1}]
 if p['GDI_cleanup_calls']!=wanted:raise ValueError('second original GDI cleanup sequence')
 remote=[]
 for at in ('0x403c81','0x403cb8','0x403958','0x4039cd'):
  identity=first['platform_hello']['device'] if at=='0x403c81' else p['texture']
  remote.append({'source_va':at,'pointer':identity['pointer'],'vtable':identity['vtable']})
 if p['remote_reads']!=remote:raise ValueError('second original remote vtable reads')
 if p['presentation']!=first['presentation']:raise ValueError('second original retained board presentation')
 if p['natural_return']!={'va':0x3000000,'sp':0x200FF04,'eax':1} or not p['first_resource_retained'] or not p['retained_ranges_unchanged'] or not first['process_exited']:raise ValueError('second natural return/retention')
 cleanup=first['COM_process_cleanup']
 if cleanup['texture_releases']!=[{'pointer':t['pointer'],'unlock_hr':0,'count':0} for t in (p['texture'],first['texture'])] or not cleanup['all_owned_resources_released']:raise ValueError('second owned resource cleanup')
 if first['remaining_GDI_cleanup']!={'fonts':0,'bitmaps':0,'dcs':2,'all_resources_released':True}:raise ValueError('second GDI cleanup')
 if any(p[k] is not False for k in ('original_text_draw_body_executed','GPU_draw_or_present_executed','original_renderer_startup_executed','dialogue_playback_completed','waves_executed','world_update_loop_executed','full_task_wrapper_executed')):raise ValueError('second scope')
 return {'complete_regions_compared':len(REGIONS),'second_actual_texture_bytes':len(bytes.fromhex(e['pixel_hex'])),'first_actual_texture_bytes':len(bytes.fromhex(p['first_actual_readback']['hex'])),
  'texture_size':e['texture_size'],'band_calls':len(e['conversion_calls']),'terminal_text_draws':len(e['text_draws']),'PC':244,'completed_text_records':2,'retained_bytes':p['retained_bytes']}

@lru_cache(maxsize=1)
def native_fixture():
 raw=EVIDENCE.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=EVIDENCE_SHA256:raise ValueError('second native evidence identity')
 return json.loads(raw)

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify',action='store_true');a=p.parse_args()
 if a.verify:print(report_text({'source':source_catalog(),'native_report_sha256':EVIDENCE_SHA256,'cases':[{'name':c['name'],**compare_case(c)} for c in native_fixture()['cases']]}))
