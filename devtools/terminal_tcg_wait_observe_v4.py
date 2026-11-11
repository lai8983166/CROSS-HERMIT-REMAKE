"""Observe real owned WOW64 NtWait CALL -> RET12 -> first consumer, read-only."""
import argparse,hashlib,json,re,time
from pathlib import Path
from devtools.terminal_tcg_roundtrip_probe import QMP,RSP,identity
from devtools.terminal_tcg_compat_context import pack,source_digest

def observe(case,readyfile):
    case=case.resolve();ready=json.loads(readyfile.read_bytes());vm=json.loads((case/'vm-ready.json').read_bytes())
    q=QMP(vm['qmp']);q.s.settimeout(40);g=RSP(vm['gdb']);g.s.settimeout(100);active=set();start=time.monotonic()
    r=dict(memory_reads=[],accepted=False,original_game=False,ready_source=identity(readyfile),ready=ready,stops=[],false_hits=[],errors=[],host_guest_state_writes=0)
    def call(name,args=None):
        v=q.call(name,args)
        if 'return'not in v:raise ValueError(v)
        return v['return']
    def cmd(text):return g.command(text)
    def bp(op,pc):
        if cmd(f'{op}1,{pc:x},1')!='OK':raise ValueError('observer breakpoint rejected')
        if op=='Z':active.add(pc)
        else:active.discard(pc)
    def memory(address,n):
        data=b''
        for i in range(0,n,1024):
            value=cmd(f'm{address+i:x},{min(n-i,1024):x}')
            r['memory_reads'].append(dict(address=address+i,bytes=min(n-i,1024),reply_error=value if value.startswith('E') else None))
            if value.startswith('E'):raise ValueError(f'unmapped current memory at {address+i:#x}, size={min(n-i,1024)}: {value}')
            data+=bytes.fromhex(value)
        if len(data)!=n:raise ValueError('short memory')
        return data
    def states():return [json.loads(call('x-query-tcg-state',{'cpu-index':i})['state'])for i in range(2)]
    def owner(s,pc):
        if int(s['eip'],16)!=pc:return False
        fs=int(s['segments_es_cs_ss_ds_fs_gs_ldt_tr_gdt_idt'][4][1],16)
        try:pid,tid=[int.from_bytes(memory(fs+0x20+i*4,4),'little')for i in range(2)]
        except ValueError:return False
        return(pid,tid)==(ready['pid'],ready['tid'])
    def stop_at(pc):
        for attempt in range(65):
            reply=cmd('c')
            if not reply.startswith('T05'):raise ValueError('unexpected stop '+reply)
            if cmd('Hg1')!='OK':raise ValueError('CPU0 select')
            s=states()
            if owner(s[0],pc):return s
            r['false_hits'].append(dict(reply=reply,cpu0_pc=s[0]['eip'],cpu0_cr3=s[0]['cr0_cr2_cr3_cr4'][2]))
            if attempt==64:raise ValueError('foreign hit budget')
            thread=re.search(r'thread:([0-9a-f]+);',reply)
            if not thread:raise ValueError('stop thread missing')
            bp('z',pc);cmd('Hc'+thread[1]);step=cmd('s');cmd('Hc-1');bp('Z',pc)
            if not step.startswith('T05'):raise ValueError('foreign step failed')
        raise ValueError('hit budget')
    def capture(label,s,checkpoint=False):
        cpu=s[0];data=memory(ready['data'],16384);esp=int(cpu['gpr'][4],16)
        code=memory(ready['code'],len(bytes.fromhex(ready['code_hex'])))
        if code.hex()!=ready['code_hex']:raise ValueError('private code identity')
        envelope=pack(cpu,expected_cpu=0,expected_vcpus=2,expected_source_sha256=source_digest(cpu))
        item=dict(label=label,states=s,compat=envelope,stack=memory(esp,64).hex(),data_hex=data.hex(),
            nt_wait=memory(ready['nt_wait'],32).hex(),timeout_hex=memory(ready['timeout_pointer'],8).hex(),
            owner_teb_client_id_hex=memory(int(cpu['segments_es_cs_ss_ds_fs_gs_ldt_tr_gdt_idt'][4][1],16)+0x20,8).hex(),code_hex=code.hex())
        if item['nt_wait']!=ready['nt_wait_before']:raise ValueError('original NtWait bytes changed')
        if checkpoint:item['ram_events']=json.loads(call('x-query-tcg-checkpoint')['state'])
        if states()!=s or memory(ready['data'],16384)!=data:raise ValueError('stopped observation changed')
        item['repeat_equal']=True;r['stops'].append(item);return item
    try:
        call('stop');cmd('Hg1');cmd('Hc-1')
        pc=ready['postcall_pc']-2;bp('Z',pc)
        (case/'observer-armed.json').write_text(json.dumps(dict(call_pc=pc,ready_sha256=identity(readyfile)['sha256'])))
        cr3=None
        for i in range(4):
            s=stop_at(pc)
            if cr3 is None:cr3=s[0]['cr0_cr2_cr3_cr4'][2]
            if s[0]['cr0_cr2_cr3_cr4'][2]!=cr3:raise ValueError('owner CR3 changed')
            before=capture(f'call-{i}',s);stack=bytes.fromhex(before['stack'])
            args=[int.from_bytes(stack[j:j+4],'little')for j in (0,4,8)]
            if args!=[ready['event_handle'],0,ready['timeout_pointer']]:raise ValueError('CALL arguments')
            bp('z',pc);bp('Z',ready['return_pc']);s=stop_at(ready['return_pc'])
            ret=capture(f'ret-{i}',s,checkpoint=i==0);stack=bytes.fromhex(ret['stack'])
            if [int.from_bytes(stack[j:j+4],'little')for j in (0,4,8,12)]!=[ready['postcall_pc'],*args]:raise ValueError('RET arguments/return owner')
            if int(s[0]['gpr'][0],16)!=(258 if i==3 else 0):raise ValueError('native return status')
            bp('z',ready['return_pc']);cmd('Hc1')
            if not cmd('s').startswith('T05'):raise ValueError('RET single-step')
            cmd('Hc-1');after=states()
            if not owner(after[0],ready['postcall_pc'])or int(after[0]['gpr'][4],16)!=int(s[0]['gpr'][4],16)+16:raise ValueError('natural RET target/ESP')
            capture(f'post-{i}',after);bp('Z',pc)
        bp('z',pc);call('cont');r['four_wait_returns_observed']=True
    except Exception as exc:r['errors'].append(type(exc).__name__+': '+str(exc))
    finally:
        for pc in list(active):
            try:bp('z',pc)
            except Exception as exc:r['errors'].append('remove breakpoint '+type(exc).__name__)
        try:call('cont')
        except Exception as exc:r['errors'].append('resume '+type(exc).__name__)
        r.update(seconds=time.monotonic()-start,qmp=q.receipts)
        q.f.close();q.s.close();g.s.close()
        (case/'observation.json').write_text(json.dumps(r,indent=2))
    print(json.dumps(dict(seconds=r['seconds'],errors=r['errors'],stops=len(r['stops']),false_hits=len(r['false_hits']))))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('case',type=Path);p.add_argument('ready',type=Path);a=p.parse_args();observe(a.case,a.ready)
