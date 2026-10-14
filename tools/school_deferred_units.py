"""Source phase0 mode11 early exit for the first two inactive templates."""
import hashlib,struct
from copy import deepcopy
from functools import lru_cache
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from tools.school_following_students import ROOT,SOURCE,SOURCE_SHA256,BASE,STRIDE,COUNT,data


@lru_cache(maxsize=1)
def source_contract():
    raw=SOURCE.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA256:raise ValueError('deferred source executable')
    md=Cs(CS_ARCH_X86,CS_MODE_32);bodies=[]
    for va in (0x479F40,0x46B0B0,0x46B0F0):
        end=next(i.address+i.size for i in md.disasm(raw[va-BASE:va-BASE+4096],va) if i.mnemonic=='ret')
        bodies.append({'va':hex(va),'end':hex(end),'sha256':hashlib.sha256(raw[va-BASE:end-BASE]).hexdigest()})
    if struct.unpack_from('<I',raw,0x475CE3-BASE+11*4)[0]!=0x475AFE:raise ValueError('deferred original mode11 inactive dispatch')
    checks={0x475B05:('call','0x479f40'),0x479F93:('call','0x46b0b0'),0x479FA1:('call','0x46b0f0'),
      0x479FA9:('mov','word ptr [eax + 0xa], 0'),0x479FBA:('mov','byte ptr [eax], dl'),
      0x47A224:('mov','eax, 1'),0x46B7E3:('je','0x46b7ea'),0x46B7E5:('jmp','0x46b9f7')}
    proof=[]
    for va,wanted in checks.items():
        i=next(md.disasm(raw[va-BASE:va-BASE+16],va))
        if (i.mnemonic,i.op_str)!=wanted:raise ValueError('deferred exact operand '+hex(va))
        proof.append({'va':hex(va),'hex':i.bytes.hex(),'mnemonic':i.mnemonic,'operands':i.op_str})
    return {'source_image_sha256':SOURCE_SHA256,'functions':bodies,'instructions':proof,'indices':[215,216],'next_slot':217,
      'handler_return':1,'template_activation':False,'scope':'First two actual state0 mode11 templates phase0, natural early return; no animation/regen/map or template activation'}


def ranges():return tuple((int(r['va'],16),int(r['end'],16)) for r in source_contract()['functions'])


def project(before):
    source_contract();d=data(before);ctrl=d['control'];w=d['works'];units=[]
    if struct.unpack_from('<h',ctrl,2)[0]!=1 or (ctrl[4],ctrl[24],ctrl[26])!=(1,1,5) or any(ctrl[i] for i in (6,9,10)):raise ValueError('deferred natural action/closed command/AI gates')
    for i,job in ((215,337),(216,301)):
        at=i*STRIDE;rec=struct.unpack_from('<I',w,at+0x258)[0];roff=rec-before[1]['pointer']
        if roff%176 or not 0<=roff<=len(d['records'])-176:raise ValueError('deferred original record bounds')
        r=d['records'][roff:roff+176]
        if struct.unpack_from('<h',w,at)[0]==0 or r[15]!=0 or r[164]!=5 or struct.unpack_from('<H',r,2)[0]!=job:raise ValueError('deferred unchanged inactive record')
        if w[at+0x290]!=11 or w[at+0x292] or w[at+0x293] or w[at+0x2A7]!=1 or struct.unpack_from('<I',w,at+0x518)[0]:raise ValueError('deferred exact inactive mode/phase/empty queue')
        w[at+8]&=0x7F;w[at+6]=0;w[at+7]=0;struct.pack_into('<h',w,at+10,0);w[at+0x293]=1
        struct.pack_into('<I',d['current_work'],0,before[0]['pointer']+at)
        units.append({'index':i,'job':job,'record_state':0,'phase_after':1,'handler_return':1,'unit_return':1,
          'animation_executed':False,'regeneration_executed':False,'map_executed':False,'activated':False})
    if struct.unpack_from('<h',w,217*STRIDE)[0]==0:raise ValueError('deferred exact next occupied scene slot')
    out=deepcopy(before)
    for row in out:row['hex']=d[row['name']].hex()
    return {'after':out,'units':units,'next_slot':217,'templates_activated':0,'world_completed':False}
