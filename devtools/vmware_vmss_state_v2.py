"""Version 2: observed VMSS v2 and VMSN v3 CPU containers; no native I/O.

Both observed profiles use the bounded parser's 64-bit extended tag lengths.
The original header and report must agree; the header reserved field is retained
without assigning it undocumented meaning. Register semantics remain unchanged.

VMware mapping anchors are recorded in the accompanying mapping audit. FXSAVE
common fields follow Intel SDM vol.2A FXSAVE tables; FP0..7 are physical registers
as in Unicorn 2.1.4. Unknown pointer format is an explicit gap, never guessed.
"""
from __future__ import annotations

import hashlib
import io
import struct

from devtools.vmware_vmss_cpu_v2 import parse_cpu_groups, CheckpointError

GP_NAMES = "rax rcx rdx rbx rsp rbp rsi rdi r8 r9 r10 r11 r12 r13 r14 r15".split()
SEG_NAMES = "ES CS SS DS FS GS LDTR TR".split()
CANONICAL_NAMES = ("EAX EBX ECX EDX ESI EDI EBP ESP EIP EFLAGS FPCW FPSW FPTAG "
                   "FIP FDP FCS FDS FOP MXCSR CS DS ES FS GS SS CR0 CR2 CR3 CR4 GDTR IDTR LDTR TR").split()
CANONICAL_NAMES += [f"FP{i}" for i in range(8)] + [f"XMM{i}" for i in range(8)] + [f"DR{i}" for i in range(8)]


def decode_fxsave(raw: bytes, *, pointer_format: str | None = None) -> dict:
    """Decode 512-byte architectural FXSAVE common fields and optional pointers.

    pointer_format is explicitly 'legacy32', 'fxsave64', or unknown (None).
    fxsave64 has no selector fields: FCS/FDS remain missing. Raw bytes and extra
    XMM8..15 are retained by the enclosing source, not silently discarded.
    """
    if len(raw) != 512 or pointer_format not in (None, "legacy32", "fxsave64"):
        raise CheckpointError("FXSAVE size or pointer format")
    u16 = lambda off: int.from_bytes(raw[off:off + 2], "little")
    u32 = lambda off: int.from_bytes(raw[off:off + 4], "little")
    out = {"FPCW": u16(0), "FPSW": u16(2), "FOP": u16(6), "MXCSR": u32(24)}
    top = (out["FPSW"] >> 11) & 7
    ftw = raw[4]
    full_tag = 0
    for physical in range(8):
        logical = (physical - top) & 7
        slot = raw[32 + 16 * logical:42 + 16 * logical]
        mantissa, exponent = struct.unpack("<QH", slot)
        out[f"FP{physical}"] = [mantissa, exponent]
        exp = exponent & 0x7fff
        if not ftw & (1 << physical):
            tag = 3
        elif exp == 0 and mantissa == 0:
            tag = 1
        elif exp in (0, 0x7fff) or not mantissa & (1 << 63):
            tag = 2
        else:
            tag = 0
        full_tag |= tag << (2 * physical)
    out["FPTAG"] = full_tag
    for index in range(8):
        out[f"XMM{index}"] = int.from_bytes(raw[160 + 16 * index:176 + 16 * index], "little")
    if pointer_format == "legacy32":
        out.update(FIP=u32(8), FCS=u16(12), FDP=u32(16), FDS=u16(20))
    elif pointer_format == "fxsave64":
        out.update(FIP=int.from_bytes(raw[8:16], "little"), FDP=int.from_bytes(raw[16:24], "little"))
    return {"registers": out, "pointer_format": pointer_format, "top": top,
            "abridged_ftw": ftw, "mxcsr_mask": u32(28),
            "missing": [n for n in ("FIP", "FDP", "FCS", "FDS") if n not in out],
            "raw_sha256": hashlib.sha256(raw).hexdigest(), "accepted": False}


