"""Owned diskless probe VM with normal multi-instruction TCG blocks."""
import subprocess
import time
from devtools.terminal_tcg_ram_event_probe_v2 import VM as BaseVM
from devtools.terminal_tcg_roundtrip_probe import QMP, RSP


class VM(BaseVM):
    def __init__(self, args, out, role, expected):
        self.out, self.role, self.expected = out, role, expected
        qp, gp = ['chaomofa-' + out.name + '-' + role + '-' + s for s in ('qmp', 'gdb')]
        self.command = [str(args.binary.resolve()), '-L', str(args.firmware.resolve()),
            '-machine', 'pc', '-accel', 'tcg,thread=single', '-smp', '2', '-m', '4G',
            '-icount', 'shift=0,align=off,sleep=off', '-rtc', 'clock=vm,base=2026-11-11T00:00:00',
            '-display', 'none', '-serial', 'none', '-monitor', 'none', '-nic', 'none', '-no-shutdown',
            '-kernel', str(out / 'guest.elf'), '-debugcon', 'file:' + str(out / (role + '.bin')),
            '-device', 'isa-debug-exit,iobase=0xf4,iosize=4', '-S',
            '-qmp', 'unix:' + qp + ',abstract=on,server=on,wait=off',
            '-gdb', 'unix:' + gp + ',abstract=on,server=on,wait=off']
        self.err = (out / (role + '.stderr')).open('wb')
        self.proc = subprocess.Popen(self.command, stdout=self.err, stderr=self.err, start_new_session=True)
        self.qmp = self.rsp = None
        start = time.monotonic()
        try:
            while self.qmp is None:
                if self.proc.poll() is not None or time.monotonic() - start > 5:
                    raise RuntimeError('startup failed')
                try:
                    self.qmp = QMP(qp)
                except (FileNotFoundError, ConnectionRefusedError):
                    time.sleep(.05)
            self.qmp.s.settimeout(10)
            self.rsp = RSP(gp)
            self.rsp.s.settimeout(10)
        except Exception:
            self.close()
            raise
