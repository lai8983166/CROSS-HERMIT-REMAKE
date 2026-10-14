import struct,unittest
from tools.school_world_command import source_contract,normalize_selection,cell,project,STRIDE,COUNT


def fixture():
    works=bytearray(STRIDE*COUNT);records=[None]*COUNT
    for i,state,group in [(0,1,0),(1,0,0),(2,1,5),(3,0,5),(4,1,5)]:
        at=i*STRIDE;struct.pack_into('<h',works,at,1);works[at+0x28C]=1;works[at+0x290]=12 if i==4 else 2
        rec=bytearray(176);rec[15]=state;rec[164]=group;records[i]=bytes(rec)
        struct.pack_into('<2i',works,at+0x2EC,32<<16,16<<16);works[at+0x4E7:at+0x4EB]=bytes([1,1,7,8])
    return works,records


class SourceTests(unittest.TestCase):
    def test_source_identity_and_gates(self):
        s=source_contract();self.assertEqual(len(s['functions']),16)
        self.assertIn({'va':'0x46b7a6','hex':'e942020000','mnemonic':'jmp','operands':'0x46b9ed'},s['instructions'])

    def test_selection_priority_and_inactive_cleanup(self):
        works,records=fixture();out,rows,kind=normalize_selection(works,records,0)
        self.assertEqual((rows,kind),([0],1));self.assertEqual([out[i*STRIDE+0x28C] for i in range(5)],[1,0,0,0,0])
        works[0x28C]=0;out,rows,kind=normalize_selection(works,records,0);self.assertEqual((rows,kind),([1],2))
        works[STRIDE+0x28C]=0;out,rows,kind=normalize_selection(works,records,0);self.assertEqual((rows,kind),([2],3))
        self.assertEqual(out[3*STRIDE+0x28C],0);self.assertEqual(out[4*STRIDE+0x28C],0)
        works[2*STRIDE+0x28C]=0;self.assertEqual(normalize_selection(works,records,0)[1:],([],0))

    def test_cell_signed_truncation_and_invalid_full_inputs(self):
        for n in (-65,-33,-32,-31,-1,0,1,31,32,33,65):
            self.assertEqual(cell(n<<16,32),int(n/32))
        with self.assertRaises(ValueError):cell(0x80000000,32)
        with self.assertRaises(ValueError):normalize_selection(bytes(STRIDE),[None]*COUNT,0)

    def test_full_region_projection_and_refusal(self):
        works,records=fixture();base=0xE081000;matrix=bytearray(256);matrix[5]=1
        names=['queue','works','selection','cursor','scratch','fog_current','fog_history','occupancy','current_work']
        data=[bytes(20),works,bytes([0xCC])*1016,bytes([0xCC])*10,bytes([0xCC])*2048,bytes(6144),bytes(6144),bytes(12288),bytes([0xCC])*4]
        regions=[{'name':n,'pointer':0x500000+i*0x100000,'bytes':len(b),'hex':bytes(b).hex()} for i,(n,b) in enumerate(zip(names,data))]
        inputs={'gates':[1,0,0,0,0,0],'map_state':0,'task_mouse':[0,0,0],'ctrl_keys':[0,0],
          'record_hex':[r.hex() if r is not None else None for r in records],'team':0,'relations':matrix.hex(),'work_base':base}
        p=project(inputs,regions);after={r['name']:bytes.fromhex(r['hex']) for r in p['after']}
        self.assertEqual(p['occupied_indices'],list(range(5)));self.assertEqual(p['active_indices'],[0,2,4])
        self.assertEqual(p['vision_calls'],[{'index':0,'args':[1,1,0]}]);self.assertEqual(p['cell_changes'],[])
        self.assertEqual(after['cursor'],bytes(6)+b'\xff\xff'+bytes(2));self.assertFalse(any(after['scratch']))
        self.assertEqual(struct.unpack_from('<2I',after['selection']),(1,1));self.assertEqual(struct.unpack_from('<I',after['selection'],16)[0],base)
        self.assertEqual(after['selection'][20:],bytes([0xCC])*996);self.assertEqual(after['fog_current'][65],255)
        inputs['gates'][1]=1
        with self.assertRaises(ValueError):project(inputs,regions)
        inputs['gates'][1]=0;regions[0]['hex']=(bytes(16)+struct.pack('<I',1)).hex()
        with self.assertRaises(ValueError):project(inputs,regions)


if __name__=='__main__':unittest.main()
