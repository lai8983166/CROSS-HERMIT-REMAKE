import struct
import unittest
from types import SimpleNamespace

from tools import terminal_unit_frontends_emulation as source
from tools import terminal_replacement_emulation as replacement
from tools import terminal_multiline_emulation as multiline
from tools import terminal_last_dialogue_emulation as last
from tools.terminal_unit_frontends_projection_verification import Projection,POINTER,BITS


class RAM:
    def __init__(self):self.words={};self.budget_stop=False
    def read(self,address,size):
        if size!=4:raise AssertionError('word fixture only')
        return struct.pack('<I',self.words.get(address,0))


class ProjectionGuards(unittest.TestCase):
    def test_original_portrait_registration_groups_keep_their_call_lifetime(self):
        for group in (20,30,31,32,90):
            p=Projection(source.previous.overlay.parent.corpus()[0]);r=RAM()
            sp=0x12008000
            r.cpu=lambda:dict(ESP=sp)
            r.words.update({sp:source.previous.RETURN,sp+8:group})
            p.observe(r,0x416790)
            self.assertEqual(p.resource_stack[-1]['group'],group)
            r.cpu=lambda:dict(ESP=sp+12)
            p.observe(r,source.previous.RETURN)
            self.assertEqual(p.resource_stack,[])
        p=Projection(source.previous.overlay.parent.corpus()[0]);r=RAM()
        r.cpu=lambda:dict(ESP=0x12008000)
        r.words[0x12008008]=40
        with self.assertRaises(ValueError):p.observe(r,0x416790)

    def test_current_original_vm_pc_and_record_select_namespace(self):
        for case in source.previous.overlay.parent.corpus():
            p=Projection(case);r=RAM()
            branch=replacement.branch(case['name'])
            for i,pc in enumerate(branch['text_PCs']):
                r.words[source.previous.VM+28]=pc
                record=replacement.TEXTURE+i*replacement.STRIDE
                self.assertEqual(p.domain(r,record),'overlay-replacement-'+str(i))
                with self.assertRaises(ValueError):p.domain(r,record+4)
            for module,prefix in ((multiline,'overlay-multiline-'),(last,'overlay-last-dialogue-')):
                for i,line in enumerate(module.branch(case['name'])['lines']):
                    r.words[source.previous.VM+28]=line['PC']
                    record=module.record_at(line['layer'],line['record_index'])
                    self.assertEqual(p.domain(r,record),prefix+str(i))
                    with self.assertRaises(ValueError):p.domain(r,record+4)

    def test_new_guest_identity_is_recomputed_and_not_reallocated(self):
        p=Projection(source.previous.overlay.parent.corpus()[0])
        p.bridge=SimpleNamespace(overlay_next=0x66001000)
        p.expected='overlay-replacement-0'
        self.assertTrue(p.approve(p.expected,123,0x66001000))
        self.assertEqual(p.bridge.overlay_next,0x66101000)
        self.assertTrue(p.approve(p.expected,123,0x66001000))
        self.assertEqual(p.bridge.overlay_next,0x66101000)
        self.assertFalse(p.approve(p.expected,123,0x66101000))
        self.assertFalse(p.approve(p.expected,124,0x66001000))
        self.assertFalse(p.approve('arbitrary',124,0x66101000))

    def test_retired_surface_alias_requires_exact_actual_released_owner(self):
        p=Projection(source.previous.overlay.parent.corpus()[1]);p.expected=POINTER
        with self.assertRaises(ValueError):p.approve(BITS,123,0x65001000)
        from tools.terminal_followup_emulation import OLD_TEXT_RECORD
        p.retired=[dict(record=OLD_TEXT_RECORD,width=128,height=32,pitch=256,length=8192,
                        domain='overlay',bits=0x65001000)]
        self.assertFalse(p.approve(BITS,123,0x65101000))
        self.assertTrue(p.approve(BITS,123,0x65001000))


if __name__=='__main__':unittest.main()
