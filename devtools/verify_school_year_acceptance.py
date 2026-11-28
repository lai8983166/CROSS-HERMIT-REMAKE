"""Compare all thirty played calendar positions; publish only a complete verified report."""
import argparse
import hashlib
import json
import os
import tempfile
from pathlib import Path

from devtools.verify_november_sortie_result import verify_rewards
from tools.school_august_four_lesson_check import verify as verify_work
from tools.school_job_change_export import build as native_job_change
from tools.school_job_menu_export import source_menu
from tools.school_personal_skills_export import original_equipment
from tools.school_year_played_week import digest, verify as verify_original_week
from tools.tactics_exit_emulation import ROOT, SOURCE_SHA256


PARENTS = [
    ('october-one-v31.json','3c1eee1843f5835493569835514268d4cb81a6dcc8dad69d3c393d592eb9d82e'),
    ('october-course-check/november-two.json','bd8442a88105ef9e3ea8f2a881a2683b41c98850720918ca101c329b276e4d9c'),
    ('november-three-verified.json','66a5f47ca9b3dfeea6d1ad65559a807031fee72b844e761443ce470fbd73760f'),
    ('november41-victory-campaign/november-four.json','e691ab2ec7f1faedc8580447b0ef87135d5c230400f6ef28b441ebdf2c43b0c2'),
    ('november-five-verification/week-five-v37.json','922b5117f45e72753f3f1274a1880ff74d4e4648f4f6ff321be31821eb48f101'),
    ('december-one-verification/december-v38.json','12118416dc0e9d40601e89463593a3b2d1d938d5a99a106f9131e257d3f7e0f8'),
    ('december31/formal/december-two-v39.json','05aa0e94a801cb687cab070210b1a105d5febe2dfc3e0a6e513e8fbed6d9aafe'),
]
HISTORIC = [
    ('prototype/data/school_year_loop_evidence_oct_nov.json','9e770b611f0502e50660fa15effbaefd52792510b375395d9a8eb19f66c79bab'),
    ('analysis/november-forty-one-acceptance.json','08fcaa71ce75975e465977c7957190ca135ed6d41c50cb807b5324e57b380006'),
    ('analysis/school-november-five-acceptance.json','af1e5a3cecc51bf4396eb4e15138ceb772ee7073e3b39696d13da400fabb48f9'),
    ('analysis/school-december-one-acceptance.json','f5b70ac4222bbafef4fa70e7028ca398b6250eb680fb010586dd3a2b8eb533da'),
    ('analysis/december-thirty-one-acceptance.json','83dd45c575d36a51e01fcf39c8bf7d37ae380d60d82a76c40539c396126ef0c8'),
]
DATES=[(m,w) for m in range(10,16) for w in range(1,6)]
BATTLES={(11,3):41,(12,1):31,(12,3):32,(13,2):44,(13,3):29,(15,4):45}


def check(actual, expected, label):
    if actual!=expected:raise ValueError(f'{label} differs: {str(actual)[:160]} != {str(expected)[:160]}')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path):
    return json.loads(path.read_bytes())


def pinned(path, expected):
    check(sha(path),expected,str(path))
    return load(path)


def historical_sources():
    docs=[pinned(ROOT/path,expected) for path,expected in HISTORIC]
    checks={}
    for row in docs[0]['weeks']:
        checks[tuple(row['date'])]=(0,row,row['native_comparison'])
    battle=docs[1]['battle']
    checks[(11,3)]=(1,{'total':battle['score_after'],'mvp':battle['mvp'],'adventure':battle['scene']},docs[1]['original_settlement_checks'])
    for date,i,key in [((11,4),2,'native_comparison'),((11,5),3,'original_comparison'),((12,1),4,'native_comparison')]:
        row=docs[i]['settlement']
        checks[date]=(i,row,row[key])
    return checks


def validate_parents(final, replay):
    result=[]
    last=0
    for name,expected in PARENTS:
        source=ROOT/'.venv-audit'/name
        parent=pinned(source,expected)
        count=len(parent['commands'])
        if count<=last:raise ValueError('historical parent command counts are out of order')
        check(final['commands'][:count],parent['commands'],f'{name} command prefix')
        check(replay['parents'][str(count)],parent['state_sha256'],f'{name} independently rebuilt state')
        result.append({'path':str(source.relative_to(ROOT).as_posix()),'bytes':source.stat().st_size,
                       'sha256':expected,'state_sha256':parent['state_sha256'],'commands':count})
        last=count
    return result


