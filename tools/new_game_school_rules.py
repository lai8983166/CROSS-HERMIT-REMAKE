"""Export source-only rules for the operable new-game school, without expected snapshots."""
import argparse
import hashlib

from tools.new_game_school_emulation import origin_rules, course_rules
from tools.new_game_school_movement_emulation import work_rules
from tools.school_waitlist_emulation import category_rules
from tools.tactics_exit_emulation import ROOT, report_text


def rules():
    return {'origin_rules':origin_rules(),'course_rules':course_rules(),
            'sort_rules':category_rules(),'work_rules':work_rules()}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',required=True)
    args = parser.parse_args()
    payload = report_text(rules())
    with (ROOT/args.out).open('x',encoding='utf-8',newline='\n') as handle:
        handle.write(payload)
    print(hashlib.sha256(payload.encode()).hexdigest())
