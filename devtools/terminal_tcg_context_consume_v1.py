"""Verify the same owned helper's first saved return record and cleanup, not game consumption."""
import hashlib
import struct
from pathlib import Path
from devtools.terminal_tcg_compat_context import unpack,source_digest
from devtools.terminal_tcg_wait_consume_v2 import differences,fx_differences
from devtools.terminal_vm_wait_fixture import image


def verify(trace,result):
    report=dict(accepted=False,original_game=False,first_saved_record_verified=False,checks=[],errors=[])
    def check(name,value):report['checks'].append(dict(name=name,passed=bool(value)))
    try:
        ready=trace['ready'];points={p['label']:p for p in trace['points']}
        check('same_current_fixture',result['ready']==ready and result['accepted'] is False and result['original_game_observed'] is False and result['kind']=='owned_wow64_tcg_wait_fixture')
        template,meta=image();patched=bytearray(template)
        for p in meta['patches']:
            struct.pack_into('<I',patched,p['offset'],(ready['data'] if p['symbol']=='data' else ready['nt_wait'])+p['addend'])
        check('original_helper_bytes',len(template)==214 and hashlib.sha256(template).hexdigest()==ready['template_sha256']==result['template_sha256'] and bytes(patched).hex()==ready['code_hex']==result['code_after'])
        source=Path(__file__).with_name('terminal_tcg_wait_fixture_v3.cs').read_bytes()
        check('helper_source',hashlib.sha256(source).hexdigest()==ready['source_sha256']==result['source_sha256'])
        check('nt_wait_unchanged',ready['nt_wait_before']==result['nt_wait_before']==result['nt_wait_after'])
        check('native_returns',result['returns']==[0,0,0,258] and all(type(v)is int for v in result['returns']) and result['signals']==3 and result['peer_completed'] is True and result['peer_error'] is None and result['error'] is None and result['go_received'] is True and result['counter_native_entered']==[True,True])
        check('cleanup_exit',result['cleanup_errors']==[] and result['counter_errors']==[None,None] and result['counter_affinity_restored']==[True,True] and all(result[k] is True for k in ('fixture_completed','workers_stopped','handles_closed','buffers_released','main_affinity_restored','watchdog_disarmed','process_exited')))
        final=bytes.fromhex(result['data_hex'])
        check('four_saved_records',len(final)==meta['data_bytes']==16384 and int.from_bytes(final[0x200:0x204],'little')==4)
        for name in ('call','ret32','consumer'):
            p=points[name];raw=p['states'][0];boundary=p['boundary']
            check(name+'.lossless_context',unpack(boundary['compat'],expected_cpu=0,expected_vcpus=2,expected_source_sha256=source_digest(raw))==raw)
            data=bytes.fromhex(boundary['data_hex'])
            check(name+'.first_record_not_yet_written',len(data)==16384 and data[0x200:0x204]==bytes(4) and data[0x1000:0x1400]==bytes(1024))
        post=points['consumer']['states'][0];gp=[int(v,16)&0xffffffff for v in post['gpr']]
        frame=list(struct.unpack_from('<9I',final,0x1200))
        expected=[gp[7],gp[6],gp[5],(gp[4]-4)&0xffffffff,gp[3],gp[2],gp[1],gp[0],int(post['eflags'],16)&~0x30000]
        report['frame_differences']=differences(expected,frame)
        report['fx_differences']=fx_differences(post,final[0x1000:0x1200])
        check('actual_pushfd_pushad_record',not report['frame_differences'])
        check('actual_fxsave32_record',not report['fx_differences'])
        report['first_saved_record_verified']=all(c['passed'] for c in report['checks'])
        report['scope']='First owned helper record only; FXSAVE32 architectural fields, not reserved bytes/MXCSR_MASK; remaining three returns are helper receipts, not three fully observed game handshakes.'
    except (KeyError,TypeError,ValueError,IndexError,struct.error) as exc:
        report['errors'].append(type(exc).__name__+': '+str(exc))
    return report
