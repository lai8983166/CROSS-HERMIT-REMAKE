"""Bounded, read-only audit of the retained guest kernel's user #DB route.

No debugger connection, guest input, kernel patch, or acceptance decision.
RVA labels were resolved from the retained local PDB with DbgHelp; this audit
independently requires the fixed original image hash and exact branch bytes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import capstone
import pefile

ROOT = Path(__file__).resolve().parents[1]
KERNEL = ROOT / '.venv-audit/native-worker/guest-ntoskrnl.exe'
SHA = '5669b9b8bfcf20f08b7d1d65dc2deccbf836279c0e3f66722d72ad33ee7f672a'


def audit(path: Path) -> dict:
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != SHA:
        raise ValueError('fixed guest kernel identity required')
    pe = pefile.PE(data=raw)
    expected = {
        0x2ebee0: '488b8178050000c3',  # PsGetProcessDebugPort
        0x2a6af4: '4883ba7805000000',  # current process DebugPort
        0x2a6afc: '7512',              # nonzero -> trap-class gate
        0x2a6afe: '803deb3a9a0000',    # KdIgnoreUmExceptions
        0x2a6b10: '84c07428',          # not special KD trap -> forward
        0x2a6b4d: 'e832384a00',        # DbgkForwardException
        0xa440f2: '3d03000080',        # STATUS_BREAKPOINT
        0xa440f9: '3d1f000040',        # STATUS_WX86_BREAKPOINT
        0xa44100: '32c0c3',            # otherwise false
    }
    for rva, hex_bytes in expected.items():
        value = bytes.fromhex(hex_bytes)
        if pe.get_data(rva, len(value)) != value:
            raise ValueError(f'branch-byte disagreement at {rva:x}')
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    excerpts = []
    for start, end in [(0x2ebee0, 0x2ebee8), (0x2a6a82, 0x2a6b5a),
                       (0xa440f0, 0xa44114), (0x2a7424, 0x2a7453)]:
        data = pe.get_data(start, end - start)
        decoded = list(md.disasm(data, start))
        if sum(i.size for i in decoded) != len(data):
            raise ValueError('bounded excerpt did not decode completely')
        excerpts.append({'start_rva': start, 'end_rva': end,
                         'hex': data.hex(), 'instructions': [
                             {'rva': i.address, 'hex': i.bytes.hex(),
                              'mnemonic': i.mnemonic, 'operands': i.op_str}
                             for i in decoded]})
    return {
        'kind': 'guest_kernel_kd_user_db_static_refusal_v1',
        'accepted': False, 'native_test_performed': False,
        'kernel': {'path': str(path), 'bytes': len(raw), 'sha256': SHA},
        'symbols': {'KiDispatchException': 0x2a66f0, 'KdTrap': 0x2a7424,
                    'KdIsThisAKdTrap': 0xa440f0, 'KdIgnoreUmExceptions': 0xc4a5f0,
                    'DbgkForwardException': 0x74a384,
                    'PsGetProcessDebugPort': 0x2ebee0},
        'static_checks': {hex(k): v for k, v in expected.items()},
        'excerpts': excerpts,
        'preconditions': ['user-mode first-chance ordinary hardware execution #DB',
                          'current process retains the original non-null DebugPort',
                          'ordinary kernel exception path, no synthetic KD service record'],
        'route': [
            'WOW64 compatibility CS may remap STATUS_SINGLE_STEP 0x80000004 to '
            'STATUS_WX86_SINGLE_STEP 0x4000001e; neither is a special KD service.',
            'KdIsThisAKdTrap accepts only 0x80000003 or 0x4000001f with nonzero '
            'NumberParameters and ExceptionInformation[0]; ordinary #DB returns false.',
            'Non-null EPROCESS.DebugPort (+0x578) branches past the '
            'KdIgnoreUmExceptions check; false special-trap result skips KdTrap.',
            'DbgkForwardException receives DebugPort=true and SecondChance=false. '
            'The original user debugger handles this event before KD can observe it '
            'through the requested user-address breakpoint mechanism.',
        ],
        'standard_configuration_can_preempt_existing_debugport': False,
        'candidate': 'reject KD ba e1 at user NtWait boundary under these preconditions',
        'reason': 'kdbgctrl -eu / clearing ignore-user-exceptions does not override '
                  'the earlier DebugPort branch. Debugger exception filters act on '
                  'delivered events and cannot move this kernel dispatch branch.',
        'limits': [
            'This rejects the specified user-address hardware-breakpoint route, '
            'not every possible kernel observation design.',
            'A kernel breakpoint in exception dispatch can observe the later '
            'kernel frame but ordinary continuation still forwards the original '
            '#DB; swallowing it requires additional semantic intervention.',
            'A syscall kernel boundary is a different stop point. No claim that '
            'it exposes the full original x86 state at the required WOW64 user return.',
            'No VMX/BCD change, KD connection, original-parent reply alteration, '
            'kernel write, user breakpoint, or guest execution was performed.',
        ],
        'sources': [
            'https://learn.microsoft.com/en-us/windows-hardware/drivers/debugger/user-space-and-system-space',
            'https://learn.microsoft.com/en-us/windows-hardware/drivers/debugger/using-kdbgctrl',
            'https://learn.microsoft.com/en-us/windows-hardware/drivers/debugger/enabling-postmortem-debugging',
        ],
    }


def kernel_boundary_audit(path: Path) -> dict:
    result = audit(path)
    pe = pefile.PE(data=path.read_bytes())
    checks = {
        0x2a69b4: '448a4500', 0x2a69bb: '7567',
        0x2a69dc: 'e8430a0000',  # kernel-mode path invokes KdTrap
        0x6fcc6a: '4883c438', 0x6fcc6e: 'c3',
        0x428c33: 'ffd0', 0x428c35: '0f1f00',
        0x428c40: '488b9dc0000000',
        0x4289fb: '807b0300', 0x428a1d: 'f6430324',
        0x428e70: '33d2', 0x428e72: '660fefc0',
        0x428e8a: '488b8de8000000', 0x428e91: '4c8b9df8000000',
        0x428ec0: '0f01f8', 0x428ec3: '480f07',
    }
    for rva, value in checks.items():
        if pe.get_data(rva, len(bytes.fromhex(value))) != bytes.fromhex(value):
            raise ValueError(f'kernel boundary changed at {rva:x}')
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    excerpts = []
    for start, end in [(0x2a69b4, 0x2a69e9), (0x6fcc00, 0x6fcc6f),
                       (0x428780, 0x42880b), (0x4289da, 0x428a43),
                       (0x428c30, 0x428c6b), (0x428e5e, 0x428ec6)]:
        data = pe.get_data(start, end - start)
        rows = list(md.disasm(data, start))
        if sum(i.size for i in rows) != len(data):
            raise ValueError('incomplete boundary decode')
        excerpts.append({'start_rva': start, 'end_rva': end, 'hex': data.hex(),
                         'instructions': [
                             {'rva': i.address, 'hex': i.bytes.hex(),
                              'mnemonic': i.mnemonic, 'operands': i.op_str}
                             for i in rows]})
    return {
        'kind': 'guest_kernel_wait_boundary_static_candidate_v1',
        'accepted': False, 'native_test_performed': False,
        'kernel': result['kernel'],
        'static_checks': {hex(k): v for k, v in checks.items()},
        'excerpts': excerpts,
        'candidate': 'kernel-only NtWait return breakpoint, bounded development preflight only',
        'distinct_from_rejected_user_db': True,
        'dispatch_reason': 'The #DB instruction executes at kernel CPL. '
                           'KiDispatchException PreviousMode==0 invokes KdTrap '
                           'before user-mode DebugPort dispatch. The syscall caller '
                           'being user mode does not make the breakpoint exception user mode.',
        'boundaries': {
            'NtWaitForSingleObject_entry': 0x6fcc00,
            'NtWaitForSingleObject_return_epilogue': 0x6fcc6a,
            'NtWaitForSingleObject_ret': 0x6fcc6e,
            'normal_service_indirect_call_return': 0x428c35,
            'shared_KiSystemServiceExit': 0x428c40,
            'normal_tail_load_user_rip_to_rcx': 0x428e8a,
            'normal_tail_load_user_eflags_to_r11': 0x428e91,
            'normal_swapgs': 0x428ec0,
            'normal_sysretq': 0x428ec3,
            'shadow_tail_branch_target': 0xa8adc0,
            'alternative_iretq': 0x42908b,
        },
        'preflight_limit': 'A stop at the NtWait epilogue may test KD dispatch, '
                           'thread/process filtering and ordinary continuation. '
                           'Do not use the post-swapgs/pre-sysret window as the '
                           'initial probe; active GS/address-space state differs there.',
        'required_filter': ['actual module relocation and exact original bytes',
                            'current target EPROCESS and ETHREAD/TID',
                            'user-origin syscall frame and expected user return RIP',
                            'matched entry/return of this NtWait call and process lifetime'],
        'frame_limits': [
            'Original syscall prologue establishes RBP=trap-frame base+0x80; '
            'user RIP/CS/EFLAGS/RSP/SS therefore occur at RBP+0xe8/0xf0/0xf8/0x100/0x108.',
            'Syscall trap RAX initially holds the syscall number. At the wait '
            'epilogue the true return value is in live kernel RAX; trap RAX '
            'must not be assumed current.',
            'XMM0..5 are saved only on conditional syscall paths. Existence '
            'of trap-frame fields does not establish valid bytes in those fields.',
            'The common fast exit explicitly zeros RDX and XMM0..5, reloads '
            'MXCSR, and changes volatile registers; wait epilogue values are '
            'not user-return poststate.',
            'A KTRAP_FRAME alone contains neither x87/FPCW/FPSW/FPTAG/FIP/FDP/'
            'FCS/FDS/FOP nor XMM6..15 or R12..15. Full processor context and '
            'thread xstate ownership, valid bits, save format and refresh '
            'timing remain unproved.',
            'Kernel breakpoint handling creates another exception frame. '
            'The stopped kernel frame and original syscall user frame must '
            'be distinguished; KTHREAD.TrapFrame alone is not authority.',
        ],
        'unresolved': ['KD transport and all-vCPU coherent stop/resume',
                       'kernel execution breakpoint delivery without DR state loss',
                       'exact original kernel tail and selected SYSRET/IRET/shadow route',
                       'complete x87/XMM/control/descriptor/debug state capture',
                       'original WOW64 64-to-32 return bridge and contiguous instruction interval',
                       'original game/parent behavior, resources and fresh native lifetime'],
        'canonical57_supported': False, 'user_poststate_supported': False,
        'sources': result['sources'],
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--kernel', type=Path, default=KERNEL)
    parser.add_argument('--out', type=Path)
    parser.add_argument('--kernel-boundary', action='store_true')
    args = parser.parse_args()
    result = kernel_boundary_audit(args.kernel) if args.kernel_boundary else audit(args.kernel)
    if args.out:
        with args.out.open('x', encoding='utf-8') as f:
            json.dump(result, f, indent=2)
            f.write('\n')
    print(json.dumps({'candidate': result['candidate'], 'accepted': False,
                      'checked_original_branches': len(result['static_checks'])}))
