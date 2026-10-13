"""Original current-unit attack snapshots plus declared scalar damage probes."""
import argparse
import hashlib
import json
import pickle
import struct
from copy import deepcopy
from unicorn.x86_const import UC_X86_REG_ESP, UC_X86_REG_EIP, UC_X86_REG_ECX
from tools.school_formation_placement_emulation import SchoolFormationPlacementEmulator, UNITCTRL, WORK_OFFSET, WORK_BYTES
from tools.school_deployment_tail_emulation import CHECKPOINTS, parent_evidence
from tools.tactics_exit_emulation import ExitEmulator, ROOT, SOURCE_SHA256, STACK, RETURN, report_text
from tools.school_attack_inputs import source_rules, project, from_record, snapshot_bytes, scalar_damage, snapshot

SCRATCH = 0x23000000
NATIVE = ((0x488AF0,0x488BC0),(0x4DEAA0,0x4DEAF0),(0x4DE930,0x4DEA30),(0x4DEA30,0x4DEAA0),
    (0x4DFA70,0x4DFB20),(0x4DE8F0,0x4DE930),(0x46C9F0,0x46CA60),(0x46B3E0,0x46B470),
    (0x43B9E0,0x43BB90),(0x48A260,0x48A380),(0x48A380,0x48A730),(0x48A730,0x48ABA0),
    (0x4824D0,0x4826F0),(0x4826F0,0x482810))
CODE = frozenset(va for a,b in NATIVE for va in range(a,b))


class AttackProbe(SchoolFormationPlacementEmulator):
    def __init__(self):
        self.attack_loading = False
        super().__init__()

    def _write_hook(self, uc, access, address, size, value, context):
        if not self.attack_loading: return super()._write_hook(uc,access,address,size,value,context)
        allowed = [(STACK,STACK+65536),(SCRATCH,SCRATCH+44)] if self.attack_phase == 'snapshot' else [(STACK,STACK+65536),(SCRATCH+40,SCRATCH+44)]
        if not any(a<=address and address+size<=b for a,b in allowed): raise RuntimeError('attack forbidden write '+hex(address))

    def _hook(self, uc, address, size, context):
        if not self.attack_loading: return super()._hook(uc,address,size,context)
        sp=uc.reg_read(UC_X86_REG_ESP)
        if address == 0x56CEC0:
            values = [self.read(sp+offset) for offset in (4,8,12)]
            if self.attack_phase != 'snapshot' or values != [SCRATCH,0,44] or self.read(sp) != 0x4DE955:
                raise RuntimeError('attack exact snapshot clear')
            self.uc.mem_write(SCRATCH,bytes(44)); self._stub_return(SCRATCH,0); return
        if address == 0x467E00:
            if self.attack_phase != 'damage' or not self.rolls: raise RuntimeError('attack declared RNG exhausted')
            value=self.rolls.pop(0)
            self.roll_calls.append({'return_va':hex(self.read(sp)),'value':value})
            self._stub_return(value,0); return
        if address == 0x56CE80: return ExitEmulator._hook(self,uc,address,size,context)
        if address in CODE: self.visited.add(address); return
        raise RuntimeError('attack undeclared instruction '+hex(address))

    def original_snapshot(self, identity, attack_id):
        work = next(UNITCTRL+WORK_OFFSET+i*WORK_BYTES for i in range(3)
            if self.read(self.read(UNITCTRL+WORK_OFFSET+i*WORK_BYTES+600)+2,'H') == identity)
        record=self.read(work+600); before_record=bytes(self.uc.mem_read(record,176)); before_work=bytes(self.uc.mem_read(work,WORK_BYTES))
        cell=list(before_work[1255:1257]); header=self.read(UNITCTRL+0x2A304)
        terrain=self.read(header+16+6*(cell[1]*64+cell[0]),'B')
        self.attack_phase='snapshot'; self.attack_loading=True; prior=self._function_ranges; self._function_ranges=prior+NATIVE
        retained=self.capture_scene_memory([(STACK,STACK+65536),(SCRATCH,SCRATCH+44)])
        try:
            self.call(0x488AF0,(attack_id,work,SCRATCH),receiver=UNITCTRL)
            output=bytes(self.uc.mem_read(SCRATCH,44))
            if bytes(self.uc.mem_read(record,176))!=before_record or bytes(self.uc.mem_read(work,WORK_BYTES))!=before_work:
                raise RuntimeError('attack snapshot changed actual unit')
            return {'character_id':identity,'attack_id':attack_id,'cell':cell,'terrain':terrain,
                'source_record_hex':before_record.hex(),'snapshot_hex':output.hex(),
                'condition_slots_zero':not any(before_work[20:68]),'original_snapshot_executed':True,
                'world_or_HP_application_executed':False,**self.verify_scene_memory(retained)}
        finally: self.attack_loading=False; self._function_ranges=prior

    def original_damage(self, attack, defense, rolls, magic=False):
        # Explicit probe packets, not a command accepted by the original world.
        self.uc.mem_write(SCRATCH,attack[:40]+b'\xff'*4)
        self.uc.mem_write(SCRATCH+128,defense)
        self.rolls=list(rolls); self.roll_calls=[]; self.attack_phase='damage'
        before=bytes(self.uc.mem_read(SCRATCH,40)); target=bytes(self.uc.mem_read(SCRATCH+128,44))
        self.attack_loading=True; prior=self._function_ranges; self._function_ranges=prior+NATIVE
        try:
            self.call(0x4826F0 if magic else 0x4824D0,(SCRATCH,SCRATCH+128),receiver=UNITCTRL)
            result=self.read(SCRATCH+40,'i')
            if bytes(self.uc.mem_read(SCRATCH,40))!=before or bytes(self.uc.mem_read(SCRATCH+128,44))!=target:
                raise RuntimeError('scalar damage changed input packet')
            return {'magic':magic,'attack_hex':attack.hex(),'defense_hex':defense.hex(),'declared_rolls':rolls,
                'roll_calls':deepcopy(self.roll_calls),'damage':result,'input_packets_unchanged':True,'HP_applied':False}
        finally: self.attack_loading=False; self._function_ranges=prior


