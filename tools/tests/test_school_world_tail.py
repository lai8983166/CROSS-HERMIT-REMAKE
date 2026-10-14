import struct,unittest
from copy import deepcopy
from tools.school_world_tail import source_contract,idle_effects,project,EFFECT_STRIDE,SECONDARY_STRIDE


def fixture():
    effects=bytearray([0x57])*(EFFECT_STRIDE*10)
    for i in range(10):
        at=i*EFFECT_STRIDE;struct.pack_into('<I',effects,at+0x4C,0);struct.pack_into('<I',effects,at+0x68,0)
        struct.pack_into('<H',effects,at+10,65535 if i%2 else 32767)
    secondary=bytearray([0x79])*(SECONDARY_STRIDE*5)
    for i in range(5):secondary[i*SECONDARY_STRIDE]=0
    control=bytearray(50);struct.pack_into('<h',control,2,1);control[24]=1
    data=[bytes([0x37])*10,bytes([0x47])*20,b'\x57',effects,secondary,control,bytes(20),bytes(20),b'\0',b'\0']
    names=['cursor','window','menu','effects','secondary','control','outgoing_queue','incoming_queue','dispatch_mode','script_busy']
    regions=[{'name':n,'pointer':0x500000+i*0x100000,'bytes':len(b),'hex':bytes(b).hex()} for i,(n,b) in enumerate(zip(names,data))]
    return {'pointer_xy':[-1,-1],'selection_count':0},regions


class SourceTests(unittest.TestCase):
    def test_original_source_ten_slots_and_real_ret(self):
        s=source_contract();self.assertEqual(len(s['functions']),11)
        self.assertIn({'va':'0x46b662','hex':'c3','mnemonic':'ret','operands':''},s['instructions'])

    def test_idle_effect_short_wrap_and_preserved_animation(self):
        _,regions=fixture();before=bytes.fromhex(regions[3]['hex']);after=idle_effects(before)
        for i in range(10):
            at=i*EFFECT_STRIDE;self.assertEqual(after[at+4],1)
            self.assertEqual(struct.unpack_from('<H',after,at+10)[0],0 if i%2 else 32768)
            wanted=bytearray(before[at:at+EFFECT_STRIDE]);wanted[4]=1;wanted[10:12]=after[at+10:at+12]
            self.assertEqual(after[at:at+EFFECT_STRIDE],wanted)

    def test_full_buffers_closed_cursor_hover_secondary_and_queues(self):
        inputs,regions=fixture();before=deepcopy(regions);after=project(inputs,regions)
        self.assertEqual(regions,before)
        self.assertEqual(bytes.fromhex(after[0]['hex']),bytes([0x37])*8+b'\0'+b'\x37')
        self.assertEqual(bytes.fromhex(after[1]['hex']),bytes([0x47])*16+b'\0'+bytes([0x47])*3)
        self.assertEqual(after[2]['hex'],'00')
        for i in range(4,10):self.assertEqual(after[i],before[i])

    def test_nonempty_active_animation_secondary_and_gate_refusal(self):
        inputs,regions=fixture()
        for index,offset in [(3,0x4C),(3,0x68),(4,0),(5,24),(6,16),(7,16),(8,0),(9,0)]:
            bad=deepcopy(regions);buf=bytearray.fromhex(bad[index]['hex']);buf[offset]=1 if index!=5 else 0;bad[index]['hex']=buf.hex()
            with self.assertRaises(ValueError):project(inputs,bad)
        inputs['pointer_xy']=[0,0]
        with self.assertRaises(ValueError):project(inputs,regions)


if __name__=='__main__':unittest.main()
