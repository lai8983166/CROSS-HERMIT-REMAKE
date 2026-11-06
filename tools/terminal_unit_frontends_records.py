"""Original scene-profile B0 initialization, before declared combat inputs.

This does not initialize a current school character or authorize terminal-time
record replacement. The static character11 profile is an original EXE input;
job1/3 is an explicit experiment declaration before the original initializer.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct

from unicorn import (Uc, UC_ARCH_X86, UC_MODE_32, UC_HOOK_CODE,
                     UC_HOOK_MEM_WRITE, UC_PROT_READ, UC_PROT_WRITE, UC_PROT_EXEC)
from unicorn.x86_const import (UC_X86_REG_EAX, UC_X86_REG_ECX, UC_X86_REG_EIP,
                              UC_X86_REG_ESP, UC_X86_REG_EFLAGS)

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'analysis/hermit_game.exe'
SOURCE_SHA256 = '588b4288e4c737dc489d2b9bc0652cca85e3d668b1784942ef4b4bda916f1005'
BASE, SCRATCH, CHARACTER = 0x400000, 0x7E11B0, 0x6F8368
STACK, STACK_BYTES, RETURN, DESTINATION = 0x13000000, 0x20000, 0x14000000, 0x14000100
RECORD_BYTES = 0xB0
RANGES = ((0x4DA5F0, 0x4DA70C), (0x4DFC20, 0x4E0931),
          (0x4E0A00, 0x4E1A07), (0x56CE80, 0x56CE83),
          (0x56CEC0, 0x56CF18))
MP_PROTECTED = (0x1A, 0x20)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def need(condition, message):
    if not condition:
        raise ValueError(message)


# Final values are read from the fresh, pre-root fixture, not reconstructed
# from a terminal snapshot. Earlier writes to the same field remain documented
# in these source references; no previously implicit zero byte is added.
_TARGET_FIELDS = (
    (0, 2, 'slot', 'tools/battle_lethal_combat.py:declarations'),
    (2, 2, 'record_identity', 'tools/battle_target_acquisition_emulation.py:TargetMachine.__init__'),
    (0xC, 2, 'job', 'tools/battle_hit_damage_emulation.py:DamageMachine.__init__'),
    (0xF, 1, 'liveness', 'tools/battle_target_acquisition_emulation.py:TargetMachine.__init__'),
    (0x14, 2, 'maximum_HP', 'tools/battle_lethal_combat.py:declarations'),
    (0x16, 2, 'current_HP', 'tools/battle_lethal_combat.py:declarations'),
    (0x18, 2, 'HP_recovery', 'tools/battle_lethal_combat.py:declarations'),
    (0x24, 4, 'engage_left', 'tools/battle_lethal_combat.py:declarations'),
    (0x2E, 2, 'movement_interval', 'tools/battle_bilateral_combat.py:declarations'),
    (0x32, 2, 'attack_windup', 'tools/battle_bilateral_combat.py:declarations'),
    (0x34, 2, 'attack_recovery', 'tools/battle_bilateral_combat.py:declarations'),
    (0x37, 1, 'attack_range', 'tools/battle_bilateral_combat.py:declarations'),
    (0x38, 2, 'accuracy', 'tools/battle_bilateral_combat.py:declarations'),
    (0x3A, 2, 'power', 'tools/battle_bilateral_combat.py:declarations'),
    (0x3C, 2, 'spread', 'tools/battle_bilateral_combat.py:declarations'),
    (0x4C, 1, 'evasion', 'tools/battle_bilateral_combat.py:declarations'),
    (0x4D, 1, 'armor', 'tools/battle_bilateral_combat.py:declarations'),
    (0x52, 2, 'mental', 'tools/battle_bilateral_combat.py:declarations'),
    (0x54, 2, 'survival_threshold', 'tools/battle_lethal_combat.py:declarations'),
    (0xA4, 1, 'faction', 'tools/battle_enemy_engagement.py:declarations'),
    (0xA6, 2, 'damage_owner', 'tools/battle_lethal_combat.py:declarations'),
    (0xA8, 2, 'kill_points', 'tools/battle_lethal_combat.py:declarations'),
    (0xAA, 2, 'kills', 'tools/battle_lethal_combat.py:declarations'),
    (0xAC, 2, 'contribution', 'tools/battle_lethal_combat.py:declarations'),
    (0xAE, 1, 'deaths', 'tools/battle_lethal_combat.py:declarations'),
)


def recommended_target_spans():
    """Actual explicit target-record fields for the job1/job3 live cases."""
    return [dict(offset=o, bytes=n, field=f, source=s) for o, n, f, s in _TARGET_FIELDS]


def apply_declared_record_fields(derived, existing, explicit_spans):
    """Pure pre-root field overlay; return bytes as hex plus a complete ledger.

    `derived` is the entire original 176-byte output. `existing` is the fresh
    constructor's 176-byte record, or its 256-byte fixture allocation. The
    caller must establish that no combat/binding root has run; this pure
    function cannot establish guest lifetime or authorize a late replacement.
    """
    need(type(derived) is bytes and len(derived) == RECORD_BYTES, 'complete derived B0 bytes')
    need(type(existing) is bytes and len(existing) in (RECORD_BYTES, 256), 'fresh declared B0 or 256-byte fixture')
    need(type(explicit_spans) in (list, tuple), 'explicit field span sequence')
    out = bytearray(derived)
    covered = set()
    ledger = []
    for span in explicit_spans:
        need(type(span) is dict and set(span) == {'offset', 'bytes', 'field', 'source'}, 'named field/source span')
        o, n = span['offset'], span['bytes']
        need(type(o) is int and type(n) is int and 0 <= o < o+n <= RECORD_BYTES, 'field span inside B0')
        need(all(type(span[k]) is str and span[k].strip() for k in ('field', 'source')), 'nonempty field provenance')
        need(o+n <= MP_PROTECTED[0] or o >= MP_PROTECTED[1], 'MP and MP recovery overrides forbidden')
        offsets = set(range(o, o+n))
        need(not offsets & covered, 'overlapping declared fields')
        covered.update(offsets)
        before = bytes(out[o:o+n])
        after = existing[o:o+n]
        out[o:o+n] = after
        ledger.append(dict(span, before_hex=before.hex(), after_hex=after.hex(), changed=before != after))
    need(out[0x1A:0x20] == derived[0x1A:0x20], 'all original MP fields retained')
    need(all(out[o] == derived[o] for o in range(RECORD_BYTES) if o not in covered), 'all undeclared source bytes retained')
    return dict(record_hex=out.hex(), derived_sha256=sha(derived), declared_input_sha256=sha(existing),
                record_sha256=sha(out), overrides=ledger, retained_offsets=[o for o in range(RECORD_BYTES) if o not in covered],
                required_phase='fresh constructor before first original combat/binding root')


class _OriginalRecordMachine:
    def __init__(self, raw):
        need(len(raw) == 5980160 and sha(raw) == SOURCE_SHA256, 'exact original source image')
        self.raw = raw
        self.uc = Uc(UC_ARCH_X86, UC_MODE_32)
        self.uc.mem_map(BASE, (len(raw)+4095) & ~4095)
        self.uc.mem_write(BASE, raw)
        self.uc.mem_protect(BASE, (len(raw)+4095) & ~4095, UC_PROT_READ | UC_PROT_EXEC)
        self.uc.mem_protect(SCRATCH & ~4095, 4096, UC_PROT_READ | UC_PROT_WRITE)
        self.uc.mem_map(STACK, STACK_BYTES, UC_PROT_READ | UC_PROT_WRITE)
        self.uc.mem_map(RETURN, 4096, UC_PROT_READ | UC_PROT_WRITE)
        self.instructions = self.writes = 0
        self.code_hash = hashlib.sha256()
        self.write_hash = hashlib.sha256()
        self.entries = []
        self.mp_writes = []
        self.phase = None
        self.uc.hook_add(UC_HOOK_CODE, self.code)
        self.uc.hook_add(UC_HOOK_MEM_WRITE, self.write)

    def get(self, at):
        return struct.unpack('<I', self.uc.mem_read(at, 4))[0]

    def code(self, uc, at, size, _):
        need(any(a <= at and at+size <= b for a, b in RANGES), 'undeclared original instruction '+hex(at))
        need(bytes(uc.mem_read(at, size)) == self.raw[at-BASE:at-BASE+size], 'unchanged original instruction')
        need(self.raw[at-BASE] != 0xCC, 'original assertion/padding')
        self.instructions += 1
        self.code_hash.update(struct.pack('<I', at))
        if at == 0x56CE80:
            need(uc.reg_read(UC_X86_REG_EFLAGS) & 0x40, 'original debug stack check equality')
        if at in (0x4DA5F0, 0x4DFC20, 0x4E0A00, 0x56CEC0, 0x56CE80):
            sp = uc.reg_read(UC_X86_REG_ESP)
            argc = {0x4DA5F0:1, 0x4DFC20:2, 0x4E0A00:1, 0x56CEC0:3, 0x56CE80:0}[at]
            args = [self.get(sp+4+4*j) for j in range(argc)]
            self.entries.append(dict(entry=at, caller=self.get(sp), args=args, phase=self.phase))
            if at == 0x56CEC0:
                expected = [SCRATCH, 0, 48] if self.phase == 'profile' else [DESTINATION, 0, RECORD_BYTES]
                caller = 0x4DA63D if self.phase == 'profile' else 0x4DFC73
                need(args == expected and self.get(sp) == caller, 'exact original memset contract')
            if at == 0x4E0A00:
                need(args == [DESTINATION] and self.get(sp) == 0x4E08C8, 'exact original normalizer contract')

    def write(self, uc, access, at, size, value, _):
        owners = [(STACK, STACK+STACK_BYTES)]
        owners.append((SCRATCH, SCRATCH+48) if self.phase == 'profile' else (DESTINATION, DESTINATION+RECORD_BYTES))
        need(any(a <= at and at+size <= b for a, b in owners), 'record write outside current owner '+hex(at))
        pc = uc.reg_read(UC_X86_REG_EIP)
        data = (value & ((1 << (8*size))-1)).to_bytes(size, 'little')
        self.writes += 1
        self.write_hash.update(struct.pack('<III', pc, at, size)+data)
        if DESTINATION+0x1A <= at < DESTINATION+0x20:
            self.mp_writes.append(dict(pc=pc, offset=at-DESTINATION, bytes=size, value=value & ((1 << (8*size))-1)))

    def call(self, entry, args, phase):
        self.phase = phase
        sp = STACK+STACK_BYTES-0x1000
        self.uc.mem_write(sp, struct.pack('<'+'I'*(len(args)+1), RETURN, *args))
        self.uc.reg_write(UC_X86_REG_ESP, sp)
        self.uc.reg_write(UC_X86_REG_ECX, 0)
        start = self.instructions
        self.uc.emu_start(entry, RETURN, timeout=1_000_000, count=100_000)
        need(self.uc.reg_read(UC_X86_REG_EIP) == RETURN and self.uc.reg_read(UC_X86_REG_ESP) == sp+4,
             'complete original cdecl return and stack')
        return dict(entry=entry, args=args, convention='cdecl', instructions=self.instructions-start,
                    return_EIP=RETURN, return_ESP=sp+4)


def derive_target_record(job, source_path=SOURCE):
    """Execute original profile11 -> declared job1/3 -> complete B0 initializer."""
    need(type(job) is int and job in (1, 3), 'only declared terminal jobs1/3')
    raw = Path(source_path).read_bytes()
    m = _OriginalRecordMachine(raw)
    profile_call = m.call(0x4DA5F0, [11], 'profile')
    need(m.uc.reg_read(UC_X86_REG_EAX) == SCRATCH, 'original profile scratch return')
    original = bytes(m.uc.mem_read(SCRATCH, 48))
    need(struct.unpack_from('<2H', original) == (11, 9), 'original static character11/job9')
    profile = bytearray(original)
    struct.pack_into('<H', profile, 2, job)
    m.uc.mem_write(SCRATCH, bytes(profile))
    record_call = m.call(0x4DFC20, [SCRATCH, DESTINATION], 'record')
    record = bytes(m.uc.mem_read(DESTINATION, RECORD_BYTES))
    expected_mp = 3*profile[11]+profile[9]+profile[8]
    need(struct.unpack_from('<2h', record, 0x1A) == (expected_mp, expected_mp) == (238, 238), 'original MP from source attributes')
    need(any(w['pc'] == 0x4DFE3A and w['value'] == 238 for w in m.mp_writes) and
         any(w['pc'] == 0x4DFE48 and w['value'] == 238 for w in m.mp_writes), 'both original MP writers observed')
    need(bytes(m.uc.mem_read(SCRATCH, 48)) == bytes(profile), 'initializer retains declared source profile')
    image = bytes(m.uc.mem_read(BASE, len(raw)))
    p = SCRATCH-BASE
    need(image[:p] == raw[:p] and image[p+48:] == raw[p+48:], 'all other original image bytes retained')
    return dict(schema_version=1, job=job, identity=11, record_hex=record.hex(), record_sha256=sha(record),
                original_profile_hex=original.hex(), profile_hex=profile.hex(),
                profile_declarations=[dict(offset=2, bytes=2, field='job', before_hex=original[2:4].hex(),
                                           after_hex=bytes(profile[2:4]).hex(), source='explicit job1/job3 terminal experiment before original4DFC20')],
                source=dict(path=Path(source_path).resolve().as_posix(), bytes=len(raw), sha256=sha(raw),
                            character_va=CHARACTER, character_bytes=0x4A0,
                            character_sha256=sha(raw[CHARACTER-BASE:CHARACTER-BASE+0x4A0])),
                calls=[profile_call, record_call], original_entries=m.entries, MP_writes=m.mp_writes,
                trace=dict(instructions=m.instructions, writes=m.writes, code_sha256=m.code_hash.hexdigest(),
                           write_sha256=m.write_hash.hexdigest()),
                MP=list(struct.unpack_from('<3h', record, 0x1A)),
                original_CRT_instructions_executed=True, function_return_stubs=False,
                required_phase='fresh constructor before first original combat/binding root')


def report():
    raw = SOURCE.read_bytes()
    return dict(schema_version=1, accepted=False, kind='original_target_B0_initialization_before_declared_fields',
                cases=[derive_target_record(j) for j in (3, 1)],
                code=[dict(start=a, end=b, sha256=sha(raw[a-BASE:b-BASE])) for a, b in RANGES],
                recommended_target_spans=recommended_target_spans(),
                limits=['Static EXE character11 is job9; job1/3 is an explicit early input declaration.',
                        'No current school growth, actual scene loading or complete battle witness.',
                        'Unspecified source bytes remain, including attributes, level, engage maximum, timing, view, attack metadata and skills; they can change world decisions and regeneration.',
                        'Existing explicit declarations remain experiment inputs; no whole old zero B0 restore and no MP overrides.',
                        'Fresh constructor ordering and full world/terminal acceptance belong to the caller; old cumulative hashes cannot be reused.'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    out = ROOT / args.out
    need(not out.exists(), 'new small immutable diagnostic path')
    out.write_text(json.dumps(report(), ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')
    print(out, out.stat().st_size, sha(out.read_bytes()))
