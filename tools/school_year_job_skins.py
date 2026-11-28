"""Export source-backed battle poses for the jobs offered by the school personal screen."""
import argparse
import json
from pathlib import Path

from tools import school_sortie_export as sortie
from tools.school_job_menu_export import source_menu
from tools.tactics_exit_emulation import ROOT, SOURCE, SOURCE_SHA256

ASSETS = ROOT / 'prototype/assets'
NAME = 'school_winter_jobs'
PARENTS = (
    'school_field', 'school_combat', 'school_reinforcements', 'school_sorties',
    'school_seven', 'school_four', 'school_six', 'school_ten', 'school_thirteen',
    'school_eighteen', 'school_nine', 'school_fourteen', 'school_twenty',
    'school_twenty_one', 'school_july_five', 'school_thirty_five', 'school_twenty_two',
    'school_twenty_four', 'school_forty_one', 'school_thirty_one',
    'school_winter_32', 'school_winter_44', 'school_winter_29', 'school_winter_45',
)


def parent_frames():
    frames = {}
    for name in PARENTS:
        catalog = json.loads((ASSETS/name/'catalog.json').read_bytes())
        for skin in catalog['skins'].values():
            for frame in skin['frames'].values():
                sha = frame['file_sha256']
                if sha in frames:
                    continue
                ref = frame['file']
                if not ref.startswith('res://'):
                    ref = 'res://assets/'+name+'/'+ref
                path = ROOT/'prototype'/ref.removeprefix('res://')
                if sortie.digest(path.read_bytes()) != sha:
                    raise ValueError(f'Parent animation changed at {path}')
                frames[sha] = ref
    return frames


def export(output):
    if output.name != NAME:
        raise ValueError(f'Output directory must end in {NAME} for portable resource paths')
    image = SOURCE.read_bytes()
    if sortie.digest(image) != SOURCE_SHA256:
        raise ValueError('Original executable identity mismatch')
    roles = set()
    for name in PARENTS[-4:]:
        catalog = json.loads((ASSETS/name/'catalog.json').read_bytes())
        for scene in catalog['scenes'].values():
            roles.update(map(int, scene['player_skins']))
    grid = source_menu([(role, list(range(1,31))) for role in sorted(roles)])
    data = {'source_image_sha256':SOURCE_SHA256, 'player_jobs':{}, 'skins':{}, 'jobs':{}}
    output.mkdir(parents=True, exist_ok=True)
    previous = sortie.PARENT_FRAMES
    try:
        sortie.PARENT_FRAMES = parent_frames()
        for row in grid['lookup_probes']:
            role = row['member']
            choices = {}
            for job in row['selectable_jobs']:
                rules = sortie.player_job(image, role, job)
                if data['jobs'].setdefault(str(job), rules) != rules:
                    raise ValueError(f'Inconsistent job row for member {role}, job {job}')
                offset = 0x611538-sortie.BASE+16*rules['archetype']
                timing = image[offset:offset+3]
                actions = sortie.ACTIONS + list(zip(('basic_cast','basic_attack','basic_recover'), timing))
                choices[str(job)] = sortie.skin(role, job, image, data['skins'], output, actions, extend_actions=True)
            data['player_jobs'][str(role)] = choices
    finally:
        sortie.PARENT_FRAMES = previous
    raw = (json.dumps(data, ensure_ascii=False, separators=(',',':'))+'\n').encode()
    (output/'catalog.json').write_bytes(raw)
    print(f"{len(roles)} students, {len(data['jobs'])} jobs, {len(data['skins'])} skins, SHA-256 {sortie.digest(raw)}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ASSETS/NAME)
    export(parser.parse_args().output)
