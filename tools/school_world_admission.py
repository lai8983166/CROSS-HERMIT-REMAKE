"""Original world entry on pinned real-school initialization checkpoints.

The captured gate reaches the first unexecuted mode-update call. A separately
declared zero-gate probe executes to its real return; neither is a world
tick, post-opening continuation or fabricated original opening completion.
"""
import argparse
import hashlib
import json
import pickle
from copy import deepcopy
from capstone import Cs, CS_ARCH_X86, CS_MODE_32
from unicorn.x86_const import UC_X86_REG_EIP, UC_X86_REG_ESP, UC_X86_REG_ECX
from tools.school_scene_opening_emulation import (
    SchoolSceneOpeningEmulator, restored_opening_case, read_deployment,
    parent_evidence, UNITCTRL, TACT, STACK, RETURN, ExitEmulator, ROOT,
)
from tools.school_deployment_tail_emulation import CHECKPOINTS
from tools.school_entry_control_emulation import read_opening
from tools.tactics_exit_emulation import SOURCE, SOURCE_SHA256, BASE, report_text

START, END = 0x46B470, 0x46B663
GATE, GLOBAL = UNITCTRL+0x108B32, 0x7A49E0


def source_contract():
    raw = SOURCE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        raise ValueError('world source identity')
    md = Cs(CS_ARCH_X86, CS_MODE_32)
    wanted = {0x46B48D: ('mov', 'dword ptr [0x7a49e0], 0'),
        0x46B49A: ('movsx', 'ecx, word ptr [eax + 0x108b32]'),
        0x46B4A3: ('jne', '0x46b4aa'), 0x46B4A5: ('jmp', '0x46b652'),
        0x46B4AD: ('call', '0x4678c0'), 0x46B4B5: ('movsx', 'eax, byte ptr [edx + 0x108b48]'),
        0x46B4C3: ('call', '0x499da0'), 0x46B55B: ('call', '0x468d10'),
        0x46B57F: ('call', '0x46b760'), 0x46B593: ('movsx', 'edx, byte ptr [ecx + 0x108b3a]'),
        0x46B5BF: ('call', '0x454c40'), 0x46B662: ('ret', '')}
    instructions = []
    for va, expected in wanted.items():
        instruction = next(md.disasm(raw[va-BASE:va-BASE+16], va, count=1))
        if (instruction.mnemonic, instruction.op_str) != expected:
            raise ValueError('world instruction identity')
        instructions.append({'va':hex(va), 'hex':instruction.bytes.hex(),
            'mnemonic':instruction.mnemonic, 'operands':instruction.op_str})
    return {'schema_version':1, 'source_image_sha256':SOURCE_SHA256,
        'function':hex(START), 'function_sha256':hashlib.sha256(raw[START-BASE:END-BASE]).hexdigest(),
        'gate_offset':0x108B32, 'gate_bytes':2, 'global_clear':hex(GLOBAL),
        'closed_return':0x46B662, 'first_open_call':0x4678C0, 'first_open_return':0x46B4B2,
        'instructions':instructions,
        'scope':'World admission only. Actual captured gate reaches first child entry; declared zero gate returns. No complete world tick/VM/opening/AI/waves.'}


