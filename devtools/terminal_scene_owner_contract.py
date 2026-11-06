"""Read-only original scene owner/TLS and user-retreat contract (no native calls).

Run with the audit Python; --out must name a new report. This only reads the
unpacked original image, four small implementation files and a local OS DLL.
Offsets in the OS section apply to the authenticated local DLL, not all Windows.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import struct
from pathlib import Path

from capstone import Cs, CS_ARCH_X86, CS_MODE_32
import pefile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "analysis/hermit_game.exe"
SOURCE_SHA = "588b4288e4c737dc489d2b9bc0652cca85e3d668b1784942ef4b4bda916f1005"
KERNELBASE_SHA = "dd98f0129317fe0c3fbebe79980361a27480564bb8b61cbc09a329a17c43cfec"
RANGES = (
    ("factory_and_constructor", 0x451080, 0x451470),
    ("beginthreadex_and_wrapper", 0x56E050, 0x56E221),
    ("worker", 0x421F50, 0x422090),
    ("forced_task_cancellation", 0x422090, 0x422290),
    ("wait_and_self_end", 0x422360, 0x422560),
    ("scheduler", 0x421850, 0x421BF0),
    ("manager_cancellation", 0x421BF0, 0x421C64),
    ("callback", 0x451670, 0x4519A3),
    ("scene_dispatch", 0x451A60, 0x451B10),
    ("ordinary_loop", 0x4539B0, 0x453CFC),
    ("retreat_dispatch", 0x453D00, 0x453E04),
    ("retreat_request", 0x458580, 0x4586C7),
    ("retreat_confirmation", 0x4586D0, 0x4587C4),
    ("retreat_hit_test", 0x458800, 0x458929),
    ("retreat_gate_global", 0x456B20, 0x456B58),
    ("retreat_gate_script", 0x454C40, 0x454C7A),
    ("retreat_gate_panel", 0x4577F0, 0x45782B),
    ("retreat_original_caller", 0x46B590, 0x46B618),
    ("keyboard_query", 0x4128F0, 0x412A10),
)


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def region(md, raw, start, end, base=0x400000):
    data = raw[start - base:end - base]
    need(len(data) == end - start, "source range bounds")
    instructions = list(md.disasm(data, start))
    need(sum(i.size for i in instructions) == len(data), "complete bounded decoding " + hex(start))
    return dict(start=hex(start), end_exclusive=hex(end), bytes=len(data),
                sha256=sha(data), hex=data.hex(),
                instructions=[dict(va=hex(i.address), hex=i.bytes.hex(),
                                   mnemonic=i.mnemonic, operands=i.op_str)
                              for i in instructions])


def build():
    raw = SOURCE.read_bytes()
    need(len(raw) == 5980160 and sha(raw) == SOURCE_SHA, "original source identity")
    md = Cs(CS_ARCH_X86, CS_MODE_32)
    checks = {
        0x56E141: ("call", "dword ptr [0x5921a8]"),
        0x56E15E: ("mov", "dword ptr [edx], eax"),
        0x421F88: ("call", "dword ptr [eax]"),
        0x4516D0: ("call", "0x422360"),
        0x453CB0: ("call", "0x422360"),
        0x453CB5: ("cmp", "dword ptr [ebp - 8], 0"),
        0x453C2F: ("call", "0x453d00"),
        0x4586A5: ("mov", "byte ptr [eax + 0x30], 1"),
        0x453DC9: ("mov", "byte ptr [eax + 0x31], 1"),
        0x4517D6: ("call", "0x439e30"),
        0x4519A0: ("ret", "4"),
        0x4220DD: ("call", "dword ptr [0x592260]"),
        0x421C48: ("call", "0x422090"),
        0x46B5D1: ("call", "0x458580"),
    }
    checked = []
    for at, expected in checks.items():
        instruction = next(md.disasm(raw[at - 0x400000:at - 0x400000 + 16], at))
        need((instruction.mnemonic, instruction.op_str) == expected, "instruction contract " + hex(at))
        checked.append(dict(va=hex(at), hex=instruction.bytes.hex(), mnemonic=instruction.mnemonic,
                            operands=instruction.op_str))
    rectangles = struct.unpack_from("<8h", raw, 0x60CB18 - 0x400000)
    need(rectangles == (27, 52, 103, 28, 140, 52, 102, 28), "confirmation rectangles")
    keyboard_table = struct.unpack_from("<5I", raw, 0x412A10 - 0x400000)
    need(keyboard_table[1] == 0x412957, "mode 1 keyboard source")
    os_path = Path("C:/Windows/SysWOW64/kernelbase.dll")
    os_raw = os_path.read_bytes()
    need(sha(os_raw) == KERNELBASE_SHA, "current OS DLL changed; derive TLS layout again")
    pe = pefile.PE(data=os_raw)
    export = next(x for x in pe.DIRECTORY_ENTRY_EXPORT.symbols if x.name == b"TlsGetValue")
    need(export.address == 0x12AA60 and export.forwarder is None, "local TlsGetValue export")
    tls_code = pe.get_data(export.address, 0x4A)
    need(bytes.fromhex("648b0d18000000") in tls_code, "TlsGetValue FS self")
    need(bytes.fromhex("8b8481100e0000") in tls_code, "TlsGetValue fixed slots")
    need(bytes.fromhex("8b89940f0000") in tls_code, "TlsGetValue expansion pointer")
    implementation_files = ["tools/school_native_scene.py", "tools/school_scene_bootstrap.py",
                            "tools/school_scheduler_lifetime.py", "tools/school_startup_lifetime.py"]
    reviewed = []
    for name in implementation_files:
        data = (ROOT / name).read_bytes()
        reviewed.append(dict(path=name, bytes=len(data), sha256=sha(data)))
    return dict(
        schema_version=1,
        scope="static original bytes and authenticated local OS implementation; no process executed or observed",
        original_source=dict(path=str(SOURCE), bytes=len(raw), sha256=sha(raw),
                             address_translation="file_offset = original_VA - 0x400000"),
        reviewed_implementations=reviewed,
        checked_instructions=checked,
        ranges=[dict(name=name, **region(md, raw, lo, hi)) for name, lo, hi in RANGES],
        local_tls_implementation=dict(path=str(os_path), bytes=len(os_raw), sha256=sha(os_raw),
            export="TlsGetValue", export_RVA=hex(export.address), image_base=hex(pe.OPTIONAL_HEADER.ImageBase),
            code=region(md, tls_code, export.address, export.address+len(tls_code), export.address),
            fixed_slots_offset="0xe10", fixed_slot_count=64,
            expansion_pointer_offset="0xf94", expansion_index="index - 64", total_index_limit=1088,
            live_target_authentication_required=True,
            portability="These offsets are derived from this exact local 32-bit DLL. Authenticate the target mapped module/export and live instructions before use; reject a mismatch."),
        observation_contract=observation_contract(),
        user_retreat_contract=retreat_contract(rectangles),
        limitations=[
            "No native evidence was generated; all execution/ownership/exit claims remain false.",
            "An EBP ancestor proves an active call chain, not every intervening instruction or successful WinAPI return.",
            "The original wait ignores WAIT_FAILED. A later caller frame alone cannot certify WAIT_OBJECT_0.",
            "OS stack/TEB layouts are version-sensitive and must be authenticated and cross-checked.",
            "The retreat branch is separate from retained neutral/timeout cases and cannot satisfy their full replay obligations.",
            "A dead thread, WM_CLOSE, exit code 0 or resource disappearance does not establish natural callback/CRT cleanup.",
        ],
        execution_claims=dict(native_process_started=False, current_scene_owner_proved=False,
            successful_wait_proved=False, callback_natural_return_proved=False,
            CRT_normal_cleanup_proved=False, scheduler_reclaim_proved=False,
            successor_consumption_proved=False, full_acceptance=False),
        official_sources={
            "selector": "https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-wow64getthreadselectorentry",
            "descriptor": "https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-wow64_ldt_entry",
            "TEB_layout_warning": "https://learn.microsoft.com/en-us/windows/win32/api/winternl/ns-winternl-teb",
            "thread_owner": "https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-getprocessidofthread",
            "duplicate_handle": "https://learn.microsoft.com/en-us/windows/win32/api/handleapi/nf-handleapi-duplicatehandle",
            "TLS_semantics": "https://learn.microsoft.com/en-us/windows/win32/procthread/using-thread-local-storage",
        },
    )


def observation_contract():
    return dict(
        roots="Same owned original process: 4E1B60; 4DA860(scene 76 or 77); 439E30(actual MAIN+10,16). MAIN consumes event through 49E39E ->451080 ->451170 and original scheduler.",
        node_fields={"+00": "vtable 59A430, [vtable]=451670, [vtable+4]=451630",
                     "+04": "flags: bit1 active, bit2 disabled, bit4 done, bit10000 yielded",
                     "+08": "manager; require actual MAIN+64", "+0C": "linked next",
                     "+14": "yield delay", "+18": "callback argument",
                     "+1C": "original node event", "+20": "original CRT worker thread handle",
                     "+24": "original worker thread ID", "+28": "auto-delete flag"},
        manager_fields={"+000..+0FF": "32 bucket heads, 8-byte stride; traverse safely and require node membership",
                        "+100": "original CRITICAL_SECTION, 24 bytes on target x86", "+118": "original manager event"},
        native_snapshot_steps=[
            "Use only the already-owned process/job and HWND owner. Authenticate live original ranges and actual loaded OS module/export, recording PID and module bases.",
            "Duplicate node+20 from that process with DUPLICATE_SAME_ACCESS, never DUPLICATE_CLOSE_SOURCE. GetThreadId must equal node+24; GetProcessIdOfThread must equal actual owner PID. Keep duplicate until observation completes; close it normally.",
            "Suspend the actual worker and relevant MAIN thread briefly using owned handles; record suspension return counts and restore only the increments this observer made. Read full WOW64_CONTEXT and coherent node/manager/stack bytes while stopped.",
            "Use worker context SegFs with Wow64GetThreadSelectorEntry from a 64-bit observer (32-bit observer uses GetThreadSelectorEntry). Check nonzero API success and descriptor present/data properties; derive base = BaseLow | BaseMid<<16 | BaseHi<<24.",
            "Cross-check 32-bit NT_TIB Self at +18 equals selector base, StackLimit(+8)<=ESP<StackBase(+4), ClientID process(+20)/thread(+24) equal actual owner/worker. These are version-bound checks, not evidence that arbitrary TEB64+0 is valid.",
            "Read original TLS index at 761BC0. Require 0<=index<1088 for this authenticated implementation. For index<64, slot=TEB32+E10+4*index; otherwise require nonzero pointer[TEB32+F94] and slot=pointer+4*(index-64). Never use TEB+2C ThreadLocalStoragePointer as dynamic TlsSlots.",
            "Read pointer[slot], require a readable nonzero PTD and capture all 116 bytes. Validate PTD+0==worker ID, PTD+48==421F50, PTD+4C==node; preserve all remaining PTD bytes rather than synthesize defaults.",
            "Walk only bounded readable stack frames within NT_TIB stack limits. Worker frame return56E183 should contain node at frame+8; its saved EBP is CRT wrapper frame, whose argument at saved_EBP+8 must equal TLS PTD. Callback frame return421F8A and wait ancestor4516D5/453CB5 bind the same worker/node execution.",
            "Read node+1C and manager+118 from the same coherent process snapshot and optionally duplicate them from that same handle table. Duplicates are observation references only: do not SetEvent/ResetEvent or wait on auto-reset event handles, which would alter/consume the original handshake.",
            "Record exact remote memory spans and bytes plus full CPU/context; snapshot cannot claim full-process memory/permissions or an instruction/API trace unless separately collected.",
        ],
        ptd_initial_fields={"size": 116, "+00": "actual worker ID written 56E15E after GetCurrentThreadId",
                            "+04": "FFFFFFFF initialization", "+14": "1 initialization",
                            "+48": "421F50", "+4C": "node", "+50": "761D68 initialization"},
        crt_contract="56E110 receives allocated PTD, TlsSetValue([761BC0],PTD) at56E141, writes current tid at56E15E, invokes PTD+48 with PTD+4C at56E180. A helper thread calling TlsGetValue reads its own TLS and is not a remote worker observation.",
        wait_contract="4223A8 EnterCriticalSection(manager+100);4223BE ResetEvent(node+1C);4223D7 SetEvent(manager+118);4223EF LeaveCriticalSection;422407 WaitForSingleObject(node+1C,INFINITE), return42240D. Both API success and original peer scheduler wake must be evidenced independently of function return.",
        normal_exit_contract=[
            "Observe actual 451670 ret4 at4519A0 returning421F8A after its result branch and tail, not a remote independent callback invocation.",
            "Original worker clears flags, sets done4, resets node event, sets manager event, leaves lock and invokes _endthreadex(0) at422021.",
            "Original _endthreadex56E1E0 calls5753B0/575450, releases nested PTD allocations and PTD, clears TLS via TlsSetValue and calls ExitThread at56E21B. A prior 116B PTD snapshot is not proof these happened.",
            "Original manager observes done4, sees GetExitCodeThread !=STILL_ACTIVE, closes node event, clears/unlinks and runs derived destructor/free as configured. Retain worker duplicate to observe signaled thread; verify object ownership before supplemental handle cleanup.",
            "Original thread handle+20 leak requires separately identified supplemental CloseHandle after actual worker exit. Original event/destructor/manager cleanup must not be replaced by observer cleanup.",
            "Observe published successor event and its MAIN consumption; queued event alone is incomplete. Full state/ABI/memory/permissions/cumulative original trace, fresh cases and independent replay remain separate obligations.",
        ],
    )


def retreat_contract(rectangles):
    return dict(
        status="Static viable ordinary-loop user-input path; no native execution tested here",
        actual_caller="46B5D1 calls458580 with ECX=controller[+117C38]; cross-check this equals published scene node",
        gates={"byte[7F4491]": "0", "node+43 and node+59": "not both nonzero",
               "dword[node+38]": "5", "byte[node+117F20]": "0",
               "controller+108B3A": "nonzero to reach ordinary caller block"},
        request="458580 takes ECX=node, no explicit business arguments. Reads original input, then4586A5 sets node+30=1. Do not call it as a fabricated-result API.",
        input_request_alternatives=[
            "Key query4128F0(key1,mode1), original keyboard byte at [7A49FC]+10B8+581 bit80. Same query cancels an already-open confirmation, so release before confirmation. Naming key1 Escape requires the actual input device/scan-code mapping contract.",
            "Original mouse current and stored press coordinates must both lie x9..88,y3..24 inclusive; game+19B8==3 and game+199C bit1. Candidate game-coordinate click(48,12); use real current HWND/client scaling and original input acquisition, not memory writes.",
        ],
        confirmation_origin=[377, 324],
        confirmation_rectangles_raw=list(rectangles),
        selection0_cancel_open_bounds=[404, 376, 507, 404],
        selection1_confirm_open_bounds=[517, 376, 619, 404],
        confirmation="At node+30==1,453D87 calls4586D0(node,377,324). 458800 hit-tests mouse. Selection1 plus game+199C bit1 returns2 at458756. Candidate game-coordinate click(568,390), separately pressed/released after the request. Observe original input updates; do not set game fields.",
        result="453DBC writes5FF720=-1;453DC9 writesnode+31=1;453DCD sets local result1. 453C34 preserves it in outer frame[EBP-8], original waits return at453CB5/453CD3/453CDD, then4539B0 returns1 at453CFB.",
        callback_tail="451716 consumes nonzero, ten451753 waits, controller cleanup465E60, completion4DB270 with451791 waits; node+31==1 chooses4517A9..4517DB and publishes MAIN event1 at4517D6, then4519A0 returns to421F8A.",
        safe_execution_proposal=[
            "First prove real owner/PTD and naturally reached ordinary ready scene gates without modifying them. During initialization no cooperative abort API has been established.",
            "Use a declared owned-window real input action, bounded by current focus/coordinate checks and release all injected downs on failure. Input changes belong to a separate retreat case, not retained neutral/timeout semantics.",
            "Wait for observed original node+30=1 before a separate confirm click; retain exact input receipt and before/after game input fields. If gates never become ready, report the specific gate; do not clear it.",
            "Observe saved result, post-wait caller, natural tail, worker/PTD cleanup, manager reclaim and event1 consumption. Stop within bounded budget if any dependency is unresolved.",
        ],
        rejected_shortcuts={
            "422090": "Forced cancellation: calls TerminateThread at4220DD, polls exit, closes/unlinks; not cooperative CRT cleanup.",
            "422120": "Not an instruction boundary/function entry: inside immediate of42211E mov ecx,1.",
            "421BF0": "Manager-wide cancellation loop invokes422090 at421C48; WM_CLOSE cannot certify callback natural return.",
            "422440": "Self-end helper invokes _endthreadex; not451670 normal return and must not be remotely called on another thread.",
            "direct453D00_or4586D0": "Independent remote invocation returns to the bridge, not original worker4539B0; no substitute for its real input-driven call chain.",
        },
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    need(not args.out.exists(), "immutable output already exists")
    result = build()
    data = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    need(len(data) < 1024 * 1024, "static evidence budget")
    with args.out.open("xb") as stream:
        stream.write(data)
    print(json.dumps(dict(path=str(args.out), bytes=len(data), sha256=sha(data),
                          checks=len(result["checked_instructions"]), native_executed=False)))


if __name__ == "__main__":
    main()
