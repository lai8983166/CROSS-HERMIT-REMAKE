"""Overlap independent test fixture replay with formal proof production."""
import json,time,unittest
from tools.tests.test_school_retained_opening import OpeningTests,v
original=OpeningTests.test_bound_six_proofs_and_source_execution
def bound_when_formal_proof_is_complete(self):
 path=v.ROOT/'analysis/school-retained-opening-proof-v1-20261023.json';log=v.ROOT/'analysis/school-retained-opening-proof-run-v1-20261023.log';deadline=time.monotonic()+1800;announced=False
 while True:
  try:
   p=json.loads(path.read_bytes())
   if p.get('six_original_complete_openings_verified') and len(p.get('cases',[]))==6:break
  except (FileNotFoundError,json.JSONDecodeError):pass
  if log.exists() and 'Traceback' in log.read_text(encoding='utf8'):raise RuntimeError('formal independent proof failed; no proof binding accepted')
  if time.monotonic()>=deadline:raise RuntimeError('formal independent proof was not completed within the bounded wait')
  if not announced:print('awaiting final six-case proof metadata; test fixture replay already independent',flush=True);announced=True
  time.sleep(5)
 return original(self)
OpeningTests.test_bound_six_proofs_and_source_execution=bound_when_formal_proof_is_complete
result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(OpeningTests))
raise SystemExit(0 if result.wasSuccessful() else 1)
