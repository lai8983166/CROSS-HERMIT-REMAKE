"""Full native pixel sequence, owned buffer guards, actual upload and readback proof."""
import hashlib
import json
import struct
from tools.school_font_glyph import *
from tools.school_font_glyph_emulation import OWNER,STACK,TOP,RETURN
from tools.school_font_glyph_verification import retained,verify_prefix,verify_atlas,verify_gdi,verify_raster,device_calls,platform_calls,verify_trace,unpack,verify_buffer
from tools.school_font_glyph_gdi import SOURCE as GDI_SOURCE,HELPER as GDI_HELPER
from tools.school_font_glyph_device import SOURCE as DEVICE_SOURCE,HELPER as DEVICE_HELPER,COMPILER,sha,machine


def verify_pixels(c,owner,image,objects,dib):
    row,previous=c['pixel_upload'],c['glyph_raster'];texture=objects['atlas_texture'];pointer=texture['pointer']
    if row['before_cpu']!=previous['cpu']:raise ValueError('pixel upload same original pending CPU')
    calls=row['api_calls']
    if len(calls)!=2:raise ValueError('pixel exact lock/unlock calls')
    locked=calls[0]['result'];pitch,bits=locked['pitch'],locked['bits'];before=bytes.fromhex(locked['before_hex'])
    if not 512<=pitch<=1024 or not 0<bits<0xFFFFFFFF or bits+pitch*256>0x100000000:raise ValueError('pixel bounded actual locked buffer')
    expected=pixels(dib,before,pitch)
    if calls[0]!=dict(op='atlas_lock',va=hex(texture['methods']['64']),return_va='0x401681',sp=TOP-740,
        args=[pointer,0,TOP-548,0,0],request=dict(pointer=pointer,level=0,rect=0,flags=0),
        result=dict(hr=0,locked_hex=struct.pack('<2I',pitch,bits).hex(),pitch=pitch,bits=bits,before_hex=before.hex()),live_host_observed=True):
        raise ValueError('pixel original LockRect identity/ABI/complete buffer')
    readback=calls[1]['result']['inspection'];read_bits=readback['bits']
    if not 0<read_bits<0xFFFFFFFF:raise ValueError('pixel actual readonly inspection pointer')
    if calls[1]!=dict(op='atlas_unlock',va=hex(texture['methods']['68']),return_va='0x4017af',sp=TOP-728,
        args=[pointer,0],request=dict(pointer=pointer,level=0,bytes_hex=expected.hex()),
        result=dict(hr=0,inspection=dict(native_requested=False,method='LockRect(readonly)/UnlockRect',flags=16,
            lock_hr=0,unlock_hr=0,pitch=pitch,bits=read_bits,hex=expected.hex())),live_host_observed=True):
        raise ValueError('pixel exact original external-write transfer/UnlockRect/readonly full readback')
    if row['returns']!=[dict(va='0x56ce82',return_va='0x401688',sp=TOP-720,eax=0),dict(va='0x56ce82',return_va='0x4017b6',sp=TOP-720,eax=0)]:
        raise ValueError('pixel original lock/unlock stack-check returns')
    cpu=dict(EIP=0x4017B6,ESP=TOP-716,EBP=TOP-220,EAX=0,EBX=0x55667788,ECX=pointer,EDX=pointer,ESI=TOP-716,EDI=TOP-220,EFLAGS=70)
    if row['cpu']!=cpu or row['pending']!=dict(va='0x4017b6',sp=TOP-716,first_instruction_executed=False):raise ValueError('pixel exact original cleanup admission CPU')
    if row['locals']!=dict(x=256,y=256,pitch=pitch,bits=bits,row=bits+pitch*256,cursor=bits+pitch*255+512,alpha=dib[-4]>>4):
        raise ValueError('pixel original loop locals/last alpha/pitch')
    raw=SOURCE.read_bytes();md=Cs(CS_ARCH_X86,CS_MODE_32);valid={i.address for a,b in RANGES.items() for i in md.disasm(raw[a-BASE:b-BASE],a)};visited=set(row['visited'])
    required={0x401660,0x40167E,0x4016BB,0x4016F4,0x401713,0x40171C,0x401743,0x40174F,0x401769,0x401788,0x4017AC,0x56CE82}
    if row['visited']!=sorted(visited) or not required<=visited or not visited<=valid or 0x4017B6 in visited:raise ValueError('pixel original native branches and unexecuted cleanup')
    if row['native_pixel_reads']!=65536 or row['native_pixel_writes']!=65536:raise ValueError('pixel all65536 original accesses required')
    read_hash,write_hash=hashlib.sha256(),hashlib.sha256();dib_bits=c['GDI_preparation']['GDI_locals']['bits']
    for n in range(65536):
        at=bits+(n//256)*pitch+(n%256)*2;value=struct.unpack_from('<H',expected,(n//256)*pitch+(n%256)*2)[0]
        read_hash.update(struct.pack('<II',dib_bits+n*4,4));write_hash.update(struct.pack('<IIH',at,2,value))
    if row['read_sequence_sha256']!=read_hash.hexdigest() or row['write_sequence_sha256']!=write_hash.hexdigest():raise ValueError('pixel complete source read/write order/values')
    retained(row,previous,owner,image)
    if row['slot_heap']!=previous['slot_heap'] or row['state']['foreign_maps']!=previous['state']['foreign_maps']:raise ValueError('pixel full original glyph object/maps retained')
    regions=row['external_regions']
    if len(regions)!=2:raise ValueError('pixel two bounded external shadow regions required')
    occupied=[(BASE,BASE+((len(raw)+4095)&~4095)),(OWNER,OWNER+0xC000),(STACK,STACK+65536),(RETURN,RETURN+4096),(0,4096)]
    occupied += [(r['pointer'],r['pointer']+12288) for r in [*previous['heaps'],previous['slot_heap']]]
    occupied += [(r['pointer'],r['pointer']+4096) for r in previous['state']['foreign_maps']]
    for observed,(name,pointer_value,data) in zip(regions,(('DIB',dib_bits,dib),('texture',bits,expected))):
        base=(pointer_value&~4095)-4096;end=((pointer_value+len(data)+4095)&~4095)+4096
        if {k:v for k,v in observed.items() if k!='buffer'}!=dict(name=name,pointer=pointer_value,base=base,bytes=end-base,data_bytes=len(data)):
            raise ValueError('pixel actual pointer identity/complete guarded region')
        if any(base<b and a<end for a,b in occupied):raise ValueError('pixel shadow overlap refused')
        occupied.append((base,end));full=bytearray(b'\xa5'*(end-base));full[pointer_value-base:pointer_value-base+len(data)]=data
        verify_buffer(observed['buffer'],full)
    for key in ('original_lock_executed','original_conversion_executed','original_unlock_executed','actual_texture_upload_verified','readonly_readback_inspection_only'):
        if row[key] is not True:raise ValueError('pixel original/upload completion authority')
    for key in ('original_cleanup_executed','full4010D0_returned','full415F50_returned','state_blocks_created','retained_VM_advanced'):
        if row[key] is not False:raise ValueError('pixel unresolved full font/startup boundary')


def verify_report(report):
    if report['schema_version']!=1 or report['phase']!='upload' or report['source_contract']!=source_contract():raise ValueError('upload original source contract')
    for key in ('original_IAT_changed','game_helpers_stubbed','retained_VM_advanced','GPU_drawing_or_Present','full_outer_frame','live_handles_resumable_after_cleanup'):
        if report[key] is not False:raise ValueError('upload original authority')
    if report['explicit_empty_cache_experiment'] is not True or report['CRT_adapter_executed'] is not True:raise ValueError('upload declared experiment')
    for build,source,helper in ((report['device_build'],DEVICE_SOURCE,DEVICE_HELPER),(report['platform_build'],GDI_SOURCE,GDI_HELPER)):
        if build!=dict(source_sha256=sha(source.read_bytes()),helper_sha256=sha(helper.read_bytes()),compiler_sha256=sha(COMPILER.read_bytes()),machine=0x14C) or machine(helper)!=0x14C:raise ValueError('upload actual immutable x86 builds')
    if [(c['fill'],c['hello']['width'],c['hello']['height']) for c in report['cases']]!=[(0xA5,640,480),(0xCC,1024,768)]:raise ValueError('upload exact cases')
    for c in report['cases']:
        if c['hello']['pointer_bytes']!=4 or c['hello']['window_visible'] is not False or c['platform_hello']['pointer_bytes']!=4:raise ValueError('upload owned hidden platform')
        owner,image,objects=verify_prefix(c);objects=verify_atlas(c,owner,image,objects);verify_gdi(c,owner,image);dib=verify_raster(c,owner,image);verify_pixels(c,owner,image,objects,dib)
        dc=dict(atlas_texture_release_count=0,texture_surface_release_count=1,texture_release_count=0,extra_reference_release_counts=[3,2,1],device_release_count=0,factory_release_count=0,window_destroyed=True,all_owned_resources_released=True)
        pc=dict(atlas_fonts_released=1,atlas_dcs_released=1,atlas_bitmaps_released=1,atlas_selection_restored=True,fonts_released=2,dcs_released=1,cache_bitmaps_released=1,cache_dcs_released=1,cache_selection_restored=True,all_owned_resources_released=True)
        if c['device_cleanup']!=dc or c['platform_cleanup']!=pc:raise ValueError('upload all owned resources released')
        verify_trace(c['device_trace'],[(r['op'],r['request'],r['result']) for r in device_calls(c)+c['pixel_upload']['api_calls']],dc)
        verify_trace(c['platform_trace'],[(r['op'] if 'op'in r else r['name'],r['request'],r['result']) for r in platform_calls(c)],pc)
        if len(c['refused_address_collisions'])>5:raise ValueError('upload bounded collision retries')
        for r in c['refused_address_collisions']:
            if r['error']!='live interface mapping collides with audit ownership' or r['cleanup']['all_owned_resources_released'] is not True or r['trace'][-1]['reply']['result']!=r['cleanup']:raise ValueError('upload refused collision cleanup')
    return dict(cases=2,phase='upload',glyphs_per_case=95,pixels_per_case=65536,actual_texture_upload_verified=True,retained_VM_advanced=False)


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('report');a=p.parse_args();print(json.dumps(verify_report(json.loads((ROOT/a.report).read_text(encoding='utf-8')))))
