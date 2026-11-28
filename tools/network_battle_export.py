"""Export the MAP71 terrain and the original lobby's eight default student records."""
import json
import struct

from tools import school_sortie_export as sortie
from tools.school_adventure_scene_rules import source_filenames


def export():
    image = sortie.SOURCE.read_bytes()
    assert sortie.digest(image) == sortie.SOURCE_SHA256
    out = sortie.OUT.parent / "network_battle"
    out.mkdir(exist_ok=True)
    _, files = source_filenames(image, 71)
    folder = sortie.GAME / "DATA/TACTICS/MAP"
    layout = sortie.logical_cells((folder/files[0]).read_bytes())
    graphics = (folder/files[1]).read_bytes()
    atlas = out / "map71.png"
    sortie.atlas_image(graphics, layout, sortie.map_textures(graphics, layout)).save(atlas)
    formation = sortie.formation()
    terrain = bytes.fromhex(formation["terrain_hex"])
    passability = [[int(mode == 4 or struct.unpack_from("<i", terrain, c[0]*76+mode*16+12)[0] != 0)
                    for c in layout["cells"]] for mode in range(5)]
    config = image[0x6ad1d0-sortie.BASE+71*42:0x6ad1d0-sortie.BASE+72*42]
    scene = {"cell_size": layout["cell_size"], "configuration_hex": config.hex(), "cells": layout["cells"],
             "atlas": "res://assets/network_battle/map71.png", "atlas_sha256": sortie.digest(atlas.read_bytes()),
             "passability": passability, "interaction": {"logic_hz":30,"move_interval":12,"delta_cap":0.2}}
    scene["formation_grid"] = [list(row[:3]) for row in struct.iter_unpack("<bbHH", bytes.fromhex(formation["grid_hex"]))]
    roster, skins = [], {}
    attack_rules = sortie.source_rules()
    sortie.PARENT_FRAMES = sortie.parent_frames(*([True]*12))
    for name in ("school_winter_jobs","school_winter_32","school_winter_44","school_winter_29",
                 "school_winter_45","school_eleven","school_thirty_three","school_dungeon_15","school_dungeon_16"):
        parent = json.loads((sortie.OUT.parent/name/"catalog.json").read_bytes())
        for skin in parent["skins"].values():
            for frame in skin["frames"].values():
                sortie.PARENT_FRAMES.setdefault(frame["file_sha256"], frame["file"])
    for i in range(8):
        offset = 0x605f18-sortie.BASE+176*i
        raw = image[offset:offset+176]
        role, = struct.unpack_from("<H", raw, 2)
        job, = struct.unpack_from("<H", raw, 12)
        attack_rules["jobs"][str(job)] = sortie.player_job(image, role, job)
        archetype, = struct.unpack_from("<H", image, 0x6b2d88-sortie.BASE+64*job+24)
        weapon = image[0x6c2dc8-sortie.BASE+72*archetype:0x6c2dc8-sortie.BASE+72*(archetype+1)]
        max_hp, hp = struct.unpack_from("<2h", raw, 20)
        max_mp, mp = struct.unpack_from("<2h", raw, 26)
        roster.append({"character_id": role, "job": job, "record_hex": raw.hex(), "category":0,
                       "skin_key": sortie.skin(role, job, image, skins, out),
                       "movement_type":raw[48],"limits":{"hp":hp,"hp_max":max_hp,"mp":mp,"mp_max":max_mp},
                       "combat":{**sortie.from_record(raw),"attack_id":archetype,"attack_class":weapon[5],"target_filter":weapon[25]}})
    catalog = {"scene": scene, "roster": roster, "skins": skins, "attack_rules": attack_rules}
    data = json.dumps(catalog, ensure_ascii=False, separators=(",",":")).encode()
    (out/"catalog.json").write_bytes(data)
    print("MAP71", scene["cell_size"], "default roster", [r["character_id"] for r in roster], sortie.digest(data))


if __name__ == "__main__":
    export()
