"""Whole-corpus source walk, short command variants and dependency tamper refusal."""
import copy,json,struct,unittest
from tools import school_retained_portrait_catalog as catalog
from tools.school_retained_portrait_verification import verify_catalog


class CatalogTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.report=json.loads((catalog.ROOT/'analysis/school-retained-portrait-catalog-v3-20261022.json').read_bytes())
 def test_whole_corpus_independent_walk(self):
  p=verify_catalog(self.report);self.assertTrue(p['independent_byte_walk_verified']);s=p['summary'];self.assertEqual((s['script_files'],s['VM_segments'],s['commands'],s['opcode_classes']),(45,334,22377,57));self.assertEqual((s['portrait_commands'],s['portrait_roles'],s['short_portrait_commands']),(326,21,6));self.assertFalse(p['R6_complete'])
 def test_short_commands_keep_missing_operands_unresolved(self):
  rows=[r for r in self.report['portraits'] if r['missing_declared_operands']];self.assertEqual(len(rows),6)
  self.assertEqual({r['script'] for r in rows},{'T0080.BIN','T0090.BIN'})
  for r in rows:self.assertEqual((r['declared_bytes'],len(r['expressions']),r['missing_declared_operands']),(12,2,2));self.assertEqual(len(bytes.fromhex(r['source_handler_read_window_hex'])),20)
 def reject(self,edit):
  r=copy.deepcopy(self.report);edit(r)
  with self.assertRaises((ValueError,KeyError)):verify_catalog(r)
 def test_missing_script(self):self.reject(lambda r:r['scripts'].pop())
 def test_missing_command(self):self.reject(lambda r:r['scripts'][0]['commands'].pop())
 def test_wrong_command_size(self):self.reject(lambda r:r['scripts'][0]['commands'][0].update(bytes=r['scripts'][0]['commands'][0]['bytes']+2))
 def test_false_source_hash(self):self.reject(lambda r:r['scripts'][0].update(sha256='0'*64))
 def test_false_opcode_dispatch(self):self.reject(lambda r:r['dispatch'][0].update(entry=1))
 def test_false_resource_identity(self):self.reject(lambda r:next(iter(r['roles'].values())).update(image_sha256='0'*64))
 def test_false_name(self):self.reject(lambda r:next(iter(r['roles'].values())).update(name_big5='wrong'))
 def test_hidden_short_variant(self):self.reject(lambda r:r['summary'].update(short_portrait_commands=0))
 def test_fabricated_missing_operand(self):
  self.reject(lambda r:next(x for x in r['portraits'] if x['missing_declared_operands'])['expressions'].append(dict(raw=0x20000000,type=2,payload=0,literal=0)))
 def test_incomplete_header_refused(self):
  for b in (b'',bytes(8),struct.pack('<II',9,100)):
   with self.assertRaises(ValueError):catalog.commands(b)
 def test_four_parameter_assumption_refused(self):
  with self.assertRaises(ValueError):catalog.dependency(b'',struct.pack('<HHI',30,8,0x20000008))


if __name__=='__main__':unittest.main()
