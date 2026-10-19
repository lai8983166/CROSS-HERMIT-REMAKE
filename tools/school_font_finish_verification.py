"""Independent full second-font cleanup/state/SEH/caller return proof."""
import argparse
import hashlib
import json
import struct
from tools.school_font_finish import *
from tools.school_font_finish_emulation import OWNER,TOP,COUNTER,dword,store
from tools.school_font_finish_platform import DEVICE_SOURCE,DEVICE_HELPER,GDI_SOURCE,GDI_HELPER,COMPILER,sha,machine
import tools.school_font_second_glyph_verification as parent
from tools.school_font_second_resource_verification import check_interface_maps
from tools.school_device_init_verification import unpack
from tools.school_renderer_init_verification import verify_buffer


def verify_finish(c,phase,owner,image,objects):
    row=c['finish_'+phase];previous=c['second_upload'] if phase=='cleanup' else c['finish_'+{'vertex':'cleanup','states':'vertex','return':'states'}[phase]]
    if row['phase']!=phase or row['before_cpu']!=previous['cpu']:raise ValueError('font finish same actual CPU at each boundary')
    calls=row['api_calls'];device=objects['device']['pointer'];raw=SOURCE.read_bytes();entries=[]
    value=unpack(previous['second_heap'])[4096:4096+SIZE]
    if phase=='cleanup':
        local=c['second_GDI']['GDI_locals'];pointers=[local['bitmap'],local['dc'],local['font']]
        results=[dict(result=1),dict(result=1,inspection=dict(native_requested=False,method='GdiFlush/GetObjectA/GetObjectType(bitmap)',result=0,reported_type=7)),dict(result=1)]
        expected=[dict(op='second_'+op,name=name,slot=hex(slot),va=hex(dword(raw,slot-BASE)),return_va=hex(ret),sp=TOP-724,args=[p],request=dict(pointer=p),result=r,live_host_observed=True)
            for (ret,(slot,name,op)),p,r in zip(IMPORTS.items(),pointers,results)]
        if calls!=expected:raise ValueError('font finish exact second native GDI cleanup/actual lifetime/ABI')
        returns=[(0x56CE82,0x4017CC,720,1),(0x56CE82,0x4017E2,720,1),(0x56CE82,0x4017F8,720,1),(0x56CE82,0x40180A,224,0),(0x40180D,0x4160DF,216,0)]
        cpu=dict(EIP=0x401810,ESP=TOP-212,EBP=TOP-96,EAX=1,EBX=0x55667788,ECX=SECOND,EDX=local['dc'],ESI=TOP-208,EDI=TOP-108,EFLAGS=70)
        required={0x4017BF,0x4017D5,0x4017EB,0x40180D,0x4160FC}
    elif phase=='vertex':
        if len(calls)!=1:raise ValueError('font finish one actual second VB creation')
        vertex=calls[0]['result']['buffer']
        if (not 0<vertex['pointer']<=0xFFFFFFFF or not 0<vertex['vtable']<=0xFFFFFFFF or set(vertex['methods'])!={'8','52'}
                or not all(0<p<=0xFFFFFFFF for p in vertex['methods'].values()) or vertex['pointer'] in [o['pointer'] for o in objects.values()]):
            raise ValueError('font finish distinct actual second VB identity')
        expected=dict(op='second_font_vb',method='vb',va=hex(objects['device']['methods']['92']),return_va='0x401856',sp=TOP-332,
            args=[device,8400,520,0,0,SECOND+0x60],request=dict(pointer=device,args=[8400,520,0,0]),
            result=dict(hr=0,buffer=vertex,inspection=dict(native_requested=False,method='GetDesc(vertex buffer)',result=dict(hr=0,hex=struct.pack('<6I',100,6,520,0,8400,0).hex()))),live_host_observed=True)
        if calls!=[expected]:raise ValueError('font finish original second VB ABI/full description/output')
        entries=[dict(va='0x401810',return_va='0x416101',sp=TOP-212,receiver=SECOND,args=[])]
        returns=[(0x56CE82,0x40185D,308,0)]
        cpu=dict(EIP=0x40186E,ESP=TOP-304,EBP=TOP-216,EAX=0,EBX=0x55667788,ECX=device,EDX=device,ESI=TOP-304,EDI=TOP-216,EFLAGS=70)
        value=project(value,vertex['pointer']);objects=dict(objects,second_font_vertex=vertex)
        check_interface_maps(row['state'],previous['state'],vertex);required={0x401810,0x401853,0x401864}
    elif phase=='states':
        if len(calls)!=60:raise ValueError('font finish exactly second two30-call state blocks')
        addresses=[]
        for block in range(2):addresses += [0x40189B,0x4018C2,*[r[0] for r in RENDER],*[r[0] for r in STAGES],0x401CDA if block==0 else 0x401D04]
        specs={int(r['va'],16):r for r in source_contract()['shared_state_source']['calls']};tokens=[];returns=[]
        first_tokens=[r['result']['token'] for r in c['font_states']['api_calls'] if r['method']=='end']
        for actual,at,command in zip(calls,addresses,plan(objects['second_atlas_texture']['pointer'])):
            spec=specs[at];method=command['method'];ret=int(spec['return_va'],16)
            if method=='end':
                token=actual['result']['token']
                if not 0<token<=0xFFFFFFFF or token in tokens+first_tokens:raise ValueError('font finish four distinct owned tokens')
                args=[device,SECOND+0x670+len(tokens)*4];tokens.append(token);result=dict(hr=0,token=token);depth=316
            else:
                args=[device,*command['args']];result=dict(hr=0);depth=312 if method=='begin' else 324 if method=='stage' else 320
            expected=dict(op='second_font_state',method=method,va=hex(objects['device']['methods'][str(spec['offset'])]),return_va=hex(ret),sp=TOP-depth,
                args=args,request=dict(pointer=device,**command),result=result,live_host_observed=True)
            if actual!=expected:raise ValueError('font finish complete second source state order/arguments/ABI/tokens')
            returns.append((0x56CE82,ret+7,308,0))
        returns += [(0x56CE82,0x401D25,220,0),(0x401D28,0x416101,212,0)]
        value=project(value,objects['second_font_vertex']['pointer'],tokens)
        cpu=dict(EIP=0x416101,ESP=TOP-208,EBP=TOP-96,EAX=0,EBX=0x55667788,ECX=2,EDX=device,ESI=TOP-208,EDI=TOP-108,EFLAGS=70)
        required={0x40186E,0x401880,0x40189B,0x4018C2,0x401CDA,0x401D04,0x401D28,*[r[0] for r in RENDER],*[r[0] for r in STAGES]}
    else:
        if calls:raise ValueError('font finish original loop/unwind has no platform calls')
        entry=c['device']['native']['cpu']
        cpu=dict(EIP=0x4134E3,ESP=entry['ESP']+4,EBP=entry['EBP'],EAX=0,EBX=entry['EBX'],ECX=0,EDX=device,ESI=entry['ESI'],EDI=entry['EDI'],EFLAGS=70)
        returns=[(0x56CE82,0x41612F,100,0),(0x416132,0x4134E3,92,0)];required=set(EXIT_TRACE)
        if row['instruction_trace']!=EXIT_TRACE:raise ValueError('font finish exact index2/success/SEH/ret instruction trace')
    if row['entries']!=entries or row['returns']!=[dict(va=hex(a),return_va=hex(b),sp=TOP-d,eax=e) for a,b,d,e in returns]:
        raise ValueError('font finish original entry/return/stack-check ABI')
    if row['cpu']!=cpu or row['pending']!=dict(va=hex(cpu['EIP']),sp=cpu['ESP'],first_instruction_executed=False):raise ValueError('font finish exact unexecuted original boundary CPU')
    if row['loop_locals']!=dict(index=2 if phase=='return' else 1,status=0):raise ValueError('font finish actual source loop/status locals')
    valid={i.address for a,b in RANGES.items() for i in Cs(CS_ARCH_X86,CS_MODE_32).disasm(raw[a-BASE:b-BASE],a)};visited=set(row['instruction_trace'])
    if row['visited']!=sorted(visited) or not required<=visited or not visited<=valid or cpu['EIP'] in visited or 0x4018F1 in visited:
        raise ValueError('font finish original executed bodies/flag guard/unexecuted boundary')
    verify_buffer(row['state']['owner'],owner)
    if row['state']['image_sha256']!=hashlib.sha256(image).hexdigest() or row['state']['SEH']!=(0 if phase=='return' else TOP-108) or row['state']['stack_guards_unchanged'] is not True:
        raise ValueError('font finish full owner/image/SEH restore/stack retention')
    if phase!='vertex' and row['state']['foreign_maps']!=previous['state']['foreign_maps']:raise ValueError('font finish full owned interface maps retained')
    for k in ('heaps','slot_heap','retained_heaps','external_regions','retired_regions'):
        if row[k]!=previous[k]:raise ValueError('font finish preserved all prior complete ranges '+k)
    expected=bytearray(b'\xa5'*12288);expected[4096:4096+SIZE]=value
    if row['second_heap']['pointer']!=SECOND-4096:raise ValueError('font finish declared second object')
    verify_buffer({k:v for k,v in row['second_heap'].items() if k!='pointer'},expected)
    for k in ('original_second_GDI_cleanup_executed','full_second4010D0_returned','first_font_resources_retained','external_regions_are_snapshots_after_native_GDI_release'):
        if row[k] is not True:raise ValueError('font finish native cleanup/retention authority')
    if row['second_vertex_buffer_created'] is not (phase!='cleanup'):raise ValueError('font finish second VB boundary')
    for k in ('second_state_blocks_created','second_full401810_returned','both_additional_fonts_completed'):
        if row[k] is not (phase in ('states','return')):raise ValueError('font finish second state/return completion scope')
    if row['full415F50_returned'] is not (phase=='return'):raise ValueError('font finish complete initializer return scope')
    for k in ('parent_caller_instruction_executed','manager_bound','native_font_destructor_chain_executed','GPU_drawing_or_Present','retained_VM_advanced'):
        if row[k] is not False:raise ValueError('font finish remaining caller/upstream boundary')
    return objects


