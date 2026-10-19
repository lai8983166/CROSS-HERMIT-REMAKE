import json
import unittest
from tools.school_main_context_platform import *


def prefix(platform):
    for index in range(2):
        r=platform.request('InitializeCriticalSection',index=index,before_hex='cd'*24)
        assert len(bytes.fromhex(r['hex']))==24
        assert r['native_return_type']=='void' and r['eax_is_status'] is False
        assert r['forwarder_freed'] and r['guards_unchanged']
        code=bytes.fromhex(r['forwarder_hex'])
        assert len(code)==19 and code[:7]==bytes.fromhex('558becff7508b8') and code[11:]==bytes.fromhex('ffd08be55dc20400')
    return platform.request('CreateEventA',args=[0,0,0,0])


class PlatformTests(unittest.TestCase):
    def test_actual_full_protocol_and_balanced_resources(self):
        with MainPlatform() as p:
            self.assertGreater(prefix(p)['result'],0)
            before=bytes([0xCD])*525
            d=p.request('GetCurrentDirectoryA',before_hex=before.hex());n=d['result'];raw=bytes.fromhex(d['hex'])
            self.assertEqual(raw[n+1:],before[n+1:])
            a=p.request('PathAddBackslashA',before_hex=d['hex']);path=bytes.fromhex(a['hex']);s=path.split(b'\0',1)[0]+b'\0'
            self.assertTrue(s.endswith(b'\\\0'));self.assertEqual(a['return_offset'],len(s)-1)
            for i in range(7):
                r=p.request('lstrcpyA',before_hex='cd'*260,source_hex=s.hex())
                self.assertEqual(bytes.fromhex(r['hex']),s+b'\xcd'*(260-len(s)))
            r=p.request('lstrcatA',before_hex=r['hex'],source_hex=b'SaveData\\\0'.hex())
            text=s[:-1]+b'SaveData\\\0'
            self.assertEqual(bytes.fromhex(r['hex']),text+b'\xcd'*(260-len(text)))
        self.assertEqual(p.cleanup,dict(critical_sections_deleted=2,event_handles_closed=1,all_owned_resources_released=True))

    def test_refusals_do_not_consume_resource_sequence(self):
        with MainPlatform() as p:
            for op,args in [('InitializeCriticalSection',dict(index=1,before_hex='cd'*24)),
                    ('InitializeCriticalSection',dict(index=0,before_hex='cd'*23)),
                    ('CreateEventA',dict(args=[0,0,0,0])),
                    ('lstrcpyA',dict(before_hex='cd'*260,source_hex='00'))]:
                with self.assertRaises(ValueError):p.request(op,**args)
            self.assertGreater(prefix(p)['result'],0)
            with self.assertRaises(ValueError):p.request('CreateEventA',args=[0,0,0,0])
            with self.assertRaises(ValueError):p.request('InitializeCriticalSection',index=2,before_hex='cd'*24)
        self.assertEqual(p.cleanup['critical_sections_deleted'],2)
        self.assertEqual(p.cleanup['event_handles_closed'],1)

    def test_partial_cleanup(self):
        for count in (0,1,2):
            with MainPlatform() as p:
                for i in range(count):p.request('InitializeCriticalSection',index=i,before_hex='cd'*24)
            self.assertEqual(p.cleanup,dict(critical_sections_deleted=count,event_handles_closed=0,all_owned_resources_released=True))

    def test_provenance_is_pinned_to_owned_source_and_binary(self):
        r=json.loads((ROOT/'analysis/school-main-context-platform-v1-20261019.json').read_text(encoding='utf8'))
        self.assertEqual(r['build'],dict(source_sha256=sha(SOURCE.read_bytes()),compiler_sha256=sha(COMPILER.read_bytes()),helper_sha256=sha(HELPER.read_bytes()),machine=0x14C))
        with MainPlatform() as p:
            self.assertEqual(p.hello['pointer_bytes'],4)
            self.assertTrue(p.hello['auxiliary_empty_path_module_probe'])
            self.assertEqual(p.provenance,r['system_modules'])
        self.assertTrue(p.cleanup['all_owned_resources_released'])


if __name__=='__main__':unittest.main()
