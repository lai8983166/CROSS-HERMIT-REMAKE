import copy
import struct
import unittest
from devtools import terminal_ptd_evidence_inventory as v


class PTDEvidenceInventoryTests(unittest.TestCase):
    def tls(self):
        raw = bytearray(116); struct.pack_into('<I', raw, 0, 51)
        struct.pack_into('<I', raw, 0x50, v.STATIC_LOCALE)
        return dict(PTD=0x20000, PTD_hex=raw.hex(), TLS_slot_hex=struct.pack('<I',0x20000).hex(),
                    owner_pid=42, thread_id=51, TEB=0x30000, TLS_index=20, slot=0x30e60)

    def test_zero_nested_and_static_locale_do_not_prove_free(self):
        result = v.ptd_fields(self.tls())
        self.assertEqual(result['dynamic_nested_pointers'], [])
        self.assertFalse(result['observed_release'])

    def test_nonzero_nested_and_nonstatic_locale_are_retained(self):
        tls = self.tls(); raw = bytearray.fromhex(tls['PTD_hex'])
        struct.pack_into('<I',raw,0x24,0x40000); struct.pack_into('<I',raw,0x50,0x50000)
        tls['PTD_hex']=raw.hex()
        self.assertEqual(v.ptd_fields(tls)['dynamic_nested_pointers'],[0x40000,0x50000])

    def test_bad_owner_slot_and_partial_bytes_reject(self):
        for field,value in (('thread_id',52),('TLS_slot_hex','00000000'),('PTD_hex','00'*115)):
            tls=self.tls();tls[field]=value
            with self.assertRaises(ValueError):v.ptd_fields(tls)

    def test_address_reuse_does_not_prove_previous_release(self):
        first=self.tls();second=copy.deepcopy(first);second['thread_id']=52
        raw=bytearray.fromhex(second['PTD_hex']);struct.pack_into('<I',raw,0,52);second['PTD_hex']=raw.hex()
        a,b=v.ptd_fields(first),v.ptd_fields(second)
        self.assertEqual(a['pointer'],b['pointer']);self.assertNotEqual(a['PTD_sha256'],b['PTD_sha256'])
        self.assertFalse(a['observed_release'] or b['observed_release'])

    def test_allocator_gates_do_not_assume_HeapFree(self):
        cases=[((0,123,1,None),'hook'),((2,0,1,None),'retained'),
               ((0,0,3,None),'membership'),((0,0,3,True),'small_block_free'),
               ((0,0,2,True),'small_block_free'),((0,0,2,False),'HeapFree_candidate'),
               ((0,0,1,None),'HeapFree_candidate')]
        for args,term in cases:
            result=v.allocator_branch(*args);self.assertIn(term,result['potential_branch'])
            self.assertFalse(result['actual_branch_observed'] or result['PTDcleanup'])


if __name__=='__main__':unittest.main()
