import copy
import struct
import unittest
from types import SimpleNamespace

from unicorn import x86_const as x86
from tools import terminal_unit_frontends_emulation as source
from tools.terminal_unit_frontends_inputs_verification import Driver,InitialInputs
from tools.terminal_unit_frontends_trace import CPU_REGISTERS


class InitialInputGuards(unittest.TestCase):
    def test_original_empty_application_input_query_and_old_globals_restored(self):
        device=dict(pointer=0x10001000,vtable=0x10002000,methods={'80':0x10003000})
        gpu=SimpleNamespace(device=device,hello=dict(device=device,window_size=[256,256]),trace=[])
        crt=SimpleNamespace(hello={},trace=[])
        case=source.previous.overlay.parent.corpus()[0]
        m=source.UnitFrontendMachine(case,crt,gpu,source.clock_inputs()[case['name']])
        original_input=source.previous.INPUT
        try:
            this=source.images.PATH_OWNER+0x180
            before=m.read(source.images.PATH_OWNER,0x2000)
            with source.application_input_binding():
                m.resource_root('bounded_original_empty_application_query',0x425A50,receiver=this)
                for _ in range(2):
                    m.resource_root('original_request_close_IME',0x425ED0,[0],receiver=this)
                    self.assertEqual(m.get(this+0x630,'B'),255)
                    m.task_step(0x425DE0,source.previous.INPUT)
                    self.assertEqual(m.get(this+0x630,'B'),0)
            self.assertEqual(m.getreg('EAX'),0)
            self.assertEqual(m.application_text_query_count,1)
            self.assertEqual(source.previous.INPUT,original_input)
            self.assertEqual(m.read(this+0x528,1),b'\0')
            self.assertEqual(m.read(source.images.PATH_OWNER,0x180),before[:0x180])
        finally:m.name_platform.close()

    def test_complete_initial_reconstruction_and_separate_identity_owners(self):
        # Synthetic opaque OS identities are declared fixture inputs; no GPU
        # API executes and no source after-state initializes this constructor.
        device=dict(pointer=0x10001000,vtable=0x10002000,methods={'80':0x10003000})
        gpu=SimpleNamespace(device=device,hello=dict(device=device,window_size=[256,256]))
        crt=SimpleNamespace(hello={},trace=[])
        case=source.previous.overlay.parent.corpus()[0]
        m=source.UnitFrontendMachine(case,crt,gpu,source.clock_inputs()[case['name']])
        try:
            row=dict(input=case,unit_frontends=dict(initial_platform=m.initial_platform,
                 record_input=m.unit_record_input,application_text=dict(contract=m.application_text_contract)))
            execution=dict(initial_CPU=m.cpu(),initial_memory=m.snapshot(),
                           initial_regions=[list(x) for x in m.uc.mem_regions()],
                           initial_mutable=[list(x) for x in m.mutable])
            check=InitialInputs(row)
            check(execution,source.previous.CODE,source.RANGES)
            for kind in ('CPU','memory','ownership'):
                bad=copy.deepcopy(execution)
                if kind=='CPU':bad['initial_CPU']['EAX']=1
                elif kind=='memory':bad['initial_memory'][0]['hex']='01'+bad['initial_memory'][0]['hex'][2:]
                else:bad['initial_mutable'][0][1]+=4
                with self.subTest(kind=kind),self.assertRaises(ValueError):
                    check(bad,source.previous.CODE,source.RANGES)
            before=copy.deepcopy(m.space.ledger())
            m.unit_space.guest('overlay-unit-frontends-0-0',0x123456)
            self.assertEqual(m.space.ledger(),before)
            self.assertIn('overlay-unit-frontends-0-0',{x['domain'] for x in m.unit_space.ledger()})
            self.assertTrue(all(x['domain']=='overlay' for x in m.space.ledger()))
            self.assertIsNot(m.space.native_to_guest,m.unit_space.native_to_guest)
        finally:
            m.name_platform.close()


