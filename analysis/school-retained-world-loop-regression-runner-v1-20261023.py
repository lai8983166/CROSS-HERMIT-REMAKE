"""Affected immutable opening/task/scene/world contracts; no native UI interaction."""
import contextlib,unittest
from pathlib import Path
MODULES=['tools.tests.test_school_retained_opening','tools.tests.test_school_task_frame','tools.tests.test_school_scene_bootstrap','tools.tests.test_school_native_scene_calls','tools.tests.test_school_world_mode','tools.tests.test_school_world_mode_emulation','tools.tests.test_school_world_admission','tools.tests.test_battle_parallel_exit_evidence']
root=Path.cwd()
with open(root/'analysis/school-retained-world-loop-regression-v1-20261023.log','x',encoding='utf8',buffering=1) as log,contextlib.redirect_stdout(log),contextlib.redirect_stderr(log):
 suite=unittest.defaultTestLoader.loadTestsFromNames(MODULES);expected=suite.countTestCases();print('AFFECTED_HISTORICAL_MODULES',MODULES,'EXPECTED',expected,flush=True);result=unittest.TextTestRunner(stream=log,verbosity=2).run(suite);assert result.wasSuccessful() and result.testsRun==expected
print('AFFECTED_HISTORICAL_PASS',expected,flush=True)
