"""Lossless parent-referenced evidence with bounded, deduplicated binary chunks.

The parent is immutable evidence, not a restored guest/native execution. No
uncompressed case file is written. Decoded values have ordinary JSON semantics.
"""
import copy
import gzip
import hashlib
import io
import json
import math
from pathlib import Path
import re
import struct
import zipfile
import zlib

CHUNK = 65536
PRIMARY_LIMIT = 128 * 1024 * 1024
HEX = re.compile(r'^[0-9a-f]+$')


class BudgetExceeded(ValueError):
    pass


class Budget:
    def __init__(self, limit=PRIMARY_LIMIT):
        if type(limit) is not int or limit < 1:
            raise ValueError('positive evidence budget required')
        self.limit, self.sizes = limit, {}

    def file(self, path):
        return BudgetFile(path, self)


class BudgetFile(io.FileIO):
    def __init__(self, path, budget):
        self.budget = budget
        self.key = str(path)
        if self.key in budget.sizes:
            raise ValueError('one exclusive writer per evidence path')
        super().__init__(path, 'x+')
        budget.sizes[self.key] = 0

    def write(self, data):
        high = max(self.budget.sizes[self.key], self.tell() + len(data))
        total = sum(self.budget.sizes.values()) - self.budget.sizes[self.key] + high
        if total > self.budget.limit:
            raise BudgetExceeded('evidence primary budget exceeded before disk write')
        n = super().write(data)
        self.budget.sizes[self.key] = max(self.budget.sizes[self.key], self.tell())
        return n


def normalize(value, _memo=None, _active=None):
    """Match JSON round-trip types without serializing a multi-GiB whole case."""
    if _memo is None:
        _memo, _active = {}, set()
    if value is None or type(value) in (str, int, bool):
        return value
    if type(value) is float:
        if not math.isfinite(value):
            raise ValueError('nonfinite JSON number')
        return value
    if type(value) in (dict, list, tuple):
        identity = id(value)
        if identity in _active:
            raise ValueError('circular evidence value')
        if identity in _memo:
            return _memo[identity]
        _active.add(identity)
    if type(value) in (list, tuple):
        result = [normalize(x, _memo, _active) for x in value]
        _active.remove(identity)
        _memo[identity] = result
        return result
    if type(value) is dict:
        result = {}
        for key, item in value.items():
            if type(key) is str:
                name = key
            elif key is None:
                name = 'null'
            elif type(key) is bool:
                name = 'true' if key else 'false'
            elif type(key) in (int, float):
                name = json.dumps(key, allow_nan=False)
            else:
                raise ValueError('unsupported JSON key')
            if name in result:
                raise ValueError('colliding normalized JSON keys')
            result[name] = normalize(item, _memo, _active)
        _active.remove(identity)
        _memo[identity] = result
        return result
    raise ValueError('unsupported evidence value ' + type(value).__name__)


def exact(a, b):
    if type(a) is not type(b):
        return False
    if type(a) is dict:
        return a.keys() == b.keys() and all(exact(v, b[k]) for k, v in a.items())
    if type(a) is list:
        return len(a) == len(b) and all(exact(x, y) for x, y in zip(a, b))
    return a == b


def _fingerprint_v1(value):
    """Canonical typed tree digest; independent of JSON whitespace/key order."""
    h = hashlib.sha256()

    def walk(v):
        if type(v) is dict:
            h.update(b'D' + struct.pack('<Q', len(v)))
            for key in sorted(v):
                walk(key)
                walk(v[key])
        elif type(v) is list:
            h.update(b'L' + struct.pack('<Q', len(v)))
            for x in v:
                walk(x)
        elif type(v) is str:
            h.update(b'S' + struct.pack('<Q', len(v)))
            for pos in range(0, len(v), CHUNK):
                h.update(v[pos:pos + CHUNK].encode('utf8'))
        else:
            h.update(b'V' + json.dumps(v, allow_nan=False).encode('ascii') + b';')

    walk(value)
    return h.hexdigest()


def fingerprint(value):
    """Merkle tree digest with value-preserving reuse of immutable snapshots."""
    memo = {}

    def walk(v):
        cacheable = type(v) in (dict, list, str)
        if cacheable and id(v) in memo:
            return memo[id(v)]
        h = hashlib.sha256()
        if type(v) is dict:
            h.update(b'D' + struct.pack('<Q', len(v)))
            for key in sorted(v):
                h.update(walk(key))
                h.update(walk(v[key]))
        elif type(v) is list:
            h.update(b'L' + struct.pack('<Q', len(v)))
            for item in v:
                h.update(walk(item))
        elif type(v) is str:
            h.update(b'S' + struct.pack('<Q', len(v)))
            for pos in range(0, len(v), CHUNK):
                h.update(v[pos:pos+CHUNK].encode('utf8'))
        else:
            h.update(b'V' + json.dumps(v, allow_nan=False).encode('ascii') + b';')
        result = h.digest()
        if cacheable:
            memo[id(v)] = result
        return result

    return walk(value).hex()


