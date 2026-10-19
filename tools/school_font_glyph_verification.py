"""Independent source/ABI/full-object proof for original glyphs and pixel upload."""
import json
import struct
from tools.school_font_glyph import *
from tools.school_font_glyph_emulation import OWNER,TOP
from tools.school_font_atlas_verification import verify_prefix,verify_atlas,verify_gdi
from tools.school_font_startup_verification import verify_trace
from tools.school_font_glyph_gdi import SOURCE as GDI_SOURCE,HELPER as GDI_HELPER,COMPILER,sha,machine
from tools.school_font_atlas_device import SOURCE as DEVICE_SOURCE,HELPER as DEVICE_HELPER
from tools.school_device_init_verification import unpack
from tools.school_renderer_init_verification import verify_buffer


def maps_added(state,previous,slots):
    expected={r['pointer']:bytearray(unpack(r)) for r in previous['foreign_maps']};raw=SOURCE.read_bytes()
    for slot in slots:
        at=dword(raw,slot-BASE);expected.setdefault(at&~4095,bytearray(4096))[at&4095]=0xC3
    if [r['pointer'] for r in state['foreign_maps']]!=sorted(expected):raise ValueError('glyph exact original live/import maps')
    for r in state['foreign_maps']:verify_buffer({k:v for k,v in r.items() if k!='pointer'},expected[r['pointer']])


def retained(row,previous,owner,image):
    verify_buffer(row['state']['owner'],owner)
    if row['state']['image_sha256']!=sha(image) or row['state']['SEH']!=TOP-108 or row['state']['stack_guards_unchanged'] is not True:
        raise ValueError('glyph full source/owner/SEH/stack retention')
    if row['heaps']!=previous['heaps']:raise ValueError('glyph unchanged complete parent heaps')


def verify_raster(case,owner,image):
    row,previous=case['glyph_raster'],case['GDI_preparation'];raw=SOURCE.read_bytes()
    if row['before_cpu']!=previous['cpu']:raise ValueError('glyph same pending original CPU')
    calls=row['api_calls']
    if len(calls)!=190:raise ValueError('glyph exact95 measurement/drawing pairs')
    dc,bits=previous['GDI_locals']['dc'],previous['GDI_locals']['bits']
    measures=[]
    for n in range(95):
        result=calls[n*2]['result']
        if result.get('result')!=1 or len(bytes.fromhex(result.get('hex','')))!=8:raise ValueError('glyph complete actual SIZE')
        measures.append(struct.unpack('<2I',bytes.fromhex(result['hex'])))
    rows,end=layout(measures);initial='cc'*8
    for n,r in enumerate(rows):
        ch=r['character'];measure,draw=calls[n*2:n*2+2];size_hex=struct.pack('<2I',r['width'],r['height']).hex()
        expected_measure=dict(op='glyph_measure',name='GetTextExtentPoint32A',slot='0x5920bc',va=hex(dword(raw,0x5920BC-BASE)),return_va='0x401497',sp=TOP-736,
            args=[dc,TOP-528,1,TOP-536],request=dict(pointer=dc,character=ch,before_hex=initial),result=dict(result=1,hex=size_hex),live_host_observed=True)
        expected_draw=dict(op='glyph_draw',name='ExtTextOutA',slot='0x5920c0',va=hex(dword(raw,0x5920C0-BASE)),return_va='0x401502',sp=TOP-752,
            args=[dc,r['x'],r['y'],2,0,TOP-528,1,0],request=dict(pointer=dc,character=ch,x=r['x'],y=r['y']),result=dict(result=1),live_host_observed=True)
        if measure!=expected_measure or draw!=expected_draw:raise ValueError('glyph source character/wrap/complete ABI/actual GDI calls')
        initial=size_hex
    expected_returns=[dict(va='0x56ce82',return_va=ret,sp=TOP-720,eax=1) for n in range(95) for ret in ('0x40149e','0x401509')]
    if row['returns']!=expected_returns:raise ValueError('glyph all190 original stack-check returns')
    md=Cs(CS_ARCH_X86,CS_MODE_32);valid={i.address for a,b in RANGES.items() for i in md.disasm(raw[a-BASE:b-BASE],a)};visited=set(row['visited'])
    required={0x401491,0x4014B4,0x4014FC,0x401551,0x40159D,0x4015EF,0x401641,0x401655,0x40144D,0x401463,0x56CE82}
    if row['visited']!=sorted(visited) or not required<=visited or not visited<=valid or 0x401660 in visited:raise ValueError('glyph original loop body/unexecuted boundary')
    if row['layout']!=rows or row['cursor']!=list(end) or row['character']!=127:raise ValueError('glyph all source coordinates and cursor')
    cpu=dict(EIP=0x401660,ESP=TOP-716,EBP=TOP-220,EAX=rows[-1]['x'],EBX=0x55667788,ECX=(end[0]&~255)|127,EDX=127,ESI=TOP-716,EDI=TOP-220,EFLAGS=70)
    if row['cpu']!=cpu or row['pending']!=dict(va='0x401660',sp=TOP-716,first_instruction_executed=False):raise ValueError('glyph exact final original CPU')
    retained(row,previous,owner,image);maps_added(row['state'],previous['state'],(0x5920BC,0x5920C0))
    expected=bytearray(b'\xa5'*12288);expected[4096:4096+SIZE]=glyph_object(unpack(previous['slot_heap'])[4096:4096+SIZE],measures)
    if row['slot_heap']['pointer']!=SLOT-4096:raise ValueError('glyph declared slot/guard')
    verify_buffer({k:v for k,v in row['slot_heap'].items() if k!='pointer'},expected)
    if len(row['inspections'])!=2:raise ValueError('glyph two explicit DIB snapshots')
    snapshots=[]
    for observed,stage,count in zip(row['inspections'],('before','after'),(0,95)):
        data=bytes.fromhex(observed['result']['hex'])
        if len(data)!=262144 or observed!=dict(op='glyph_pixels',request=dict(pointer=bits,stage=stage),result=dict(result=1,native_requested=False,method='GdiFlush/owned DIB snapshot',completed_glyphs=count,hex=data.hex())):
            raise ValueError('glyph exact owned inspection-only flush/DIB snapshot')
        snapshots.append(data)
    before,after=snapshots;affected=bytearray(65536)
    for r in rows:
        if r['x']+r['width']>256 or r['y']+r['height']>256:raise ValueError('glyph accepted actual raster bounds')
        for y in range(r['y'],r['y']+r['height']):affected[y*256+r['x']:y*256+r['x']+r['width']]=bytes([1])*r['width']
    if before==after or not any(after):raise ValueError('glyph actual visible raster required')
    for n,active in enumerate(affected):
        if not active and before[n*4:n*4+4]!=after[n*4:n*4+4]:raise ValueError('glyph raster changed outside source glyph rectangles')
    if row['glyphs_completed']!=95 or row['UV_stores_completed']!=380 or row['DIB_snapshot_read'] is not True:raise ValueError('glyph native completion counts')
    for key in ('native_DIB_pixels_read','texture_lock_executed','texture_upload_executed','original_cleanup_executed','full415F50_returned','state_blocks_created','retained_VM_advanced'):
        if row[key] is not False:raise ValueError('glyph exact unresolved upload/startup boundary')
    return after


