"""Independent retired mapping, second95 glyphs and65536-pixel upload proof."""
import argparse
import hashlib
import json
import struct
from tools.school_font_second_glyph import *
from tools.school_font_second_ink import ink_rectangles
from tools.school_font_second_glyph_emulation import OWNER,STACK,TOP,RETURN,COUNTER,dword,store
from tools.school_font_second_glyph_platform import DEVICE_SOURCE,DEVICE_HELPER,GDI_SOURCE,GDI_HELPER,COMPILER,sha,machine
from tools.school_font_second_resource_verification import (verify_prefix,verify_atlas,verify_gdi,verify_raster,
    verify_pixels,verify_phase,verify_second,verify_resource,device_calls,platform_calls,verify_trace,unpack,verify_buffer)


def verify_memory(row,previous,owner,image):
    verify_buffer(row['state']['owner'],owner)
    if (row['state']['image_sha256']!=hashlib.sha256(image).hexdigest() or row['state']['SEH']!=TOP-108
            or row['state']['stack_guards_unchanged'] is not True or row['state']['foreign_maps']!=previous['state']['foreign_maps']):
        raise ValueError('second glyph full owner/image/SEH/stack/maps')
    for k in ('heaps','slot_heap','retained_heaps'):
        if row[k]!=previous[k]:raise ValueError('second glyph complete prior heaps/guards '+k)
    for k in ('first_font_resources_retained',):
        if row[k] is not True:raise ValueError('second glyph first persistent resource authority')
    for k in ('full4010D0_returned','full415F50_returned','second_state_blocks_created','GPU_drawing_or_Present','retained_VM_advanced'):
        if row[k] is not False:raise ValueError('second glyph unresolved cleanup/startup authority')


def verify_retirement(c,owner,image):
    row,previous=c['DIB_retirement'],c['second_GDI']
    active,retired=retire_regions(previous['external_regions'])
    if row['phase']!='retirement' or row['before_cpu']!=previous['cpu'] or row['cpu']!=previous['cpu'] or row['pending']!=previous['pending']:
        raise ValueError('second retirement audit mapping must preserve original CPU')
    if row['api_calls']!=[] or row['original_instructions_executed']!=0 or row['second_glyphs_completed']!=0:
        raise ValueError('second retirement executes no native/platform calls')
    if row['external_regions']!=active or row['retired_regions']!=retired or row['second_heap']!=previous['second_heap']:
        raise ValueError('second retirement exact immutable old DIB and live texture')
    mappings=[[0,4095,7],[BASE,BASE+((len(SOURCE.read_bytes())+4095)&~4095)-1,7],
        [OWNER,OWNER+0xC000-1,7],[STACK,STACK+65536-1,7],[RETURN,RETURN+4095,7]]
    mappings += [[r['pointer'],r['pointer']+12287,7] for r in previous['retained_heaps']+[previous['second_heap']]]
    mappings += [[r['pointer'],r['pointer']+4095,7] for r in previous['state']['foreign_maps']]
    mappings += [[r['base'],r['base']+r['bytes']-1,7] for r in previous['external_regions']]
    if row['mappings_before']!=sorted(mappings):raise ValueError('second retirement full original map ownership')
    old=retired[0]['region'];lo,hi=old['base'],old['base']+old['bytes']-1
    expected=[r for r in sorted(mappings) if r!=[lo,hi,7]]
    if row['mappings_after']!=expected or len(expected)!=len(mappings)-1:
        raise ValueError('second retirement unmaps exactly deleted DIB guarded region')
    verify_memory(row,previous,owner,image)


