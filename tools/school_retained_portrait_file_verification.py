"""Independent source replay to the original portrait allocation boundary."""
import copy,gzip,json,struct
from unicorn import Uc,UC_ARCH_X86,UC_MODE_32
from tools import school_retained_portrait_file as work
from tools.school_retained_render_pipeline_verification import Replay as SourceReplay
from tools.school_retained_rendering import AddressSpace
from tools.school_character_name_catalog import expected_complete,TEXTURE,PATH
from tools.school_font_raster_catalog import geometry,convert_surface
from tools.school_second_live_text_catalog import bands

ROOT=work.ROOT;base=work.base;need=work.need;word=work.word;sha=work.sha;canonical=work.canonical


def protocol(c):
 need(c['name'] in ('initial','student9_waiting','fifth_class') and c['scene_capture'] in (76,77),'six known source branches')
 need(len(c['steps'])==2 and [(s['label'],s['boundary']) for s in c['steps']]==[('continuous_original_name_texture_and_resource_path',work.IMAGE),('continuous_original_image_file_open_size_to_allocation',work.ALLOCATOR)],'two continuous source intervals')
 for s in c['steps']:need('root' not in s and s['IAT_unchanged'] is True,'no new game root or source IAT changes')
 first,second=[s['api_calls'] for s in c['steps']];need([a['kind'] for a in first]==['recorded_GPU']*4+['recorded_GDI_cleanup']*4 and [a['kind'] for a in second]==['actual_read_only_file']*3,'four native GPU/four cleanup replays and three actual file APIs');need([a['name'] for a in second]==['GetCurrentDirectoryA','CreateFileA','GetFileSize'],'only planned read-only file interfaces')
 h=c['actual_open_files_at_boundary'];need(len(h)==1 and type(h[0])is int and 0<h[0]<0xffffffff,'one actual source file handle');need(c['file_cleanup']==dict(actual_handles_closed=1,open_handles=0,all_owned_files_closed=True,explicit_probe_cleanup=True,original_CloseHandle_executed=False,invalid_handle_checks=[dict(handle=h[0],result=0,error=6)]),'explicit probe close and invalid-handle check, not original CloseHandle')
 need(c['pending_allocation']['va']==work.ALLOCATOR and c['pending_allocation']['args']==[262168] and c['pending_allocation']['return_va']==0x42ad54 and c['pending_allocation']['first_instruction_executed'] is False,'original allocation input/caller before first instruction');need(c['pending_image']['first_instruction_executed'] is False,'first interval ends before original image loader')
 b=bytes.fromhex(c['converted_texture_hex']);need(len(b)==8192 and sha(b)==c['converted_texture_sha256']==work.catalog.contracts()[1]['COM_calls'][3]['result']['uploaded_sha256'],'complete source pixels equal observed historical native upload')