def current_work(directory,date,row,command):
    tag='%02d-%d'%date
    battle=BATTLES.get(date)
    case_path=directory/f'{"settled" if battle else "lesson"}-{tag}.json'
    case=load(case_path)
    before,after=case['before'],case['after']
    check((before['school']['month'],before['school']['week']),date,'settlement input date')
    summary=after['sortie_result' if battle else 'course_result']
    check(summary['recipient'],row['mvp'],'played MVP')
    check(after['school']['global_total_511c'],row['total'],'played total')
    growth=after['growth']
    result={'settlement_input_sha256':sha(case_path)}
    if date==(15,4):
        # State 12 advances immediately. Its independent observer samples the
        # synchronized participant fields just before 4D3510. The growth table
        # also keeps the earlier staged package and career snapshot for each ID.
        fields=('character_id','job','attributes','growth_pools','level_50','skill_statuses','job_sums','staged_total')
        carried=[{key:participant[key] for key in fields} for participant in after['participants']]
        check([p['character_id'] for p in carried],[g['character_id'] for g in before['growth']],'terminal roster order')
        check([{**prior,**participant} for prior,participant in zip(before['growth'],carried,strict=True)],
              growth,'complete pre-week terminal growth including retained package and career fields')
        result['complete_growth_sha256']=digest(growth)
        growth=carried
    for key,data in [('growth_sha256',growth),('history_sha256',after['records']),
                     ('relationships_sha256',after['school']['relationships']),('mvp_counts_sha256',after['counts'])]:
        check(digest(data),row[key],f'{date} played {key}')
    if battle:
        handoff_path=directory/f'handoff-{battle}.json'
        facts_path=directory/f'facts-{battle}.json'
        if not facts_path.exists() and directory.name=='formal':
            # The independently replayed fight can keep its sole facts file in
            # the sibling evidence directory. Bind it to this formal handoff.
            check(sha(directory.parent/handoff_path.name),sha(handoff_path),'independently submitted handoff')
            facts_path=directory.parent/facts_path.name
        handoff=load(handoff_path)['prepared']
        facts=load(facts_path)
        trace_path=facts_path.with_name(f'trace-{battle}.json')
        check(command.get('op'),'sortie_finish','battle settlement command')
        check(load(trace_path),command['trace'],'independent fight trace versus saved command')
        check(handoff['adventure_id'],battle,'handoff mission')
        check(facts['scene_id'],battle,'replayed mission')
        round_data,=handoff['rounds']
        ratings=handoff['class_ratings']
        result.update({'handoff_sha256':sha(handoff_path),'facts_sha256':sha(facts_path),'trace_sha256':sha(trace_path),
                       'rewards':verify_rewards(before,after,round_data,ratings,facts),
                       'growth_and_confirmation':verify_work(before,after,round_data,ratings)})
    else:result['growth_and_confirmation']=verify_work(before,after)
    return result


