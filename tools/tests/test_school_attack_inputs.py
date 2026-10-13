import json
import struct
import unittest
from copy import deepcopy
from tools.school_attack_inputs import ROOT, project, from_record, source_rules, snapshot_bytes, scalar_damage


def packet(raw):
    raw=bytes.fromhex(raw)
    return {'power':int.from_bytes(raw[:2],'little'),'power_range':int.from_bytes(raw[2:4],'little'),
        'accuracy':int.from_bytes(raw[4:6],'little'),'evasion':raw[8],'armor':raw[9],
        'magic_resist':raw[10],'magic_body':raw[11],
        'evasion_coefficient':struct.unpack_from('<i',raw,16)[0],'armor_coefficient':struct.unpack_from('<i',raw,20)[0],
        'body_coefficient':struct.unpack_from('<i',raw,24)[0],'magic_modifier':0}


class AttackInputTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rules=source_rules()
        cls.old=json.loads((ROOT/'prototype/data/school_combat_records_evidence.json').read_text('utf-8'))
        cls.native=json.loads((ROOT/'analysis/school-night-attack-probe-v3-20261014.json').read_text('utf-8'))

    def test_source_current_fields_match_all_original_cases_and_clamp_probes(self):
        cases=self.old['cases']+[{'combat_records':[v['record'] for v in self.old['counterfactuals']]}]
        for case in cases:
            for row in case['combat_records']:
                expected=project(row['input'],self.rules)
                original=from_record(bytes.fromhex(row['raw_record_hex']))
                self.assertEqual({k:expected[k] for k in original},original)
        self.assertEqual(self.native['source_rules'],self.rules)
        self.assertEqual(json.loads((ROOT/'prototype/data/school_attack_inputs_rules.json').read_text('utf-8')),self.rules)

    def test_entire_actual_current_snapshot_bytes_and_retained_native_units(self):
        for case in self.native['cases']:
            inputs=next(c['combat_records'] for c in self.old['cases'] if c['name']==case['name'])
            for snap in case['actual_current_snapshots']:
                source=next(c['input'] for c in inputs if c['input']['character_id']==snap['character_id'])
                result=project(source,self.rules)
                self.assertEqual(snapshot_bytes(result,snap['terrain'],rules=self.rules).hex(),snap['snapshot_hex'])
                self.assertTrue(snap['condition_slots_zero'] and snap['retained_ranges_unchanged'])
                self.assertFalse(snap['world_or_HP_application_executed'])

    def test_all_original_scalar_results_and_random_consumption(self):
        for p in self.native['declared_scalar_probes']:
            attack,defense=packet(p['attack_hex']),packet(p['defense_hex'])
            self.assertEqual(scalar_damage(attack,defense,p['declared_rolls'],p['magic']),p['damage'])
            count=0 if p['magic'] else 1
            if attack['power_range'] and (p['magic'] or p['damage']>=0): count+=1
            self.assertEqual(len(p['roll_calls']),count)
            self.assertTrue(p['input_packets_unchanged']); self.assertFalse(p['HP_applied'])

    def test_wrong_role_job_items_attributes_and_terrain_refuse(self):
        source=self.old['cases'][0]['combat_records'][0]['input']
        for key,value in [('character_id',101),('job',6),('equipped_items',[1]*8),('attributes',[1]*6),('attributes',[True]*7),('attributes',[256]*7)]:
            bad=deepcopy(source);bad[key]=value
            with self.assertRaises(ValueError):project(bad,self.rules)
        for terrain,mode in [(-1,0),(100,0),(1,5)]:
            with self.assertRaises(ValueError):snapshot_bytes(project(source,self.rules),terrain,mode,self.rules)


if __name__=='__main__':unittest.main()
