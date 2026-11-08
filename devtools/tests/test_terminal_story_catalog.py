import struct
import unittest
from devtools.terminal_story_catalog import Catalog,code_block,tactics_blocks


class CatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.catalog=Catalog()
    def test_observed_opening_span_disambiguated_by_actual_code_hash(self):
        rows=[r for v in self.catalog.entries.values()for r in v if r['path'].endswith('CHAPTER003.YBC')]
        self.assertEqual(len(rows),1);r=rows[0]
        from pathlib import Path
        raw=Path(r['path']).read_bytes()[r['code_offset']:r['code_offset']+r['code_bytes']]
        vm=bytearray(128);struct.pack_into('<II',vm,16,0x20000,0x20000+len(raw))
        observed=self.catalog.observe(lambda p,n:raw,vm);self.assertTrue(observed['matched'])
        damaged=bytearray(raw);damaged[0]^=1
        self.assertFalse(self.catalog.observe(lambda p,n:bytes(damaged),vm)['matched'])
    def test_tactics_one_subprogram_catalogued(self):
        rows=[r for v in self.catalog.entries.values()for r in v if r['path'].endswith('T0001.BIN')]
        self.assertTrue(any(r['block']==0 and r['record']==1 and r['code_bytes']==2050 for r in rows))
    def test_unbounded_or_malformed_containers_refused(self):
        for b in (b'',bytes(30),struct.pack('<3I',2,20,10)):
            with self.assertRaises((ValueError,struct.error)):code_block(b)
        with self.assertRaises(ValueError):list(tactics_blocks(struct.pack('<II',8,100000)))
    def test_unbounded_live_pointer_never_read(self):
        vm=bytearray(128)
        def fail(*a):raise AssertionError('must not read unbounded pointer')
        self.assertFalse(self.catalog.observe(fail,vm)['matched'])


if __name__=='__main__':unittest.main()
