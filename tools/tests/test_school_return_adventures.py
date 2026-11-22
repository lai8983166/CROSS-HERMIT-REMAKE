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

        self.assertEqual([r['id'] for r in probe.submit(6)['entries']], [17])
        self.assertEqual([r['id'] for r in probe.open(6,3)['entries']], [10,17])

        self.assertEqual([r['id'] for r in probe.submit(10)['entries']], [17])
        self.assertEqual([r['id'] for r in probe.open(6,4)['entries']], [13,17])

        self.assertEqual([r['id'] for r in probe.submit(13)['entries']], [17])
        self.assertEqual([r['id'] for r in probe.open(6,5)['entries']], [17])

    def test_mandatory_thirteen_scene_and_rewards_match_original(self):
        from tools.school_return_adventures_catalog import mandatory_adventure
        data = mandatory_adventure(13)
        self.assertEqual(data, json.loads((ROOT/'prototype/data/school_mandatory_thirteen.json').read_bytes()))
        self.assertEqual(data['scene']['template_count'], 93)
        self.assertEqual(data['scene']['script'], 'T0013.BIN')
        self.assertEqual(data['rewards']['base_points'], [350000,300000,250000,200000,75000])
        self.assertEqual(data['rewards']['objective_rewards'], [[0,0,0]] * 16)

    def test_mandatory_twenty_scene_and_rewards_match_original(self):
        from tools.school_return_adventures_catalog import mandatory_adventure
        data = mandatory_adventure(20)
        self.assertEqual(json.loads((ROOT/'prototype/data/school_mandatory_twenty.json').read_bytes()), data)
        self.assertEqual((data['scene']['template_count'],data['scene']['script']),(80,'T0020.BIN'))
        self.assertEqual(data['rewards']['base_points'],[250000,220000,160000,120000,75000])
        self.assertEqual(data['rewards']['objective_rewards'],[[0,0,0]]*16)

    def test_mandatory_twenty_one_scene_and_rewards_match_original(self):
        from tools.school_return_adventures_catalog import mandatory_adventure
        data = mandatory_adventure(21)
        self.assertEqual(data, json.loads((ROOT/'prototype/data/school_mandatory_twenty_one.json').read_bytes()))
        self.assertEqual((data['scene']['template_count'],data['scene']['script']), (91,'T0021.BIN'))
        self.assertEqual(data['rewards']['base_points'], [400000,350000,250000,200000,100000])
        self.assertEqual(data['rewards']['objective_rewards'], [[0,0,0]]*16)
        self.assertEqual(data['rewards']['unit_bonus'], 0)

    def test_mandatory_twenty_two_scene_and_rewards_match_original(self):
        from tools.school_return_adventures_catalog import mandatory_adventure
        data = mandatory_adventure(22)
        self.assertEqual(data, json.loads((ROOT/'prototype/data/school_mandatory_twenty_two.json').read_bytes()))
        self.assertEqual((data['scene']['template_count'], data['scene']['script']), (12, 'T0022.BIN'))
        self.assertEqual(data['rewards']['base_points'], [200000,180000,150000,100000,50000])
        self.assertEqual(data['rewards']['objective_rewards'], [[0,6,1]] + [[0,0,0]]*15)
        self.assertEqual(data['rewards']['time_bonuses'], [115,110,105])
        self.assertEqual(data['rewards']['unit_bonus'], 110)

    def test_mandatory_fourteen_scene_and_rewards_match_original(self):
        from tools.school_return_adventures_catalog import mandatory_adventure
        data = mandatory_adventure(14)
        self.assertEqual(data, json.loads((ROOT/'prototype/data/school_mandatory_fourteen.json').read_bytes()))
        self.assertEqual(data['scene']['script'], 'T0014.BIN')
        config = bytes.fromhex(data['scene']['configuration_hex'])
        self.assertEqual(list(config[26:]), [1,2,3] + [0]*13)
        self.assertEqual(data['rewards']['base_points'], [550000,450000,350000,200000,165000])

    def test_mandatory_nine_scene_and_rewards_match_original(self):
        from tools.school_return_adventures_catalog import mandatory_adventure
        data = mandatory_adventure(9)
        self.assertEqual(data, json.loads((ROOT/'prototype/data/school_mandatory_nine.json').read_bytes()))
        self.assertEqual((data['scene']['template_count'], data['scene']['script']), (75, 'T0009.BIN'))
        self.assertEqual(data['rewards']['base_points'], [120000,100000,70000,50000,30000])
        self.assertEqual(data['rewards']['objective_rewards'], [[0,0,0]] * 16)

    def test_mandatory_ten_scene_and_rewards_match_original(self):
        from tools.school_return_adventures_catalog import mandatory_adventure
        data = mandatory_adventure(10)
        self.assertEqual(data, json.loads((ROOT/'prototype/data/school_mandatory_ten.json').read_bytes()))
        self.assertEqual(data['scene']['template_count'], 96)
        self.assertEqual(data['scene']['script'], 'T0010.BIN')
        self.assertEqual(data['rewards']['base_points'], [135000,120000,85000,65000,30000])
        self.assertEqual(data['rewards']['objective_rewards'], [[0,0,0]] * 16)

    def test_mandatory_six_scene_and_rewards_match_original(self):
        from tools.school_return_adventures_catalog import mandatory_adventure
        data = mandatory_adventure(6)
        self.assertEqual(data, json.loads((ROOT/'prototype/data/school_mandatory_six.json').read_bytes()))
        self.assertEqual(data['scene']['template_count'], 68)
        self.assertEqual(data['scene']['script'], 'T0006.BIN')
        self.assertEqual(data['rewards']['base_points'], [90000,75000,60000,45000,30000])
        self.assertEqual(data['rewards']['objective_rewards'], [[0,0,0]] * 16)

    def test_mandatory_seven_scene_and_rewards_match_original(self):
        from tools.school_return_adventures_catalog import mandatory_seven
        data = mandatory_seven()
        self.assertEqual(data, json.loads((ROOT/'prototype/data/school_mandatory_seven.json').read_bytes()))
        self.assertEqual(data['rewards']['base_points'], [100000,90000,72000,54000,36000])
        self.assertEqual(data['scene']['script'], 'T0007.BIN')
        self.assertEqual(data['rewards']['objective_rewards'][0], [0,4,1])

    def test_august_five_optional_adventure_and_september_ledger(self):
        from tools.school_return_adventures_catalog import adventure_rules
        rules = adventure_rules(35)
        self.assertEqual(rules, json.loads((ROOT/'prototype/data/school_august_five_adventure.json').read_bytes()))
        self.assertEqual((rules['scene']['template_count'], rules['scene']['script']), (36, 'T0035.BIN'))
        rewards = rules['rewards']
        self.assertEqual(rewards['base_points'], [150000,135000,100000,75000,50000])
        self.assertEqual(rewards['unit_bonus'], 110)
        self.assertEqual(rewards['time_bonuses'], [115,110,105])
        self.assertEqual(rewards['fixed_items'], [0]*8)
        self.assertEqual(rewards['objective_rewards'], [[0,0,0]]*16)
        probe = LedgerProbe()
        for month, weeks in [(4, [(4,0),(5,5)]), (5, enumerate([8,0,17,7,17],1)),
                             (6, enumerate([4,6,10,13,17],1)), (7, enumerate([18,0,9,14,0],1)),
                             (8, enumerate([0,20,21,0],1))]:
            for week, selected in weeks:
                probe.open(month,week)
                probe.submit(selected)
        first = probe.open(8,5)['entries']
        self.assertEqual([row['id'] for row in first], [35,17])
        self.assertEqual((first[0]['limit'], first[0]['duration']), (-1,1))
        settled = probe.submit(35)['entries']
        self.assertEqual([(r['id'],r['busy'],r['elapsed']) for r in settled], [(35,0,1),(17,0,22)])
        self.assertEqual(probe.open(9,1)['entries'], settled)

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

    def test_july_one_week_adventure_consumed_or_expired(self):
        from tools.school_return_adventures_catalog import mandatory_adventure
        mission = mandatory_adventure(18)
        self.assertEqual(mission, json.loads((ROOT/'prototype/data/school_july_eighteen.json').read_bytes()))
        for decision in (18, 0):
            probe = LedgerProbe()
            for month, week, activity in [(4,4,0),(4,5,5),(5,1,8),(5,2,17),(5,3,0),(5,4,7),
                                          (5,5,0),(6,1,4),(6,2,6),(6,3,10),(6,4,13),(6,5,0)]:
                probe.open(month,week)
                probe.submit(activity)
            entries = probe.open(7,1)['entries']
            self.assertEqual([r['id'] for r in entries],[18,17])
            self.assertEqual((entries[0]['limit'],entries[0]['duration']),(1,0))
            self.assertEqual([r['id'] for r in probe.submit(decision)['entries']],[17])
            self.assertEqual([r['id'] for r in probe.open(7,2)['entries']],[17])
            probe.submit(0)
            self.assertEqual([r['id'] for r in probe.open(7,3)['entries']],[9,17])
            self.assertEqual([r['id'] for r in probe.submit(9)['entries']],[17])
            self.assertEqual([r['id'] for r in probe.open(7,4)['entries']],[14,17])
            self.assertEqual([r['id'] for r in probe.submit(14)['entries']],[17])
            self.assertEqual([r['id'] for r in probe.open(7,5)['entries']],[17])
            probe.submit(17 if decision == 18 else 0)
            self.assertEqual([r['id'] for r in probe.open(8,1)['entries']],[17])
            probe.submit(0)
            opened = probe.open(8,2)
            self.assertEqual([r['id'] for r in opened['entries']],[20,17])
            self.assertEqual((opened['entries'][0]['limit'],opened['entries'][0]['duration']),(1,0))
            self.assertEqual(probe.open(8,2),opened)
            self.assertEqual([r['id'] for r in probe.submit(20)['entries']], [17])
            self.assertEqual([r['id'] for r in probe.open(8,3)['entries']], [21,17])
            self.assertEqual([r['id'] for r in probe.submit(21)['entries']], [17])
            self.assertEqual([r['id'] for r in probe.open(8,4)['entries']], [17])
            probe.submit(17 if decision == 18 else 0)
            opened = probe.open(8,5)
            self.assertEqual([r['id'] for r in opened['entries']], [35,17])
            self.assertEqual((opened['entries'][0]['limit'],opened['entries'][0]['duration']),(-1,1))
            self.assertEqual(probe.open(8,5),opened)
            probe.submit(35)
            for week in (1, 2):
                self.assertEqual([r['id'] for r in probe.open(9,week)['entries']], [35,17])
                probe.submit(0)
            mandatory, *training = probe.open(9,3)['entries']
            self.assertEqual((mandatory['id'], mandatory['metadata'], mandatory['limit']), (22,[3,21,0],1))
            self.assertEqual([r['id'] for r in training], [35,17])
            self.assertEqual([r['id'] for r in probe.submit(22)['entries']], [35,17])
            next_mandatory, *training = probe.open(9,4)['entries']
            self.assertEqual((next_mandatory['id'], next_mandatory['metadata'], next_mandatory['limit']), (24,[3,22,0],1))
            self.assertEqual([r['id'] for r in training], [35,17])

    def test_original_timer_expiry_and_reusable17(self):
        probe=LedgerProbe();probe.open(4,4);probe.submit(0);probe.open(4,5);probe.submit(5);probe.open(5,1)
        after=probe.submit(17)['entries']
        self.assertEqual([r['id'] for r in after],[8,17])
        self.assertEqual((after[1]['busy'],after[1]['busy_elapsed'],after[1]['elapsed']),(0,1,3))
        for i in range(4):after=probe.submit(0)['entries']
        self.assertEqual([r['id'] for r in after],[17])
        self.assertEqual(probe.open(5,1)['entries'],after,'once-opened flag prevents expired8 from reopening')


if __name__=='__main__':unittest.main()
