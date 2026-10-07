"""Export a small original-art catalog for the school playground (no rule changes)."""
from pathlib import Path
import argparse
import hashlib
import json
from tools.render_dximg import render

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / 'CROSS HERMIT/CROSS HERMIT/DATA/ADV/BIN'
PORTRAITS = {
    101: ('德涅西亚', (7, 57, 61, 104)),
    3: ('帕弥菈', (155, 57, 206, 104)),
    4: ('瑟希莉丝', (211, 57, 256, 104)),
    9: ('伊里安', (264, 57, 312, 104)),
}


def export(out: Path):
    out.mkdir(parents=True, exist_ok=True)
    school = render(str(GAME / 'HAN001.BIN'))
    sky = render(str(GAME / 'BG001_A.BIN'))
    sky.crop((0, 0, 1024, 768)).save(out / 'background.png')
    characters = {}
    for identity, (name, rect) in PORTRAITS.items():
        filename = f'portrait_{identity}.png'
        school.crop(rect).save(out / filename)
        characters[str(identity)] = {'name': name, 'portrait': filename,
            'source': 'ADV/BIN/HAN001.BIN', 'crop': list(rect),
            'role': '教师' if identity == 101 else '学生'}
    courses = {
        '10': {'name': '全面训练', 'subtitle': '七项能力均衡成长', 'focus': [0,1,2,3,4,5,6],
               'description': '兼顾七项能力；技能领悟依角色条件与课程概率决定。'},
        '11': {'name': '综合研习', 'subtitle': '力量、敏捷、感知、道德、智力', 'focus': [0,1,2,3,4],
               'description': '偏重前五项能力，同时提供魔法与光暗系技能的学习机会。'},
        '12': {'name': '身心锻炼', 'subtitle': '耐力与精神集中成长', 'focus': [5,6],
               'description': '集中积累耐力与精神成长点，兼有物理与光暗系技能学习机会。'},
    }
    catalog = {'version': 1, 'characters': characters, 'courses': courses,
        'attribute_names': ['力量','敏捷','感知','道德','智力','耐力','精神'],
        'background': 'background.png',
        'provenance': {
            'sources': {name: hashlib.sha256((GAME/name).read_bytes()).hexdigest()
                        for name in ('HAN001.BIN','BG001_A.BIN')},
            'background_crop': [0,0,1024,768],
            'names_reference': 'docs/reference/超魔法大戰.CROSS.HERMIT.密技.txt:195-212',
            'course_labels': 'remake descriptive labels, not recovered original course titles',
            'course_description_source': 'prototype/data/school_course_settlement_rules.json:training[10..12]',
            'outputs': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.glob('*.png'))}}}
    (out/'catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return catalog


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=ROOT/'prototype/assets/school')
    args = parser.parse_args()
    data = export(args.out)
    print(f'Exported {len(data["characters"])} portraits, background and catalog to {args.out}')
