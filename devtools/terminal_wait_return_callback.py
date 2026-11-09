"""Build/verify a bounded OWNED WOW64 helper, never attach to an original.

The callback overwrites ECX by the Windows WOW64 callback ABI. This probe can
verify the observed EAX/return PC/stack and restoration of callback-entry state;
it cannot establish the uninstrumented ECX or a complete original ABI.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parents[1]
SLOT = 2048
MAX_HITS = 8
STACK_MAX = 768
RECORD_START = 64
FX_OFFSET = 80
STACK_OFFSET = 592
ALLOCATION = 32768
POST_START = 20480
POST_SLOT = 1024
PRIMARY_SOURCES = [
    'https://github.com/wine-mirror/wine/blob/78e52205d9b9ac1c7e6f55fc613b882f1ad093d9/dlls/ntdll/tests/exception.c',
    'https://github.com/x64dbg/ScyllaHide/blob/baa5c8e853ace2bee752631f27fdfe5b271d92f6/HookLibrary/HookHelper.cpp',
    'https://github.com/ec-d/instrumentation-callback-x86/blob/b348e3291d161ac94c3f6da523229ef4716b7cf8/InstrumentationCallbackProxy.asm',
]



def need(value, message):
    if not value:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


class Asm:
    def __init__(self):
        self.code = bytearray()
        self.labels = {}
        self.branches = []
        self.patches = []

    def b(self, code):
        self.code.extend(bytes.fromhex(code))

    def imm(self, symbol, value, addend=0):
        self.patches.append(dict(offset=len(self.code), symbol=symbol, addend=addend))
        self.code.extend(struct.pack('<I', (value+addend) & 0xffffffff))

    def label(self, name):
        self.labels[name] = len(self.code)

    def branch(self, opcode, name):
        self.b(opcode)
        self.branches.append((len(self.code), name))
        self.code.extend(b'\0'*4)

    def finish(self):
        for pos, name in self.branches:
            struct.pack_into('<i', self.code, pos, self.labels[name]-pos-4)
        return bytes(self.code)


def _callback(record_base, target_tid, nt_return_pc, caller_return_pc=None):
    """No calls, TEB writes, exception instructions, floating-point arithmetic.

