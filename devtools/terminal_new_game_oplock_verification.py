"""Independent v7 event/NEW_GAME audit plus all unchanged menu/ADV checks."""
import argparse
import json
from pathlib import Path
import struct
from devtools import terminal_new_game_verification as previous
from devtools import terminal_oplock_verification as native

host=previous.old
need=host.need
PATHS=('devtools/terminal_host_menu_preflight_v7.py',
    'devtools/terminal_new_game_oplock_capture.py','devtools/terminal_oplock.py',
    'devtools/terminal_oplock_probe.py','devtools/terminal_oplock_verification.py',
    'devtools/terminal_new_game_capture.py','devtools/terminal_menu_state_gate.py',
    'devtools/terminal_host_menu_input.py','devtools/terminal_owned_mouse.py','devtools/terminal_host_desktop.py')
verify_host_envelope=host.bind(host.verify_host_envelope,HOST_PATHS=PATHS)


def verify_clock(r,lock):
    need(r['qpc_frequency']==10_000_000,'same qualified native QPC frequency')
    for name in ('arm','break'):
        need(0<=lock[name+'_qpc']*100-lock[name+'_ns']<=10_000_000,'raw QPC/perf-counter cross-check')
    need(0<=lock['release_ns']-lock['release_begin_qpc']*100<=10_000_000,'release QPC/perf-counter cross-check')
    need(0<lock['release_ns']-lock['arm_ns']<15_000_000_000,'independent observer lifetime ceiling')


