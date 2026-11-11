"""Prepare the owned TCG Windows wait fixture; never execute it on the host."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

from devtools.terminal_vm_wait_fixture import image


def prepare(path):
    path = Path(path)
    if path.exists():
        raise ValueError('new fixture directory required')
    raw, meta = image()  # Exact frozen machine code; no original API modification.
    source = Path(__file__).with_suffix('.cs').read_bytes()
    import capstone
    ins = list(capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32).disasm(raw, 0))
    if sum(i.size for i in ins) != len(raw):
        raise ValueError('complete bounded instruction decode')
    meta.update(source_sha256=hashlib.sha256(source).hexdigest(),
                template_sha256=hashlib.sha256(raw).hexdigest(),
                source_name='terminal_tcg_wait_fixture_v3.cs', watchdog_ms=300000,
                gate_seconds=240, fixture_version=3, wait_timeout_100ns=-300000000,
                private_data_pages_pretouched=True,
                timeout_scope="self-owned TCG scheduling allowance; not game parameters", workers_gated_until_go=True,
                startup_confirms="live_affinitized_threads_only", accepted=False, original_game_observed=False,
                instructions=[dict(offset=i.address, hex=i.bytes.hex(),
                                   instruction=i.mnemonic+' '+i.op_str) for i in ins])
    path.mkdir(parents=True)
    for name, data in [('fixture.bin', raw),
                       ('manifest.json', json.dumps(meta, indent=2).encode()),
                       ('terminal_tcg_wait_fixture_v3.cs', source)]:
        with (path/name).open('xb') as f:
            f.write(data)
    return meta


def compile_fixture(path, csc=Path('C:/Windows/Microsoft.NET/Framework/v4.0.30319/csc.exe')):
    """Compile x86 only, using existing .NET tools; do not run the result."""
    path = Path(path).resolve()
    exe = path/'fixture.exe'
    if exe.exists():
        raise ValueError('new executable required')
    command = [str(csc), '/nologo', '/target:exe', '/platform:x86', '/optimize+',
               '/r:System.Web.Extensions.dll', '/out:'+str(exe),
               str(path/'terminal_tcg_wait_fixture_v3.cs')]
    p = subprocess.run(command, capture_output=True, text=True, timeout=60)
    if p.returncode != 0:
        raise RuntimeError('fixture compile failed: '+p.stdout+p.stderr)
    return dict(command=command, bytes=exe.stat().st_size,
                sha256=hashlib.sha256(exe.read_bytes()).hexdigest())


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--compile', action='store_true')
    a = p.parse_args()
    meta = prepare(a.out)
    result = dict(code_bytes=len(image()[0]), template_sha256=meta['template_sha256'])
    if a.compile:
        result['compile'] = compile_fixture(a.out)
    print(json.dumps(result))
