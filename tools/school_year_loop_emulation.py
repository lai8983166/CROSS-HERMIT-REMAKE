"""Replay the original week-settlement body from September 5 through March 5.

This probes calendar, unlock and cleanup behavior on the existing ordinary-week
test roster. Course/battle inputs and ADV branches are separate campaign checks.
"""
import hashlib
import json

from tools.tactics_exit_emulation import ROOT, SOURCE_SHA256
from tools.week_settlement_emulation import WeekSettlementEmulator


def fingerprint(state):
    encoded = json.dumps(state, sort_keys=True, separators=(',', ':')).encode()
    return hashlib.sha256(encoded).hexdigest()


def calendar_checkpoints():
    source = ROOT / 'prototype/data/week_settlement_evidence.json'
    raw = source.read_bytes()
    source_sha = hashlib.sha256(raw).hexdigest()
    if source_sha != '5bdb406c2125c610c75942a9e589a9b427cdbcd5d97b0cbf35c014b1d793aedf':
        raise ValueError('week fixture differs from the audited source')
    parent = next(c['before'] for c in json.loads(raw)['cases'] if c['name'] == 'ordinary_week_probe')
    parent.update(month=9, week=5)
    cpu = WeekSettlementEmulator()
    cpu.write(0x7A528E, 9, 'h')
    cpu.write(0x7A5290, 5, 'h')
    if cpu.week_snapshot() != parent:
        raise ValueError('September calendar input differs from the original fixture')
    checkpoints = []
    for month in range(10, 16):
        for week in range(1, 6):
            # The observer records one entry per call. Keep the same CPU memory.
            cpu.week_entry_snapshot = None
            cpu.call_week()
            after = cpu.week_snapshot()
            if cpu.week_entry_snapshot is None or (after['month'], after['week']) != (month, week):
                raise ValueError(f'unexpected original transition into {month}/{week}')
            checkpoints.append({'date': [month, week], 'state_sha256': fingerprint(after)})
    return {'source_image_sha256': SOURCE_SHA256, 'parent_sha256': source_sha,
            'parent_case': 'ordinary_week_probe', 'start_date': [9, 5],
            'scope': 'consecutive original 4D3510 calls with the fixed three-student probe roster',
            'checkpoints': checkpoints}


if __name__ == '__main__':
    print(json.dumps(calendar_checkpoints(), indent=2))
