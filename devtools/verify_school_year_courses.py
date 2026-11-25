"""Verify played October lesson inputs against original course and confirmation routines.

Run after verify_school_year_courses.gd. The small output keeps weekly
digests and numerical outcomes. Full transient bundles are used only as input.
"""
import argparse
import hashlib
import json
from pathlib import Path

from tools.school_august_four_lesson_check import verify
from tools.tactics_exit_emulation import SOURCE_SHA256


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':'), sort_keys=True).encode()).hexdigest()


def verify_week(path):
    case = json.loads(path.read_bytes())
    before, after = case['before'], case['after']
    result = verify(before, after)
    return {
        'date': [before['school']['month'], before['school']['week']],
        'native_comparison': result,
        'total': after['school']['global_total_511c'],
        'mvp': after['course_result']['recipient'],
        'growth_sha256': digest(after['growth']),
        'history_sha256': digest(after['records']),
        'relationships_sha256': digest(after['school']['relationships']),
        'mvp_counts_sha256': digest(after['counts']),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    parser.add_argument('report', type=Path)
    args = parser.parse_args()
    reports = []
    for month, week in [(10, w) for w in range(1, 6)]+[(11, 1)]:
        row = verify_week(args.directory / f'settlement-{month:02}-{week}.json')
        if row['date'] != [month, week]:
            raise ValueError(f'settlement has incorrect date at {month}/{week}')
        reports.append(row)
        print('verified', row['date'], row['total'], flush=True)
    report = {'source_image_sha256': SOURCE_SHA256,
              'opening_save_sha256': '3c1eee1843f5835493569835514268d4cb81a6dcc8dad69d3c393d592eb9d82e',
              'scope': 'original x86 lesson dispatcher, skill rolls, MVP and course confirmation on consecutive played inputs',
              'weeks': reports}
    with args.report.open('x', encoding='utf8', newline='\n') as handle:
        json.dump(report, handle, ensure_ascii=False, indent=2)
        handle.write('\n')


if __name__ == '__main__':
    main()
