"""Independently verify two fresh native refusals; refusal is not scene success."""
import argparse
import json
from pathlib import Path
from devtools import terminal_scene_owner_verification as owner

need=owner.need
word=owner.u32


def verify_report(report,raw):
    owner.false_fields(report,('accepted','old_terminal_cases_replayed','independent_full_replay',
        'full_native_instruction_or_API_trace','R3_complete','R4_complete','R5_complete','R6_complete',
        'full_resource_lifetime_proved','full_battle_exit_accepted'))
    p=report['probe'];pre=p['construction_preflight'];life=report['lifecycle'];auto=report['automation']
    need(p['stop_reason']=='unsafe_native_scene_construction_rejected' and p['error'],
         'explicit failed construction, never successful execution')
    need(pre['error']=="ValueError('existing registered worker: refuse independent scene roots and input')",
         'actual non-empty scheduler refusal')
    owner.false_fields(pre,('authorized','original_scene_roots_called'))
    owner.false_fields(p,('original_scene_constructor_and_factory','native_retreat_observed',
                         'source_code_IAT_or_general_registers_written','full_battle_exit_accepted'))
    owner.false_fields(auto,('action_attempted','human_operation_required','original_input_object_written',
                            'complete_battle_exit_accepted'))
    need(auto['action'] is None and p['calls']==[] and p['samples']==[],
         'no scene root, script input or scene samples after refusal')
    pid=p['pid'];main=p['main']
    need(Path(p['process_image']).resolve()==(owner.ROOT/owner.APP).resolve(),
         'exact private original executable path')
    need(pre['pid']==life['ready']['pid']==pid and pre['main']==life['ready']['main']['pointer']==main,
         'same current startup/MAIN owner')
    need(pre['all_existing_threads_paused'] is True and pre['frames'],'atomic paused preflight read')
    need(word(owner.blob(pre['main_global_hex'],4,'MAIN global'))==main
         and word(owner.blob(pre['main_vtable_hex'],4,'MAIN class'))==0x5986A0,'actual original MAIN')
    owner.blob(pre['MAIN_event_hex'],8,'MAIN pending')
    manager=owner.blob(pre['manager_hex'],0x120,'scheduler');rows=pre['registered_tasks']
    need(0<len(rows)<=128,'nonempty bounded graph')
    nodes={r['pointer']:r for r in rows};need(len(nodes)==len(rows),'unique graph nodes')
    visited=[]
    for bucket in range(32):
        ptr=word(manager,bucket*8)
        while ptr:
            need(ptr in nodes and ptr not in visited,'complete acyclic registered graph')
            row=nodes[ptr];head=owner.blob(row['head_hex'],48,'task header')
            need(row['bucket']==bucket and word(head,8)==main+0x64,'actual scheduler owner')
            visited.append(ptr);ptr=word(head,12)
    need(visited==list(nodes),'exact traversal of all32 buckets')
    need(any(word(bytes.fromhex(r['head_hex']))==0x5CAA48 for r in rows),'original startup still registered')
    need(all(word(bytes.fromhex(r['head_hex']))!=0x59A430 for r in rows),'no independently constructed battle')
    expected=owner.source_rows(raw)+[dict(pointer=a,bytes=b-a,sha256=owner.sha(raw[a-0x400000:b-0x400000]))
                                    for a,b in owner.RESOURCE_RANGES]
    need(p['source_before']==p['source_after'] and p['source_before']['code']==expected,
         'live original source unchanged around refusal')
    iat=p['source_before']['IAT']
    need([r['slot'] for r in iat]==list(owner.IAT)
         and all(word(owner.blob(r['hex'],4,'IAT address'))>=0x10000 for r in iat),
         'all expected non-null original IAT slots')
    for frame in pre['frames']:owner.verify_frame(frame)
    frees=p['private_frees'];need(len(frees)==3 and all(r['released'] is True for r in frees),
                                'all private bridge blocks released')
    need(sorted(f['bytes'] for f in frees)==[4096,4096,2097152],
         'exact two code pages and private call arena extents')
    allocations=sorted((f['pointer'],f['pointer']+f['bytes']) for f in frees)
    need(all(0x10000<=a<b<=0x100000000 and a%0x10000==0 for a,b in allocations)
         and all(b<=c for (a,b),(c,d) in zip(allocations,allocations[1:])),
         'distinct non-overlapping aligned native private allocations')
    game=life['ready']['game']['pointer']
    protected=[(0x400000,0x400000+len(raw)),(main,main+0x184),(game,game+0xB218)]
    protected += [(ptr,ptr+48) for ptr in nodes]
    need(all(b<=c or d<=a for a,b in allocations for c,d in protected),
         'private allocations exclude original image and native owners')
    writes=p['host_private_writes'];need(len(writes)==2,'only two fresh bridge code writes')
    need([(r['bytes'],r['sha256']) for r in writes]==
         [(len(x),owner.sha(x)) for x in (owner.THUNK,owner.CDECL)],'exact original call-bridge bytes')
    for w in writes:
        need(any(f['pointer']<=w['pointer'] and w['pointer']+w['bytes']<=f['pointer']+f['bytes'] for f in frees),
             'host writes only inside freed private bridge allocations')
    lifetime=life['lifetime']
    need(life['error'] is None and lifetime['forced_termination'] is False
         and not lifetime['members_after_cleanup'],'owned native lifetime ended without forced kill')
    need(any(pid in r['pids'] for r in lifetime['membership']),'native child belongs to this Job')
    need(all(r['restored_exact'] is True for r in report['mutable_private_runtime_files']),
         'private mutable files restored')
    return dict(pid=pid,parent_pid=lifetime['parent_pid'],refusal_verified=True,
                prior_task_vtables=[hex(word(bytes.fromhex(r['head_hex']))) for r in rows],
                original_scene_roots=0,input_actions=0,private_allocations_released=len(frees),
                full_battle_exit_accepted=False)


