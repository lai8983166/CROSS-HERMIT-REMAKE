"""Exact two-constant correction of the frozen DC collector; no evidence rewrite.

The prior source/report remain immutable. OBJ_DC is read and checked against the
same Windows SDK used to build the native observer. No API return is replaced.
Importing this module does not launch native code. CLI keeps the original
single-attempt marker, fresh-output rule, exact build and offline identity gates.
"""
import hashlib as _hashlib
from pathlib import Path as _Path
import re as _re
from devtools import terminal_scene_dc_probe as _previous

_parent = _Path(_previous.__file__)
_source = _parent.read_bytes()
if _hashlib.sha256(_source).hexdigest() != '994d5ab7877c10bb3de9cc72ef00eaba9f57732ee646372d03c45d991258fed9':
    raise ValueError('frozen DC collector identity changed')
_sdk = _Path('C:/Program Files (x86)/Windows Kits/10/Include/10.0.26100.0/um/wingdi.h')
_match = _re.search(rb'^#define\s+OBJ_DC\s+(\d+)\s*$', _sdk.read_bytes(), _re.M)
if not _match or int(_match[1]) != 3:
    raise ValueError('Windows SDK OBJ_DC contract')
_corrected = _source.decode('utf-8')
for _field in ('before_type', 'now_type'):
    _old = "q['" + _field + "']==1"
    if _corrected.count(_old) != 1:
        raise ValueError('one exact original enum comparison required')
    _corrected = _corrected.replace(_old, "q['" + _field + "']==" + _match[1].decode('ascii'))
exec(compile(_corrected, str(_Path(__file__).resolve()), 'exec'), globals())
