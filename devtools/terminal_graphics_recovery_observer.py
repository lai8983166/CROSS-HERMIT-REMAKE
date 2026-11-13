"""Read-only real desktop observer; has no restoration or graphics-owner admission."""
from __future__ import annotations
import ctypes as C
from devtools import terminal_graphics_desktop as parent

class ReadOnlyWindowsBackend(parent.WindowsBackend):
    evidence_kind='native-readonly'
    def __init__(self):
        # This separate class admits only existing observation methods. The
        # frozen native restoration gate remains false in the parent module.
        parent.frozen.Desktop.__init__(self)
        self.g=C.WinDLL('gdi32',use_last_error=True)
    def write(self,*args,**kwargs):
        raise ValueError('read-only observer forbids every desktop mutation')
    def _gamma(self,device,value=None):
        parent.need(value is None,'read-only observer forbids gamma writes')
        return super()._gamma(device)
    def first(self):
        initial=parent.frozen.Desktop.read(self)
        parent.need(initial['monitors'],'attached display metadata required')
        # This is a declared observation target, not a D3D adapter mapping proof.
        self.device=initial['monitors'][0]['device']
        return self.read(self.device)
