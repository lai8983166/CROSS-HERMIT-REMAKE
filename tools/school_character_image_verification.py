"""Independent real-file, original DX resource, all-row and ownership proof."""
from tools.school_character_image_catalog import *
from tools.school_character_name_verification import compare_texture as compare_name

def parent_view(case,completed=False):
 first=case['first_live_text'];cleanup=first['COM_process_cleanup']
 old=[case['name_texture']['texture'],case['second_live_text']['texture'],first['texture']]
 owned=([case['image_live']['texture']] if completed else [])+old
 if cleanup['texture_releases']!=[{'pointer':t['pointer'],'unlock_hr':0,'count':0} for t in owned] or not cleanup['all_owned_resources_released'] or not first['process_exited']:raise ValueError('image actual complete COM ownership/cleanup')
 view=dict(case);f=dict(first);c=dict(cleanup);c['texture_releases']=cleanup['texture_releases'][-3:];f['COM_process_cleanup']=c;view['first_live_text']=f
 compare_name(view)

def compare_prefix(case,completed=False):
 parent_view(case,completed);p=case['image_prefix'];parent=case['name_texture'];f=frames(parent)
 if p['before']!=parent['after']:raise ValueError('image natural completed name parent')
 expected=expected_prefix(p['before'])
 if any(p[k]!=expected[k] for k in ('after','record_hex','table_hex')):raise ValueError('image full source prefix state')
 if p['renderer']!=case['first_live_text']['raster']['inputs']['graphics_context'] or p['table_address']!=p['renderer']+0x844+32*8:raise ValueError('image actual source table')
 if p['array_hex']!=struct.pack('<I',1).hex()+expected['record_hex'] or p['actual_file_sha256']!=RESOURCE_SHA or p['file_buffer_sha256']!=RESOURCE_SHA:raise ValueError('image full loaded source/container array')
 pending={'va':0x403BD0,'receiver':RECORD,'args':[case['first_live_text']['binding']['bound'],0],'return_va':0x4050B4,'sp':f['texture_sp'],'ebp':f['dx'],'first_instruction_executed':False}
 if p['pending_texture']!=pending:raise ValueError('image exact original texture stack')
 calls=p['file_calls']
 if len(calls)!=5:raise ValueError('image original file call count')
 handle=calls[1]['result'];base=str((ROOT/'CROSS HERMIT/CROSS HERMIT').resolve()).encode('ascii')
 expected_calls=[('GetCurrentDirectoryA',0x592214,[260,0x7A0EBC],'0x42ac7a',len(base)),('CreateFileA',0x5921EC,[PATH,0x80000000,1,0,3,1,0],'0x42ac9c',handle),
  ('GetFileSize',0x5921F0,[handle,0],'0x42ad0d',262168),('ReadFile',0x5921E8,[handle,FILE_BUFFER,262168,f['file_loader']-12,0],'0x42ad82',1),('CloseHandle',0x592270,[handle],'0x42ada5',1)]
 if type(handle)is not int or not 0<handle<0xFFFFFFFF or [(r['name'],int(r['slot'],16),r['args'],r['return_va'],r['result']) for r in calls]!=expected_calls:raise ValueError('image every original real-file call/handle')
 if p['file_cleanup']!={'actual_handles_closed':1,'open_handles':0,'all_owned_files_closed':True}:raise ValueError('image real file close')
 alloc=[{'pointer':FILE_BUFFER,'bytes':262168,'kind':'file_buffer','return_va':'0x42ad54','freed':False},{'pointer':ARRAY,'bytes':88,'kind':'texture_array','return_va':'0x41f142','freed':False}]
 if p['allocations']!=alloc or p['SEH_pending_hex']!=struct.pack('<I',f['container']-12).hex():raise ValueError('image original allocation/SEH')
 if p['prior_actual_readbacks']!=parent['prior_actual_readbacks']+[parent['actual_readback']] or not p['retained_ranges_unchanged']:raise ValueError('image all three prior pixels/retention')
 if not p['real_file_API_executed'] or not p['original_vector_constructor_executed'] or any(p[k] is not False for k in ('image_texture_created','image_loader_returned','GPU_draw_or_present_executed')):raise ValueError('image prefix exact scope')
 return {'name':case['name'],'loaded_bytes':262168,'table_slot':32,'complete_regions':len(REGIONS),'prior_texture_bytes':[len(bytes.fromhex(x['hex'])) for x in p['prior_actual_readbacks']],
  'retained_bytes':p['retained_bytes'],'image_texture_created':False}

