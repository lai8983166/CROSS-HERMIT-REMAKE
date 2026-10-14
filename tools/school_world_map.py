"""Independent original clock and locked-opening map-frame source projection."""
import hashlib
import struct
from copy import deepcopy
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from tools.tactics_exit_emulation import SOURCE,SOURCE_SHA256,BASE

RANGES=((0x493630,0x493665),(0x467B60,0x467C19),(0x46E9C0,0x46EA04),
 (0x43B350,0x43B3B6),(0x43D230,0x43D266),(0x43D130,0x43D19A),(0x43D0C0,0x43D122),
 (0x43B530,0x43B70E),(0x43B710,0x43B7AD),(0x43B7B0,0x43B8B0),
 (0x43C9C0,0x43CAA6),(0x43C700,0x43C917),(0x4406F0,0x440973),
 (0x481610,0x4816BB),(0x415040,0x415069),(0x56CEC0,0x56CF18))
MAP_STATE_BASE=0x2646C
MAP_STATE_BYTES=0x265F0-MAP_STATE_BASE


def source_contract(raw=None):
    raw=SOURCE.read_bytes() if raw is None else raw
    if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA256:raise ValueError('world map source identity')
    md=Cs(CS_ARCH_X86,CS_MODE_32)
    checks={0x46B4D3:('call','0x467b60'),0x46B4DB:('call','0x46e9c0'),0x46B4E3:('call','0x49b180'),
        0x467B80:('movsx','ecx, byte ptr [eax + 0x108b48]'),0x467B92:('movsx','eax, byte ptr [edx + 0x108b3a]'),
        0x467BC3:('jg','0x467c06'),0x467BCD:('call','0x415040'),
        0x467BE0:('mov','dword ptr [edx + 0x2e6f4], ecx'),0x467BF0:('jge','0x467c06'),
        0x43B5C0:('cmp','dword ptr [ebp - 0x14], 0x240'),0x43B5C7:('jge','0x43b6eb'),
        0x43B753:('cmp','dword ptr [ebp - 0xc], 0x23a'),0x43B75A:('jge','0x43b790'),
        0x43D107:('call','0x56cec0'),0x56CF01:('rep stosd','dword ptr es:[edi], eax')}
    proof=[]
    for a,wanted in checks.items():
        i=next(md.disasm(raw[a-BASE:a-BASE+16],a))
        if (i.mnemonic,i.op_str)!=wanted:raise ValueError('world map source instruction '+hex(a))
        proof.append({'va':hex(a),'hex':i.bytes.hex(),'mnemonic':i.mnemonic,'operands':i.op_str})
    functions=[{'va':hex(a),'end':hex(b),'sha256':hashlib.sha256(raw[a-BASE:b-BASE]).hexdigest()} for a,b in RANGES]
    code='\n'.join(i.op_str for a,b in RANGES for i in md.disasm(raw[a-BASE:b-BASE],a))
    for required in ['ecx, dword ptr [eax + 0xa8]','dword ptr [edx + 0xa4], ecx',
                     'dword ptr [edx + 0xa8], eax','0x240','0x23a']:
        if required not in code:raise ValueError('world map swap/hover instruction identity '+required)
    return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'functions':functions,'instructions':proof,
        'map_dimensions':[64,96],'hover_screen_y':[30,605],'pixel_screen_y':[30,599],
        'timer_word_offsets':[0x2E6F4,0x2E6F8,0x2E6FC],'timer_gate_offsets':[0x108B48,0x108B3A],
        'buffer_pointer_offsets':[0xA0,0xA4,0xA8],'cleared_plane':'original_slot_A8',
        'map_state_offset':MAP_STATE_BASE,'map_state_bytes':MAP_STATE_BYTES,
        'scope':'Closed original opening gates and finite declared timer/pointer probes; no full world/AI/VM/settlement'}


