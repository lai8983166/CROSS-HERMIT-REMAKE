"""Own current x86 manager lock/events; never executes a game callback."""
from tools import school_retained_world_loop_platform as old
ROOT=old.ROOT;SOURCE=ROOT/'tools/school_retained_scheduler_platform.cs'

def build(path):
 import types
 return types.FunctionType(old.build.__code__,dict(old.build.__globals__,SOURCE=SOURCE),'build_current_scheduler_platform')(path)

Live=old.Live
