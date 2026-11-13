"""Pure byte/receipt regressions: no helper, device, window or desktop API."""
import unittest
from devtools.terminal_texture_platform import logical_pixels,validate_receipt
from devtools.terminal_texture_native import self_check

class TextureTests(unittest.TestCase):
    def receipt(self):
        return dict(result=1,source_generation=4,verify_generation=5,lock_hresult=0,unlock_hresult=0,readonly_lock_acquired=1,readonly_unlock_attempted=1,readonly_unlock_succeeded=1,geometry_valid=1,copied=1,pending=0,readonly_flags=16,level=0,logical_row_bytes=512,rows=256,logical_bytes=131072,pitch=768,bits=0x300000,padding_bytes_per_row=256,state_restored=1,original_last_error=7,restored_last_error=7,last_error=7,ptd_before_hex='ab'*116,ptd_observed_hex='cd'*116,ptd_restored_hex='ab'*116,read_process_memory_result=1,read_rows=256,read_bytes=131072,read_error=0,read_failed_row=0xffffffff)
    def test_new_pitch_and_padding(self):
        rows=[bytes([y])*512 for y in range(256)]
        a=b''.join(r+b'A'*256 for r in rows);b=b''.join(r+b'B'*512 for r in rows)
        self.assertEqual(logical_pixels(a,768),logical_pixels(b,1024))
        broken=bytearray(b);broken[1024+10]^=1
        self.assertNotEqual(logical_pixels(a,768),logical_pixels(broken,1024))
    def test_geometry_rejections(self):
        for size,pitch in [(512*255,512),(511*256,511),(1025*256,1025)]:
            with self.assertRaises(ValueError):logical_pixels(bytes(size),pitch)
    def test_receipt_success(self):
        validate_receipt(self.receipt(),4,bytes.fromhex('ab'*116),7)
    def test_failure_rejections(self):
        cases=[('result',0),('source_generation',3),('verify_generation',4),('lock_hresult',0x80004005),('unlock_hresult',0x80004005),('readonly_unlock_attempted',0),('readonly_unlock_succeeded',0),('pending',1),('readonly_flags',0),('pitch',511),('padding_bytes_per_row',0),('restored_last_error',8),('ptd_restored_hex','cd'*116),('state_restored',0)]
        for key,value in cases:
            with self.subTest(key=key),self.assertRaises(ValueError):validate_receipt(dict(self.receipt(),**{key:value}),4,bytes.fromhex('ab'*116),7)
    def test_frozen_native_composition(self):
        report=self_check();self.assertFalse(report['native_executed']);self.assertEqual(report['operations'],{'TEX_VERIFY':3})
    def test_read_failure_with_successful_cleanup_is_not_acceptance(self):
        q=dict(self.receipt(),result=0,copied=0,pending=1,read_process_memory_result=0,read_rows=3,read_bytes=1536,read_error=299,read_failed_row=3)
        self.assertEqual(q['readonly_unlock_attempted'],1);self.assertEqual(q['readonly_unlock_succeeded'],1)
        with self.assertRaises(ValueError):validate_receipt(q,4,bytes.fromhex('ab'*116),7)
        # Static control-flow check: failed reads break the row loop, then reach
        # the same explicit Unlock call. This is not a native fault injection.
        from devtools.terminal_texture_native import INCLUDE
        s=INCLUDE.read_text();tail=s.split('if(!readOK||actualBytes!=512)',1)[1].split('unlocked=static_cast<LONG>(unlockHR)>=0;',1)[0]
        self.assertIn('break;',tail);self.assertIn('gameMethod(a[0],17)',tail);self.assertNotIn('return ',tail)

if __name__=='__main__':unittest.main()
