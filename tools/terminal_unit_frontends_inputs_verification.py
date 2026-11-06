"""Initial input reconstruction and strictly bounded host call scaffolding.

Native opaque identities are declared initial OS inputs. Guest memory, CPU,
permissions and write ownership are reconstructed before original execution;
no reported final state is used as an initialization oracle.
"""
import copy
import struct
from types import SimpleNamespace

from tools import terminal_unit_frontends_emulation as source
from tools import battle_live_terminal_emulation as original_battle
from tools.terminal_unit_frontends_trace import CPU_REGISTERS
from unicorn import x86_const as x86


def need(ok, message):
    if not ok:
        raise ValueError(message)


class InitialInputs:
    def __init__(self, row):
        self.row = row

    def __call__(self, execution, original_code, ranges):
        need(original_code == source.previous.CODE and tuple(ranges) == source.RANGES,
             'independently pinned original executable and admitted source ranges')
        case = self.row['input']
        need(case in source.previous.overlay.parent.corpus(), 'exact selected case input')
        platform = self.row['unit_frontends']['initial_platform']
        need(platform['device'] == platform['GPU']['device'], 'one declared initial native device')
        gpu = SimpleNamespace(hello=copy.deepcopy(platform['GPU']),
                              device=copy.deepcopy(platform['device']))
        crt = SimpleNamespace(hello=copy.deepcopy(platform['CRT']), trace=[])
        def unexpected(*args, **kwargs):
            raise ValueError('no native execution or after-state during initial reconstruction')
        crt.request = unexpected
        fresh = None
        try:
            fresh = source.UnitFrontendMachine(case, crt, gpu,
                                               source.clock_inputs()[case['name']])
            need(execution['initial_CPU'] == fresh.cpu(), 'fresh entire initial57 CPU')
            need(execution['initial_regions'] == [list(x) for x in fresh.uc.mem_regions()],
                 'fresh initial whole memory partition and permissions')
            need(execution['initial_mutable'] == [list(x) for x in fresh.mutable],
                 'fresh exact initial guest write ownership')
            expected = fresh.snapshot()
            need(len(expected) == len(execution['initial_memory']), 'all fresh initial regions')
            for actual, want in zip(execution['initial_memory'], expected):
                need(actual == want, 'fresh complete initial memory at '+hex(want['pointer']))
            need(self.row['unit_frontends']['record_input'] == fresh.unit_record_input,
                 'source-derived B0 and every explicit early experiment field')
            need(self.row['unit_frontends']['application_text']['contract'] == fresh.application_text_contract,
                 'declared application input and exact original member-query contract')
        finally:
            if fresh is not None:
                fresh.name_platform.close()


