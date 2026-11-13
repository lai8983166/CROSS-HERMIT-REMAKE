"""Independent offline review of original input publication and cleanup evidence."""
import argparse
import copy
import gzip
import hashlib
import json
from pathlib import Path
import struct

from devtools.terminal_input_native import original_contract, IMAGE, ROOT, identity
from devtools.terminal_input_platform import verify_original_format


def require(value, why):
    if not value:
        raise ValueError(why)


def format_controls():
    contract = original_contract()
    original = IMAGE.read_bytes()
    results = []
    for f in contract['formats']:
        va, table, count = f['va'], f['header'][5], f['header'][4]
        valid = verify_original_format(lambda a,n: original[a-0x400000:a-0x400000+n], contract, va)
        require(valid['sha256'] == f['sha256'], 'independent full format positive')
        addresses = dict(header_final_byte=va+23, final_object_final_byte=table+count*16-1,
                         referenced_GUID_final_byte=next(x[0] for x in f['objects'] if x[0])+15)
        for name, address in addresses.items():
            changed = bytearray(original)
            changed[address-0x400000] ^= 1
            try:
                verify_original_format(lambda a,n: bytes(changed[a-0x400000:a-0x400000+n]), contract, va)
            except ValueError as exc:
                results.append(dict(format_va=va, mutation=name, changed_va=address, rejected=True, reason=str(exc)))
            else:
                raise ValueError('format mutation accepted: '+name)
    return results