def at_path(base, path):
    value = base
    if type(path) is not list:
        raise ValueError('reference path must be a list')
    for part in path:
        if type(value) is dict and type(part) is str and part in value:
            value = value[part]
        elif type(value) is list and type(part) is int and 0 <= part < len(value):
            value = value[part]
        else:
            raise ValueError('invalid parent reference path')
    return value


def chunks(text):
    mode = 'hex' if len(text) % 2 == 0 and HEX.fullmatch(text) else 'utf8'
    if mode == 'hex':
        for pos in range(0, len(text), CHUNK * 2):
            yield mode, pos, bytes.fromhex(text[pos:pos + CHUNK * 2])
    else:
        # Character offsets permit bounded UTF-8 decoding of parent slices.
        for pos in range(0, len(text), CHUNK // 4):
            yield mode, pos, text[pos:pos + CHUNK // 4].encode('utf8')


def parent_chunk(base, ref):
    path, mode, pos, size, digest = ref
    text = at_path(base, path)
    if type(text) is not str or type(pos) is not int or pos < 0:
        raise ValueError('invalid parent string reference')
    if mode == 'hex':
        if size < 1 or size > CHUNK or pos % 2 or pos + size * 2 > len(text):
            raise ValueError('invalid parent hex extent')
        raw = bytes.fromhex(text[pos:pos + size * 2])
    elif mode == 'utf8':
        if size < 1 or size > CHUNK // 4 or pos + size > len(text):
            raise ValueError('invalid parent text extent')
        raw = text[pos:pos + size].encode('utf8')
    else:
        raise ValueError('unknown parent chunk mode')
    if hashlib.sha256(raw).hexdigest() != digest:
        raise ValueError('parent chunk SHA mismatch')
    return raw


class ParentIndex:
    def __init__(self, base):
        self.base, self.by_hash, self.by_string = base, {}, {}
        self._walk(base, [])

    def _walk(self, value, path):
        if type(value) is dict:
            for key, item in value.items():
                self._walk(item, path + [key])
        elif type(value) is list:
            for i, item in enumerate(value):
                self._walk(item, path + [i])
        elif type(value) is str and len(value) >= 4096:
            digest = hashlib.sha256(value.encode('utf8')).hexdigest()
            # Canonical cross-field references prevent shifted memory-map lists
            # from making identical data depend on thousands of different paths.
            if digest in self.by_string:
                return
            self.by_string[digest] = path
            for mode, pos, raw in chunks(value):
                digest = hashlib.sha256(raw).hexdigest()
                count = len(raw) if mode == 'hex' else len(raw.decode('utf8'))
                self.by_hash.setdefault(digest, [path, mode, pos, count, digest])


class BlobWriter:
    def __init__(self, path, budget):
        self.file = budget.file(path)
        self.zip = zipfile.ZipFile(self.file, 'w', compression=zipfile.ZIP_STORED)
        self.seen = set()

    def put(self, raw):
        if not 1 <= len(raw) <= CHUNK:
            raise ValueError('bounded nonempty raw chunk required')
        digest = hashlib.sha256(raw).hexdigest()
        if digest not in self.seen:
            if len(self.seen) >= 32768:
                raise BudgetExceeded('new unique chunk count exceeded')
            info = zipfile.ZipInfo(digest, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_STORED
            self.zip.writestr(info, zlib.compress(raw, 6))
            self.seen.add(digest)
        return digest

    def close(self):
        try:
            self.zip.close()
        finally:
            self.file.close()


class BlobReader:
    def __init__(self, path):
        self.zip = zipfile.ZipFile(path, 'r')
        rows = self.zip.infolist()
        names = [x.filename for x in rows]
        if len(names) != len(set(names)) or len(names) > 32768:
            self.zip.close()
            raise ValueError('duplicate or excess chunk members')
        if any(not re.fullmatch('[0-9a-f]{64}', x.filename) or
               x.file_size > CHUNK * 2 or x.compress_type != zipfile.ZIP_STORED
               for x in rows):
            self.zip.close()
            raise ValueError('invalid chunk member')

    def get(self, digest):
        if not re.fullmatch('[0-9a-f]{64}', digest):
            raise ValueError('invalid chunk identity')
        try:
            packed = self.zip.read(digest)
        except KeyError as e:
            raise ValueError('missing evidence chunk') from e
        inflater = zlib.decompressobj()
        raw = inflater.decompress(packed, CHUNK + 1)
        if not inflater.eof or inflater.unused_data or len(raw) > CHUNK or not raw:
            raise ValueError('invalid bounded chunk stream')
        if hashlib.sha256(raw).hexdigest() != digest:
            raise ValueError('evidence chunk SHA mismatch')
        return raw

    def close(self):
        self.zip.close()


def encode(value, base, blobs, index=None):
    value = normalize(value)
    index = ParentIndex(base) if index is None else index
    missing = object()
    shared, interned = [], {}
    encoded_objects = {}

    def intern(node):
        wire = json.dumps(node, ensure_ascii=False, separators=(',', ':')).encode('utf8')
        if len(wire) < 80:
            return node
        key = hashlib.sha256(wire).digest()
        if key not in interned:
            interned[key] = len(shared)
            shared.append(node)
        return ['n', interned[key]]

    def walk(v, old, path):
        cacheable = type(v) in (dict, list) or type(v) is str and len(v) >= 4096
        if cacheable and id(v) in encoded_objects:
            return encoded_objects[id(v)]
        result = build(v, old, path)
        if cacheable:
            encoded_objects[id(v)] = result
        return result

    def build(v, old, path):
        if type(v) is str and len(v) >= 4096:
            prior = index.by_string.get(hashlib.sha256(v.encode('utf8')).hexdigest())
            if prior is not None:
                return ['r', prior]
        if type(v) in (dict, list) and old is not missing and exact(v, old):
            return ['r', path]
        if type(v) is dict:
            return intern(['d', [[k, walk(x, old.get(k, missing) if type(old) is dict else missing,
                                         path + [k])] for k, x in v.items()]])
        if type(v) is list:
            children = [walk(x, old[i] if type(old) is list and i < len(old) else missing,
                             path + [i]) for i, x in enumerate(v)]
            if len(children) > 128:
                return intern(['a', [intern(['l', children[i:i+128]])
                                     for i in range(0, len(children), 128)]])
            return intern(['l', children])
        if type(v) is str and len(v) >= 4096:
            refs, mode = [], None
            for mode, pos, raw in chunks(v):
                digest = hashlib.sha256(raw).hexdigest()
                prior = index.by_hash.get(digest)
                refs.append(['p', prior] if prior is not None else ['b', blobs.put(raw)])
            return intern(['s', mode, len(v), hashlib.sha256(v.encode('utf8')).hexdigest(), refs])
        return ['v', v]

    node = walk(value, base, [])
    return dict(schema_version=2,base_tree_sha256=fingerprint(base),
                value_tree_sha256=fingerprint(value),node=node,shared=shared)


def decode(record, base, blobs):
    version = record.get('schema_version')
    tree_hash = fingerprint if version == 2 else _fingerprint_v1
    if version not in (1, 2) or tree_hash(base) != record['base_tree_sha256']:
        raise ValueError('wrong immutable parent case')
    shared = record.get('shared', [])
    cache, active = {}, set()

    def walk(node):
        if type(node) is not list or not node:
            raise ValueError('invalid evidence node')
        kind = node[0]
        if kind == 'n' and len(node) == 2:
            i = node[1]
            if type(i) is not int or not 0 <= i < len(shared) or i in active:
                raise ValueError('invalid or cyclic shared evidence node')
            if i not in cache:
                active.add(i)
                cache[i] = walk(shared[i])
                active.remove(i)
            return copy.deepcopy(cache[i])
        if kind == 'r' and len(node) == 2:
            return copy.deepcopy(at_path(base, node[1]))
        if kind == 'v' and len(node) == 2 and type(node[1]) not in (dict, list):
            return normalize(node[1])
        if kind == 'l' and len(node) == 2:
            return [walk(x) for x in node[1]]
        if kind == 'a' and len(node) == 2 and version == 2:
            out = []
            for child in node[1]:
                part = walk(child)
                if type(part) is not list:
                    raise ValueError('invalid shared array chunk')
                out.extend(part)
            return out
        if kind == 'd' and len(node) == 2:
            result = {}
            for key, child in node[1]:
                if type(key) is not str or key in result:
                    raise ValueError('invalid/duplicate evidence object key')
                result[key] = walk(child)
            return result
        if kind == 's' and len(node) == 5:
            mode, count, digest, refs = node[1:]
            if mode not in ('hex', 'utf8') or type(count) is not int or count < 4096:
                raise ValueError('invalid string encoding')
            pieces = []
            for kind, arg in refs:
                if kind == 'p':
                    raw = parent_chunk(base, arg)
                elif kind == 'b':
                    raw = blobs.get(arg)
                else:
                    raise ValueError('unknown chunk source')
                pieces.append(raw.hex() if mode == 'hex' else raw.decode('utf8'))
            value = ''.join(pieces)
            if len(value) != count or hashlib.sha256(value.encode('utf8')).hexdigest() != digest:
                raise ValueError('restored string identity mismatch')
            return value
        raise ValueError('unsupported evidence node')

    value = walk(record['node'])
    if tree_hash(value) != record['value_tree_sha256']:
        raise ValueError('restored case tree mismatch')
    return value


class CorpusWriter:
    """Exclusive two-file corpus. Errors remove only files created by this writer."""
    def __init__(self, prefix, base_identity, budget=PRIMARY_LIMIT):
        prefix = Path(prefix)
        self.paths = [Path(str(prefix) + '.chunks.zip'), Path(str(prefix) + '.delta.jsonl.gz')]
        if any(p.exists() for p in self.paths):
            raise ValueError('fresh immutable corpus paths required')
        self.budget = Budget(budget)
        self.created = []
        self.count = 0
        self.finished = False
        try:
            self.blobs = BlobWriter(self.paths[0], self.budget)
            self.created.append(self.paths[0])
            self.meta_file = self.budget.file(self.paths[1])
            self.created.append(self.paths[1])
            self.meta = gzip.GzipFile(filename='', mode='wb', fileobj=self.meta_file, mtime=0)
            self._line(dict(kind='header', schema_version=1, base=base_identity,
                            chunk_bytes=CHUNK, chunks_file=self.paths[0].name,
                            primary_budget=budget))
        except Exception:
            self.abort()
            raise

    def _line(self, value):
        raw = json.dumps(value, ensure_ascii=False, separators=(',', ':'), allow_nan=False).encode('utf8')
        if len(raw) > 64 * 1024 * 1024:
            raise BudgetExceeded('one case metadata exceeds64MiB before writing')
        self.meta.write(raw + b'\n')
        self.meta.flush()

    def append(self, name, value, base):
        if self.finished:
            raise ValueError('corpus already closed')
        try:
            self._line(dict(kind='case', name=name, evidence=encode(value, base, self.blobs)))
            self.count += 1
        except Exception:
            self.abort()
            raise

    def close(self):
        if self.finished:
            return
        try:
            self._line(dict(kind='footer', complete=True, cases=self.count))
            self.meta.close()
            self.meta_file.close()
            self.blobs.close()
            self.finished = True
        except Exception:
            self.abort()
            raise

    def abort(self):
        # A budget failure must not become a persistent large failed dump.
        for resource in ('meta', 'meta_file', 'blobs'):
            value = getattr(self, resource, None)
            if value is not None:
                try:
                    value.close()
                except Exception:
                    pass
        for path in self.created:
            if path.is_file():
                path.unlink()
        self.finished = True


def read_corpus(metadata, chunks_path, base_identity, base_cases):
    """Yield one full case at a time after validating its exact fixed parent.

    The caller verifies the immutable base file size/SHA before supplying its
    streamed cases. No retired development/failed source is a dependency.
    """
    maximum = 64 * 1024 * 1024
    blobs = BlobReader(chunks_path)
    try:
        with gzip.open(metadata, 'rb') as f:
            def line():
                raw = f.readline(maximum + 2)
                if not raw or len(raw) > maximum + 1 or not raw.endswith(b'\n'):
                    raise ValueError('missing, truncated or oversized corpus row')
                return json.loads(raw)

            header = line()
            if (header.get('kind'), header.get('schema_version'), header.get('base'),
                    header.get('chunk_bytes'), header.get('chunks_file')) != (
                    'header', 1, base_identity, CHUNK, Path(chunks_path).name):
                raise ValueError('wrong immutable corpus header/parent')
            count = 0
            for name, base in base_cases:
                row = line()
                if row.get('kind') != 'case' or row.get('name') != name:
                    raise ValueError('parent/current case order or identity differs')
                value = decode(row['evidence'], base, blobs)
                count += 1
                yield name, value
            if line() != dict(kind='footer', complete=True, cases=count) or f.read(1):
                raise ValueError('incomplete corpus, extra cases or trailing data')
    finally:
        blobs.close()
