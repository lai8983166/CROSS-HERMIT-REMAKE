"""Independent second atlas/GDI proof, complete retention and honest x86 traces."""
import argparse
import json
import struct
from tools.school_font_second_resource import *
from tools.school_font_second_resource_emulation import OWNER,TOP,COUNTER,dword,store
from tools.school_font_second_verification import verify_second
from tools.school_font_state_verification import verify_phase
from tools.school_font_glyph_upload_verification import (verify_prefix,verify_atlas,verify_gdi,
    verify_raster,verify_pixels,device_calls,platform_calls,verify_trace,unpack,verify_buffer)
from tools.school_font_second_resource_platform import (DEVICE_SOURCE,DEVICE_HELPER,GDI_SOURCE,GDI_HELPER,COMPILER,sha,machine)


def check_interface_maps(state,previous,texture):
    expected={r['pointer']:bytearray(unpack(r)) for r in previous['foreign_maps']}
    def put(at,raw):
        for n,value in enumerate(raw):expected.setdefault((at+n)&~4095,bytearray(4096))[(at+n)&4095]=value
    put(texture['pointer'],struct.pack('<I',texture['vtable']))
    for offset,target in texture['methods'].items():
        put(texture['vtable']+int(offset),struct.pack('<I',target));put(target,b'\xc3')
    if [r['pointer'] for r in state['foreign_maps']]!=sorted(expected):raise ValueError('second atlas exact interface pages')
    for r in state['foreign_maps']:verify_buffer({k:v for k,v in r.items() if k!='pointer'},expected[r['pointer']])


