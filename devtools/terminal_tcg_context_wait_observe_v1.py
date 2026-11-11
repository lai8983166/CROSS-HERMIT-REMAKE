"""First nonzero-timeout WOW64 wait: context-filtered original instruction witnesses and CR2 chain. Not game acceptance."""
import argparse,hashlib,json,re,time,copy
from pathlib import Path
from devtools.terminal_tcg_roundtrip_probe import RSP,identity
from devtools.terminal_cr2_qmp import QMP
from devtools.terminal_cr2_ledger_verify import verify as ledger_verify
from devtools.terminal_tcg_compat_context import pack,source_digest

def trace(case,planfile):
    ready=json.loads((case/'ready.json').read_bytes());plan=json.loads(planfile.read_bytes())
    kernel=Path(plan['kernel_path']).read_bytes()
    if hashlib.sha256(kernel).hexdigest()!=plan['kernel_sha256']:raise ValueError('kernel identity')
    vm=json.loads((case/'vm-ready.json').read_bytes());q=QMP(vm['qmp']);g=RSP(vm['gdb'])
    q.s.settimeout(15);g.s.settimeout(65);active=set();start=time.monotonic();context=None
    r=dict(accepted=False,original_game=False,cr2_explained=False,errors=[],points=[],reads=[],foreign_hits=[],steps=[],ready=ready,plan_source=identity(planfile))
    def cmd(s):return g.command(s)
    def query(name,args=None):
        v=q.call(name,args)
        if 'return'not in v:raise ValueError(v)
        return v['return']
    def states():return [json.loads(query('x-query-tcg-state',{'cpu-index':i})['state'])for i in range(2)]
    def mem(a,n):
        out=b''
        for off in range(0,n,1024):
            chunk=cmd(f'm{a+off:x},{min(n-off,1024):x}')
            r['reads'].append(dict(address=a+off,size=min(n-off,1024),error=chunk if chunk.startswith('E')else None))
            if chunk.startswith('E'):raise ValueError(f'memory {a+off:#x}: {chunk}')
            out+=bytes.fromhex(chunk)
        if len(out)!=n:raise ValueError('short memory')
        return out
    def bp(op,pc):
        if cmd(f'{op}1,{pc:x},1')!='OK':raise ValueError('breakpoint')
        active.add(pc)if op=='Z'else active.discard(pc)
    def owner(s):
        fs=int(s['segments_es_cs_ss_ds_fs_gs_ldt_tr_gdt_idt'][4][1],16)
        return mem(fs+0x20,8)==ready['pid'].to_bytes(4,'little')+ready['tid'].to_bytes(4,'little')
    def filter_command(op):
        value=json.loads(query('x-query-tcg-state',{'cpu-index':op})['state'])
        r.setdefault('context_filter',[]).append(value)
        if value.get('poisoned'):raise ValueError('context filter poisoned')
        return value
    def until(pcs,user=False):
        for pc in pcs:
            if pc not in active:bp('Z',pc)
        if context is not None:filter_command(-7)
        for attempt in range(65):
            if time.monotonic()-start>210:raise ValueError('210s trace budget')
            reply=cmd('c');cmd('Hg1');s=states();pc=int(s[0]['eip'],16)
            if not reply.startswith('T05'):raise ValueError('unexpected stop '+reply)
            stopped=re.search(r'thread:([0-9a-f]+);',reply)
            if stopped and int(stopped[1],16)==1 and pc in pcs and(owner(s[0])if user else int(s[0]['gpr'][13],16)==context):
                for address in pcs:bp('z',address)
                return s
            r['foreign_hits'].append(dict(reply=reply,pc=pc))
            if context is not None:raise ValueError('filtered foreign stop')
            if attempt==64:raise ValueError('foreign budget')
            for address in pcs:bp('z',address)
            thread=re.search(r'thread:([0-9a-f]+);',reply)
            if not thread:raise ValueError('stop thread')
            cmd('Hc'+thread[1])
            if not cmd('s').startswith('T05'):raise ValueError('foreign single-step stop')
            cmd('Hc-1')
            for address in pcs:bp('Z',address)
        raise ValueError('stop budget')
    def take(label,s,extra=None):
        if not owner(s[0]):raise ValueError('point TEB owner mismatch')
        fs=int(s[0]['segments_es_cs_ss_ds_fs_gs_ldt_tr_gdt_idt'][4][1],16)
        item=dict(label=label,states=s,code_hex=mem(int(s[0]['eip'],16),32).hex(),extra=extra or {},owner_teb_client_id_hex=mem(fs+0x20,8).hex())
        if states()!=s:raise ValueError('unstable stop')
        if label in ('call','ret32','consumer'):
            cpu=s[0];esp=int(cpu['gpr'][4],16)
            item['boundary']=dict(compat=pack(cpu,expected_cpu=0,expected_vcpus=2,expected_source_sha256=source_digest(cpu)),data_hex=mem(ready['data'],16384).hex(),stack_hex=mem(esp,64).hex(),timeout_hex=mem(ready['timeout_pointer'],8).hex(),private_code=mem(ready['code'],len(bytes.fromhex(ready['code_hex']))).hex(),nt_wait=mem(ready['nt_wait'],32).hex())
            if item['boundary']['private_code']!=ready['code_hex'] or item['boundary']['nt_wait']!=ready['nt_wait_before']:raise ValueError('boundary original bytes')
            if not owner(cpu) or states()!=s:raise ValueError('boundary owner/stability')
        r['points'].append(item)
    def step(label,s):
        before=mem(int(s[0]['eip'],16),16).hex();cmd('Hc1');reply=cmd('s')
        thread=re.search(r'thread:([0-9a-f]+);',reply)
        if not reply.startswith('T05') or not thread or int(thread[1],16)!=1:raise ValueError('single step owner')
        cmd('Hc-1');after=states();r['steps'].append(dict(label=label,before=s,bytes_hex=before,after=after,reply=reply));return after
    try:
        query('stop');cmd('Hg1');cmd('Hc-1');pc=ready['postcall_pc']-2;bp('Z',pc)
        (case/'observer-armed.json').write_text(json.dumps(dict(call_pc=pc,ready_sha256=identity(case/'ready.json')['sha256'])))
        s=until([pc],True)
        if int.from_bytes(mem(ready['timeout_pointer'],8),'little',signed=True)!=-300000000:raise ValueError('first nonzero-timeout input')
        context=int(s[0]['gpr'][13],16);wow=int(s[0]['gpr'][15],16)-plan['wow_table_rva'];nt=ready['nt_wait']-plan['ntwait_rva']
        live=mem(wow+plan['wow_text_rva'],len(bytes.fromhex(plan['wow_text_hex'])))
        if live.hex()!=plan['wow_text_hex']:raise ValueError('live WOW64 code differs')
        slot=nt+plan['nt_slot_rva'];bop=int.from_bytes(mem(slot,4),'little');entry=mem(nt+plan['nt_entry_rva'],6)
        if entry!=b'\xff\x25'+slot.to_bytes(4,'little'):raise ValueError('live transition indirection')
        table=mem(wow+plan['wow_table_rva']+13*8,8)
        if int.from_bytes(table,'little')!=wow+0x1b46:raise ValueError('selector13 table')
        take('call',s,dict(wow_base=wow,nt_base=nt,context=context,live_wow_code=live.hex(),transition=entry.hex(),slot=slot,bop=bop,bop_bytes=mem(bop,16).hex(),table13=table.hex()))
        bp('Z',wow+0x1b46);filter_command(-4)
        r['ledger_arm']=json.loads(query('x-query-tcg-state',{'cpu-index':-2})['state'])
        s=until([wow+0x1b46]);take('selector13',s,dict(saved_return=mem(context+0x3c,4).hex(),context_bytes=mem(context-0x80,0x240).hex()))
        s=until([wow+0x1cf1,wow+0x1cf4]);take('system-entry',s)
        if int(s[0]['eip'],16)!=wow+0x1cf1:raise ValueError('INT2E branch needs separate witness')
        if mem(wow+0x1cf1,2)!=b'\x0f\x05':raise ValueError('SYSCALL opcode')
        s=step('syscall',s)
        if int(s[0]['gpr'][13],16)!=context or int(s[0]['segments_es_cs_ss_ds_fs_gs_ldt_tr_gdt_idt'][1][0],16)!=0x10:raise ValueError('kernel entry owner/mode')
        entrypc=int(s[0]['eip'],16);signature=mem(entrypc,64);candidates=[]
        for m in re.finditer(re.escape(signature),kernel):
            for sec in plan['kernel_sections']:
                if sec['raw']<=m.start()<sec['raw']+sec['size']:candidates.append(entrypc-(sec['rva']+m.start()-sec['raw']))
        if len(candidates)!=1:raise ValueError('unique live kernel entry mapping')
        kb=candidates[0];take('kernel-entry',s,dict(kernel_base=kb,signature=signature.hex()))
        s=until([kb+x for x in plan['kernel_clear_rvas']]);take('kernel-clear-before',s);clear=int(s[0]['eip'],16)
        if mem(clear,24)!=bytes.fromhex('660fefc0660fefc9660fefd2660fefdb660fefe4660fefed'):raise ValueError('original PXOR bytes')
        for i in range(6):
            if int(s[0]['eip'],16)!=clear+4*i:raise ValueError('PXOR before PC')
            expected=copy.deepcopy(s[0]);expected['eip']=f'{clear+4*(i+1):016x}';expected['xmm_low64_high64'][i]=['0000000000000000','0000000000000000']
            s=step('pxor-'+str(i),s)
            if s[0]!=expected:raise ValueError('PXOR exact full-state effect')
        take('kernel-clear-after',s);s=until([wow+0x1cf3]);take('native-return',s)
        s=until([wow+0x1b7f,wow+0x1b91]);take('shadow-predecessor',s)
        if int(s[0]['eip'],16)!=wow+0x1b7f or mem(wow+0x1b7f,3)!=bytes.fromhex('418ed0'):raise ValueError('MOV SS predecessor')
        s=step('mov-ss',s);take('return-branch',s,dict(saved_return=mem(context+0x3c,4).hex()))
        if int(s[0]['eip'],16)!=wow+0x1b82:raise ValueError('slow IRET branch needs separate witness')
        target=int.from_bytes(mem(context+0x3c,4),'little')
        if target!=ready['return_pc']:raise ValueError('saved return owner')
        if mem(wow+0x1b82,4)!=bytes.fromhex('458b4d3c'):raise ValueError('R9 opcode')
        expected=copy.deepcopy(s[0]);expected['eip']=f'{wow+0x1b86:016x}';expected['gpr'][9]=f'{target:016x}'
        s=step('load-r9d',s)
        if int(expected['hflags'],16)&8!=8:raise ValueError('MOV SS interrupt shadow absent')
        expected['hflags']=f"{int(expected['hflags'],16)&~8:016x}"
        if s[0]!=expected:raise ValueError('R9 exact full-state effect')
        take('r9-after',s);s=until([ready['return_pc']],True);r['ledger_end']=json.loads(query('x-query-tcg-state',{'cpu-index':-3})['state']);take('ret32',s);esp=int(s[0]['gpr'][4],16)
        if mem(ready['return_pc'],3)!=bytes.fromhex('c20c00'):raise ValueError('RET opcode')
        expected=copy.deepcopy(s[0]);expected['eip']=f"{ready['postcall_pc']:016x}";expected['gpr'][4]=f'{esp+16:016x}';s=step('ret12',s)
        if s[0]!=expected:raise ValueError('RET exact full-state effect')
        take('consumer',s)
        r['ledger_verification']=ledger_verify(r['ledger_arm'],r['ledger_end'],r['points'][0]['states'],next(p['states'] for p in r['points'] if p['label']=='ret32'))
        if not r['ledger_verification']['cr2_chain_verified']:raise ValueError('continuous CR2 ledger')
        r['instruction_witness_complete']=True
    except Exception as exc:r['errors'].append(type(exc).__name__+': '+str(exc))
    finally:
        try:query('stop')
        except Exception as exc:r['errors'].append('cleanup stop '+type(exc).__name__)
        try:filter_command(-5)
        except Exception as exc:r['errors'].append('filter cleanup '+type(exc).__name__+': '+str(exc))
        for pc in list(active):
            try:bp('z',pc)
            except Exception as exc:r['errors'].append('bp cleanup '+type(exc).__name__)
        try:query('cont')
        except Exception as exc:r['errors'].append('resume '+type(exc).__name__)
        if r['errors']:r['instruction_witness_complete']=False
        r.update(seconds=time.monotonic()-start,qmp=q.receipts);q.f.close();q.s.close();g.s.close()
        (case/'observation.json').write_text(json.dumps(r,indent=2))
    print(json.dumps(dict(seconds=r['seconds'],errors=r['errors'],points=len(r['points']),steps=len(r['steps']))))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('case',type=Path);p.add_argument('plan',type=Path);a=p.parse_args();trace(a.case,a.plan)
