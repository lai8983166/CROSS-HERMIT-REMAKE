"""Resume-aware detach for the dedicated external VMM monitor.

VMware ignores normal RSP packets while running. Stop before removing an
owned breakpoint or detaching; never silently leave a live paused VM behind.
"""
from devtools.terminal_vm_monitor_v3 import Monitor as PriorMonitor
from devtools.terminal_vm_monitor import need


class Monitor(PriorMonitor):
    def close(self):
        if self.sock is None:
            return
        try:
            if not self.stopped:
                self.interrupt()
            for item in list(self.breakpoints):
                need(self.query(b'z1,' + item) == b'OK', 'remove owned hardware breakpoint')
            need(self.query(b'D') == b'OK', 'explicit stopped VMM detach/resume')
            self.stopped = False
        finally:
            self.sock.close()
            self.sock = None