def verify_delta(final, replay, parents, directory):
    path=ROOT/'prototype/sim/tests/school_year_winter_commands.json'
    package=load(path)
    check(package['parent_sha256'],parents[-1]['sha256'],'delta parent file')
    check(package['file_sha256'],replay['save_sha256'],'delta final file')
    check(package['header'],{k:v for k,v in final.items() if k!='commands'},'delta final header')
    suffix=package['commands']
    offset=parents[-1]['commands']
    check(suffix,final['commands'][offset:],'retained winter command delta')
    inputs=load(directory/'played-job-transfers.json')
    check(digest(inputs),replay['job_transfers_sha256'],'observed transfer inputs')
    expected=[(i,c) for i,c in enumerate(suffix,offset+1) if c['op']=='return_job']
    check([row['command'] for row in inputs],[i for i,_ in expected],'played transfer commands')
    transfers=[]
    for row,(_,cmd) in zip(inputs,expected,strict=True):
        check([row['member'],row['target']],[cmd['member'],cmd['job']],'actual requested transfer')
        enabled=[i+1 for i,flag in enumerate(row['unlock_flags']) if flag==1]
        menu=source_menu([(row['member'],enabled)])['lookup_probes'][0]
        if row['target'] not in menu['selectable_jobs']:raise ValueError('transfer outside the original personal menu')
        original=native_job_change(row)['case']['after']
        check(original,row['after'],'original transfer equipment, skills, inventory and level')
        transfers.append({'command':row['command'],'date':row['date'],'member':row['member'],
                          'old_job':row['before']['job'],'new_job':row['target'],
                          'equipment_state_sha256':digest(original)})
    observations=load(directory/'played-skills.json')
    check(digest(observations),replay['played_skills_sha256'],'observed skill inputs')
    planned=[(i,c) for i,c in enumerate(suffix,offset+1) if c['op']=='return_skill']
    check([r['command'] for r in observations],[i for i,_ in planned],'played skill commands')
    assignments=[]
    for row,(_,cmd) in zip(observations,planned,strict=True):
        member,skill,slot=(cmd[key] for key in ('member_id','skill','slot'))
        check([row['member_id'],row['skill'],row['slot']],[member,skill,slot],'requested skill assignment')
        bundle=row['before']
        check([bundle['school']['month'],bundle['school']['week']],row['date'],'skill assignment date')
        actor=next(p for p in bundle['participants'] if p['character_id']==member)
        growth=next(p for p in bundle['growth'] if p['character_id']==member)
        actor['equipped_skills'],actor['skill_statuses'],bundle['item_flags']=original_equipment(
            member,actor['job'],skill,slot,actor['equipped_skills'],actor['skill_statuses'],(actor['level_50'],bundle['item_flags']))
        growth['skill_statuses']=actor['skill_statuses']
        check(digest(bundle),row['after_sha256'],'original personal equipment and complete resulting school state')
        assignments.append({key:row[key] for key in ('command','date','member_id','skill','slot','after_sha256')})
    return {'path':path.relative_to(ROOT).as_posix(),'sha256':sha(path),'bytes':path.stat().st_size,
            'parent_sha256':parents[-1]['sha256'],'commands':len(suffix),'job_transfers':transfers,'skill_assignments':assignments}


def verification_sources():
    names=['devtools/verify_school_year_replay.gd','devtools/verify_school_year_acceptance.py',
           'devtools/verify_november_sortie_result.py','tools/school_year_played_week.py',
           'tools/week_settlement_emulation.py','tools/school_job_menu_export.py','tools/school_job_change_export.py','tools/school_personal_skills_export.py',
           'tools/school_august_four_lesson_check.py','prototype/sim/school_sortie_week.gd',
           'prototype/sim/school_winter_story.gd','prototype/sim/school_year_loop.gd',
           'prototype/sim/school_postbattle_flow.gd','prototype/sim/week_settlement_replay.gd','prototype/sim/school_playground.gd']
    return {name:hashlib.sha256((ROOT/name).read_bytes().replace(bytes([13,10]),bytes([10]))).hexdigest() for name in names}


