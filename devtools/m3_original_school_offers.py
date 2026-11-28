"""Run the original school list builder on a checksum-verified v7 save."""
import argparse
import hashlib
import json
import struct
from pathlib import Path

from unicorn import Uc, UC_ARCH_X86, UC_MODE_32
from unicorn.x86_const import UC_X86_REG_EIP, UC_X86_REG_ESP

from devtools.inspect_m3_adventure44_guest_saves import inspect_save
from tools.tactics_exit_emulation import BASE, SOURCE, SOURCE_SHA256


def offers(save):
    state = inspect_save(save)
    raw = SOURCE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        raise ValueError("Unexpected original executable image")
    cpu = Uc(UC_ARCH_X86, UC_MODE_32)
    cpu.mem_map(BASE, max(0x400000, (len(raw) + 4095) & ~4095))
    cpu.mem_write(BASE, raw)
    cpu.mem_write(0x7A50E8, save)
    stack, stop = 0x2100800, 0x2101000
    cpu.mem_map(0x2100000, 0x2000)
    cpu.mem_write(stack, struct.pack("<I", stop))
    cpu.reg_write(UC_X86_REG_ESP, stack)
    cpu.emu_start(0x4A1C70, stop, count=15000)
    if cpu.reg_read(UC_X86_REG_EIP) != stop:
        raise ValueError("Original school list did not return")
    categories = []
    for category, count in enumerate(struct.unpack("<3h", cpu.mem_read(0x7D62FA, 6))):
        if not 0 <= count <= 80:
            raise ValueError("Invalid original school offer count")
        categories.append([struct.unpack("<h", cpu.mem_read(0x7D599E + category*0x320 + row*10, 2))[0]
                           for row in range(count)])
    return {"date":state["date"], "sha256":hashlib.sha256(save).hexdigest(), "categories":categories,
            "selected":struct.unpack("<h", cpu.mem_read(0x7AAB16, 2))[0]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("saves", nargs="+", type=Path)
    for path in parser.parse_args().saves:
        print(json.dumps(offers(path.read_bytes())))
