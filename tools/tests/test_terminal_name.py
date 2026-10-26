"""Refuse forged terminal name pixels, platform contracts, stacks and progress."""
import copy,gzip,json,struct,unittest
from types import SimpleNamespace
from tools import terminal_name_emulation as e
from tools import terminal_name_verification as v
REPORT='analysis/terminal-name-source-v5-20261026.json.gz'

class TerminalNameTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.report=json.loads(gzip.decompress((e.ROOT/REPORT).read_bytes()));cls.rows=cls.report['cases']
 def reject(self,edit,check=v.verify_case):
  r=copy.deepcopy(self.rows[0]);edit(r)
  with self.assertRaises((ValueError,KeyError,IndexError,StopIteration)):check(r)
 def test_both_complete_contracts(self):
  self.assertEqual(self.report['source_contract'],e.source_contract())
  for row in self.rows:
   with self.subTest(name=row['input']['name']):self.assertEqual(v.verify_case(row)['VM_PC'],76)
 def test_distinct_source_roles(self):
  self.assertEqual([v.independent_pixels(r)[0] for r in self.rows],[2,1])
 def test_source_guard_algorithm_preserved(self):self.assertIs(e.NameMachine.source_code.__code__,e.parent.FadeMachine.source_code.__code__)
 def test_runtime_host_setup_guard(self):
  row=self.rows[0];g=e.NameMachine(e.parent.parent.parent.corpus()[0],SimpleNamespace(hello=row['current_CRT_hello']),SimpleNamespace(hello=row['current_GPU_hello'],device=row['current_GPU_hello']['device']))
  try:
   for p in (e.VM+28,e.VM+0x20,e.NODE,e.MAIN+0xB208):
    with self.assertRaises(ValueError):g.put(p,0)
   g.put(e.STACK+0xF000,e.RETURN)
   for p in (0x401000,0x5920A0):
    with self.assertRaises(ValueError):g.write_hook(g.uc,0,p,4,0,None)
  finally:g.name_platform.close()
 def test_wrong_source_name(self):self.reject(lambda r:r['terminal_name']['calls'][4].update(text_hex='41'))
 def test_wrong_font_height(self):self.reject(lambda r:r['terminal_name']['calls'][0]['args'].__setitem__(0,21))
 def test_wrong_original_font_IAT(self):self.reject(lambda r:r['terminal_name']['calls'][0].update(target=0x12345678))
 def test_fabricated_API_receipt(self):self.reject(lambda r:r['terminal_name']['calls'][0].update(actual_API_executed=False),v.native)
 def test_cross_owner_GDI_handle(self):self.reject(lambda r:r['terminal_name']['GDI_trace'][2]['native_args'].__setitem__(0,123),v.native)
 def test_missing_GDI_receipt(self):self.reject(lambda r:r['terminal_name']['GDI_trace'].pop(),v.native)
 def test_wrong_raw_GPU_sequence(self):self.reject(lambda r:r['GPU_trace'][5]['reply'].update(id=99),v.native)
 def test_false_GPU_readback(self):self.reject(lambda r:r['terminal_name']['readback'].update(hex='00'),v.native)
 def test_missing_texture_release(self):self.reject(lambda r:r['name_cleanup']['GPU_APIs'].pop(),v.native)
 def test_supplemental_helper_texture_release(self):self.reject(lambda r:r['GPU_cleanup'].update(texture_releases=[1]),v.native)
 def test_leaked_measurement_DC(self):self.reject(lambda r:r['name_cleanup']['GDI'].update(dcs=0),v.native)
 def test_wrong_portrait_path(self):self.reject(lambda r:r['terminal_name'].update(path='data\\adv\\bin\\sc004.bin'),v.independent_pixels)
 def test_wrong_measured_extent(self):self.reject(lambda r:r['terminal_name']['raster']['measured'].__setitem__(0,43),v.independent_pixels)
 def test_wrong_selected_face(self):self.reject(lambda r:r['terminal_name']['raster'].update(selected_face='Arial'),v.independent_pixels)
 def test_wrong_ANSI_codepage(self):self.reject(lambda r:r['terminal_name']['raster'].update(ACP=950),v.independent_pixels)
 def test_wrong_shadow_pixels(self):self.reject(lambda r:r['terminal_name']['raster']['stages'][1].update(hex='00'),v.independent_pixels)
 def test_wrong_complete_raster(self):self.reject(lambda r:r['terminal_name']['raster'].update(raster_hex='00'),v.independent_pixels)
 def test_wrong_conversion_rectangle(self):self.reject(lambda r:r['terminal_name']['conversions'][0]['rect'].__setitem__(2,1),v.independent_pixels)
 def test_wrong_converted_pixels(self):self.reject(lambda r:r['terminal_name'].update(upload_hex='00'),v.independent_pixels)
 def test_unrelated_GYBC_changed(self):self.reject(lambda r:r['terminal_name']['GYBC_readback'].update(hex='00'),v.independent_pixels)
 def test_missing_natural_GDI_cleanup(self):self.reject(lambda r:r['terminal_name']['calls'].pop(),v.independent_pixels)
 def test_false_handler_return(self):self.reject(lambda r:r['terminal_name']['pending'].update(first_instruction_executed=True))
 def test_PC_host_advanced(self):
  def edit(r):
   b=bytearray.fromhex(r['terminal_name']['state']['VM']);struct.pack_into('<I',b,28,96);r['terminal_name']['state']['VM']=b.hex()
  self.reject(edit)
 def test_stack_ancestor_changed(self):self.reject(lambda r:r['terminal_name']['pending'].update(stack='00'))
 def test_whole_CPU_changed(self):self.reject(lambda r:r['terminal_name']['CPU'].update(EAX=0))
 def test_original_PC_digest_changed(self):self.reject(lambda r:r['terminal_name']['local_trace'].update(code_sha256='0'*64))
 def test_original_write_digest_changed(self):self.reject(lambda r:r['terminal_name']['local_trace'].update(write_sha256='0'*64))
 def test_missing_original_leaf(self):self.reject(lambda r:r['terminal_name']['leaves'].pop())
 def test_wrong_COM_output(self):self.reject(lambda r:r['terminal_name']['GPU_APIs'][0]['memory_outputs'][0].update(hex='00000000'))

if __name__=='__main__':unittest.main()
