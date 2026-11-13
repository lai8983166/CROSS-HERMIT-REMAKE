"""Bounded symbolic current-owner route; no Win32 or desktop operations.

The frozen CRT/string model is reused by hash. Creation message shapes come from
the pinned old stream, with explicit symbolic ownership projection. Destruction
uses a declared minimal message model. None of these values is native evidence.
"""
import argparse
import ast
import copy
import gzip
import json
from pathlib import Path
import struct
import time

from devtools.terminal_window_lifetime import execute, DestructionEngine, Owner, base, need, ROOT
from devtools.terminal_window_destruction import DestructionOwner, SymbolicCloseOwner

MODEL_INPUTS = [
    ('.venv-audit/terminal-native-owner-build-v1-20261113/offline_route.py', 'Oracle', '6717b2ee45378c87480c1e874be41f962671f5416d1fe1be10889285ba10bb4d'),
    ('.venv-audit/terminal-scene-owner-build-v1-20261113/offline_model.py', 'Model', '1a7688e10abc40196c29f28e54fee5441e9084f60a293a20ee3de30e5cd32128')]


def primitive_model():
    namespace = dict(time=time, struct=struct)
    for path, name, digest in MODEL_INPUTS:
        raw = (ROOT/path).read_bytes()
        need(base.sha(raw) == digest, 'fixed existing primitive model ' + name)
        node = next(n for n in ast.parse(raw).body if isinstance(n, ast.ClassDef) and n.name == name)
        exec(compile(ast.Module(body=[node], type_ignores=[]), path, 'exec'), namespace)
    return namespace['Model']()


