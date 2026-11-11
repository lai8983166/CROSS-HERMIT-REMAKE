"""Offline QEMU qualification verifier; importing never executes native APIs.

A valid failed-graphics report can prove input isolation, never game acceptance.
Expected identities/challenge/boot are supplied independently by the caller.
"""
import argparse
import json
import re
import uuid
from pathlib import Path
from devtools.isolated_vm_preflight import verify_foreground, validate_boot_utc

GUEST_UUID = uuid.UUID('626d1a20-6383-4cd3-85d5-6c9831d6f941')


def verify(report, *, expected_source_sha256, expected_executable_sha256,
           expected_boot_utc, expected_nonce):
    def need(ok, reason):
        if not ok:
            raise ValueError(reason)
    def integer(value):
        return type(value) is int
    def context(row, session):
        need(integer(row['session']) and integer(row['active_console_session'])
             and row['session'] == row['active_console_session'] == session
             and row['input_desktop'] == 'Default'
             and row['input_desktop_query_succeeded'] is True
             and row['input_desktop_closed'] is True, 'actual current input desktop and console')
    for digest in (expected_source_sha256, expected_executable_sha256):
        need(isinstance(digest, str) and re.fullmatch('[0-9a-f]{64}', digest) is not None,
             'independently expected SHA256')
    validate_boot_utc(expected_boot_utc)
    need(integer(expected_nonce) and 0x40000000 <= expected_nonce <= 0x5fffffff, 'expected challenge domain')
    need(report['schema'] == 'terminal-tcg-qualification-v1' and report['accepted'] is False,
         'dedicated qualification envelope, never acceptance')
    g = report['guest']; h = report['host_observation']; m = g['machine']
    need(integer(report['nonce']) and integer(g['nonce']) and report['nonce'] == g['nonce'] == expected_nonce,
         'independently expected challenge')
    need(report['source_sha256'] == g['source_sha256'] == expected_source_sha256, 'source identity')
    exe = report['guest_executable']
    need(integer(exe['bytes']) and 0 < exe['bytes'] <= 4*1024**2
         and exe['sha256'] == g['executable_sha256'] == expected_executable_sha256, 'executable identity')
    need(g['schema'] == 'terminal-tcg-qualification-guest-v1' and g['accepted'] is False
         and g['game_executed'] is False and g['guest_guard_passed'] is True, 'guarded probe schema')
    need(uuid.UUID(m['uuid']) == GUEST_UUID and uuid.UUID(report['host']['uuid']).int != 0
         and uuid.UUID(report['host']['uuid']) != GUEST_UUID, 'dedicated QEMU UUID distinct from host')
    need(m['computer_name'] == 'CHAOMOFA-WORKER' and m['manufacturer'] == 'QEMU', 'dedicated QEMU identity')
    need(integer(m['logical_processors']) and m['logical_processors'] == 2
         and integer(m['memory_bytes']) and 3*1024**3 <= m['memory_bytes'] <= 4*1024**3, '2 CPU / 4 GiB bounds')
    need(integer(m['session']) and integer(m['active_console_session']) and m['session'] > 0
         and m['session'] == m['active_console_session'], 'own active console session')
    need(validate_boot_utc(m['boot_utc']) == expected_boot_utc, 'same expected boot')
    need(h['hooks_installed'] is True and h['hooks_removed'] == [True, True] and h['error'] is None,
         'complete host observation')
    need(integer(h['tagged_mouse']) and integer(h['tagged_keyboard'])
         and h['tagged_mouse'] == h['tagged_keyboard'] == 0
         and h['host_input_injected'] is False and h['host_input_blocked'] is False, 'host input isolation')
    foreground = verify_foreground(g)
    context(g['initial_input_context'], m['session'])
    need(len(g['input_guards']) == 5, 'guard immediately before all five guest input submissions')
    for row in g['input_guards']:
        context(row, m['session'])
    context(g['cleanup_input_context'], m['session'])
    need(g['cleanup_foreground_owned'] is True and not g.get('cleanup_input_error')
         and integer(g['cleanup_release_submissions']) and g['cleanup_release_submissions'] == 2
         and g['window_destroyed'] is True, 'input release and window cleanup')
    need(g['input_messages_received'] is True and [e['message'] for e in g['events']] == [0x201,0x202,0x100,0x101]
         and all(integer(e['extra']) and e['extra'] == expected_nonce and e['foreground'] is True for e in g['events']),
         'four exact tagged guest foreground messages')
    rows = g['graphics']
    need(len(rows) == 2 and rows[0]['fullscreen'] is False and rows[1]['fullscreen'] is True,
         'both original HAL modes attempted')
    graphics = True
    for r in rows:
        need(r['sdk_version'] == 220 and r['device_type'] == 1 and r['behavior_flags'] == 36
             and r['fallback_attempted'] is False and r['factory_attempted'] is True
             and type(r['passed']) is bool, 'original HAL path without fallback')
        if r['passed']:
            need(not r.get('error') and r['factory_created'] is True and r['device_created'] is True and integer(r['adapter_count']) and r['adapter_count'] > 0
                 and r['adapter_identifier_buffer_freed'] is True
                 and all(integer(r[k]) and r[k] >= 0 for k in ('display_mode_hr','create_hr','clear_hr','present_hr'))
                 and integer(r['device_release']) and integer(r['factory_release'])
                 and r['device_release'] == r['factory_release'] == 0, 'HAL rendering and resource release')
        else:
            need(isinstance(r.get('error'), str) and bool(r['error']), 'durable graphics failure details')
            if r.get('factory_created') is True:
                need(integer(r.get('factory_release')) and r['factory_release'] == 0, 'failed factory released')
            if r.get('device_created') is True or 'device_release' in r:
                need(integer(r.get('device_release')) and r['device_release'] == 0, 'failed device released')
            graphics = False
    need(g['preflight_passed'] is graphics and (not g.get('error') if graphics else bool(g.get('error'))),
         'graphics outcome agrees with guest status')
    return dict(input_isolation_verified=True, graphics_verified=graphics, qualified=graphics,
                accepted=False, original_game_compatible=False, full_battle_exit_accepted=False,
                continuous_host_performance_unaffected_proved=False, **foreground)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('report', type=Path)
    p.add_argument('--expected-source-sha256', required=True)
    p.add_argument('--expected-executable-sha256', required=True)
    p.add_argument('--expected-boot-utc', required=True)
    p.add_argument('--expected-nonce', required=True, type=lambda s: int(s, 0))
    a = p.parse_args()
    print(json.dumps(verify(json.loads(a.report.read_bytes()), expected_source_sha256=a.expected_source_sha256,
          expected_executable_sha256=a.expected_executable_sha256, expected_boot_utc=a.expected_boot_utc,
          expected_nonce=a.expected_nonce), indent=2))