def verify_report(report):
    if report['schema_version']!=1 or report['phase']!='full_return' or report['source_contract']!=source_contract():raise ValueError('font finish fixed source contract')
    for build,source,helper in ((report['device_build'],DEVICE_SOURCE,DEVICE_HELPER),(report['platform_build'],GDI_SOURCE,GDI_HELPER)):
        if build!=dict(source_sha256=sha(source.read_bytes()),helper_sha256=sha(helper.read_bytes()),compiler_sha256=sha(COMPILER.read_bytes()),machine=0x14C) or machine(helper)!=0x14C:raise ValueError('font finish honest immutable actual x86 builds')
    for k in ('original_IAT_changed','game_helpers_stubbed','retained_VM_advanced','GPU_drawing_or_Present','full_outer_frame','live_handles_resumable_after_cleanup'):
        if report[k] is not False:raise ValueError('font finish original authority')
    for k in ('one_continuous_trajectory_per_case','explicit_empty_cache_experiment','CRT_adapter_executed'):
        if report[k] is not True:raise ValueError('font finish explicit continuous inputs')
    if [(c['fill'],c['hello']['width'],c['hello']['height']) for c in report['cases']]!=[(0xA5,640,480),(0xCC,1024,768)]:raise ValueError('font finish exact two cases')
    for c in report['cases']:
        if c['hello']['pointer_bytes']!=4 or c['hello']['window_visible'] is not False or c['platform_hello']['pointer_bytes']!=4:raise ValueError('font finish hidden owned x86 platform')
        owner,image,objects=parent.verify_prefix(c);objects=parent.verify_atlas(c,owner,image,objects);parent.verify_gdi(c,owner,image)
        dib=parent.verify_raster(c,owner,image);parent.verify_pixels(c,owner,image,objects,dib)
        for p in ('cleanup','vertex','states'):objects=parent.verify_phase(c,p,owner,image,objects)
        for p in ('loop','constructor','atlas'):parent.verify_second(c,p,owner,image,objects)
        owner=bytearray(owner);store(owner,0x1094,SECOND);image=bytearray(image);store(image,COUNTER-BASE,dword(image,COUNTER-BASE)+SIZE)
        for p in ('texture','gdi'):objects=parent.verify_resource(c,p,bytes(owner),bytes(image),objects)
        parent.verify_retirement(c,bytes(owner),bytes(image));dib=parent.verify_second_raster(c,bytes(owner),bytes(image));parent.verify_second_upload(c,bytes(owner),bytes(image),objects,dib)
        for p in PHASES:objects=verify_finish(c,p,bytes(owner),bytes(image),objects)
        dc=dict(second_font_state_block_delete_results=[0,0],font_state_block_delete_results=[0,0],second_font_texture_unbind_hr=0,second_font_vertex_buffer_release_count=0,
            font_texture_unbind_hr=0,font_vertex_buffer_release_count=0,second_atlas_texture_release_count=0,atlas_texture_release_count=0,
            texture_surface_release_count=1,texture_release_count=0,extra_reference_release_counts=[3,2,1],device_release_count=0,factory_release_count=0,window_destroyed=True,all_owned_resources_released=True)
        pc=dict(second_atlas_fonts_released=0,second_atlas_dcs_released=0,second_atlas_bitmaps_released=0,second_atlas_selection_restored=True,
            second_native_GDI_cleanup_executed=True,second_native_atlas_fonts_released=1,second_native_atlas_dcs_released=1,second_native_atlas_bitmaps_released=1,second_native_bitmap_delete_issued=True,
            native_atlas_fonts_released=1,native_atlas_dcs_released=1,native_atlas_bitmaps_released=1,native_bitmap_delete_issued=True,native_cleanup_completed=True,
            atlas_fonts_released=0,atlas_dcs_released=0,atlas_bitmaps_released=0,atlas_selection_restored=True,fonts_released=2,dcs_released=1,cache_bitmaps_released=1,cache_dcs_released=1,cache_selection_restored=True,all_owned_resources_released=True)
        if c['device_cleanup']!=dc or c['platform_cleanup']!=pc:raise ValueError('font finish balanced actual native/owned-helper cleanup')
        d=parent.device_calls(c)+c['pixel_upload']['api_calls']+c['font_vertex']['api_calls']+c['font_states']['api_calls']+c['second_atlas']['api_calls']+c['second_texture']['api_calls']+c['second_upload']['api_calls']+c['finish_vertex']['api_calls']+c['finish_states']['api_calls']
        p=parent.platform_calls(c)+c['font_cleanup']['api_calls']+c['second_GDI']['api_calls']+c['second_raster']['inspections'][:1]+c['second_raster']['api_calls']+c['second_raster']['inspections'][1:]+c['finish_cleanup']['api_calls']
        parent.verify_trace(c['device_trace'],[(r['op'],r['request'],r['result']) for r in d],dc)
        parent.verify_trace(c['platform_trace'],[(r['op'] if 'op'in r else r['name'],r['request'],r['result']) for r in p],pc)
        if len(c['refused_address_collisions'])>5:raise ValueError('font finish bounded collisions')
        for r in c['refused_address_collisions']:
            if r['error']!='live interface mapping collides with audit ownership' or r['cleanup']['all_owned_resources_released'] is not True or r['trace'][-1]['reply']['result']!=r['cleanup']:raise ValueError('font finish refused process cleanup')
    return dict(cases=2,one_continuous_trajectory_per_case=True,original_second_cleanup_executed=True,vertex_buffers=2,distinct_state_tokens=4,
        full415F50_returned=True,return_va='0x4134e3',caller_instruction_executed=False,manager_bound=False,retained_VM_advanced=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('report');a=p.parse_args()
    print(json.dumps(verify_report(json.loads((ROOT/a.report).read_text(encoding='utf8')))))