class WorldAdmission(SchoolSceneOpeningEmulator):
    def __init__(self):
        self.world_loading = False
        self.world_probe = None
        self.world_visited = set()
        super().__init__()

    def _write_hook(self, uc, access, address, size, value, context):
        if not self.world_loading:
            return super()._write_hook(uc, access, address, size, value, context)
        if not any(a <= address and address+size <= b for a,b in ((STACK,STACK+65536),(GLOBAL,GLOBAL+4))):
            raise RuntimeError('world admission forbidden write '+hex(address))

    def _hook(self, uc, address, size, context):
        if not self.world_loading:
            return super()._hook(uc, address, size, context)
        if address == 0x4678C0:
            sp = uc.reg_read(UC_X86_REG_ESP)
            if self.world_probe != 'actual_captured_entry' or uc.reg_read(UC_X86_REG_ECX) != UNITCTRL or self.read(sp) != 0x46B4B2:
                raise RuntimeError('world first child natural stack')
            self.world_pending = {'va':hex(address),'receiver':UNITCTRL,'sp':sp,'return_va':hex(self.read(sp))}
            uc.emu_stop()
            return
        if address == 0x56CE80:
            return ExitEmulator._hook(self, uc, address, size, context)
        if START <= address < END:
            self.world_visited.add(address)
            return
        raise RuntimeError('world admission undeclared instruction '+hex(address))

    def audit_world_entry(self):
        if self.read(TACT+0x38) != 5 or self.read(TACT+0x170,'B') != 1 or self.read(TACT+0x171,'B') != 0 or self.read(GATE,'h') == 0:
            raise RuntimeError('world actual initialized parent gate')
        before = bytes(self.uc.mem_read(UNITCTRL+0x108B30,50))
        retained = self.capture_scene_memory([(STACK,STACK+65536),(GLOBAL,GLOBAL+4)])
        prior = self._function_ranges
        self.world_loading = True
        self._function_ranges = prior+((START,END),)
        try:
            captured_gate = self.read(GATE,'h')
            self.world_probe = 'actual_captured_entry'; self.world_pending = None
            self.world_visited = set()
            sp = STACK+0xFF00
            self.write(sp,RETURN)
            self.uc.reg_write(UC_X86_REG_ESP,sp); self.uc.reg_write(UC_X86_REG_ECX,UNITCTRL)
            self.uc.emu_start(START,RETURN,timeout=1_000_000,count=20000)
            after = bytes(self.uc.mem_read(UNITCTRL+0x108B30,50))
            if before != after or self.world_pending is None or self.uc.reg_read(UC_X86_REG_EIP) != 0x4678C0:
                raise RuntimeError('world actual first-child boundary/retention')
            actual = {'before_control_hex':before.hex(),'after_control_hex':after.hex(),
                'captured_gate':captured_gate,'pending':deepcopy(self.world_pending),
                'visited':sorted(self.world_visited),'children_executed':False,
                **self.verify_scene_memory(retained)}
            cpu = self.uc.context_save()
            stack = bytes(self.uc.mem_read(STACK,65536))
            global_before = bytes(self.uc.mem_read(GLOBAL,4))
            self.write(GATE,0,'h')
            self.world_probe = 'declared_zero_gate'; self.world_visited = set()
            value = self.call(START, receiver=UNITCTRL)
            if self.uc.reg_read(UC_X86_REG_EIP) != RETURN:
                raise RuntimeError('world zero gate natural return')
            probe = {'declared_gate':0,'write_address':hex(GATE),'return_eax':value,
                'return_sp':self.uc.reg_read(UC_X86_REG_ESP),
                'visited':sorted(self.world_visited),'first_child_executed':False,
                'actual_original_opening_completion':False}
            # Explicit isolated input restoration, never original gate completion.
            self.uc.mem_write(GATE,captured_gate.to_bytes(2,'little',signed=True)); self.uc.mem_write(STACK,stack)
            self.uc.mem_write(GLOBAL,global_before); self.uc.context_restore(cpu)
            if bytes(self.uc.mem_read(UNITCTRL+0x108B30,50)) != before:
                raise RuntimeError('world probe did not restore captured parent')
            probe.update(self.verify_scene_memory(retained))
            return {'actual_captured_entry':actual,'declared_zero_gate_return':probe,
                'captured_parent_restored':True,'full_world_tick_executed':False,'enemy_AI_executed':False}
        finally:
            self.world_loading = False; self._function_ranges = prior


def report():
    contract = source_contract()
    parent, deployment, old_opening = parent_evidence(), read_deployment(), read_opening()
    cases = []
    for index in range(3):
        name, sha = CHECKPOINTS[index]
        raw = (ROOT/f'.venv-audit/formation-actual-checkpoint-{index}.pkl').read_bytes()
        if hashlib.sha256(raw).hexdigest() != sha: raise ValueError('world trusted checkpoint identity')
        payload = pickle.loads(raw)
        if payload['source_sha'] != SOURCE_SHA256 or payload['evidence_kind'] != 'private_actual_cpu_after_full35_before_placement':
            raise ValueError('world checkpoint provenance')
        e = WorldAdmission()
        e.__dict__.update({k:v for k,v in payload['state'].items() if not k.startswith('_audit_') and k != 'uc'})
        for at,data in payload['memory']: e.uc.mem_write(at,data)
        e.uc.context_restore(payload['cpu'])
        if e.run_placement() != parent['cases'][index]['formation_placement']: raise ValueError('world parent placement')
        if e.run_deployment_tail() != deployment['cases'][index]['deployment_tail']: raise ValueError('world parent deployment')
        provenance = {'name':name,'provenance':{'checkpoint_sha256':sha,'placement_and_deployment_equal':True,'upstream_rerun':False}}
        opening = e.run_initialization_and_opening()
        if opening != old_opening['cases'][index]['scene_opening']: raise ValueError('world complete original opening parent')
        result = e.audit_world_entry()
        cases.append({**provenance,'parent_opening':opening,'world_admission':result})
        print('Original world admission '+name+': actual first-child stack; declared zero-gate return',flush=True)
    return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'source_contract':contract,'cases':cases,
        'original_world_tick_executed':False,'original_opening_completed':False,'persistent_write_authority':False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',required=True)
    args = parser.parse_args(); path = ROOT/args.out
    if path.exists(): parser.error('use a new immutable report path')
    path.write_text(report_text(report()),encoding='utf-8',newline='\n')
