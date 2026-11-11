import copy
import json
from pathlib import Path
import tempfile
import unittest
from devtools import terminal_host_desktop as d


def healthy():
    return dict(monitors=[dict(device='DISPLAY1', screen=[0,0,3072,1728],
                              work=[0,0,3072,1688], mode={'width':3840,'height':2160})],
        taskbars=[dict(hwnd=1,pid=2,rect=[0,1688,3072,1728],visible=True,hung=False)],
        shell_window=3, game_window=0, auto_hide=False, appbar_state=0, metrics={'0':3072,'1':1728},
        input_desktop=dict(ready=True,input_desktop='Default',observer_desktop='Default',
                           foreground_hwnd=4,foreground_pid=5))


class DesktopTests(unittest.TestCase):
    def test_actual_failure_shape_rejected(self):
        s=healthy(); s['taskbars'][0]['rect']=[0,1727,3072,1728]
        self.assertIn('taskbar_collapsed_or_hidden', d.health(s))

    def test_intentional_auto_hide_not_changed(self):
        s=healthy(); s['auto_hide']=True; s['appbar_state']=1
        s['taskbars'][0]['rect']=[0,1727,3072,1728]
        self.assertEqual(d.health(s), [])
        changed=copy.deepcopy(s); changed['appbar_state']=0
        self.assertIn('appbar_state_changed',d.differences(s,changed))

    def test_resolution_workarea_focus_and_lock_detected(self):
        for mutate, expected in (
            (lambda s:s['monitors'][0]['mode'].update(width=1024), 'monitors_changed'),
            (lambda s:s['monitors'][0].update(work=[0,0,3072,1728]),'monitors_changed'),
            (lambda s:s['input_desktop'].update(foreground_hwnd=9),'foreground_hwnd_changed'),
            (lambda s:s['input_desktop'].update(ready=False),'input_desktop_unavailable'),
            (lambda s:s.update(game_window=9),'game_window_remaining')):
            a=healthy(); b=copy.deepcopy(a); mutate(b)
            self.assertIn(expected,d.differences(a,b))

    def exercise(self, states, action):
        directory=tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[2]/'.venv-audit')
        self.addCleanup(directory.cleanup)
        path=Path(directory.name)/'desktop.json'
        seq=iter(states)
        return path, lambda:d.guarded_run(action,path,read=lambda:next(seq),sleep=lambda _:None)

    def test_exception_path_still_writes_both_cleanup_checks(self):
        def fail(): raise ValueError('capture failed')
        path,run=self.exercise([healthy(),healthy(),healthy()],fail)
        with self.assertRaisesRegex(ValueError,'capture failed'):run()
        r=json.loads(path.read_text()); self.assertTrue(r['restored']); self.assertEqual(len(r['after']),2)

    def test_transient_restoration_cannot_pass(self):
        bad=healthy();bad['taskbars'][0]['rect']=[0,1727,3072,1728]
        path,run=self.exercise([healthy(),bad,healthy()],lambda:dict(success=True))
        with self.assertRaisesRegex(RuntimeError,'not verified'):run()
        self.assertFalse(json.loads(path.read_text())['restored'])

    def test_bad_baseline_never_launches_action(self):
        bad=healthy();bad['taskbars']=[]
        def forbidden():self.fail('must not launch')
        path,run=self.exercise([bad,bad,bad],forbidden)
        with self.assertRaisesRegex(RuntimeError,'baseline rejected'):run()

    def test_normal_cleanup_preserves_result(self):
        path,run=self.exercise([healthy(),healthy(),healthy()],lambda:42)
        self.assertEqual(run(),42);self.assertTrue(json.loads(path.read_text())['restored'])

    def test_failed_post_query_fails_closed(self):
        path,run=self.exercise([healthy()],lambda:42)
        with self.assertRaisesRegex(RuntimeError,'not verified'):run()
        self.assertIn('audit_error',json.loads(path.read_text()))

    def test_invalid_work_area_refused(self):
        s=healthy();s['monitors'][0]['work']=[0,0,5000,5000]
        self.assertIn('invalid_work_area',d.health(s))


if __name__=='__main__': unittest.main()