def report():
    rules=source_rules(); parent=parent_evidence(); cases=[]; emulator=None
    for index in range(3):
        name,sha=CHECKPOINTS[index]; raw=(ROOT/f'.venv-audit/formation-actual-checkpoint-{index}.pkl').read_bytes()
        if hashlib.sha256(raw).hexdigest()!=sha: raise ValueError('attack trusted checkpoint identity')
        payload=pickle.loads(raw)
        if payload['source_sha']!=SOURCE_SHA256 or payload['evidence_kind']!='private_actual_cpu_after_full35_before_placement': raise ValueError('attack checkpoint provenance')
        e=AttackProbe();e.__dict__.update({k:v for k,v in payload['state'].items() if not k.startswith('_audit_') and k!='uc'})
        for at,data in payload['memory']: e.uc.mem_write(at,data)
        e.uc.context_restore(payload['cpu'])
        if e.run_placement()!=parent['cases'][index]['formation_placement']: raise ValueError('attack parent full placement')
        e.uc.mem_map(SCRATCH,4096)
        roles=[3,4,9] if index==0 else [3,4]; snapshots=[]
        for identity in roles:
            job={3:10,4:6,9:7}[identity]; attack_id=rules['jobs'][str(job)]['archetype']
            snapshots.append(e.original_snapshot(identity,attack_id))
        cases.append({'name':name,'checkpoint_sha256':sha,'actual_current_snapshots':snapshots})
        if index==0: emulator=e
        print('Original current snapshots '+name,flush=True)
    scalar=[]
    # Zero/critical/miss boundaries, including original reuse of the same hit roll.
    for accuracy in [0,90,200]:
        for roll in [0,4,5,94,95,99]:
            fields={'power':12,'power_range':3,'accuracy':accuracy,'evasion':12,'armor':3,'body':5,'magic_body':4,'magic_resist':20,'mental':10}
            packet=snapshot_bytes(fields,12,rules=rules)
            output=emulator.original_damage(packet,packet,[roll,11])
            scalar.append(output)
    for power,armor in [(0,0),(1,5),(12,1)]:
        fields={'power':power,'power_range':3 if power==12 else 0,'accuracy':200,'evasion':0,'armor':armor,'body':5,'magic_body':4,'magic_resist':20,'mental':10}
        packet=snapshot_bytes(fields,12,rules=rules)
        for magic in [False,True]: scalar.append(emulator.original_damage(packet,packet,[0,11],magic))
    return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'cases':cases,'declared_scalar_probes':scalar,
        'source_rules':rules,'scope':'Original actual-current snapshot bodies and isolated declared scalar formulas. No original command/AI/world/HP mutation or settlement.'}


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--out',required=True)
    args=parser.parse_args();p=ROOT/args.out
    if p.exists():parser.error('use a new immutable evidence path')
    p.write_text(report_text(report()),encoding='utf-8',newline='\n')
