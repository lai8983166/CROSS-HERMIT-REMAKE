import contextlib,re,unittest
from pathlib import Path
root=Path.cwd();text=(root/'analysis/school-retained-role9-regression-v1-20261023.log').read_text(encoding='utf8');mods=sorted(set(re.findall(r'\((tools\.tests\.[^. ]+)\.',text)));mods+=['tools.tests.test_school_retained_role9'];assert len(set(mods))==len(mods)==35
with open(root/'analysis/school-retained-opening-regression-v1-20261023.log','x',encoding='utf8',buffering=1) as log,contextlib.redirect_stdout(log),contextlib.redirect_stderr(log):
 result=unittest.TextTestRunner(stream=log,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromNames(mods));assert result.wasSuccessful() and result.testsRun==756
print('HISTORICAL_756_PASS',flush=True)