def verify_resource(c,phase,owner,image,objects):
    row=c['second_texture' if phase=='texture' else 'second_GDI']
    previous=c['second_atlas' if phase=='texture' else 'second_texture']
    device=objects['device']['pointer'];raw=SOURCE.read_bytes()
    if row['phase']!=phase or row['before_cpu']!=previous['cpu']:raise ValueError('second resource same pending original CPU')
    calls=row['api_calls']
    if phase=='texture':
        if len(calls)!=1:raise ValueError('second texture exactly one original creation')
        texture=calls[0]['result']['texture']
        if (not 0<texture['pointer']<=0xFFFFFFFF or not 0<texture['vtable']<=0xFFFFFFFF
                or set(texture['methods'])!={'8','56','64','68'} or not all(0<t<=0xFFFFFFFF for t in texture['methods'].values())
                or texture['pointer'] in [o['pointer'] for o in objects.values()]):
            raise ValueError('second texture distinct live owned identity')
        desc=struct.pack('<8I',26,1,0,1,131072,0,256,256).hex()
        tokens=[r['result']['token'] for r in c['font_states']['api_calls'] if r['method']=='end']
        result=dict(hr=0,texture=texture,inspection=dict(native_requested=False,method='GetLevelDesc',level=0,result=dict(hr=0,hex=desc)),
            retention_inspection=dict(native_requested=False,method='GetLevelDesc(first texture)/GetDesc(first vertex buffer)',
                first_texture=dict(pointer=objects['atlas_texture']['pointer'],hr=0,hex=desc),
                first_vertex=dict(pointer=objects['font_vertex']['pointer'],result=dict(hr=0,hex=struct.pack('<6I',100,6,520,0,8400,0).hex()))),
            retained_state_tokens=tokens,retained_state_tokens_are_ownership_metadata=True)
        expected=dict(op='second_atlas_create',va=hex(objects['device']['methods']['80']),return_va='0x40120f',sp=TOP-752,
            args=[device,256,256,1,0,26,1,SECOND+0x5C],request=dict(pointer=device,width=256,height=256,levels=1,usage=0,format=26,pool=1),result=result,live_host_observed=True)
        if calls!=[expected]:raise ValueError('second texture original ABI/full descriptions/retained first resources')
        entries=[dict(va='0x56cec0',return_va='0x401237',sp=TOP-732,receiver=device,args=[TOP-488,0,40])]
        returns=[(0x56CE82,0x401216,720,0),(0x56CF12,0x401237,732,TOP-488)]
        required={0x40120C,0x401232,0x40123A,0x40124A,0x401258,0x40125E,0x401267,0x401271,0x40127E,0x56CF01,0x56CF12}
        stop=dword(raw,0x592094-BASE)
        cpu=dict(EIP=stop,ESP=TOP-724,EBP=TOP-220,EAX=SECOND,EBX=0x55667788,ECX=0xFFFFFF00,EDX=256,ESI=TOP-716,EDI=TOP-220,EFLAGS=135)
        pending=dict(va=hex(stop),sp=TOP-724,first_instruction_executed=False,platform_call_executed=False,return_va='0x401284',args=[0])
        if row['GDI_locals'] is not None:raise ValueError('second GDI not created at texture stop')
        check_interface_maps(row['state'],previous['state'],texture)
        value=texture_object(unpack(previous['second_heap'])[4096:4096+SIZE],texture['pointer'])
        objects=dict(objects,second_atlas_texture=texture)
    else:
        if len(calls)!=10:raise ValueError('second GDI exactly ten original calls')
        dc,bitmap,bits,font,old_bitmap,old_font=(calls[0]['result']['result'],calls[1]['result']['result'],
            calls[1]['result']['bits'],calls[4]['result']['result'],calls[5]['result']['result'],calls[6]['result']['result'])
        if not all(isinstance(v,int) and 0<v<0xFFFFFFFF for v in (dc,bitmap,bits,font,old_bitmap,old_font)):
            raise ValueError('second GDI actual owned resource identities')
        specs=[(724,[0],{},dict(result=dc)),
            (744,[dc,TOP-488,0,TOP-444,0,0],dict(pointer=dc,header_hex=bitmap_header().hex()),dict(result=bitmap,bits=bits)),
            (728,[dc,1],dict(pointer=dc,value=1),dict(result=1)),
            (732,[8,96,72],dict(args=[8,96,72]),dict(result=11)),
            (776,[v&0xFFFFFFFF for v in FONT_ARGS]+[SECOND],dict(args=FONT_ARGS,face_hex=FACE.hex()),
                dict(result=font,inspection=dict(native_requested=False,method='GetObjectA',result=60,hex=font_logfont().hex()))),
            (728,[dc,bitmap],dict(pointer=dc,object=bitmap),dict(result=old_bitmap)),
            (728,[dc,font],dict(pointer=dc,object=font),dict(result=old_font)),
            (728,[dc,0xFFFFFF],dict(pointer=dc,value=0xFFFFFF),dict(result=0)),
            (728,[dc,0],dict(pointer=dc,value=0),dict(result=0xFFFFFF)),
            (728,[dc,0],dict(pointer=dc,value=0),dict(result=0))]
        for actual,(slot,name,ret,count,op),(depth,args,request,result) in zip(calls,IMPORTS,specs):
            if actual!=dict(op='second_'+op,name=name,slot=hex(slot),va=hex(dword(raw,slot-BASE)),return_va=hex(ret),sp=TOP-depth,
                    args=args,request=request,result=result,live_host_observed=True):
                raise ValueError('second GDI exact original ABI/ANSI font/real arithmetic/selection')
        entries=[dict(va='0x56cfcc',return_va='0x4012f8',sp=TOP-724,receiver=dc,args=[])]
        returns=[(0x56CE82,0x40128B,720,dc),(0x56CE82,0x4012BB,720,bitmap),(0x56CE82,0x4012D9,720,1),
            (0x56CFF2,0x4012F8,724,96),(0x56CE82,0x40130D,720,11),(0x56CE82,0x401385,720,font),
            (0x56CE82,0x4013BB,720,old_bitmap),(0x56CE82,0x4013D8,720,old_font),
            (0x56CE82,0x4013F3,720,0),(0x56CE82,0x40140B,720,0xFFFFFF),(0x56CE82,0x401423,720,0)]
        required={0x40128B,0x4012BB,0x4012F3,0x40130D,0x401322,0x401328,0x401378,0x4013AE,0x4013CB,
            0x401416,0x401444,0x40145C,0x401472,0x56CFCC,0x56CFE5,0x56CFF2}
        stop=0x401491
        cpu=dict(EIP=stop,ESP=TOP-732,EBP=TOP-220,EAX=dc,EBX=0x55667788,ECX=TOP-536,EDX=TOP-528,ESI=TOP-716,EDI=TOP-220,EFLAGS=147)
        pending=dict(va=hex(stop),sp=TOP-732,first_instruction_executed=False,platform_call_executed=False,
            method_target=dword(raw,0x5920BC-BASE),args=[dc,TOP-528,1,TOP-536])
        if row['GDI_locals']!=dict(dc=dc,bitmap=bitmap,bits=bits,font=font,height=0xFFFFFFF5,weight=400,
                italic=0,x=0,y=0,text_hex='2000',character='20'):
            raise ValueError('second native GDI locals/height/weight/first character')
        if row['state']['foreign_maps']!=previous['state']['foreign_maps']:raise ValueError('second GDI preserves actual maps/IAT')
        value=unpack(previous['second_heap'])[4096:4096+SIZE]
    if row['entries']!=entries or row['returns']!=[dict(va=hex(a),return_va=hex(b),sp=TOP-d,eax=e) for a,b,d,e in returns]:
        raise ValueError('second resource original native entries/returns/stack arithmetic')
    if row['cpu']!=cpu or row['pending']!=pending:raise ValueError('second resource exact unexecuted boundary CPU/ABI')
    valid={i.address for a,b in RANGES.items() for i in Cs(CS_ARCH_X86,CS_MODE_32).disasm(raw[a-BASE:b-BASE],a)}
    visited=set(row['visited'])
    if row['visited']!=sorted(visited) or not required<=visited or not visited<=valid or stop in visited:
        raise ValueError('second resource original bodies/unexecuted stop')
    if row['bitmap_header']!=dict(pointer=TOP-488,hex=bitmap_header().hex()):raise ValueError('second complete native bitmap header')
    verify_buffer(row['state']['owner'],owner)
    if row['state']['image_sha256']!=hashlib.sha256(image).hexdigest() or row['state']['SEH']!=TOP-108 or row['state']['stack_guards_unchanged'] is not True:
        raise ValueError('second resource complete owner/image/SEH/stack')
    for k in ('heaps','slot_heap','retained_heaps','external_regions'):
        if row[k]!=previous[k]:raise ValueError('second resource complete previous heaps/pixels/guards '+k)
    expected=bytearray(b'\xa5'*12288);expected[4096:4096+SIZE]=value
    if row['second_heap']['pointer']!=SECOND-4096:raise ValueError('second resource guarded object address')
    verify_buffer({k:v for k,v in row['second_heap'].items() if k!='pointer'},expected)
    for k in ('external_regions_are_retained_snapshots','first_additional_font_resources_retained','second_texture_created'):
        if row[k] is not True:raise ValueError('second resource actual retention authority')
    if row['second_GDI_prepared'] is not (phase=='gdi'):raise ValueError('second GDI completion boundary')
    for k in ('second_glyph_measurement_executed','second_DIB_pixels_mapped','second_DIB_pixels_read','second_glyph_upload_executed',
            'second_state_blocks_created','full415F50_returned','GPU_drawing_or_Present','retained_VM_advanced'):
        if row[k] is not False:raise ValueError('second resource pending glyph/upload/return authority')
    return objects


