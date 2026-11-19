import hashlib
import json
import struct
import unittest
from unicorn import UC_HOOK_MEM_WRITE
from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_EIP, UC_X86_REG_ESP

from tools.school_return_adventures_catalog import catalog
from tools.tactics_exit_emulation import ExitEmulator, ROOT, STACK
from tools.school_adventure_handoff_emulation import ledger_snapshot


class LedgerProbe(ExitEmulator):
    """Existing bounded CPU runner, only ledger bodies; class rating is declared."""
    def __init__(self):
        super().__init__()
        self._function_ranges=((0x4a17b0,0x4a1920),(0x4a1920,0x4a1c70),(0x4a9d90,0x4aa320))
        self.selected=0
        self.uc.mem_write(0x7a55fc,bytes(101))
        self.uc.mem_write(0x7a5662,bytes(80*16))
        self.write(0x7a5b62,0,'h')
        self.uc.hook_add(UC_HOOK_MEM_WRITE,self._write)

    def _write(self,uc,access,address,size,value,context):
        if any(a<=address and address+size<=b for a,b in [(STACK,STACK+0x10000),(0x7a55fc,0x7a5b64)]):return
        raise RuntimeError(f'ledger write outside contract {address:#x}/{size}')

    def _hook(self,uc,address,size,context):
        if address==0x4a95f0:
            sp=uc.reg_read(UC_X86_REG_ESP)
            destination,group=struct.unpack('<II',uc.mem_read(sp+4,8))
            state=2 if group==0 and self.selected else 4 if group==0 else 0
            uc.mem_write(destination,struct.pack('<7h',state,0,0,0,0,self.selected if state==2 else 0,0))
            uc.reg_write(UC_X86_REG_EAX,destination)
            uc.reg_write(UC_X86_REG_ESP,sp+12);uc.reg_write(UC_X86_REG_EIP,self.read(sp));return
        return super()._hook(uc,address,size,context)

    def open(self,month,week):
        self.write(0x7a528e,month,'h');self.write(0x7a5290,week,'h');self.call(0x4a17b0)
        return ledger_snapshot(self)

    def submit(self,selected):
        self.selected=selected;self.call(0x4a1920);return ledger_snapshot(self)


class SchoolReturnAdventuresTests(unittest.TestCase):
    def test_june_mandatory_four_and_next_school(self):
        from tools.school_return_adventures_catalog import mandatory_adventure
        data = mandatory_adventure(4)
        self.assertEqual(data, json.loads((ROOT/'prototype/data/school_mandatory_four.json').read_bytes()))
        self.assertEqual(data['scene']['script'], 'T0004.BIN')
        self.assertEqual(data['rewards']['base_points'], [100000, 80000, 60000, 45000, 30000])
        self.assertEqual(data['rewards']['time_bonuses'], [115, 110, 105])
        self.assertEqual(data['rewards']['objective_rewards'][:2], [[0,3,1], [0,2,2]])
        probe = LedgerProbe()
        for month, week, action in [(4,4,0), (4,5,5), (5,1,8), (5,2,0), (5,3,17), (5,4,7), (5,5,17)]:
            probe.open(month,week)
            probe.submit(action)
        self.assertEqual([r['id'] for r in probe.open(6,1)['entries']], [4,17])
        self.assertEqual([r['id'] for r in probe.submit(4)['entries']], [17])
        self.assertEqual([r['id'] for r in probe.open(6,2)['entries']], [6,17])

    def test_mandatory_seven_scene_and_rewards_match_original(self):
        from tools.school_return_adventures_catalog import mandatory_seven
        data = mandatory_seven()
        self.assertEqual(data, json.loads((ROOT/'prototype/data/school_mandatory_seven.json').read_bytes()))
        self.assertEqual(data['rewards']['base_points'], [100000,90000,72000,54000,36000])
        self.assertEqual(data['scene']['script'], 'T0007.BIN')
        self.assertEqual(data['rewards']['objective_rewards'][0], [0,4,1])

    def test_catalog_identity_complete_date_filter_and_resources(self):
        data=catalog()
        self.assertEqual(data,json.loads((ROOT/'prototype/data/school_return_adventures.json').read_text(encoding='utf8')))
        self.assertEqual([r['id'] for r in data['adventures'] if r['present'] and r['gate'] and r['kind'] and (r['month'],r['week'])==(5,1)],[8])
        self.assertEqual(len(data['adventures']),100)
        for sid in (8,17):
            row=data['adventures'][sid-1]
            self.assertEqual(row['rounds'],[{'scene_id':sid,'selection_word':1}])
            self.assertEqual(len(data['scenes'][str(sid)]['map_resources']),4)

    def test_original_ledger_preserves17_and_removes5_then_opens8_once(self):
        probe=LedgerProbe()
        a=probe.open(4,4)['entries'];self.assertEqual([r['id'] for r in a],[17])
        self.assertEqual((a[0]['limit'],a[0]['duration']),(-1,1))
        self.assertEqual(probe.submit(0)['entries'][0]['elapsed'],1)
        self.assertEqual([r['id'] for r in probe.open(4,5)['entries']],[5,17])
        self.assertEqual([r['id'] for r in probe.submit(5)['entries']],[17])
        result=probe.open(5,1)
        self.assertEqual([r['id'] for r in result['entries']],[8,17])
        self.assertEqual([r['elapsed'] for r in result['entries']],[0,2])
        self.assertEqual(probe.open(5,1),result)
        self.assertEqual(bytes(probe.uc.mem_read(0x7a55fd,100)).count(1),3)
        self.assertEqual([r['id'] for r in probe.submit(8)['entries']],[17])

    def test_original_timer_expiry_and_reusable17(self):
        probe=LedgerProbe();probe.open(4,4);probe.submit(0);probe.open(4,5);probe.submit(5);probe.open(5,1)
        after=probe.submit(17)['entries']
        self.assertEqual([r['id'] for r in after],[8,17])
        self.assertEqual((after[1]['busy'],after[1]['busy_elapsed'],after[1]['elapsed']),(0,1,3))
        for i in range(4):after=probe.submit(0)['entries']
        self.assertEqual([r['id'] for r in after],[17])
        self.assertEqual(probe.open(5,1)['entries'],after,'once-opened flag prevents expired8 from reopening')


if __name__=='__main__':unittest.main()
