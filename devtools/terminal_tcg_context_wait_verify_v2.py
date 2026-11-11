"""Same-run instruction and CR2 witnesses; narrowly scoped, never game acceptance."""
import copy
from devtools.terminal_tcg_wow64_effects_v3 import verify as effects
from devtools.terminal_cr2_ledger_verify import verify as ledger


def verify(trace, plan):
    result = dict(accepted=False, original_game=False, full_windows_admission=False,
                  same_wait_writes_verified=False, exported_endpoint_verified=False,
                  checks=[], errors=[])
    def check(name, value):
        result['checks'].append(dict(name=name, passed=bool(value)))
    try:
        narrow = effects(trace, plan)
        result['instruction_effects'] = narrow
        check('strict_raw64_and_seven_effects', narrow['local_effects_verified'])
        points = {p['label']:p for p in trace['points']}
        steps = {p['label']:p for p in trace['steps']}
        check('completed_without_observer_error', trace['instruction_witness_complete'] is True and trace['errors'] == [])
        filters=trace['context_filter']
        check('filter_lifetime', len(filters)>=2 and filters[0]['active'] is True and filters[-1]['active'] is False and all(f['poisoned'] is False and f['schema']=='tcg-context-v1' for f in filters) and filters[-1]['accepted']>=5)
        check('no_warm_zero_wait', not any(p.startswith('warm-') for p in points))
        call,ret,post = [points[k] for k in ('call','ret32','consumer')]
        ready = trace['ready']; wow = call['extra']['wow_base']; context = call['extra']['context']
        check('nonzero_timeout', all(int.from_bytes(bytes.fromhex(p['boundary']['timeout_hex']),'little',signed=True)==-300000000 for p in (call,ret,post)))
        check('current_teb_at_every_point', all(p['owner_teb_client_id_hex']==ready['pid'].to_bytes(4,'little').hex()+ready['tid'].to_bytes(4,'little').hex() and p['states'][0]['segments_es_cs_ss_ds_fs_gs_ldt_tr_gdt_idt'][4][1]==call['states'][0]['segments_es_cs_ss_ds_fs_gs_ldt_tr_gdt_idt'][4][1] for p in points.values()))
        check('filter_current_owner', all(f['cr3']==call['states'][0]['cr0_cr2_cr3_cr4'][2] and f['r13']==call['states'][0]['gpr'][13] and type(f['cpu']) is int and f['cpu']==0 for f in filters))
        check('current_owner_all_stops', all(p['states'][0]['cr0_cr2_cr3_cr4'][2] == call['states'][0]['cr0_cr2_cr3_cr4'][2] and int(p['states'][0]['gpr'][13],16)==context for p in points.values()))
        a,b=steps['mov-ss']['before'][0],steps['mov-ss']['after'][0]
        check('mov_ss_actual_predecessor', a==points['shadow-predecessor']['states'][0] and b==points['return-branch']['states'][0] and steps['mov-ss']['bytes_hex'].startswith('418ed0') and int(a['eip'],16)==wow+0x1b7f and steps['mov-ss']['reply']=='T05thread:01;')
        expected=copy.deepcopy(a);expected['eip']=f'{wow+0x1b82:016x}';expected['hflags']=f"{int(a['hflags'],16)|8:016x}"
        check('mov_ss_exact_effect', b==expected and int(a['hflags'],16)&8==0 and int(a['gpr'][8],16)&65535==int(a['segments_es_cs_ss_ds_fs_gs_ldt_tr_gdt_idt'][2][0],16))
        check('r9_after_connected', steps['load-r9d']['after'][0]==points['r9-after']['states'][0])
        r9=points['r9-after']['states'][0]
        check('writes_reach_ret', ret['states'][0]['gpr'][9]==r9['gpr'][9] and ret['states'][0]['xmm_low64_high64'][:6]==points['kernel-clear-after']['states'][0]['xmm_low64_high64'][:6])
        result['ledger']=ledger(trace['ledger_arm'],trace['ledger_end'],call['states'],ret['states'])
        check('continuous_cr2', result['ledger']['cr2_chain_verified'])
        aa,bb=call['states'][0],ret['states'][0]
        expected=copy.deepcopy(aa)
        expected['eip']=f"{ready['return_pc']:016x}"
        expected['gpr'][0]='0000000000000000'
        expected['gpr'][1]=steps['syscall']['after'][0]['gpr'][1]
        expected['gpr'][2]=steps['syscall']['before'][0]['gpr'][2]
        expected['gpr'][4]=f"{int(aa['gpr'][4],16)-4:016x}"
        expected['gpr'][9]=r9['gpr'][9]
        expected['xmm_low64_high64'][:6]=points['kernel-clear-after']['states'][0]['xmm_low64_high64'][:6]
        expected['cr0_cr2_cr3_cr4'][1]=trace['ledger_end']['end'][0]['cr2']
        check('syscall_link', steps['syscall']['before'][0]==points['system-entry']['states'][0] and steps['syscall']['after'][0]==points['kernel-entry']['states'][0] and steps['syscall']['bytes_hex'].startswith('0f05') and int(steps['syscall']['before'][0]['eip'],16)==wow+0x1cf1 and int(expected['gpr'][1],16)==wow+0x1cf3 and int(expected['gpr'][2],16)==0)
        check('entire_exported_call_ret_endpoint', expected==bb)
        stack=lambda p:[int.from_bytes(bytes.fromhex(p['boundary']['stack_hex'])[i:i+4],'little') for i in (0,4,8,12)]
        args=[ready['event_handle'],0,ready['timeout_pointer']]
        check('current_call_stack', stack(call)[:3]==args and stack(ret)==[ready['postcall_pc'],*args])
        expected=copy.deepcopy(bb);expected['eip']=f"{ready['postcall_pc']:016x}";expected['gpr'][4]=f"{int(bb['gpr'][4],16)+16:016x}"
        check('ret12_exact_and_connected', steps['ret12']['before'][0]==bb and steps['ret12']['after'][0]==post['states'][0]==expected and steps['ret12']['bytes_hex'].startswith('c20c00'))
        check('original_boundary_code', all(p['boundary']['private_code']==ready['code_hex'] and p['boundary']['nt_wait']==ready['nt_wait_before'] for p in (call,ret,post)))
        result['same_wait_writes_verified']=not result['errors'] and all(c['passed'] for c in result['checks'])
        result['exported_endpoint_verified']=result['same_wait_writes_verified']
        result['scope']='One owned nonzero-timeout wait; CPU0 exported endpoint, seven actual write effects and CPU0/1 CR2 chain. Not all intermediate instructions, RAM replay, Windows general admission or game acceptance.'
    except (KeyError,TypeError,ValueError,IndexError) as exc:
        result['errors'].append(type(exc).__name__+': '+str(exc))
    return result
