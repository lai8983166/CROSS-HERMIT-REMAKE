"""Check the original post-hit animation gate and recovery counter using the game image."""
import hashlib
import json
import struct

from unicorn import Uc, UC_ARCH_X86, UC_MODE_32, UC_HOOK_MEM_READ
from unicorn.x86_const import UC_X86_REG_EBP, UC_X86_REG_EIP, UC_X86_REG_ESP

from tools.tactics_exit_emulation import SOURCE, SOURCE_SHA256


def original_recovery(target_alive):
    image = SOURCE.read_bytes()
    if hashlib.sha256(image).hexdigest() != SOURCE_SHA256:
        raise ValueError("Original game image changed")
    cpu = Uc(UC_ARCH_X86, UC_MODE_32)
    cpu.mem_map(0x400000, (len(image) + 4095) // 4096 * 4096)
    cpu.mem_write(0x400000, image)
    cpu.mem_map(0x10000, 0x5000)
    frame, stack, controller = 0x10800, 0x11F00, 0x1000000
    cpu.mem_map(controller, 0x90000)
    unit = controller + 0x80AEC
    target = unit + 0x520
    target_record = 0x13000
    cpu.mem_write(frame - 4, struct.pack("<I", controller))
    cpu.mem_write(target + 0x258, struct.pack("<I", target_record))
    cpu.reg_write(UC_X86_REG_EBP, frame)
    cpu.reg_write(UC_X86_REG_ESP, stack)
    cpu.mem_write(frame + 8, struct.pack("<I", unit))
    cpu.mem_write(frame - 0x2C, struct.pack("<I", unit + 0x293))
    cpu.mem_write(unit + 0x4EE, struct.pack("<h", 1))
    cpu.mem_write(unit + 0x293, bytes([0x16]))
    cpu.mem_write(unit + 0x12, struct.pack("<h", 90))
    cpu.mem_write(target_record + 15, bytes([1 if target_alive else 4]))
    reads = []
    for start, size in [(target, 0x520), (target_record, 0xB0)]:
        cpu.hook_add(UC_HOOK_MEM_READ, lambda *args: reads.append(args[2]), begin=start, end=start + size - 1)

    def run(start, stop):
        cpu.emu_start(start, stop, count=100)
        if cpu.reg_read(UC_X86_REG_EIP) != stop:
            raise ValueError("Original instruction boundary missed")

    # Case 16h leaves the phase unchanged until the release animation is complete.
    run(0x4784B2, 0x47875F)
    assert cpu.mem_read(unit + 0x293, 1) == bytes([0x16])
    cpu.mem_write(unit + 4, bytes([1]))
    # Stop just before external presentation setup, after the actual phase and timer writes.
    run(0x4784B2, 0x4784D7)
    assert cpu.mem_read(unit + 0x293, 1) == bytes([0x17])
    for remaining in range(89, -1, -1):
        # At zero, stop immediately before the return-to-idle animation call.
        run(0x478521, 0x47854A if remaining == 0 else 0x47875F)
        assert struct.unpack("<h", cpu.mem_read(unit + 0x10, 2))[0] == remaining
    if reads:
        raise ValueError("Post-hit gate or recovery read target memory")
    return {"release_gate": 0x16, "recovery_phase": 0x17, "source_countdown": 90,
            "target_reads": len(reads), "target_alive": target_alive}


if __name__ == "__main__":
    print(json.dumps([original_recovery(alive) for alive in (True, False)]))
