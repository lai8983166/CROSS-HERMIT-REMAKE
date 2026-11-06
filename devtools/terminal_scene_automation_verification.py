"""Independent, bounded native input verification; never full battle acceptance."""
import argparse
import json
import struct
import zipfile
from pathlib import Path

from devtools import terminal_scene_owner_verification as owner
from tools.school_native_dialogue_verification import OriginalKeyQuery, INPUT_RANGES

ROOT=owner.ROOT
need=owner.need
word=owner.u32


def verify_input(report, raw):
    p=report['probe'];auto=report['automation'];action=auto['action']
    need(auto['action_attempted'] is True and auto['maximum_actions']==1 and action is not None,
         'one actual automatic confirmation required')
    owner.false_fields(auto,('human_operation_required','original_input_object_written',
                            'complete_battle_exit_accepted'))
    owner.false_fields(action,('suspension_during_input','game_memory_written',
                              'full_instruction_causality_proved'))
    need(action['error'] is None and action['transition_observed'] is True,'successful input observation')
    expected=[dict(pointer=a,bytes=b-a,sha256=owner.sha(raw[a-0x400000:b-0x400000]))
              for a,b in INPUT_RANGES]
    need(action['input_code_identity']==expected,'live original input code')
    hwnd=p['window']['hwnd'];pid=p['pid']
    need(action['activation']['hwnd']==action['activation']['after']==hwnd,'own foreground activation')
    need(action['game']==report['lifecycle']['ready']['game']['pointer'],'original input game owner')
    rows=action['samples'];need(3<=len(rows)<=256,'bounded input samples')
    need([r['index'] for r in rows]==list(range(len(rows))),'contiguous input order')
    need(all(a['wall_time_ns']<=b['wall_time_ns'] for a,b in zip(rows,rows[1:])),'input time order')
    pc=action['wait_PC'];need(pc==154,'declared first T0004 confirmation')
    q=OriginalKeyQuery();states=[];pcs=[]
    for row in rows:
        need(row['foreground_hwnd']==hwnd,'actual own foreground during input')
        keyboard=owner.blob(row['keyboard_hex'],0xA00,'complete input state')
        vm=owner.blob(row['VM_hex'],128,'VM state')
        owner.blob(row['mouse_hex'],0x58,'mouse state')
        # Execute the source query, including its unchanged object and ret8 ABI.
        states.append(q.query(keyboard));pcs.append(word(vm,28))
        if not any(states):
            need(vm[4]!=0 and struct.unpack_from('<HH',vm,32)==(1,51),
                 'active original opcode51 confirmation before the first observed press')
        elif all(value==pc for value in pcs):
            # Original consumption clears wait before changing PC. These are
            # unsuspended observations, so wait0 at the press is legitimate.
            need(vm[4]!=0 and struct.unpack_from('<H',vm,34)[0]==51,
                 'active confirmation consumption before first PC advancement')
    need(states[0]==0 and pcs[0]==pc and set(states)<={0,1},'initial released original query')
    press=next((i for i,v in enumerate(states) if v),None)
    need(press is not None,'original key query observed a press')
    release=next((i for i in range(press+1,len(states)) if not states[i]),None)
    advance=next((i for i,v in enumerate(pcs) if v!=pc),None)
    need(release is not None and advance is not None and advance>=press,'source input release and advancement')
    need((action['press_index'],action['release_index'],action['advanced_index'])==(press,release,advance),
         'cached input boundary derived independently')
    need(action['before_PC']==pc and action['after_PC']==pcs[advance],'derived original transition')
    receipt=action['backend']['receipt']
    need(receipt['scan_code']==0x39 and receipt['hold_ms']==receipt['maximum_hold_ms']==120
         and receipt['hold_ms_is_ceiling'] is True
         and receipt['hold_policy']=='release_on_first_observed_VM_advance_or_120ms',
         'bounded single-confirmation release policy')
    need(receipt['input_returned'] is True and receipt['released'] is True
         and receipt['down_submitted'] is True and receipt['up_attempted'] is True
         and receipt['down_result']==1 and receipt['up_results']==[1],'actual key down/up receipt')
    need((receipt['hwnd'],receipt['pid'])==(hwnd,pid)
         and receipt['existing_process_memory_written'] is False,'input exact native owner')
    need(rows[0]['wall_time_ns']<=receipt['down_wall_time_ns']<=receipt['up_wall_time_ns']
         <=rows[-1]['wall_time_ns'],'input bracketed by recorded observation')
    need(receipt['start_ns']<=receipt['down_ns']<=receipt['up_ns']<=receipt['end_ns'],
         'monotonic input receipt')
    actual_hold=receipt['up_ns']-receipt['down_ns']
    wall_hold=receipt['up_wall_time_ns']-receipt['down_wall_time_ns']
    need(0<actual_hold<=120_000_000,'observed key hold must satisfy the120ms limit')
    # The frozen backend uses a Windows monotonic clock whose tick resolution
    # can differ from wall_time_ns. Preserve a declared25ms comparison tolerance.
    need(abs(actual_hold-wall_hold)<=25_000_000,'wall and monotonic hold duration agree')
    need(abs((receipt['end_ns']-receipt['start_ns'])-
             (receipt['end_wall_time_ns']-receipt['start_wall_time_ns']))<=25_000_000,
         'wall and monotonic backend duration agree')
    # Observations are unsuspended reads, not an instruction-by-instruction proof.
    return dict(original_key_query_replays=len(rows),query_results=states,
                press_index=press,release_index=release,advanced_index=advance,
                observed_hold_ns=actual_hold,clock_comparison_tolerance_ns=25_000_000,
                transition_observed=True,full_instruction_causality_proved=False)


