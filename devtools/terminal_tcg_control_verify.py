"""Fail-closed interpretation of bounded guest-control evidence."""
from devtools.terminal_tcg_guest_query import UUID

def completed(r):
    return (not r.get('errors') and not r.get('timed_out') and r.get('host_job_active_after')==0
        and r.get('host_exit_code')==0 and r.get('remote_completion')=='observed'
        and r.get('response',{}).get('ok')is True)

def evaluate(report,sidecar):
    controls=[x['control']for x in report.get('observations',[])if 'control'in x]
    status=next((x['response']['value']for x in controls if completed(x)),None)
    owner=bool(status and status.get('computer')=='CHAOMOFA-WORKER'
        and status.get('manufacturer')=='QEMU' and status.get('uuid','').lower()==UUID
        and status.get('cpu')==2 and 3*1024**3<status.get('memory',0)<=4*1024**3 and status.get('boot'))
    clean=bool(report.get('all_processes_exited') and sidecar.get('process_exited')
        and sidecar.get('host_job_active_after')==0 and sidecar.get('stop_requested')
        and report.get('parent_size_mtime_unchanged') and not report.get('errors') and not sidecar.get('errors'))
    wow=report.get('wow64',{});v=wow.get('response',{}).get('value',{})
    wow_pass=bool(owner and completed(wow) and v.get('pointer_bytes')==4 and v.get('process64')is False
        and v.get('os64')is True and v.get('child_exited')is True and v.get('uuid','').lower()==UUID)
    return dict(accepted=False,control_preflight_passed=owner and clean,wow64_process_preflight_passed=wow_pass and clean,
        cleanup_observed=clean,original_wait_return_verified=False,full_state_replay_admitted=False,
        timing_scope='Scheduled sampling and bounded WinRM requests; not a hard whole-system deadline')
