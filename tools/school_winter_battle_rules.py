"""Project the original winter mission identities and settlement tables."""
import json

from tools.school_return_adventures_catalog import catalog, mandatory_adventure
from tools.tactics_exit_emulation import ROOT


WINTER_MISSIONS = (32, 44, 29, 45)


def rules():
    adventures = {row['id']: row for row in catalog(())['adventures']}
    return {str(scene): dict(mandatory_adventure(scene), adventure=adventures[scene])
            for scene in WINTER_MISSIONS}


if __name__ == '__main__':
    path = ROOT / 'prototype/data/school_mandatory_winter.json'
    path.write_text(json.dumps(rules(), ensure_ascii=False, indent=2) + '\n',
                    encoding='utf8', newline='\n')
