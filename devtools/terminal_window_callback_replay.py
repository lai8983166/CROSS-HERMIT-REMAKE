"""Bounded offline original-code replay of two frozen native callback streams.

The old native handles are inert input values only. This module has no native
launch, window operation, input, screenshot, or fresh-lifetime claim.
"""
from __future__ import annotations
import argparse
import base64
import copy
import hashlib
import json
from pathlib import Path
import struct
import time
import zlib

from devtools.terminal_window_callbacks import WindowEngine, WindowOwner, base, need, ENTRY, CREATE_SLOT
from devtools.terminal_window_preparation import PreparedWindowEngine, PREPARATION

ROOT = base.ROOT
SOURCE = ROOT / 'analysis/school-window-startup-trajectory-v3-20261020.json'
SOURCE_SHA = 'a5f30898f2add507e70277617838ad51e5328b56915c227460e3bc43f2afcd48'


def unpack(blob):
    raw = zlib.decompress(base64.b64decode(blob['zlib_base64']))
    need(len(raw) == blob['bytes'] and base.sha(raw) == blob['sha256'], 'frozen source buffer integrity')
    return raw


def line(tag, row):
    return tag + ' ' + ' '.join(str(k) + '=' + ('-' if v == '' else str(v)) for k, v in row.items())


class RecordedOwner(WindowOwner):
    """Exercise the production parser/recursive waiting with recorded leaves."""
    def __init__(self, case, engine):
        self.waiting, self.callback_packets, self.callback_active = [], [], []
        self.trace, self.responses, self.requests = [], {}, {}
        self.events = [dict(event='READY', main_tid=123, main_teb=456)]
        self.seq, self.callback_handler = 0, self.replay_callback
        self.case, self.engine = case, engine
        self.nodes = {n['setup']['packet']['callback_id']: n for n in case['callbacks']}
        self.positions = {k: 0 for k in self.nodes}
        self.deliveries = {}
        self.deadline = time.monotonic() + 15

    def check(self):
        need(time.monotonic() < self.deadline, '15 second offline case bound')

    def replay_callback(self, packet):
        node = self.nodes[packet['callback_id']]
        need(self.engine.read(0x1ffff000, 0x4000) == unpack(node['guarded_owner_before']), 'retained original MAIN before callback')
        value = self.engine.callback(packet)
        actual = self.engine.callbacks[packet['callback_id'] - 1]
        need(actual['instruction_runs'] == node['instruction_runs'], 'exact frozen original callback instruction sequence')
        need(value == node['result'], 'original callback return equals actual recorded return')
        need(self.engine.read(0x1ffff000, 0x4000) == unpack(node['state']['guarded_owner']), 'complete original MAIN after callback')
        need(len(actual['API_calls']) == len(node['platform_calls']), 'all recorded platform calls consumed')
        for new, old in zip(actual['API_calls'], node['platform_calls']):
            need((new['name'], new['slot'], new['ret'], new['value']) ==
                 (old['name'], int(old['slot'], 16), int(old['return_va'], 16), old['observed_EAX']), 'original leaf/return ABI continuity')
        return value

    def packet(self, cid, parent_request):
        old = self.nodes[cid]['setup']['packet']
        row = {k: old[k] for k in ('callback_id', 'depth', 'guest_entry', 'hwnd', 'message', 'wParam', 'lParam', 'data_kind', 'data_hex')}
        row.update(parent_request=parent_request, parent_callback_id=self.nodes[cid]['parent_callback_id'] or 0,
                   data_bytes=len(bytes.fromhex(old['data_hex'])), lane=0, tid=123, teb=456, last_error=0,
                   tls_slot=0xffffffff, tls_value=0, tls_tracked_value=0, tls_error=0, ptd_bytes=0, ptd_hex='')
        return row

    def send(self, lane, op, *args):
        self.check()
        need(lane == 0, 'recorded MAIN only')
        self.seq += 1
        seq = self.seq
        self.requests[seq] = (lane, op)
        self.trace.append(dict(direction='request', id=seq, lane=lane, op=op, args=list(args)))
        cid = self.callback_active[-1] if self.callback_active else 0
        children, reply = [], {}
        if op == 'CreateWindowExA':
            need(not cid and list(args) == self.case['creation']['args'], 'frozen pending CreateWindowExA frame')
            children = [i for i, n in self.nodes.items() if n['parent_callback_id'] is None]
            reply['result'] = self.case['creation_result']['result']
        elif op == 'CB_RETURN':
            need(args == (cid, self.nodes[cid]['result']) and self.positions[cid] == len(self.nodes[cid]['platform_calls']), 'complete original callback return before acknowledgment')
            reply['result'] = 1
            reply['callback_result'] = args[1]
        else:
            need(cid and args[0] == cid, 'recorded callback ID')
            node = self.nodes[cid]
            old = node['platform_calls'][self.positions[cid]]
            self.positions[cid] += 1
            expected = {'GetPropA': 'CB_GET_PROP', 'SetPropA': 'CB_SET_PROP', 'GetWindowLongA': 'CB_GET_LONG', 'DefWindowProcA': 'CB_DEFAULT'}[old['name']]
            need(op == expected, 'exact recorded leaf sequence')
            p = node['setup']['packet']
            wanted = {'CB_GET_PROP': (cid, p['hwnd']), 'CB_SET_PROP': (cid, p['hwnd'], 0x20000000),
                      'CB_GET_LONG': (cid, p['hwnd'], old['args'][1]),
                      'CB_DEFAULT': (cid, p['hwnd'], p['message'], p['wParam'], p['lParam'])}[op]
            need(args == wanted, 'actual source leaf arguments with declared buffer projection only')
            reply = dict(old['result'])
            children = [i for i in old['nested_callback_ids'] if self.nodes[i]['parent_callback_id'] == cid]
        reply.setdefault('last_error', 0)
        reply.update(teb=456)
        if cid:
            reply['callback_id'] = cid
        deliveries = [line('C', self.packet(i, seq)) for i in children]
        extra = {k: int(v) if isinstance(v, bool) else v for k, v in reply.items()
                 if k not in ('result', 'last_error', 'host_args') and isinstance(v, (str, int, bool))}
        deliveries.append('R ' + ' '.join(map(str, (seq, 0, 123, reply['last_error'], 1, reply['result']))) +
                          ' ' + ' '.join(k + '=' + str(v) for k, v in extra.items()))
        self.deliveries[seq] = deliveries
        return seq

    def poll(self, block=False):
        self.check()
        pending = self.waiting[-1]
        need(self.deliveries[pending], 'pending response stream not exhausted')
        self.consume_line(self.deliveries[pending].pop(0))


