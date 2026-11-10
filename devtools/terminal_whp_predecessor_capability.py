"""Bounded read-only documented WHP PMU/LBR capability preflight; no partition."""
import ctypes as C
import json
from pathlib import Path
from devtools.isolated_windows_vm import identity

def collect():
    dll=Path('C:/Windows/System32/WinHvPlatform.dll')
    sdk=Path('C:/Program Files (x86)/Windows Kits/10/Include/10.0.26100.0/um/WinHvPlatformDefs.h')
    f=C.WinDLL(str(dll)).WHvGetCapability
    f.argtypes=[C.c_uint32,C.c_void_p,C.c_uint32,C.POINTER(C.c_uint32)];f.restype=C.c_long
    buffer=C.create_string_buffer(bytes([0xa5])*64);written=C.c_uint32()
    hr=f(0x1009,buffer,64,C.byref(written));valid=hr==0 and written.value==8
    bits=int.from_bytes(buffer.raw[:8],'little')if valid else None
    return dict(accepted=False,fullstate=False,partition_created=False,host_input_actions=0,
                dll=identity(dll),sdk=identity(sdk),code=0x1009,name='ProcessorPerfmonFeatures',
                hresult=hex(hr&0xffffffff),written=written.value,buffer_raw=buffer.raw.hex(),
                valid=valid,pmu_supported=bool(bits&1)if valid else None,lbr_supported=bool(bits&2)if valid else None,
                actual_predecessor_obtained=False,event_history_obtained=False,
                note='Capability only. Failure is unknown, never interpreted as zero; TLFS identifiers are not WHV register identifiers.')

if __name__=='__main__':
    p=Path('analysis/terminal-wait-whp-predecessor-capability-v1-20261110.json')
    if p.exists():raise ValueError('fresh receipt required')
    r=collect()
    with p.open('x',encoding='utf8')as f:json.dump(r,f,indent=2)
    print(json.dumps(r,indent=2))
