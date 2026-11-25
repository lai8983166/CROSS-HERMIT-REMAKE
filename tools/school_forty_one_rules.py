"""Compact source projection of the November week-three compulsory sortie."""
import json
import struct

from tools.school_adventure_scene_rules import catalog as scene_catalog
from tools.school_return_adventures_catalog import catalog, mandatory_adventure
from tools.tactics_exit_emulation import BASE, ROOT, SOURCE


def rules():
    mission = mandatory_adventure(41)
    mission['adventure'] = next(row for row in catalog(())['adventures'] if row['id'] == 41)
    scene = scene_catalog((41,))['scenes']['41']
    image = SOURCE.read_bytes()
    grade_target, sentinel = struct.unpack_from('<hh', image, 0x5ff898 - BASE)
    assert sentinel == -1

    def actor(ordinal):
        template = bytes.fromhex(scene['templates_hex'][ordinal - 1])
        return {'ordinal': ordinal, 'role': struct.unpack_from('<h', template)[0]}

    mission['objective'] = {
        'function': '0x435cd0',
        'defeat_target': actor(1),
        'ownership_target': actor(grade_target),
        'priority': [
            {'when': 'target_state_4_owned_no_losses', 'ending_sub': 2, 'selector': 1},
            {'when': 'target_state_4_owned', 'ending_sub': 5, 'selector': 2},
            {'when': 'target_state_4', 'ending_sub': 8, 'selector': 3},
            {'when': 'time_remaining_zero', 'ending_sub': 11, 'selector': 4},
            {'when': 'party_down', 'ending_sub': 14, 'selector': 5},
        ],
    }
    opening = next(s for s in scene['scripts'] if (s['block'], s['sub']) == (0, 1))
    mission['opening_timers'] = [
        dict(zip(('slot', 'block', 'sub', 'delay'), cmd['values'], strict=True))
        for cmd in opening['commands'] if cmd['opcode'] == 124
    ]
    return mission


if __name__ == '__main__':
    path = ROOT / 'prototype/data/school_mandatory_forty_one.json'
    path.write_text(json.dumps(rules(), ensure_ascii=False, indent=2) + '\n',
                    encoding='utf8', newline='\n')
