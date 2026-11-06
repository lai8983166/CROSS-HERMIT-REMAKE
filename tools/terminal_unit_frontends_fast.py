"""Explicit scalar-observation adapter; all frozen guest/proof code is inherited."""
import contextlib
from unittest.mock import patch

from unicorn import x86_const as x86
from tools import terminal_unit_frontends_emulation as source
from tools.terminal_unit_frontends_trace import CPU_REGISTERS

ORIGINAL_MACHINE = source.UnitFrontendMachine
REGISTER_IDS = {name: getattr(x86, 'UC_X86_REG_' + name) for name in CPU_REGISTERS}


class FastUnitFrontendMachine(ORIGINAL_MACHINE):
    """A scalar query reads one register; full checkpoint cpu() stays unchanged."""
    def getreg(self, name):
        value = self.uc.reg_read(REGISTER_IDS[name])
        return list(value) if isinstance(value, tuple) else value


@contextlib.contextmanager
def scalar_observations():
    if source.UnitFrontendMachine is not ORIGINAL_MACHINE:
        raise ValueError('unexpected or nested source machine substitution')
    with patch.object(source, 'UnitFrontendMachine', FastUnitFrontendMachine):
        yield


def contract():
    return dict(schema_version=1, name='single-register-observation-v1',
                only_overridden_method='getreg', registers=list(CPU_REGISTERS),
                full_CPU_capture_unchanged=True, original_guards_and_callbacks_unchanged=True,
                guest_code_or_memory_modified=False, raw_trace_comparison_required=True,
                independent_replay_unchanged=True)