def verify_file(path, expected_sha):
    report=owner.read_report(path,expected_sha)
    core=owner.verify_file(path,expected_sha)
    raw=(ROOT/'analysis/hermit_game.exe').read_bytes()
    for row in report['automation']['implementations']:
        file=(ROOT/row['path']).resolve()
        need(file.is_relative_to(ROOT),'implementation inside repository')
        need(file.stat().st_size==row['bytes'] and owner.sha(file.read_bytes())==row['sha256'],
             'current automation/backend identity')
    required={'devtools/terminal_scene_automation.py','tools/school_native_dialogue_input.py',
              'tools/school_native_dialogue_desktop.py',
              'analysis/school-native-dialogue-authorization-v1-20261022.json'}
    need({r['path'] for r in report['automation']['implementations']}==required,'complete implementation identity')
    adapter=report['resource_adapter'];file=ROOT/'devtools/terminal_scene_resources.py'
    need(Path(adapter['path']).resolve()==file.resolve() and owner.sha(file.read_bytes())==adapter['sha256'],
         'resource observer identity')
    need(adapter['base_sha256']==report['observer']['sha256'],'same base observer identity')
    hook=adapter['post_sample_hook']
    auto=next(r for r in report['automation']['implementations'] if r['path']=='devtools/terminal_scene_automation.py')
    need(hook['source_sha256']==auto['sha256'] and hook['invoked_after_original_threads_resumed'] is True,
         'actual input hook identity and resumed sampling boundary')
    owner.false_fields(adapter,('input_automation_performed_by_adapter','manual_input_required',
                               'game_memory_written','original_renderer_return_substituted'))
    need(report['lifecycle']['error'] is None and report['lifecycle']['lifetime']['forced_termination'] is False,
         'bounded observation cleaned without forced Job termination')
    for s in report['probe']['samples']:
        resource=s['resources'];budget=resource['read_budget']
        need(resource['same_pause_as_owner_sample'] is True and resource['fault_proved'] is False,
             'same-pause resource observation without reported fault')
        need(budget['bytes_requested']<=4096 and budget['calls']<=96,'bounded resource reads')
    return dict(schema_version=1,status='bounded_automatic_confirmation_verified',accepted=False,
                core_owner=core,input=verify_input(report,raw),
                source_report=core['source_report'],verifier_sha256=owner.sha(Path(__file__).read_bytes()),
                resource_failure_fixed=False,full_resource_lifetime_proved=False,
                full_battle_exit_accepted=False,
                limitation='One real automatic confirmation and bounded owner snapshots; no full native instruction/API trace or resource lifetime proof.')


