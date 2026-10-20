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


if __name__=='__main__':unittest.main()
