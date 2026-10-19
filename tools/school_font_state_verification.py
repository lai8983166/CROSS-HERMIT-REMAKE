"""Independent original cleanup/VB/two-state-block proof with honest helper provenance."""
import json
import struct
from tools.school_font_state import *
from tools.school_font_state_emulation import OWNER,TOP
from tools.school_font_glyph_upload_verification import verify_prefix,verify_atlas,verify_gdi,verify_raster,verify_pixels,device_calls,platform_calls,verify_trace,unpack,verify_buffer
from tools.school_font_glyph_verification import maps_added,retained
from tools.school_font_state_gdi import SOURCE as GDI_SOURCE,HELPER as GDI_HELPER,COMPILER,sha,machine


def verify_phase(c,phase,owner,image,objects):
    row=c[{'cleanup':'font_cleanup','vertex':'font_vertex','states':'font_states'}[phase]]
    previous=c[{'cleanup':'pixel_upload','vertex':'font_cleanup','states':'font_vertex'}[phase]]
    device=objects['device']['pointer'];raw=SOURCE.read_bytes();contract=source_contract()
    if row['phase']!=phase or row['before_cpu']!=previous['cpu']:raise ValueError('font state original pending CPU continuation')
    entries=[] if phase!='vertex' else [dict(va='0x401810',return_va='0x416101',sp=TOP-212,receiver=SLOT,args=[])]
    if row['entries']!=entries:raise ValueError('font state original caller/receiver/entry')
    value=unpack(previous['slot_heap'])[4096:4096+SIZE];calls=row['api_calls']
    if phase=='cleanup':
        locals=c['GDI_preparation']['GDI_locals'];pointers=[locals['bitmap'],locals['dc'],locals['font']]
        results=[dict(result=1),dict(result=1,inspection=dict(native_requested=False,method='GdiFlush/GetObjectA/GetObjectType(bitmap)',result=0,reported_type=7)),dict(result=1)]
        expected=[dict(op=op,name=name,slot=hex(slot),va=hex(dword(raw,slot-BASE)),return_va=hex(ret),sp=TOP-724,args=[pointer],request=dict(pointer=pointer),result=result,live_host_observed=True)
            for (ret,(slot,name,op)),pointer,result in zip(IMPORTS.items(),pointers,results)]
        if calls!=expected:raise ValueError('font original three GDI deletion calls/actual lifetime/ABI')
        returns=[(0x56CE82,0x4017CC,720,1),(0x56CE82,0x4017E2,720,1),(0x56CE82,0x4017F8,720,1),
                 (0x56CE82,0x40180A,224,0),(0x40180D,0x4160DF,216,0)]
        cpu=dict(EIP=0x401810,ESP=TOP-212,EBP=TOP-96,EAX=0,EBX=0x55667788,ECX=SLOT,EDX=locals['dc'],ESI=TOP-208,EDI=TOP-108,EFLAGS=70)
        maps_added(row['state'],previous['state'],(0x5920C4,0x592060))
    elif phase=='vertex':
        if len(calls)!=1:raise ValueError('font one real vertex creation')
        vertex=calls[0]['result']['buffer']
        if not 0<vertex['pointer']<0xFFFFFFFF or not 0<vertex['vtable']<0xFFFFFFFF or set(vertex['methods'])!={'8','52'} or not all(0<p<0xFFFFFFFF for p in vertex['methods'].values()):raise ValueError('font actual vertex buffer identity')
        expected=dict(op='font_vb',method='vb',va=hex(objects['device']['methods']['92']),return_va='0x401856',sp=TOP-332,
            args=[device,8400,520,0,0,SLOT+0x60],request=dict(pointer=device,args=[8400,520,0,0]),
            result=dict(hr=0,buffer=vertex,inspection=dict(native_requested=False,method='GetDesc(vertex buffer)',result=dict(hr=0,hex=struct.pack('<6I',100,6,520,0,8400,0).hex()))),live_host_observed=True)
        if calls[0]!=expected:raise ValueError('font original vertex ABI/complete resource description')
        objects=dict(objects,font_vertex=vertex);value=project(value,vertex['pointer']);returns=[(0x56CE82,0x40185D,308,0)]
        cpu=dict(EIP=0x40186E,ESP=TOP-304,EBP=TOP-216,EAX=0,EBX=0x55667788,ECX=device,EDX=device,ESI=TOP-304,EDI=TOP-216,EFLAGS=70)
        expected_maps={r['pointer']:bytearray(unpack(r)) for r in previous['state']['foreign_maps']}
        def put(at,data):
            for n,v in enumerate(data):expected_maps.setdefault((at+n)&~4095,bytearray(4096))[(at+n)&4095]=v
        put(vertex['pointer'],struct.pack('<I',vertex['vtable']))
        for slot,target in vertex['methods'].items():put(vertex['vtable']+int(slot),struct.pack('<I',target));put(target,b'\xc3')
        if [r['pointer'] for r in row['state']['foreign_maps']]!=sorted(expected_maps):raise ValueError('font exact new vertex interface maps')
        for r in row['state']['foreign_maps']:verify_buffer({k:v for k,v in r.items() if k!='pointer'},expected_maps[r['pointer']])
    else:
        if len(calls)!=60:raise ValueError('font exactly two complete30-call blocks')
        addresses=[]
        for block in range(2):addresses += [0x40189B,0x4018C2,*[r[0] for r in RENDER],*[r[0] for r in STAGES],0x401CDA if block==0 else 0x401D04]
        specs={int(r['va'],16):r for r in contract['calls']};tokens=[];returns=[]
        for actual,at,command in zip(calls,addresses,plan(objects['atlas_texture']['pointer'])):
            spec=specs[at];method=command['method'];ret=int(spec['return_va'],16)
            if method=='end':
                token=actual['result']['token']
                if not 0<token<=0xFFFFFFFF or token in tokens:raise ValueError('font two distinct actual state tokens')
                out=SLOT+0x670+len(tokens)*4;tokens.append(token);args=[device,out];result=dict(hr=0,token=token);depth=316
            else:
                args=[device,*command['args']];result=dict(hr=0);depth=312 if method=='begin' else 324 if method=='stage' else 320
            expected=dict(op='font_state',method=method,va=hex(objects['device']['methods'][str(spec['offset'])]),return_va=hex(ret),sp=TOP-depth,
                args=args,request=dict(pointer=device,**command),result=result,live_host_observed=True)
            if actual!=expected:raise ValueError('font exact original60 state methods/arguments/order/tokens/ABI')
            returns.append((0x56CE82,ret+7,308,0))
        returns += [(0x56CE82,0x401D25,220,0),(0x401D28,0x416101,212,0)]
        value=project(value,objects['font_vertex']['pointer'],tokens)
        cpu=dict(EIP=0x416101,ESP=TOP-208,EBP=TOP-96,EAX=0,EBX=0x55667788,ECX=2,EDX=device,ESI=TOP-208,EDI=TOP-108,EFLAGS=70)
        if row['state']['foreign_maps']!=previous['state']['foreign_maps']:raise ValueError('font state retained full live maps')
    if row['returns']!=[dict(va=hex(a),return_va=hex(b),sp=TOP-d,eax=e) for a,b,d,e in returns]:raise ValueError('font original natural returns/stack checks')
    if row['cpu']!=cpu or row['pending']!=dict(va=hex(cpu['EIP']),sp=cpu['ESP'],first_instruction_executed=False):raise ValueError('font exact native boundary CPU')
    md=Cs(CS_ARCH_X86,CS_MODE_32);valid={i.address for a,b in RANGES.items() for i in md.disasm(raw[a-BASE:b-BASE],a)};visited=set(row['visited'])
    required={'cleanup':{0x4017BF,0x4017D5,0x4017EB,0x40180D,0x4160FC},'vertex':{0x401810,0x401853,0x401864},
        'states':{0x40186E,0x401880,0x40189B,0x4018C2,0x401CDA,0x401D04,0x401D28,*[r[0] for r in RENDER],*[r[0] for r in STAGES]}}[phase]
    if row['visited']!=sorted(visited) or not required<=visited or not visited<=valid or cpu['EIP'] in visited or 0x4018F1 in visited:raise ValueError('font original bodies/flag branch/unexecuted continuation')
    retained(row,previous,owner,image)
    expected=bytearray(b'\xa5'*12288);expected[4096:4096+SIZE]=value
    if row['slot_heap']['pointer']!=SLOT-4096:raise ValueError('font declared slot address')
    verify_buffer({k:v for k,v in row['slot_heap'].items() if k!='pointer'},expected)
    if row['external_regions']!=previous['external_regions'] or row['external_regions_are_retained_snapshots'] is not True:raise ValueError('font retained complete pixel snapshots/guards')
    for k in ('original_GDI_cleanup_executed','full4010D0_returned'):
        if row[k] is not True:raise ValueError('font cleanup/atlas return authority')
    for k in ('vertex_buffer_created',):
        if row[k] is not (phase!='cleanup'):raise ValueError('font vertex completion scope')
    for k in ('state_blocks_created','full401810_returned','first_additional_font_completed'):
        if row[k] is not (phase=='states'):raise ValueError('font first-slot device-state completion scope')
    for k in ('second_additional_font_constructed','full415F50_returned','GPU_drawing_or_Present','retained_VM_advanced'):
        if row[k] is not False:raise ValueError('font unresolved next-slot/upstream boundary')
    return objects


