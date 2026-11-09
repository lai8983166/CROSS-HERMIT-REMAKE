"""Bounded, offline RSP decoding. No sockets, VM control, writes, or ABI claims.

Wire/layout rules: sourceware.org/gdb/current/onlinedocs/gdb.html/{Overview,
Packets,Target-Description-Format}.html. VMware layouts must come from captured
target.xml and its captured annexes; packet length never selects a guessed ABI.
"""
from __future__ import annotations

import hashlib
import re
import xml.etree.ElementTree as ET

MAX_PACKET = 65536
MAX_XML = 131072
MAX_REGISTERS = 512
XI = "{http://www.w3.org/2001/XInclude}include"


class DecodeError(ValueError):
    pass


def decode_payload(encoded: bytes, *, limit: int = MAX_PACKET) -> bytes:
    """Decode wire escaping and RLE in one pass; escaped '*' is literal."""
    if not 0 < limit <= MAX_PACKET or len(encoded) > limit:
        raise DecodeError("encoded payload limit")
    out = bytearray()
    i = 0
    while i < len(encoded):
        c = encoded[i]
        i += 1
        if c == 0x7D:
            if i == len(encoded):
                raise DecodeError("truncated escape")
            out.append(encoded[i] ^ 0x20)
            i += 1
        elif c == 0x2A:
            if not out or i == len(encoded):
                raise DecodeError("invalid RLE prefix")
            count = encoded[i]
            i += 1
            if not 32 <= count <= 126 or count in (35, 36):
                raise DecodeError("invalid RLE count")
            repeat = count - 29
            if len(out) + repeat > limit:
                raise DecodeError("expanded payload limit")
            out.extend(bytes([out[-1]]) * repeat)
        else:
            if c in (35, 36):
                raise DecodeError("unescaped frame delimiter")
            out.append(c)
        if len(out) > limit:
            raise DecodeError("expanded payload limit")
    return bytes(out)


def decode_frame(frame: bytes, *, limit: int = MAX_PACKET) -> bytes:
    """Decode exactly one complete $...#cc frame (acks are transport's job)."""
    if len(frame) > limit + 4 or len(frame) < 4 or frame[:1] != b"$" or frame[-3:-2] != b"#":
        raise DecodeError("invalid frame boundaries or size")
    if not re.fullmatch(rb"[0-9a-fA-F]{2}", frame[-2:]):
        raise DecodeError("invalid checksum encoding")
    encoded = frame[1:-3]
    if sum(encoded) % 256 != int(frame[-2:], 16):
        raise DecodeError("checksum mismatch")
    return decode_payload(encoded, limit=limit)


def encode_packet(payload: bytes) -> bytes:
    """Frame bytes, without interpreting the command or performing any I/O."""
    if len(payload) > MAX_PACKET:
        raise DecodeError("payload limit")
    encoded = bytearray()
    for c in payload:
        if c in (35, 36, 42, 125):
            encoded.extend((125, c ^ 32))
        else:
            encoded.append(c)
    if len(encoded) > MAX_PACKET:
        raise DecodeError("encoded payload limit")
    return b"$" + encoded + b"#" + f"{sum(encoded) % 256:02x}".encode()


