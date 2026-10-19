"""Source-walk, ABI and complete-buffer verification of the original startup caller."""
import argparse
import hashlib
import json
from functools import lru_cache
from tools.school_font_caller import *
from tools.school_font_finish_verification import verify_report as verify_font
from tools.school_device_init_verification import unpack
from tools.school_owner_startup import project_image
from tools.school_renderer_init_verification import verify_buffer
from tools.school_font_caller_emulation import OWNER,TOP,COUNTER,HEAD,CACHE,dword,store


@lru_cache(maxsize=3)
def source_runs(phase):
    """Walk pinned instructions using source-proven success/nonnull/alignment/loop predicates.

    This does not consume recorded trace, observed CPU, or execute the audit emulator.
    REP includes its final zero-count observation, as Unicorn's code hook specifies.
    """
    raw=SOURCE.read_bytes();md=Cs(CS_ARCH_X86,CS_MODE_32)
    instructions={i.address:i for a,b in RANGES.items() for i in md.disasm(raw[a-BASE:b-BASE],a)}
    branches={0x4134EA:True,0x41351A:True,0x40DADC:True,0x40DAF4:True,
        0x40DB5B:True,0x40DBB4:True,0x40DC38:True,0x40DCA4:True,0x428A8C:True,
        0x56CECA:False,0x56CED8:False,0x56CEDF:True,0x56CEFF:False,0x56CF05:True,0x56CE80:False}
    reps={0x40D987:18,0x4142C7:18,0x40DAC7:18,0x40DB27:19,0x428A56:18,
        0x40DBA7:18,0x40DC07:19,0x40DC97:18,0x416C57:19,0x416CD7:18}
    at,stop=PHASES[phase];stack=[];runs=[];clears=0;gamma_tests=0
    while at!=stop:
        if len(runs)>10000:raise ValueError('font caller bounded source walk')
        i=instructions[at];nxt=at+i.size;count=1
        if i.mnemonic.startswith('rep '):
            if at==0x56CF01:count=(LAYER_BYTES,ARENA_BYTES)[clears]//4+1;clears+=1
            else:count=reps[at]
        runs.append(dict(va=at,count=count))
        if i.mnemonic=='call':
            target=int(i.op_str,16)
            if target!=0x56E810:stack.append(nxt);nxt=target
        elif i.mnemonic=='ret':nxt=stack.pop()
        elif i.mnemonic=='jmp':nxt=int(i.op_str,16)
        elif i.mnemonic.startswith('j'):
            if at==0x416C76:gamma_tests+=1;taken=gamma_tests==257
            else:taken=branches[at]
            if taken:nxt=int(i.op_str,16)
        at=nxt
    if stack!=([0x413546] if phase=='gamma' else []):raise ValueError('font caller source walk pending child stack')
    return runs


def expected_abi(phase,device):
    manager=OWNER+0x1058
    if phase=='bind':
        ent=[(0x40D970,0x413505,96,manager,[OWNER]),(0x4142B0,0x40D99F,184,OWNER,[])]
        ret=[(0x4142DC,0x40D99F,184,device),(0x56CE82,0x40D9B4,104,0),(0x40D9B7,0x413505,96,0)]
    elif phase=='queues':
        ent=[(0x40DAB0,0x413513,92,manager,[]),(0x40DB10,0x40DADA,184,manager,[4096]),
            (0x428A40,0x40DB45,280,4096,[LAYER_BYTES]),(0x40DB90,0x40DB6C,276,manager,[]),
            (0x56CEC0,0x40DBD5,376,HEADS,[HEADS,0,LAYER_BYTES]),(0x40DBF0,0x40DAF2,184,manager,[ARENA_BYTES]),
            (0x428A40,0x40DC22,280,ARENA_BYTES,[ARENA_BYTES]),(0x56CEC0,0x40DC56,288,ARENA,[ARENA,0,ARENA_BYTES]),
            (0x40DC80,0x40DC61,276,manager,[])]
        ret=[(0x56CE82,0x428AC2,288,HEADS),(0x428AC5,0x40DB45,280,HEADS),(0x56CF12,0x40DBD5,376,HEADS),
            (0x56CE82,0x40DBE7,284,0),(0x40DBEA,0x40DB6C,276,0),(0x56CE82,0x40DB7B,192,0),
            (0x40DB7E,0x40DADA,184,0),(0x56CE82,0x428AC2,288,ARENA),(0x428AC5,0x40DC22,280,ARENA),
            (0x56CF12,0x40DC56,288,ARENA),(0x40DCCB,0x40DC61,276,0),(0x56CE82,0x40DC70,192,0),
            (0x40DC73,0x40DAF2,184,0),(0x56CE82,0x40DB0C,100,0),(0x40DB0F,0x413513,92,0)]
    else:
        ent=[(0x416C40,0x413534,96,OWNER,[OWNER+0xB408]),(0x416CC0,0x413546,96,OWNER,[OWNER+0xB408])]
        ret=[(0x416CBC,0x413534,96,256)]
    return ([dict(va=hex(a),return_va=hex(b),sp=TOP-d,receiver=r,args=args) for a,b,d,r,args in ent],
        [dict(va=hex(a),return_va=hex(b),sp=TOP-d,eax=e) for a,b,d,e in ret])


def expected_allocations():
    c=source_contract()['allocator']
    return [dict(name=name,va='0x56e810',return_va='0x428a73',sp=TOP-384,
        args=[n,c['block_type'],c['file'],c['line']],pointer=p,bytes=n,initial_byte=0xCD,
        initial_sha256=hashlib.sha256(b'\xcd'*n).hexdigest(),adapter='declared debug CRT allocation')
        for name,p,n in (('heads',HEADS,LAYER_BYTES),('arena',ARENA,ARENA_BYTES))]


