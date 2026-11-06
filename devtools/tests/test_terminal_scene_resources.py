"""Resource adapter tests use byte maps only; never start a game or call WinAPI."""
from contextlib import contextmanager
import struct
import types
import unittest
from devtools import terminal_scene_resources as r


def put(data,offset,value):struct.pack_into('<I',data,offset,value)


class Memory:
    def __init__(self):self.regions={};self.calls=[];self.require_paused=None
    def add(self,pointer,data):self.regions[pointer]=bytearray(data)
    def get(self,pointer,size):
        if self.require_paused is not None:
            if not self.require_paused():raise AssertionError('read outside original pause')
        self.calls.append((pointer,size))
        for start,data in self.regions.items():
            if start<=pointer and pointer+size<=start+len(data):return bytes(data[pointer-start:pointer-start+size])
        raise ValueError('unreadable simulated region')


def fixture(texture=0x300000):
    m=Memory();game=0x100000;renderer=game+0x1058;node=0x210000;desc=0x220020
    m.add(0x7A49FC,struct.pack('<I',game));rh=bytearray(0x38)
    put(rh,4,0x400000);put(rh,8,1);put(rh,0x10,0x200000);put(rh,0x14,0x210000)
    m.add(renderer,rh);m.add(0x200000,struct.pack('<2I',node,0))
    nh=bytearray(0x5C);put(nh,4,1);put(nh,0x50,desc);m.add(node,nh)
    dh=bytearray(0xA0);put(dh,0x10,0x80);put(dh,0x14,1);dh[0x1C:0x20]=b'\xfd'*4
    put(dh,0x20+0x2C,texture);m.add(desc-0x20,dh)
    stack=bytearray(0x1000);sp=0x500000;m.add(sp,stack)
    # Rows describe callee EBP at the saved return sites, not caller EBP.
    bind_bp=sp+0x300;draw_bp=sp+0x500;d3d_bp=sp+0x200;render_bp=sp+0x700
    for at,value in ((bind_bp-4,renderer),(bind_bp+8,texture),(draw_bp-4,renderer),
        (draw_bp-8,node),(draw_bp+8,node),(draw_bp-0x8C,desc),(d3d_bp+8,0x400000),
        (d3d_bp+12,0),(d3d_bp+16,texture),(render_bp-12,0)):
        put(m.regions[sp],at-sp,value)
    frames=[dict(tid=11,ESP=sp+0x100,EBP=d3d_bp,EIP=0x6F51D8E8,chain=[
        dict(bp=d3d_bp,saved_bp=bind_bp,return_va=0x40E24A),
        dict(bp=bind_bp,saved_bp=draw_bp,return_va=0x40EA11),
        dict(bp=draw_bp,saved_bp=render_bp,return_va=0x40E573),
        dict(bp=render_bp,saved_bp=sp+0x800,return_va=0x49E6DE)])]
    return m,frames,dict(game=game,renderer=renderer,node=node,desc=desc,sp=sp)


class ReaderTests(unittest.TestCase):
    def test_poison_and_derived_poison_never_reach_reader(self):
        m=Memory();reader=r.Reader(m.get)
        for pointer in (0,0xDDDDDDDD,0xDDDDDD8D,0xCDCDCDCD,0xCCCCCCCC,0xFEEEFEEE,-1,0xFFFFFFFF):
            self.assertEqual(reader.read(pointer,4,'bad')['status'],'invalid_pointer')
        self.assertEqual(m.calls,[])

    def test_address_overflow_and_alignment(self):
        m=Memory();reader=r.Reader(m.get)
        for pointer,size,alignment in ((0xFFFFFFFC,8,4),(0x10001,4,4),(0xFFFF,4,1),(0x10000,4097,1)):
            self.assertEqual(reader.read(pointer,size,'bounds',alignment)['status'],'invalid_pointer')
        self.assertFalse(m.calls)

    def test_budget_refuses_before_backend(self):
        m=Memory();m.add(0x10000,bytes(32));reader=r.Reader(m.get,max_bytes=8,max_calls=2)
        self.assertEqual(reader.read(0x10000,4,'a')['status'],'readable')
        self.assertEqual(reader.read(0x10004,4,'b')['status'],'readable')
        self.assertEqual(reader.read(0x10008,4,'c')['status'],'budget')
        self.assertEqual(len(m.calls),2)

    def test_unreadable_is_evidence_not_native_argument(self):
        reader=r.Reader(Memory().get)
        self.assertEqual(reader.read(0x11000,32,'missing')['status'],'unreadable')

    def test_short_read_rejected(self):
        self.assertEqual(r.Reader(lambda p,n:b'x').read(0x10000,4,'short')['status'],'short_read')


