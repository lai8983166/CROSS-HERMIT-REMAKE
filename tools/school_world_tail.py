"""Original first paused world-tail policy, bounded to idle effects/empty queues."""
import hashlib,struct
from copy import deepcopy
from functools import lru_cache
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from tools.tactics_exit_emulation import SOURCE,SOURCE_SHA256,BASE

FUNCTIONS=(0x490FC0,0x49CC60,0x49C400,0x466880,0x40A100,0x493A30,
           0x48CE60,0x456B20,0x48D5D0,0x496450,0x427DE0)
EFFECT_STRIDE=0x520;SECONDARY_STRIDE=0x524


@lru_cache(maxsize=1)
def source_contract():
    raw=SOURCE.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA256:raise ValueError('tail source identity')
    md=Cs(CS_ARCH_X86,CS_MODE_32);functions=[]
    for a in FUNCTIONS:
        end=next((i.address+i.size for i in md.disasm(raw[a-BASE:a-BASE+4096],a) if i.mnemonic=='ret'),None)
        if end is None:raise ValueError('tail complete function range')
        functions.append({'va':hex(a),'end':hex(end),'sha256':hashlib.sha256(raw[a-BASE:end-BASE]).hexdigest()})
    checks={0x490FE7:('cmp','ecx, -1'),0x490FFE:('mov','byte ptr [ecx + 0x30994], 0'),
      0x49CC8E:('mov','byte ptr [edx + 0x115cb8], 0'),0x49C420:('mov','byte ptr [eax + 0x2f160], 0'),
      0x4668AF:('cmp','dword ptr [ebp - 8], 0xa'),0x4668D8:('call','0x40a100'),
      0x4668E0:('mov','byte ptr [ecx + 4], al'),0x4668F1:('mov','word ptr [eax + 0xa], dx'),
      0x40A153:('cmp','dword ptr [eax + 4], 0'),0x40A177:('mov','dword ptr [ebp - 0x10], 1'),
      0x493A5F:('cmp','dword ptr [ebp - 8], 5'),0x48CE86:('call','0x456b20'),
      0x48CE94:('call','0x48d5d0'),0x48D60D:('add','ecx, 0x2a80'),0x48D613:('call','0x427de0'),
      0x46B662:('ret','')}
    proof=[]
    for a,wanted in checks.items():
        i=next(md.disasm(raw[a-BASE:a-BASE+16],a))
        if (i.mnemonic,i.op_str)!=wanted:raise ValueError('tail original operands '+hex(a))
        proof.append({'va':hex(a),'hex':i.bytes.hex(),'mnemonic':i.mnemonic,'operands':i.op_str})
    return {'source_image_sha256':SOURCE_SHA256,'functions':functions,'instructions':proof,
       'effects':10,'effect_stride':EFFECT_STRIDE,'secondary_slots':5,'secondary_stride':SECONDARY_STRIDE,
       'scope':'First paused46B470 function return to declared audit driver; idle effects and empty forwarding only, no gameplay/task-frame/VM completion'}


def ranges():return tuple((int(r['va'],16),int(r['end'],16)) for r in source_contract()['functions'])


def idle_effects(buf):
    if len(buf)!=EFFECT_STRIDE*10:raise ValueError('tail complete effect region')
    out=bytearray(buf)
    for n in range(10):
        at=n*EFFECT_STRIDE
        if struct.unpack_from('<I',out,at+0x48+4)[0] or struct.unpack_from('<I',out,at+0x48+0x20)[0]:raise ValueError('active or child animation unsupported')
        out[at+4]=1
        count=struct.unpack_from('<H',out,at+10)[0];struct.pack_into('<H',out,at+10,(count+1)&65535)
    return bytes(out)


def project(inputs,regions):
    source_contract();out=deepcopy(regions)
    names=['cursor','window','menu','effects','secondary','control','outgoing_queue','incoming_queue','dispatch_mode','script_busy']
    sizes=[10,20,1,EFFECT_STRIDE*10,SECONDARY_STRIDE*5,50,20,20,1,1]
    if [r['name'] for r in out]!=names or [r['bytes'] for r in out]!=sizes:raise ValueError('tail complete owned regions')
    data={r['name']:bytearray.fromhex(r['hex']) for r in out}
    if any(len(data[r['name']])!=r['bytes'] for r in out):raise ValueError('tail complete owned buffer bytes')
    ctrl=data['control']
    if struct.unpack_from('<h',ctrl,2)[0]!=1 or any(ctrl[n] for n in (4,6,8,9,10)) or ctrl[24]!=1:raise ValueError('tail actual paused opening gates')
    if inputs['pointer_xy']!=[-1,-1] or inputs['selection_count']!=0:raise ValueError('tail no target selection')
    if data['dispatch_mode']!=b'\0' or data['script_busy']!=b'\0':raise ValueError('tail unsupported queue driver')
    for name in ('outgoing_queue','incoming_queue'):
        if data[name][8:20]!=bytes(12):raise ValueError('tail nonempty queue unsupported')
    if any(data['secondary'][i*SECONDARY_STRIDE] for i in range(5)):raise ValueError('tail active secondary effect unsupported')
    data['cursor'][8]=0;data['window'][16]=0;data['menu'][0]=0
    data['effects'][:]=idle_effects(data['effects'])
    for r in out:r['hex']=data[r['name']].hex()
    return out