def verify_report(report):
    phase=report['phase']
    if report['schema_version']!=1 or phase not in ('cleanup','vertex','states') or report['source_contract']!=source_contract():raise ValueError('font state fixed original source contract')
    if phase=='cleanup':
        from tools.school_font_glyph_device import SOURCE as DEVICE_SOURCE,HELPER as DEVICE_HELPER
    else:
        from tools.school_font_state_device import SOURCE as DEVICE_SOURCE,HELPER as DEVICE_HELPER
    for build,source,helper in ((report['device_build'],DEVICE_SOURCE,DEVICE_HELPER),(report['platform_build'],GDI_SOURCE,GDI_HELPER)):
        if build!=dict(source_sha256=sha(source.read_bytes()),helper_sha256=sha(helper.read_bytes()),compiler_sha256=sha(COMPILER.read_bytes()),machine=0x14C) or machine(helper)!=0x14C:raise ValueError('font state actual immutable x86 build')
    for k in ('original_IAT_changed','game_helpers_stubbed','retained_VM_advanced','GPU_drawing_or_Present','full_outer_frame','live_handles_resumable_after_cleanup'):
        if report[k] is not False:raise ValueError('font state original authority')
    if report['explicit_empty_cache_experiment'] is not True or report['CRT_adapter_executed'] is not True:raise ValueError('font state explicit inputs')
    if [(c['fill'],c['hello']['width'],c['hello']['height']) for c in report['cases']]!=[(0xA5,640,480),(0xCC,1024,768)]:raise ValueError('font state exact cases')
    for c in report['cases']:
        if c['hello']['pointer_bytes']!=4 or c['hello']['window_visible'] is not False or c['platform_hello']['pointer_bytes']!=4:raise ValueError('font state hidden owned x86 platform')
        owner,image,objects=verify_prefix(c);objects=verify_atlas(c,owner,image,objects);verify_gdi(c,owner,image);dib=verify_raster(c,owner,image);verify_pixels(c,owner,image,objects,dib)
        objects=verify_phase(c,'cleanup',owner,image,objects)
        if phase!='cleanup':objects=verify_phase(c,'vertex',owner,image,objects)
        if phase=='states':objects=verify_phase(c,'states',owner,image,objects)
        dc=dict(atlas_texture_release_count=0,texture_surface_release_count=1,texture_release_count=0,extra_reference_release_counts=[3,2,1],device_release_count=0,factory_release_count=0,window_destroyed=True,all_owned_resources_released=True)
        if phase!='cleanup':dc.update(font_texture_unbind_hr=0,font_vertex_buffer_release_count=0)
        if phase=='states':dc['font_state_block_delete_results']=[0,0]
        pc=dict(native_atlas_fonts_released=1,native_atlas_dcs_released=1,native_atlas_bitmaps_released=1,native_bitmap_delete_issued=True,native_cleanup_completed=True,
            atlas_fonts_released=0,atlas_dcs_released=0,atlas_bitmaps_released=0,atlas_selection_restored=True,fonts_released=2,dcs_released=1,cache_bitmaps_released=1,cache_dcs_released=1,cache_selection_restored=True,all_owned_resources_released=True)
        if c['device_cleanup']!=dc or c['platform_cleanup']!=pc:raise ValueError('font state complete native/fallback resource cleanup')
        d=device_calls(c)+c['pixel_upload']['api_calls']
        if phase!='cleanup':d+=c['font_vertex']['api_calls']
        if phase=='states':d+=c['font_states']['api_calls']
        p=platform_calls(c)+c['font_cleanup']['api_calls']
        verify_trace(c['device_trace'],[(r['op'],r['request'],r['result']) for r in d],dc)
        verify_trace(c['platform_trace'],[(r['op'] if 'op'in r else r['name'],r['request'],r['result']) for r in p],pc)
        if len(c['refused_address_collisions'])>5:raise ValueError('font state bounded collisions')
        for r in c['refused_address_collisions']:
            if r['error']!='live interface mapping collides with audit ownership' or r['cleanup']['all_owned_resources_released'] is not True or r['trace'][-1]['reply']['result']!=r['cleanup']:raise ValueError('font state refused process cleanup')
    return dict(cases=2,phase=phase,original_GDI_cleanup_executed=True,full4010D0_returned=True,vertex_buffer_created=phase!='cleanup',
        state_blocks=2 if phase=='states' else 0,first_additional_font_completed=phase=='states',retained_VM_advanced=False)


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('report');a=p.parse_args();print(json.dumps(verify_report(json.loads((ROOT/a.report).read_text(encoding='utf-8')))))
