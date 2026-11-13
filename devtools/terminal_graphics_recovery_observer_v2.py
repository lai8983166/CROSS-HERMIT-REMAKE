"""Read-only observer with the inherited legacy repair entry explicitly closed."""
from devtools.terminal_graphics_recovery_observer import ReadOnlyWindowsBackend

class GuardedReadOnlyWindowsBackend(ReadOnlyWindowsBackend):
    def repair(self,*args,**kwargs):
        raise ValueError('read-only observer forbids inherited desktop repair')