class Driver:
    """Admit root stack ABI, fixed keyboard captures and exact prior CPU only."""
    def __init__(self, case):
        self.case = case
        self.root_count = 0
        self.restores = 0
        self.keyboard_count = 0
        self.frontier_reached = False
        self.active_keyboard_stop = None
        self.names = {getattr(x86, 'UC_X86_REG_'+name):name for name in CPU_REGISTERS}
        e=source.previous
        self.initial_root_plan=[(0x57B9D0,0,[1]),(0x576F60,0,[]),
                                (0x4075E0,source.minimap.BACKGROUND,[]),
                                (0x4075E0,source.minimap.FOG,[]),
                                (0x407780,source.minimap.BACKGROUND,[]),
                                (0x404870,source.minimap.BACKGROUND,[0x64001000,0,source.minimap.BMP_POINTER,1,1,1]),
                                (0x4404A0,source.minimap.MAP,[2048,1536]),
                                (0x497800,e.overlay.WORK,[]),
                                (0x467020,e.CTRL,[e.terminal.TARGET,self.case_job()])]
        self.initial_root_plan += [(0x437C90,original_battle.FINE,[u+off])
                                   for u in (e.terminal.UNIT,e.terminal.TARGET) for off in (0x2F4,0x3E0)]
        self.initial_root_plan += [(0x467020,e.CTRL,[e.terminal.UNIT,self.case_job()])]
        self.initial_root_plan += [(entry,e.CTRL,[]) for _ in range(
            1 if case['name']=='neutral_running' else 3) for entry in (0x46B470,0x432100)]
        self.initial_root_index=0
        self.scene_roots=0

    @staticmethod
    def word(replay, pointer):
        return struct.unpack('<I', replay.read(pointer, 4))[0]

    def root(self, replay, entry, receiver, args):
        e = source.previous
        t = e.terminal
        current=replay.cpu()['EIP']
        need((self.initial_root_index==0 and current==0) or current==e.RETURN
             or current in (0x4116A4,0x411CE2) or (current==source.WAIT and self.frontier_reached),
             'new root only after natural return or declared keyboard/forward frontier')
        if self.initial_root_index<len(self.initial_root_plan):
            need((entry,receiver,args)==self.initial_root_plan[self.initial_root_index],
                 'fixed early CRT/unit/world/event original root sequence')
            self.initial_root_index+=1
        if entry==0x4539B0:
            need(self.scene_roots==0 and self.initial_root_index==len(self.initial_root_plan)
                 and self.word(replay,e.TASK+0x38)==20
                 and replay.read(e.TASK+0x171,2)==b'\x01\x01',
                 'one scene-loop root only after natural completed terminal stage20')
            self.scene_roots+=1
        # The whitelist contains only explicit host method roots already used
        # by the frozen harness, plus original unit CRT/cache roots. It is not
        # derived from the submitted report's resource/root annotations.
        fixed = {
            0x57B9D0:(0,[1]), 0x576F60:(0,[]),
            0x576FA0:(0,[]), 0x57BA60:(0,[]),
            0x497800:(e.overlay.WORK,[]), 0x46B470:(e.CTRL,[]),
            0x432100:(e.CTRL,[]), 0x425DE0:(source.APPLICATION_INPUT,[]),
            0x454CF0:(e.TASK,[]), 0x453F10:(e.TASK,[]),
            0x4539B0:(e.TASK,[]), 0x466F00:(e.CTRL,[]),
            0x40D970:(e.MANAGER,[e.MAIN]),
            0x40DB10:(e.MANAGER,[4096]),
            0x40DBF0:(e.MANAGER,[65536]),
            0x40DB90:(e.MANAGER,[]), 0x40DC80:(e.MANAGER,[]),
        }
        if entry in fixed:
            need((receiver,args) == fixed[entry], 'exact original root receiver/arguments')
            return
        if entry == 0x467020:
            need(receiver == e.CTRL and args in ([t.TARGET, self.case_job()],
                                                 [t.UNIT, self.case_job()]),
                 'only declared target/actor unit binding roots')
        elif entry == 0x437C90:
            need(receiver == original_battle.FINE and args in [[u+off] for u in (t.UNIT,t.TARGET)
                                                  for off in (0x2F4,0x3E0)],
                 'only original unit fine-grid insertion roots')
        elif entry in (0x4075E0,0x4077C0):
            records=[e.TASK+0x68]+[e.CTRL+off for off in e.CONTROLLER_PACKETS]
            if entry==0x4075E0:records += [source.minimap.BACKGROUND,source.minimap.FOG]
            need(receiver in records
                 and args == ([] if entry == 0x4075E0 else [e.MAIN]),
                 'original declared scene/controller packet constructor/owner roots')
        elif entry==0x407780:
            need(receiver==source.minimap.BACKGROUND and not args,'original empty minimap background reset')
        elif entry==0x404870:
            need(receiver==source.minimap.BACKGROUND and
                 args==[0x64001000,0,source.minimap.BMP_POINTER,1,1,1],
                 'original complete real MAP05 memory bitmap loader ABI')
        elif entry==0x4404A0:
            need(receiver==source.minimap.MAP and args==[2048,1536],
                 'original fog initialization from real MAP05 dimensions')
        elif entry == 0x42AE20:
            need(receiver == 0 and len(args) == 1 and args[0] in (e.overlay.PATH,e.COMMON_PATH_PTR),
                 'only original declared resource file paths')
        elif entry == 0x428AD0:
            need(receiver == 0 and len(args) == 1, 'original cdecl buffer free ABI')
            # Ownership of this user pointer is independently enforced at the
            # native HeapValidate/HeapFree leaf, before any release is accepted.
            need(0x50001000 <= args[0] < 0x64000000, 'bounded original CRT-owned user buffer')
        elif entry == 0x416790:
            need(receiver == e.MAIN and len(args) == 2 and args[1] in (20,90)
                 and 0x50001000 <= args[0] < 0x64000000, 'original resource registration ABI')
        elif entry == 0x41F4E0:
            need(receiver == e.MAIN+0x844 and len(args) == 1 and args[0] in (20,30,31,32,90),
                 'only declared resource bank destruction roots')
        elif entry == 0x403730:
            need(not args and any(a <= receiver and receiver+84 <= b for a,b in replay.mutable),
                 'original bounded owned image-record destructor')
        else:
            raise ValueError('unadmitted original host root '+hex(entry))

    def case_job(self):
        return next(c['aftermath']['combat']['job'] for c in original_battle.combat_corpus()
                    if c['name'] == self.case['base'])

    def keyboard(self, replay, actions, row):
        e = source.previous
        need(replay.cpu()['EIP'] in (e.RETURN,0x4116A4,0x411CE2),
             'keyboard fragment begins only at a natural return or prior keyboard boundary')
        stop=row['after_CPU']['EIP']
        need(stop in (0x4116A4,0x411CE2) and row['end'] in (0,stop),
             'keyboard has its declared original stop or an audited hook stop')
        scene = '76' if self.case['name'] == 'neutral_running' else '77'
        captures = e.followup.parent.parent.input_contract()['streams'][scene]['captures']
        raw = captures[self.keyboard_count % len(captures)]['raw_device_hex']
        bp = e.STACK+0xF800
        expected = [dict(kind='mem_write',address=e.KEYBOARD+12,hex=raw),
                    dict(kind='mem_write',address=bp-4,hex=struct.pack('<I',e.KEYBOARD).hex())]
        if stop == 0x411CE2:
            expected.append(dict(kind='mem_write',address=bp-8,
                                 hex=struct.pack('<I',e.KEYBOARD+0x890).hex()))
        expected += [dict(kind='reg_write',register=getattr(x86,'UC_X86_REG_'+name),value=value)
                     for name,value in (('EBP',bp),('ESP',bp-0x70),('EFLAGS',0x202))]
        need(row['entry'] == 0x4113D5
             and actions == expected, 'exact pinned raw keyboard input and original fragment locals')
        self.keyboard_count += 1
        self.active_keyboard_stop = stop

    def __call__(self, replay, actions, row, history):
        self.active_keyboard_stop = None
        actions = list(actions)
        # Supplemental cleanup restores an actual previously captured entire
        # CPU, never a reported after-CPU chosen by the evidence producer.
        if len(actions) >= len(CPU_REGISTERS):
            first = actions[:len(CPU_REGISTERS)]
            if all(a['kind']=='reg_write' for a in first):
                values = {self.names.get(a['register']):a['value'] for a in first}
                if set(values) == set(CPU_REGISTERS):
                    need(self.frontier_reached,'full CPU restoration only after frozen forward frontier')
                    need(values in history, 'whole CPU restore must equal prior independent execution')
                    self.restores += 1
                    actions = actions[len(CPU_REGISTERS):]
        while actions and actions[0]['kind'] == 'mem_protect':
            a = actions.pop(0)
            need((a['address'],a['bytes'],a['permission']) in ((0x5FF000,4096,3),
                 (*source.previous.SORTING_RW_PAGES,3)), 'only original writable data pages exposed')
        if not actions:
            need(row is None or row['entry'] == replay.cpu()['EIP'],
                 'rootless continuation begins at actual independently executed PC')
            return
        need(row is not None, 'no final synthetic writes')
        if actions[0].get('address') == source.previous.KEYBOARD+12:
            self.keyboard(replay,actions,row)
            return
        stack = source.previous.STACK+0xF000
        need(actions[0] == dict(kind='mem_write',address=stack,
                               hex=struct.pack('<I',source.previous.RETURN).hex()),
             'root ABI begins with owned stack return address')
        writes = []
        i = 0
        while i < len(actions) and actions[i]['kind'] == 'mem_write':
            a = actions[i]
            need(a['address'] == stack+4*i and len(a['hex']) == 8,
                 'only contiguous four-byte root arguments on owned stack')
            writes.append(struct.unpack('<I',bytes.fromhex(a['hex']))[0])
            i += 1
        need(len(actions)-i == 2, 'root changes only ESP and ECX')
        sp, cx = actions[i:]
        need(sp == dict(kind='reg_write',register=x86.UC_X86_REG_ESP,value=stack)
             and cx['kind']=='reg_write' and cx['register']==x86.UC_X86_REG_ECX,
             'root register ABI order and values')
        self.root(replay,row['entry'],cx['value'],writes[1:])
        self.root_count += 1