class Replay(SourceReplay):
 def api(self,a):
  need(a['key']=='portrait_file_platform','only declared platform responses');r=a['call'];sp=self.cpu()['ESP'];ret=word(self.read(sp));args=[word(self.read(sp+4+4*i)) for i in range(r['pop']//4)];need(r['sp']==sp and r['return_va']==ret and r['args']==args and r['target']==a['va'],'exact original platform caller and arguments');maps=[];outputs=[];extra={};old=self.native;parent=self.case['parent_boundary'];o=parent['offscreen'];kind=r['kind'];frame=self.cpu()['EBP']
  def put(p,b):outputs.append(dict(pointer=p,hex=b.hex()))
  if kind=='recorded_GPU':
   index=self.gpu_count;need(index<4,'bounded historical texture transcript');row=old['COM_calls'][index];slot=[80,56,64,68][index];need(r['historical_call_index']==index and r['slot']==slot and r['historical_response']==row['result'] and ret==int(row['source_va'],16)+3,'pinned original COM call/reply/order');result=copy.deepcopy(row['result']);t=self.texture
   if index==0:
    need(a['va']==self.device_method and args==[self.device,128,32,1,0,25,1,TEXTURE+0x2c] and r['pop']==32,'source CreateTexture ABI and typed inherited device');result=copy.deepcopy(self.creation);maps=list(dict.fromkeys((p&~4095,4096) for p in [t['pointer'],t['vtable'],*t['methods'].values()]));put(t['pointer'],struct.pack('<I',t['vtable']))
    for offset,target in t['methods'].items():put(t['vtable']+int(offset),struct.pack('<I',target))
    put(args[-1],struct.pack('<I',t['pointer']))
   elif index==1:
    need(a['va']==t['methods']['56'] and args==[t['pointer'],0,frame-0x34] and r['pop']==12,'source original texture descriptor dispatch');put(args[2],bytes.fromhex(result['hex']))
   elif index==2:
    need(a['va']==t['methods']['64'] and args==[t['pointer'],0,word(self.read(frame+8)),0,0x800] and r['pop']==20,'source original lock output/flags');result=copy.deepcopy(self.lock);b=bytes.fromhex(result['hex']);p=result['bits']&~4095;maps=[(p,(result['bits']-p+len(b)+4095)&~4095)];put(result['bits'],b);put(args[2],struct.pack('<2I',result['pitch'],result['bits']))
   else:
    need(a['va']==t['methods']['68'] and args==[t['pointer'],0] and r['pop']==8,'original texture unlock dispatch');pixels=self.read(self.lock['bits'],8192);need(r['uploaded_hex']==pixels.hex() and sha(pixels)==result['uploaded_sha256'],'independent original complete texture write/upload bytes')
   need(r['result']==result,'exact typed projection of historical response');value=result['hr'];self.gpu_count+=1
  else:
   slot=r['import_slot'];api=r['name'];need(work.IMPORTS[slot]==(api,r['pop']) and a['va']==word(self.read(slot)),'original source IAT and exact platform ABI')
   if kind=='recorded_GDI_cleanup':
    index=self.cleanup_count;need(index<4,'bounded source GDI cleanup');oldrow=old['GDI_cleanup_calls'][index];old_bitmap=next(x['result'] for x in parent['parent_step']['api_calls'] if x['name']=='SelectObject' and x['return_va']==0x40541b);expected=[[o['raster_dc'],old_bitmap],[o['bitmap']],[o['raster_dc']],[o['font']]][index];need(api==oldrow['name'] and ret==int(oldrow['return_va'],16) and args==expected and r['historical_call_index']==index and r['historical_response']==oldrow and r['logical_object_roles_rebased'] is True,'exact original cleanup and pinned response under source-owned handle rebasing');value=o['bitmap'] if index==0 else oldrow['result'];self.cleanup_count+=1
   else:
    need(kind=='actual_read_only_file','no unobserved file/heap/game function');h=self.case['actual_open_files_at_boundary'][0]
    if api=='GetCurrentDirectoryA':
     b=(str(ROOT.resolve())+chr(0)).encode('mbcs');need(ret==0x42ac7a and args==[260,0x7a0ebc] and r['directory_hex']==b.hex(),'original bounded actual working-directory result');value=len(b)-1;put(args[1],b)
    elif api=='CreateFileA':
     raw=work.name.text(self,args[0]);need(ret==0x42ac9c and raw==b'data\\adv\\bin\\sc004.bin' and args[1:]==[0x80000000,1,0,3,1,0] and r['source_path_hex']==raw.hex() and r['native_absolute_read_only_path']==str(work.catalog.INSTALLED/'DATA/ADV/BIN/SC004.BIN') and r['declared_relative_path_binding'] is True,'natural original path and actual read-only source binding');value=h
    else:
     need(api=='GetFileSize' and ret==0x42ad0d and args==[h,0],'source owned file-size caller');value=len((work.catalog.INSTALLED/'DATA/ADV/BIN/SC004.BIN').read_bytes());need(value==262168,'independent source file size')
  need(r['new_mappings']==[dict(pointer=p,bytes=n) for p,n in maps] and r['memory_outputs']==outputs and r['value']==value,'independent full API outputs and only observed interface/mirror allocations')
  for p,n in maps:
   need(all(not(a<p+n and p<=b) for a,b,_ in self.u.mem_regions()),'independent fresh platform-response mapping');self.u.mem_map(p,n)
  for row in outputs:self.u.mem_write(row['pointer'],bytes.fromhex(row['hex']))
  self.u.reg_write(base.REGISTERS['EAX'],value);self.u.reg_write(base.REGISTERS['ESP'],sp+4+r['pop']);self.u.reg_write(base.REGISTERS['EIP'],ret)


def chain(r,expected):
 p=r.cpu()['EBP'];rows=[]
 for label,ret in expected:
  need(word(r.read(p+4))==ret,'independent original '+label+' frame');rows.append(dict(label=label,bp=p,return_va=ret));p=word(r.read(p))
 return rows


def verify_case(c):
 protocol(c);memory,cpu,provenance=work.boundary(c['name'],c['scene_capture']);need(canonical(c['parent_boundary'])==canonical(provenance),'complete independently verified parent boundary');r=Replay.__new__(Replay);r.u=Uc(UC_ARCH_X86,UC_MODE_32);r.image=base.SOURCE.read_bytes();r.objects={};r.locks={};r.case=c;r.native=work.catalog.contracts()[1];space=AddressSpace();space.next=0x68001000;r.creation=space.result('recorded_name',r.native['COM_calls'][0]['result']);r.lock=space.result('recorded_name',r.native['COM_calls'][2]['result']);r.texture=r.creation['texture'];r.gpu_count=r.cleanup_count=0;need(space.ledger()==c['typed_projection'],'independent typed projection of observed resource identity')
 for at,b in memory:r.u.mem_map(at,len(b));r.u.mem_write(at,b)
 r.u.context_restore(cpu);r.device=word(r.read(word(r.read(0x7a49fc))+0xb210));r.device_method=word(r.read(word(r.read(r.device))+80));need(r.cpu()['EIP']==0x403bd0 and work.name.portrait.regions(r)==c['before'],'continuous exact pending texture state');iat={slot:r.read(slot) for slot in work.IMPORTS};count=0;outer=provenance['parent_font_frames'][1:]
 for index,s in enumerate(c['steps']):
  maps=[]
  for at in [r.device_method,*[word(r.read(slot)) for slot in work.IMPORTS]]:
   if not any(a<=at<=b for a,b,_ in r.u.mem_regions()):p=at&~4095;r.u.mem_map(p,4096);maps.append(dict(pointer=p,bytes=4096))
  need(maps==s['entry_mappings'],'only missing original platform-entry pages mapped');calls=[dict(key='portrait_file_platform',va=a['target'],call=a) for a in s['api_calls']];r.u.ctl_remove_cache(s['before_cpu']['EIP'],s['before_cpu']['EIP']+1);count+=r.step(dict(label=s['label'],root=None,result=dict(s,api_calls=calls)))
  if index==0:
   expected=expected_complete(dict(after=c['before'],measured=provenance['offscreen']['measured']),r.texture['pointer'],r.device,c['accounting_before']);need(expected==c['expected_name'] and work.name.portrait.regions(r)==c['after_name_texture']==expected['after'] and word(r.read(0x765720))==expected['accounting_after'],'independent complete resource state/accounting');pixels=r.read(r.lock['bits'],8192);model=bytes.fromhex(r.lock['hex']);cfg=geometry(provenance['offscreen']['measured'])
   for band in bands(cfg):model=convert_surface(bytes.fromhex(provenance['parent_raster']['hex']),cfg['raster_size'],band['rect'],model,r.lock['pitch'],band['point'])
   need(model==pixels==bytes.fromhex(c['converted_texture_hex']),'independent every-pixel A1R5G5B5 conversion');sp=r.cpu()['ESP'];frames=chain(r,[('resource',0x4cc26d),*[(f['label'],f['return_va']) for f in outer]]);pending=dict(va=work.IMAGE,sp=sp,receiver=base.VM,args=[PATH,32],return_va=0x4cc0d2,frames=frames,first_instruction_executed=False)
   need(pending==c['pending_image'] and r.cpu()['ECX']==base.VM and [word(r.read(sp+i)) for i in (0,4,8)]==[0x4cc0d2,PATH,32] and frames[0]['bp']==outer[0]['bp']-120 and sp==frames[0]['bp']-116,'natural source image call and original outer frames');need(work.name.text(r,PATH)==b'data\\adv\\bin\\sc004.bin','original complete resource path')
 need(r.gpu_count==r.cleanup_count==4 and iat=={slot:r.read(slot) for slot in work.IMPORTS},'complete platform protocol and no IAT edits');sp=r.cpu()['ESP'];frames=chain(r,[('file_loader',0x42ae47),('file_wrapper',0x4cde36),('image',0x4cc0d2),*[(f['label'],f['return_va']) for f in c['pending_image']['frames']]]);pending=dict(va=work.ALLOCATOR,sp=sp,args=[262168],return_va=0x42ad54,frames=frames,first_instruction_executed=False)
 need(pending==c['pending_allocation'] and word(r.read(sp))==0x42ad54 and word(r.read(sp+4))==262168 and sp==frames[0]['bp']-100 and frames[1]['bp']==frames[2]['bp']-100 and frames[0]['bp']==frames[2]['bp']-204,'independent natural eight-frame original allocator request')
 need(base.memory_rows(r.u)==c['final_memory'] and canonical(base.architectural_cpu(r.u))==canonical(c['final_architectural_cpu']),'all final source memory and complete architectural CPU');need(word(r.read(0x765720))==c['accounting_after']==c['accounting_before']+8192,'original source texture accounting preserved through file boundary');visited={i['va'] for s in c['steps'] for i in s['instruction_counts']};need({0x405a80,0x56cda0,0x4cde10,0x42ae20,0x42ac50}<=visited and work.ALLOCATOR not in visited,'original pixel converter/CRT concat/image loader bodies and unexecuted allocator')
 return dict(name=c['name'],scene_capture=c['scene_capture'],new_original_instructions_replayed=count,original_writes=sum(s['writes'] for s in c['steps']),recorded_GPU_calls=4,recorded_GDI_cleanup_calls=4,actual_read_only_file_APIs=3,converted_texture_bytes=8192,full_final_memory_regions=len(c['final_memory']),natural_allocation_frames=len(frames),allocation_bytes=262168,allocator_executed=False,image_loader_completed=False,R3_complete=False)


def verify(r):
 need(r['schema_version']==1 and r['platform_contract']==work.catalog.contracts()[2] and r['new_game_roots']==r['game_function_substitutions']==r['IAT_rebindings']==0,'pinned source/platform scope without game substitutes')
 for k in ('new_GPU','new_window','new_OS_input','original_allocator_executed','original_ReadFile_executed','original_CloseHandle_executed','image_loader_completed','same_native_lifetime','R3_complete'):need(r[k] is False,'honest allocation-boundary scope '+k)
 need(r['recorded_GPU_and_GDI_cleanup_only'] is r['actual_read_only_file_open_and_size'] is True,'explicit recorded graphics and actual file API distinction');need([(c['name'],c['scene_capture']) for c in r['cases']]==[(n,s) for n in ('initial','student9_waiting','fifth_class') for s in (76,77)],'all six retained branches')
 for c in r['cases']:protocol(c)
 return dict(schema_version=1,cases=[verify_case(c) for c in r['cases']],six_original_texture_file_handoffs_verified=True,new_native_GPU=False,expired_native_handles_reused=False,original_allocator_executed=False,image_loader_completed=False,R3_complete=False)


if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('report');p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('fresh immutable proof required')
 r=json.loads(gzip.decompress((ROOT/a.report).read_bytes()));checked=verify(r);out.write_text(json.dumps(checked,indent=2)+chr(10),encoding='utf8',newline=chr(10));print('six original name texture and actual file handoffs independently verified',flush=True)
