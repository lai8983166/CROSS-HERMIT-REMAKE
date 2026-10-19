"""Original void gamma invocation and complete413450 startup success return."""
import argparse
import hashlib
import json
import struct
from functools import lru_cache
from tools.school_font_caller import ROOT,SOURCE,SOURCE_SHA256,BASE,Cs,CS_ARCH_X86,CS_MODE_32,gamma_bytes

RANGES={0x416CFA:0x416D17,0x413546:0x41355B,0x56CE80:0x56CE83}
PHASES={'gamma':(0x416CFA,0x413546),'return':(0x413546,0x22000000)}
GAMMA_TRACE=[0x416CFA,0x416CFD,0x416CFF,0x56CE80,0x56CE82,
    0x416D04,0x416D05,0x416D06,0x416D07,0x416D0A,0x416D0C,0x56CE80,0x56CE82,
    0x416D11,0x416D13,0x416D14]
RETURN_TRACE=[0x413546,0x413548,0x413549,0x41354A,0x41354B,0x41354E,
    0x413550,0x56CE80,0x56CE82,0x413555,0x413557,0x413558]
CAPTURE_PREFIX=bytes.fromhex('558becff7510ff750cff7508b8')
CAPTURE_SUFFIX=bytes.fromhex('ffd08be55dc20c00')
API_REFERENCE='https://learn.microsoft.com/en-sg/previous-versions/windows/embedded/ms889716(v=msdn.10)'


def capture_code(target):
    if not isinstance(target,int) or not 0<target<=0xFFFFFFFF:raise ValueError('startup return actual x86 gamma method required')
    return CAPTURE_PREFIX+struct.pack('<I',target)+CAPTURE_SUFFIX


@lru_cache(maxsize=1)
def source_contract():
    raw=SOURCE.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA256:raise ValueError('startup return source SHA')
    md=Cs(CS_ARCH_X86,CS_MODE_32);proof=[]
    checks={0x416CFA:('call','dword ptr [eax + 0x48]'),0x416CFD:('cmp','esi, esp'),
        0x416D14:('ret','4'),0x413546:('xor','eax, eax'),0x41354B:('add','esp, 0x48'),
        0x413550:('call','0x56ce80'),0x413558:('ret','0x14')}
    for at,expected in checks.items():
        i=next(md.disasm(raw[at-BASE:at-BASE+16],at))
        if (i.mnemonic,i.op_str)!=expected:raise ValueError('startup return instruction '+hex(at))
        proof.append(dict(va=hex(at),hex=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str))
    return dict(source_image_sha256=SOURCE_SHA256,instructions=proof,
        functions=[dict(va=hex(a),end=hex(b),sha256=hashlib.sha256(raw[a-BASE:b-BASE]).hexdigest()) for a,b in RANGES.items()],
        phases={p:dict(start=hex(a),stop=hex(b)) for p,(a,b) in PHASES.items()},
        gamma_trace=[hex(a) for a in GAMMA_TRACE],return_trace=[hex(a) for a in RETURN_TRACE],
        gamma=dict(method_offset=72,flags=1,bytes=1536,return_type='void',HRESULT_available=False,
            EAX='observed register bits only; no success/failure meaning',reference=API_REFERENCE),
        capture=dict(prefix_hex=CAPTURE_PREFIX.hex(),target_bytes=4,suffix_hex=CAPTURE_SUFFIX.hex(),bytes=25,
            owned_process_only=True,original_game_code_patched=False),
        gamma_callee_ret_bytes=4,startup_ret_bytes=20,startup_success=0,
        external_cleanup_restores_device_and_desktop_gamma=True,real_upstream_caller_executed=False,
        inherited_cache_repaired=False,retained_VM_advanced=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
    if path.exists():p.error('fresh immutable startup return source required')
    path.write_text(json.dumps(source_contract(),indent=2)+chr(10),encoding='utf8',newline=chr(10))
