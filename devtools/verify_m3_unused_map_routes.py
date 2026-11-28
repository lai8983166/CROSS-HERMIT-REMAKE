"""Check school/network reachability and the original dispatcher for MAP23 and MAP30."""
import struct
from hashlib import sha256

from devtools.m3_map_routes import routes
from tools.tactics_exit_emulation import BASE, SOURCE, SOURCE_SHA256


def main():
    image = SOURCE.read_bytes()
    assert sha256(image).hexdigest() == SOURCE_SHA256
    mappings = routes()

    def word(address):
        return struct.unpack_from("<I", image, address - BASE)[0]

    def dispatch(scene):
        table_index = image[0x432533 - BASE + scene]
        return word(0x43247f + table_index * 4)

    assert image[0x43219b-BASE:0x4321a8-BASE] == bytes.fromhex("8a8a33254300ff248d7f244300")
    assert dispatch(71) == 0x4323df
    for terrain, scene in (("MAP23", 93), ("MAP30", 94)):
        assert dict(mappings[terrain]) == {"scenes": [scene]}
        assert dispatch(scene) == 0x43243c
    # Default dispatch calls the source assertion reporter, then branches to the common exit.
    start = 0x43243c - BASE
    branch = image[start:start+0x30]
    calls = [0x43243c + i + 5 + struct.unpack_from("<i", branch, i+1)[0]
             for i in range(len(branch)-4) if branch[i] == 0xe8]
    assert 0x424f80 in calls
    print("MAP23/30 have terrain pointers but no school/network choice or normal objective dispatch")


if __name__ == "__main__":
    main()
