"""Compare the submitted skill handoff with the original personal-screen instructions."""
import argparse
import hashlib
import json
from pathlib import Path
from tools.school_personal_skills_export import original_equipment


def verify(before_file, after_file, planning_file):
    before=json.loads(before_file.read_bytes())
    after=json.loads(after_file.read_bytes())
    assignments=[c for c in json.loads(planning_file.read_bytes()) if c.get('op')=='return_skill']
    if not assignments:raise ValueError('No skill assignments in submitted planning')
    if before['date']!=after['date']:raise ValueError('Source handoff date differs')
    participants={p['character_id']:p for p in before['participants']}
    for command in assignments:
        member,skill,slot=(command[k] for k in ('member_id','skill','slot'))
        actor=participants[member]
        actor['equipped_skills'],actor['skill_statuses']=original_equipment(member,actor['job'],skill,slot,
            actor['equipped_skills'],actor['skill_statuses'])
        next(g for g in before['growth'] if g['character_id']==member)['skill_statuses']=actor['skill_statuses']
    if before!=after:raise ValueError('Handoff differs from original slot writes or refreshed skill states')
    return {'date':after['date'],'assignments':assignments,'before_sha256':hashlib.sha256(before_file.read_bytes()).hexdigest(),
            'after_sha256':hashlib.sha256(after_file.read_bytes()).hexdigest(),'all_handoff_fields_equal':True}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('before',type=Path,help='Submitted handoff after the same earlier planning commands')
    parser.add_argument('after',type=Path)
    parser.add_argument('plan',type=Path)
    args=parser.parse_args()
    print(json.dumps(verify(args.before,args.after,args.plan),ensure_ascii=False,indent=2))
