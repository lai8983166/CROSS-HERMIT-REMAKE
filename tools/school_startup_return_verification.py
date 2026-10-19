"""Honest new-helper provenance, full original prefix and startup return proof."""
import argparse
import json
from tools.school_startup_return import *
from tools.school_startup_return_platform import DEVICE_SOURCE,DEVICE_HELPER,GDI_SOURCE,GDI_HELPER,COMPILER,sha,machine
from tools.school_startup_return_prefix import verify_native_prefix,parent
from tools.school_font_caller_verification import verify_case as verify_caller
from tools.school_font_second_resource_verification import check_interface_maps
from tools.school_startup_return_emulation import OWNER,TOP,RETURN

RETAINED=('heaps','slot_heap','retained_heaps','second_heap','external_regions','retired_regions','queues','allocations')


def verify_result(result,target):
    keys={'native_return_type','eax_bits_observed','eax_is_status','method_pointer','input_after_hex','forwarder_hex','forwarder_freed','inspection'}
    if set(result)!=keys or result['native_return_type']!='void' or result['eax_is_status'] is not False:
        raise ValueError('startup return actual void API; no HRESULT')
    if not isinstance(result['eax_bits_observed'],int) or not 0<=result['eax_bits_observed']<=0xFFFFFFFF:
        raise ValueError('startup return bounded observed EAX bits')
    if result['method_pointer']!=target or result['forwarder_hex']!=capture_code(target).hex() or result['forwarder_freed'] is not True:
        raise ValueError('startup return exact owned x86 forwarding/capture/release')
    if result['input_after_hex']!=gamma_bytes().hex():raise ValueError('startup return native const gamma payload')
    inspection=result['inspection']
    if set(inspection)!={'native_requested','device_before_hex','device_after_hex','desktop_before_hex','desktop_after_hex'} or inspection['native_requested'] is not False:
        raise ValueError('startup return auxiliary gamma inspection authority')
    for key in ('device_before_hex','device_after_hex','desktop_before_hex','desktop_after_hex'):
        if len(inspection[key])!=3072 or len(bytes.fromhex(inspection[key]))!=1536:raise ValueError('startup return complete gamma inspection buffers')


def verify_admission(c,device):
    row,previous=c['gamma_admission'],c['caller_gamma'];r=row['inspection'];identity=r['result']['device']
    if (row['before_cpu']!=previous['cpu'] or row['cpu']!=previous['cpu'] or row['pending']!=previous['pending']
            or row['original_instructions_executed']!=0 or row['original_gamma_call_executed'] is not False):
        raise ValueError('startup return method inspection must preserve pending CPU')
    if (identity['pointer']!=device['pointer'] or identity['vtable']!=device['vtable'] or set(identity['methods'])!={'72'}
            or not 0<identity['methods']['72']<=0xFFFFFFFF):raise ValueError('startup return same owned actual gamma identity')
    if r!=dict(op='gamma_prepare',request=dict(pointer=device['pointer']),
            result=dict(native_requested=False,method='Read owned device vtable+72',device=identity)):
        raise ValueError('startup return exact late auxiliary method query')
    if (len(row['stack_before_sha256'])!=64 or row['stack_before_sha256']!=row['stack_after_sha256']):
        raise ValueError('startup return inspection full stack preservation')
    if {k:v for k,v in row['state'].items() if k!='foreign_maps'}!={k:v for k,v in previous['state'].items() if k!='foreign_maps'}:
        raise ValueError('startup return inspection owner/image/SEH/stack retention')
    check_interface_maps(row['state'],previous['state'],identity)
    for key in RETAINED:
        if row[key]!=previous[key]:raise ValueError('startup return admission retained full memory '+key)
    return identity


