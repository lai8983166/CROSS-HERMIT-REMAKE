"""Exercise original network-lobby transfer into tactical state, without a peer connection."""
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
    lobby, stack, end = 0x2000000, 0x2300000, 0x2400000
    uc.mem_map(lobby, 0x20000)
    uc.mem_map(stack, 0x10000)
    uc.mem_map(end, 4096)
    uc.mem_write(0x56ce80, bytes.fromhex("c3"))
    uc.mem_write(0x7a49fc, pack("<I", lobby))
    conn = lobby + 0x9178
    uc.mem_write(conn + 0x138, pack("<I", 1001))
    for player in range(4):
        uc.mem_write(conn + 0x1780 + 0x88*player, bytes([1]))
        uc.mem_write(conn + 0x1804 + 0x88*player, pack("<I", 1000+player))

    def execute(address):
        top = stack + 0xff00
        uc.mem_write(top, pack("<I", end))
        uc.reg_write(UC_X86_REG_ESP, top)
        uc.reg_write(UC_X86_REG_ECX, lobby)
        uc.emu_start(address, end, count=100000)
        assert uc.reg_read(UC_X86_REG_EIP) == end

    execute(0x44a960)
    for i in range(8):
        at = lobby + 0x1ab0 + 8*i
        assert uc.mem_read(at, 2) == bytes([1, 0])
        assert uc.mem_read(at+4, 4) == pack("<I", 0x605f18+176*i)
    for i in (0, 7):
        uc.mem_write(lobby+0x1ab1+8*i, bytes([1]))
    execute(0x442090)
    for slot, i in enumerate((0, 7)):
        offset = 0x605f18 - BASE + 176*i
        expected = bytearray(image[offset:offset+176])
        expected[:2] = pack("<H", 2)
        expected[0xa4] = 1
        assert uc.mem_read(lobby+0x1c30+slot*176, 176) == expected

    for choice, scene, count in ((1, 71, 4), (68, 42, 20), (69, 43, 80)):
        uc.mem_write(lobby+0x1a88, pack("<h", choice))
        uc.mem_write(lobby+0x1aa4, pack("<h", scene))
        uc.mem_write(lobby+0x1aa8, pack("<I", 1703))
        teams = bytes([0, 1, 1, 2])
        uc.mem_write(lobby+0x1a8c, teams)
        positions = bytes([2, 3, 1, 0])
        uc.mem_write(lobby+0x1aac, positions)
        actors = bytearray()
        for slot in range(count):
            record = bytearray(image[0x607708-BASE:0x607708-BASE+176])
            record[:4] = pack("<HH", 1, 1+slot%20)
            record[0xa4] = slot//20 if count==80 else slot%4
            actors.extend(record)
        uc.mem_write(lobby+0x1c30, bytes(actors).ljust(80*176, bytes(1)))
        uc.mem_write(0x7f4518, bytes([0xa5])*(80*176))
        execute(0x448a30)
        assert unpack("<h", uc.mem_read(0x7f4488, 2))[0] == scene
        assert uc.mem_read(0x7f448d, 1) == bytes([count])
        assert uc.mem_read(0x7f4490, 2) == bytes([1,1])
        assert uc.mem_read(0x7f4518, 80*176) == bytes(actors).ljust(80*176, bytes(1))
        assert uc.mem_read(0x7f44e4, 16) == teams.ljust(16, bytes(1))
        assert uc.mem_read(0x7f44f4, 16) == positions.ljust(16, bytes(1))
        assert uc.mem_read(0x7f44d0, 4) == pack("<I", 1703)
    print("Original lobby transfer preserved selected scenes 71/42/43, 4/20/80 actor records and four player slots")


if __name__ == "__main__":
    run()