def initialize(case, engine_type=WindowEngine):
    engine = engine_type()
    engine.u.mem_map(0x1ffff000, 0x4000)
    engine.md.topology()
    engine.put(0x1ffff000, unpack(case['callbacks'][0]['guarded_owner_before']))
    engine.put(base.cold.old.STACK, unpack(case['creation']['native_stack']))
    title = engine.image[0x7a2628 - 0x400000:0x7a2628 - 0x400000 + 13]
    need(title == b'Cross Hermit\0', 'frozen observed class/title bytes')
    engine.put(0x7a2628, title)
    for name, value in case['creation']['cpu'].items():
        engine.reg(name, value)
    # Recorded prefix has not yet published GAME. No fake GAME/result state.
    need(engine.word(0x7a49fc) == 0 and engine.word(0x80a398) == 0, 'original pre-GAME globals')
    engine.allocations[0x20000000] = dict(native=0, bytes=0x1110)
    engine.bind_window(0x20000000, case['creation']['args'][10])
    engine.owner = RecordedOwner(case, engine)
    # Deliberately retain nonzero SIMD/control fields through callbacks. These
    # are declared offline seeds, never claimed to be imported host registers.
    for i in range(8):
        engine.reg('XMM' + str(i), (0x123456789abcdef0 << 64) | (i + 1))
    engine.reg('CR2', 0x87654321)
    engine.reg('MXCSR', 0x1f80)
    return engine


