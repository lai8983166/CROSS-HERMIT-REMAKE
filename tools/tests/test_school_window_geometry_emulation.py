import json
import unittest
from tools.school_window_geometry import ROOT,parent,window
from tools.school_window_geometry_emulation import generate
from tools.school_window_geometry_verification import verify_report


def report():return json.loads((ROOT/'analysis/school-window-geometry-trajectory-v1-20261020.json').read_text(encoding='utf8'))


class RectangleTests(unittest.TestCase):
    def test_original_prefix_setrect_and_complete_client_rectangle(self):
        self.assertEqual(verify_report(report(),'rect')['cases'],2)

    def test_refuses_coordinate_pointer_or_dirty_buffer_fabrication(self):
        for mutation in ('coords','pointer','before','result'):
            r=report();api=r['cases'][0]['rect']['platform_calls'][0]
            if mutation=='coords':api['args'][3]=800
            elif mutation=='pointer':api['mapped_output_pointer']+=4
            elif mutation=='before':api['request']['before_hex']='00'*16
            else:api['result']['hex']='00'*16
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):verify_report(r,'rect')

    def test_refuses_import_admission_frame_or_native_store_corruption(self):
        for mutation in ('map','cpu','write','frame','prefix'):
            r=report();n=r['cases'][0]['rect']
            if mutation=='map':n['import_admission']['foreign_after'][0]['sha256']='0'*64
            elif mutation=='cpu':n['import_admission']['after_cpu']['EIP']+=1
            elif mutation=='write':n['native_writes'].pop()
            elif mutation=='frame':n['entries'][0]['sp']+=4
            else:r['cases'][0]['branch']['cpu']['ESP']+=4
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):verify_report(r,'rect')


class AdjustmentTests(unittest.TestCase):
    def test_native_copy_and_real_adjustment_preserve_client_rectangle(self):
        r=report();verify_report(r,'adjust')
        for c in r['cases']:
            self.assertEqual(c['adjust']['state']['owner'],c['rect']['state']['owner'])
            self.assertEqual(c['adjust']['state']['client_rectangle']['sha256'],c['adjust']['state']['local_rectangle']['sha256'])

    def test_refuses_wrong_style_menu_copy_and_api_stack(self):
        for mutation in ('style','menu','copy','stack'):
            r=report();n=r['cases'][0]['adjust'];api=n['platform_calls'][0]
            if mutation=='style':api['args'][1]=0
            elif mutation=='menu':api['request']['menu']=1
            elif mutation=='copy':next(w for w in n['native_writes'] if w['pc']==0x4503A7)['value']=1
            else:api['sp']+=4
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):verify_report(r,'adjust')

    def test_refuses_local_guard_return_cpu_or_second_map_change(self):
        for mutation in ('guard','return','cpu','mapping'):
            r=report();n=r['cases'][0]['adjust']
            if mutation=='guard':n['state']['stack']['sha256']='0'*64
            elif mutation=='return':n['returns'][0]['return_va']='0x4503ce'
            elif mutation=='cpu':n['cpu']['ECX']=1024
            else:n['import_admission']={}
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):verify_report(r,'adjust')


class ClassTests(unittest.TestCase):
    def test_exact_seven_class_fields_and_unexecuted_import_instruction(self):
        r=report();result=verify_report(r)
        self.assertEqual((result['partial_class_initialized_dwords'],result['partial_class_uninitialized_dwords']),(7,5))
        for c in r['cases']:
            p=c['class']['pending'];self.assertEqual(p['stack_args'],[window.HINSTANCE,157])
            self.assertNotIn('return_va',p);self.assertFalse(p['call_instruction_executed'])
            self.assertEqual(c['class']['state']['owner'],c['adjust']['state']['owner'])

    def test_refuses_fabricated_class_callback_instance_or_icon_success(self):
        for mutation in ('class','callback','instance','pending','icon'):
            r=report();n=r['cases'][0]['class']
            if mutation=='class':n['state']['class_structure']['sha256']='0'*64
            elif mutation=='callback':next(w for w in n['native_writes'] if w['pc']==0x4503EA)['value']=0
            elif mutation=='instance':next(w for w in n['native_writes'] if w['pc']==0x4503F7)['value']=0x400000
            elif mutation=='pending':n['pending']['return_va']='0x45041c'
            else:n['LoadIconA_executed']=True
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):verify_report(r)

    def test_fresh_full_two_case_run_preserves_old_source_metadata(self):
        before=dict(parent.functions());ranges=dict(window.RANGES)
        r=generate();self.assertEqual(parent.functions(),before);self.assertEqual(window.RANGES,ranges)
        self.assertEqual(verify_report(r)['cases'],2)
        for c in r['cases']:
            self.assertEqual(c['rect']['before_cpu'],c['branch']['cpu'])
            self.assertEqual(c['adjust']['before_cpu'],c['rect']['cpu'])
            self.assertEqual(c['class']['before_cpu'],c['adjust']['cpu'])
            self.assertTrue(c['platform_cleanup']['all_owned_resources_released'])


if __name__=='__main__':unittest.main()
