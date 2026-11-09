import unittest
from devtools import terminal_exit_cleanup_contract as c


class CleanupContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.raw=c.SOURCE.read_bytes()

    def test_original_identity_and_actual_destructor(self):
        result=c.source_contract(self.raw)
        self.assertEqual(result['normal_owner_close_sites'],[0x421B4C])
        self.assertGreaterEqual(len(result['checked_instructions']),50)
        bad=bytearray(self.raw);bad[0x57554F-c.BASE]^=1
        with self.assertRaises(ValueError):c.source_contract(bytes(bad))

    def test_PTD_nested_frees_select_original_order_and_type(self):
        nested={offset:0x21000000+i*0x100 for i,offset in enumerate(c.PTD_NESTED)}
        result=c.ptd_probe(self.raw,nested,locale=0x22000000)
        frees=[row for row in result['calls']if row['kind']=='declared_free_boundary']
        self.assertEqual([x['pointer']for x in frees],[*nested.values(),0x22000000,result['PTD']])
        self.assertTrue(all(x['block_type']==2 for x in frees))
        self.assertEqual([x['site']for x in frees],list(c.FREE_SITES))
        self.assertEqual(result['calls'][-1],dict(site=0x57554F,kind='declared_TLS_clear',index=2,value=0,result=1))
        self.assertFalse(result['actual_heap_release_proved'])

    def test_null_nested_and_static_locale_are_not_freed(self):
        result=c.ptd_probe(self.raw)
        self.assertEqual([x['pointer']for x in result['calls']if x['kind']=='declared_free_boundary'],[result['PTD']])
        result=c.ptd_probe(self.raw,locale=0)
        self.assertEqual([x['pointer']for x in result['calls']if x['kind']=='declared_free_boundary'],[0,result['PTD']])

    def test_null_argument_uses_current_TLS_and_null_lookup_only_clears(self):
        result=c.ptd_probe(self.raw,argument_is_null=True)
        self.assertEqual(result['calls'][0]['kind'],'declared_TLS_lookup')
        self.assertEqual(result['calls'][0]['result'],result['PTD'])
        result=c.ptd_probe(self.raw,argument_is_null=True,lookup_is_null=True)
        self.assertEqual([x['kind']for x in result['calls']],['declared_TLS_lookup','declared_TLS_clear'])

    def test_invalid_TLS_index_skips_all_cleanup_and_clear_failure_is_ignored(self):
        self.assertEqual(c.ptd_probe(self.raw,tls_index=0xFFFFFFFF)['calls'],[])
        failed=c.ptd_probe(self.raw,tls_success=False)
        self.assertEqual(failed['calls'][-1]['result'],0)
        self.assertTrue(failed['return_reached'])
        self.assertFalse(failed['TLS_result_checked_by_original'])

    def test_original_unlink_head_middle_tail_and_last_bucket(self):
        for position in range(3):
            for bucket in (0,31):
                with self.subTest(position=position,bucket=bucket):
                    result=c.unlink_probe(self.raw,position,bucket)
                    self.assertTrue(result['ABI_preserved']and result['removed_next_preserved'])
                    self.assertFalse(result['leaf_substitutions'])
                    self.assertLess(result['instructions'],4000)

    def test_bounded_inputs_and_no_native_claim(self):
        with self.assertRaises(ValueError):c.unlink_probe(self.raw,3)
        with self.assertRaises(ValueError):c.unlink_probe(self.raw,0,32)
        with self.assertRaises(ValueError):c.ptd_probe(self.raw,{0x20:1})
        result=c.build(self.raw)
        self.assertFalse(result['accepted']or result['native_execution']or result['full_cleanup_proved']or result['formal_terminal_boundary_advanced'])
        plan=result['observation_plan']
        self.assertFalse(plan['supplemental_thread_owner']['normal_original_close'])
        self.assertFalse(plan['PTD']['TLS_clear_result_checked_by_original'])


if __name__=='__main__':unittest.main()
