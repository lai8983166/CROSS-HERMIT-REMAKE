import hashlib
from pathlib import Path
import unittest
from unittest.mock import patch
from devtools import terminal_heap_etw_probe_v2 as v


class HeapPathAdapterTests(unittest.TestCase):
    def test_dependencies_read_all_four_real_files(self):
        rows=v.dependencies()
        self.assertEqual([Path(x['path']).name for x in rows],['terminal_heap_etw_probe.py','terminal_heap_etw_probe_v2.py',
            'terminal_heap_etw_helper.cs','terminal_wait_etw_probe.py'])
        for row in rows:
            data=Path(row['path']).read_bytes()
            self.assertEqual((row['bytes'],row['sha256']),(len(data),hashlib.sha256(data).hexdigest()))

    def test_only_run_and_decode_dependency_lookup_changes(self):
        for wrapped,original in ((v.run,v.parent.run),(v.decode,v.parent.decode)):
            self.assertIs(wrapped.__code__,original.__code__)
            self.assertIs(wrapped.__globals__['dependencies'],v.dependencies)
            for name in original.__globals__:
                if name!='dependencies':self.assertIs(wrapped.__globals__[name],original.__globals__[name])
        self.assertIs(v.main.__globals__['run'],v.run);self.assertIs(v.main.__globals__['decode'],v.decode)

    def test_frozen_parent_drift_refused(self):
        with patch.object(v,'PARENT_SHA','0'*64):
            with self.assertRaisesRegex(ValueError,'fixed first heap'):v.dependencies()

    def test_host_qualification_remains_before_dependencies(self):
        with patch.object(v.parent,'qualified',side_effect=ValueError('not guest')):
            # Clone afresh so the test's explicit qualification substitute is used.
            call=v.clone(v.parent.run,dependencies=v.dependencies)
            with self.assertRaisesRegex(ValueError,'not guest'):call(Path('not-created.json'))


if __name__=='__main__':unittest.main()
