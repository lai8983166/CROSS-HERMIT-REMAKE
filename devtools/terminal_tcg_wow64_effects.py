"""Narrow CPU0 instruction semantics; never a whole-machine or game acceptance."""
import argparse,copy,hashlib,json
from pathlib import Path


def verify(trace,plan):
    r=dict(accepted=False,cr2_explained=False,consumer_connected_in_this_trace=False,
           cpu_scope='CPU0 only; CPU1 ran between stopped observations',checks=[],errors=[])
    def check(name,value):r['checks'].append(dict(name=name,passed=bool(value)))
    try:
        points={p['label']:p for p in trace['points']};steps={s['label']:s for s in trace['steps']}
        call=points['call'];wow=call['extra']['wow_base'];context=call['extra']['context']
        check('live_wow_bytes',call['extra']['live_wow_code']==plan['wow_text_hex'])
        check('selector13',int.from_bytes(bytes.fromhex(call['extra']['table13']),'little')==wow+0x1b46)
        kb=points['kernel-entry']['extra']['kernel_base']
        before=points['kernel-clear-before']['states'][0];pc=int(before['eip'],16)
        check('kernel_clear_candidate',pc-kb in plan['kernel_clear_rvas'])
        for i in range(6):
            step=steps['pxor-'+str(i)];a,b=step['before'][0],step['after'][0]
            opcode=bytes([0x66,0x0f,0xef,0xc0+9*i]).hex()
            check(f'pxor{i}.owner',step['reply']=='T05thread:01;' and a['cpu']==b['cpu']==0 and int(a['gpr'][13],16)==context)
            check(f'pxor{i}.bytes',step['bytes_hex'].startswith(opcode))
            check(f'pxor{i}.chain',a==before and int(a['eip'],16)==pc+4*i)
            expected=copy.deepcopy(a);expected['eip']=f'{pc+4*(i+1):016x}';expected['xmm_low64_high64'][i]=['0000000000000000','0000000000000000']
            check(f'pxor{i}.exact_effect',b==expected);before=b
        check('kernel_clear_endpoint',before==points['kernel-clear-after']['states'][0])
        native=points['native-return']['states'][0]
        check('native_return_pc',int(native['eip'],16)==wow+0x1cf3)
        check('native_return_xmm',native['xmm_low64_high64'][:6]==[['0000000000000000','0000000000000000']]*6)
        branch=points['return-branch'];step=steps['load-r9d'];a,b=step['before'][0],step['after'][0]
        target=int.from_bytes(bytes.fromhex(branch['extra']['saved_return']),'little')
        check('r9.owner_bytes',step['reply']=='T05thread:01;' and step['bytes_hex'].startswith('458b4d3c') and
              a==branch['states'][0] and int(a['eip'],16)==wow+0x1b82 and int(a['gpr'][13],16)==context and target==trace['ready']['return_pc'])
        check('shadow_observed',int(a['hflags'],16)&8==8)
        expected=copy.deepcopy(a);expected['eip']=f'{wow+0x1b86:016x}';expected['gpr'][9]=f'{target:016x}'
        expected['hflags']=f"{int(a['hflags'],16)&~8:016x}"
        check('r9_exact_effect_with_shadow_end',b==expected)
        r['shadow_rule']='Only this known MOV instruction with observed preexisting HF_INHIBIT_IRQ=1: exact clearing of mask0x8 at TB end. No generic masking and no assertion about the actual shadow-setting predecessor.'
    except (KeyError,ValueError,IndexError,TypeError)as exc:r['errors'].append(type(exc).__name__+': '+str(exc))
    r['local_effects_verified']=not r['errors'] and bool(r['checks']) and all(x['passed']for x in r['checks'])
    return r


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('trace',type=Path);p.add_argument('plan',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    report=verify(json.loads(a.trace.read_bytes()),json.loads(a.plan.read_bytes()))
    report['inputs']={str(x):hashlib.sha256(x.read_bytes()).hexdigest()for x in (a.trace,a.plan)}
    with a.out.open('x',encoding='utf8')as f:json.dump(report,f,indent=2)
    print(json.dumps(dict(local_effects_verified=report['local_effects_verified'],errors=report['errors'],failed=[x['name']for x in report['checks']if not x['passed']])))
