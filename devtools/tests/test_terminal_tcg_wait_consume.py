"""Synthetic offline acceptance and tamper rejection; no native execution."""
from copy import deepcopy
import hashlib
from pathlib import Path
import struct
import unittest

from devtools import terminal_tcg_wait_consume as c
from devtools.terminal_tcg_compat_context import pack, source_digest
from devtools.terminal_tcg_canonical57_v2 import DR_POLICY


def hx(v):
    return f'{v:016x}'


def raw():
    seg = [[hx(16), hx(0), hx(0xffffffff), hx(0xcf9300)] for _ in range(10)]
    seg[1] = [hx(8), hx(0), hx(0xffffffff), hx(0xcf9b00)]
    seg[4][1] = hx(0x700000)
    for i in (8, 9):
        seg[i][2] = hx(0xffff)
    return dict(schema='tcg-state-v1', fullstate_accepted=False,
        vp_stopped=[dict(cpu=i, stopped=True) for i in range(2)], cpu=0, target_bits=64,
        gpr=[hx(0)]*16, eip=hx(0), eflags=hx(0x202), hflags=hx(0x4042b0), efer=hx(0x500),
        segments_es_cs_ss_ds_fs_gs_ldt_tr_gdt_idt=seg,
        cr0_cr2_cr3_cr4=list(map(hx, (0x80000033, 0, 0x101000, 0x620))),
        dr0_dr1_dr2_dr3_dr6_dr7=[hx(0)]*6, dr4_dr5_policy=DR_POLICY,
        fp_control=895, fp_status=7 << 11, top=7, fp_empty_mask=127, fop=4, fcs=0, fds=0,
        fip=hx(0x10010039f), fdp=hx(0x100100904), mxcsr=0x1f80,
        fp_physical_low64_high16=[[hx(i+1), hx(0x4000)] for i in range(8)],
        xmm_low64_high64=[[hx(i+10), hx(i+20)] for i in range(16)])


def sample():
    template, meta = c.image()
    ready = dict(pid=123, tid=456, data=0x200000, code=0x100000, nt_wait=0x300000,
        event_handle=1234, timeout_pointer=0x400000,
        source_sha256=hashlib.sha256(Path(c.__file__).with_name('terminal_tcg_wait_fixture_v2.cs').read_bytes()).hexdigest(),
        template_sha256=hashlib.sha256(template).hexdigest(), fixture_version=2,
        counter_startup_confirmed=True, counter_native_started=False,
        peer_request_wait_started=False, workers_gated_until_go=True)
    ready.update(postcall_pc=ready['code']+meta['postcall_offset'], return_pc=ready['nt_wait']+12)
    machine = bytearray(template)
    for p in meta['patches']:
        struct.pack_into('<I', machine, p['offset'], ready[p['symbol']]+p['addend'])
    ready['code_hex'] = machine.hex()
    ready['nt_wait_before'] = (bytes.fromhex('b804000d00ba11223344ffd2c20c00')+bytes(17)).hex()
    result = dict(accepted=False, original_game_observed=False, kind='owned_wow64_tcg_wait_fixture', ready=ready,
        template_sha256=ready['template_sha256'], source_sha256=ready['source_sha256'], code_after=machine.hex(),
        nt_wait_before=ready['nt_wait_before'], nt_wait_after=ready['nt_wait_before'], returns=[0, 0, 0, 258],
        signals=3, peer_completed=True, peer_error=None, error=None, go_received=True, counter_native_entered=[True, True],
        cleanup_errors=[], counter_errors=[None, None], counter_affinity_restored=[True, True])
    for k in ('fixture_completed', 'workers_stopped', 'handles_closed', 'buffers_released', 'main_affinity_restored', 'watchdog_disarmed'):
        result[k] = True
    observation = dict(accepted=False, ready=ready, errors=[], four_wait_returns_observed=True, host_guest_state_writes=0, stops=[])
    data = bytearray(16384)
    for i in range(4):
        args = [ready['event_handle'], 0, ready['timeout_pointer']]
        for phase in ('call', 'ret', 'post'):
            r = raw()
            r['eip'] = hx({'call': ready['postcall_pc']-2, 'ret': ready['return_pc'], 'post': ready['postcall_pc']}[phase])
            r['gpr'][4] = hx({'call': 0x500000, 'ret': 0x4ffffc, 'post': 0x50000c}[phase])
            r['gpr'][0] = hx(ready['nt_wait'] if phase == 'call' else 258 if i == 3 else 0)
            stack = struct.pack('<III', *args) if phase == 'call' else struct.pack('<IIII', ready['postcall_pc'], *args) if phase == 'ret' else b''
            observation['stops'].append(dict(label=f'{phase}-{i}', states=[r, {}],
                compat=pack(r, expected_cpu=0, expected_vcpus=2, expected_source_sha256=source_digest(r)),
                repeat_equal=True, owner_teb_client_id_hex=struct.pack('<II', 123, 456).hex(), code_hex=machine.hex(),
                nt_wait=ready['nt_wait_before'], timeout_hex=struct.pack('<q', 0 if i == 3 else -20000000).hex(),
                data_hex=data.hex(), stack=stack.ljust(64, b'\0').hex()))
        base = 0x1000+i*0x400
        for off, n, value in [(0, 2, r['fp_control']), (2, 2, r['fp_status']), (4, 1, 128), (6, 2, 4),
                              (8, 4, 0x10039f), (16, 4, 0x100904), (24, 4, r['mxcsr'])]:
            data[base+off:base+off+n] = value.to_bytes(n, 'little')
        for j in range(8):
            lo, hi = r['fp_physical_low64_high16'][(7+j) & 7]
            data[base+32+16*j:base+42+16*j] = (int(lo, 16) | int(hi, 16) << 64).to_bytes(10, 'little')
            lo, hi = r['xmm_low64_high64'][j]
            data[base+160+16*j:base+176+16*j] = (int(lo, 16) | int(hi, 16) << 64).to_bytes(16, 'little')
        struct.pack_into('<9I', data, base+0x200, 0, 0, 0, 0x500008, 0, 0, 0, 258 if i == 3 else 0, 0x202)
        struct.pack_into('<I', data, 0x200, i+1)
    result['data_hex'] = data.hex()
    return observation, result