def verify_archived_input(path,expected_sha,archive,archive_sha):
    """Explicit old collector authentication; never rewrite a source receipt.

    This entry is input/recorded-owner verification only. It does not enable a
    fresh native execution with the historical, unsafe scene construction.
    """
    report=owner.read_report(path,expected_sha);archive=Path(archive)
    need(report['observer']['path']=='devtools/terminal_scene_owner.py','exact historical owner source path')
    need(archive.stat().st_size<1024*1024 and owner.sha(archive.read_bytes())==archive_sha,
         'explicit immutable development implementation archive')
    names={'devtools/terminal_scene_owner.py','devtools/terminal_scene_resources.py',
           'devtools/terminal_scene_automation.py'}
    with zipfile.ZipFile(archive) as z:
        need(set(z.namelist())==names|{'manifest.json'} and all(i.file_size<128*1024 for i in z.infolist()),
             'bounded exact archive member set')
        sources={name:z.read(name) for name in names}
        manifest=json.loads(z.read('manifest.json'))
    need({r['path'] for r in manifest['files']}==names,'complete archive source manifest')
    for row in manifest['files']:
        data=sources[row['path']]
        need(len(data)==row['bytes'] and owner.sha(data)==row['sha256'],'archived manifest exact bytes')
    required={'devtools/terminal_scene_automation.py','tools/school_native_dialogue_input.py',
              'tools/school_native_dialogue_desktop.py',
              'analysis/school-native-dialogue-authorization-v1-20261022.json'}
    need({r['path'] for r in report['automation']['implementations']}==required,'complete archived input identities')
    for row in [report['observer'],*report['automation']['implementations']]:
        need(row['path'] in names|required,'declared collector/backend identity only')
        data=sources.get(row['path'])
        if data is None:data=(ROOT/row['path']).read_bytes()
        need(len(data)==row['bytes'] and owner.sha(data)==row['sha256'],'exact historical collector/backend bytes')
    adapter=report['resource_adapter']
    need(Path(adapter['path']).resolve()==(ROOT/'devtools/terminal_scene_resources.py').resolve()
         and adapter['sha256']==owner.sha(sources['devtools/terminal_scene_resources.py'])
         and Path(adapter['base_path']).resolve()==(ROOT/'devtools/terminal_scene_owner.py').resolve()
         and adapter['base_sha256']==report['observer']['sha256'], 'historical resource/base adapter identity')
    hook=adapter['post_sample_hook']
    need(hook['source_sha256']==owner.sha(sources['devtools/terminal_scene_automation.py'])
         and hook['invoked_after_original_threads_resumed'] is True,
         'historical input hook belongs to the archived resumed observer')
    need(Path(report['probe']['process_image']).resolve()==(ROOT/owner.APP).resolve(),'private original image path')
    need(owner.sha((ROOT/owner.APP).read_bytes())=='030dca584a3a0b20751a72609f7acc823e8d79d820cebf1fcde8be6a791a9df7',
         'private original executable identity')
    raw=(ROOT/'analysis/hermit_game.exe').read_bytes()
    core=owner.verify_report(report,raw)
    return dict(schema_version=1,status='historical_automatic_input_reverified',accepted=False,
                source_report=dict(path=Path(path).as_posix(),sha256=expected_sha),
                explicit_source_archive=dict(path=archive.as_posix(),sha256=archive_sha),
                verifier_sha256=owner.sha(Path(__file__).read_bytes()),core_owner=core,
                input=verify_input(report,raw),unsafe_construction_enabled=False,
                resource_failure_fixed=False,full_battle_exit_accepted=False)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',type=Path,required=True);parser.add_argument('--sha256',required=True)
    parser.add_argument('--out',type=Path,required=True);args=parser.parse_args()
    result=verify_file(args.report,args.sha256)
    with args.out.open('x',encoding='utf8') as stream:json.dump(result,stream,ensure_ascii=False,indent=2)
    print(json.dumps(dict(status=result['status'],accepted=False)))


if __name__=='__main__':main()
