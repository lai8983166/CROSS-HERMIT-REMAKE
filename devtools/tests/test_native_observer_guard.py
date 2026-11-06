import unittest
from devtools.native_observer_guard import other_processes


class GuardTests(unittest.TestCase):
    def test_only_exact_own_venv_chain_excluded(self):
        own = dict(ProcessId=2,ParentProcessId=1,CommandLine='"real python" -B -m devtools.terminal_scene_owner')
        parent = dict(ProcessId=1,ExecutablePath='venv.exe',CommandLine='venv.exe -B -m devtools.terminal_scene_owner')
        foreign = dict(ProcessId=3,ParentProcessId=1,CommandLine=own['CommandLine'])
        self.assertEqual(other_processes([parent,own,foreign],2,1,'venv.exe'),[foreign])
        for key,value in (('ExecutablePath','other.exe'),('CommandLine','venv.exe -m tools.battle_other')):
            changed = dict(parent,**{key:value})
            self.assertEqual(other_processes([changed,own,foreign],2,1,'venv.exe'),[changed,foreign])

    def test_missing_current_never_excludes_parent(self):
        parent = dict(ProcessId=1,ExecutablePath='venv.exe',CommandLine='venv.exe -m tools.battle_other')
        self.assertEqual(other_processes([parent],2,1,'venv.exe'),[parent])


if __name__ == '__main__':
    unittest.main()