def verify_second_raster(c,owner,image):
    row,previous=c['second_raster'],c['DIB_retirement'];calls=row['api_calls'];raw=SOURCE.read_bytes()
    if row['phase']!='raster' or row['before_cpu']!=previous['cpu'] or len(calls)!=190:
        raise ValueError('second raster same CPU/exact95 GDI pairs')
    dc,bits=c['second_GDI']['GDI_locals']['dc'],c['second_GDI']['GDI_locals']['bits'];measures=[]
    for n in range(95):
        r=calls[n*2]['result']
        if r.get('result')!=1 or len(bytes.fromhex(r.get('hex','')))!=8:raise ValueError('second raster complete SIZE')
        measures.append(struct.unpack('<2I',bytes.fromhex(r['hex'])))
    rows,end=layout(measures);initial='cc'*8
    for n,r in enumerate(rows):
        ch=r['character'];size=struct.pack('<2I',r['width'],r['height']).hex()
        expected=[dict(op='second_glyph_measure',name='GetTextExtentPoint32A',slot='0x5920bc',va=hex(dword(raw,0x5920BC-BASE)),return_va='0x401497',sp=TOP-736,
                args=[dc,TOP-528,1,TOP-536],request=dict(pointer=dc,character=ch,before_hex=initial),result=dict(result=1,hex=size),live_host_observed=True),
            dict(op='second_glyph_draw',name='ExtTextOutA',slot='0x5920c0',va=hex(dword(raw,0x5920C0-BASE)),return_va='0x401502',sp=TOP-752,
                args=[dc,r['x'],r['y'],2,0,TOP-528,1,0],request=dict(pointer=dc,character=ch,x=r['x'],y=r['y']),result=dict(result=1),live_host_observed=True)]
        if calls[n*2:n*2+2]!=expected:raise ValueError('second raster exact native character/layout/ABI/actual GDI')
        initial=size
    returns=[dict(va='0x56ce82',return_va=ret,sp=TOP-720,eax=1) for _ in rows for ret in ('0x40149e','0x401509')]
    if row['returns']!=returns:raise ValueError('second raster all190 original stack checks')
    check_visited(row,{0x401491,0x4014B4,0x4014FC,0x401551,0x40159D,0x4015EF,0x401641,0x401655,0x40144D,0x401463,0x56CE82},0x401660)
    cpu=dict(EIP=0x401660,ESP=TOP-716,EBP=TOP-220,EAX=rows[-1]['x'],EBX=0x55667788,ECX=(end[0]&~255)|127,EDX=127,ESI=TOP-716,EDI=TOP-220,EFLAGS=70)
    if row['cpu']!=cpu or row['pending']!=dict(va='0x401660',sp=TOP-716,first_instruction_executed=False) or row['layout']!=rows or row['cursor']!=list(end) or row['character']!=127:
        raise ValueError('second raster exact final native CPU/layout/cursor')
    expected=bytearray(b'\xa5'*12288);expected[4096:4096+SIZE]=glyph_object(unpack(previous['second_heap'])[4096:4096+SIZE],measures)
    if row['second_heap']['pointer']!=SECOND-4096:raise ValueError('second raster object address')
    verify_buffer({k:v for k,v in row['second_heap'].items() if k!='pointer'},expected)
    snapshots=[];ink=None
    if len(row['inspections'])!=2:raise ValueError('second raster two inspections')
    for observed,stage,count in zip(row['inspections'],('before','after'),(0,95)):
        data=bytes.fromhex(observed['result']['hex'])
        inspection=observed['result']['ink_inspection']
        rectangles=ink_rectangles(rows,inspection)
        if ink is None:ink=rectangles
        elif rectangles!=ink:raise ValueError('second raster ABC inspection changed across original loop')
        if len(data)!=262144 or observed!=dict(op='second_glyph_pixels',request=dict(pointer=bits,stage=stage),
                result=dict(result=1,native_requested=False,method='GdiFlush/owned DIB snapshot',completed_glyphs=count,hex=data.hex(),ink_inspection=inspection)):
            raise ValueError('second raster explicit actual snapshot/flush authority')
        snapshots.append(data)
    before,after=snapshots;affected=bytearray(65536)
    for r in ink:
        for y in range(r['top'],r['bottom']):affected[y*256+r['left']:y*256+r['right']]=bytes([1])*(r['right']-r['left'])
    if before==after or not any(after):raise ValueError('second raster real visible glyph output')
    for n,active in enumerate(affected):
        if not active and before[n*4:n*4+4]!=after[n*4:n*4+4]:raise ValueError('second raster changed outside source rectangles')
    verify_memory(row,previous,owner,image)
    if row['external_regions']!=previous['external_regions'] or row['retired_regions']!=previous['retired_regions']:
        raise ValueError('second raster preserves retired old DIB/first texture')
    if row['second_glyphs_completed']!=95 or row['UV_stores_completed']!=380 or row['native_second_DIB_pixels_read'] is not False or row['second_texture_upload_executed'] is not False:
        raise ValueError('second raster original counts/upload boundary')
    return after


