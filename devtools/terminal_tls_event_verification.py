"""Offline verifier for owned TLS event positive/negative controls; no native APIs."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import struct

ROOT=Path(__file__).resolve().parents[1]
DEPS=('devtools/terminal_tls_event_probe.py','devtools/terminal_tls_event_fixture.cs',
      'tools/school_crt_init_capture.py','tools/school_startup_inputs.py')


def need(ok,message):
    if not ok:raise ValueError(message)


def word(raw,offset=0):return struct.unpack_from('<I',raw,offset)[0]


def blob(value,size):
    b=bytes.fromhex(value);need(len(b)==size,'complete raw state');return b


def identity(record):
    p=(ROOT/record['path']).resolve();need(p.is_relative_to(ROOT),'project identity path')
    b=p.read_bytes();need(len(b)==record['bytes'] and hashlib.sha256(b).hexdigest()==record['sha256'],
                         'exact bound implementation/binary bytes')


def check_capture(cap,pid,tid,index,pointer,value):
    need((cap['tid'],cap['index'],cap['pointer'])==(tid,index,pointer),'same capture generation')
    a=blob(cap['context_before_hex'],716);b=blob(cap['context_after_hex'],716)
    need(a==b and word(a)==0x1003F and word(a,144)==cap['FS'],'same complete returned WOW64 context')
    need(cap['live_wait_before']==cap['live_wait_after']==258,'thread live across raw observation')
    desc=blob(cap['selector_hex'],8)
    teb=struct.unpack_from('<H',desc,2)[0]|desc[4]<<16|desc[7]<<24
    need(teb==cap['TEB'] and teb>=0x10000,'actual descriptor TEB base')
    head=blob(cap['TEB_head_hex'],64)
    need((word(head,24),word(head,32),word(head,36))==(teb,pid,tid),'TEB self and current process/thread')
    need(word(head,8)<=word(a,196)<word(head,4),'same thread stack bounds')
    if index<64:
        need(cap['expansion_hex'] is None,'no invented expansion')
        slot=teb+0xE10+4*index
    else:
        expansion=word(blob(cap['expansion_hex'],4));need(expansion>0,'native expansion pointer')
        slot=expansion+(index-64)*4
    need(cap['slot']==slot and word(blob(cap['slot_hex'],4))==value,'actual native TLS slot')
    if value:
        raw=blob(cap['payload_hex'],116)
        expected=bytearray((i*13+7)&255 for i in range(116))
        struct.pack_into('<6I',expected,0,0x544C5350,pid,tid,index,0x1234ABCD,pointer)
        need(raw==expected,'complete actual helper TLS block, distinct from game CRT PTD')
    else:need(cap['payload_hex']=='','no payload from cleared/uninitialized slot')


def verify_case(case):
    need(case['error'] is None and case['observer_memory_writes']==case['observer_context_writes']==[],
         'no target writes and no capture error')
    need(case['breakpoints_installed'] is False and case['current_process_attach'] is False
         and case['original_adaptation_eligible'] is False and case['accepted'] is False,
         'owned mechanism only without trap/attach or game claim')
    need(case['forced_termination'] is False and case['job_members_after']==[]
         and case['process_signaled_after_cleanup'] is True and case['all_owned_handles_closed'] is True,
         'normal process and complete owned cleanup')
    need(0<case['wall_seconds']<17 and case['process_exit_code']==case['queried_process_exit']==0,
         'bounded normal process exit')
    events=case['events'];need(1<=len(events)<=256 and events[0]['code']==3 and events[-1]['code']==5,
                              'complete bounded debug lifecycle')
    need(events[-1]['exit_code']==0,'actual process exit event0')
    pid,tid,index,pointer,finished,frequency,begun,ready,cleared,ended=case['done']
    need(pid==case['pid'] and tid!=case['main_tid'] and 0<=index<1088 and pointer>=0x10000
         and frequency==case['qpc_frequency']>0,'actual helper identity and common QPC frequency')
    need(0<begun<=ready<=cleared<=ended<=finished,'helper ordered QPC stamps')
    previous=0;raw_previous=0
    for event in events:
        need(event['pid']==pid and event['continued'] is True and
             previous<=event['qpc']<=event['continued_qpc'] and event['raw_qpc']>=raw_previous,
             'owned ordered events all continued')
        need('text' not in event or event['code']==8,'debug string only on actual output event')
        delta=event['qpc']-event['raw_qpc']*1000000000//frequency
        need(0<=delta<=5000000,'same QPC timebase with bounded sequential-read skew')
        previous=event['continued_qpc'];raw_previous=event['raw_qpc']
        if event['code']==1:
            loader=event['exception_code'] in (0x80000003,0x4000001F) and event['tid']==case['main_tid']
            need(event['continue_status']==(0x10002 if loader else 0x80010001),'exception policy unchanged')
        else:need(event['continue_status']==0x10002,'non-exception event continued unchanged')
    config=[(i,e) for i,e in enumerate(events) if e.get('text','').startswith('TLS1 config ')]
    need(len(config)==1,'exact one configuration event')
    ci,ce=config[0];cv=list(map(int,ce['text'].split()[2:]))
    need(len(cv)==6 and cv[:4]==[pid,case['main_tid'],index,0] and cv[5]==frequency
         and ce['tid']==case['main_tid'] and cv[4]<=ce['raw_qpc'],'config binds actual main/index/QPC')
    mapping={w['tid']:w for w in case['threads']}
    creations={e['tid']:i for i,e in enumerate(events) if e['code'] in (2,3)}
    need(len(mapping)==len(case['threads'])==len(creations)==sum(e['code'] in (2,3) for e in events)
         and set(mapping)==set(creations),
         'exact unique retained native threads')
    for wt,w in mapping.items():
        need(w['create_event']==creations[wt] and w['owner_pid']==pid and w['duplicate_succeeded'] is True
             and w['final_wait']==0,'every retained thread created and finally signaled')
        exits=[i for i,e in enumerate(events) if e['code']==4 and e['tid']==wt]
        if exits:
            need(len(exits)==1 and w['exit_event']==exits[0] and creations[wt]<exits[0]
                 and w['exit_code']==w['queried_exit']==events[exits[0]]['exit_code']==0,
                 'every retained exit agrees with its event and handle query')
        else:
            need('exit_event' not in w and 'exit_code' not in w and w['queried_exit']==0,
                 'remaining threads signaled at normal process exit')
    worker=next(w for w in case['threads'] if w['tid']==tid)
    need(worker['owner_pid']==pid and worker['duplicate_succeeded'] is True
         and worker['final_wait']==worker['queried_exit']==worker['exit_code']==0,'same retained worker exit0')
    create,exit=worker['create_event'],worker['exit_event']
    need(ci<create<exit and events[create]['code']==2 and events[exit]['code']==4
         and events[create]['tid']==events[exit]['tid']==tid and events[exit]['exit_code']==0,
         'same worker creation and normal exit events')
    need(events[create]['raw_qpc']<begun and ended<=events[exit]['raw_qpc'],
         'native worker interval inside OS lifecycle')
    own=[(i,e) for i,e in enumerate(events) if e['tid']==tid]
    attempts=[x for x in case['event_attempts'] if x['tid']==tid]
    need(len(attempts)==1 and attempts[0]['event_index']==create and attempts[0]['error'] is None,
         'actual worker creation-time TLS observation')
    check_capture(attempts[0]['capture'],pid,tid,index,0,0)
    need(attempts[0]['capture']['event_index']==create,'creation sample event association')
    caps=case['captures']
    if case['mode']=='notified':
        need([e['code'] for _,e in own]==[2,8,8,4] and [c['stage'] for c in caps]==['live','clear'],
             'two cooperative synchronous TLS boundaries')
        for cap,stage,value in zip(caps,('live','clear'),(pointer,0)):
            i=cap['event_index'];event=events[i]
            fields=event['text'].split()
            need(create<i<exit and event['tid']==tid and fields[:2]==['TLS1',stage], 'actual worker output event')
            values=list(map(int,fields[2:]))
            need(values[:4]==[pid,tid,index,pointer] and values[5]==frequency,'output/raw ownership match')
            need((ready if stage=='live' else cleared)<=values[4]<=event['raw_qpc'], 'notification QPC order')
            check_capture(cap,pid,tid,index,pointer,value)
        need(caps[0]['event_index']<caps[1]['event_index'],'live TLS precedes clear')
        need(all(caps[0][k]==caps[1][k] for k in ('TEB','FS','selector_hex','slot','index')),
             'same native TLS storage for live and clear')
        observed=True
    else:
        need(case['mode']=='silent' and caps==[] and [e['code'] for _,e in own]==[2,4],
             'unnotified worker supplies no initialized-TLS synchronous event')
        need(not any(begun<=e['raw_qpc']<=ended for e in events),
             'no process-wide synchronous event during silent worker body')
        observed=False
    done=[e for e in events if e.get('text','').startswith('TLS1 done ')]
    need(len(done)==1 and list(map(int,done[0]['text'].split()[2:]))==case['done']
         and done[0]['tid']==case['main_tid'] and done[0]['raw_qpc']>=finished,'original completed helper receipt')
    return dict(mode=case['mode'],pid=pid,tid=tid,creation_TLS_zero=True,initialized_TLS_captured=observed,
                TLS_clear_captured=observed,retained_worker_exit0=True,
                marked_TLS_interval_ticks=cleared-ready,qpc_frequency=frequency,
                worker_body_seconds=(ended-begun)/frequency,cooperative_notification_required=observed,
                original_adaptation_eligible=False,accepted=False)


def verify(report,check_disk=True):
    need(report['kind']=='owned_WOW64_TLS_event_controls' and report['accepted'] is False
         and report['original_adaptation_eligible'] is False and report['original_game_started'] is False,
         'no original game qualification')
    need(not report.get('error') and report['implementations_unchanged'] is True and report['build']['returncode']==0,
         'successful fixed implementation build/run')
    need([x['path'] for x in report['implementations']]==list(DEPS),'exact implementation dependency set')
    binary=report['binary'];bp=(ROOT/binary['path']).resolve()
    need(bp.is_relative_to(ROOT/'.venv-audit') and bp.name=='tls-event-fixture.exe'
         and 0<binary['bytes']<65536,'only bounded locally built fixture binary')
    if check_disk:
        for item in report['implementations']+[report['binary']]:identity(item)
        pe=bp.read_bytes();offset=word(pe,0x3C)
        need(pe[:2]==b'MZ' and pe[offset:offset+4]==b'PE\0\0'
             and struct.unpack_from('<H',pe,offset+4)[0]==0x14C
             and struct.unpack_from('<H',pe,offset+24)[0]==0x10B
             and struct.unpack_from('<H',pe,offset+24+68)[0]==2,'actual x86 PE32 GUI-subsystem fixture')
    need([c['mode'] for c in report['cases']]==['notified','silent'],'one positive and one negative control')
    results=[verify_case(c) for c in report['cases']]
    from devtools.terminal_host_desktop import health,differences
    before=report['desktop_before'];after=report['desktop_after']
    checks=[differences(before,s) for s in after]
    need(not health(before) and len(after)==2 and checks==report['desktop_checks']==[[],[]],
         'unchanged healthy desktop')
    need(before['time_ns']<after[0]['time_ns']<after[1]['time_ns']
         and after[1]['time_ns']-after[0]['time_ns']>=900000000,'two separated final desktop checks')
    clock=report['clock']['perf_counter']
    need(clock['monotonic'] is True and clock['adjustable'] is False and clock['resolution']<=1e-6
         and 'QueryPerformanceCounter' in clock['implementation'],'high-resolution QPC observer clock')
    return dict(controls_verified=True,fixture_capture_passed=True,without_notification_TLS_capture_passed=False,
        original_adaptation_eligible=False,accepted=False,cases=results,desktop_restored=True,
        fault_cleanup_qualified=False,
        limitations=['The positive control adds OutputDebugString at initialized TLS; no equivalent mandatory game boundary or protected-parent ownership bridge is proved.',
                     'Only the observed normal cleanup paths passed. v1 has unqualified exception cleanup paths; do not reuse it as a qualified controller.',
                     'This is a helper-owned 116-byte TLS block, not the original CRT PTD or complete architectural state.',
                     'The desktop checks are independently recomputed; the original collector DEPS did not bind the desktop module or compiler at collection time.'])


def verify_file(path,digest):
    p=Path(path);raw=p.read_bytes();need(len(raw)<512*1024 and hashlib.sha256(raw).hexdigest()==digest,'bounded exact source')
    if p.suffix=='.gz':raw=gzip.decompress(raw)
    need(len(raw)<512*1024,'bounded decoded source');return verify(json.loads(raw))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--report',required=True)
    parser.add_argument('--sha256',required=True);parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args();result=verify_file(args.report,args.sha256)
    need(args.out.resolve().is_relative_to(ROOT/'analysis'),'new project evidence')
    result['source']=dict(path=args.report,sha256=args.sha256)
    result['verifier_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result['desktop_verifier_sha256']=hashlib.sha256((ROOT/'devtools/terminal_host_desktop.py').read_bytes()).hexdigest()
    with args.out.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps(result))