def i32(value):return (value+0x80000000)%0x100000000-0x80000000
def i16(value):return (value+0x8000)%0x10000-0x8000
def quotient(value,divisor):return (abs(value)//divisor)*(-1 if value<0 else 1)


def clock_step(opening,event,remaining,elapsed,limit):
    if any(type(v) is not int for v in (opening,event,remaining,elapsed,limit)) or not 0<=opening<=255 or not 0<=event<=255:
        raise ValueError('clock input types/range')
    if any(not -0x80000000<=v<=0x7FFFFFFF for v in (remaining,elapsed,limit)):raise ValueError('clock signed32 input')
    if opening or not event:return {'remaining':remaining,'elapsed':elapsed,'limit':limit,'return_eax':0,'increment_called':False}
    # Original signed jg against INT_MAX cannot succeed for any signed32 limit.
    next_remaining=i32(remaining-1)
    return {'remaining':max(0,next_remaining),'elapsed':i32(elapsed+1),'limit':limit,
        'return_eax':1 if next_remaining<0 else 0,'increment_called':True}


def pointer_outputs(mouse,camera=(0,0),dimensions=(64,96)):
    if not isinstance(mouse,(list,tuple)) or len(mouse)!=2 or any(type(v) is not int or not -0x80000000<=v<=0x7FFFFFFF for v in mouse):
        raise ValueError('pointer signed32 coordinates')
    if tuple(dimensions)!=(64,96) or len(camera)!=2 or any(type(v) is not int or not -32768<=v<=32767 for v in camera):
        raise ValueError('pointer map/camera')
    x,y=mouse;cx,cy=camera;relative_y=i32(y-30)
    tile=[-1,-1];pixel=[-1,-1]
    if 0<=relative_y<=575:
        def add_div(a,b,d):return quotient(a,d)+quotient(b,d)+quotient(a-quotient(a,d)*d+b-quotient(b,d)*d,d)
        tile=[i16(add_div(x,cx,32)),i16(add_div(relative_y,cy,16))]
        if tile[0]>=64 or tile[1]>=96:tile=[-1,-1]
    if 0<=relative_y<=569:pixel=[i16(x+cx),i16(relative_y+cy)]
    return {'tile':tile,'pixel':pixel}


def project_map_frame(before,mouse=(0,0)):
    source_contract();out=deepcopy(before)
    if [r['name'] for r in out]!=['map_slots','map_state','fog_history','fog_current','fog_previous','minimap_globals']:
        raise ValueError('world map owned regions')
    data={r['name']:bytearray.fromhex(r['hex']) for r in out}
    sizes=[12,MAP_STATE_BYTES,6144,6144,6144,32]
    if any(len(data[r['name']])!=n or r['bytes']!=n for r,n in zip(out,sizes)):raise ValueError('world map complete sizes')
    slots=list(struct.unpack('<3I',data['map_slots']))
    if len(set(slots))!=3 or slots!=[r['pointer'] for r in out[2:5]]:raise ValueError('world map buffer ownership')
    state=data['map_state']
    def index(offset):return offset-MAP_STATE_BASE
    if list(state[index(0x26595):index(0x26599)])!=[1]*4:raise ValueError('only actual locked opening map supported')
    camera=struct.unpack_from('<2h',state,index(0x265A6));outputs=pointer_outputs(mouse,camera)
    struct.pack_into('<3I',data['map_slots'],0,slots[0],slots[2],slots[1]);data['fog_previous'][:]=b'\0'*6144
    struct.pack_into('<2h',state,index(0x265AA),*outputs['tile'])
    struct.pack_into('<2h',state,index(0x265AE),*outputs['pixel'])
    struct.pack_into('<I',state,index(0x265D8),0)
    struct.pack_into('<Ihh',state,index(0x265E0),0,-1,-1)
    struct.pack_into('<I',state,index(0x265E8),0)
    x,y,w,h=struct.unpack_from('<4I',state,0)
    struct.pack_into('<8I',data['minimap_globals'],0,x,y,(x+w)&0xFFFFFFFF,(y+h)&0xFFFFFFFF,x,y,w,h)
    for row in out:row['hex']=data[row['name']].hex()
    return out
