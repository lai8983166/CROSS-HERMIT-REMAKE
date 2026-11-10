"""Offline authentication of the bounded WHP fixture; always refuses fullstate."""
import argparse
import hashlib
import json
from pathlib import Path
import struct


def need(v,message):
    if not v:raise ValueError(message)


def raw(reg,name):
    b=bytes.fromhex(reg[str(name)]);need(len(b)==16,'complete register union');return b


def value(reg,name):return int.from_bytes(raw(reg,name)[:8],'little')


def full_tag(fx):
    top=(int.from_bytes(fx[2:4],'little')>>11)&7;abridged=fx[4];result=0
    for physical in range(8):
        if not abridged&(1<<physical):tag=3
        else:
            logical=(physical-top)&7;b=fx[32+16*logical:42+16*logical]
            mantissa=int.from_bytes(b[:8],'little');exponent=int.from_bytes(b[8:10],'little')&0x7fff
            if exponent==0 and mantissa==0:tag=1
            elif exponent in(0,0x7fff) or not(mantissa>>63):tag=2
            else:tag=0
        result|=tag<<(physical*2)
    return result


def verify(r,read):
    need(r['accepted'] is False and r['fullstate'] is False and r['fullABI'] is False,'fixture must not claim game/fullstate acceptance')
    need(not r['errors'] and r['original_game_starts']==0 and r['windows_boots']==0,'bounded fixture scope')
    need(r['vp_count']==2 and r['committed_mapped_bytes']==65536 and r['reserved_address_bytes']==2**32,'exact synthetic resources')
    need(r['cleanup']==['deleted VP 1','deleted VP 0','unmapped 64 KiB','deleted partition','released 4 GiB reservation'],'actual clean resource completion')
    need(r['all_runs_joined_at_cleanup'],'no active VP at cleanup')
    need(r['register_write_calls_after_first_run']==0 and r['injected_guest_events']==0,'observer control scope')
    initial=read(r['initial_memory']);need(len(initial)==65536,'exact initial bytes')
    need(initial[0x3076:0x307b]==bytes.fromhex('e885efffff'),'original CALL target and natural return')
    need(initial[0x307b:0x3086]==bytes.fromhex('ff8300020000e97a1f0000'),'natural one-count consumer then next boundary')
    need(len(r['phases'])==3,'three distinct boundaries')
    expected=(('callee-entry',0x2000,0),('natural-return',0x307b,0),('after-consumer',0x5000,1))
    rows=[]
    for index,(p,(name,target,marker))in enumerate(zip(r['phases'],expected)):
        need(p['name']==name and p['all_run_threads_joined'],'all VP calls returned at boundary')
        mem=read(p['memory']);need(len(mem)==65536 and mem[0x1000:0x4000]==initial[0x1000:0x4000],'unchanged original code')
        for vp in(0,1):
            ex=p['exits'][vp];exraw=bytes.fromhex(ex['raw']);reg=p['registers'][vp];base=0x8000+vp*0x1000
            need(len(exraw)==224 and ex['hresult']=='0x0','complete successful exit record')
            decoded=dict(reason=struct.unpack_from('<I',exraw)[0],rip=struct.unpack_from('<Q',exraw,32)[0],access_info=struct.unpack_from('<I',exraw,68)[0],gpa=struct.unpack_from('<Q',exraw,72)[0],gva=struct.unpack_from('<Q',exraw,80)[0])
            need(all(ex[k]==v for k,v in decoded.items()),'decoded exit matches raw record')
            need(ex['reason']==1 and ex['access_info']&3==2 and ex['rip']==target and ex['gpa']==target,'exact execute-denial target')
            if ex['access_info']&8:need(ex['gva']==target,'valid exit GVA')
            need(value(reg,0x10)==target and value(reg,0x11)==struct.unpack_from('<Q',exraw,40)[0],'live PC/flags agree with exit')
            need(value(reg,0x11)&0x10000,'RF effect must be preserved, never silently cleared')
            sp=0xaf00+vp*0x1000-(4 if index==0 else 0)
            need(value(reg,4)==sp,'actual CALL/RET stack transition')
            if index==0:need(mem[sp:sp+4]==struct.pack('<I',0x307b),'original return address on stack')
            need(mem[base+0x200:base+0x204]==struct.pack('<I',marker),'consumer executes exactly once after release')
            for n in list(range(0x21,0x27))+[0x80000000,0x80000001,0x80000002,0x80000004,0x80000006]:
                need(raw(reg,n)==raw(r['registers_initialized'][vp],n),'DR and pending state preserved')
            xs=p['xsave'][vp];x=read(xs['file'])
            need(xs['hresult']=='0x0' and len(x)==xs['written'] and 576<=len(x)<=16384,'valid bounded XSAVE payload')
            if 'xsave_reread'in p:need(x==read(p['xsave_reread'][vp]['file']),'raw XSAVE stable on same-stop reread')
            if index==0:continue # XSTATE_BV init-state semantics: no fabricated FCW=0.
            fx=mem[base+0x400:base+0x600]
            need((int.from_bytes(x[512:520],'little')&3)==3,'x87/SSE state is present')
            need(raw(reg,0x1018)==fx[:16] and raw(reg,0x1019)==fx[16:32],'raw control aggregates equal executed FXSAVE')
            need(x[:32]==fx[:32],'XSAVE control header equals executed FXSAVE')
            for n in range(8):
                need(raw(reg,0x1010+n)[:10]==fx[32+n*16:42+n*16]==x[32+n*16:42+n*16],'80-bit logical FP stack order')
                need(raw(reg,0x1000+n)==fx[160+n*16:176+n*16]==x[160+n*16:176+n*16]==initial[base+0x100+n*16:base+0x110+n*16],'nonzero XMM patterns agree')
            need(((int.from_bytes(fx[2:4],'little')>>11)&7)==4 and fx[4]==0xb0,'nonzero TOP with physical FTW holes')
            need(full_tag(fx)==0x30ff,'full x87 tag reconstruction')
            cw,sw,op=struct.unpack_from('<H',fx)[0],struct.unpack_from('<H',fx,2)[0],struct.unpack_from('<H',fx,6)[0]
            fip,fcs,fdp,fds=struct.unpack_from('<I',fx,8)[0],struct.unpack_from('<H',fx,12)[0],struct.unpack_from('<I',fx,16)[0],struct.unpack_from('<H',fx,20)[0]
            cpuid7=struct.unpack_from('<I',mem,base+0x244)[0]
            need(cpuid7&(1<<13) and fcs==0 and fds==0,'measured deprecated FCS/FDS semantics')
            cs=raw(reg,0x13);attr=struct.unpack_from('<H',cs,14)[0]
            need(attr&0x4000 and not(attr&0x2000) and not(value(reg,0x2001)&0x400),'32-bit protected mode only')
            need(value(reg,0x1c)&1 and not(value(reg,0x1f)&8),'CR0.PE and CR4.DE=0; DR4/5 are not independent fields')
            need(fip==r['fixture']['last_fp'],'actual last x87 instruction pointer')
            if cw==0x37b:
                need(sw&0x8084==0x8084 and op==0x4b3 and fdp==base+8,'actual pending unmasked FDIV opcode/data pointer')
                need(initial[fip:fip+6]==bytes.fromhex('dcb308000000'),'original FDIV instruction')
            else:
                need(cw==0x37f and op==0 and fdp==0,'v1 ordinary native floating-point observation')
                need(int.from_bytes(mem[base+0x308:base+0x30a],'little')==full_tag(fx),'independent executed FNSTENV full tag')
            rows.append(dict(phase=name,vp=vp,fcw=cw,fsw=sw,ftw=fx[4],full_tag=full_tag(fx),fop=op,fip=fip,fdp=fdp,fcs=fcs,fds=fds,xstate_bv=int.from_bytes(x[512:520],'little'),xcomp_bv=hex(int.from_bytes(x[520:528],'little'))))
    return dict(accepted=False,fullstate=False,fullABI=False,fixture_boundary_and_raw_fp_checks_passed=True,original_game_starts=0,rflags_transparent=False,raw_fields=rows,remaining=['RF=1 at EPT execute exit; unknown pre-exit RF cannot be cleared by assumption.','64-bit/WOW64 compatibility mode, hidden high descriptor bases, existing enabled debug-break behavior and Windows ownership have not been tested.','No independent DR4/5 storage; no canonical57 acceptance.'])


def authenticate(report,sha):
    report=Path(report).resolve();b=report.read_bytes();need(hashlib.sha256(b).hexdigest()==sha,'fixed report identity')
    def read(row):
        p=Path(row['path']).resolve();need(p.parent==report.parent,'owned evidence directory')
        need(0<p.stat().st_size<=65536,'bounded evidence file')
        b=p.read_bytes();need(len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],'exact original evidence bytes');return b
    r=json.loads(b);result=verify(r,read);result['source_report_sha256']=sha;return result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--report',required=True);p.add_argument('--sha256',required=True);p.add_argument('--output',required=True);a=p.parse_args()
    out=Path(a.output);need(not out.exists(),'fresh verification output')
    result=authenticate(a.report,a.sha256);out.write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