def check_visited(row,required,stop):
    raw=SOURCE.read_bytes();valid={i.address for a,b in RANGES.items() for i in Cs(CS_ARCH_X86,CS_MODE_32).disasm(raw[a-BASE:b-BASE],a)}
    visited=set(row['visited'])
    if row['visited']!=sorted(visited) or not required<=visited or not visited<=valid or stop in visited:
        raise ValueError('second glyph original native bodies/unexecuted stop')


def verify_second_upload(c,owner,image,objects,dib):
    row,previous=c['second_upload'],c['second_raster'];texture=objects['second_atlas_texture'];pointer=texture['pointer'];calls=row['api_calls']
    if row['phase']!='upload' or row['before_cpu']!=previous['cpu'] or len(calls)!=2:raise ValueError('second upload same CPU/exact lock pair')
    locked=calls[0]['result'];pitch,bits=locked['pitch'],locked['bits'];before=bytes.fromhex(locked['before_hex'])
    if not 512<=pitch<=1024 or not 0<bits<0xFFFFFFFF or bits+pitch*256>0x100000000:raise ValueError('second bounded actual locked buffer')
    expected=pixels(dib,before,pitch)
    first=c['pixel_upload']['api_calls'][1]['result']['inspection'];retained=calls[1]['result']['retained_first_texture_inspection'];read=calls[1]['result']['inspection']
    if not 0<read['bits']<0xFFFFFFFF or not 0<retained['bits']<0xFFFFFFFF:raise ValueError('second actual readback pointers')
    first_inspection=dict(native_requested=False,method='LockRect(first texture readonly)/UnlockRect',pointer=objects['atlas_texture']['pointer'],flags=16,
        lock_hr=0,unlock_hr=0,pitch=first['pitch'],bits=retained['bits'],hex=first['hex'])
    expected_calls=[dict(op='second_atlas_lock',va=hex(texture['methods']['64']),return_va='0x401681',sp=TOP-740,
            args=[pointer,0,TOP-548,0,0],request=dict(pointer=pointer,level=0,rect=0,flags=0),result=dict(hr=0,locked_hex=struct.pack('<2I',pitch,bits).hex(),pitch=pitch,bits=bits,before_hex=before.hex()),live_host_observed=True),
        dict(op='second_atlas_unlock',va=hex(texture['methods']['68']),return_va='0x4017af',sp=TOP-728,args=[pointer,0],
            request=dict(pointer=pointer,level=0,bytes_hex=expected.hex()),result=dict(hr=0,inspection=dict(native_requested=False,method='LockRect(readonly)/UnlockRect',flags=16,
                lock_hr=0,unlock_hr=0,pitch=pitch,bits=read['bits'],hex=expected.hex()),retained_first_texture_inspection=first_inspection),live_host_observed=True)]
    if calls!=expected_calls:raise ValueError('second upload exact original ABI/full pixels/readback/actual first texture retention')
    if row['returns']!=[dict(va='0x56ce82',return_va='0x401688',sp=TOP-720,eax=0),dict(va='0x56ce82',return_va='0x4017b6',sp=TOP-720,eax=0)]:raise ValueError('second upload original stack checks')
    cpu=dict(EIP=0x4017B6,ESP=TOP-716,EBP=TOP-220,EAX=0,EBX=0x55667788,ECX=pointer,EDX=pointer,ESI=TOP-716,EDI=TOP-220,EFLAGS=70)
    if row['cpu']!=cpu or row['pending']!=dict(va='0x4017b6',sp=TOP-716,first_instruction_executed=False):raise ValueError('second upload exact cleanup boundary CPU')
    if row['locals']!=dict(x=256,y=256,pitch=pitch,bits=bits,row=bits+pitch*256,cursor=bits+pitch*255+512,alpha=dib[-4]>>4):raise ValueError('second upload exact pixel loop locals')
    check_visited(row,{0x401660,0x40167E,0x4016BB,0x4016F4,0x401713,0x40171C,0x401743,0x40174F,0x401769,0x401788,0x4017AC,0x56CE82},0x4017B6)
    if row['native_pixel_reads']!=65536 or row['native_pixel_writes']!=65536:raise ValueError('second complete65536 source reads/writes')
    read_hash,write_hash=hashlib.sha256(),hashlib.sha256();dib_bits=c['second_GDI']['GDI_locals']['bits']
    for n in range(65536):
        offset=(n//256)*pitch+(n%256)*2;value=struct.unpack_from('<H',expected,offset)[0]
        read_hash.update(struct.pack('<II',dib_bits+n*4,4));write_hash.update(struct.pack('<IIH',bits+offset,2,value))
    if row['read_sequence_sha256']!=read_hash.hexdigest() or row['write_sequence_sha256']!=write_hash.hexdigest():raise ValueError('second full native access order/value digest')
    verify_memory(row,previous,owner,image)
    if row['second_heap']!=previous['second_heap'] or row['retired_regions']!=previous['retired_regions']:raise ValueError('second upload retains full UV object/retired snapshot')
    regions=row['external_regions']
    if len(regions)!=3 or regions[0]!=previous['external_regions'][0]:raise ValueError('second upload preserves first live texture shadow')
    occupied=[(r['base'],r['base']+r['bytes']) for r in previous['external_regions']]
    occupied += [(BASE,BASE+((len(SOURCE.read_bytes())+4095)&~4095)),(OWNER,OWNER+0xC000),(STACK,STACK+65536),(RETURN,RETURN+4096),(0,4096)]
    occupied += [(r['pointer'],r['pointer']+12288) for r in previous['retained_heaps']+[previous['second_heap']]]
    occupied += [(r['pointer'],r['pointer']+4096) for r in previous['state']['foreign_maps']]
    for observed,(name,p,data) in zip(regions[1:],(('second_DIB',dib_bits,dib),('second_texture',bits,expected))):
        base=(p&~4095)-4096;end=((p+len(data)+4095)&~4095)+4096
        if {k:v for k,v in observed.items() if k!='buffer'}!=dict(name=name,pointer=p,base=base,bytes=end-base,data_bytes=len(data)) or any(base<b and a<end for a,b in occupied):
            raise ValueError('second actual new pixel shadows bounded/nonoverlapping')
        occupied.append((base,end));full=bytearray(b'\xa5'*(end-base));full[p-base:p-base+len(data)]=data;verify_buffer(observed['buffer'],full)
    if row['second_glyphs_completed']!=95:raise ValueError('second upload requires all glyphs')
    for k in ('original_lock_executed','original_conversion_executed','original_unlock_executed','second_texture_upload_executed','actual_second_readback_verified','actual_first_texture_unchanged_verified'):
        if row[k] is not True:raise ValueError('second native upload/readback authority')


def verify_report(report):
    phase=report['phase']
    if report['schema_version']!=1 or phase not in ('retirement','raster','upload') or report['source_contract']!=source_contract():raise ValueError('second glyph fixed source contract')
    for build,source,helper in ((report['device_build'],DEVICE_SOURCE,DEVICE_HELPER),(report['platform_build'],GDI_SOURCE,GDI_HELPER)):
        if build!=dict(source_sha256=sha(source.read_bytes()),helper_sha256=sha(helper.read_bytes()),compiler_sha256=sha(COMPILER.read_bytes()),machine=0x14C) or machine(helper)!=0x14C:raise ValueError('second glyph honest actual immutable x86 builds')
    for k in ('original_IAT_changed','game_helpers_stubbed','retained_VM_advanced','GPU_drawing_or_Present','full_outer_frame','live_handles_resumable_after_cleanup'):
        if report[k] is not False:raise ValueError('second glyph original authority')
    if report['explicit_empty_cache_experiment'] is not True or report['CRT_adapter_executed'] is not True:raise ValueError('second glyph independent explicit input')
    if [(c['fill'],c['hello']['width'],c['hello']['height']) for c in report['cases']]!=[(0xA5,640,480),(0xCC,1024,768)]:raise ValueError('second glyph exact two cases')
    for c in report['cases']:
        if c['hello']['pointer_bytes']!=4 or c['hello']['window_visible'] is not False or c['platform_hello']['pointer_bytes']!=4:raise ValueError('second glyph hidden owned x86 platform')
        owner,image,objects=verify_prefix(c);objects=verify_atlas(c,owner,image,objects);verify_gdi(c,owner,image)
        dib=verify_raster(c,owner,image);verify_pixels(c,owner,image,objects,dib)
        for p in ('cleanup','vertex','states'):objects=verify_phase(c,p,owner,image,objects)
        for p in ('loop','constructor','atlas'):verify_second(c,p,owner,image,objects)
        owner=bytearray(owner);store(owner,0x1094,SECOND);image=bytearray(image);store(image,COUNTER-BASE,dword(image,COUNTER-BASE)+SIZE)
        for p in ('texture','gdi'):objects=verify_resource(c,p,bytes(owner),bytes(image),objects)
        verify_retirement(c,bytes(owner),bytes(image))
        if phase!='retirement':dib=verify_second_raster(c,bytes(owner),bytes(image))
        if phase=='upload':verify_second_upload(c,bytes(owner),bytes(image),objects,dib)
        dc=dict(second_atlas_texture_release_count=0,font_state_block_delete_results=[0,0],font_texture_unbind_hr=0,font_vertex_buffer_release_count=0,
            atlas_texture_release_count=0,texture_surface_release_count=1,texture_release_count=0,extra_reference_release_counts=[3,2,1],device_release_count=0,factory_release_count=0,window_destroyed=True,all_owned_resources_released=True)
        pc=dict(second_atlas_fonts_released=1,second_atlas_dcs_released=1,second_atlas_bitmaps_released=1,second_atlas_selection_restored=True,second_native_GDI_cleanup_executed=False,
            native_atlas_fonts_released=1,native_atlas_dcs_released=1,native_atlas_bitmaps_released=1,native_bitmap_delete_issued=True,native_cleanup_completed=True,
            atlas_fonts_released=0,atlas_dcs_released=0,atlas_bitmaps_released=0,atlas_selection_restored=True,fonts_released=2,dcs_released=1,cache_bitmaps_released=1,cache_dcs_released=1,cache_selection_restored=True,all_owned_resources_released=True)
        if c['device_cleanup']!=dc or c['platform_cleanup']!=pc:raise ValueError('second glyph actual native/fallback cleanup')
        d=device_calls(c)+c['pixel_upload']['api_calls']+c['font_vertex']['api_calls']+c['font_states']['api_calls']+c['second_atlas']['api_calls']+c['second_texture']['api_calls']
        p=platform_calls(c)+c['font_cleanup']['api_calls']+c['second_GDI']['api_calls']
        if phase!='retirement':p+=c['second_raster']['inspections'][:1]+c['second_raster']['api_calls']+c['second_raster']['inspections'][1:]
        if phase=='upload':d+=c['second_upload']['api_calls']
        verify_trace(c['device_trace'],[(r['op'],r['request'],r['result']) for r in d],dc)
        verify_trace(c['platform_trace'],[(r['op'] if 'op'in r else r['name'],r['request'],r['result']) for r in p],pc)
        if len(c['refused_address_collisions'])>5:raise ValueError('second glyph bounded collisions')
        for r in c['refused_address_collisions']:
            if r['error']!='live interface mapping collides with audit ownership' or r['cleanup']['all_owned_resources_released'] is not True or r['trace'][-1]['reply']['result']!=r['cleanup']:raise ValueError('second glyph refused process cleanup')
    return dict(cases=2,phase=phase,deleted_first_DIB_mapping_retired=True,first_texture_retained=True,
        second_glyphs_per_case=0 if phase=='retirement' else 95,second_UV_stores=0 if phase=='retirement' else 380,
        pixels_per_case=65536 if phase=='upload' else 0,actual_second_upload_verified=phase=='upload',actual_first_texture_readback_unchanged=phase=='upload',
        original_second_cleanup_executed=False,full415F50_returned=False,retained_VM_advanced=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('report');a=p.parse_args()
    print(json.dumps(verify_report(json.loads((ROOT/a.report).read_text(encoding='utf8')))))
