"""Synthetic file/contract checks; no capture device, window or desktop access."""
import copy
import tempfile
import unittest
from pathlib import Path
from PIL import Image
from devtools import terminal_dxgi_frame_v2 as frame


class FrameTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=frame.ROOT/'.venv-audit')
        self.addCleanup(self.temp.cleanup);self.directory=Path(self.temp.name)
        palette=[(255,0,0),(0,255,0),(0,0,255),(255,255,0),(255,0,255),(0,255,255),(0,0,0),(255,255,255)]
        for seed in (1,2):
            im=Image.new('RGB',(256,192));im.putdata([palette[(x//32+3*(y//32)+seed)%8]
                for y in range(192) for x in range(256)])
            im.save(self.directory/('pattern-'+str(seed)+'.bmp'))
        self.report=dict(owned_window_destroyed=True,all_capture_scopes_released=True,
            frames=[dict(seed=i,mismatched_pixels=0,request_qpc=i*10,present_qpc=i*10+1,accumulated_frames=1) for i in (1,2)])

    def test_exact_pixels_and_temporal_order(self):
        self.assertEqual(len(frame.verify_patterns(self.directory,self.report)),2)

    def test_one_pixel_corruption_rejected_even_with_success_receipt(self):
        p=self.directory/'pattern-1.bmp'
        with Image.open(p) as im:changed=im.copy()
        changed.putpixel((0,0),(1,2,3));changed.save(p)
        with self.assertRaisesRegex(ValueError,'pixel comparison'):frame.verify_patterns(self.directory,self.report)

    def test_stale_frame_and_mouse_only_frame_refused(self):
        for field,value in (('present_qpc',10),('accumulated_frames',0),('mismatched_pixels',1)):
            r=copy.deepcopy(self.report);r['frames'][0][field]=value
            with self.assertRaises(ValueError):frame.verify_patterns(self.directory,r)

    def test_incomplete_cleanup_refused(self):
        r=copy.deepcopy(self.report);r['owned_window_destroyed']=False
        with self.assertRaises(ValueError):frame.verify_patterns(self.directory,r)

    def test_no_authorization_never_queries_desktop(self):
        with self.assertRaises(PermissionError):frame.qualify(None,desktop_until=0)

    def test_expired_authorization_never_opens_device(self):
        with self.assertRaises(ValueError):frame.qualify(None,desktop_until=0,explicit_monitor_capture=True)


if __name__=='__main__':unittest.main()
