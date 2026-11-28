"""Export extra original action timelines and palette frames for equipped skills."""
import json
from pathlib import Path
from tools import school_sortie_export as sortie
from tools.school_personal_skills_export import NAME_OFFSETS
from tools.school_year_job_skins import NAME, parent_frames
from tools.tactics_exit_emulation import ROOT, SOURCE, SOURCE_SHA256


def export():
    source=SOURCE.read_bytes()
    if sortie.digest(source)!=SOURCE_SHA256:raise ValueError('Source executable changed')
    assets=ROOT/'prototype/assets'
    out=assets/'school_personal_skills'
    out.mkdir(parents=True,exist_ok=True)
    jobs=json.loads((assets/NAME/'catalog.json').read_bytes())
    classes=json.loads((ROOT/'prototype/data/school_job_change.json').read_bytes())['classes']
    data={'source_image_sha256':SOURCE_SHA256,'jobs':{},'frames':{}}
    previous=sortie.PARENT_FRAMES
    try:
        sortie.PARENT_FRAMES=parent_frames()
        for skin in jobs['skins'].values():
            for frame in skin['frames'].values():
                path=ROOT/'prototype'/frame['file'].removeprefix('res://')
                if sortie.digest(path.read_bytes())!=frame['file_sha256']:raise ValueError('Parent frame changed')
                sortie.PARENT_FRAMES.setdefault(frame['file_sha256'],frame['file'])
        for key,base in jobs['skins'].items():
            job=base['job']
            moves={}
            for skill in NAME_OFFSETS:
                if skill not in classes[job-1]['skills']:continue
                off=0x611538-sortie.BASE+16*skill
                moves[str(skill)]=list(source[off:off+3])
            actions=sorted({action for group in moves.values() for action in group})
            if not actions:continue
            skins={}
            actual=sortie.skin(base['character_id'],job,source,skins,out,[(str(i),i) for i in actions])
            if actual!=key:raise ValueError('Mismatched player palette')
            extra=skins[key]
            chart={'skills':moves,'actions':extra['actions']}
            if data['jobs'].setdefault(str(job),chart)!=chart:raise ValueError('Palette changed action timeline')
            data['frames'][key]={k:v for k,v in extra['frames'].items() if k not in base['frames']}
    finally:
        sortie.PARENT_FRAMES=previous
    (out/'catalog.json').write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')


if __name__=='__main__':
    export()
