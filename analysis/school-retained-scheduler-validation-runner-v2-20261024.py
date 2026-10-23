import contextlib,os,unittest
from pathlib import Path
if __name__=='__main__':
 os.environ['SCHOOL_RETAINED_SCHEDULER_PROOF_OUT']='analysis/school-retained-scheduler-single-proof-v1-20261024.json'
 with open(Path.cwd()/'analysis/school-retained-scheduler-validation-v2-20261024.log','x',encoding='utf8',buffering=1) as log,contextlib.redirect_stdout(log),contextlib.redirect_stderr(log):
  suite=unittest.defaultTestLoader.loadTestsFromName('tools.tests.test_school_retained_scheduler');expected=suite.countTestCases();print('EXPECTED_TESTS',expected,flush=True);r=unittest.TextTestRunner(stream=log,verbosity=2).run(suite);assert r.wasSuccessful() and r.testsRun==expected
 print('NEW_VALIDATION_PASS',expected,flush=True)
