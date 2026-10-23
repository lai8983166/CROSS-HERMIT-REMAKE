import contextlib,unittest
from pathlib import Path
if __name__=='__main__':
 names=['tools.tests.test_school_scheduler_lifetime','tools.tests.test_school_scheduler_verification','tools.tests.test_school_scene_bootstrap','tools.tests.test_school_scene_resources_emulation','tools.tests.test_school_world_mode_emulation','tools.tests.test_school_world_mode']
 with open(Path.cwd()/'analysis/school-retained-scheduler-regression-v1-20261024.log','x',encoding='utf8',buffering=1) as log,contextlib.redirect_stdout(log),contextlib.redirect_stderr(log):
  suite=unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromName(n) for n in names);expected=suite.countTestCases();print('EXPECTED_HISTORICAL_TESTS',expected,flush=True);r=unittest.TextTestRunner(stream=log,verbosity=2).run(suite);assert r.wasSuccessful() and r.testsRun==expected
 print('REGRESSION_PASS',expected,flush=True)
