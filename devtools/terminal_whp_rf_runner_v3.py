"""One fresh CPU-only contrast per invocation, with a private Job deadline."""
import argparse,json
from devtools.isolated_windows_vm import WORKER,VMX,vmrun
from devtools.isolated_vm_bounded_query_v3 import _supervise,runtime_paths,completed
from devtools.terminal_whp_rf_probe_v3 import CASES

def main():
    p=argparse.ArgumentParser();p.add_argument('case',choices=CASES);a=p.parse_args()
    if str(VMX).lower()in vmrun(['list'],timeout=10).lower():raise ValueError('existing Windows VM must stay off')
    out=WORKER/('whp-rf-v3-20261110-'+a.case+'-supervision.json')
    if out.exists():raise ValueError('fresh supervision')
    code=('import sys,json;json.loads(sys.stdin.readline());sys.path[:0]='+repr(runtime_paths())+
          ';from devtools.terminal_whp_rf_probe_v3 import run;r=run('+repr(a.case)+');'+
          'print(json.dumps(dict(ok=not r["errors"],errors=r["errors"],remote_completion="observed",accepted=False,markers=r.get("markers"))))')
    r=_supervise({},20,code);out.write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
    return not completed(r)

if __name__=='__main__':raise SystemExit(main())