def verify_report(report):
    phase=report['phase']
    if report['schema_version']!=1 or phase not in ('texture','gdi') or report['source_contract']!=source_contract():raise ValueError('second resource fixed source contract')
    for build,source,helper in ((report['device_build'],DEVICE_SOURCE,DEVICE_HELPER),(report['platform_build'],GDI_SOURCE,GDI_HELPER)):
        if build!=dict(source_sha256=sha(source.read_bytes()),helper_sha256=sha(helper.read_bytes()),compiler_sha256=sha(COMPILER.read_bytes()),machine=0x14C) or machine(helper)!=0x14C:
            raise ValueError('second resource honest actual x86 helper provenance')
    for k in ('original_IAT_changed','game_helpers_stubbed','retained_VM_advanced','GPU_drawing_or_Present','full_outer_frame','live_handles_resumable_after_cleanup'):
        if report[k] is not False:raise ValueError('second resource original authority')
    if report['explicit_empty_cache_experiment'] is not True or report['CRT_adapter_executed'] is not True:raise ValueError('second resource explicit independent inputs')
    if [(c['fill'],c['hello']['width'],c['hello']['height']) for c in report['cases']]!=[(0xA5,640,480),(0xCC,1024,768)]:raise ValueError('second resource exact two cases')
    for c in report['cases']:
        if c['hello']['pointer_bytes']!=4 or c['hello']['window_visible'] is not False or c['platform_hello']['pointer_bytes']!=4:raise ValueError('second resource hidden owned x86 platform')
        owner,image,objects=verify_prefix(c);objects=verify_atlas(c,owner,image,objects);verify_gdi(c,owner,image)
        dib=verify_raster(c,owner,image);verify_pixels(c,owner,image,objects,dib)
        for p in ('cleanup','vertex','states'):objects=verify_phase(c,p,owner,image,objects)
        for p in ('loop','constructor','atlas'):verify_second(c,p,owner,image,objects)
        owner=bytearray(owner);store(owner,0x1094,SECOND)
        image=bytearray(image);store(image,COUNTER-BASE,dword(image,COUNTER-BASE)+SIZE)
        objects=verify_resource(c,'texture',bytes(owner),bytes(image),objects)
        if phase=='gdi':objects=verify_resource(c,'gdi',bytes(owner),bytes(image),objects)
        dc=dict(second_atlas_texture_release_count=0,font_state_block_delete_results=[0,0],font_texture_unbind_hr=0,font_vertex_buffer_release_count=0,
            atlas_texture_release_count=0,texture_surface_release_count=1,texture_release_count=0,extra_reference_release_counts=[3,2,1],
            device_release_count=0,factory_release_count=0,window_destroyed=True,all_owned_resources_released=True)
        pc=dict(second_atlas_fonts_released=1 if phase=='gdi' else 0,second_atlas_dcs_released=1 if phase=='gdi' else 0,
            second_atlas_bitmaps_released=1 if phase=='gdi' else 0,second_atlas_selection_restored=True,second_native_GDI_cleanup_executed=False,
            native_atlas_fonts_released=1,native_atlas_dcs_released=1,native_atlas_bitmaps_released=1,native_bitmap_delete_issued=True,native_cleanup_completed=True,
            atlas_fonts_released=0,atlas_dcs_released=0,atlas_bitmaps_released=0,atlas_selection_restored=True,fonts_released=2,dcs_released=1,
            cache_bitmaps_released=1,cache_dcs_released=1,cache_selection_restored=True,all_owned_resources_released=True)
        if c['device_cleanup']!=dc or c['platform_cleanup']!=pc:raise ValueError('second resource actual native/fallback cleanup')
        d=device_calls(c)+c['pixel_upload']['api_calls']+c['font_vertex']['api_calls']+c['font_states']['api_calls']+c['second_atlas']['api_calls']+c['second_texture']['api_calls']
        p=platform_calls(c)+c['font_cleanup']['api_calls']
        if phase=='gdi':p+=c['second_GDI']['api_calls']
        verify_trace(c['device_trace'],[(r['op'],r['request'],r['result']) for r in d],dc)
        verify_trace(c['platform_trace'],[(r['op'] if 'op'in r else r['name'],r['request'],r['result']) for r in p],pc)
        if len(c['refused_address_collisions'])>5:raise ValueError('second resource bounded collisions')
        for r in c['refused_address_collisions']:
            if r['error']!='live interface mapping collides with audit ownership' or r['cleanup']['all_owned_resources_released'] is not True or r['trace'][-1]['reply']['result']!=r['cleanup']:
                raise ValueError('second resource refused collision cleanup')
    return dict(cases=2,phase=phase,second_real_texture_created=True,first_font_resources_retained=True,
        second_GDI_prepared=phase=='gdi',full_second_object_bytes=1656,total_guarded_heap_bytes=61440,
        second_glyphs_measured=0,second_glyph_upload_executed=False,full415F50_returned=False,retained_VM_advanced=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('report');a=p.parse_args()
    print(json.dumps(verify_report(json.loads((ROOT/a.report).read_text(encoding='utf8')))))
