"""Run MAP71's original unit aggregation and network result on bounded unit records."""
from hashlib import sha256
from struct import pack, unpack

from unicorn import Uc, UC_ARCH_X86, UC_MODE_32
from unicorn.x86_const import UC_X86_REG_ECX, UC_X86_REG_EIP, UC_X86_REG_ESP
from tools.tactics_exit_emulation import BASE, SOURCE, SOURCE_SHA256


def run():
    image = SOURCE.read_bytes()
    assert sha256(image).hexdigest() == SOURCE_SHA256
    uc = Uc(UC_ARCH_X86, UC_MODE_32)
    uc.mem_map(BASE, (len(image) + 4095) & ~4095)
    uc.mem_write(BASE, image)
    ctrl, task, stack, end = 0x2000000, 0x2200000, 0x2300000, 0x2400000
    for addr, size in ((ctrl, 0x120000), (task, 4096), (stack, 65536), (end, 4096)):
        uc.mem_map(addr, size)
    uc.mem_write(ctrl + 0x117c38, pack("<I", task))
    uc.mem_write(0x4549d0, bytes.fromhex("c21c00"))  # post-result script dispatch
    uc.mem_write(0x56ce80, bytes.fromhex("c3"))
    for player in range(4):
        membership = bytearray([1] * 4)
        membership[player] = 0
        uc.mem_write(ctrl + 0x115aac + player*16, bytes(membership))
    cases = (
        ((1, 1, 0, 0), 1, 0, -1), ((1, 0, 0, 0), 1, 0, 1),
        ((0, 1, 0, 0), 1, 0, 5), ((0, 0, 0, 0), 0, 0, 5),
        ((3, 1, 0, 0), 0, 0, 1), ((1, 3, 0, 0), 0, 0, 5),
        ((3, 3, 0, 0), 0, 0, 3), ((1, 3, 0, 0), 0, 1, 3),
        ((3, 1, 0, 0), 0, 1, 5),
    )
    for counts, remaining, local_side, expected in cases:
        uc.mem_write(0x7f4490, pack("<i", local_side))
        uc.mem_write(ctrl + 0x80aec, bytes(250 * 0x520))
        slot = 0
        for side, count in enumerate(counts):
            for _ in range(count):
                work = ctrl + 0x80aec + slot * 0x520
                record = ctrl + 0xd0c2c + slot * 176
                uc.mem_write(work, pack("<h", 1))
                uc.mem_write(work + 600, pack("<I", record))
                uc.mem_write(record + 2, pack("<H", slot + 1))
                uc.mem_write(record + 15, bytes([1]))
                uc.mem_write(record + 0xa4, bytes([side]))
                slot += 1
        # Fallen students remain in occupied work slots after their state changes to 4.
        work = ctrl + 0x80aec + slot * 0x520
        record = ctrl + 0xd0c2c + slot * 176
        uc.mem_write(work, pack("<h", 1))
        uc.mem_write(work + 600, pack("<I", record))
        uc.mem_write(record + 2, pack("<H", slot + 1))
        uc.mem_write(record + 15, bytes([4]))
        uc.mem_write(record + 0xa4, bytes([local_side]))
        uc.mem_write(ctrl + 0x2e6f4, pack("<i", remaining))
        uc.mem_write(task + 0x174, pack("<i", -1))
        top = stack + 0xff00
        uc.mem_write(top, pack("<I", end))
        uc.reg_write(UC_X86_REG_ECX, ctrl)
        uc.reg_write(UC_X86_REG_ESP, top)
        uc.emu_start(0x4368b0, end, count=100000)
        assert uc.reg_read(UC_X86_REG_EIP) == end
        assert unpack("<4h", uc.mem_read(ctrl + 0x116074, 8)) == counts
        actual, = unpack("<i", uc.mem_read(task + 0x174, 4))
        assert actual == expected, (counts, remaining, local_side, expected, actual)
    print(f"MAP71 original network result passed {len(cases)} side-count, local-side and timeout cases")


if __name__ == "__main__":
    run()
