"""Export the original fixed and random loot rows for the three April sorties."""
import json
import struct

from tools.tactics_exit_emulation import BASE, ROOT, SOURCE, SOURCE_SHA256
from hashlib import sha256


def catalog():
    image = SOURCE.read_bytes()
    if sha256(image).hexdigest() != SOURCE_SHA256:
        raise ValueError("Original image digest mismatch")
    missions = {}
    for mission in (1, 2, 3):
        def words(address, count):
            return list(struct.unpack_from(f'<{count}h', image, address-BASE+mission*256))
        missions[str(mission)] = {
            'loot_quotas': [words(0x73bf1a+14*i, 7) for i in range(5)],
            'fixed_items': words(0x73bf60, 8),
            'objective_rewards': [words(0x73bf70+6*i, 3) for i in range(16)]}
    return {'source_image_sha256': SOURCE_SHA256, 'missions': missions}


if __name__ == '__main__':
    output = ROOT/'prototype/data/school_native_april_rewards.json'
    output.write_text(json.dumps(catalog(), separators=(',', ':'))+'\n',encoding='utf8',newline='\n')
    print(sha256(output.read_bytes()).hexdigest())
