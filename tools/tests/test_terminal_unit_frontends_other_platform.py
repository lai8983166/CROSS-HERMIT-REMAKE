import copy
import struct
import unittest
from types import SimpleNamespace

from unicorn import Uc,UC_ARCH_X86,UC_MODE_32
from unicorn import x86_const as x86
from tools import terminal_unit_frontends_emulation as source
from tools.terminal_unit_frontends_other_platform_verification import GDI,OtherLeaves,return_effects


class Fixture:
    def __init__(self):
        self.u=Uc(UC_ARCH_X86,UC_MODE_32)
        self.u.mem_map(0x592000,4096)
        self.u.mem_write(0x592000,source.previous.CODE[0x192000:0x193000])
        self.u.mem_map(0x12000000,8192)
        self.mutable=[]
        self.cpu_value=dict(ESP=0x12000800,EIP=0)

    def cpu(self):return dict(self.cpu_value)
    def read(self,p,n):return bytes(self.u.mem_read(p,n))
    def entry(self,pc,ret,args):
        self.cpu_value['EIP']=pc
        self.u.mem_write(self.cpu_value['ESP'],struct.pack('<'+'I'*(len(args)+1),ret,*args))


class OtherPlatformTests(unittest.TestCase):
    def test_real_common_marker_query_is_not_gdi(self):
        case=source.previous.overlay.parent.corpus()[0]
        replay=Fixture();replay.u.mem_map(0x594000,4096)
        replay.u.mem_write(0x594734,b'Dm-No-MakeTex\0')
        target=struct.unpack('<I',replay.read(0x5922C4,4))[0]
        replay.entry(target,0x41F416,[0x594734])
        checker=OtherLeaves(dict(input=case,platform=dict(trace=[])))
        event=dict(pc=target,effects=return_effects(replay,13,4),stop=False,continues_guest=False)
        self.assertTrue(checker.handles(replay,event))
        checker.validate_event(replay,event)
        self.assertEqual(checker.common_count,1)
        replay.u.mem_write(0x594734,b'Xm-No-MakeTex\0')
        with self.assertRaises(ValueError):
            OtherLeaves(dict(input=case,platform=dict(trace=[]))).validate_event(replay,event)

    def test_lstrcmp_uses_actual_win32_collation(self):
        case=source.previous.overlay.parent.corpus()[0]
        replay=Fixture()
        a,b=0x12001000,0x12001010
        for left,right in ((b'a',b'B'),(b'a',b'A'),(b'!',b'-')):
            replay.u.mem_write(a,left+b'\0');replay.u.mem_write(b,right+b'\0')
            replay.entry(0x7701F780,0x45521C,[a,b])
            checker=OtherLeaves(dict(input=case,platform=dict(trace=[])))
            actual=int(checker.kernel.lstrcmpA(left,right))
            byte_order=(left>right)-(left<right)
            self.assertNotEqual(actual,byte_order)
            event=dict(pc=0x7701F780,effects=return_effects(replay,actual,8),stop=False,continues_guest=False)
            checker.validate_event(replay,event)
            event['effects']=return_effects(replay,byte_order,8)
            with self.assertRaises(ValueError):
                OtherLeaves(dict(input=case,platform=dict(trace=[]))).validate_event(replay,event)

    def test_fixed_raw_clock_and_no_extra_effect(self):
        case=source.previous.overlay.parent.corpus()[0]
        replay=Fixture();replay.entry(0x77022640,0x45528D,[])
        row=dict(input=case,platform=dict(trace=[]))
        expected=return_effects(replay,source.clock_inputs()[case['name']][0],0)
        event=dict(pc=0x77022640,effects=expected,stop=False,continues_guest=False)
        check=OtherLeaves(row)
        check.validate_event(replay,event)
        for kind in ('clock','write','caller'):
            bad=copy.deepcopy(event)
            if kind=='clock':bad['effects'][0]['value']+=1
            elif kind=='write':bad['effects'].insert(0,dict(kind='mem_write',address=0x12001000,hex='00'))
            else:replay.entry(0x77022640,0x45528E,[])
            with self.subTest(kind=kind),self.assertRaises(ValueError):
                OtherLeaves(row).validate_event(replay,bad)

    def test_fresh_real_font_api_only_returns_planned_opaque_role(self):
        case=source.previous.overlay.parent.corpus()[0]
        replay=Fixture()
        face=0x12001000
        replay.u.mem_write(face,b'Arial\0')
        args=[16,0,0,0,400,0,0,0,0,0,0,0,0,face]
        target=struct.unpack('<I',replay.read(0x5920A0,4))[0]
        replay.entry(target,0x4CA7CB,args)
        row=dict(input=case,GDI_trace=[dict(name='CreateFontA',args=args,logical_result=0x6A101000,
                 native_result=dict(name='CreateFontA',args=args,result=123,
                                    memory_outputs=[],face_hex=b'Arial'.hex()))])
        event=dict(pc=target,effects=return_effects(replay,0x6A101000,56),stop=False,continues_guest=False)
        for mutate in (False,True):
            check=GDI(row)
            try:
                candidate=copy.deepcopy(event)
                if mutate:candidate['effects'][0]['value']+=1
                if mutate:
                    with self.assertRaises(ValueError):check.validate_event(replay,candidate)
                else:
                    check.validate_event(replay,candidate)
                    self.assertEqual(check.ordinal,1)
            finally:check.close()


if __name__=='__main__':unittest.main()
