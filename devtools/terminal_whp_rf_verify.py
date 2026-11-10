"""Offline raw-byte RF contrast verification. Never authorizes RF normalization."""
import argparse,hashlib,json,struct,zipfile
from pathlib import Path,PureWindowsPath

def need(v,message):
    if not v:raise ValueError(message)

def digest(b):return hashlib.sha256(b).hexdigest()
def key(p):return str(PureWindowsPath(p)).lower()
def scalar(reg,n):return int.from_bytes(bytes.fromhex(reg[str(n)])[:8],'little')

class Bundle:
    def __init__(self,path,sha):
        p=Path(path);need(digest(p.read_bytes())==sha,'fixed capsule SHA')
        self.zip=zipfile.ZipFile(p)
        need(sum(x.file_size for x in self.zip.infolist())<=8*1024*1024,'bounded capsule')
        self.manifest=json.loads(self.zip.read('manifest.json'))
        self.files={key(x['path']):x for x in self.manifest['files']}
        need(len(self.files)==len(self.manifest['files']),'unique paths')
    def read(self,p):
        row=self.files[key(p)];b=self.zip.read('sha256/'+row['sha256'])
        need(len(b)==row['bytes'] and digest(b)==row['sha256'],'original capsule bytes')
        return b
    def close(self):self.zip.close()

