"""List original scene configurations, school rounds and network choices by terrain."""
import hashlib
import re
import struct
from collections import defaultdict

from tools.school_return_adventures_catalog import catalog
from tools.tactics_exit_emulation import ROOT, SOURCE, SOURCE_SHA256


def routes():
    image = SOURCE.read_bytes()
    if hashlib.sha256(image).hexdigest() != SOURCE_SHA256:
        raise ValueError('Original image changed')
    folder = ROOT / 'CROSS HERMIT/CROSS HERMIT/DATA/TACTICS/MAP'
    terrain = {p.stem.upper(): defaultdict(list) for p in folder.glob('*')
               if re.fullmatch(r'MAP\d\d\.BIN', p.name.upper()) and
               all(p.with_suffix(ext).is_file() or p.with_suffix(ext.lower()).is_file()
                   for ext in ('.MAP', '.BMP', '.VPT'))}

    def word(address):
        return struct.unpack_from('<h', image, address - 0x400000)[0]

    def map_name(scene):
        offset = struct.unpack_from('<I', image, 0x2B13F0 + scene*16)[0] - 0x400000
        if not 0 <= offset <= len(image)-10:
            return ''
        raw = image[offset:offset+10]
        return raw[:5].decode().upper() if re.fullmatch(rb'map\d\d\.bin\x00', raw) else ''

    for scene in range(256):
        name = map_name(scene)
        if name in terrain and word(0x6AD1D0 + scene*42) == scene:
            terrain[name]['scenes'].append(scene)
    for row in catalog(())['adventures']:
        for entry in row['rounds']:
            scene = entry['scene_id']
            visited = set()
            while scene > 0:
                if scene in visited or scene >= 256:
                    raise ValueError(f'Invalid scene chain for adventure {row["id"]}')
                visited.add(scene)
                name = map_name(scene)
                if name in terrain:
                    terrain[name]['school'].append((row['id'], scene))
                scene = word(0x6AD1D2 + 42*scene)
    for index in range(128):
        scene = word(0x5FFCB2 + 8*index)
        name = map_name(scene)
        if name in terrain:
            terrain[name]['network'].append((index, scene))
    return terrain


if __name__ == '__main__':
    for name, fields in sorted(routes().items()):
        print(name, dict(fields))
