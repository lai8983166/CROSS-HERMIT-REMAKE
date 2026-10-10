from copy import deepcopy
import json,struct,unittest
from tools.school_scene_unit_constructor_catalog import (
    source_catalog,native_fixture,expected_binding,expected_constructor,animation_inputs,ROOT)
from tools.school_scene_unit_constructor_emulation import scene_resource
from tools.school_scene_unit_work_catalog import expected_prefix,source_catalog as prefix_rules
from tools.dxanim_lib import DxAnimError


class SceneUnitConstructorSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.rules,cls.fixture=source_catalog(),native_fixture()

    def binding(self,a,**changes):
        args={'before_controller_hex':a['before_controller_hex'],
              'file_pointer':a['request']['buffer_pointer'],'metadata_pointer':a['metadata_pointer'],
              'texture_allocation':a['allocations'][2]['pointer'],'texture_table':a['texture_table'],
              'variant':a['variant'],'rules':self.rules['binding']}
        args.update(changes);return expected_binding(**args)

    def tail(self,c,**changes):
        t,a=c['scene_unit_constructor'],c['scene_unit_animation']
        args={k:t[k] for k in ('before_work_hex','record_hex','work_pointer','before_cm_hex')}
        args.update(controller_pointer=a['controller'],metadata_pointer=a['metadata_pointer'],rules=self.rules['constructor'])
        args.update(changes);return expected_constructor(**args)

    def test_native_controller_metadata_textures_pixels_palettes_and_release_against_source(self):
        animations=[c['scene_unit_animation'] for c in self.fixture['cases'][:3]]
        animations += [n['animation'] for n in self.fixture['declared_palette_diagnostic']['probes']]
        for a in animations:
            e=self.binding(a)
            for key in ('controller_hex','metadata_hex'):self.assertEqual(a[key],e[key])
            self.assertEqual(a['binding']['args'],e['binding_args'])
            self.assertEqual(a['file_release']['sha256_at_release'],e['source_sha256_at_release'])
            self.assertEqual(len(a['entries']),e['texture_count'])
            uploads=[n for n in a['boundaries'] if n['kind']=='pixel_upload']
            for actual,x,upload in zip(a['entries'],e['texture_entries'],uploads):
                for key in x:
                    if key!='upload_args':self.assertEqual(actual[key],x[key],(a['variant'],x['index'],key))
                self.assertEqual(upload['args'],x['upload_args'])

    def test_complete_work_record_shared_and_cell_from_independent_prefix_and_tail(self):
        r=prefix_rules()
        for c in self.fixture['cases'][:3]:
            p,t=c['scene_unit_work'],c['scene_unit_constructor']
            prefix=expected_prefix(p['before_record_hex'],0,p['cache_before_hex'],p['counter_before'],
                p['renderer'],p['allocation']['pointer'],p['classification_selector'],p['relation_hex'],r)
            for key in ('work_hex','record_hex','cache_hex','controller_hex','counter','cache_slot'):
                self.assertEqual(prefix[key],p[key],key)
            self.assertEqual(prefix['work_hex'],t['before_work_hex']);self.assertEqual(prefix['record_hex'],t['record_hex'])
            self.assertEqual(prefix['controller_hex'],c['scene_unit_animation']['before_controller_hex'])
            e=self.tail(c)
            for key in ('work_hex','record_hex','shared_hex','cm_hex','cm_sha256','constructor_coordinates'):
                self.assertEqual(t[key],e[key],key)
            self.assertEqual([e[k] for k in ('action','direction','mapped_direction','block','animation','flags','descriptor_index')],
                             [1,2,1,0,4,0,579])
            self.assertEqual(e['fixed_coordinates'],[((52<<5)+16)<<16,((65<<4)+8)<<16])

    def test_visible_descriptor_original_program_and_cell_wrap_coordinates(self):
        c=self.fixture['cases'][0];r=self.rules['constructor']
        self.assertEqual(r['programs'][0][4][0]['raw'],'800043fffffff2ff2800')
        self.assertEqual(r['programs'][0][4][0]['descriptors'],[579,4095,4095,4095])
        layers=r['initial_program']['visible_layers']
        self.assertEqual(len(layers),1)
        self.assertEqual([layers[0][k] for k in ('descriptor','frame','x','y','draw_group')],[579,36,2,-38,7])
        e=self.tail(c);descriptor=bytes.fromhex(r['descriptor_hex'])[579*10:580*10]
        self.assertEqual(struct.unpack_from('<I',bytes.fromhex(e['work_hex']),0x60)[0],descriptor[8])
        cm=bytearray.fromhex(c['scene_unit_constructor']['before_cm_hex']);cm[2*(65*64+52)+1]=255
        self.assertEqual(bytes.fromhex(self.tail(c,before_cm_hex=cm.hex())['cm_hex'])[2*(65*64+52)+1],0)
        record=bytearray.fromhex(c['scene_unit_constructor']['record_hex']);record[0x9B:0x9D]=bytes([63,95])
        e=self.tail(c,record_hex=record.hex());self.assertEqual(e['constructor_coordinates'],[63,95])
        self.assertEqual(bytes.fromhex(e['cm_hex'])[-1],1)

    def test_malformed_archives_and_unsupported_binding_or_constructor_inputs_rejected(self):
        raw,_,_=scene_resource(4,5);offsets=self.rules['binding']['animation']['sections']
        bad=bytearray(raw);bad[offsets[8]['offset']]=2
        bad_bmp=bytearray(raw);at=offsets[6]['offset']+self.rules['binding']['animation']['texture_entries'][0]['offset'];bad_bmp[at:at+2]=b'XX'
        for data in (b'',raw[:20],raw[:-1],bytes(bad),bytes(bad_bmp)):
            with self.assertRaises((ValueError,DxAnimError)):animation_inputs(data)
        c=self.fixture['cases'][0];a=c['scene_unit_animation']
        for variant in (0,41,True,'5'):
            with self.assertRaises(ValueError):self.binding(a,variant=variant)
        for pointer in (0,-4,True,'4',3,0xFFFFFFFF):
            with self.assertRaises(ValueError):self.binding(a,file_pointer=pointer)
            with self.assertRaises(ValueError):self.tail(c,work_pointer=pointer)
        for key in ('before_work_hex','record_hex','before_cm_hex'):
            for value in (None,'zz','00'):
                with self.assertRaises(ValueError):self.tail(c,**{key:value})
        with self.assertRaises(ValueError):self.binding(a,metadata_pointer=a['request']['buffer_pointer'])
        for at,value in ((2,6),(12,10),(0xA4,3),(0xF,0),(0x9B,64),(0x9C,96)):
            record=bytearray.fromhex(c['scene_unit_constructor']['record_hex']);record[at]=value
            with self.assertRaises(ValueError):self.tail(c,record_hex=record.hex())
        rules=deepcopy(self.rules['constructor']);rules['programs'][0][4][0]['opcode']=1
        with self.assertRaises(ValueError):self.tail(c,rules=rules)
        rules=deepcopy(self.rules['constructor']);rules['position_words'][4]=0xFFFF
        with self.assertRaises(ValueError):self.tail(c,rules=rules)

    def test_rules_and_frozen_evidence_exports_separate_and_exact(self):
        rules=json.loads((ROOT/'prototype/data/school_scene_unit_constructor_rules.json').read_text('utf-8'))
        fixture=json.loads((ROOT/'prototype/data/school_scene_unit_constructor_evidence.json').read_text('utf-8'))
        self.assertEqual(rules,self.rules);self.assertEqual(fixture,self.fixture)
        self.assertNotIn('cases',rules);self.assertNotIn('binding',fixture)
        saved=deepcopy(rules);fixture['cases'][0]['scene_unit_constructor']['work_hex']=''
        self.assertEqual(saved,rules)


if __name__=='__main__':unittest.main()
