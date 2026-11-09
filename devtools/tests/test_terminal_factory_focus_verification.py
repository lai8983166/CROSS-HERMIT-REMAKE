"""Independent canonical binding rejection cases; no native calls."""
import ast
import copy
import hashlib
import struct
import unittest
from unittest.mock import patch
from devtools import terminal_factory_focus_verification as v
from devtools.tests.test_terminal_worker_retention_verification import frame


def fixture():
    raw=v.frozen.menu.contract.read_source()
    tree=ast.parse((v.ROOT/'tools/school_startup_lifetime.py').read_text())
    ranges=next(ast.literal_eval(n.value)for n in tree.body if isinstance(n,ast.Assign)
        and any(isinstance(t,ast.Name)and t.id=='RANGES'for t in n.targets))
    code=[dict(va=a,bytes=b-a,sha256=hashlib.sha256(raw[a-0x400000:b-0x400000]).hexdigest())for a,b in ranges]
    g={'0x7a4a00':0x210000,'0x7a49fc':0x220000,'0x80a398':0x230000,'0x7a0bb4':88}
    initial=dict(pid=77,elapsed=1.0,globals=dict(g,**{'0x7a49fc':0,'0x80a398':0}),
        frames=[frame(11,(0x49DF8A,0x45060F,0x5714E6))],source=code)
    ready=dict(pid=77,elapsed=2.0,globals=g,frames=[frame(11,(0x49DFD1,0x5714E6))],source=code,
        window=dict(pid=77,hwnd=88))
    for name,key,size in (('main','0x7a4a00',0x1110),('game','0x7a49fc',0xBA20),('cache','0x80a398',176)):
        ready[name]=dict(pointer=g[key],hex=bytes(size).hex())
    identities=[v.identity(v.ROOT/p)for p,digest in v.LAYER_IDENTITIES]
    qualification=dict(path='qualification.json',bytes=1,sha256='a'*64,current_guest_uuid='guest',
        current_guest_boot_utc='boot',current_guest_resources={},source_utf8='not copied into proof')
    receipt=dict(schema_version=1,kind='factory_and_ready_before_automatic_focus',capture_hook_restored=True,
        scope_errors=[],accepted=False,activation_success_inferred=False,full_factory_trace_proved=False,
        host_game_calls=[],host_memory_writes=[],host_input_actions=[],implementations=identities,
        implementations_after=copy.deepcopy(identities),qualification=qualification,deferred_members_calls=10,
        captures=[],focused_members_resumed=[dict(pid=77,elapsed=2.1,factory_capture_index=0,ready_capture_index=1,
            original_focused_members_dispatched=True,activation_success_claimed=False)])
    for kind,snapshot in (('factory',initial),('ready',ready)):
        digest=v.canonical(snapshot);receipt['captures'].append(dict(kind=kind,pid=77,elapsed=snapshot['elapsed'],
            capture_returned=True,original_capture_bytes=digest['bytes'],original_capture_sha256=digest['sha256'],
            canonical_encoding=v.ENCODING,factory_frame_tids=[11]if kind=='factory'else []))
    return dict(factory_focus_observation=receipt,lifecycle=dict(factory=initial,ready=ready),
        input_isolation=qualification,startup_activation=[dict(elapsed=2.2)])


class FactoryBindingTests(unittest.TestCase):
    def setUp(self):
        self.report=fixture()
        for name,result in (('verify_input_isolation',{}),('verify_guest_focus',{'path':'direct'})):
            mocking=patch.object(v.frozen,name,return_value=result);mocking.start();self.addCleanup(mocking.stop)

    def test_canonical_binding_is_small_and_preserves_input(self):
        before=copy.deepcopy(self.report);result=v.verify_observation(self.report)
        self.assertEqual(self.report,before);self.assertFalse(result['accepted'])
        self.assertNotIn('source_utf8',result['qualification'])
        self.assertEqual(result['activation']['outcome'],'original_activation_verified')

    def test_changed_canonical_snapshot_or_claimed_hash_rejected(self):
        for mutate in (lambda r:r['lifecycle']['factory'].update(elapsed=.9),
            lambda r:r['factory_focus_observation']['captures'][1].update(original_capture_sha256='0'*64)):
            r=copy.deepcopy(self.report);mutate(r)
            with self.assertRaisesRegex(ValueError,'canonical'):v.verify_observation(r)

    def test_early_activation_wrong_owner_or_fake_success_rejected(self):
        changes=[dict(pid=78),dict(elapsed=1.9),dict(factory_capture_index=1),dict(activation_success_claimed=True)]
        for change in changes:
            r=copy.deepcopy(self.report);r['factory_focus_observation']['focused_members_resumed'][0].update(change)
            with self.assertRaises(ValueError):v.verify_observation(r)

    def test_hook_identity_code_and_qualification_tamper_rejected(self):
        mutations=[lambda r:r['factory_focus_observation'].update(capture_hook_restored=False),
            lambda r:r['factory_focus_observation']['implementations_after'][0].update(sha256='0'*64),
            lambda r:r['lifecycle']['factory']['source'][0].update(sha256='0'*64),
            lambda r:r['factory_focus_observation'].update(qualification={})]
        for mutate in mutations:
            r=copy.deepcopy(self.report);mutate(r)
            with self.assertRaises(ValueError):v.verify_observation(r)

    def test_original_focus_error_is_not_rewritten_as_success(self):
        self.report['startup_activation']=[dict(elapsed=2.2,error='original foreground guard rejected')]
        result=v.verify_observation(self.report)
        self.assertEqual(result['activation'],dict(outcome='original_activation_failed',error='original foreground guard rejected'))
        self.assertFalse(result['full_school_source_verified'])

    def test_factory_only_mode_never_calls_complete_prefix_verifier(self):
        with patch.object(v.frozen,'read_report',return_value=self.report), \
             patch.object(v.retention,'verify_file',side_effect=AssertionError('fullschool must not execute')):
            result=v.verify_file(v.ROOT/'devtools/terminal_factory_focus.py','not-used-by-pure-mock',factory_only=True)
        self.assertFalse(result['full_school_source_verified']);self.assertFalse(result['accepted'])


if __name__=='__main__':unittest.main()