def decode_cpu_report(report: dict, *, fx_pointer_format: str | None = None) -> dict:
    """Reparse raw group bytes, ignoring supplied tag offsets/names as authority."""
    magic_text = report.get("magic")
    if magic_text not in ("bed2bed2", "bed3bed3") or len(report.get("cpu_groups", [])) != 1:
        raise CheckpointError("unsupported CPU checkpoint profile")
    magic = int(magic_text, 16)
    version = magic & 15
    reserved = report.get("header_reserved")
    if (type(report.get("version")) is not int or report["version"] != version
            or type(reserved) is not int or not 0 <= reserved <= 0xffffffff):
        raise CheckpointError("inconsistent CPU checkpoint profile")
    header_hex = report.get("header_and_directory_hex")
    if not isinstance(header_hex, str) or len(header_hex) > 2 * (12 + 512 * 80):
        raise CheckpointError("checkpoint header budget or encoding")
    try:
        original_header = bytes.fromhex(header_hex)
    except ValueError as exc:
        raise CheckpointError("checkpoint header encoding") from exc
    if len(original_header) < 12:
        raise CheckpointError("short checkpoint header")
    header_magic, header_reserved, group_count = struct.unpack_from("<III", original_header)
    if (header_magic != magic or header_reserved != reserved or not 0 < group_count <= 512
            or len(original_header) != 12 + 80 * group_count):
        raise CheckpointError("checkpoint header/report disagreement")
    group = report["cpu_groups"][0]
    if len(group.get("raw_hex", "")) > 2 * 1024 * 1024:
        raise CheckpointError("CPU raw group budget")
    try:
        raw = bytes.fromhex(group["raw_hex"])
    except (KeyError, ValueError) as exc:
        raise CheckpointError("CPU raw encoding") from exc
    if len(raw) != group.get("bytes") or hashlib.sha256(raw).hexdigest() != group.get("sha256"):
        raise CheckpointError("CPU raw identity mismatch")
    # A synthetic directory lets the already bounded container parser re-read
    # the original tag bytes. Only metadata offsets change; no tag bytes do.
    prefix = struct.pack("<III64sQQ", magic, reserved, 1, b"cpu", 92, 0)
    parsed = parse_cpu_groups(io.BytesIO(prefix + raw), len(prefix) + len(raw))["cpu_groups"][0]
    if parsed["bytes"] != len(raw):
        raise CheckpointError("CPU raw group has trailing bytes")

    def tag(name, indices, size):
        rows = [t for t in parsed["tags"] if t["name"] == name and t["indices"] == indices]
        if len(rows) != 1:
            raise CheckpointError(f"missing or ambiguous CPU tag: {name}{indices}")
        t = rows[0]
        if t["disk_size"] != size or t["memory_size"] != size:
            raise CheckpointError(f"CPU tag size/compression: {name}{indices}")
        offset = t["data_offset"] - 92
        return raw[offset:offset + size]

    scalar = lambda name, indices, size: int.from_bytes(tag(name, indices, size), "little")
    count = scalar("cpu:numVCPUs", [], 4)
    if not 0 < count <= 16:
        raise CheckpointError("CPU count budget")
    cpus = []
    for cpu in range(count):
        gp = dict(zip(GP_NAMES, struct.unpack("<16Q", tag("gpregs", [cpu], 128))))
        rip = scalar("rip", [cpu], 8)
        flag_low = scalar("eflags", [cpu], 4)
        flag_other = scalar("EFLAGS", [cpu], 4)
        flags = flag_low | flag_other
        controls = list(struct.unpack("<9Q", tag("CR64", [cpu], 72)))
        debug = list(struct.unpack("<8Q", tag("DR64", [cpu], 64)))
        segments = {}
        for index, name in enumerate(SEG_NAMES):
            sel = scalar("S", [cpu, index], 4)
            base = scalar("S.base64", [cpu, index], 8)
            limit = scalar("S.limit", [cpu, index], 4)
            rights = scalar("S.rights", [cpu, index], 4)
            if sel > 0xffff or limit > 0xfffff:
                raise CheckpointError("segment selector/encoded limit width")
            effective_limit = (limit << 12) | 0xfff if rights & 0x800000 else limit
            segments[name] = {"selector": sel, "base": base, "encoded_limit": limit,
                              "limit": effective_limit, "rights": rights}
        tables = {}
        for name in ("GDTR", "IDTR"):
            limit, base = struct.unpack("<HQ", tag(name, [cpu], 10))
            tables[name] = {"base": base, "limit": limit}
        fxraw = tag("fpu:fxstate", [cpu], 512)
        fx = decode_fxsave(fxraw, pointer_format=fx_pointer_format)
        canonical = {"E" + name[1:].upper(): gp[name] & 0xffffffff for name in GP_NAMES[:8]}
        canonical.update(EIP=rip & 0xffffffff, EFLAGS=flags)
        canonical.update({name: segments[name]["selector"] for name in SEG_NAMES[:6]})
        canonical.update({f"CR{i}": controls[i] for i in (0, 2, 3, 4)})
        canonical.update({f"DR{i}": debug[i] for i in range(8)})
        canonical.update({name: [0, value["base"], value["limit"], 0] for name, value in tables.items()})
        for name in ("LDTR", "TR"):
            s = segments[name]
            canonical[name] = [s["selector"], s["base"], s["limit"], s["rights"]]
        canonical.update(fx["registers"])
        cs_rights = segments["CS"]["rights"]
        compatibility32 = not bool(cs_rights & 0x200000) and bool(cs_rights & 0x400000)
        missing = [n for n in CANONICAL_NAMES if n not in canonical]
        cpus.append({"index": cpu, "gpr64": gp, "rip64": rip, "eflags": flags,
                     "flags_parts": {"eflags": flag_low, "EFLAGS": flag_other},
                     "control64": controls, "debug64": debug, "segments": segments,
                     "tables": tables, "kernel_gs_base": scalar("KERNELGSBASE", [cpu], 8),
                     "fx_common": fx, "fpu_vm_fcs_raw": tag("fpu:vmFcs", [cpu], 2).hex(),
                     "fpu_vm_fds_raw": tag("fpu:vmFds", [cpu], 2).hex(),
                     "xstate_header_raw": tag("xsave:xheader", [cpu], 64).hex(),
                     "canonical_fields": canonical, "canonical_missing": missing,
                     "compatibility32": compatibility32,
                     "canonical57_mapping_complete": not missing and compatibility32,
                     "unicorn32_descriptor_base_truncation_gap": any(v["base"] > 0xffffffff for v in tables.values())
                         or any(segments[n]["base"] > 0xffffffff for n in ("LDTR", "TR")),
                     "fullstate": False, "fullABI": False, "accepted": False})
    return {"container_profile": {"magic": magic_text, "version": version,
                                  "header_reserved": reserved},
            "cpu_group_sha256": group["sha256"], "cpus": cpus,
            "same_stopped_epoch_verified": False, "fullstate": False, "accepted": False}
