"""Full independent parent/loop source replay, adversarial checks and actual lock owner."""
import contextlib,time,unittest
from pathlib import Path
if __name__=='__main__':
 root=Path.cwd();path=root/'analysis/school-retained-world-loop-single-v4-20261023.json.gz'
 for attempt in range(240):
  if path.exists():break
  time.sleep(5)
 else:raise RuntimeError('complete current source case did not become available')
 with open(root/'analysis/school-retained-world-loop-validation-v3-20261023.log','x',encoding='utf8',buffering=1) as log,contextlib.redirect_stdout(log),contextlib.redirect_stderr(log):
  names=['tools.tests.test_school_retained_world_loop','tools.tests.test_school_retained_world_loop_platform'];suite=unittest.defaultTestLoader.loadTestsFromNames(names);expected=suite.countTestCases();print('NEW_MODULES',names,'EXPECTED',expected,flush=True);result=unittest.TextTestRunner(stream=log,verbosity=2).run(suite);assert result.wasSuccessful() and result.testsRun==expected
 print('NEW_VALIDATION_PASS',expected,flush=True)