class ConsumeTests(unittest.TestCase):
    def test_complete_synthetic_and_receipt(self):
        o, r = sample()
        report = c.consume(o, {'value': r})
        self.assertTrue(report['fixture_observation_passed'], report)
        self.assertFalse(report['accepted'])
        self.assertFalse(report['original_game_observed'])

    def test_incomplete_and_identity_rejected(self):
        for mutation in ('missing', 'short', 'owner', 'code', 'cleanup'):
            o, r = sample()
            if mutation == 'missing':
                del r['data_hex']
            elif mutation == 'short':
                o['stops'].pop()
            elif mutation == 'owner':
                del o['stops'][1]['owner_teb_client_id_hex']
            elif mutation == 'code':
                o['stops'][1]['code_hex'] = '00'
            else:
                r['handles_closed'] = False
            self.assertFalse(c.consume(o, r)['fixture_observation_passed'], mutation)

    def test_raw_rf_cr3_and_extended_register_tamper(self):
        for key in ('eflags', 'cr3', 'xmm15'):
            o, r = sample()
            stop = o['stops'][2]
            s = stop['states'][0]
            if key == 'eflags':
                s['eflags'] = hx(0x10202)
            elif key == 'cr3':
                s['cr0_cr2_cr3_cr4'][2] = hx(0x102000)
            else:
                s['xmm_low64_high64'][15][1] = hx(999)
            stop['compat'] = pack(s, expected_cpu=0, expected_vcpus=2, expected_source_sha256=source_digest(s))
            report = c.consume(o, r)
            self.assertFalse(report['fixture_observation_passed'], key)
            self.assertTrue(any(not d['allowed'] for group in report['raw64_differences'] for d in group['differences']))

    def test_fx_mapping_and_frame_tamper(self):
        for offset in (0x1000+32, 0x1000+160, 0x1000+0x200+12, 0x1000+0x200+32):
            o, r = sample()
            data = bytearray.fromhex(r['data_hex'])
            data[offset] ^= 1
            r['data_hex'] = data.hex()
            self.assertFalse(c.consume(o, r)['fixture_observation_passed'])

    def test_no_rf_mask_and_precise_abi_allowance(self):
        a = raw()
        b = deepcopy(a)
        b['eflags'] = hx(int(a['eflags'], 16) ^ 1)
        self.assertTrue(c.transition(a, b, 'call-ret')[0]['allowed'])
        self.assertFalse(c.transition(a, b, 'ret-post')[0]['allowed'])
        b['eflags'] = hx(int(a['eflags'], 16) ^ 0x10000)
        self.assertFalse(c.transition(a, b, 'call-ret')[0]['allowed'])


if __name__ == '__main__':
    unittest.main()
