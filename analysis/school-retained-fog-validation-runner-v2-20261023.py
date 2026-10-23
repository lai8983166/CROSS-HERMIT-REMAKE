"""Full original parent/fog/loop replay and current surface/ownership tampering."""
import contextlib,unittest
from pathlib import Path
if __name__=='__main__':
 root=Path.cwd()
 with open(root/'analysis/school-retained-fog-validation-v2-20261023.log','x',encoding='utf8',buffering=1) as log,contextlib.redirect_stdout(log),contextlib.redirect_stderr(log):
  suite=unittest.defaultTestLoader.loadTestsFromName('tools.tests.test_school_retained_fog');expected=suite.countTestCases();print('NEW_TESTS_EXPECTED',expected,flush=True);result=unittest.TextTestRunner(stream=log,verbosity=2).run(suite);assert result.wasSuccessful() and result.testsRun==expected
 print('NEW_VALIDATION_PASS',expected,flush=True)
