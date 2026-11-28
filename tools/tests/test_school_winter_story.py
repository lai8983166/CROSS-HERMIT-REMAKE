import hashlib
import json
import struct
import unittest

from unicorn import Uc, UC_ARCH_X86, UC_MODE_32
from unicorn.x86_const import UC_X86_REG_EBP, UC_X86_REG_EIP
from tools.school_winter_story_export import ROOT, december_three, winter
from tools.tactics_exit_emulation import SOURCE, SOURCE_SHA256


class WinterStoryTests(unittest.TestCase):
    def test_programs_are_reproducible_from_original_routes_and_chapters(self):
        expected = ROOT / 'prototype/data'
        self.assertEqual(json.loads((expected / 'school_year_december_three.json').read_bytes()), december_three())
        data = winter()
        encoded = (json.dumps(data, ensure_ascii=False, separators=(',', ':')) + '\n').encode()
        self.assertEqual((expected / 'school_year_winter.json').read_bytes(), encoded)
        for row in data['arrivals']:
            if not row['terminal']:
                card = row['date_card']
                image = ROOT / 'prototype' / card['image'].removeprefix('res://')
                self.assertEqual(hashlib.sha256(image.read_bytes()).hexdigest(), card['png_sha256'])
        last = data['arrivals'][-1]
        self.assertEqual((last['departure'], last['arrival']), ((15, 4), [15, 5]))
        self.assertEqual([(r['router'], r['date']) for r in last['routes']], [('CH003.YBC', [15, 5])])
        self.assertEqual(last['sections'], [{'chapter': '097', 'effects': []}])

    def test_final_successor_dispatches_the_original_ending_task(self):
        raw = SOURCE.read_bytes()
        entry, = struct.unpack_from('<I', raw, 0x49e4d3-0x400000 + 18*4)
        self.assertEqual(entry, 0x49e3d0)
        offset = entry - 0x400000
        self.assertEqual(raw[offset], 0xe8)
        target = entry + 5 + struct.unpack_from('<i', raw, offset+1)[0]
        self.assertEqual(target, 0x4fb1e0)
        filename = raw.index(b'game'+bytes([92])+b'src'+bytes([92])+b'hata'+bytes([92])+b'edtask.cpp')
        string_start = raw.rfind(bytes(1), 0, filename) + 1
        self.assertIn(struct.pack('<I', string_start + 0x400000), raw[target-0x400000:0xfb2d0])

    def test_original_ending_selector_on_zero_spending_ties_and_last_candidate(self):
        image = SOURCE.read_bytes()
        self.assertEqual(hashlib.sha256(image).hexdigest(), SOURCE_SHA256)
        # The complete selector loop runs between the prologue and the VM
        # variable write. Its locals are relative to EBP. No API calls occur.
        for spending, expected in [({}, 1), ({4: 7, 5: 7}, 4), ({11: 1, 12: 99}, 11),
                                   ({2: -1, 12: 100}, 1)]:
            vm = Uc(UC_ARCH_X86, UC_MODE_32)
            vm.mem_map(0x4d1000,0x1000)
            vm.mem_write(0x4d1000,image[0xd1000:0xd2000])
            vm.mem_map(0x7cf000,0x2000)
            vm.mem_map(0x1000000,0x1000)
            frame=0x1000100
            vm.reg_write(UC_X86_REG_EBP,frame)
            for i, amount in spending.items():
                vm.mem_write(0x7cf468+i*0x124,struct.pack('<i',amount))
            vm.emu_start(0x4d1583,0x4d15df,count=512)
            self.assertEqual(vm.reg_read(UC_X86_REG_EIP),0x4d15df)
            self.assertEqual(struct.unpack('<h',vm.mem_read(frame-0x10,2))[0],expected)


if __name__ == '__main__':
    unittest.main()
