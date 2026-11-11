"""Diagnose a fixed incoming path using an authenticated retained stream.

Cross-build comparison is explicit and never promoted to same-build acceptance.
"""
import argparse,hashlib,json,os,signal,threading,time
from pathlib import Path
from devtools.terminal_tcg_ram_event_probe import VM
from devtools.terminal_tcg_roundtrip_probe import identity


def run(a):
    parent=json.loads((a.source/'report.json').read_bytes())
    stream=a.source/'checkpoint.bin'
    if identity(stream)['sha256']!=parent['checkpoint']['sha256']:raise ValueError('checkpoint changed')
    a.output.mkdir(exist_ok=False);(a.output/'guest.elf').write_bytes((a.source/'guest.elf').read_bytes())
    expected=parent['expected'];r=dict(accepted=False,same_build_acceptance=False,errors=[],
        binary=identity(a.binary),parent_report=identity(a.source/'report.json'),checkpoint=identity(stream))
    vm=None;done=threading.Event();start=time.monotonic()
    def watch():
        if not done.wait(65):
            r['errors'].append('65 second deadline')
            if vm and vm.proc.poll()is None:os.killpg(vm.proc.pid,signal.SIGKILL)
    threading.Thread(target=watch,daemon=True).start()
    try:
        vm=VM(a,a.output.resolve(),'target',expected,incoming=True)
        vm.call('migrate-incoming',{'uri':'file:'+str(stream.resolve())});r['incoming']=vm.migration_done()
        if vm.call('query-status')['running']:raise ValueError('unexpected run')
        r['target_a']=vm.sample(expected['a'])
        vm.bp('Z',expected['b']);vm.stop();r['target_b']=vm.sample(expected['b'])
        r['exit_code']=vm.exit()
        r['differences']={stage:[k for k in parent['source_'+stage]if parent['source_'+stage][k]!=r['target_'+stage][k]]for stage in ('a','b')}
        r['matching_source_states']=not any(r['differences'].values())
        r['output_matches']=(a.output/'target.bin').read_bytes()==(a.source/'source.bin').read_bytes()[parent['prefix_bytes']:]
    except Exception as e:r['errors'].append(str(e))
    finally:
        done.set()
        if vm:r['qmp']=vm.qmp.receipts;r['command']=vm.command;vm.close()
        r['seconds']=time.monotonic()-start
        r['diagnostic_passed']=r.get('matching_source_states',False)and r.get('output_matches',False)and r.get('exit_code')==33 and not r['errors']
        (a.output/'report.json').write_text(json.dumps(r,indent=2))
    print(json.dumps({k:r.get(k)for k in ('diagnostic_passed','errors','differences','seconds')},indent=2))
    return r['diagnostic_passed']
if __name__=='__main__':
    p=argparse.ArgumentParser()
    for name in ('binary','firmware','source','output'):p.add_argument('--'+name,type=Path,required=True)
    raise SystemExit(not run(p.parse_args()))
