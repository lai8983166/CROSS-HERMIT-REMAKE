"""Offline-only small recovery report; no desktop/native entry point."""
import argparse
import copy
import hashlib
import io
import json
from pathlib import Path
import unittest

from devtools import terminal_graphics_desktop as d
from devtools.tests.test_terminal_graphics_desktop import (
    ModelBackend, DEVICE, OWNER, OTHER_RAMP, receipt)

ROOT = Path(__file__).resolve().parents[1]
FROZEN = {
    'devtools/terminal_window_desktop.py': '8a8a0f9583bd9df18cd4a4656dc4ae3bd569654df44c32655ea0df71ab80d52b',
    'devtools/terminal_host_desktop.py': 'c2e5781af633e83db4d93e507971ef7a04ddf3601b0313f54698360110d24b76',
}


def prove():
    frozen = {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in FROZEN}
    d.need(frozen == FROZEN, 'frozen desktop source bytes changed')
    output = io.StringIO()
    suite = unittest.defaultTestLoader.loadTestsFromNames([
        'devtools.tests.test_terminal_graphics_desktop',
        'devtools.tests.test_terminal_window_desktop',
        'devtools.tests.test_terminal_host_desktop'])
    tests = unittest.TextTestRunner(stream=output).run(suite)
    d.need(tests.wasSuccessful(), output.getvalue())
    backend = ModelBackend()
    baseline = d.capture_baseline(backend, DEVICE, OWNER)
    backend.state['monitors'][0]['mode']['width'] = 800
    backend.state['graphics']['gamma_hex'] = OTHER_RAMP
    successful = d.recover(baseline, receipt(baseline, backend), backend, sleep=lambda _: None)
    d.need(successful['restored'], successful['error'])
    failed_backend = ModelBackend()
    failed_backend.state['graphics']['gamma_hex'] = OTHER_RAMP
    failed_backend.gamma_noop = True
    failed = d.recover(baseline, receipt(baseline, failed_backend), failed_backend, sleep=lambda _: None)
    d.need(not failed['restored'] and 'readback mismatch' in failed['error'], 'silent gamma failure must reject')
    tracked = ['devtools/terminal_graphics_desktop.py',
               'devtools/tests/test_terminal_graphics_desktop.py',
               'devtools/prove_terminal_graphics_desktop.py']
    return dict(schema='terminal-graphics-desktop-offline-preflight-v1',
        evidence_kind='model-only', native_admission=False, desktop_calls=0,
        native_helpers_run=0, game_published=False, formal_acceptance='2/8 unchanged',
        tests=dict(run=tests.testsRun, failures=len(tests.failures), errors=len(tests.errors)),
        frozen_sha256=frozen,
        implementation=[dict(path=p, bytes=(ROOT / p).stat().st_size,
            sha256=hashlib.sha256((ROOT / p).read_bytes()).hexdigest()) for p in tracked],
        baseline=baseline, successful_model=successful, silent_gamma_failure_model=failed,
        limits=dict(max_recovery_seconds=d.MAX_RECOVERY_SECONDS, default_recovery_seconds=10,
                    default_operations=40, max_operations=64, gamma_bytes=d.GAMMA_BYTES,
                    output_bytes_limit=262144, native_gate_closed=True),
        limitations=[
            'WindowsBackend API code was not instantiated or run; no OS compatibility qualification.',
            'No DirectInput implementation or native cleanup evidence; model receipts cannot qualify native.',
            'The runner must authenticate source refs and aggregate original wire/Job events independently.',
            'Native requires an external process watchdog; Python Budget cannot interrupt a blocked Win32/driver call.',
            'LastInput tick plus bounded age is not a complete event-generation proof; same-tick and external color changes remain unqualified.',
            'HDR/calibration/display-event behavior and GDI-to-D3D adapter mapping need actual qualification.',
            'Parent refuses cursor shape/visibility mismatch; original MAIN must balance its ShowCursor count.',
            'No launcher, new desktop authorization, native lifetime, replay, or GAME acceptance is provided.'],
        sources=[
            'https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-setdevicegammaramp',
            'https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-getdevicegammaramp',
            'https://learn.microsoft.com/en-us/windows/win32/menurc/about-cursors'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    path = Path(args.output).resolve()
    d.need(path.is_relative_to(ROOT / 'analysis') or path.is_relative_to(ROOT / '.venv-audit'), 'F workspace output only')
    d.need(path.drive.lower() == 'f:', 'F disk only')
    body = json.dumps(prove(), ensure_ascii=False, indent=2) + '\n'
    d.need(len(body.encode('utf-8')) < 262144, 'bounded model report')
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(body)
    print(json.dumps(dict(output=str(path), bytes=path.stat().st_size,
        sha256=hashlib.sha256(path.read_bytes()).hexdigest())))