class PreparedRecordedOwner(RecordedOwner):
    """Recorded original leaves plus explicitly modeled marshalling buffers."""
    def __init__(self, case, engine):
        super().__init__(case, engine)
        self.buffers, self.next_buffer, self.prep_position = {}, 0x18000000, 0
        self.prep_calls = [call for phase in ('query', 'rect', 'adjust', 'icons', 'class_ready', 'registered')
                           for call in case[phase]['platform_calls']]

    def send(self, lane, op, *args):
        if op not in ('MEM_ALLOC', 'MEM_WRITE', 'MEM_READ', 'MEM_FREE', 'lstrcpyA', *[v[0] for v in PREPARATION.values()]):
            return super().send(lane, op, *args)
        need(not self.callback_active and lane == 0, 'marshalling outside callback only')
        reply = {}
        if op == 'MEM_ALLOC':
            need(0 < args[0] <= 260, 'bounded preparation buffer model')
            pointer = self.next_buffer
            self.next_buffer += 4096
            self.buffers[pointer] = bytearray(args[0])
            reply['result'] = pointer
        elif op == 'MEM_WRITE':
            raw = bytes.fromhex(args[1])
            need(args[0] in self.buffers and len(raw) <= len(self.buffers[args[0]]), 'bounded modeled buffer write')
            self.buffers[args[0]][:len(raw)] = raw
            reply['result'] = len(raw)
        elif op == 'MEM_READ':
            need(args[0] in self.buffers and len(self.buffers[args[0]]) == args[1], 'whole modeled buffer read')
            reply.update(result=args[1], hex=self.buffers[args[0]].hex())
        elif op == 'MEM_FREE':
            need(args[0] in self.buffers, 'owned modeled buffer free')
            del self.buffers[args[0]]
            reply['result'] = 1
        else:
            old = self.prep_calls[self.prep_position]
            self.prep_position += 1
            need(op == old['name'], 'recorded original preparation call order')
            reply = dict(old['result'])
            if op == 'lstrcpyA':
                need(self.buffers[args[0]][:256].hex() == old['request']['before_hex'] and
                     self.buffers[args[1]][:13].hex() == old['request']['source_hex'], 'recorded title copy input')
                self.buffers[args[0]][:256] = bytes.fromhex(reply['hex'])
                reply['result'] = args[0] + reply['return_offset']
            elif op == 'FindWindowA':
                need(bytes(self.buffers[args[0]]) == b'Cross Hermit\0' and args[1] == 0, 'original duplicate query buffer')
            elif op in ('SetRect', 'AdjustWindowRect'):
                need(args[1:] == tuple(old['args'][1:]) and len(self.buffers[args[0]]) == 16, 'original geometry ABI')
                self.buffers[args[0]][:] = bytes.fromhex(reply['hex'])
            elif op == 'RegisterClassExA':
                raw = bytearray(self.buffers[args[0]])
                name = struct.unpack_from('<I', raw, 40)[0]
                need(bytes(self.buffers[name]) == b'Cross Hermit\0', 'real class pointer projection bytes')
                struct.pack_into('<I', raw, 40, 0x7a2628)
                need(raw.hex() == old['result']['guest_hex'], 'complete recorded original class bytes')
                reply['result'] = old['observed_EAX']
            else:
                need(args == tuple(old['args']), 'exact original preparation resource arguments')
        self.seq += 1
        self.requests[self.seq] = (0, op)
        self.trace.append(dict(direction='request', id=self.seq, lane=0, op=op, args=list(args), modeled_marshalling=op.startswith('MEM_')))
        extra = {k: int(v) if isinstance(v, bool) else v for k, v in reply.items()
                 if k not in ('result', 'last_error') and isinstance(v, (int, bool, str)) and ' ' not in str(v)}
        extra['teb'] = 456
        self.deliveries[self.seq] = ['R ' + ' '.join(map(str, (self.seq, 0, 123, reply.get('last_error', 0), 1, reply['result']))) +
                                     ' ' + ' '.join(k + '=' + str(v) for k, v in extra.items())]
        return self.seq