All changes occur after pushfd/pushad and are undone by popad/popfd. FXSAVE
reads the architectural FX state without changing it. Only the selected thread
can enter the record path, and that path makes no system or library calls.
"""
    a = Asm()
    a.b('9c 60 89 e5')                         # saved frame = EBP
    a.b('64 a1 24 00 00 00 3d'); a.imm('target_tid', target_tid)
    a.branch('0f 85', 'exit')
    a.b('8b 45 18 3d'); a.imm('nt_return_pc', nt_return_pc)
    a.branch('0f 85', 'exit')
    if caller_return_pc is not None:
        # Self-helper additionally filters the actual caller return on a bounded
        # original stack, so CLR/PInvoke waits on this same thread cannot count.
        a.b('8d 45 24 64 3b 05 08 00 00 00')
        a.branch('0f 82', 'exit')
        a.b('64 8b 15 04 00 00 00 29 c2')
        a.branch('0f 82', 'exit')
        a.b('83 fa 04'); a.branch('0f 82', 'exit')
        a.b('81 38'); a.imm('caller_return_pc', caller_return_pc)
        a.branch('0f 85', 'exit')
    a.b('a1'); a.imm('record_base', record_base)
    a.b('83 f8 08'); a.branch('0f 83', 'overflow')
    a.b('69 d0 00 08 00 00 81 c2'); a.imm('record_base', record_base, RECORD_START)
    a.b('89 02')                               # zero-based sequence
    a.b('64 a1 24 00 00 00 89 42 04')         # TID
    a.b('8b 45 18 89 42 08 8d 45 24 89 42 0c') # PC, original ESP
    a.b('64 a1 08 00 00 00 89 42 10')         # StackLimit
    a.b('64 a1 04 00 00 00 89 42 14')         # StackBase
    a.b('c7 42 18 00 00 00 00 c7 42 1c 00 00 00 00')
    a.b('0f ae 42 50')                         # fxsave [edx+80], 16-byte aligned
    a.b('fc 89 ee 8d 7a 20 b9 09 00 00 00 f3 a5') # copy saved frame
    a.b('8d 75 24 3b 72 10'); a.branch('0f 82', 'badstack')
    a.b('3b 72 14'); a.branch('0f 87', 'badstack')
    a.b('8b 4a 14 29 f1 81 f9 00 03 00 00')
    a.branch('0f 86', 'length')
    a.b('b9 00 03 00 00')
    a.label('length'); a.b('89 4a 18 8d ba 50 02 00 00 f3 a4')
    a.branch('e9', 'publish')
    a.label('badstack'); a.b('c7 42 1c 01 00 00 00 ff 05'); a.imm('record_base', record_base, 8)
    a.label('publish'); a.b('ff 05'); a.imm('record_base', record_base)
    a.branch('e9', 'exit')
    a.label('overflow'); a.b('c7 05'); a.imm('record_base', record_base, 4); a.b('01 00 00 00')
    a.label('exit'); a.b('61 9d ff e1')
    return a.finish(), a.patches


def emit_callback(record_base, target_tid, nt_return_pc, caller_return_pc=None):
    for value in (record_base, target_tid, nt_return_pc):
        need(0 <= value <= 0xffffffff, '32-bit callback parameter')
    need(record_base % 16 == 0, 'FXSAVE alignment')
    return _callback(record_base, target_tid, nt_return_pc, caller_return_pc)[0]


def build_image():
    callback, patches = _callback(0, 0, 0, 0)
    image = bytearray(callback)
    image.extend(b'\x90'*(-len(image) % 16))
    wrapper_offset = len(image)
    a = Asm()
    # stdcall wrapper(handle, LARGE_INTEGER*); only pushes before native call.
    a.b('ff 74 24 08 6a 00 ff 74 24 0c b8'); a.imm('nt_wait', 0)
    a.b('ff d0')
    postcall = len(a.code)
    a.b('9c 60 89 e5 a1'); a.imm('record_base', 0, 12)
    a.b('83 f8 04'); a.branch('0f 83', 'overflow')
    a.b('69 d0 00 04 00 00 81 c2'); a.imm('record_base', 0, POST_START)
    a.b('0f ae 42 50 fc 89 ee 8d 7a 20 b9 09 00 00 00 f3 a5')
    a.b('ff 05'); a.imm('record_base', 0, 12)
    a.branch('e9', 'exit')
    a.label('overflow'); a.b('c7 05'); a.imm('record_base', 0, 16); a.b('01 00 00 00')
    a.label('exit'); a.b('61 9d c2 08 00')
    image.extend(a.finish())
    patches += [dict(x, offset=x['offset']+wrapper_offset) for x in a.patches]
    return bytes(image), dict(callback_size=len(callback), wrapper_offset=wrapper_offset,
        wrapper_postcall_offset=wrapper_offset+postcall, patches=patches,
        slot=SLOT, max_hits=MAX_HITS, stack_max=STACK_MAX, allocation=ALLOCATION)


def audit_image(image, metadata):
    import capstone
    cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
    instructions = list(cs.disasm(image, 0))
    need(sum(i.size for i in instructions) == len(image), 'complete machine-code decoding')
    starts = {i.address for i in instructions}
    callback = [i for i in instructions if i.address < metadata['callback_size']]
    need(callback[0].mnemonic == 'pushfd' and callback[1].mnemonic == 'pushal', 'flags first')
    need([i.mnemonic for i in callback[-3:]] == ['popal', 'popfd', 'jmp'], 'restore all then jump ECX')
    need(callback[-1].op_str == 'ecx', 'natural callback continuation')
    for i in callback:
        need(i.mnemonic not in ('call', 'ret', 'int', 'int3', 'sysenter', 'syscall', 'fxrstor'), 'no native or trapping callback operation')
        if i.mnemonic.startswith('j') and i.op_str != 'ecx':
            need(int(i.op_str, 16) in starts, 'branch to instruction boundary')
        if 'fs:' in i.op_str:
            need(i.mnemonic in ('mov','cmp') and i.op_str.split(', ')[0] in ('eax','edx'), 'TEB reads only')
    return [dict(offset=i.address, hex=i.bytes.hex(), mnemonic=i.mnemonic, operands=i.op_str) for i in instructions]


def prepare(directory):
    directory = Path(directory)
    need(not directory.exists(), 'new output directory')
    image, metadata = build_image()
    metadata['instructions'] = audit_image(image, metadata)
    metadata['template_sha256'] = sha(image)
    metadata['primary_sources'] = PRIMARY_SOURCES
    source = Path(__file__).with_suffix('.cs').read_bytes()
    metadata['source_sha256'] = sha(source)
    metadata['generator_sha256'] = sha(Path(__file__).read_bytes())
    directory.mkdir(parents=True)
    (directory/'callback.bin').write_bytes(image)
    (directory/'manifest.json').write_text(json.dumps(metadata, indent=2), encoding='utf-8')
    (directory/'terminal_wait_return_callback.cs').write_bytes(source)
    return metadata


def u32(data, offset):
    return struct.unpack_from('<I', data, offset)[0]


def verify(report):
    need(report['kind'] == 'owned_wow64_wait_callback_preflight', 'only self-helper evidence')
    for name in ('accepted', 'full_original_abi', 'uninstrumented_ecx_observed', 'original_program_observed'):
        need(report.get(name) is False, 'must not upgrade scope: '+name)
    need(report['error'] is None and report['cleanup_errors'] == [], 'successful bounded cleanup')
    need(report['registration_status'] == 0 and report['unregistration_status'] == 0, 'actual registration and removal')
    need(report['wow64'] is True and report['pointer_size'] == 4, 'real WOW64 helper')
    need(report['peer_completed'] is True and report['peer_signals'] == 3 and report['peer_error'] is None, 'three real controlled signals')
    need(report['callback_overwrites_ecx'] is True, 'scope acknowledges Windows ECX overwrite')
    need(report['returns'] == [0, 0, 0, 0x102], 'three success and one nonsignaled timeout')
    before = bytes.fromhex(report['nt_wait_before'])
    need(before == bytes.fromhex(report['nt_wait_after']), 'original syscall stub unchanged')
    need(len(before) == 32 and before[:1] == b'\xb8' and before[5] == 0xba
         and before[10:15] == bytes.fromhex('ffd2c20c00'), 'fixed NtWait+12 calling sequence')
    image, metadata = build_image()
    patched = bytearray(image)
    values = dict(record_base=report['record_base'], target_tid=report['target_tid'],
                  nt_wait=report['nt_wait'], nt_return_pc=report['nt_wait']+12,
                  caller_return_pc=report['code_base']+metadata['wrapper_postcall_offset'])
    for p in metadata['patches']:
        struct.pack_into('<I', patched, p['offset'], values[p['symbol']]+p['addend'])
    need(bytes(patched).hex() == report['code_before'] == report['code_after'], 'only known owned code and relocations')
    need(report['source_sha256'] == sha(Path(__file__).with_suffix('.cs').read_bytes()), 'current frozen source')
    need(report['template_sha256'] == sha(image), 'current exact machine-code template')
    need(report['code_protection'] == 'PAGE_EXECUTE_READ' and report['record_protection'] == 'PAGE_READWRITE', 'separate RX/RW allocations')
    data = bytes.fromhex(report['records_hex'])
    need(len(data) == ALLOCATION, 'bounded complete allocation')
    need([u32(data, x) for x in (0,4,8,12,16)] == [4,0,0,4,0], 'exact callback and return counts; no overflow/bounds error')
    for k, status in enumerate(report['returns']):
        start = RECORD_START+k*SLOT
        record = data[start:start+SLOT]
        need([u32(record,x) for x in (0,4,8,28)] == [k,report['target_tid'],report['nt_wait']+12,0], 'ordered identity and original return PC')
        sp, low, high, length = [u32(record,x) for x in (12,16,20,24)]
        need(low <= sp <= high and length == min(STACK_MAX,high-sp) and length >= 16, 'bounded original stack')
        frame = record[32:68]
        need(u32(frame,24) == report['nt_wait']+12 and u32(frame,28) == status and u32(frame,12)+4 == sp, 'real EAX, callback ECX and ESP')
        stack = record[STACK_OFFSET:STACK_OFFSET+length]
        need([u32(stack,x) for x in (0,4,8,12)] == [report['code_base']+metadata['wrapper_postcall_offset'],report['event_handle'],0,report['timeout_pointer']], 'original native wait arguments and actual caller return')
        post = data[POST_START+k*POST_SLOT:POST_START+(k+1)*POST_SLOT]
        for offset in range(0,36,4):
            need(u32(post,32+offset) == u32(frame,offset)+(16 if offset == 12 else 0), 'callback-entry GPR/flags restored through native RET')
        need(record[FX_OFFSET:FX_OFFSET+512] == post[FX_OFFSET:FX_OFFSET+512], 'FX state preserved until actual native RET')
    need(report['buffers_released'] and report['handles_closed'] and report['watchdog_disarmed'], 'normal cleanup')
    return dict(accepted=False, self_helper_preflight_passed=True, observed_wait_returns=4,
        success_returns=3, timeout_returns=1, full_original_abi=False,
        uninstrumented_ecx_observed=False, original_program_observed=False,
        callback_entry_state_restored=True, maximum_stack_bytes=STACK_MAX)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='command', required=True)
    sub.add_parser('prepare').add_argument('--out', type=Path, required=True)
    sub.add_parser('verify').add_argument('report', type=Path)
    args = p.parse_args()
    if args.command == 'prepare':
        m = prepare(args.out)
        print(json.dumps(dict(output=str(args.out), code_bytes=len(build_image()[0]), template_sha256=m['template_sha256'])))
    else:
        print(json.dumps(verify(json.loads(args.report.read_text(encoding='utf-8-sig'))), indent=2))