def verify_pair(cases):
    raw=(owner.ROOT/'analysis/hermit_game.exe').read_bytes();results=[];identities=[]
    for path,digest in cases:
        report=owner.read_report(path,digest)
        need(report['observer']['path']=='devtools/terminal_scene_owner.py','exact owner collector path')
        required={'devtools/terminal_scene_automation.py','tools/school_native_dialogue_input.py',
                  'tools/school_native_dialogue_desktop.py',
                  'analysis/school-native-dialogue-authorization-v1-20261022.json'}
        implementations=report['automation']['implementations']
        need(len(implementations)==len(required) and {r['path'] for r in implementations}==required,
             'complete exact automation/backend implementation set')
        for row in [report['observer'],*report['automation']['implementations']]:
            file=(owner.ROOT/row['path']).resolve()
            need(file.is_relative_to(owner.ROOT) and file.stat().st_size==row['bytes']
                 and owner.sha(file.read_bytes())==row['sha256'],'current exact collector/backend identity')
        adapter=report['resource_adapter'];file=owner.ROOT/'devtools/terminal_scene_resources.py'
        need(Path(adapter['path']).resolve()==file.resolve()
             and owner.sha(file.read_bytes())==adapter['sha256']
             and Path(adapter['base_path']).resolve()==(owner.ROOT/report['observer']['path']).resolve()
             and adapter['base_sha256']==report['observer']['sha256'],'current exact resource/base adapter')
        hook=adapter['post_sample_hook']
        auto=next(r for r in implementations if r['path']=='devtools/terminal_scene_automation.py')
        need(hook['source_sha256']==auto['sha256'] and hook['invoked_after_original_threads_resumed'] is True,
             'exact recorded automation hook')
        need(owner.sha((owner.ROOT/owner.APP).read_bytes())==
             '030dca584a3a0b20751a72609f7acc823e8d79d820cebf1fcde8be6a791a9df7',
             'current private original executable bytes')
        identities.append((report['observer'],report['automation']['implementations'],adapter['sha256']))
        result=verify_report(report,raw)
        result['source']=dict(path=Path(path).as_posix(),bytes=Path(path).stat().st_size,sha256=digest)
        results.append(result)
    need(len(results)==2 and identities[0]==identities[1],'two cases under identical implementations')
    need(len({r['pid'] for r in results})==len({r['parent_pid'] for r in results})==2,
         'two distinct current original process trees')
    dependencies=[]
    for relative in ('devtools/terminal_scene_transition_contract.py',
                     'devtools/terminal_scene_owner_verification.py'):
        file=owner.ROOT/relative
        dependencies.append(dict(path=relative,bytes=file.stat().st_size,sha256=owner.sha(file.read_bytes())))
    return dict(schema_version=1,status='unsafe_construction_refused_in_two_fresh_lifetimes',accepted=False,
                cases=results,verifier_sha256=owner.sha(Path(__file__).read_bytes()),
                current_verification_dependencies=dependencies,native_dependency_attestation_complete=False,
                full_battle_exit_accepted=False,resource_lifetime_repaired=False,
                natural_scene_handoff_implemented=False,
                limitation='Proves fail-closed refusal and cleanup, not successful automatic battle execution.')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case',nargs=2,action='append',required=True,metavar=('PATH','SHA256'))
    parser.add_argument('--out',type=Path,required=True);args=parser.parse_args()
    result=verify_pair(args.case)
    with args.out.open('x',encoding='utf8') as stream:json.dump(result,stream,ensure_ascii=False,indent=2)
    print(json.dumps(dict(status=result['status'],accepted=False)))


if __name__=='__main__':main()