class Model(DestructionOwner):
    def __init__(self, engine, case):
        self.engine, self.case, self.primitive = engine, case, primitive_model()
        self.waiting, self.callback_packets, self.callback_active = [], [], []
        self.trace, self.responses, self.requests, self.deliveries = [], {}, {}, {}
        self.seq = 0
        self.events = [dict(event='READY', main_tid=101, main_teb=4096)]
        self.callback_handler = engine.callback
        self.deadline = time.monotonic()+25
        self.primitive.deadline = self.deadline
        self.module, self.hwnd, self.atom = 0x12340000, 0x4444, 0x5555
        self.property, self.gate, self.module_live, self.class_live, self.window_live = 0, 0, 0, 0, 0
        self.closed, self.quit = False, False

    def check(self):
        need(time.monotonic() < self.deadline, '25 second complete symbolic route')

    def data(self, cid, after=False):
        if cid > 17:
            return b''
        node = self.case['callbacks'][cid-1]
        packet = node['setup']['packet']
        raw = bytes.fromhex(packet['data_hex'])
        if after:
            calls = [r for r in node['platform_calls'] if r['name'] == 'DefWindowProcA']
            if calls:
                raw = bytes.fromhex(calls[0]['result']['after_hex'])
        raw = bytearray(raw)
        if packet['data_kind'] == 'CREATESTRUCTA':
            struct.pack_into('<II', raw, 0, self.engine.window_owner, self.module)
        elif packet['data_kind'] == 'WINDOWPOS':
            struct.pack_into('<I', raw, 0, self.hwnd)
        return bytes(raw)

    def packet(self, cid, parent):
        if cid <= 17:
            node = self.case['callbacks'][cid-1]
            old = node['setup']['packet']
            packet = {k: old[k] for k in ('message', 'wParam', 'lParam', 'depth', 'data_kind')}
            packet['parent_callback_id'] = node['parent_callback_id'] or 0
        else:
            packet = dict(message={18:16, 19:2, 20:130}[cid], wParam=0, lParam=0,
                          depth=1 if cid == 18 else 2, parent_callback_id=0 if cid == 18 else 18, data_kind='opaque')
        ptd = self.engine.thread_ptd[0]
        raw = self.data(cid)
        packet.update(callback_id=cid, parent_request=parent, lane=0, tid=101, teb=4096, guest_entry=0x424980,
                      hwnd=self.hwnd, last_error=0, data_bytes=len(raw), data_hex=raw.hex(), tls_slot=5,
                      tls_value=self.engine.native(ptd), tls_tracked_value=self.engine.native(ptd), tls_error=0,
                      ptd_bytes=116, ptd_hex=self.engine.read(ptd, 116).hex())
        return packet

    def send(self, lane, op, *args):
        self.check()
        need(lane == 0, 'symbolic MAIN only')
        self.seq += 1
        seq = self.seq
        self.requests[seq] = (0, op)
        self.trace.append(dict(direction='request', id=seq, lane=0, op=op, args=list(args)))
        cid = self.callback_active[-1] if self.callback_active else 0
        children, reply = [], dict(result=0, last_error=self.primitive.errors[0])
        if op == 'WINDOW_GATE':
            self.gate = args[0]
            reply['result'] = 1
        elif op == 'WINDOW_MODULE':
            need(self.gate and not self.module_live, 'symbolic module lifetime')
            self.module_live = 1
            reply['result'] = self.module
        elif op == 'WINDOW_MODULE_CLOSE':
            need(args == (self.module,) and not self.window_live and not self.class_live, 'symbolic module cleanup')
            self.module_live = 0
            reply['result'] = 1
        elif op == 'FindWindowA':
            need(args[1] == 0, 'original duplicate query')
        elif op in ('SetRect', 'AdjustWindowRect'):
            data, offset = self.primitive.region(args[0], 16)
            data[offset:offset+16] = struct.pack('<4I', 0, 0, 1024, 768)
            reply['result'] = 1
        elif op in ('LoadIconA', 'LoadCursorA', 'GetStockObject'):
            reply['result'] = {'LoadIconA':0x6666, 'LoadCursorA':0x7777, 'GetStockObject':0x8888}[op]
        elif op == 'RegisterClassExA':
            self.class_live = 1
            reply.update(result=self.atom, atom=self.atom)
        elif op == 'CreateWindowExA':
            need(self.class_live and args[10:] == (self.module, self.engine.window_owner), 'current symbolic creation inputs')
            self.window_live = 1
            children = [i+1 for i, n in enumerate(self.case['callbacks']) if n['parent_callback_id'] is None]
            reply['result'] = self.hwnd
        elif op == 'WINDOW_CLOSE':
            need(args == (self.hwnd,) and self.window_live, 'current modeled HWND to original WM_CLOSE')
            children = [18]
            reply.update(is_window_after=0, ncdestroy_observed=1, quit_posted=1, property_removed=1)
        elif op == 'UnregisterClassA':
            need(args == (self.atom, self.module) and self.closed and self.quit and not self.property, 'class cleanup after modeled original close')
            self.class_live = 0
            reply['result'] = 1
        elif op.startswith('CB_'):
            need(cid == args[0], 'active modeled callback')
            reply['callback_id'] = cid
            if op == 'CB_GET_PROP':
                reply['result'] = self.property
            elif op == 'CB_SET_PROP':
                need(args[2] == self.engine.window_owner, 'original current MAIN property')
                self.property = args[2]
                reply.update(result=1, observed_property=self.property)
            elif op == 'CB_GET_LONG':
                reply.update(result=0 if args[2] == 4 else 0x424980, host_result=0x100200, reverse_translated=int(args[2] != 4))
            elif op == 'CB_DEFAULT':
                reply.update(before_hex=self.data(cid).hex(), after_hex=self.data(cid, True).hex())
                if cid <= 17:
                    node = self.case['callbacks'][cid-1]
                    old = next(r for r in node['platform_calls'] if r['name'] == 'DefWindowProcA')
                    reply['result'] = old['observed_EAX']
                    children = [n for n in old['nested_callback_ids'] if self.case['callbacks'][n-1]['parent_callback_id'] == cid]
            elif op == 'CB_DESTROY_WINDOW':
                need(cid == 18 and args[1] == self.hwnd, 'original close DestroyWindow')
                self.closed, self.window_live = True, 0
                children = [19, 20]
                reply.update(result=1, is_window_after=0, ncdestroy_observed=1)
            elif op == 'CB_POST_QUIT':
                need(cid == 19 and args[1] == 0, 'original destroy PostQuitMessage')
                self.quit = True
            elif op == 'CB_REMOVE_PROP':
                need(cid == 19 and self.property == self.engine.window_owner, 'original property removal')
                reply.update(result=self.property, observed_property=0)
                self.property = 0
            elif op == 'CB_RETURN':
                reply.update(result=1, callback_result=args[1])
            else:
                raise ValueError('unsupported callback model ' + op)
        else:
            reply = self.primitive.call(op, *args)
            if op == 'STATUS':
                reply.update(ui_gate=self.gate, window_modules=self.module_live, window_classes=self.class_live,
                    windows=self.window_live, callback_depth=len(self.callback_active), allocations=len(self.primitive.blocks),
                    memory_bytes=sum(map(len, self.primitive.blocks.values())), heaps=int(bool(self.engine.heap)), handles=0,
                    criticals=len(self.primitive.locks), tls_slots=int(any(self.primitive.tls.values())),
                    fonts=len(self.primitive.fonts), dcs=len(self.primitive.dcs))
        rows = ['C '+' '.join(k+'='+('-' if v == '' else str(v)) for k, v in self.packet(child, seq).items()) for child in children]
        extra = {k:v for k, v in reply.items() if k not in ('result', 'last_error', 'ok', 'tid', 'teb')}
        extra['teb'] = 4096
        rows.append('R '+' '.join(map(str, (seq, 0, 101, reply['last_error'], 1, reply['result'])))+' '+
                    ' '.join(k+'='+('-' if v == '' else str(v)) for k, v in extra.items()))
        self.deliveries[seq] = rows
        return seq

    def poll(self, block=False):
        self.check()
        self.consume_line(self.deliveries[self.waiting[-1]].pop(0))

    def wait(self, milliseconds):
        return 0


