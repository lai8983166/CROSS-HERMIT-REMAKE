"""Execute 4359C0 with bounded inputs at its clear/loss predicate boundaries."""
from hashlib import sha256
from struct import pack, unpack

from unicorn import Uc, UC_ARCH_X86, UC_MODE_32, UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_ECX, UC_X86_REG_ESP
from tools.tactics_exit_emulation import BASE, SOURCE, SOURCE_SHA256


def original_result(image, elapsed, clear, lost):
    uc = Uc(UC_ARCH_X86, UC_MODE_32)
    uc.mem_map(BASE, (len(image) + 4095) & ~4095)
    uc.mem_write(BASE, image)
    work, stack, end = 0x2000000, 0x2300000, 0x2400000
    uc.mem_map(work, 0x120000)
    uc.mem_map(stack, 0x10000)
    uc.mem_map(end, 4096)
    top = stack + 0xff00
    uc.reg_write(UC_X86_REG_ESP, top)
    uc.reg_write(UC_X86_REG_ECX, work)
    uc.mem_write(top, pack('<I', end))
    uc.mem_write(work + 0x2e6f8, pack('<i', elapsed))
    seen = []
    for address, value in ((0x4307b0, clear), (0x430df0, lost)):
        uc.mem_write(address, b'\xb8' + pack('<I', value) + b'\xc3')
    uc.mem_write(0x454ab0, b'\xc2\x04\x00')
    uc.mem_write(0x56ce80, b'\xc3')

    def capture(machine, _address, _size, _data):
        sp = machine.reg_read(UC_X86_REG_ESP)
        seen.append(unpack('<I', machine.mem_read(sp + 4, 4))[0])

    uc.hook_add(UC_HOOK_CODE, capture, begin=0x454ab0, end=0x454ab0)
    uc.emu_start(0x4359c0, end, count=1000)
    assert uc.reg_read(UC_X86_REG_EAX) == 0
    return seen


if __name__ == '__main__':
    image = SOURCE.read_bytes()
    assert sha256(image).hexdigest() == SOURCE_SHA256
    elapsed_cases = ((0, 2), (36000, 2), (36001, 5), (54000, 5),
                     (54001, 8), (108000, 8), (108001, 11))
    for elapsed, sub in elapsed_cases:
        for lost in (False, True):
            assert original_result(image, elapsed, True, lost) == [sub]
            assert original_result(image, elapsed, False, lost) == ([11] if lost else [])
    print('MAP33 original 4359C0 passed 28 predicate/clock boundary cases.')
