"""Offline decoding of XML-bound g prefixes, p replies and observed monitor text.

Keeps the executed v1 parser unchanged. GDB remote.c process_g_packet permits
whole-register g prefixes and uses p for omitted registers; partial registers
still fail. See sourceware.org/pipermail/gdb-cvs/2016-November/040560.html.
No fabricated bytes, guest I/O, state restoration, or acceptance decision.
"""
from __future__ import annotations

import re

from devtools.vmware_rsp_state import (DecodeError, MAX_PACKET,
                                      decode_registers as decode_raw_registers,
                                      register_layout)


def _value(raw: bytes, reg: dict, source: str) -> dict:
    size = reg["bitsize"] // 8
    if len(raw) != size * 2 or not re.fullmatch(rb"[0-9a-fA-Fx]+", raw):
        raise DecodeError("register reply width or encoding")
    if b"x" in raw and raw != b"x" * len(raw):
        raise DecodeError("partially unavailable register")
    available = b"x" not in raw
    return {**reg, "raw_hex": raw.decode(), "source": source, "available": available,
            "status": "value" if available else "unavailable",
            "value_hex": format(int.from_bytes(bytes.fromhex(raw.decode()), "little"),
                                f"0{size * 2}x") if available else None}


def decode_registers(payload: bytes, annexes: dict[str, bytes],
                     p_replies: dict[int, bytes] | None = None) -> dict:
    """Decode XML-described whole-register prefix and explicit p replies.

    p_replies keys are integer XML regnums, not text packet numbers. This pure
    function cannot establish that separate replies describe one stopped epoch;
    the caller must retain the stop/selection/run-control transcript.
    """
    result = decode_raw_registers(payload)
    layout = register_layout(annexes)
    length = len(payload) // 2
    if not payload or length > layout["expected_bytes"]:
        raise DecodeError("empty or oversized g reply")
    offset = 0
    for reg in layout["registers"]:
        size = reg["bitsize"] // 8
        if offset < length < offset + size:
            raise DecodeError("g reply truncates a register")
        if offset < length:
            item = _value(payload[offset * 2:(offset + size) * 2], reg, "g")
        else:
            item = {**reg, "raw_hex": None, "source": None, "available": False,
                    "status": "absent_from_g", "value_hex": None}
        item["in_g_packet"] = offset < length
        result["registers"][reg["name"]] = item
        offset += size
    p_replies = {} if p_replies is None else p_replies
    if (len(p_replies) > len(layout["registers"])
            or sum(map(len, p_replies.values())) > MAX_PACKET):
        raise DecodeError("p reply budget")
    for number, raw in p_replies.items():
        if type(number) is not int or not 0 <= number < len(layout["registers"]):
            raise DecodeError("p reply register number absent from XML")
        reg = layout["registers"][number]
        prior = result["registers"][reg["name"]]
        if not raw or re.fullmatch(rb"E[0-9a-fA-F]{2}", raw):
            item = {**reg, "raw_hex": raw.decode(), "source": "p", "available": False,
                    "status": "unsupported_p" if not raw else "p_error", "value_hex": None}
        else:
            item = _value(raw, reg, "p")
        if prior["available"]:
            if not item["available"] or prior["value_hex"] != item["value_hex"]:
                raise DecodeError("g/p register replies disagree")
            prior["matching_p_reply_hex"] = raw.decode()
        else:
            item["in_g_packet"] = prior["in_g_packet"]
            result["registers"][reg["name"]] = item
    missing = [r["name"] for r in result["registers"].values() if not r["available"]]
    result.update(layout_known=True, layout=layout, g_bytes=length,
                  missing=missing, unavailable=missing,
                  p_replies={str(k): v.decode("ascii") for k, v in p_replies.items()},
                  stopped_epoch_verified=False)
    return result


def parse_monitor_register(command: str, text: bytes) -> dict:
    """Parse only actual register formats observed in availability-v4.

    Segment 'base' is retained as reported_base, never promoted to the active
    FS_BASE/GS_BASE MSR. Missing descriptor attributes remain absent. Empty OK
    (observed for dr0/dr7) is not a value of zero or a supported read.
    """
    if len(text) > 2048:
        raise DecodeError("monitor register text budget")
    match = re.fullmatch(r"r (cr[0234]|[cdefgs]s|gdtr|idtr|ldtr|dr[0-7])", command)
    if not match:
        raise DecodeError("unsupported register command")
    name = match[1]
    try:
        raw = text.decode("ascii")
    except UnicodeDecodeError as exc:
        raise DecodeError("non-ASCII monitor register text") from exc
    result = {"command": command, "name": name, "raw_text": raw,
              "available": False, "fields": {}, "fullstate": False, "accepted": False}
    if not raw:
        return {**result, "status": "empty_reply"}
    line = raw.removesuffix("\n").removesuffix("\r")
    scalar = re.fullmatch(r"(cr[0234])=0x([0-9a-fA-F]{1,16})", line)
    table = re.fullmatch(r"(gdtr|idtr) base=0x([0-9a-fA-F]{1,16}) limit=0x([0-9a-fA-F]{1,4})", line)
    segment = re.fullmatch(r"([cdefgs]s|ldtr) (?:sel )?0x([0-9a-fA-F]{1,4}) "
        r"base 0x([0-9a-fA-F]{1,16}) limit 0x([0-9a-fA-F]{1,8}) "
        r"type 0x([0-9a-fA-F]) s ([01]) dpl ([0-3]) p ([01])(?: db ([01]))?", line)
    parsed = scalar or table or segment
    if parsed is None or parsed[1] != name:
        raise DecodeError("unrecognized or wrong-register monitor text")
    if scalar:
        fields = {"value": int(scalar[2], 16)}
        kind = "control"
    elif table:
        fields = {"reported_base": int(table[2], 16), "limit": int(table[3], 16)}
        kind = "descriptor_table"
    else:
        fields = {"selector": int(segment[2], 16), "reported_base": int(segment[3], 16),
                  "limit": int(segment[4], 16), "type": int(segment[5], 16),
                  "s": int(segment[6]), "dpl": int(segment[7]), "p": int(segment[8])}
        if segment[9] is not None:
            fields["db"] = int(segment[9])
        kind = "segment_descriptor_report"
        result["effective_base_verified"] = False
    return {**result, "available": True, "status": "parsed_observed_format",
            "kind": kind, "fields": fields}