def register_layout(annexes: dict[str, bytes]) -> dict:
    """Resolve captured XML only. No file/network resolver; missing annex fails.

    VMware's legacy XML uses xi:include without declaring xmlns:xi. Only this
    exact include syntax is normalized, and the original-byte hash is retained.
    """
    if not annexes or len(annexes) > 16 or sum(map(len, annexes.values())) > MAX_XML:
        raise DecodeError("XML budget")
    if "target.xml" not in annexes:
        raise DecodeError("missing target.xml")
    registers = []
    sources = {}
    active = set()
    used = set()
    architecture = None
    next_number = 0

    def visit(name: str, depth: int = 0):
        nonlocal architecture, next_number
        if depth > 8 or name in active or name in used or name not in annexes:
            raise DecodeError("missing, cyclic or repeated XML annex")
        if not re.fullmatch(r"[A-Za-z0-9_.-]{1,80}", name):
            raise DecodeError("unsafe XML annex name")
        raw = annexes[name]
        if re.search(rb"<!\s*(?:DOCTYPE|ENTITY)", raw, re.I):
            raise DecodeError("XML declarations unsupported")
        sources[name] = {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}
        normalized = re.sub(rb'<xi:include href="([A-Za-z0-9_.-]{1,80})"\s*/>',
                            rb'<include xmlns="http://www.w3.org/2001/XInclude" href="\1"/>', raw)
        try:
            root = ET.fromstring(normalized)
        except ET.ParseError as exc:
            raise DecodeError("invalid XML") from exc
        if root.tag != ("target" if name == "target.xml" else "feature"):
            raise DecodeError("unexpected XML root")
        active.add(name)
        used.add(name)

        def walk(element, level=0):
            nonlocal architecture, next_number
            if level > 16:
                raise DecodeError("XML depth")
            if element.tag == XI:
                if set(element.attrib) != {"href"} or len(element):
                    raise DecodeError("invalid XML include")
                visit(element.attrib["href"], depth + 1)
                return
            if element.tag == "architecture":
                if architecture is not None or element.text not in ("i386", "i386:x86-64"):
                    raise DecodeError("unsupported or duplicate architecture")
                architecture = element.text
            if element.tag == "reg":
                regname = element.get("name", "")
                if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]{0,63}", regname):
                    raise DecodeError("invalid register name")
                try:
                    bits = int(element.attrib["bitsize"], 10)
                    number = int(element.get("regnum", str(next_number)), 10)
                except (KeyError, ValueError) as exc:
                    raise DecodeError("invalid register width/number") from exc
                if not 0 < bits <= 4096 or bits % 8 or number != next_number:
                    raise DecodeError("unsupported width or noncontiguous register numbering")
                if len(registers) >= MAX_REGISTERS or any(r["name"] == regname for r in registers):
                    raise DecodeError("duplicate register or register budget")
                registers.append({"name": regname, "bitsize": bits, "regnum": number})
                next_number += 1
            for child in element:
                walk(child, level + 1)

        walk(root)
        active.remove(name)

    visit("target.xml")
    if architecture is None or not registers:
        raise DecodeError("missing architecture or registers")
    return {"architecture": architecture, "byte_order": "little", "registers": registers,
            "expected_bytes": sum(r["bitsize"] // 8 for r in registers), "xml_sources": sources}


def decode_registers(payload: bytes, annexes: dict[str, bytes] | None = None) -> dict:
    """Decode a g response. Unknown layout remains raw with no named registers."""
    if len(payload) > MAX_PACKET or len(payload) % 2 or not re.fullmatch(rb"[0-9a-fA-Fx]*", payload):
        raise DecodeError("invalid g register payload")
    result = {"raw_hex": payload.decode("ascii"), "raw_sha256": hashlib.sha256(payload).hexdigest(),
              "layout_known": False, "registers": {}, "unavailable": [], "fullstate": False,
              "fullABI": False, "accepted": False}
    if annexes is None:
        return result
    layout = register_layout(annexes)
    if len(payload) != layout["expected_bytes"] * 2:
        raise DecodeError("g payload length disagrees with captured XML")
    offset = 0
    for reg in layout["registers"]:
        size = reg["bitsize"] // 8
        raw = payload[offset * 2:(offset + size) * 2]
        offset += size
        if b"x" in raw and raw != b"x" * len(raw):
            raise DecodeError("partially unavailable register")
        available = b"x" not in raw
        result["registers"][reg["name"]] = {**reg, "raw_hex": raw.decode(), "available": available,
            "value_hex": format(int.from_bytes(bytes.fromhex(raw.decode()), "little"), f"0{size * 2}x") if available else None}
        if not available:
            result["unavailable"].append(reg["name"])
    result.update(layout_known=True, layout=layout)
    return result


def decode_monitor_reply(packets: list[bytes], *, limit: int = MAX_PACKET) -> bytes:
    """Join decoded qRcmd response packets: O-hex intermediates plus final OK/hex.

    A successful interpreter reply does not establish success of its command.
    Callers must inspect the actual text (e.g. 'unimplemented' is not a value).
    """
    if (not packets or len(packets) > 256 or not 0 < limit <= MAX_PACKET
            or sum(map(len, packets)) > 2 * limit + 256):
        raise DecodeError("monitor response budget")
    out = bytearray()
    for index, packet in enumerate(packets):
        final = index == len(packets) - 1
        if final and packet == b"OK":
            continue
        if not final:
            if not packet.startswith(b"O"):
                raise DecodeError("invalid intermediate monitor packet")
            packet = packet[1:]
        if not re.fullmatch(rb"(?:[0-9a-fA-F]{2})*", packet):
            raise DecodeError("invalid monitor output hex")
        if len(out) + len(packet) // 2 > limit:
            raise DecodeError("monitor output limit")
        out.extend(bytes.fromhex(packet.decode()))
    return bytes(out)