def verify(read,report_paths):
    cases={};sources=[]
    for path in report_paths:
        report_bytes=read(path);r=json.loads(report_bytes);case=r['case']
        # v2 is a retained guard refusal, never quietly promoted to native success.
        name=case if not r['errors'] else ('ret-baseline' if 'v1-'in str(path) else 'ret-before-ept-guard-refusal')
        need(name not in cases,'unique contrast source')
        need(r['accepted'] is False and r['fullstate'] is False and r['fullABI'] is False,'no fullstate promotion')
        need(r['vp_count']==2 and r['reserved_address_bytes']==2**32 and r['committed_mapped_bytes']==65536,'bounded owned resources')
        need(r['original_game_starts']==r['windows_boots']==r['host_input_actions']==r['injected_events']==0,'scope')
        need(r['all_runs_joined_at_cleanup'] and r['cleanup']==['deleted VP 1','deleted VP 0','unmapped 64 KiB','deleted partition','released 4 GiB reservation'],'explicit cleanup')
        for row in (r['implementation'],r['parent_implementation']):
            b=read(row['path']);need(len(b)==row['bytes'] and digest(b)==row['sha256'],'frozen implementation')
        def artifact(row):
            b=read(row['path']);need(len(b)==row['bytes'] and digest(b)==row['sha256'],'raw artifact identity');return b
        initial=artifact(r['initial_memory']);need(len(initial)==65536,'exact memory extent')
        need(initial[0x3076:0x307b]==bytes.fromhex('e885efffff'),'original near CALL')
        need(initial[0x307b:0x3086]==bytes.fromhex('ff8300020000e97a1f0000'),'original consumer')
        tail=r['fixture']['tail_start'];kind=r['fixture']['kind']
        tail_bytes=bytes.fromhex('c3'if kind=='ret'else '589c810c24000001000e50cf')
        need(initial[tail:tail+len(tail_bytes)]==tail_bytes,'actual near RET or RF=1 IRETD program')
        handler=bytes.fromhex('60ff83040200000f21f08983080200008b44242089830c0200008b442428898310020000814c24280000010061cf')
        need(initial[0x4000:0x4000+len(handler)]==handler,'actual guest #DB handler with RF=1 IRETD')
        need(initial[0x6808:0x6810]==struct.pack('<HHBBH',0x4000,8,0,0x8e,0),'guest IDT #DB gate')
        if name=='ret-baseline':need(r['errors']==["ValueError('expected boundary after-consumer-halt')"],'retain initial HLT predicate failure')
        elif name=='ret-before-ept-guard-refusal':need(r['errors']==["ValueError('no consumer or #DB handler before EPT')"],'retain preemption guard refusal')
        else:need(not r['errors'] and r['experiment_completed'],'successful bounded native contrast')
        expected_names=['callee-entry']+(['return-ept']if 'ept'in case else [])+([]if name=='ret-before-ept-guard-refusal'else ['after-consumer-halt'])
        need([p['name']for p in r['phases']]==expected_names,'complete ordered boundaries')
        rows=[]
        for p in r['phases']:
            mem=artifact(p['memory']);need(len(mem)==65536 and mem[0x1000:0x6000]==initial[0x1000:0x6000],'unchanged guest code')
            need(p['all_run_threads_joined'] and p['stable_reread'],'all VP calls joined and stable')
            for vp in (0,1):
                ex=p['exits'][vp];raw=bytes.fromhex(ex['raw']);reg=p['registers'][vp];data=0x8000+vp*0x1000
                need(len(raw)==224 and ex['hresult']=='0x0','complete native exit')
                reason=struct.unpack_from('<I',raw)[0];pc,flags=struct.unpack_from('<QQ',raw,32)
                need((reason,pc,flags)==(ex['reason'],ex['rip'],ex['rflags']),'raw exit decoding')
                need(pc==scalar(reg,16) and flags==scalar(reg,17),'actual PC and flags readback')
                target={'callee-entry':(1,0x2000),'return-ept':(1,0x307b),'after-consumer-halt':(8,0x5001)}[p['name']]
                need((reason,pc)==target,'exact stop boundary; HLT is retired')
                if reason==1:
                    need(struct.unpack_from('<I',raw,68)[0]&3==2 and struct.unpack_from('<Q',raw,72)[0]==pc,'execute denial at actual PC')
                    need(flags&0x10000,'raw EPT RF must not be normalized')
                need(scalar(reg,33)==0x307b and scalar(reg,38)==0x401,'original enabled execution breakpoint retained')
                expected_sp=0xaefc+vp*0x1000 if p['name']=='callee-entry'else 0xaf00+vp*0x1000
                need(scalar(reg,4)==expected_sp,'CALL/return original stack')
                counters=struct.unpack_from('<IIIII',mem,data+0x200)
                if p['name']=='callee-entry':
                    need(counters==(0,0,0,0,0) and mem[expected_sp:expected_sp+4]==struct.pack('<I',0x307b),'entry before guest effects')
                else:
                    x=artifact(p['xsave'][vp]);fx=mem[data+0x400:data+0x600]
                    need(len(x)==960 and int.from_bytes(x[512:520],'little')&3==3,'valid x87/SSE XSAVE')
                    need(bytes.fromhex(reg[str(0x1018)])==fx[:16]==x[:16] and bytes.fromhex(reg[str(0x1019)])==fx[16:32]==x[16:32],'raw control fields')
                    for i in range(8):
                        need(bytes.fromhex(reg[str(0x1010+i)])[:10]==fx[32+16*i:42+16*i]==x[32+16*i:42+16*i],'80-bit FP slots')
                        need(bytes.fromhex(reg[str(0x1000+i)])==fx[160+16*i:176+16*i]==x[160+16*i:176+16*i],'XMM slots')
                    if p['name']=='return-ept':
                        need(counters[0]==0 and counters[1]==(1 if kind=='ret'else 0),'RET #DB occurs before EPT; IRET RF=1 suppresses it')
                    else:
                        expected=(1 if kind=='ret'else 0)+(1 if 'unsafe-clear'in case else 0)
                        need(counters[:2]==(1,expected),'consumer once and exact native #DB count')
                    if counters[1]:need(counters[2:]==(0xffff0ff1,0x307b,0x46),'actual debug frame/DR6')
                rows.append(dict(phase=p['name'],vp=vp,consumer=counters[0],debug_handler=counters[1],rflags=flags,dr6=scalar(reg,37)))
        writes=r['host_register_writes_after_start'];unsafe='unsafe-clear'in case
        need(len(writes)==(2 if unsafe else 0),'no RF correction outside explicit unsafe control')
        for vp,row in enumerate(writes):
            before=int.from_bytes(bytes.fromhex(row['before']),'little');after=int.from_bytes(bytes.fromhex(row['after']),'little')
            need(row['vp']==vp and row['register']==17 and before^after==0x10000 and after&0x10000==0 and 'unsafe-negative-control'in row['intent'],'explicit unsafe RF-only delta')
        cases[name]=(r,rows);sources.append(dict(path=str(path),sha256=digest(report_bytes),bytes=len(report_bytes),native_errors_retained=r['errors']))
    required={'ret-baseline','ret-before-ept-guard-refusal','ret-ept-raw','ret-ept-unsafe-clear','iret-baseline','iret-ept-preserve','iret-ept-unsafe-clear'}
    need(set(cases)==required,'all fixed diagnostic contrasts')
    def final(name):return cases[name][0]['phases'][-1]
    for base,observed in (('ret-baseline','ret-ept-raw'),('iret-baseline','iret-ept-preserve')):
        a,b=final(base),final(observed)
        need(read(a['memory']['path'])==read(b['memory']['path']) and a['registers']==b['registers'],'raw-preserve final full memory/register equality')
        need(all(read(x['path'])==read(y['path'])for x,y in zip(a['xsave'],b['xsave'])),'raw-preserve full XSAVE equality')
    a,b=final('ret-ept-raw'),final('ret-ept-unsafe-clear')
    need(a['registers']==b['registers'],'duplicate #DB can be invisible in final full registers')
    am,bm=read(a['memory']['path']),read(b['memory']['path'])
    need([i for i in range(65536)if am[i]!=bm[i]]==[0x8204,0x9204],'duplicate #DB exact memory counter difference')
    return dict(accepted=False,fullstate=False,fullABI=False,original_game_starts=0,contrast_checks_passed=True,
                uniform_RF_clear_refuted=True,stack_and_return_PC_prove_direct_RET=False,
                raw_preserve_matches_two_fixture_baselines=True,production_RF_restoration_authorized=False,
                sources=sources,observations={n:rows for n,(_,rows)in cases.items()},
                limits=['Baselines share the callee-entry EPT; only return EPT is contrasted.',
                        'Closed 32-bit self-owned code, explicit guest #DB handler and disabled external input; not Windows/WOW64 or original-game acceptance.',
                        'Original RF provenance at arbitrary Windows return still missing. Do not infer it from stack or final register equality.'])

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--capsule',required=True);p.add_argument('--sha256',required=True);p.add_argument('--output',required=True);a=p.parse_args()
    b=Bundle(a.capsule,a.sha256)
    try:r=verify(b.read,b.manifest['reports'])
    finally:b.close()
    with Path(a.output).open('x',encoding='utf8')as f:json.dump(r,f,indent=2)
    print(json.dumps({k:v for k,v in r.items()if k not in ('sources','observations')},indent=2))