class CaptureTests(unittest.TestCase):
    def test_valid_descriptor_does_not_claim_complete_lifetime(self):
        m,f,_=fixture();out=r.collect_resources(m,f,11)
        self.assertFalse(out['fault_proved']);self.assertFalse(out['all_heap_traversed'])
        self.assertFalse(out['texture_pixels_read']);self.assertFalse(out['queue']['complete_graph'])
        self.assertLessEqual(out['read_budget']['bytes_requested'],r.MAX_READ_BYTES)

    def test_actual_poison_arguments_stop_candidate(self):
        m,f,a=fixture(0xDDDDDDDD);out=r.collect_resources(m,f,11)
        self.assertTrue(out['fault_proved']);self.assertEqual(out['fault']['value'],0xDDDDDDDD)
        self.assertEqual(out['current_call']['node']['descriptor']['texture'],0xDDDDDDDD)
        self.assertFalse(any(abs(p-0xDDDDDDDD)<256 for p,n in m.calls))

    def test_null_texture_is_legal_unbind_not_failure(self):
        m,f,_=fixture(0);self.assertFalse(r.collect_resources(m,f,11)['fault_proved'])

    def test_descriptor_link_records_agreement(self):
        m,f,_=fixture(0xDDDDDDDD);out=r.collect_resources(m,f,11)
        link=out['fault']['descriptor_argument_link']
        self.assertTrue(link['texture_matches_argument']);self.assertTrue(link['saved_local_matches_node'])

    def test_unreadable_descriptor_not_claimed_same_source(self):
        m,f,a=fixture(0xDDDDDDDD);del m.regions[a['desc']-0x20]
        out=r.collect_resources(m,f,11)
        self.assertTrue(out['fault_proved'])
        self.assertIsNone(out['fault']['descriptor_argument_link']['texture_matches_argument'])

    def test_changed_descriptor_records_mismatch_without_concealing_bad_argument(self):
        m,f,a=fixture(0xDDDDDDDD);put(m.regions[a['desc']-0x20],0x20+0x2C,0x300000)
        out=r.collect_resources(m,f,11)
        self.assertTrue(out['fault_proved']);self.assertFalse(out['fault']['descriptor_argument_link']['texture_matches_argument'])

    def test_runtime_fill_values_are_not_static_code_identity(self):
        m,f,_=fixture();m.add(0x7619CC,b'\xaa\xbb')
        out=r.collect_resources(m,f,11)
        self.assertEqual(out['CRT_runtime_fill_bytes']['hex'],'aabb')
        self.assertFalse(any(a<=0x7619CC<b for a,b in r.RESOURCE_RANGES))

    def test_missing_active_d3d_frame_prevents_false_failure(self):
        m,f,_=fixture(0xDDDDDDDD);f[0]['chain']=f[0]['chain'][1:]
        self.assertFalse(r.collect_resources(m,f,11)['fault_proved'])

    def test_mismatched_recorded_arguments_not_proved(self):
        m,f,a=fixture(0xDDDDDDDD);put(m.regions[a['sp']],0x210,0x300000)
        self.assertFalse(r.collect_resources(m,f,11)['fault_proved'])

    def test_poison_game_pointer_not_arithmetically_dereferenced(self):
        m=Memory();m.add(0x7A49FC,struct.pack('<I',0xDDDDDDDD))
        out=r.collect_resources(m,[],11)
        self.assertEqual(out['status'],'game_unreadable');self.assertEqual(m.calls,[(0x7619CC,2),(0x7A49FC,4)])

    def test_queue_cycle_is_bounded_and_explicit(self):
        m,f,a=fixture();put(m.regions[a['node']],0,a['node'])
        out=r.collect_resources(m,f,11)
        self.assertEqual(out['queue']['status'],'cycle_or_shared_node');self.assertFalse(out['fault_proved'])

    def test_queue_node_cap(self):
        m,f,a=fixture()
        for i in range(9):
            b=bytearray(0x5C);put(b,0,a['node']+(i+1)*0x100 if i<8 else 0)
            put(b,4,2);m.add(a['node']+i*0x100,b)
        out=r.collect_resources(m,f,11)
        self.assertEqual(out['queue']['status'],'node_budget');self.assertEqual(len(out['queue']['nodes']),r.MAX_NODES)

    def test_invalid_bucket_count_and_base(self):
        for offset,value,status in ((8,5000,'invalid_bucket_count'),(0x10,0xDDDDDDDD,'invalid_bucket_base')):
            m,f,a=fixture();put(m.regions[a['renderer']],offset,value)
            self.assertEqual(r.collect_resources(m,f,11)['queue']['status'],status)

    def test_crt_layout_size_is_10_block_is_14(self):
        m=Memory();head=bytearray(32);put(head,8,0x20000);put(head,12,123)
        put(head,16,0x80);put(head,20,1);put(head,24,456);head[28:32]=b'\xfd'*4
        m.add(0x10000,head);m.add(0x20000,b'example.cpp\0'+bytes(52))
        out=r.crt_header(r.Reader(m.get),0x10020,'test')
        self.assertEqual(out['fields']['data_size'],128);self.assertEqual(out['fields']['block_use'],1)
        self.assertEqual(out['file_prefix_text'],'example.cpp');self.assertTrue(out['file_name_complete'])
        self.assertFalse(out['allocation_base_proved'])

    def test_dd_header_never_follows_poisoned_file_link(self):
        m=Memory();m.add(0x10000,b'\xdd'*32)
        out=r.crt_header(r.Reader(m.get),0x10020,'dd')
        self.assertTrue(out['all_DD']);self.assertFalse(out['plausible_debug_header']);self.assertEqual(len(m.calls),1)

    def test_producer_alternate_descriptor_rule(self):
        m,f,a=fixture();sprite=0x230020;data=bytearray(0xA0)
        put(data,0x20+0x48,a['desc']);struct.pack_into('<H',data,0x20+0x58,0x80);m.add(sprite-32,data)
        producer_bp=a['sp']+0x900;put(m.regions[a['sp']],0x8FC,sprite);put(m.regions[a['sp']],0x8F8,a['node'])
        f.append(dict(tid=12,EIP=0x408080,EBP=producer_bp,ESP=a['sp']+0x800,chain=[]))
        out=r.collect_resources(m,f,11)
        self.assertEqual(out['producer_selections'][0]['selected_descriptor'],a['desc'])

    def test_source_contract_pins_original_bytes(self):
        raw=(r.ROOT/'analysis/hermit_game.exe').read_bytes();contract=r.source_contract(raw)
        self.assertEqual(contract['CRT_header']['block_use_offset'],20)
        changed=bytearray(raw);changed[0xE244]^=1
        with self.assertRaises(ValueError):r.source_contract(bytes(changed))