def verify_case(c):
    prior=c['finish_return'];device=unpack(prior['state']['owner']);device=dword(device,0xB210)
    # The complete parent verifier already binds this actual object to its owned interface map.
    calls=c['device']['native']['live_results']
    identity=next(r['result']['device'] for r in calls if r['op']=='create_device' and r['result'].get('device'))
    if identity['pointer']!=device:raise ValueError('font caller same owned device')
    image=bytearray(project_image({r['name']:r['result'] for r in c['constructor']['platform_calls']}))
    store(image,COUNTER-BASE,dword(image,COUNTER-BASE)+3600);store(image,HEAD-BASE,CACHE)
    for phase,(_,stop) in PHASES.items():
        row=c['caller_'+phase]
        if row['phase']!=phase or row['before_cpu']!=prior['cpu']:raise ValueError('font caller continuous original CPU')
        entry=c['device']['native']['cpu']
        cpu=dict(EIP=stop,ESP=TOP-88,EBP=TOP-4,EAX=0,EBX=entry['EBX'],ECX=OWNER+0x1058,EDX=OWNER+0x1058,
            ESI=entry['ESI'],EDI=entry['EDI'],EFLAGS=70)
        if phase=='gamma':cpu.update(ESP=TOP-192,EBP=TOP-100,EAX=identity['vtable'],ECX=device,EDX=device,ESI=TOP-180,EDI=TOP-100,EFLAGS=2)
        pending=dict(va=hex(stop),sp=cpu['ESP'],first_instruction_executed=False)
        if phase=='gamma':pending.update(device=device,vtable=identity['vtable'],method_offset=72,args=[device,1,OWNER+0xB408],target_read_executed=False)
        entries,returns=expected_abi(phase,device)
        if row['cpu']!=cpu or row['pending']!=pending or row['entries']!=entries or row['returns']!=returns:
            raise ValueError('font caller exact original ABI/CPU/unexecuted boundary')
        if row['instruction_runs']!=source_runs(phase):raise ValueError('font caller exact independent source control flow/REP/loop trace')
        writes={'bind':dict(stack=dict(count=51,bytes=204),manager=dict(count=2,bytes=8)),
            'queues':dict(stack=dict(count=200,bytes=800),manager=dict(count=6,bytes=24),counter=dict(count=2,bytes=8),
                heads=dict(count=LAYER_BYTES//4,bytes=LAYER_BYTES),arena=dict(count=ARENA_BYTES//4,bytes=ARENA_BYTES)),
            'gamma':dict(stack=dict(count=312,bytes=1248),gamma=dict(count=768,bytes=1536))}[phase]
        if row['native_writes']!=writes:raise ValueError('font caller exact bounded native writes/zeroing/gamma stores')
        alloc=[] if phase=='bind' else expected_allocations()
        if row['allocations']!=alloc:raise ValueError('font caller exact declared CRT allocation responses')
        if phase=='queues':store(image,COUNTER-BASE,dword(image,COUNTER-BASE)+LAYER_BYTES+ARENA_BYTES)
        owner=project_owner(unpack(prior['state']['owner']),phase,OWNER,device)
        verify_buffer(row['state']['owner'],owner)
        if (row['state']['image_sha256']!=hashlib.sha256(image).hexdigest() or row['state']['SEH']!=0
                or row['state']['stack_guards_unchanged'] is not True or row['state']['foreign_maps']!=prior['state']['foreign_maps']):
            raise ValueError('font caller whole image/SEH/stack/interface retention')
        for k in ('heaps','slot_heap','retained_heaps','second_heap','external_regions','retired_regions'):
            if row[k]!=prior[k]:raise ValueError('font caller complete retained font/cache/pixels/evidence '+k)
        if len(row['queues'])!=2:raise ValueError('font caller two guarded queue regions')
        for r,(name,p,n) in zip(row['queues'],(('heads',HEADS,LAYER_BYTES),('arena',ARENA,ARENA_BYTES))):
            if {k:v for k,v in r.items() if k!='buffer'}!=dict(name=name,pointer=p,guard_bytes=4096,payload_bytes=n):
                raise ValueError('font caller queue address/shape/guards')
            verify_buffer(r['buffer'],b'\xa5'*4096+(b'\xa5'*n if phase=='bind' else bytes(n))+b'\xa5'*4096)
        if row['manager_bound'] is not True or row['queues_initialized'] is not (phase!='bind') or row['gamma_table_generated'] is not (phase=='gamma'):
            raise ValueError('font caller exact stage authority')
        for k in ('gamma_device_call_executed','full413450_returned','retained_VM_advanced','GPU_drawing_or_Present','saved_live_pointers_resumable'):
            if row[k] is not False:raise ValueError('font caller unresolved device/startup/VM authority')
        prior=row


def verify_report(report):
    if report['schema_version']!=1 or report['source_contract']!=source_contract():raise ValueError('font caller source contract')
    verify_font(report['font_report'])
    for c in report['font_report']['cases']:verify_case(c)
    for k in ('one_continuous_trajectory_per_case','owned_helpers_unchanged'):
        if report[k] is not True:raise ValueError('font caller same continuous owned trajectory')
    for k in ('retained_VM_advanced','gamma_device_call_executed','full413450_returned','GPU_drawing_or_Present'):
        if report[k] is not False:raise ValueError('font caller unresolved native completion')
    return dict(cases=2,manager_bound=True,queues_initialized=True,queue_payload_bytes=LAYER_BYTES+ARENA_BYTES,
        gamma_entries=768,stop='0x416cfa',gamma_device_call_executed=False,full413450_returned=False,retained_VM_advanced=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('report');a=p.parse_args()
    print(json.dumps(verify_report(json.loads((ROOT/a.report).read_text(encoding='utf8')))))
