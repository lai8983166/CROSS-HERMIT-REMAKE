import struct,unittest
from copy import deepcopy
from tools.school_student_tail import *


def fixture():
    w=bytearray(STRIDE*COUNT);w[0]=1;struct.pack_into('<2i',w,0x2EC,336<<16,280<<16);w[0x4E7:0x4EB]=bytes([10,17,10,17])
    r=bytearray(176);r[15]=1;r[44]=9;struct.pack_into('<H',r,0xC,10);struct.pack_into('<6h',r,0x14,117,117,263,445,445,125)
    ctrl=bytearray(50);ctrl[4]=1;ctrl[24]=1;ctrl[26]=5
    data=[w,r,bytes(2048),bytes(6144),bytes(6144),bytes(12288),bytes(NODE*SLOTS),ctrl,bytes(400),struct.pack('<I',0xE080C7C)]
    names=['works','record','region_stats','fog_current','fog_history','occupancy','pool','control','task','current_work']
    rows=[{'name':n,'pointer':0x10000000+i*0x100000,'bytes':len(b),'hex':bytes(b).hex()} for i,(n,b) in enumerate(zip(names,data))]
    return {'team':0,'map_sha256':source_contract()['map_source']['sha256']},rows


class SourceTests(unittest.TestCase):
    def test_source_region_class_and_full_stationary_vision_projection(self):
        inputs,before=fixture();original=deepcopy(before);p=project(inputs,before);out={r['name']:bytes.fromhex(r['hex']) for r in p['after']}
        self.assertEqual(before,original);self.assertEqual(p['event_region'],0);self.assertEqual(p['event_class_mask'],16)
        self.assertEqual(out['region_stats'][:4],b'\1\0\x10\0');self.assertEqual(p['vision_args'],[10,17,9]);self.assertGreater(sum(out['fog_current']),255)
        self.assertEqual(out['fog_current'],out['fog_history']);self.assertEqual(p['actual_heals'],[]);self.assertTrue(p['first_unit_completed'])
        for n in ('record','pool','control','task','occupancy','current_work'):self.assertEqual(out[n],bytes.fromhex(next(r for r in before if r['name']==n)['hex']))

    def test_regen_native_threshold_special_state_wrap_and_zero_HP_rules(self):
        _,before=fixture();basework=bytes.fromhex(before[0]['hex'])[:STRIDE];baserecord=bytes.fromhex(before[1]['hex'])
        expected_heals=[[],[],[[0,1],[1,1]],[[0,1],[1,1]],[],[[1,1]]]
        for p,heals in zip(PROBES,expected_heals):
            w=bytearray(basework);r=bytearray(baserecord);r[15]=p['state'];put(r,0x16,117-p['hp_gap']);put(r,0x1C,445-p['mp_gap']);put(w,0x504,p['hp_counter']);put(w,0x506,p['mp_counter'])
            out=regen(w,r);self.assertEqual(out['heals'],heals)
            if p['hp_counter']==32767:self.assertEqual(get(bytes.fromhex(out['work_hex']),0x504),-32768)
            if p['hp_gap']==117:self.assertEqual(get(bytes.fromhex(out['record_hex']),0x16),0)

    def test_full_values_clear_counters_and_signed_negative_period_clamp(self):
        _,before=fixture();w=bytearray.fromhex(before[0]['hex'])[:STRIDE];r=bytearray.fromhex(before[1]['hex'])
        put(w,0x504,123);put(w,0x506,-1);out=regen(w,r);self.assertEqual(get(bytes.fromhex(out['work_hex']),0x504),0);self.assertEqual(get(bytes.fromhex(out['work_hex']),0x506),0)
        put(r,0x16,116);put(r,0x18,0);put(w,0x508,1);put(w,0x504,0);self.assertEqual(regen(w,r)['heals'],[[0,1]])

    def test_nonempty_event_damage_invalid_HP_and_moving_scope_refusals(self):
        inputs,before=fixture()
        for at in (0x48+0x34,0x48+0x40,0xA0+0x34,0x510,0x4E7):
            bad=deepcopy(before);w=bytearray.fromhex(bad[0]['hex']);w[at]=1;bad[0]['hex']=w.hex()
            with self.assertRaises(ValueError):project(inputs,bad)
        w=bytes.fromhex(before[0]['hex'])[:STRIDE];r=bytearray.fromhex(before[1]['hex']);put(r,0x16,118)
        with self.assertRaises(ValueError):regen(w,r)


if __name__=='__main__':unittest.main()
