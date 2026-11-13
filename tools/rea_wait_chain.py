"""One bounded, read-only REA session for the original wait/consumer chain.

Reuses the frozen pilot's MCP transport. This imports an analysis database only;
it never launches the target executable or changes an existing Ghidra project.
"""
import hashlib
import json
import os
from pathlib import Path
import queue
import subprocess
import threading
import time

from tools.rea_native_pilot import MCP, evidence, save

ROOT = Path(__file__).resolve().parents[1]
ENV_ROOT = ROOT / '.venv-audit/rea-wait-20261113'
OUTPUT = ENV_ROOT / 'run-v1'
PACKAGE = ENV_ROOT / 'node_modules/rea-agents'
TARGET = ROOT / 'analysis/hermit_game.exe'
FUNCTIONS = ('422360', '4225a0', '4539b0', '496410', '4967b0', '56ce80', '421850')


def pin(path):
    raw = path.read_bytes()
    return {'path': str(path), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


class HiddenMCP(MCP):
    def __init__(self, entry, env, output, node):
        self.stderr = (output / 'server-stderr.log').open('w', encoding='utf-8')
        self.process = subprocess.Popen(
            [node, str(entry), 'mcp'], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=self.stderr, text=True, encoding='utf-8', env=env,
            creationflags=subprocess.CREATE_NO_WINDOW)
        self.messages = queue.Queue()
        self.sequence = 0
        self.notifications = []
        threading.Thread(target=self._read, daemon=True).start()


def main():
    OUTPUT.mkdir(parents=True, exist_ok=False)
    started = time.monotonic()
    deadline = started + 900  # Whole query phase; close has a separate 120s cap.
    env = dict(os.environ)
    for key in list(env):
        if key.startswith('REA_GHIDRA_'):
            del env[key]
    for key, child in [('TEMP', 'tmp'), ('TMP', 'tmp'), ('USERPROFILE', 'home'),
                       ('APPDATA', 'config'), ('LOCALAPPDATA', 'cache')]:
        directory = ENV_ROOT / child
        directory.mkdir(exist_ok=True)
        env[key] = str(directory)
    seeds = ['# Analyst-supplied entry hints, not independent REA discoveries.']
    seeds += [f'0x{x}\tfunction\twait_review_{x}' for x in FUNCTIONS]
    iat = ROOT / 'analysis/hermit_real_iat.json'
    for slot, name in sorted(json.loads(iat.read_bytes()).items(), key=lambda x: int(x[0])):
        label = 'API_' + name.replace('!', '_').replace('.', '_')
        seeds.append(f'{int(slot):#x}\tlabel\t{label}')
    seed_path = OUTPUT / 'seeds.tsv'
    seed_path.write_text('\n'.join(seeds) + '\n', encoding='utf-8')
    env.update(GHIDRA_INSTALL_DIR='F:/ghidra/ghidra_12.1.3_PUBLIC',
               JAVA_HOME='C:/Program Files/Eclipse Adoptium/jdk-21.0.12.101-hotspot',
               REA_ANALYSIS_PROVIDER='ghidra', REA_GHIDRA_STARTUP_TIMEOUT_MS='480000',
               REA_GHIDRA_SEED_FILE=str(seed_path))
    report = {'kind': 'rea-original-wait-chain', 'completed': False, 'accepted': False,
              'game_started': False, 'queries': [], 'query_budget_seconds': 900,
              'target_before': pin(TARGET), 'seed': pin(seed_path), 'iat': pin(iat),
              'implementations': [pin(Path(__file__)), pin(ROOT/'tools/rea_native_pilot.py')],
              'package': pin(PACKAGE/'package.json'), 'lock': pin(ENV_ROOT/'package-lock.json'),
              'started_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
              'scope': 'Static original PE analysis; entry hints are prior assertions; no runtime state claim.'}
    if report['target_before']['sha256'] != '588b4288e4c737dc489d2b9bc0652cca85e3d668b1784942ef4b4bda916f1005':
        raise RuntimeError('fixed source identity changed')
    client = HiddenMCP(PACKAGE/'scripts/rea.mjs', env, OUTPUT, 'C:/Program Files/nodejs/node.exe')
    opened = False

    def call(label, tool, arguments, limit=45, closing=False):
        remaining = deadline - time.monotonic()
        if not closing and remaining <= 0:
            raise TimeoutError('whole REA query budget exhausted')
        print('START', label, flush=True)
        begin = time.monotonic()
        result = client.request('tools/call', {'name': tool, 'arguments': arguments,
                                '_meta': {'progressToken': label}}, limit if closing else min(limit, remaining))
        save(OUTPUT / (label + '.json'), result)  # Preserve the real MCP envelope.
        row = {'label': label, 'tool': tool, 'arguments': arguments,
               'seconds': round(time.monotonic()-begin, 3), 'is_error': bool(result.get('isError'))}
        report['queries'].append(row)
        save(OUTPUT/'run.json', report)
        print('DONE', label, row['seconds'], 'error=', row['is_error'], flush=True)
        if row['is_error']:
            raise RuntimeError('REA query failed: ' + label)
        return evidence(result)

    try:
        report['initialize'] = client.request('initialize', {
            'protocolVersion': '2025-03-26', 'capabilities': {},
            'clientInfo': {'name': 'chaomofa-rea-wait-chain', 'version': '1'}}, 30)
        client.notify('notifications/initialized')
        schemas = client.request('tools/list', {}, 30)['tools']
        names = {'open_binary', 'close_binary', 'binary_session', 'binary_overview',
                 'procedure_assembly', 'procedure_pseudo_code', 'procedure_callers',
                 'procedure_callees', 'read_bytes', 'xrefs'}
        if not names.issubset({x['name'] for x in schemas}):
            raise RuntimeError('required live interface unavailable')
        save(OUTPUT/'live-schemas.json', [x for x in schemas if x['name'] in names])
        call('open', 'open_binary', {'path': str(TARGET), 'provider_id': 'ghidra'})
        opened = True
        call('session', 'binary_session', {'expected_package_version': '6.4.0'})
        call('overview', 'binary_overview', {}, 540)
        for address in FUNCTIONS:
            for tool in ('procedure_assembly', 'procedure_pseudo_code'):
                call(address+'-'+tool, tool, {'procedure': '0x'+address})
        for address in ('422360', '4539b0', '4967b0'):
            for tool in ('procedure_callers', 'procedure_callees'):
                call(address+'-'+tool, tool, {'procedure': '0x'+address})
        for address in ('453cb5', '422360', '4967b0'):
            call(address+'-xrefs', 'xrefs', {'address': '0x'+address})
        for address, length in [('422360', 0xd4), ('453c80', 0x80), ('4967b0', 0x100), ('4225a0', 0x3a)]:
            call(address+'-bytes', 'read_bytes', {'address': '0x'+address, 'length': length})
        report['completed'] = True
    except Exception as error:
        report['failure'] = repr(error)
        print('FAILED', repr(error), flush=True)
    finally:
        if opened:
            try:
                call('close', 'close_binary', {}, 120, True)
                report['closed'] = True
            except Exception as error:
                report['closed'] = False
                report['close_error'] = repr(error)
        report['server_exit_code'] = client.shutdown()
        save(OUTPUT/'notifications.json', client.notifications)
        report['target_after'] = pin(TARGET)
        report['target_unchanged'] = report['target_before'] == report['target_after']
        report['elapsed_seconds'] = round(time.monotonic()-started, 3)
        save(OUTPUT/'run.json', report)
    return 0 if report['completed'] and report.get('closed') and report['target_unchanged'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
