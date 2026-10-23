"""Affected original world/source-resource and current x86 platform contracts."""
import contextlib,unittest
from pathlib import Path
from unittest.mock import patch
from tools import school_retained_fog as work
from tools.tests.test_school_retained_world_loop import WorldLoopTests
MODULES=['tools.tests.test_school_retained_world_loop','tools.tests.test_school_retained_world_loop_platform','tools.tests.test_school_scene_resources_emulation','tools.tests.test_school_scene_resource_catalog','tools.tests.test_school_world_mode_emulation','tools.tests.test_school_world_admission','tools.tests.test_school_d3d8_image_bridge']
if __name__=='__main__':
 root=Path.cwd()
 with open(root/'analysis/school-retained-fog-regression-v1-20261023.log','x',encoding='utf8',buffering=1) as log,contextlib.redirect_stdout(log),contextlib.redirect_stderr(log):
  setup=work.previous.previous.adapt(WorldLoopTests.setUpClass.__func__,[("analysis/school-retained-world-loop-single-proof-v1-20261023.json","analysis/school-retained-fog-parent-regression-proof-v1-20261023.json")])
  WorldLoopTests.setUpClass=classmethod(setup)
  suite=unittest.defaultTestLoader.loadTestsFromNames(MODULES);expected=suite.countTestCases();print('AFFECTED_MODULES',MODULES,'EXPECTED',expected,flush=True);result=unittest.TextTestRunner(stream=log,verbosity=2).run(suite);assert result.wasSuccessful() and result.testsRun==expected
 print('AFFECTED_HISTORICAL_PASS',expected,flush=True)
