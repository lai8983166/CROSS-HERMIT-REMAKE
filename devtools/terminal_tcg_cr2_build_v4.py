"""After v5 VM exit, build the CR2 helper global-read contract correction.

No old source, object, log or binary is overwritten. Only translate.c is compiled.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import struct
import subprocess

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / '.venv-audit/native-worker'
SOURCE = WORK / 'tcg-build-v1/source'
BUILD = WORK / 'tcg-build-v1/build'
OUT = WORK / 'tcg-cr2-build-v4'


def identity(path):
    data = path.read_bytes()
    return dict(path=str(path), bytes=len(data), sha256=hashlib.sha256(data).hexdigest())


def require(ok, message):
    if not ok:
        raise ValueError(message)


def check(row):
    require(identity(Path(row['path']))['sha256'] == row['sha256'], 'identity changed: ' + row['path'])


def helper_symbol(path):
    """Read an ELF64 LE symbol directly, without executing the binary."""
    data = path.read_bytes()
    require(data[:6] == b'\x7fELF\x02\x01', 'expected ELF64 LE')
    shoff = struct.unpack_from('<Q', data, 40)[0]
    size, count = struct.unpack_from('<HH', data, 58)
    sections = [struct.unpack_from('<IIQQQQIIQQ', data, shoff + i * size) for i in range(count)]
    for section in sections:
        if section[1] != 2:
            continue
        strings = sections[section[6]]
        table = data[strings[4]:strings[4] + strings[5]]
        for pos in range(section[4], section[4] + section[5], section[9]):
            name, info, other, index, value, length = struct.unpack_from('<IBBHQQ', data, pos)
            if table[name:].split(b'\0', 1)[0] == b'helper_info_write_crN':
                target = sections[index]
                raw = data[target[4] + value - target[3]:target[4] + value - target[3] + length]
                require(len(raw) > 28, 'helper symbol size')
                return dict(bytes=len(raw), raw_hex=raw.hex(), flags_byte_x86_64_offset28=raw[28])
    raise ValueError('helper_info_write_crN symbol absent')


def main():
    gate = WORK / 'tcg-wait-native-v5/report.json'
    require(gate.is_file(), 'v5 exit report absent; compilation forbidden')
    require(json.loads(gate.read_bytes()).get('process_exited') is True, 'v5 VM not confirmed exited')
    require(not OUT.exists(), 'new output required; never overwrite executed build')
    parent_path = WORK / 'tcg-cr2-build-v3/manifest.json'
    parent = json.loads(parent_path.read_bytes())
    for row in (parent['compiler_and_libraries'] + parent['link_inputs'] + parent['build_config'] + parent['overlay'] + [parent['binary']]):
        check(row)
    for row in parent['compilation']:
        check(row['object'])
    v12 = json.loads((WORK / 'tcg-checkpoint-build-v12/manifest.json').read_bytes())
    old_header = next(row for row in v12['modified_source'] if row['path'].endswith('/target/i386/helper.h'))
    check(old_header)
    row = next(row for row in parent['compilation'] if row['overlay']['path'].endswith('/tcg/translate.c'))
    overlay = OUT / 'overlay/target/i386'
    (overlay / 'tcg').mkdir(parents=True)
    for name in ('translate.c', 'emit.c.inc'):
        original = Path(row['overlay']['path']).parent / name
        (overlay / 'tcg' / name).write_bytes(original.read_bytes())
    text = Path(old_header['path']).read_text()
    old = 'DEF_HELPER_FLAGS_3(write_crN, TCG_CALL_NO_RWG, void, env, int, tl)'
    new = 'DEF_HELPER_FLAGS_3(write_crN, 0, void, env, int, tl)'
    require(text.count(old) == 1, 'exact helper declaration')
    header = overlay / 'helper.h'
    header.write_text(text.replace(old, new))
    obj = OUT / 'translate.c.o'
    args = shlex.split(row['command'])
    args[1:1] = ['-iquote', str(overlay)]
    args[args.index('-c') + 1] = str(overlay / 'tcg/translate.c')
    for flag, value in (('-o', str(obj)), ('-MF', str(obj) + '.d'), ('-MQ', str(obj))):
        args[args.index(flag) + 1] = value
    env = dict(os.environ, TMPDIR=str(WORK / 'tcg-build-v1/tmp'), XDG_CACHE_HOME=str(WORK / 'tcg-build-v1/cache'), PYTHONDONTWRITEBYTECODE='1')
    with (OUT / 'build.log').open('xb') as log:
        subprocess.run(args, cwd=BUILD, env=env, stdout=log, stderr=log, check=True, timeout=180)
        deps = Path(str(obj) + '.d').read_text()
        require(str(header) in deps, 'new helper.h absent from actual compiler dependencies')
        require(old_header['path'] not in deps and '../source/target/i386/helper.h' not in deps, 'old helper.h unexpectedly included')
        before, after = helper_symbol(Path(row['object']['path'])), helper_symbol(obj)
        require(before['flags_byte_x86_64_offset28'] == 1 and after['flags_byte_x86_64_offset28'] == 0, 'compiled helper flags not corrected')
        link = shlex.split(parent['link'])
        require(link.count(row['object']['path']) == 1, 'unique translate link input')
        link = [str(obj) if token == row['object']['path'] else token for token in link]
        binary = OUT / 'qemu-system-x86_64'
        link[link.index('-o') + 1] = str(binary)
        subprocess.run(link, cwd=BUILD, env=env, stdout=log, stderr=log, check=True, timeout=180)
    record = dict(accepted=False, parent_manifest=identity(parent_path), gate=identity(gate), binary=identity(binary), old_header=old_header, new_header=identity(header), declaration_before=old, declaration_after=new, original_object=row['object'], object=identity(obj), helper_symbol_before=before, helper_symbol_after=after, actual_dependency_file=identity(Path(str(obj)+'.d')), compile_command=shlex.join(args), link_command=shlex.join(link), compiler_and_link_inputs_rehashed_against_parent=True, only_recompiled_translation_unit='target/i386/tcg/translate.c')
    (OUT / 'manifest.json').write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps(record['binary']))


if __name__ == '__main__':
    main()