def verify_return_case(c,device):
    identity=verify_admission(c,device);pointer=device['pointer'];target=identity['methods']['72']
    call=c['startup_gamma']['api_calls']
    if len(call)!=1:raise ValueError('startup return exactly one original gamma API')
    actual=call[0];result=actual['result'];verify_result(result,target);eax=result['eax_bits_observed']
    expected=dict(op='gamma_set',va=hex(target),return_va='0x416cfd',sp=TOP-196,args=[pointer,1,OWNER+0xB408],
        request=dict(pointer=pointer,flags=1,hex=gamma_bytes().hex()),result=result,live_host_observed=True)
    if actual!=expected:raise ValueError('startup return exact native void call ABI/identity/input')
    previous=c['gamma_admission']
    for phase in PHASES:
        row=c['startup_'+phase]
        if row['phase']!=phase or row['before_cpu']!=previous['cpu']:raise ValueError('startup return one continuous original CPU')
        entry=c['device']['native']['cpu']
        cpu=dict(EIP=0x413546,ESP=TOP-88,EBP=TOP-4,EAX=eax,EBX=entry['EBX'],ECX=pointer,EDX=pointer,
            ESI=entry['ESI'],EDI=entry['EDI'],EFLAGS=70)
        returns=[(0x56CE82,0x416D04,184,eax),(0x56CE82,0x416D11,104,eax),(0x416D14,0x413546,96,eax)]
        trace=GAMMA_TRACE
        if phase=='return':
            cpu.update(EIP=RETURN,ESP=TOP+24,EBP=0x11223344,EAX=0,EDI=0x44332211)
            returns=[(0x56CE82,0x413555,8,0),(0x413558,RETURN,0,0)];trace=RETURN_TRACE
            if row['api_calls']:raise ValueError('startup return source epilogue has no API calls')
        if row['cpu']!=cpu or row['pending']!=dict(va=hex(cpu['EIP']),sp=cpu['ESP'],first_instruction_executed=False):
            raise ValueError('startup return exact natural return CPU/stack/saved registers')
        if row['instruction_trace']!=trace or row['returns']!=[dict(va=hex(a),return_va=hex(b),sp=TOP-d,eax=e) for a,b,d,e in returns]:
            raise ValueError('startup return exact original call/stack-check/unwind/ret trace')
        if row['state']!=previous['state']:raise ValueError('startup return complete owner/image/SEH/interfaces retained')
        for key in RETAINED:
            if row[key]!=previous[key]:raise ValueError('startup return complete queues/fonts/pixels/guards '+key)
        if row['original_gamma_call_executed'] is not True or row['full416CC0_returned'] is not True or row['full413450_returned'] is not (phase=='return'):
            raise ValueError('startup return exact native completion scope')
        for key in ('original_font_destructor_chain_executed','upstream_caller_executed','retained_VM_advanced','GPU_drawing_or_Present','saved_live_pointers_resumable'):
            if row[key] is not False:raise ValueError('startup return remaining upstream/VM/GPU authority')
        previous=row
    return actual


def verify_report(report):
    if report['schema_version']!=1 or report['source_contract']!=source_contract():raise ValueError('startup return fixed source contract')
    for build,source,helper in ((report['device_build'],DEVICE_SOURCE,DEVICE_HELPER),(report['platform_build'],GDI_SOURCE,GDI_HELPER)):
        if build!=dict(source_sha256=sha(source.read_bytes()),helper_sha256=sha(helper.read_bytes()),compiler_sha256=sha(COMPILER.read_bytes()),machine=0x14C) or machine(helper)!=0x14C:
            raise ValueError('startup return honest immutable actual helper build')
    if [(c['fill'],c['hello']['width'],c['hello']['height']) for c in report['cases']]!=[(0xA5,640,480),(0xCC,1024,768)]:
        raise ValueError('startup return exact two declared cases')
    for key in ('one_continuous_trajectory_per_case','explicit_empty_cache_experiment','CRT_adapter_executed','full413450_returned'):
        if report[key] is not True:raise ValueError('startup return continuous native authority')
    for key in ('original_IAT_changed','game_helpers_stubbed','retained_VM_advanced','GPU_drawing_or_Present','full_outer_frame','live_handles_resumable_after_cleanup'):
        if report[key] is not False:raise ValueError('startup return remaining source/VM/GPU boundary')
    for c in report['cases']:
        if c['hello']['pointer_bytes']!=4 or c['hello']['window_visible'] is not False or c['platform_hello']['pointer_bytes']!=4:
            raise ValueError('startup return owned hidden x86 platform')
        objects,dc,pc,d,p=verify_native_prefix(c);verify_caller(c);gamma=verify_return_case(c,objects['device'])
        cleanup=c['device_cleanup'];changed=cleanup.get('gamma_desktop_restore_write_required')
        if type(changed) is not bool:raise ValueError('startup return gamma restoration observation')
        count=5 if changed else 4
        dc.update(gamma_desktop_restore_write_required=changed,gamma_native_calls=1,gamma_device_restored=True,
            gamma_desktop_restored=True,gamma_DCs_acquired=count,gamma_DCs_released=count,gamma_DCs_balanced=True)
        if cleanup!=dc or c['platform_cleanup']!=pc:raise ValueError('startup return complete gamma/resource restoration and cleanup')
        extra=[(r['op'],r['request'],r['result']) for r in d]
        inspection=c['gamma_admission']['inspection'];extra.append((inspection['op'],inspection['request'],inspection['result']))
        extra.append((gamma['op'],gamma['request'],gamma['result']))
        parent.verify_trace(c['device_trace'],extra,dc)
        parent.verify_trace(c['platform_trace'],[(r['op'] if 'op'in r else r['name'],r['request'],r['result']) for r in p],pc)
        if len(c['refused_address_collisions'])>5:raise ValueError('startup return bounded ownership collisions')
        for r in c['refused_address_collisions']:
            if r['error']!='live interface mapping collides with audit ownership' or r['cleanup']['all_owned_resources_released'] is not True or r['trace'][-1]['reply']['result']!=r['cleanup']:
                raise ValueError('startup return refused process full cleanup')
    return dict(cases=2,actual_void_gamma_invoked=True,original416CC0_returned=True,original413450_returned=True,
        startup_result=0,startup_stack_cleanup=20,device_and_desktop_gamma_restored=True,retained_VM_advanced=False,GPU_drawing_or_Present=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('report');a=p.parse_args()
    print(json.dumps(verify_report(json.loads((ROOT/a.report).read_text(encoding='utf8')))))