def verify_event(report,raw,check_disk=True):
    p=report['probe'];capture=p['targeted_capture'];r=capture['oplock'];lock=r['oplock']
    verify_clock(r,lock)
    need(capture['pause_clock']=='perf_counter' and report['host_preflight']['elapsed_clock']=='perf_counter',
         'precise native lifetime and pause clocks')
    need(r['mode']=='private_CH001_RW_oplock' and r['error'] is None and r['accepted'] is False
         and r['game_memory_writes'] is False and r['debugger_attach'] is False,'one read-only event observer')
    need(r['file_before']==r['file_after'] and r['file_before']['path']==lock['path'], 'same unchanged locked file')
    expected=host.ROOT/'.venv-audit/scene-callback-runtime/CROSS HERMIT/CROSS HERMIT/DATA/ADV/DAT/CH001.YBC'
    need(native.windows_path(lock['path'])==native.windows_path(expected),'only reviewed private CH001')
    need(native.windows_path(r['ntdll_disk']['path'])==native.windows_path('C:/Windows/SysWOW64/ntdll.dll'),
         'recorded system module path')
    need(lock['request_error']==997 and lock['requested_level']==5 and lock['internal']==0
         and (lock['access'],lock['share'],lock['flags'])==(0x80000000,7,0x40000000), 'actual pending RW grant')
    need(struct.unpack('<HHIIIIH2x',native.raw(lock['output_hex'],24))==(1,24,5,1,1,0,0),'actual ACK-required file break')
    need(not lock['watchdog_release'] and all(lock[k] is True for k in ('file_closed','async_completed','event_closed')),
         'normal close ACK and completed async buffer')
    owner=r['owner_before'];pid=p['pid'];parent=report['lifecycle']['lifetime']['parent_pid']
    for point in ('owner_before','owner_during','owner_after'):
        record=r[point];basic=native.raw(record['basic_hex'],48)
        need(record==owner and record['debug_port']==0xffffffffffffffff
             and record['pid']==pid==struct.unpack_from('<Q',basic,32)[0]
             and record['parent_pid']==parent==struct.unpack_from('<Q',basic,40)[0], 'preserved original parent and debug port')
    rows=[s for s in p['samples'] if s['elapsed']==r['sample_elapsed']]
    need(len(rows)==1,'one retained event snapshot')
    row=rows[0];tasks=[t for t in row['tasks'] if t['vtable']==host.menu.NEW_GAME]
    need(len(tasks)==1 and (tasks[0]['pointer'],tasks[0]['thread_id'])==(r['node'],r['thread_id'])
         and 'TLS' in tasks[0],'same actual NEW_GAME instance and TLS')
    task=tasks[0];frame=next(f for f in row['frames'] if f['tid']==r['thread_id']);call=frame['oplock_file_open']
    need({0x49F53E,0x42ABF3,0x421F8A,0x56E183}<={x['return_va'] for x in frame['chain']},'original file/NEW_GAME/CRT ancestry')
    need(native.raw(call['wrapper_hex'],0x90)==raw[0x2ABC0:0x2AC50],'original file wrapper')
    stub=native.raw(call['nt_code_hex'],32);context=native.raw(frame['context_hex'],716)
    need(stub[0]==0xb8 and stub[5]==0xba and stub[10:15]==bytes.fromhex('ffd2c22c00')
         and frame['EIP']==native.u32(context,184)==call['nt_create_file']+12,'actual saved NtCreateFile return state')
    need(call['mapped_file'].casefold().endswith('\\windows\\syswow64\\ntdll.dll'), 'system call mapping')
    head=native.raw(call['TEB_hex'],48);descriptor=native.raw(call['descriptor_hex'],8)
    teb=struct.unpack_from('<H',descriptor,2)[0]|descriptor[4]<<16|descriptor[7]<<24
    need(teb==call['TEB']==task['TLS']['TEB'] and head==native.raw(task['TLS']['TEB_head_hex'],64)[:48]
         and descriptor==native.raw(task['TLS']['selector_hex'],8),'same independent TLS/stack owner')
    esp=frame['ESP'];stack=native.raw(call['stack_hex']);base,limit=struct.unpack_from('<2I',head,4)
    need(esp==native.u32(context,196) and limit<=esp<base and len(stack)==min(4096,base-esp),'original bounded stack')
    args=struct.unpack_from('<11I',stack,4)
    need(list(args)==call['args'] and args[1]==0x80100080 and args[4:]==(0,1,1,1,0x60,0,0), 'original readonly file args')
    oa=native.raw(call['object_attributes_hex'],24);us=native.raw(call['unicode_string_hex'],8)
    def at(pointer,size):
        offset=pointer-esp;need(0<=offset<=len(stack)-size,'argument points within recorded stack');return stack[offset:offset+size]
    need(at(args[2],24)==oa and at(native.u32(oa,8),8)==us and native.u32(oa)==24
         and native.u32(oa,4)==0 and native.u32(oa,12)==0x40,'raw object attributes and Unicode pointer chain')
    length,maximum,pointer=struct.unpack('<HHI',us);name=native.raw(call['name_hex'])
    need(0<length<=maximum<=2048 and len(name)==length and length%2==0 and pointer!=0,'complete actual filename')
    need(native.windows_path(name.decode('utf-16le'))==native.windows_path('\\??\\'+lock['path']),'actual syscall names locked CH001')
    need(lock['arm_qpc']<lock['break_qpc']<=r['snapshot_begin_qpc']<=call['captured_qpc']==r['captured_qpc']
         <=r['snapshot_end_qpc']<lock['release_begin_qpc']<r['exit']['qpc'],'event capture release and actual thread exit order')
    need(0<(lock['release_begin_qpc']-lock['arm_qpc'])/r['qpc_frequency']<15,'hard bounded gate')
    worker=next(w for w in p['workers'] if (w['pointer'],w['thread_id'])==(r['node'],r['thread_id']))
    need({k:v for k,v in r['exit'].items() if k!='qpc'}==worker['exit'] and worker['exit']['code']==0,
         'event lifetime ends at retained original worker exit0')
    if check_disk:
        native.same_file(r['file_before']);native.same_file(r['ntdll_disk'])
    return dict(event_triggered_NEW_GAME_observed=True,thread_id=r['thread_id'],node=r['node'],
                retained_exit_code=0,original_debugger_preserved=True,accepted=False,
                file_gate_changes_timing=True,PTD_free_not_independently_observed=True)


def verify_report(report,raw,check_disk=True):
    previous.verify_capture(report['probe'])
    result=host.bind(host.verify_report,verify_host_envelope=verify_host_envelope)(report,raw,check_disk)
    result['oplock']=verify_event(report,raw,check_disk)
    return result


def verify_file(path,digest,desktop_digest,recovery_path=None,recovery_digest=None):
    result=host.bind(host.verify_file,verify_host_envelope=verify_host_envelope,verify_report=verify_report)(
        path,digest,desktop_digest,recovery_path,recovery_digest)
    result['oplock_verifier']=host.identity('devtools/terminal_new_game_oplock_verification.py')
    result['oplock_verifier_dependencies']=[host.identity(p) for p in (
        'devtools/terminal_new_game_verification.py','devtools/terminal_oplock_verification.py')]
    return result


if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--report',required=True);a.add_argument('--sha256',required=True)
    a.add_argument('--desktop-sha256',required=True);a.add_argument('--recovery');a.add_argument('--recovery-sha256')
    a.add_argument('--out',type=Path,required=True);args=a.parse_args()
    result=verify_file(args.report,args.sha256,args.desktop_sha256,args.recovery,args.recovery_sha256)
    with args.out.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps(dict(host_menu_observation_verified=True,accepted=False)))
