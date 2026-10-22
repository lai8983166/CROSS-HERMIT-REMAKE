"""Full source corpus and changed byte/alpha/layout/platform claims."""
import copy,gzip,json,unittest
from tools import school_retained_portrait_file_catalog as work


class CatalogTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.report=json.loads(gzip.decompress((work.ROOT/'analysis/school-retained-portrait-file-catalog-v1-20261022.json.gz').read_bytes()))
 def reject(self,edit):
  r=copy.deepcopy(self.report);edit(r)
  with self.assertRaises((ValueError,KeyError)):work.verify(r)
 def test_all_21_complete_source_pixels(self):self.assertEqual(work.verify(self.report)['complete_pixels'],2752512)
 def test_missing_image(self):self.reject(lambda r:r['images'].pop())
 def test_duplicate_role(self):self.reject(lambda r:r['images'][1].update(role=1))
 def test_changed_private_path(self):self.reject(lambda r:r['images'][0].update(private_path=r['images'][1]['private_path']))
 def test_changed_image_identity(self):self.reject(lambda r:r['images'][0].update(source_sha256='0'*64))
 def test_changed_alpha_count(self):self.reject(lambda r:r['images'][0]['container'].update(opaque_pixels=0))
 def test_changed_last_row(self):self.reject(lambda r:r['images'][0]['container']['row_sha256'].__setitem__(511,'0'*64))
 def test_changed_bounds(self):self.reject(lambda r:r['images'][0]['container'].update(opaque_bbox=[0,0,256,512]))
 def test_changed_historical_platform_pin(self):self.reject(lambda r:r['platform_contract'].update(native_texture_report_sha256='0'*64))
 def test_false_reachability(self):self.reject(lambda r:r.update(script_reachability_verified=True))
 def test_truncated_file(self):
  with self.assertRaisesRegex(ValueError,'byte extent'):work.parse(bytes(262167))


if __name__=='__main__':unittest.main()
