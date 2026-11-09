"""Version 2: preserve repeated CPU tag identities as separate occurrences.

Read bounded CPU tag groups from VMware checkpoint metadata, never guest RAM.

Format reference (independent implementation, no imported Volatility code):
https://github.com/volatilityfoundation/volatility/blob/master/volatility/plugins/addrspaces/vmware.py
Only container layout is interpreted. Raw CPU group bytes are retained once;
register names, array ordering and extended/compressed payload semantics require
separate evidence. This reader neither suspends nor restores a virtual machine.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
import struct
from typing import BinaryIO


MAGICS = {0xBED2BED0, 0xBAD1BAD1, 0xBED2BED2, 0xBED3BED3}
MAX_GROUPS = 512
MAX_CPU_GROUP_BYTES = 1024 * 1024
MAX_READ_BYTES = 4 * 1024 * 1024
MAX_TAGS = 8192


class CheckpointError(ValueError):
    pass


def parse_cpu_groups(stream: BinaryIO, file_size: int) -> dict:
    """Seek/read group directory and cpu group only, under a 4 MiB I/O budget.

    file_size must describe the same fixed source as stream. All ranges use
    absolute file offsets. Payloads from non-cpu groups are never opened.
    """
    if type(file_size) is not int or not 12 <= file_size <= 2**40:
        raise CheckpointError("invalid source size")
    read_bytes = 0

    def read(offset: int, size: int) -> bytes:
        nonlocal read_bytes
        if not (0 <= offset <= file_size and 0 <= size <= file_size - offset):
            raise CheckpointError("checkpoint range outside source")
        if size > MAX_READ_BYTES - read_bytes:
            raise CheckpointError("checkpoint read budget")
        stream.seek(offset)
        data = stream.read(size)
        read_bytes += len(data)
        if len(data) != size:
            raise CheckpointError("short checkpoint read")
        return data

    header = read(0, 12)
    magic, reserved, count = struct.unpack("<III", header)
    if magic not in MAGICS or not 0 < count <= MAX_GROUPS:
        raise CheckpointError("unknown checkpoint magic or group count")
    version = magic & 15
    directory = read(12, count * 80)
    directory_end = 12 + count * 80
    groups = []
    names = set()
    offsets = set()
    for number in range(count):
        record = directory[number * 80:(number + 1) * 80]
        raw_name, offset, trailing = struct.unpack("<64sQQ", record)
        if b"\0" not in raw_name:
            raise CheckpointError("unterminated group name")
        try:
            name = raw_name.split(b"\0", 1)[0].decode("ascii")
        except UnicodeDecodeError as exc:
            raise CheckpointError("non-ASCII group name") from exc
        if not name or name in names or offset in offsets or not directory_end <= offset < file_size:
            raise CheckpointError("duplicate or out-of-range group")
        names.add(name)
        offsets.add(offset)
        groups.append({"name": name, "tags_offset": offset, "directory_trailing_u64": trailing})
    ordered = sorted(offsets)
    boundaries = {off: ordered[i + 1] if i + 1 < len(ordered) else file_size
                  for i, off in enumerate(ordered)}
    cpu_groups = []
    for group in groups:
        if group["name"] != "cpu":
            continue
        start = group["tags_offset"]
        end = min(boundaries[start], start + MAX_CPU_GROUP_BYTES)
        offset = start
        tags = []
        identities = {}

        def bounded_read(where: int, size: int) -> bytes:
            if not start <= where <= end or not 0 <= size <= end - where:
                raise CheckpointError("CPU tag crosses group boundary or byte budget")
            return read(where, size)

        while True:
            tag_offset = offset
            flags, name_length = bounded_read(offset, 2)
            offset += 2
            if flags == 0 and name_length == 0:
                break
            if not name_length or len(tags) >= MAX_TAGS:
                raise CheckpointError("invalid tag name or tag budget")
            raw_name = bounded_read(offset, name_length)
            offset += name_length
            try:
                name = raw_name.decode("ascii")
            except UnicodeDecodeError as exc:
                raise CheckpointError("non-ASCII CPU tag name") from exc
            if any(ord(c) < 32 or ord(c) > 126 for c in name):
                raise CheckpointError("invalid CPU tag name")
            index_count = flags >> 6
            indices = list(struct.unpack("<" + "I" * index_count,
                          bounded_read(offset, index_count * 4)))
            offset += index_count * 4
            identity = (name, tuple(indices))
            occurrence = identities.get(identity, 0)
            identities[identity] = occurrence + 1
            size_code = flags & 63
            disk_size = memory_size = size_code
            padding_size = 0
            if size_code in (62, 63):
                size_width = 4 if version == 0 else 8
                fmt = "<II" if size_width == 4 else "<QQ"
                disk_size, memory_size = struct.unpack(fmt, bounded_read(offset, size_width * 2))
                offset += size_width * 2
                padding_size = struct.unpack("<H", bounded_read(offset, 2))[0]
                offset += 2
                bounded_read(offset, padding_size)
                offset += padding_size
            data_offset = offset
            data = bounded_read(data_offset, disk_size)
            offset += disk_size
            tag = {"name": name, "indices": indices, "flags": flags, "size_code": size_code,
                   "tag_offset": tag_offset, "data_offset": data_offset, "occurrence": occurrence,
                   "disk_size": disk_size, "memory_size": memory_size,
                   "padding_size": padding_size, "data_sha256": hashlib.sha256(data).hexdigest()}
            if size_code < 62 and disk_size in (1, 2, 4, 8):
                tag["little_endian_scalar"] = int.from_bytes(data, "little")
            tags.append(tag)
        raw_group = bounded_read(start, offset - start)
        cpu_groups.append({"name": group["name"], "offset": start,
                           "bytes": len(raw_group), "sha256": hashlib.sha256(raw_group).hexdigest(),
                           "raw_hex": raw_group.hex(), "tags": tags,
                           "duplicate_identities": [{"name": k[0], "indices": list(k[1]), "count": v}
                                                    for k, v in identities.items() if v > 1]})
    if not cpu_groups:
        raise CheckpointError("no cpu group")
    return {"magic": f"{magic:08x}", "version": version, "header_reserved": reserved,
            "source_bytes": file_size, "header_and_directory_hex": (header + directory).hex(),
            "groups": groups, "cpu_groups": cpu_groups, "bytes_read": read_bytes,
            "memory_groups_read": False, "fullstate": False, "fullABI": False,
            "same_stopped_epoch_verified": False, "accepted": False}


def read_cpu_groups(path: str | Path) -> dict:
    """Read a stable checkpoint file; do not hash or scan its unselected ranges."""
    path = Path(path).resolve(strict=True)
    before = path.stat()
    with path.open("rb") as stream:
        result = parse_cpu_groups(stream, before.st_size)
    after = path.stat()
    if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
        raise CheckpointError("checkpoint changed during read")
    result["source"] = {"path": str(path), "bytes": before.st_size,
                        "mtime_ns": before.st_mtime_ns, "full_file_hashed": False}
    return result
