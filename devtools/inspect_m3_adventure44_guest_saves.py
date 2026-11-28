"""Inspect the powered-down worker's installed game saves through read-only disk handles."""
import hashlib
import json
import struct
from contextlib import ExitStack
from pathlib import Path

from dissect.hypervisor.disk.qcow2 import QCow2
from dissect.hypervisor.disk.vmdk import VMDK
from dissect.ntfs import NTFS
from dissect.volume.disk import Disk

from devtools.isolated_windows_vm import ROOT, VMX, WORKER, validate_vmx, vmrun
from devtools.verify_school_year_acceptance import load, pinned

GAME = 'ChaomofaWorker/project/CROSS HERMIT/CROSS HERMIT/SAVEDATA'
COPY = 'ChaomofaWorker/project/.venv-audit/scene-callback-runtime/CROSS HERMIT/CROSS HERMIT/SAVEDATA'


def open_disk(stack, path, seen):
    path = path.resolve()
    if not path.is_relative_to(WORKER.resolve()) or path in seen:
        raise ValueError('Unexpected worker disk chain')
    stream = stack.enter_context(path.open('rb'))
    if path == WORKER/'worker.vmdk':
        return VMDK(stream)
    header = stream.read(20)
    if header[:4] != b'QFI\xfb':
        raise ValueError('Invalid QCOW2 header')
    start, length = struct.unpack_from('>QI', header, 8)
    if not 0 < length <= 4096:
        raise ValueError('Missing QCOW2 parent')
    stream.seek(start)
    parent = stream.read(length).decode()
    if parent.startswith('/mnt/f/'):
        parent = 'F:/' + parent[7:]
    backing = open_disk(stack, path.parent/parent, seen | {path})
    stream.seek(0)
    return QCow2(stream, backing_file=backing).open()


def inspect_save(raw):
    if len(raw) != 0x306d4 or struct.unpack_from('<H', raw)[0] != 7:
        raise ValueError('Unrecognized native save')
    checksum = sum(b if b < 128 else b-256 for b in raw[:44]+raw[48:])
    if checksum != struct.unpack_from('<i', raw, 44)[0]:
        raise ValueError('Native signed checksum mismatch')
    count, = struct.unpack_from('<h', raw, 0x178)
    if not 0 <= count <= 40:
        raise ValueError('Invalid student count')
    return {'bytes': len(raw), 'checksum': checksum, 'date': list(struct.unpack_from('<hh', raw, 0x1a6)),
            'roster': list(struct.unpack_from(f'<{count}h', raw, 0x128))}


def inspect():
    validate_vmx(VMX.read_text(encoding='utf8'))
    if str(VMX).lower() in vmrun(['list']).lower():
        raise ValueError('Worker must be powered down for offline inspection')
    prior = load(ROOT/'analysis/school-year-loop-acceptance.json')
    january = next(r for r in prior['calendar'] if r['date'] == [13, 2])
    before = pinned(ROOT/'.venv-audit/school-year-completion/corrected/formal/settled-13-2.json',
                      january['settlement']['original']['settlement_input_sha256'])['before']
    expected = before['school']
    target = {'date': [expected['month'], expected['week']], 'roster': expected['student_ids'][:expected['student_count']]}
    disks = [WORKER/'worker.vmdk', *sorted(WORKER.glob('*/disk.qcow2'))]
    views, saves = {}, {}
    for disk in disks:
        with ExitStack() as stack:
            stream = open_disk(stack, disk, set())
            partition, = [p for p in Disk(stream).partitions if p.offset == 525336576]
            fs = NTFS(partition.open())
            found = {}
            for folder in (GAME, COPY):
                directory = fs.mft.get(folder)
                for name in sorted(directory.listdir(ignore_dos=True)):
                    if name.lower().endswith('.sav'):
                        raw = directory.get(name).open().read(0x306d5)
                        key = hashlib.sha256(raw).hexdigest()
                        saves[key] = inspect_save(raw)
                        found[folder+'/'+name] = key
            views[disk.relative_to(WORKER).as_posix()] = found
    matches = [k for k,v in saves.items() if all(v[f] == target[f] for f in target)]
    closeout = load(ROOT/'analysis/terminal-school-closeout-guest-v5-20261109.json')
    proof = pinned(ROOT/closeout['proof']['path'], closeout['proof']['sha256'])
    programs = sorted({asset.split('/')[-1] for row in proof['original_program_identities'] for asset in row['assets']})
    early_scripts = [name for name in programs if name.startswith('T') and name.endswith('.BIN')]
    campaign = pinned(ROOT/'.venv-audit/school-year-completion/corrected/formal/march-ending-v40.json',
                      prior['ending_save']['sha256'])
    student = next(row for row in before['records'] if row['character_id'] == 9)
    origin_comparison = {
        'original_guest_proof': closeout['proof'], 'observed_programs': programs,
        'observed_tactical_scripts': early_scripts, 'campaign_sha256': prior['ending_save']['sha256'],
        'first_stored_command': campaign['commands'][0],
        'january_student9_april_weeks_1_to_4': [student['week_records'][i:i+3] for i in range(0, 12, 3)],
        'native_january_observed': False}
    return {'origin_comparison': origin_comparison, 'target': target, 'native_saves': saves, 'guest_directories_by_disk': views,
            'date_and_roster_candidates': matches, 'battle_started': False, 'battle_first_difference': None}


if __name__ == '__main__':
    print(json.dumps(inspect(), ensure_ascii=False, indent=2))