def rejection_checks(engine, outcome):
    results = []
    for field, value in (('is_window_after', 1), ('ncdestroy_observed', 0), ('quit_posted', 0), ('property_removed', 0)):
        probe = copy.copy(engine)
        probe.window_closed = False
        try:
            probe.assert_closed(dict(outcome['close'], **{field:value}))
        except ValueError as error:
            results.append(dict(case=field, rejected=True, reason=str(error)))
        else:
            raise ValueError('incomplete close accepted: ' + field)
    for name, patch in (('wrong_MAIN_thread', dict(tid=999)), ('wrong_MAIN_TEB', dict(teb=999)),
                        ('wrong_close_message', dict(message=2)), ('wrong_close_parent', dict(parent_request=2)),
                        ('wrong_callback_depth', dict(depth=2)), ('wrong_callback_lane', dict(lane=1))):
        owner = SymbolicCloseOwner(engine)
        owner.requests[1], owner.waiting = (0, 'WINDOW_CLOSE'), [1]
        packet = owner.packet(16, 1, 1, 0, 1)
        packet.update(patch)
        def forbidden(_):
            raise AssertionError('bad close envelope reached original executor')
        owner.callback_handler = forbidden
        try:
            owner.consume_line(owner.callback_line(packet))
        except ValueError as error:
            results.append(dict(case=name, rejected=True, reason=str(error)))
        else:
            raise ValueError('bad close envelope accepted: ' + name)
    # No Win32 object is constructed by this watchdog admission regression.
    owner = Owner.__new__(Owner)
    owner.start, owner.deadline = 100, 130
    need(owner.deadline == 120, 'actual inherited watchdog input tightened to20 seconds')
    results.append(dict(case='watchdog20_before_timer_creation', passed=True, native_executed=False))
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True)
    parser.add_argument('--helper', required=True)
    args = parser.parse_args()
    output = (ROOT/args.out).resolve()
    need(output.is_relative_to(ROOT) and not output.exists(), 'fresh symbolic route report')
    source = ROOT/'analysis/school-window-startup-trajectory-v3-20261020.json'
    need(base.sha(source.read_bytes()) == 'a5f30898f2add507e70277617838ad51e5328b56915c227460e3bc43f2afcd48', 'fixed template source')
    engine = DestructionEngine()
    model = Model(engine, json.loads(source.read_text())['cases'][0])
    started = time.monotonic()
    report = dict(route_closed=False, native_executed=False, symbolic_only=True, formal_acceptance=False,
                  collector=base.identity(ROOT/'devtools/terminal_window_lifetime.py'), model=base.identity(__file__),
                  native_helper=base.identity(ROOT/args.helper), primitive_models=[base.identity(ROOT/p) for p, _, _ in MODEL_INPUTS],
                  source_message_shape_template=base.identity(source), pins=[], actual_native_cleanup_proven=False)
    try:
        report['outcome'] = execute(engine, model)
        need(not model.requests and not model.callback_active and not model.primitive.blocks, 'complete modeled stream and buffers empty')
        report['rejections'] = rejection_checks(engine, report['outcome'])
        report['route_closed'] = True
    except BaseException as exc:
        report.update(failure=repr(exc), failure_pc=hex(engine.reg('EIP')), last_requests=model.trace[-4:])
    report.update(seconds=time.monotonic()-started, instructions=engine.count, API_calls=len(engine.records),
                  callbacks=len(engine.callbacks), roots=[r['label'] for r in engine.roots],
                  CPU57_restored=all(c['suspended_caller']['cpu'] == c['restored_caller']['cpu'] for c in engine.callbacks),
                  instruction_sha256=engine.ih.hexdigest(), write_sha256=engine.wh.hexdigest())
    report['pins'] = [base.identity(ROOT/p) for p in ('devtools/terminal_window_lifetime.py', 'devtools/terminal_window_desktop.py',
        'devtools/terminal_window_destruction.py', 'devtools/terminal_window_native_v2.py', 'devtools/terminal_window_callbacks.py',
        'devtools/terminal_window_preparation.py', 'devtools/terminal_window_native.py', 'devtools/terminal_window_native.inc')]
    output.write_text(json.dumps(report, indent=2)+'\n', encoding='utf8', newline='\n')
    print(json.dumps({k:v for k, v in report.items() if k not in ('pins', 'primitive_models', 'outcome')}))
    return 0 if report['route_closed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
