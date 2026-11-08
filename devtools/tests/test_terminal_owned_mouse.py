import unittest
from devtools import terminal_owned_mouse as mouse
from devtools.tests.test_terminal_menu_input import Api

def inert_cursor(api):
    ticks=[0]
    def snapshot(target):
        ticks[0]+=20_000_000
        return dict(screen_point=list(api.position()),os_game_point=list(api.position()),
                    game_point=list(api.position()),geometry=api.geometry(target),
                    wall_time_ns=ticks[0],monotonic_ns=ticks[0])
    api.cursor_snapshot=snapshot
    return api


class DesktopApi(Api):
    def __init__(self):
        super().__init__();self.geometry_calls=0;self.freeze=False;self.bias=-1
        inert_cursor(self)
    def geometry(self,target):
        self.geometry_calls+=1
        return dict(screen_target=list(target),virtual_desktop=[-3840,0,4864,1440],
                    window_rect=[0,0,1024,768])
    def submit(self,value):
        p=value.data.mi
        if p.dwFlags==0xC001:
            self.flags.append(p.dwFlags)
            if not self.freeze:self.xy=(-3840+p.dx*4864//65536,p.dy*1440//65536+self.bias)
            return 1
        return super().submit(value)


class OwnedMouseTests(unittest.TestCase):
    def click(self,api,sleep=lambda _:None):
        return mouse.guarded_click(api,lambda:None,mouse.TARGETS[0],sleep,absolute=True)
    def test_observed_negative_origin_one_pixel_error_converges_exactly(self):
        api=DesktopApi();r=self.click(api)
        self.assertIsNone(r['error']);self.assertEqual(r['before_click'],[318,508])
        self.assertEqual(r['moves'][0]['normalized'],[56034,23135])
        self.assertEqual(r['moves'][1]['before'],[318,507])
        self.assertEqual(r['moves'][1]['feedback_correction']['error'],[0,1])
        self.assertEqual(api.flags,[0xC001,0xC001,2,4]);self.assertTrue(r['released'])
    def test_four_move_limit_never_clicks_one_pixel_miss(self):
        api=DesktopApi();api.freeze=True;api.xy=(318,507);r=self.click(api)
        self.assertEqual(len(r['moves']),4);self.assertFalse(r['down_submitted'])
        self.assertNotIn(2,api.flags);self.assertIsNotNone(r['error'])
    def test_large_error_never_uses_feedback_correction(self):
        api=DesktopApi();api.bias=-4;r=self.click(api)
        self.assertTrue(all('feedback_correction'not in m for m in r['moves']))
        self.assertFalse(r['down_submitted'])
    def test_changed_geometry_restarts_original_mapping(self):
        api=DesktopApi();old=api.geometry
        def changed(target):
            g=old(target);g['window_rect'][2]+=api.geometry_calls
            return g
        api.geometry=changed;r=self.click(api)
        self.assertEqual(len(r['moves']),1)
        self.assertTrue(all('feedback_correction'not in m for m in r['moves']))
        self.assertFalse(r['down_submitted'])
    def test_feedback_requires_owned_window_margin(self):
        api=DesktopApi();old=api.geometry
        def edge(target):
            g=old(target);g['window_rect']=[318,0,1024,768];return g
        api.geometry=edge;r=self.click(api)
        self.assertEqual(len(r['moves']),1);self.assertFalse(r['down_submitted'])
        self.assertIn('margin',r['error'])
    def test_release_after_hold_exception(self):
        api=DesktopApi();api.xy=mouse.TARGETS[0]
        def fail(delay):
            if delay==.08:raise RuntimeError('interrupted')
        r=self.click(api,fail)
        self.assertTrue(r['released']);self.assertEqual(api.flags,[2,4])
    def test_stale_game_sample_cannot_submit_button(self):
        api=DesktopApi();api.xy=mouse.TARGETS[0];old=api.cursor_snapshot
        def stale(target):
            row=old(target);row['os_game_point'][1]+=1;return row
        api.cursor_snapshot=stale;r=self.click(api)
        self.assertFalse(r['down_submitted']);self.assertEqual(len(r['before_click_settling']),32)
    def test_cursor_moves_after_settling_before_down(self):
        api=DesktopApi();api.xy=mouse.TARGETS[0];old=api.cursor_snapshot;calls=[0]
        def moved(target):
            calls[0]+=1;row=old(target)
            if calls[0]>=5:row['os_game_point'][0]+=1
            return row
        api.cursor_snapshot=moved;r=self.click(api)
        self.assertFalse(r['down_submitted']);self.assertIn('before button-down',r['error'])


if __name__=='__main__':unittest.main()
