"""Bounded actual-file corruption checks against the retained pending-IRQ case."""
import hashlib,json,shutil,tempfile,unittest
from pathlib import Path
from devtools.terminal_tcg_ram_event_verify import verify

ROOT=Path(__file__).resolve().parents[2]
WORK=ROOT/'.venv-audit/native-worker'


class EvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory(prefix='tcg-corruption-',dir=WORK)
        cls.copy=Path(cls.temp.name)/'case'
        shutil.copytree(WORK/'tcg-ram-event-v3-pending-irq',cls.copy)
        cls.sha=hashlib.sha256((cls.copy/'report.json').read_bytes()).hexdigest()
    @classmethod
    def tearDownClass(cls):cls.temp.cleanup()
    def corrupt(self,name,mutation):
        p=self.copy/name;original=p.read_bytes();p.write_bytes(mutation(original))
        try:
            with self.assertRaises(ValueError):verify(self.copy,self.sha)
        finally:p.write_bytes(original)
    def test_baseline(self):self.assertTrue(verify(self.copy,self.sha)['bounded_a_to_b_passed'])
    def test_report_cpu_bit(self):
        def change(raw):
            r=json.loads(raw);r['source_a']['states'][0]['eflags']='0000000000010002'
            return json.dumps(r).encode()
        self.corrupt('report.json',change)
    def test_event_vector(self):
        self.corrupt('source.trace',lambda b:b.replace(b'v=20 ',b'v=21 ',1))
    def test_checkpoint_payload(self):
        self.corrupt('checkpoint.bin',lambda b:b[:1024]+bytes([b[1024]^1])+b[1025:])
    def test_natural_output(self):
        self.corrupt('target.bin',lambda b:bytes([b[0]^1])+b[1:])

if __name__=='__main__':unittest.main()
