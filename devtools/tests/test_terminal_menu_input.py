import unittest
from devtools.terminal_menu_input import guarded_click,owned_main_menu_click,TARGETS,absolute_coordinates


class Api:
    def __init__(self):self.xy=(0,0);self.flags=[];self.stuck=False;self.held=False;self.up_fail=False;self.final_fail=False
    def position(self):return self.xy
    def left_button_down(self):return self.held
    def submit(self,value):
        p=value.data.mi;self.flags.append(p.dwFlags)
        if p.dwFlags==1 and not self.stuck:self.xy=(self.xy[0]+p.dx,self.xy[1]+p.dy)
        if p.dwFlags==4 and self.up_fail:self.up_fail=False;return 0
        return 1
    def final_guard(self):
        if self.final_fail:raise ValueError('focus changed')


class MouseSafetyTests(unittest.TestCase):
    def test_absolute_endpoints_and_negative_monitor_origin(self):
        self.assertEqual(absolute_coordinates((-1920,0),(-1920,0,3840,1080)),(0,0))
        self.assertEqual(absolute_coordinates((1919,1079),(-1920,0,3840,1080)),(65535,65535))
        for point,desktop in (((-1,0),(0,0,1024,768)),((0,0),(0,0,0,768))):
            with self.assertRaises(ValueError):absolute_coordinates(point,desktop)
    def test_absolute_movement_avoids_relative_acceleration(self):
        api=Api();old=api.submit
        api.geometry=lambda target:dict(screen_target=list(target),virtual_desktop=[0,0,1024,768])
        def submit(value):
            p=value.data.mi
            if p.dwFlags==0xC001:
                api.flags.append(p.dwFlags);api.xy=(round(p.dx*1023/65535),round(p.dy*767/65535));return 1
            if p.dwFlags==1:
                api.xy=(api.xy[0]+4*p.dx,api.xy[1]+4*p.dy);return 1
            return old(value)
        api.submit=submit;r=guarded_click(api,lambda:None,TARGETS[0],lambda _:None,absolute=True)
        self.assertIsNone(r['error']);self.assertEqual(api.flags,[0xC001,2,4]);self.assertTrue(r['released'])
    def test_already_at_absolute_target_still_checks_occlusion(self):
        api=Api();api.xy=TARGETS[0]
        def covered(_):raise ValueError('target covered')
        api.geometry=covered;r=guarded_click(api,lambda:None,TARGETS[0],lambda _:None,absolute=True)
        self.assertEqual(api.flags,[]);self.assertFalse(r['down_submitted']);self.assertIsNotNone(r['error'])
    def test_disabled_without_separate_user_override(self):
        with self.assertRaises(PermissionError):owned_main_menu_click(None,None,0)
    def test_unreviewed_menu_target_refused_without_input(self):
        api=Api()
        with self.assertRaises(ValueError):guarded_click(api,lambda:None,(1,2),lambda _:None)
        self.assertEqual(api.flags,[])
    def test_actual_cursor_feedback_before_click(self):
        api=Api();r=guarded_click(api,lambda:None,TARGETS[0],lambda _:None)
        self.assertEqual(r['before_click'],list(TARGETS[0]));self.assertIsNone(r['error'])
        self.assertEqual(api.flags[-2:],[2,4]);self.assertTrue(r['released']);self.assertFalse(r['transition_proved'])
    def test_undelivered_movement_never_clicks(self):
        api=Api();api.stuck=True;r=guarded_click(api,lambda:None,TARGETS[0],lambda _:None)
        self.assertEqual(api.flags,[1]*4);self.assertFalse(r['down_submitted']);self.assertIsNotNone(r['error'])
    def test_user_held_button_refused(self):
        api=Api();api.held=True;r=guarded_click(api,lambda:None,TARGETS[0],lambda _:None)
        self.assertEqual(api.flags,[]);self.assertIsNotNone(r['error'])
    def test_foreground_failure_prevents_input(self):
        api=Api()
        def fail():raise ValueError('foreign window')
        r=guarded_click(api,fail,TARGETS[0],lambda _:None)
        self.assertEqual(api.flags,[]);self.assertIsNotNone(r['error'])
    def test_release_retried_once_on_failure(self):
        api=Api();api.up_fail=True;r=guarded_click(api,lambda:None,TARGETS[0],lambda _:None)
        self.assertEqual(api.flags[-3:],[2,4,4]);self.assertTrue(r['released']);self.assertIsNotNone(r['error'])
    def test_error_during_hold_still_releases(self):
        api=Api();api.xy=TARGETS[0]
        def fail(_):raise ValueError('interrupted')
        r=guarded_click(api,lambda:None,TARGETS[0],fail)
        self.assertEqual(api.flags,[2,4]);self.assertTrue(r['released']);self.assertIsNotNone(r['error'])
    def test_focus_change_after_click_is_not_success(self):
        api=Api();api.final_fail=True;r=guarded_click(api,lambda:None,TARGETS[0],lambda _:None)
        self.assertTrue(r['released']);self.assertIsNotNone(r['error'])
    def test_release_exception_retained_and_retried(self):
        api=Api();api.xy=TARGETS[0];old=api.submit;count=[0]
        def submit(value):
            if value.data.mi.dwFlags==4:
                count[0]+=1
                if count[0]==1:raise OSError('injection error')
            return old(value)
        api.submit=submit;r=guarded_click(api,lambda:None,TARGETS[0],lambda _:None)
        self.assertTrue(r['released']);self.assertIsNotNone(r['error']);self.assertEqual(count[0],2)
    def test_final_release_exception_does_not_destroy_receipt(self):
        api=Api();api.xy=TARGETS[0];old=api.submit
        def submit(value):
            if value.data.mi.dwFlags==4:raise OSError('injection error')
            return old(value)
        api.submit=submit;r=guarded_click(api,lambda:None,TARGETS[0],lambda _:None)
        self.assertFalse(r['released']);self.assertIsNotNone(r['error']);self.assertIn('release_error',r)


if __name__=='__main__':unittest.main()
