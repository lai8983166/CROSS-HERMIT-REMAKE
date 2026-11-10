"""Recheck a retained bounded source and reject concrete independent corruptions."""
import argparse
import copy
import json
from pathlib import Path
from devtools.terminal_tcg_longmode_probe import validate


def main(source, output):
    report=json.loads((source/'report.json').read_bytes())
    raw=(source/'guest.bin').read_bytes()
    def check(data,states):
        result=copy.deepcopy(report)
        return validate(data,report['expected'],states,result)
    states=report['states']
    if not check(raw,states): raise ValueError('baseline rejected')
    rejected={}
    for name,offset in [('high_fip',512+12),('xmm15',512+160+15*16)]:
        data=bytearray(raw);data[offset]^=1
        rejected[name]=not check(bytes(data),copy.deepcopy(states))
    for name in ('vp_running','wrong_cpu','unstable_read'):
        sample=copy.deepcopy(states)
        if name=='vp_running':
            for s in sample:s['vp_stopped'][1]['stopped']=False
        elif name=='wrong_cpu':
            for s in sample:s['cpu']=1
        else: sample[1]['fop']^=1
        rejected[name]=not check(raw,sample)
    result=dict(baseline_passed=True,tamper_rejected=rejected,accepted=False,
                scope='Retained long-mode fixture only; not native game acceptance')
    with output.open('x')as f:json.dump(result,f,indent=2)
    print(json.dumps(result))
    if not all(rejected.values()):raise SystemExit(1)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('output',type=Path)
    a=p.parse_args();main(a.source,a.output)
