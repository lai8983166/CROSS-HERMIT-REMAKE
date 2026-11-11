"""Freeze then run: bounded offline readback evidence for architectural57 v1."""
import hashlib
import json
import sys
from pathlib import Path

from devtools.terminal_tcg_canonical57 import from_tcg, from_unicorn, Canonical57Error
from devtools.tests.test_terminal_tcg_canonical57 import SOURCES, WORKER, actual, unicorn_from_source
from devtools.terminal_tcg_canonical57_oracle import identity


def main(output):
    output = Path(output).resolve()
    if output.exists() or output.drive.lower() != 'f:':
        raise ValueError('fresh F-drive output required')
    sources = [Path(__file__), Path(__file__).with_name('terminal_tcg_canonical57.py'),
               Path(__file__).parent/'tests/test_terminal_tcg_canonical57.py']
    result = dict(schema='architectural57-offline-readback-v1', native_vm_runs=0,
                  accepted=False, full_machine_state=False, windows_admitted=False,
                  inputs=[identity(p) for p in sources], cases=[])
    for name in SOURCES:
        raw = actual(name)
        expected = from_tcg(raw, expected_cpu=0, expected_vcpus=2)
        u = unicorn_from_source(name, raw)
        readback = from_unicorn(u)
        if readback['registers'] != expected['registers']:
            raise ValueError('architectural57 readback mismatch: '+name)
        from unicorn import x86_const as x
        result['cases'].append(dict(name=name,
            source_report=identity(WORKER/name/'report.json'),
            source_elf=identity(WORKER/name/'guest.elf'),
            tcg_projection_sha256=hashlib.sha256(json.dumps(expected,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
            readback=readback, all57_equal=True,
            legacy_raw_dr4=u.reg_read(x.UC_X86_REG_DR4),
            legacy_raw_dr5=u.reg_read(x.UC_X86_REG_DR5)))
    high = json.loads((WORKER/'tcg-device-restore64-v4/report.json').read_bytes())
    try:
        from_tcg(high['before'][0],expected_cpu=0,expected_vcpus=2)
    except Canonical57Error as exc:
        result['actual_high64_refused'] = str(exc)
    else:
        raise ValueError('high64 silently accepted')
    result['all_cases_passed']=True
    output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(identity(output)))


if __name__ == '__main__':
    main(sys.argv[1])
