"""Host preflight with mandatory before/after desktop checks; plan-only by default.

The v1 collector and its failure evidence remain byte-for-byte unchanged.
No automatic shell restart, display-mode write or user preference change.
"""
import argparse
from datetime import datetime
import json
from pathlib import Path
from devtools import terminal_host_desktop as desktop


def require_capture_qualification():
    # The original callbacks route WM_PRINTCLIENT to DefWindowProc, which does
    # not draw client content. A longer startup wait cannot qualify this path.
    # No CLI override: a different capture implementation needs its own proof.
    raise RuntimeError('PrintWindow capture is unqualified; native menu test disabled before desktop access')


def run(out, deadline_utc, capture_override):
    if capture_override is not True:
        raise PermissionError('native screenshot override required before desktop work')
    require_capture_qualification()
    from devtools import terminal_host_menu_preflight as prior
    # Reject expired windows before even taking the desktop baseline.
    import time
    prior.validate_window(deadline_utc, time.time())
    out = Path(out).resolve()
    if not out.is_relative_to(prior.ROOT/'analysis'):
        raise ValueError('output must remain under F project analysis')
    receipt = Path(str(out)+'.desktop.json')
    result = desktop.guarded_run(lambda: prior.run(out, deadline_utc, capture_override), receipt)
    return dict(result, desktop_restored=True, desktop_receipt=str(receipt))


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--execute', action='store_true')
    p.add_argument('--allow-native-capture', action='store_true')
    p.add_argument('--desktop-until')
    p.add_argument('--out', type=Path)
    a = p.parse_args()
    if not a.execute:
        print(json.dumps(dict(mode='plan_only', desktop_actions=False, accepted=False,
            execution_enabled=False, blocked_by='PrintWindow client drawing is not implemented by original callbacks',
            checks=['healthy baseline before game', 'resolution and monitor topology',
                    'taskbar visibility/geometry/auto-hide', 'desktop work area',
                    'input desktop and foreground restoration', 'no remaining game window',
                    'two stable post-cleanup samples, including error paths'],
            restoration_failure='nonzero exit; never report desktop restored',
            recovery='explicit agent recovery; never silently alter shell or preferences'), indent=2))
    else:
        if not a.desktop_until or not a.out: p.error('deadline and fresh output required')
        expiry = datetime.fromisoformat(a.desktop_until)
        if expiry.tzinfo is None: p.error('deadline timezone required')
        r = run(a.out, expiry.timestamp(), a.allow_native_capture)
        print(json.dumps(r))
        if r['probe_error'] or r['lifecycle_error'] or r['budget_events'] or not r['successor_observed']:
            raise SystemExit(1)
