"""Reject mutations of the fresh original-game file-event observation."""
import copy
import gzip
import json
import unittest
from devtools import terminal_new_game_oplock_verification as v


class NativeEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.path=v.host.ROOT/'analysis/terminal-new-game-oplock-native-v1-20261112.json.gz'
        cls.report=json.loads(gzip.decompress(cls.path.read_bytes()))
        cls.raw=(v.host.ROOT/'analysis/hermit_game.exe').read_bytes()

    def source(self):
        report=copy.deepcopy(self.report);p=report['probe'];gate=p['targeted_capture']['oplock']
        row=next(s for s in p['samples'] if s['elapsed']==gate['sample_elapsed'])
        task=next(t for t in row['tasks'] if t['vtable']==v.host.menu.NEW_GAME)
        frame=next(f for f in row['frames'] if f['tid']==gate['thread_id'])
        return report,p,gate,task,frame

    def test_real_game_handoff_and_unchanged_acceptance_boundary(self):
        result=v.verify_report(self.report,self.raw,check_disk=False)
        self.assertTrue(result['host_menu_observation_verified'])
        self.assertTrue(result['oplock']['event_triggered_NEW_GAME_observed'])
        for key in ('accepted','wait_return_proved','result_consumption_proved',
                    'normal_PTD_cleanup_proved','full_battle_exit_accepted','WinMain_normal_return_proved'):
            self.assertIs(result[key],False)

    def test_changed_debug_owner_rejected(self):
        r,p,g,t,f=self.source();g['owner_during']['debug_port']=0
        with self.assertRaisesRegex(ValueError,'debug port'):v.verify_event(r,self.raw,False)

    def test_wrong_file_rejected(self):
        r,p,g,t,f=self.source();s=bytearray.fromhex(f['oplock_file_open']['name_hex']);s[-2]=ord('Z')
        f['oplock_file_open']['name_hex']=s.hex()
        with self.assertRaisesRegex(ValueError,'CH001'):v.verify_event(r,self.raw,False)

    def test_release_before_capture_rejected(self):
        r,p,g,t,f=self.source();g['snapshot_end_qpc']=g['oplock']['release_begin_qpc']+1
        with self.assertRaisesRegex(ValueError,'order'):v.verify_event(r,self.raw,False)

    def test_changed_real_PTD_owner_rejected(self):
        r,p,g,t,f=self.source();s=bytearray.fromhex(t['TLS']['PTD_hex']);s[0]^=1;t['TLS']['PTD_hex']=s.hex()
        with self.assertRaises(ValueError):v.verify_report(r,self.raw,False)

    def test_missing_retained_exit_rejected(self):
        r,p,g,t,f=self.source();w=next(w for w in p['workers'] if w['thread_id']==g['thread_id']);del w['exit']
        with self.assertRaises(ValueError):v.verify_report(r,self.raw,False)

    def test_ADV_without_TLS_rejected(self):
        r,p,g,t,f=self.source()
        for row in p['samples']:
            for task in row['tasks']:
                if task['vtable']==v.host.menu.ADV:task.pop('TLS',None)
        with self.assertRaisesRegex(ValueError,'ADV'):v.verify_report(r,self.raw,False)

    def test_false_desktop_recovery_rejected(self):
        d=json.loads((v.host.ROOT/(str(self.path.relative_to(v.host.ROOT))+'.desktop.json')).read_text())
        p=v.host.ROOT/'analysis/terminal-new-game-oplock-native-v1-recovery-20261112.json'
        recovery=json.loads(p.read_text());recovery['final_after'][1]['taskbars'][0]['visible']=False
        with self.assertRaises(ValueError):v.host.verify_desktop(self.report,d,recovery)


if __name__=='__main__':unittest.main()
