"""Same-process CPU/device restore with actual high x87 pointers in long mode."""
import argparse
from pathlib import Path
from devtools import terminal_tcg_device_restore_probe_v3 as runner
from devtools.terminal_tcg_longmode_image import image as longmode_image


def image(root,inverse=False):
    if inverse:raise ValueError('inverse belongs to protected-mode fixture')
    raw, prior=longmode_image(root)
    elf=bytearray(raw);a=prior['stop'];offset=4096+a-0x100000000-0x100000
    # No memory writes between A and B. Keep FS base high but disturb all
    # state explicitly tested below through ordinary guest instructions.
    code=bytes.fromhex('90dbe366450fefff4831c04831db4831c94883c001fc')
    b=a+len(code)
    code+=bytes.fromhex('90b052e6e9b810000000e7f4f4ebfd')
    elf[offset:offset+len(code)]=code
    return bytes(elf),dict(a=a,b=b,inverse=False,paging=True,interval_writes_ram=False,
        fip=prior['fip'],fdp=prior['fdp'],fs_base=prior['fs_base'])


if __name__=='__main__':
    p=argparse.ArgumentParser()
    for name in ('binary','firmware','output'):p.add_argument('--'+name,type=Path,required=True)
    a=p.parse_args();a.inverse=False
    runner.image=image
    raise SystemExit(not runner.run(a))
