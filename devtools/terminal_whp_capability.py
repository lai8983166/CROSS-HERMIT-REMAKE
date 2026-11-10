"""Read-only local WHP capability query. No partition or guest execution."""
import ctypes as C
import json
from pathlib import Path
from devtools.isolated_windows_vm import WORKER,identity


def collect():
    path=Path('C:/Windows/System32/WinHvPlatform.dll')
    r=dict(accepted=False,fullstate=False,partition_created=False,original_game_starts=0,host_input_actions=0,dll=identity(path),capabilities=[])
    api=C.WinDLL(str(path));f=api.WHvGetCapability
    f.argtypes=[C.c_uint32,C.c_void_p,C.c_uint32,C.POINTER(C.c_uint32)];f.restype=C.c_long
    for code,name in((0,'HypervisorPresent'),(1,'Features'),(2,'ExtendedVmExits'),(3,'ExceptionExitBitmap'),(0x1000,'ProcessorVendor'),(0x1003,'ProcessorXsaveFeatures')):
        b=C.create_string_buffer(64);got=C.c_uint32();hr=f(code,b,len(b),C.byref(got))
        r['capabilities'].append(dict(code=code,name=name,hresult=hex(hr&0xffffffff),written=got.value,raw=b.raw[:min(got.value,64)].hex()))
    return r


if __name__=='__main__':
    out=WORKER/'whp-capability-v1-20261110.json'
    if out.exists():raise ValueError('fresh capability receipt')
    r=collect();out.write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
