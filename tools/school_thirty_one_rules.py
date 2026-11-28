"""Project the December rescue objective and the original adventure reward table."""
import json
import struct

from tools.school_adventure_scene_rules import catalog as scene_catalog
from tools.school_return_adventures_catalog import catalog, mandatory_adventure
from tools.tactics_exit_emulation import BASE, ROOT, SOURCE


def rules():
    mission = mandatory_adventure(31)
    mission['adventure'] = next(row for row in catalog(())['adventures'] if row['id'] == 31)
    templates = scene_catalog((31,))['scenes']['31']['templates_hex']
    targets = struct.unpack_from('<4h', SOURCE.read_bytes(), 0x5ff880 - BASE)
    assert targets == (13, 14, 15, -1)
    mission['objective'] = {'function': '0x4356b0', 'region': 1, 'escorts': [
        {'ordinal': n, 'role': struct.unpack_from('<h', bytes.fromhex(templates[n-1]))[0]}
        for n in targets[:-1]]}
    return mission


if __name__ == '__main__':
    path = ROOT / 'prototype/data/school_mandatory_thirty_one.json'
    path.write_text(json.dumps(rules(), ensure_ascii=False, indent=2) + '\n', encoding='utf8', newline='\n')