def compare_live(case):
 result=compare_prefix(case,True);p=case['image_live'];prefix=case['image_prefix'];parent=case['name_texture'];f=frames(parent);dev=case['first_live_text']['binding']['bound'];tex=p['texture']['pointer']
 if p['before']!=prefix['after'] or tex in [x['pointer'] for x in (case['first_live_text']['texture'],case['second_live_text']['texture'],parent['texture'])]:raise ValueError('image fourth independent actual texture')
 expected=expected_complete(p['before'],dev,tex)
 if any(p[k]!=expected[k] for k in ('after','record_hex','table_hex')) or p['array_hex']!=struct.pack('<I',1).hex()+expected['record_hex'] or p['file_buffer_sha256']!=RESOURCE_SHA:raise ValueError('image full source return/table/array/buffer')
 if p['table_address']!=prefix['table_address']:raise ValueError('image captured table retained')
 calls=p['COM_calls'];lock=p['lock'];pitch=lock['pitch'];ptr=p['texture'];dx=f['dx'];copy_frame=dx-76-12-12-8
 wanted_args=[[dev,256,512,1,0,25,1,RECORD+0x2C],[tex,0,f['texture_sp']-4-0x34],[tex,0,copy_frame-0xC,0,0x800],[tex,0]]
 if len(calls)!=4:raise ValueError('image original COM count')
 for c,at,offset,args in zip(calls,('0x403c87','0x403cbb','0x40395b','0x4039d0'),(80,56,64,68),wanted_args):
  identity=case['first_live_text']['platform_hello']['device'] if offset==80 else ptr
  if c['source_va']!=at or c['offset']!=offset or c['args']!=args or c['vtable']!=identity['vtable'] or c['actual_method']!=identity['methods'][str(offset)] or c['result']['hr']!=0:raise ValueError('image every original actual COM call')
 if calls[0]['result']['texture']!=ptr or struct.unpack('<8I',bytes.fromhex(calls[1]['result']['hex']))!=(25,1,0,1,262144,0,256,512):raise ValueError('image actual texture descriptor')
 actual_lock=calls[2]['result']
 if (actual_lock['pitch'],actual_lock['bits'],actual_lock['hex'])!=(pitch,lock['host_bits'],lock['before_hex']) or lock['mirror']!=IMAGE_MIRROR:raise ValueError('image actual lock provenance')
 out=expected_pixels(bytes.fromhex(lock['before_hex']),pitch);rb=p['actual_readback']
 if rb['hex']!=out.hex() or lock['after_hex']!=out.hex() or rb['pitch']!=pitch or rb['sha256']!=hashlib.sha256(out).hexdigest() or rb['hr']!=0 or rb['unlock_hr']!=0:raise ValueError('image all original DX rows/padding/readback')
 rows=[{'row':i,'args':[IMAGE_MIRROR+i*pitch,FILE_BUFFER+24+i*512,512],'return_va':'0x40483f'} for i in range(512)]
 if p['rows']!=rows:raise ValueError('image every original memcpy row input')
 remote=[]
 for at in ('0x403c81','0x403cb8','0x403958','0x4039cd'):
  identity=case['first_live_text']['platform_hello']['device'] if at=='0x403c81' else ptr;remote.append({'source_va':at,'pointer':identity['pointer'],'vtable':identity['vtable']})
 if p['remote_reads']!=remote:raise ValueError('image actual remote COM ownership')
 allocations=[dict(a) for a in prefix['allocations']];allocations[0]['freed']=True
 if p['allocations']!=allocations or p['SEH_after_hex']!=prefix['SEH_before_hex'] or p['natural_return']!={'va':0x4CC0D2,'sp':parent['pending_image']['frames']['sp']+12,'ebp':parent['pending_image']['frames']['resource'],'eax':0}:raise ValueError('image natural return/declared free/SEH restore')
 if p['accounting_before']!=parent['accounting_after'] or p['accounting_after']!=p['accounting_before']+262144 or p['prior_actual_readbacks']!=prefix['prior_actual_readbacks'] or not p['retained_ranges_unchanged']:raise ValueError('image accounting/three prior resources/retention')
 if not p['image_texture_created'] or not p['original_rows_uploaded'] or not p['image_loader_returned'] or any(p[k] is not False for k in ('animation_executed','GPU_draw_or_present_executed','world_update_loop_executed')):raise ValueError('image exact completed scope')
 return {**result,'image_texture_created':True,'image_loader_returned':True,'image_bytes':len(out),'original_row_copies':512,'PC':252,'retained_bytes':p['retained_bytes']}

if __name__=='__main__':
 import sys
 sys.stdout.reconfigure(encoding='utf-8');parser=argparse.ArgumentParser();parser.add_argument('report');parser.add_argument('--live',action='store_true');a=parser.parse_args();raw=(ROOT/a.report).read_bytes();d=json.loads(raw)
 print(report_text({'native_sha256':hashlib.sha256(raw).hexdigest(),'cases':[(compare_live if a.live else compare_prefix)(c) for c in d['cases']]}),end='')
