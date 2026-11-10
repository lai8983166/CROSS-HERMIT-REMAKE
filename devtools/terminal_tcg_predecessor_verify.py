"""Finite microguest predecessor verification; Trace entry is not retirement."""
import hashlib,json,re,struct
from pathlib import Path
from capstone import Cs,CS_ARCH_X86,CS_MODE_32

def need(v,m):
    if not v:raise ValueError(m)

def verify(elf,trace,output):
    need(elf[:7]==bytes.fromhex('7f454c46010101'),'ELF32 identity')
    need(len(output)==22 and output[:3]==b'SHD'and output[-3:]==b'R1E','exact observed guest output')
    frame=struct.unpack('<IIII',output[3:19]);need(frame==(0x100305,8,6,0xffff0ff1),'original #DB stack and DR6')
    lines=trace.splitlines();events=[];decoded=[];dis=Cs(CS_ARCH_X86,CS_MODE_32)
    for n,line in enumerate(lines):
        m=re.match(r'Trace (\d+): .*?\[[^/]+/([0-9a-f]+)/',line)
        if not m:continue
        vp,pc=int(m[1]),int(m[2],16)
        if not 0x100000<=pc<0x105000:continue
        need(vp==0,'only BSP measured; no fabricated AP chain')
        off=4096+pc-0x100000;ins=list(dis.disasm(elf[off:off+15],pc,count=1));need(len(ins)==1,'original instruction bytes')
        decoded.append(dict(line=n,pc=pc,hex=ins[0].bytes.hex(),instruction=ins[0].mnemonic+' '+ins[0].op_str))
    pcs=[x['pc']for x in decoded]
    need(pcs.count(0x100300)==pcs.count(0x100384)==pcs.count(0x100400)==pcs.count(0x100305)==1,'single CALL/RET/handler/consumer path')
    need(elf[4096+0x300:4096+0x305]==bytes.fromhex('e87b000000') and elf[4096+0x384]==0xc3,'natural CALL/near RET')
    start=decoded[0]['line'];window='\n'.join(lines[start:])
    need('Stopped execution'not in window,'no logged unstarted TB in target interval')
    for n,line in enumerate(lines[start:],start):
        if re.search(r'\bv=\w+.*\bi=',line):events.append((n,line))
    need(len(events)==1 and re.search(r'v=01 .*i=0 .*IP=0008:0000000000100305',events[0][1]),'one actual #DB at return')
    event_line=events[0][0];ret=next(x for x in decoded if x['pc']==0x100384);handler=next(x for x in decoded if x['pc']==0x100400)
    consumer_index=pcs.index(0x100305);prior=decoded[consumer_index-1]
    need(prior['hex']=='cf' and prior['instruction'].startswith('iretd'),'actual immediately preceding handler IRETD')
    need(ret['line']<event_line<handler['line']<prior['line'],'RET then event then handler then IRET')
    event_block='\n'.join(lines[event_line:handler['line']])
    need('DR0=0000000000100305'in event_block and 'DR6=00000000ffff0ff1 DR7=0000000000000401'in event_block,'real enabled breakpoint and DR6')
    need('EIP=00100305 EFL=00000006'in event_block,'event flags agree with raw frame')
    need(any(x['hex']=='814c242800000100'for x in decoded),'guest handler sets RF in its own frame')
    return dict(accepted=False,fullstate=False,fullABI=False,finite_TCG_predecessor_event_observed=True,
        original_game_starts=0,windows_boots=0,measured_vps=[0],configured_vps=2,
        event_frame=dict(eip=frame[0],cs=frame[1],eflags=frame[2],dr6=frame[3]),
        direct_consumer_predecessor=prior,trace=decoded,
        limits=['Trace records TB entry, not instruction retirement by itself; conclusion combines original code, event record, guest frame and subsequent execution.',
                'Self-owned TCG code only. R appears once; 1 is the handler count, not an independent consumer counter.',
                'No Windows/WOW64, complete57, hardware-native equivalence, two-VP handshake or original-game state.',
                'Exact publisher binary to source-build correspondence remains unproven; old GDB/HMP floating-point limitations unchanged.'])

if __name__=='__main__':
    root=Path('F:/project/chaomofa');d=root/'.venv-audit/native-worker/tcg-predecessor-v3-20261110'
    r=json.loads((d/'report.json').read_text());need(r['execution_complete']and not r['errors'],'bounded source completed')
    for row in r['files']:
        p=Path(row['path']);b=p.read_bytes();need(len(b)==row['bytes']and hashlib.sha256(b).hexdigest()==row['sha256'],'raw source identity')
    result=verify((d/'guest.elf').read_bytes(),(d/'trace.log').read_text(),(d/'guest.txt').read_bytes())
    result['report_sha256']=hashlib.sha256((d/'report.json').read_bytes()).hexdigest()
    p=root/'analysis/terminal-wait-tcg-predecessor-proof-v1-20261110.json'
    with p.open('x',encoding='utf8')as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items()if k!='trace'},indent=2))