class DriverGuards(unittest.TestCase):
    def setUp(self):
        self.case = source.previous.overlay.parent.corpus()[0]
        self.driver = Driver(self.case)
        self.replay = SimpleNamespace(cpu=lambda:dict(EIP=source.previous.RETURN), mutable=[])
        self.driver.initial_root_index=len(self.driver.initial_root_plan)
        self.stack = source.previous.STACK+0xF000
        self.actions = [dict(kind='mem_write',address=self.stack,
                             hex=struct.pack('<I',source.previous.RETURN).hex()),
                        dict(kind='reg_write',register=x86.UC_X86_REG_ESP,value=self.stack),
                        dict(kind='reg_write',register=x86.UC_X86_REG_ECX,value=source.previous.TASK)]
        self.row = dict(entry=0x454CF0,end=source.previous.RETURN)

    def test_only_explicit_root_abi_admitted(self):
        self.driver(self.replay,self.actions,self.row,[])
        self.assertEqual(self.driver.root_count,1)
        for target in ('return','receiver','extra','entry'):
            actions,row = copy.deepcopy(self.actions),dict(self.row)
            if target == 'return':actions[0]['hex']='00000000'
            elif target == 'receiver':actions[-1]['value']+=4
            elif target == 'extra':actions.insert(0,dict(kind='mem_write',address=source.previous.TASK+0x38,hex='14000000'))
            else:row['entry']=0x473860
            with self.subTest(target=target),self.assertRaises(ValueError):
                self.driver(self.replay,actions,row,[])

    def test_rootless_continuation_uses_actual_eip(self):
        self.replay.cpu=lambda:dict(EIP=0x454CF0)
        self.driver(self.replay,[],dict(entry=0x454CF0),[])
        with self.assertRaises(ValueError):
            self.driver(self.replay,[],dict(entry=0x453F10),[])
        with self.assertRaises(ValueError):
            self.driver(self.replay,self.actions,None,[])

    def test_mid_function_stop_cannot_start_another_root(self):
        self.replay.cpu=lambda:dict(EIP=0x454D00)
        with self.assertRaisesRegex(ValueError,'natural return'):
            self.driver(self.replay,self.actions,self.row,[])

    def test_first_root_must_be_fresh_original_heap_initialization(self):
        self.driver=Driver(self.case)
        self.replay.cpu=lambda:dict(EIP=0)
        with self.assertRaisesRegex(ValueError,'fixed early'):
            self.driver(self.replay,self.actions,self.row,[])

    def test_complete_cpu_restore_must_be_previous_execution(self):
        cpu = {name:0 for name in CPU_REGISTERS}
        actions = [dict(kind='reg_write',register=getattr(x86,'UC_X86_REG_'+name),value=value)
                   for name,value in cpu.items()]
        with self.assertRaises(ValueError):
            self.driver(self.replay,actions,None,[cpu])
        self.driver.frontier_reached=True
        self.driver(self.replay,actions,None,[cpu])
        actions[0]['value']=1
        with self.assertRaises(ValueError):
            self.driver(self.replay,actions,None,[cpu])

    def test_keyboard_raw_bytes_order_and_locals(self):
        e = source.previous
        captures = e.followup.parent.parent.input_contract()['streams']['76']['captures']
        bp = e.STACK+0xF800
        for capture in captures:
            actions = [dict(kind='mem_write',address=e.KEYBOARD+12,hex=capture['raw_device_hex']),
                       dict(kind='mem_write',address=bp-4,hex=struct.pack('<I',e.KEYBOARD).hex())]
            actions += [dict(kind='reg_write',register=getattr(x86,'UC_X86_REG_'+name),value=value)
                        for name,value in (('EBP',bp),('ESP',bp-0x70),('EFLAGS',0x202))]
            row = dict(entry=0x4113D5,end=0x4116A4,after_CPU=dict(EIP=0x4116A4))
            bad = copy.deepcopy(actions);bad[0]['hex']='ff'*256
            with self.assertRaises(ValueError):self.driver(self.replay,bad,row,[])
            self.driver(self.replay,actions,row,[])
        self.assertEqual(self.driver.keyboard_count,len(captures))
        row['end']=0
        actions[0]['hex']=captures[0]['raw_device_hex']
        self.replay.cpu=lambda:dict(EIP=0x56CF01)
        with self.assertRaisesRegex(ValueError,'natural return'):
            self.driver(self.replay,actions,row,[])
        self.replay.cpu=lambda:dict(EIP=e.RETURN)
        self.driver(self.replay,actions,row,[])
        self.assertEqual(self.driver.active_keyboard_stop,0x4116A4)

    def test_keyboard_hook_stop_requires_the_current_declared_fragment(self):
        from tools.terminal_unit_frontends_verification import CaseVerifier
        verifier=CaseVerifier.__new__(CaseVerifier)
        verifier.driver=self.driver
        event=dict(pc=0x411CE2,effects=[],CPU_changes={},stop=True,continues_guest=False)
        replay=SimpleNamespace(read=lambda address,size:bytes(size))
        self.driver.active_keyboard_stop=0x411CE2
        verifier.event(replay,event)
        self.driver.active_keyboard_stop=None
        with self.assertRaises(ValueError):verifier.event(replay,event)
        self.driver.active_keyboard_stop=0x411CE2
        event['CPU_changes']={'EAX':1}
        with self.assertRaises(ValueError):verifier.event(replay,event)


if __name__ == '__main__':
    unittest.main()