def preparation(case):
    engine = initialize(case, PreparedWindowEngine)
    start = case['tasks']
    engine.put(0x1ffff000, unpack(start['state']['guarded_owner']))
    engine.put(base.cold.old.STACK, unpack(start['state']['stack']))
    engine.put(0x7a2628, unpack(start['state']['title']))
    engine.put(0x7a2728, struct.pack('<I', start['state']['instance_value']))
    engine.put(0x7a4a00, struct.pack('<I', 0x20000000))
    for name, value in start['cpu'].items():
        engine.reg(name, value)
    engine.owner = PreparedRecordedOwner(case, engine)
    engine.ctx[0] = engine.u.context_save()
    engine.stop, engine.done[0] = 0x4504e1, False
    engine.drive()
    expected_runs = [row for stage in ('query', 'branch', 'rect', 'adjust', 'class', 'icons', 'class_ready',
                                       'registered', 'create_ready', 'creation', 'hwnd_publication')
                     for row in case[stage]['instruction_runs']]
    need(engine.preparation_runs == expected_runs, 'all original preparation/publication instructions match frozen stream')
    need(all(engine.reg(k) == v for k, v in case['hwnd_publication']['cpu'].items()), 'complete source10 publication CPU')
    need(engine.read(0x1ffff000, 0x4000) == unpack(case['hwnd_publication']['state']['guarded_owner']), 'complete source MAIN at publication')
    need(not engine.owner.buffers and not engine.owner.requests and engine.owner.prep_position == len(engine.owner.prep_calls),
         'all preparation calls and temporary marshalling buffers complete')
    return dict(fill=case['fill'], entry=0x49de2c, end=0x4504e1, original_instructions=engine.count,
                original_preparation_instructions=sum(r['count'] for r in engine.preparation_runs),
                original_preparation_leafs=engine.owner.prep_position, callbacks=len(engine.callbacks),
                callback_depth=max(r['packet']['depth'] for r in engine.callbacks),
                instruction_sha256=engine.ih.hexdigest(), write_sha256=engine.wh.hexdigest(),
                exact_original_sequences=True, exact_MAIN_bytes=True, CPU57_callback_restore=True,
                original_HWND_publication=engine.word(0x7a0bb4), temporary_buffers_empty=True,
                modeled_marshalling_only=True, actual_new_native_execution=False,
                API_calls=[r for r in engine.records if 'callback_id' not in r], callback_records=engine.callbacks)


def replay(case):
    engine = initialize(case)
    before = engine.state()
    engine.run_generator(engine.api(CREATE_SLOT))
    result = engine.records[0]['native_leaf']
    need(not engine.owner.requests and not engine.owner.waiting and not engine.frames, 'all nested requests completed')
    need(all(not q for q in engine.owner.deliveries.values()), 'complete recorded stream consumed')
    need(all(engine.reg(k) == v for k, v in case['hwnd_publication']['before_cpu'].items()), 'original creation return CPU equals frozen result')
    need(engine.read(0x1ffff000, 0x4000) == unpack(case['hwnd_publication']['state']['guarded_owner']), 'recorded final MAIN object')
    # Continue from the production API adapter's returned original frame.
    # Only original instructions publish HWND; no separate publication root.
    engine.ctx[0] = engine.u.context_save()
    engine.stop, engine.done[0] = 0x4504e1, False
    engine.drive()
    need(all(engine.reg(k) == v for k, v in case['hwnd_publication']['cpu'].items()), 'original publication CPU equals frozen result')
    need(engine.word(0x7a0bb4) == result['result'], 'original instruction published actual HWND')
    return dict(fill=case['fill'], callbacks=len(engine.callbacks), max_depth=max(r['packet']['depth'] for r in engine.callbacks),
                original_instructions=engine.count, instruction_sha256=engine.ih.hexdigest(), write_sha256=engine.wh.hexdigest(),
                wire_requests=engine.owner.seq, CPU_fields=len(before['cpu']), CPU57_restored=True,
                exact_recorded_original_sequences=True, exact_MAIN_bytes=True, original_CreateWindow_result=result['result'],
                callbacks_detail=engine.callbacks, source_leaf_results_only=True, native_executed=False)


