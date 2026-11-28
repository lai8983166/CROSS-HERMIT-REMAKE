"""Export the MAP71 terrain and the original lobby's eight default student records."""
import json
import struct

from tools import school_sortie_export as sortie
from tools.school_adventure_scene_rules import source_filenames


def export(scene_id=71):
    if scene_id not in (42, 43, 71, 93, 94):
        raise ValueError(scene_id)
    image = sortie.SOURCE.read_bytes()
    assert sortie.digest(image) == sortie.SOURCE_SHA256
    out = sortie.OUT.parent / ("network_battle" if scene_id == 71 else f"terrain_practice_{scene_id}" if scene_id in (93,94) else f"network_battle_{scene_id}")
    out.mkdir(exist_ok=True)
    _, files = source_filenames(image, scene_id)
    folder = sortie.GAME / "DATA/TACTICS/MAP"
    layout = sortie.logical_cells((folder/files[0]).read_bytes())
    graphics = (folder/files[1]).read_bytes()
    atlas = out / files[0].lower().replace(".bin", ".png")
    sortie.atlas_image(graphics, layout, sortie.map_textures(graphics, layout)).save(atlas)
    formation = sortie.formation()
    terrain = bytes.fromhex(formation["terrain_hex"])
    passability = [[int(mode == 4 or struct.unpack_from("<i", terrain, c[0]*76+mode*16+12)[0] != 0)
                    for c in layout["cells"]] for mode in range(5)]
    config = image[0x6ad1d0-sortie.BASE+scene_id*42:0x6ad1d0-sortie.BASE+(scene_id+1)*42]
    scene = {"cell_size": layout["cell_size"], "configuration_hex": config.hex(), "cells": layout["cells"],
             "atlas": f"res://assets/{out.name}/{atlas.name}", "atlas_sha256": sortie.digest(atlas.read_bytes()),
             "passability": passability, "interaction": {"logic_hz":30,"move_interval":12,"delta_cap":0.2}}
    scene["formation_grid"] = [list(row[:3]) for row in struct.iter_unpack("<bbHH", bytes.fromhex(formation["grid_hex"]))]
    if scene_id in (93,94):
        data = json.dumps({"scene":scene, "skins":{}}, separators=(",",":")).encode()
        (out/"catalog.json").write_bytes(data)
        print(scene_id, scene["cell_size"], sortie.digest(data))
        return
    roster, skins = [], {}
    attack_rules = sortie.source_rules()
    sortie.PARENT_FRAMES = sortie.parent_frames(*([True]*12))
    for name in ("school_winter_jobs","school_winter_32","school_winter_44","school_winter_29",
                 "school_winter_45","school_eleven","school_thirty_three","school_dungeon_15","school_dungeon_16"):
        parent = json.loads((sortie.OUT.parent/name/"catalog.json").read_bytes())
        for skin in parent["skins"].values():
            for frame in skin["frames"].values():
                sortie.PARENT_FRAMES.setdefault(frame["file_sha256"], frame["file"])
    if scene_id != 71:
        actors = []
        rules = sortie.record_rules(scene_id, image)
        for ordinal, template in enumerate(rules["templates"]):
            record = sortie.expected_record(template, rules=rules)
            raw = bytes.fromhex(record["record_hex"])
            job = bytes.fromhex(rules["jobs"][str(record["job"])]["row_hex"])
            attack_id, = struct.unpack_from("<H", job, 24)
            attack = bytes.fromhex(rules["archetypes"][str(attack_id)]["row_hex"])
            actions = list(sortie.ACTIONS)
            if attack_id not in (0, 511):
                timing = image[0x611538-sortie.BASE+16*attack_id:][:3]
                names = ("cast", "attack", "recover")
                actions = [(name, timing[names.index(name)] if name in names else action) for name, action in actions]
            extra = {}
            if raw[0x96] == 2:
                actions += [("summon_prepare", 12), ("summon", 17)]
                extra["summon_interval"], = struct.unpack_from("<I", bytes.fromhex(template), 52)
            limits = {name: record[name+"_max"] for name in ("hp", "mp")}
            actors.append({"instance_id":1249-ordinal, "character_id":record["identity"],
                           "job":record["job"], "state":record["state"], "category":record["category"],
                           "cell":record["coordinates"], "record_hex":raw.hex(), "movement_type":raw[48],
                           "search_mode":bytes.fromhex(template)[0x24], "vision":raw[0x2c],
                           "skin_key":sortie.skin(record["identity"], record["job"], image, skins, out, actions, extend_actions=True),
                           "limits":{**limits,"hp_max":limits["hp"],"mp_max":limits["mp"]},
                           "combat":{**sortie.from_record(raw),"attack_id":attack_id,"attack_class":attack[5],"target_filter":attack[25]},
                           **extra})
        scene["actors"] = actors
        data = json.dumps({"scene":scene, "skins":skins}, ensure_ascii=False, separators=(",",":")).encode()
        (out/"catalog.json").write_bytes(data)
        print(scene_id, len(actors), sortie.digest(data))
        return
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
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("scene", type=int, choices=(42,43,71,93,94), default=71, nargs="?")
    export(parser.parse_args().scene)
