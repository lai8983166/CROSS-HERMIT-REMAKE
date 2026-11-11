"""Reject numeric aliases for raw64 CPU metadata before v2 validation."""
from devtools.terminal_tcg_wow64_effects_v2 import verify as verify_v2


def verify(trace, plan):
    try:
        for group in ('points', 'steps'):
            for entry in trace[group]:
                for key in (('states',) if group == 'points' else ('before', 'after')):
                    for state in entry[key]:
                        if type(state['target_bits']) is not int:
                            raise ValueError('target_bits must be int')
                        for vp in state['vp_stopped']:
                            if type(vp['cpu']) is not int or vp['stopped'] is not True:
                                raise ValueError('invalid stopped CPU metadata type')
    except (KeyError, TypeError, ValueError) as exc:
        return dict(accepted=False, cr2_explained=False, consumer_connected_in_this_trace=False,
                    local_effects_verified=False, checks=[], errors=[str(exc)])
    return verify_v2(trace, plan)