def device_calls(c):
    return (c['device']['native']['live_results']+c['factory']['cache_calls']+c['requirements']['api_calls']+c['texture']['api_calls']+
        c['sprite']['device_calls']+c['font_return']['device_calls']+c['atlas_admission']['api_calls']+c['atlas_texture']['api_calls'])


def platform_calls(c):
    return (c['constructor']['platform_calls']+c['font']['platform_calls']+c['font_return']['gdi_calls']+c['GDI_preparation']['api_calls']+
        c['glyph_raster']['inspections'][:1]+c['glyph_raster']['api_calls']+c['glyph_raster']['inspections'][1:])


def verify_report(report):
    if report['schema_version']!=1 or report['phase']!='raster' or report['source_contract']!=source_contract():raise ValueError('glyph exact original contract')
    for key in ('original_IAT_changed','game_helpers_stubbed','retained_VM_advanced','GPU_drawing_or_Present','full_outer_frame','live_handles_resumable_after_cleanup'):
        if report[key] is not False:raise ValueError('glyph original authority')
    if report['explicit_empty_cache_experiment'] is not True or report['CRT_adapter_executed'] is not True:raise ValueError('glyph declared experiment inputs')
    for build,source,helper in ((report['device_build'],DEVICE_SOURCE,DEVICE_HELPER),(report['platform_build'],GDI_SOURCE,GDI_HELPER)):
        if build!=dict(source_sha256=sha(source.read_bytes()),helper_sha256=sha(helper.read_bytes()),compiler_sha256=sha(COMPILER.read_bytes()),machine=0x14C) or machine(helper)!=0x14C:raise ValueError('glyph actual immutable x86 builds')
    if [(c['fill'],c['hello']['width'],c['hello']['height']) for c in report['cases']]!=[(0xA5,640,480),(0xCC,1024,768)]:raise ValueError('glyph exact two cases')
    for c in report['cases']:
        if c['hello']['pointer_bytes']!=4 or c['hello']['window_visible'] is not False or c['platform_hello']['pointer_bytes']!=4:raise ValueError('glyph hidden owned platform')
        owner,image,objects=verify_prefix(c);verify_atlas(c,owner,image,objects);verify_gdi(c,owner,image);verify_raster(c,owner,image)
        dc=dict(atlas_texture_release_count=0,texture_surface_release_count=1,texture_release_count=0,extra_reference_release_counts=[3,2,1],device_release_count=0,factory_release_count=0,window_destroyed=True,all_owned_resources_released=True)
        pc=dict(atlas_fonts_released=1,atlas_dcs_released=1,atlas_bitmaps_released=1,atlas_selection_restored=True,fonts_released=2,dcs_released=1,cache_bitmaps_released=1,cache_dcs_released=1,cache_selection_restored=True,all_owned_resources_released=True)
        if c['device_cleanup']!=dc or c['platform_cleanup']!=pc:raise ValueError('glyph complete owned resource cleanup')
        verify_trace(c['device_trace'],[(r['op'],r['request'],r['result']) for r in device_calls(c)],dc)
        verify_trace(c['platform_trace'],[(r['op'] if 'op' in r else r['name'],r['request'],r['result']) for r in platform_calls(c)],pc)
        if len(c['refused_address_collisions'])>5:raise ValueError('glyph bounded collisions')
        for r in c['refused_address_collisions']:
            if r['error']!='live interface mapping collides with audit ownership' or r['cleanup']['all_owned_resources_released'] is not True or r['trace'][-1]['reply']['result']!=r['cleanup']:raise ValueError('glyph refused collision cleanup')
    return dict(cases=2,phase='raster',glyphs_per_case=95,UV_stores_per_case=380,texture_upload_executed=False,retained_VM_advanced=False)


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('report');a=p.parse_args();print(json.dumps(verify_report(json.loads((ROOT/a.report).read_text(encoding='utf-8')))))