def audit(report):
    require(report['reached'] and not report.get('failure'), 'model completed original publication and cleanup')
    require(not any(report[k] for k in ('native_executed','desktop_used','ready_for_native','formal_acceptance',
                                      'native_cleanup_qualified','worker_created','wait_return','result_consumed')), 'no model promotion to native/worker acceptance')
    raw = IMAGE.read_bytes()
    sites = {x['pc']: x for x in report['instruction_sites']}
    for row in report['instruction_sites']:
        code = bytes.fromhex(row['hex'])
        require(row['count'] > 0 and raw[row['pc']-0x400000:row['pc']-0x400000+len(code)] == code, 'original executed instruction bytes')
    for va in (0x41359a,0x410ed0,0x410ee8,0x410f00,0x4110fa,0x4506e9,0x410ce7,0x410d0b,0x410d2f,0x410d5d,0x410d88):
        require(va in sites, 'required original input/publication/cleanup instruction '+hex(va))
    point = next(x for x in report['checkpoints'] if x['label']=='original_GAME_publication_after_input')
    require(point['state']['cpu']['EIP']==0x4506eb and point['GAME']==report['published_GAME'], 'original output store checkpoint')
    rows = [x for x in report['API_calls'] if x['name'].startswith('INPUT_')]
    require(len(rows)==23, 'bounded exact successful original input API trajectory')
    expected = ['INPUT_CREATE','INPUT_DEVICE','INPUT_FORMAT','INPUT_COOPERATIVE','INPUT_ACQUIRE',
                'INPUT_CLIENT_TO_SCREEN','INPUT_CURSOR_POS','INPUT_METRIC','INPUT_METRIC','INPUT_DOUBLE_CLICK',
                'INPUT_METRIC','INPUT_METRIC','INPUT_DEVICE','INPUT_FORMAT','INPUT_COOPERATIVE','INPUT_PROPERTY',
                'INPUT_DEVICE_INFO','INPUT_ACQUIRE','INPUT_UNACQUIRE','INPUT_UNACQUIRE',
                'INPUT_RELEASE','INPUT_RELEASE','INPUT_RELEASE']
    require([x['name'] for x in rows]==expected, 'original input API initialization and cleanup sequence')
    for row in rows:
        before, after = row['before']['cpu'], row['after']['cpu']
        require(len(before)==len(after)==57, 'complete CPU57 input envelope')
        require(all(before[k]==after[k] for k in before if k not in ('EAX','ESP','EIP')), 'input preserved remaining CPU components')
        require(after['EAX']==row['native_leaf']['result']==row['value'] and
                after['ESP']==row['sp']+4+len(row['args'])*4 and after['EIP']==row['ret'], 'original stdcall result/stack/return')
        require(all(t.get('released') for t in row['temporary_buffers']), 'input temporary release receipts')
        require(len(bytes.fromhex(row['current_native_PTD']['hex']))==116, 'full explicit model PTD input envelope')
    formats = [x['original_format'] for x in rows if x['name']=='INPUT_FORMAT']
    require([x['bytes'] for x in formats]==[4120,200], 'complete data format header/table records')
    create = rows[0]
    require(create['args'][1:3]==[0x800,0x5cc1bc] and create['args'][4]==0 and
            create['instance']['original_instance']==create['args'][0] and not create['instance']['helper_instance_substituted'], 'original module/version/IID retained')
    require(all(x['args'][2]==6 for x in rows if x['name']=='INPUT_COOPERATIVE'), 'foreground/nonexclusive original flags6')
    supplement = rows[-1]['supplemental_input_restore']
    require(all(x['result']==1 for x in supplement.values()) and supplement['cursor']['actual_readback']==1, 'declared supplemental cursor restoration/close/gate')
    requests = [x for x in report['native_trace'] if x['direction']=='request']
    names = [x['op'] for x in requests]
    final_release = max(i for i,x in enumerate(names) if x=='INPUT_RELEASE')
    cursor = names.index('INPUT_CURSOR_RESTORE')
    close = names.index('INPUT_CLOSE')
    first_graphics_release_after = next(i for i in range(final_release+1,len(names)) if names[i]=='GFX_RELEASE')
    window = names.index('WINDOW_CLOSE')
    require(final_release < cursor < close < first_graphics_release_after < window, 'input/cursor before graphics and window teardown')
    require(all(c['suspended_caller']['cpu']==c['restored_caller']['cpu'] and
                len(c['restored_caller']['cpu'])==57 for c in report['callbacks']), 'all recorded callback CPU57 restored')
    cleanup = report['cleanup']
    require(all(cleanup['status'][k]==0 for k in cleanup['zero_fields']), 'actual model final resource ledger zero')
    require(not cleanup['WinMain_completed'] and not cleanup['cleaned_state_resumable'] and
            not cleanup['actual_desktop_gamma_after_mode_restore_proven'], 'supplemental cleanup limits retained')
    return dict(original_instruction_sites=len(sites),original_instruction_hooks=report['instructions'],input_API_count=len(rows),
        callbacks_CPU57=len(report['callbacks']),dataformat_bytes=[x['bytes']for x in formats],
        source_descriptors=original_contract()['original_imports'],original_input_release_order=True,
        cursor_restore_before_graphics_window=True,all_final_model_resources_zero=True,
        publication_va='0x4506e9',publication_checkpoint='0x4506eb',reported_seconds=report['seconds'])


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model',required=True);parser.add_argument('--out',required=True)
    args=parser.parse_args();source=(ROOT/args.model).resolve();output=(ROOT/args.out).resolve()
    require(source.is_relative_to(ROOT/'.venv-audit') and output.is_relative_to(ROOT/'analysis') and not output.exists(),'bounded F model and fresh review output')
    report=json.loads(gzip.decompress(source.read_bytes()))
    summary=audit(report)
    controls=format_controls()
    for name, mutate in (
        ('publication_site_removed',lambda r:r['instruction_sites'].__setitem__(slice(None),[x for x in r['instruction_sites']if x['pc']!=0x4506e9])),
        ('input_CPU57_omitted',lambda r:next(x for x in r['API_calls']if x['name']=='INPUT_CREATE')['after']['cpu'].pop('XMM7')),
        ('live_input_resource',lambda r:r['cleanup']['status'].__setitem__('input_interfaces',1))):
        changed=copy.deepcopy(report);mutate(changed)
        try:audit(changed)
        except ValueError as exc:controls.append(dict(mutation=name,rejected=True,reason=str(exc)))
        else:raise ValueError('model evidence mutation accepted '+name)
    pins=[]
    for item in report['implementation']:
        actual=identity(ROOT/item['path']);require(actual==item,'final implementation pin '+item['path']);pins.append(actual)
    result=dict(kind='independent_input_platform_offline_review',accepted_within_model_scope=True,
        native_executed=False,desktop_used=False,native_admission=False,model=identity(source),reviewer=identity(__file__),
        implementation=pins,checks=summary,tamper_rejections=controls,
        native_source_review='Input native implementation was authored by this reviewer; its independent review belongs to the main agent, not this report.',
        limits=['Successful Windows/DirectInput/glyph/cursor/mode results are explicit model assumptions.',
                'No native lifetime, actual desktop gamma final readback, full independent replay, worker/wait/first-result acceptance.',
                'The source byte/site and recorded CPU57 checks validate the evidence envelope; this reviewer did not independently re-execute every instruction.',
                'Input ShowCursor/failed HRESULT paths are implemented but absent from this successful publication trajectory.',
                'Original GAME global is an abandoned pending-state artifact after supplemental destructor/free; do not resume it.'])
    body=json.dumps(result,ensure_ascii=False,indent=2)+'\n';require(len(body.encode())<65536,'small independent report')
    output.write_text(body,encoding='utf8',newline='\n');print(json.dumps(identity(output)))


if __name__=='__main__':main()