def base_sample(c,owned,hwnd,main_tid,worker_tid,node,worker_exited=False):
    # The injected name intentionally comes from clone's globals.
    with original.frozen(c,1,[main_tid]) as frames:
        return dict(index=0,frames=frames,base_body_observed_pause=owned['paused'])


class InjectionTests(unittest.TestCase):
    def sample(self,texture,hook=None):
        m,frames,_=fixture(texture);state={'paused':False};m.require_paused=lambda:state['paused']
        @contextmanager
        def frozen(*args):
            state['paused']=True
            try:yield frames
            finally:state['paused']=False
        original=types.SimpleNamespace(frozen=frozen)
        failure={};source=lambda c:dict(extra_live_identity_while_paused=state['paused'])
        fn=r.make_sampler(base_sample,original,failure,source,hook)
        return fn,m,state,failure

    def test_capture_inside_one_pause_and_hook_only_after_resume(self):
        seen=[]
        def hook(c,owned,hwnd,row):
            seen.append(owned['paused']);self.assertIn('resources',row);return {'bounded_handoff':True}
        fn,m,state,_=self.sample(0x300000,hook)
        row=fn(m,state,0,11,None,None)
        self.assertTrue(row['base_body_observed_pause']);self.assertEqual(seen,[False])
        self.assertFalse(state['paused']);self.assertTrue(row['post_sample_handoff']['bounded_handoff'])

    def test_first_bad_resource_saves_sample_resumes_and_skips_hook(self):
        seen=[];fn,m,state,failure=self.sample(0xDDDDDDDD,lambda *x:seen.append('input'))
        with self.assertRaises(r.ResourceDependencyError):fn(m,state,0,11,None,None)
        self.assertFalse(state['paused']);self.assertFalse(seen)
        self.assertTrue(failure['failure_sample']['resources']['fault_proved'])
        self.assertTrue(failure['source_after']['extra_live_identity_while_paused'])

    def test_bound_method_hook_runs_after_resume(self):
        class Hook:
            def observe(self,c,owned,hwnd,row):return {'paused':owned['paused']}
        fn,m,state,_=self.sample(0x300000,Hook().observe)
        self.assertFalse(fn(m,state,0,11,None,None)['post_sample_handoff']['paused'])


if __name__=='__main__':unittest.main()