def verify(directory,final_path):
    sources=verification_sources()
    replay=load(directory/'independent-year-replay.json')
    final=load(final_path)
    check(replay['runtime_sha256_lf'],{k:v for k,v in sources.items() if k.startswith('prototype/sim/')},'independently loaded runtime sources')
    check(final['version'],40,'final save version')
    check(replay['phase'],'school_year_complete','final phase')
    check(replay['ending_chapter'],'097A','actual ending branch')
    check(replay['terminal_commands_rejected'],['post_next','return_settle','return_depart','post_school'],'terminal guards')
    check(replay['save_sha256'],sha(final_path),'final save bytes')
    check(replay['state_sha256'],final['state_sha256'],'independent replay state')
    check(replay['commands'],len(final['commands']),'independent command count')
    check(replay['tamper']['reason'],'save_rules_changed','altered winter rules')
    check(replay['tamper']['preserved_state_sha256'],final['state_sha256'],'state after refusal')
    parents=validate_parents(final,replay)
    delta=verify_delta(final,replay,parents,directory)
    historic=historical_sources()
    work=replay['work']
    check([tuple(r['date']) for r in work],DATES[:-1],'29 playable weeks')
    check([tuple(r['date']) for r in replay['weeks']],DATES,'30 actual dates')
    arrivals=[r['command'] for r in replay['weeks']]
    check(arrivals,sorted(set(arrivals)),'ordered arrival commands')
    rows=[]
    for i,date in enumerate(DATES):
        month,week=date
        checkpoint=replay['weeks'][i]
        case=load(directory/f'original-week-{month:02}-{week}.json')
        check(case['expected_sha256'],checkpoint['state_sha256'],'command checkpoint')
        compared=verify_original_week(case)
        check(tuple(compared['date']),date,'original weekly transition')
        row={'date':list(date),'arrival_command':checkpoint['command'],'original_week':compared}
        if i<len(work):
            details=work[i]
            battle=BATTLES.get(date)
            work_index=details['command']
            if not arrivals[i]<work_index<=arrivals[i+1]:raise ValueError(f'work outside its week at {date}')
            check(work_index==arrivals[i+1],date==(15,4),'week advanced inside the battle confirmation')
            check(final['commands'][work_index-1].get('op'),'sortie_finish' if battle else 'return_settle','work command')
            check(details['work'],'adventure' if battle else 'lesson','school work kind')
            if battle:check(details['adventure'],battle,'school mission')
            if date in historic:
                src,prior,original=historic[date]
                for key in ['total','mvp','growth_sha256','history_sha256','mvp_counts_sha256','relationships_sha256','adventure']:
                    if key in prior:check(details[key],prior[key],f'{date} historical {key}')
                original={'source':HISTORIC[src][0],'comparison':original}
            else:original=current_work(directory,date,details,final['commands'][details['command']-1])
            row['settlement']={**details,'original':original}
            if date==(15,4):
                row['settlement']['observed_pre_week_participant_growth_sha256']=details['growth_sha256']
                row['settlement']['growth_sha256']=original['complete_growth_sha256']
        else:
            check(final['commands'][checkpoint['command']-1]['op'],'sortie_finish','terminal week entered by result')
            row['terminal']={'original_successor':18,'original_dispatch_address':'0x49E3D0','ending_task_factory':'0x4FB1E0','chapter':replay['ending_chapter'],'ordinary_school_return':False,
                             'rejected_commands':replay['terminal_commands_rejected']}
        rows.append(row)
        print('verified calendar',date,flush=True)
    check(verification_sources(),sources,'verification source bytes during comparison')
    return {'schema':1,'verification_source_sha256_lf':sources,'source_image_sha256':SOURCE_SHA256,'scope':'Played command campaign and bounded original x86 school/settlement routines.',
            'coverage':{'calendar_positions':len(rows),'playable_school_weeks':len(work),'completed_adventures':len(BATTLES),
                        'source_week_body':'0x4D3510','source_qualification':'0x4D3AA0','source_personal_grid':'0x4B12A0',
                        'qualification_bytes':sum(r['original_week']['qualification_bytes_compared'] for r in rows),
                        'personal_grid_cells':sum(r['original_week']['menu_cells_compared'] for r in rows)},
            'command_delta':delta,'parents':parents,'historical_report_sha256':dict(HISTORIC),'calendar':rows,
            'ending_save':{'bytes':final_path.stat().st_size,'sha256':sha(final_path),'commands':len(final['commands']),
                           'state_sha256':final['state_sha256'],'phase':replay['phase']},'tamper':replay['tamper']}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory',type=Path)
    parser.add_argument('final_save',type=Path)
    parser.add_argument('report',type=Path)
    args=parser.parse_args()
    if args.report.exists():raise FileExistsError(args.report)
    report=verify(args.directory,args.final_save)
    payload=(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode()
    with tempfile.NamedTemporaryFile(dir=args.report.parent,delete=False) as handle:
        temporary=Path(handle.name)
    try:
        temporary.write_bytes(payload)
        os.link(temporary,args.report)
    finally:
        temporary.unlink(missing_ok=True)


if __name__=='__main__':
    main()
