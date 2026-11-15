import json
import struct
import unittest
from tools.school_adventure_scene_rules import catalog
from tools.tactics_exit_emulation import ExitEmulator, TASK, STACK, RETURN, ROOT
from unicorn.x86_const import UC_X86_REG_EIP, UC_X86_REG_ESP


class SceneRulesTests(unittest.TestCase):
    def test_source_offsets_and_event_cells(self):
        data = catalog()
        self.assertEqual(data, json.loads((ROOT/'prototype/data/school_adventure_scene_rules.json').read_text(encoding='utf8')))
        opening = data['scenes']['8']['scripts'][0]
        waves = [c for c in opening['commands'] if c['opcode'] == 136]
        self.assertEqual([c['offset'] for c in waves], list(range(0x1ec,0x3ec,32)))
        self.assertEqual([c['values'][1] for c in waves], [10800,14400,18000,28800,36000,46800,50400,61200,68400,75600,82800,86400,79200,86400,82800,9000])
        self.assertEqual(data['scenes']['17']['event1_cells'], [[90,15],[90,16],[91,16],[91,17],[92,17],[92,18]])
        self.assertEqual([len(p) for p in opening['pages']], [5,3,4,3])
        self.assertEqual([len(p) for p in data['scenes']['17']['scripts'][0]['pages']], [4,1,3])

    def test_fana_current_original_record(self):
        e = ExitEmulator()
        e._function_ranges += ((0x4B93C0,0x4BAA90),(0x4DB340,0x4DB420),
            (0x4DCF00,0x4DD510),(0x56CFCC,0x56CFF3),(0x56CEC0,0x56CF18),(0x4D1BA0,0x4D1C00))
        character,record,modifier = TASK+0x2000,TASK+0x3000,TASK+0x4000
        e.uc.mem_write(character,bytes(e.uc.mem_read(0x6F5088+5*0x4a0,0x4a0)))
        e.write(character,5,'H');e.write(character+6,4,'H');e.write(character+0x50,28,'B')
        for i,a in enumerate([17,69,11,33,12,33,34]):
            e.write(character+0xc+i*8,a,'B')
        e.uc.mem_write(character+0x52,bytes(32));e.write(character+0x52,11,'H')
        self.assertEqual(e.read(0x738998+11*4),0)
        original = bytes(e.uc.mem_read(character,0x4a0))
        sp=STACK+0xff00
        for i,v in enumerate([RETURN,character,record,modifier]):e.write(sp+4*i,v)
        e.uc.reg_write(UC_X86_REG_ESP,sp)
        e.uc.emu_start(0x4B93C0,RETURN,timeout=1_000_000,count=100_000)
        self.assertEqual(e.uc.reg_read(UC_X86_REG_EIP),RETURN)
        self.assertEqual(e.uc.reg_read(UC_X86_REG_ESP),sp+4)
        self.assertEqual(bytes(e.uc.mem_read(character,0x4a0)),original)
        raw=bytes(e.uc.mem_read(record,176));mod=bytes(e.uc.mem_read(modifier,76))
        self.assertEqual([(i,v[0]) for i,v in enumerate(struct.iter_unpack('<h',mod)) if v[0]],[(12,35)])
        self.assertEqual([struct.unpack_from('<H',raw,o)[0] for o in (20,26,56,58,60)], [259,161,149,36,10])
        saved=json.loads((ROOT/'analysis/fana-current-record-local-v1-20261115.json').read_text(encoding='utf8'))
        self.assertEqual(raw.hex(),saved['record_hex'])
        self.assertEqual(mod.hex(),saved['modifier_hex'])


if __name__=='__main__':unittest.main()
