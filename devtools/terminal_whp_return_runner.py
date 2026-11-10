"""Bound the independent CPU-only WHP preflight in a private host Job."""
import json
from devtools.isolated_windows_vm import WORKER,VMX,vmrun
from devtools.isolated_vm_bounded_query_v3 import _supervise,runtime_paths


def main():
    need_off=vmrun(['list'],timeout=10)
    if str(VMX).lower()in need_off.lower():raise ValueError('do not overlap the existing Windows VM')
    out=WORKER/'whp-return-v1-supervision-20261110.json'
    if out.exists():raise ValueError('fresh supervision')
    code=('import sys,json;json.loads(sys.stdin.readline());sys.path[:0]='+repr(runtime_paths())+
          ';from devtools.terminal_whp_return_probe import run;'+
          'r=run('+repr(str(WORKER/'whp-return-v1-20261110'))+');'+
          'print(json.dumps(dict(ok=not r["errors"],errors=r["errors"],remote_completion="observed",accepted=False,phases=len(r["phases"]))))')
    r=_supervise({},30,code);out.write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
    return bool(r['errors']or r.get('timed_out')or not r.get('response',{}).get('ok'))


if __name__=='__main__':raise SystemExit(main())
