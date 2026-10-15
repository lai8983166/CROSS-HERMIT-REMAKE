"""Source projection for the remaining22 inactive mode11 templates."""
import struct
from copy import deepcopy
from tools.school_following_students import ROOT,SOURCE,SOURCE_SHA256,BASE,STRIDE,COUNT,data
from tools.school_deferred_units import source_contract as inactive_policy

INDICES=list(range(218,240))


def source_contract():
    return {'source_image_sha256':SOURCE_SHA256,'native_policy':inactive_policy(),'indices':INDICES,'next_slot':240,
      'source_jobs':[301,316,317,337,452],'record_state':0,'group':5,'mode':11,'work_2A7':1,
      'scope':'Continuous22 actual inactive template units, no activation/animation/regen/map/world/VM completion'}


def project(before):
    s=source_contract();d=data(before);ctrl=d['control'];w=d['works'];jobs=[]
    if struct.unpack_from('<h',ctrl,2)[0]!=1 or (ctrl[4],ctrl[24],ctrl[26])!=(1,1,5) or any(ctrl[i] for i in (6,9,10)):raise ValueError('template batch current opening/action gates')
    for i in INDICES:
        at=i*STRIDE;rp=struct.unpack_from('<I',w,at+0x258)[0];roff=rp-before[1]['pointer']
        if not 0<=roff<=len(d['records'])-176 or roff%176:raise ValueError('template batch record bounds')
        r=d['records'][roff:roff+176];job=struct.unpack_from('<H',r,2)[0]
        if not struct.unpack_from('<h',w,at)[0] or r[15]!=0 or r[164]!=5 or job not in s['source_jobs']:raise ValueError('template batch actual inactive records')
        if w[at+0x290]!=11 or w[at+0x292] or w[at+0x293] or w[at+0x2A7]!=1 or struct.unpack_from('<I',w,at+0x518)[0]:raise ValueError('template batch actual mode/queue/phase')
        w[at+8]&=0x7F;w[at+6:at+8]=b'\0\0';struct.pack_into('<h',w,at+10,0);w[at+0x293]=1
        struct.pack_into('<I',d['current_work'],0,before[0]['pointer']+at);jobs.append(job)
    if not struct.unpack_from('<h',w,240*STRIDE)[0]:raise ValueError('template batch next occupied240')
    out=deepcopy(before)
    for row in out:row['hex']=d[row['name']].hex()
    return {'after':out,'unit_indices':INDICES,'unit_jobs':jobs,'units_completed':22,'templates_activated':0,'next_slot':240,'world_completed':False}
