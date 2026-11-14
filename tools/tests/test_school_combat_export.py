import json
import struct
import tempfile
import unittest
from pathlib import Path
from PIL import Image
from tools.school_combat_export import source_inputs, export, OUTPUT, ROOT, digest, ACTIONS
from tools.school_attack_inputs import from_record


class CombatExportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.catalog,cls.images=source_inputs()

    def test_initial_activity_positions_fields_match_original_work_records(self):
        native=json.loads((ROOT/'prototype/data/school_formation_placement_evidence.json').read_text('utf-8'))
        for case in native['cases'][:3]:
            rows={u['index']:u for u in case['formation_placement']['units']}
            for actor in self.catalog['actors']:
                unit=rows[actor['work_index']];record=bytes.fromhex(unit['record_hex']);work=bytes.fromhex(unit['work_hex'])
                self.assertEqual(actor['character_id'],int.from_bytes(record[2:4],'little'))
                self.assertEqual(actor['category'],record[164]);self.assertEqual(record[15],1)
                self.assertEqual(actor['cell'],list(work[1255:1257]))
                self.assertEqual({k:actor['combat'][k] for k in from_record(record)},from_record(record))
                self.assertEqual(actor['limits']['hp'],int.from_bytes(record[20:22],'little'))
        self.assertEqual(len(self.catalog['actors']),11)
        self.assertEqual(len({a['instance_id'] for a in self.catalog['actors']}),11)
        self.assertEqual([a['ordinal'] for a in self.catalog['actors']],[0,1,2,3,4,5,6,7,8,9,32])

    def test_complete_directional_attack_programs_and_source_pixel_frames(self):
        for key,skin in self.catalog['skins'].items():
            expected={'idle'} if key.startswith('scene_') and not key.startswith('scene_383_') else {a[0] for a in ACTIONS}
            self.assertEqual(set(skin['actions']),expected)
            self.assertEqual(skin['palette_variant'],{'3':3,'4':4,'9':2,'scene_4_v5':5,'scene_383_v1':1}.get(key,0))
            for directions in skin['actions'].values():
                self.assertEqual(len(directions),8)
                for program in directions.values():
                    for step in program['steps']:
                        for layer in step['layers']:self.assertIn(str(layer['frame']),skin['frames'])
            for frame in skin['frames'].values():self.assertEqual(digest(self.images[frame['file']].tobytes()),frame['rgba_sha256'])

    def test_checked_in_export_is_deterministic_complete_and_source_only(self):
        checked=json.loads((OUTPUT/'catalog.json').read_text('utf-8'))
        with tempfile.TemporaryDirectory() as directory:
            result=export(Path(directory));self.assertEqual(result,checked)
            for skin in result['skins'].values():
                for frame in skin['frames'].values():
                    rel=frame['file'].removeprefix('res://assets/school_combat/')
                    p=OUTPUT/rel
                    self.assertEqual(p.read_bytes(),(Path(directory)/rel).read_bytes())
                    self.assertEqual(digest(p.read_bytes()),frame['file_sha256'])
                    with Image.open(p) as image:self.assertEqual(digest(image.tobytes()),frame['rgba_sha256'])
        self.assertFalse(checked['trial_policy']['victory_or_reward_authority'])

    def test_reinforcements_reuse_source_records_art_dialogue_and_mask(self):
        from tools.ybc32_disasm import parse, load_pool
        from tools.school_map_common_emulation import map_common_resource
        target=ROOT/'prototype/assets/school_reinforcements'
        checked=json.loads((target/'catalog.json').read_text('utf-8'))
        with tempfile.TemporaryDirectory() as directory:
            result=export(Path(directory),reinforcements=True)
            self.assertEqual(result,checked)
            for skin in result['skins'].values():
                for frame in skin['frames'].values():
                    rel=frame['file'].removeprefix('res://assets/school_reinforcements/')
                    self.assertEqual((target/rel).read_bytes(),(Path(directory)/rel).read_bytes())
                    with Image.open(target/rel) as image:
                        self.assertEqual(digest(image.tobytes()),frame['rgba_sha256'])
        records=[bytes.fromhex(a['record_hex']) for a in checked['actors']]
        self.assertEqual(len(records),24)
        self.assertTrue(all(r[15]==0 for r in records))
        self.assertEqual([sum(r[0x98]==g for r in records) for g in range(1,7)],[9,3,3,3,3,3])
        boss=next(a for a in checked['actors'] if a['work_index']==239)
        self.assertEqual(boss['character_id'],452)
        initial=json.loads((OUTPUT/'catalog.json').read_text('utf-8'))['skins']['scene_4_v5']
        self.assertEqual(checked['skins']['scene_4_v5']['source'],initial['source'])
        self.assertEqual(checked['skins']['scene_4_v5']['palette_variant'],5)
        script=(ROOT/'CROSS HERMIT/CROSS HERMIT/DATA/TACTICS/SCRIPT/T0005.BIN').read_bytes()
        pool=next(r[3] for r in parse(script) if r[:2]==(0,20))
        strings=load_pool(script,pool)
        texts=[p for page in checked['event20_dialogue'] for p in page]
        self.assertEqual([p['text_index'] for p in texts],list(range(58)))
        for page in texts:
            self.assertEqual(page['text'],strings[page['text_index']][2])
            self.assertEqual(struct.unpack_from('<3H',script,page['source_offset']),(17,6,page['text_index']))
        mask=checked['capture_mask'];common,identity=map_common_resource()
        self.assertEqual(mask['source'],identity)
        self.assertEqual(common[344:344+121].hex(),mask['hex'])
        exe=(ROOT/'analysis/hermit_game.exe').read_bytes()
        self.assertEqual(list(exe[0x19558c+10:0x19558c+12]),[mask['width'],mask['height']])


if __name__=='__main__':unittest.main()
