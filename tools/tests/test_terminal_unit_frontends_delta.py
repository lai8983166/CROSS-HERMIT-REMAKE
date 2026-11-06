import copy
import hashlib
import os
from pathlib import Path
import tempfile
import unittest
import zipfile
import zlib

from tools import terminal_unit_frontends_delta as d


class DeltaEvidenceTests(unittest.TestCase):
    def test_complete_corpus_roundtrip_and_wrong_header(self):
        base_id = dict(path='fixed-parent.gz', bytes=123, sha256='a' * 64)
        bases = [('neutral', {'a': 'ab' * 4000}), ('timeout', {'x': False})]
        values = [{'a': 'ab' * 4000, 'new': 'ce' * 4000}, {'x': 0}]
        with tempfile.TemporaryDirectory() as directory:
            writer = d.CorpusWriter(Path(directory) / 'corpus', base_id)
            for (name, base), value in zip(bases, values):
                writer.append(name, value, base)
            writer.close()
            self.assertEqual(list(d.read_corpus(writer.paths[1], writer.paths[0], base_id, bases)),
                             list(zip(['neutral', 'timeout'], values)))
            with self.assertRaises(ValueError):
                list(d.read_corpus(writer.paths[1], writer.paths[0], {}, bases))
            self.assertLess(sum(p.stat().st_size for p in writer.paths), 10000)

    def test_corpus_failure_cleanup_preserves_preexisting_files(self):
        with tempfile.TemporaryDirectory() as directory:
            prefix = Path(directory) / 'corpus'
            writer = d.CorpusWriter(prefix, {}, budget=400)
            with self.assertRaises(d.BudgetExceeded):
                writer.append('case', {'random': os.urandom(d.CHUNK).hex()}, {})
            self.assertTrue(all(not p.exists() for p in writer.paths))
            writer.paths[0].write_bytes(b'original')
            with self.assertRaises(ValueError):
                d.CorpusWriter(prefix, {})
            self.assertEqual(writer.paths[0].read_bytes(), b'original')

    def make(self, directory, base, value, limit=2 * 1024 * 1024):
        path = Path(directory) / 'chunks.zip'
        budget = d.Budget(limit)
        writer = d.BlobWriter(path, budget)
        try:
            record = d.encode(value, base, writer)
            count = len(writer.seen)
        finally:
            writer.close()
        return path, record, count

    def test_full_typed_round_trip_with_parent_and_cross_field_chunks(self):
        pixel = os.urandom(d.CHUNK).hex()
        base = dict(memory=[dict(hex=pixel * 2)], rows=[0, False, 'old'])
        value = dict(memory=[dict(hex=pixel * 2)], rows=[False, 0, 'new'],
                     copied_pixel=pixel, changed_pixel=pixel + 'ab' * d.CHUNK,
                     unicode='原始证据' * 7000, tuple=(1, 2), mapping={3: 'x'})
        with tempfile.TemporaryDirectory() as directory:
            path, record, count = self.make(directory, base, value)
            reader = d.BlobReader(path)
            try:
                actual = d.decode(record, base, reader)
                self.assertTrue(d.exact(actual, d.normalize(value)))
                self.assertIs(type(actual['rows'][0]), bool)
                self.assertIs(type(actual['rows'][1]), int)
                self.assertLess(path.stat().st_size, 20000)
                self.assertLess(count, 5)
                actual['memory'][0]['hex'] = 'changed'
                self.assertEqual(base['memory'][0]['hex'], pixel * 2)
            finally:
                reader.close()

    def test_exact_reuse_writes_no_blob(self):
        base = {'data': 'a1' * 200000, 'CPU': {'EAX': 1}}
        with tempfile.TemporaryDirectory() as directory:
            path, record, count = self.make(directory, base, copy.deepcopy(base))
            self.assertEqual(record['node'], ['r', []])
            self.assertEqual(count, 0)
            self.assertLess(path.stat().st_size, 100)

    def test_duplicate_new_bytes_stored_only_once(self):
        value = {'a': '2d' * d.CHUNK, 'b': '2d' * d.CHUNK}
        with tempfile.TemporaryDirectory() as directory:
            path, record, count = self.make(directory, {}, value)
            self.assertEqual(count, 1)
            reader = d.BlobReader(path)
            try:
                self.assertEqual(d.decode(record, {}, reader), value)
            finally:
                reader.close()

    def test_wrong_parent_and_invalid_reference_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path, record, _ = self.make(directory, {'a': 1}, {'a': 1})
            reader = d.BlobReader(path)
            try:
                with self.assertRaisesRegex(ValueError, 'wrong immutable parent'):
                    d.decode(record, {'a': 2}, reader)
                record['node'] = ['r', ['missing']]
                with self.assertRaisesRegex(ValueError, 'reference path'):
                    d.decode(record, {'a': 1}, reader)
            finally:
                reader.close()

    def test_missing_chunk_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path, record, _ = self.make(directory, {}, {'a': 'cd' * 5000})
            with zipfile.ZipFile(path, 'w'):
                pass
            reader = d.BlobReader(path)
            try:
                with self.assertRaisesRegex(ValueError, 'missing evidence chunk'):
                    d.decode(record, {}, reader)
            finally:
                reader.close()

    def test_corrupted_raw_chunk_and_bomb_are_rejected(self):
        for payload in (b'different', b'x' * (d.CHUNK + 1)):
            with self.subTest(bytes=len(payload)), tempfile.TemporaryDirectory() as directory:
                path, record, _ = self.make(directory, {}, {'a': 'cd' * 5000})
                with zipfile.ZipFile(path) as original:
                    name = original.namelist()[0]
                with zipfile.ZipFile(path, 'w', compression=zipfile.ZIP_STORED) as corrupted:
                    corrupted.writestr(name, zlib.compress(payload))
                reader = d.BlobReader(path)
                try:
                    with self.assertRaises(ValueError):
                        d.decode(record, {}, reader)
                finally:
                    reader.close()

    def test_changed_scalar_or_parent_chunk_digest_is_rejected(self):
        base = {'original': 'ed' * d.CHUNK}
        with tempfile.TemporaryDirectory() as directory:
            path, record, _ = self.make(directory, base, {'copy': base['original'] + '12' * 1000, 'number': 2})
            reader = d.BlobReader(path)
            try:
                changed = copy.deepcopy(record)
                changed['node'][1][1][1] = ['v', 3]
                with self.assertRaisesRegex(ValueError, 'case tree mismatch'):
                    d.decode(changed, base, reader)
                node = record['node'][1][0][1]
                if node[0] == 'n':
                    node = record['shared'][node[1]]
                node[4][0][1][-1] = '0' * 64
                with self.assertRaisesRegex(ValueError, 'parent chunk SHA'):
                    d.decode(record, base, reader)
            finally:
                reader.close()

    def test_budget_applies_across_files_and_before_write(self):
        with tempfile.TemporaryDirectory() as directory:
            budget = d.Budget(100)
            with budget.file(Path(directory) / 'a') as a, budget.file(Path(directory) / 'b') as b:
                a.write(b'a' * 70)
                with self.assertRaises(d.BudgetExceeded):
                    b.write(b'b' * 31)
                self.assertEqual(b.tell(), 0)
                b.write(b'b' * 30)
                a.seek(0)
                a.write(b'c')
                with self.assertRaises(d.BudgetExceeded):
                    a.seek(70)
                    a.write(b'd')
            self.assertEqual(sum(p.stat().st_size for p in Path(directory).iterdir()), 100)

    def test_normalization_rejects_collisions_and_nonfinite(self):
        with self.assertRaises(ValueError):
            d.normalize({1: 'x', '1': 'y'})
        with self.assertRaises(ValueError):
            d.normalize(float('nan'))

    def test_repeated_new_memory_pages_do_not_repeat_metadata(self):
        page = dict(pointer=0x34000000, bytes=4096, hex=os.urandom(4096).hex())
        value = dict(frames=[[copy.deepcopy(page)] for i in range(1000)])
        with tempfile.TemporaryDirectory() as directory:
            path, record, count = self.make(directory, {}, value)
            import json
            self.assertLess(len(json.dumps(record)), 20000)
            self.assertEqual(count, 1)
            reader = d.BlobReader(path)
            try:
                actual = d.decode(record, {}, reader)
                self.assertEqual(actual, value)
                actual['frames'][0][0]['pointer'] = 1
                self.assertEqual(actual['frames'][1][0]['pointer'], 0x34000000)
                bad = copy.deepcopy(record)
                bad['shared'] = [['n', 0]]
                bad['node'] = ['n', 0]
                with self.assertRaisesRegex(ValueError, 'cyclic'):
                    d.decode(bad, {}, reader)
            finally:
                reader.close()


if __name__ == '__main__':
    unittest.main()