def negatives(case):
    engine = initialize(case)
    owner = engine.owner
    req = owner.send(0, 'CreateWindowExA', *case['creation']['args'])
    owner.waiting.append(req)
    packet = owner.packet(1, req)
    checks = {
        'wrong_thread': lambda p: p.update(tid=999),
        'wrong_TEB': lambda p: p.update(teb=999),
        'wrong_parent_request': lambda p: p.update(parent_request=99),
        'wrong_parent_callback': lambda p: p.update(parent_callback_id=1),
        'wrong_depth': lambda p: p.update(depth=2),
        'wrong_lane': lambda p: p.update(lane=1),
        'duplicate_field': None,
    }
    results = []
    for name, mutate in checks.items():
        changed = copy.deepcopy(packet)
        if mutate:
            mutate(changed)
        raw = line('C', changed) + (' lane=0' if mutate is None else '')
        try:
            owner.consume_line(raw)
        except (ValueError, KeyError) as error:
            results.append(dict(name=name, rejected=True, reason=str(error)))
        else:
            raise ValueError('negative accepted: ' + name)
        need(not owner.callback_packets and not engine.callbacks, 'invalid envelope rejected before guest execution')
    owner.waiting.pop()
    # Payload/entry checks are deliberately tested at the executor boundary,
    # independently of the native transport's envelope admission.
    for name, mutation in (
        ('wrong_original_entry', dict(guest_entry=ENTRY + 1)),
        ('truncated_CREATESTRUCT', dict(data_hex=packet['data_hex'][:-2])),
        ('wrong_CREATESTRUCT_owner', dict(data_hex='01000020' + packet['data_hex'][8:])),
        ('wrong_payload_kind', dict(data_kind='opaque')),
        ('unexpected_native_TLS', dict(tls_slot=1, tls_value=123)),
    ):
        changed = dict(packet, **mutation)
        try:
            engine.callback(changed)
        except ValueError as error:
            results.append(dict(name=name, rejected=True, reason=str(error)))
        else:
            raise ValueError('negative accepted: ' + name)
        need(not engine.callbacks, 'invalid callback payload rejected before execution')
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    output = (ROOT / args.out).resolve()
    need(output.is_relative_to(ROOT) and not output.exists(), 'fresh workspace evidence')
    raw = SOURCE.read_bytes()
    need(base.sha(raw) == SOURCE_SHA, 'accepted frozen native source identity')
    source = json.loads(raw)
    results = [replay(case) for case in source['cases']]
    prepared = [preparation(case) for case in source['cases']]
    for case in results:
        # The continuous preparation run retains the callback states once.
        # The direct-boundary regression needs only its result/digest summary.
        del case['callbacks_detail']
    report = dict(schema_version=1, kind='original_window_callbacks_offline_same_owner_adapter',
                  offline_passed=True, native_executed=False, desktop_used=False, screenshot=False,
                  formal_acceptance=False, new_native_lifetime=False, original_wait_return=False, first_result_consumption=False,
                  source=base.identity(SOURCE), implementation=base.identity(__file__),
                  adapter=base.identity(ROOT / 'devtools/terminal_window_callbacks.py'),
                  preparation_adapter=base.identity(ROOT / 'devtools/terminal_window_preparation.py'),
                  original=base.identity(base.cold.base.SOURCE),
                  parent_implementation_pins=[base.identity(ROOT / p) for p in (
                      'devtools/terminal_native_owner_probe.py', 'devtools/terminal_scene_construction.py',
                      'tools/school_window_startup.py', 'tools/school_window_startup_platform.cs',
                      'analysis/school-window-startup-acceptance-20261020.json')],
                  case_results=results, preparation_results=prepared, negative_checks=negatives(source['cases'][0]),
                  limits=['Recorded handles are inert replay inputs; no current ownership claimed',
                          'Legacy source lacks TID/TEB/TLS; transport IDs123/456 and absentTLS are declared model fields only',
                          'New native window extension remains unexecuted; no desktop admission',
                          'CPU57 seeds extend legacy10-field callback ABI; not host state capture',
                          'Native window preparation/cleanup, GAME publication, wait/result consumption still pending'])
    import gzip
    output.write_bytes(gzip.compress((json.dumps(report, separators=(',', ':')) + '\n').encode(), mtime=0))
    print(json.dumps(dict(output=base.identity(output), cases=[{k: v for k, v in c.items() if k != 'callbacks_detail'} for c in results], negatives=len(report['negative_checks']))))


if __name__ == '__main__':
    main()
