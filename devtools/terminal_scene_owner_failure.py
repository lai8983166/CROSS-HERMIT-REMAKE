"""Correlate one bounded native failure with its OS crash record and original bytes.

This is a failure diagnosis, never an acceptance or a substitute for a live trace.
Only selected WER fields are retained; no full memory dump or asset copy is made.
"""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import struct

ROOT=Path(__file__).resolve().parents[1]
SOURCE_SHA='588b4288e4c737dc489d2b9bc0652cca85e3d668b1784942ef4b4bda916f1005'


def need(value,message):
    if not value:raise ValueError(message)


def sha(raw):return hashlib.sha256(raw).hexdigest()


def word(raw,offset=0):return struct.unpack_from('<I',raw,offset)[0]


def diagnose(report,wer,dll_bytes,source):
    import pefile
    need(sha(source)==SOURCE_SHA,'fixed original image')
    p=report['probe'];pid=p['pid'];worker=p['worker']['thread_id']
    need(report['accepted'] is False and not p['native_retreat_observed'],'failed observation only')
    need(wer['EventType']=='APPCRASH' and wer['Sig[3].Value'].lower()=='d3d8.dll'
         and int(wer['Sig[6].Value'],16)==0xC0000005,'OS D3D8 access violation')
    need(int(wer['AppSessionGuid'].split('-')[0],16)==pid,'OS record actual observed PID')
    need(wer['AppPath'].replace('\\','/').lower()==p['process_image'].replace('\\','/').lower(),
         'OS crash belongs to exclusively owned private runtime')
    pe=pefile.PE(data=dll_bytes)
    rva=int(wer['Sig[7].Value'],16)
    need(pe.FILE_HEADER.Machine==0x14C and pe.FILE_HEADER.TimeDateStamp==int(wer['Sig[5].Value'],16),
         'current x86 DLL version matches OS fault module')
    need(rva==0x4D8E8 and pe.get_data(rva,3)==bytes.fromhex('ff4710'),'fault instruction inc [edi+10]')
    need(pe.get_data(0x4D87E,12)==bytes.fromhex('8b7d108d47b0f7df1bff23f8'),
         'resource argument to internal pointer transform')
    need(source[0x40E244-0x400000:0x40E24A-0x400000]==bytes.fromhex('ff90f4000000'),
         'original renderer virtual method +F4')
    need(source[0x40E9FF-0x400000:0x40EA11-0x400000]==bytes.fromhex('8b9574ffffff8b422c508b4dfce8fff7ffff'),
         'original renderer resource descriptor +2C to source40E210')
    fault=[]
    for sample in p['samples']:
        for frame in sample['frames']:
            chain=[x['return_va'] for x in frame['chain']]
            if frame['tid']==p['window']['main_tid'] and 0x40E24A in chain and 0x40EA11 in chain:
                context=bytes.fromhex(frame['context_hex'])
                if len(context)==716 and word(context,184)==frame['EIP'] and word(context,156)==0xDDDDDD8D:
                    fault.append((sample,frame,context))
    need(fault,'retained main-thread fault register and original renderer ancestry')
    first,frame,context=fault[0]
    ready=report['lifecycle']['ready']
    game=bytes.fromhex(ready['game']['hex'])
    device=word(context,164)
    need(word(game,0x105C)==word(game,0xB210)==device
         and any(i['offset']==0xB210 and i['pointer']==device for i in ready['interfaces']),
         'fault device is the actual original startup device')
    base=frame['EIP']-rva
    need(base>0 and base%65536==0 and all(f['EIP']==base+rva for _,f,_ in fault),
         'same actual module base and fault instruction')
    exit_row=p['worker_exit']
    need(exit_row['thread_id']==worker and exit_row['exit_code']==0xC0000005
         and exit_row['before_WM_CLOSE'] is True,'actual worker abnormal exit before observer close')
    life=report['lifecycle']['lifetime']
    need(life['exits'][str(pid)]['signaled'] is True and life['exits'][str(pid)]['code']==0xC0000005
         and not life['members_after_cleanup'] and not life['forced_termination'],'failed process ended without observer job termination')
    head=bytes.fromhex(first['scene_head_hex']);vm=bytes.fromhex(first['VM_hex'])
    need(head[0x31]==0 and not exit_row['tail_wait_observed'],'fault precedes retreat and tail wait')
    selected={k:wer[k] for k in ('EventType','EventTime','Sig[3].Value','Sig[4].Value',
        'Sig[5].Value','Sig[6].Value','Sig[7].Value','AppSessionGuid','AppPath')}
    return dict(schema_version=1,accepted=False,kind='bounded_original_renderer_failure',
        source_sha256=SOURCE_SHA,OS_record=selected,
        DLL=dict(sha256=sha(dll_bytes),bytes=len(dll_bytes),machine=pe.FILE_HEADER.Machine,
                 timestamp=pe.FILE_HEADER.TimeDateStamp,native_base=base,fault_RVA=rva,
                 fault_instruction_hex='ff4710',fault_instruction='inc dword ptr [edi + 0x10]',
                 argument_transform_hex=pe.get_data(0x4D87E,12).hex(),
                 module_bytes_from_matching_disk_file_not_live_code_capture=True),
        first_fault_sample=first['index'],first_fault_elapsed=first['elapsed'],
        repeated_fault_contexts=len(fault),main_thread=frame['tid'],main_context_hex=context.hex(),
        main_chain=frame['chain'],EDI=word(context,156),ECX=word(context,172),
        device=device,renderer=ready['game']['pointer']+0x1058,
        same_original_startup_device_verified=True,
        attempted_write_address=(word(context,156)+16)&0xFFFFFFFF,
        inferred_nonnull_resource_argument=(word(context,156)+0x50)&0xFFFFFFFF,
        resource_argument_is_inference_from_matching_code_and_context=True,
        resource_argument_stack_bytes_not_captured=True,
        renderer_callsite_bytes_are_static_original_not_captured_live=True,
        VM_PC=word(vm,28),VM_wait=struct.unpack_from('<H',vm,32)[0],
        input_at_fault=first['input'],worker_exit=exit_row,owned_job_empty=True,
        collector_secondary_error=p['error'],close_secondary_error=report['lifecycle']['error'],
        interpretation='Invalid resource reference at renderer +F4 call; 0xDD fill is consistent with freed debug-heap storage. Exact freeing owner and scheduling cause remain unproved.',
        CRT_debug_fill_reference='https://learn.microsoft.com/en-us/cpp/c-runtime-library/crt-debug-heap-details',
        complete_battle_exit=False,wait_API_success_proved=False,
        next_capture=['Original40E210 receiver/argument and40E9FF render descriptor +50/+2C bytes',
                      'Bounded renderer queue, texture creation/release and original scene transition order',
                      'Same current native owner; do not patch game results, bypass rendering or reuse exited handles'])


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',type=Path,required=True)
    parser.add_argument('--sha256',required=True)
    parser.add_argument('--wer',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args();need(not args.out.exists(),'fresh immutable diagnosis')
    packed=args.report.read_bytes();need(len(packed)<8*1024*1024 and sha(packed)==args.sha256,'fixed bounded failure report')
    with gzip.open(args.report,'rb') as stream:raw=stream.read(32*1024*1024+1)
    need(len(raw)<=32*1024*1024,'bounded decompressed failure')
    wer_raw=args.wer.read_bytes();need(len(wer_raw)<128*1024,'bounded OS crash metadata')
    wer=dict(line.split('=',1) for line in wer_raw.decode('utf-16').splitlines() if '=' in line)
    result=diagnose(json.loads(raw),wer,Path('C:/Windows/SysWOW64/d3d8.dll').read_bytes(),
                    (ROOT/'analysis/hermit_game.exe').read_bytes())
    result.update(report=dict(path=args.report.as_posix(),bytes=len(packed),sha256=args.sha256),
                  WER_original=dict(path=str(args.wer),bytes=len(wer_raw),sha256=sha(wer_raw)),
                  implementation_sha256=sha(Path(__file__).read_bytes()))
    with args.out.open('xb') as stream:stream.write((json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode())
    print(json.dumps(dict(path=args.out.as_posix(),bytes=args.out.stat().st_size,
                         attempted_write_address=hex(result['attempted_write_address']),accepted=False)))


if __name__=='__main__':main()
