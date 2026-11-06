"""Bounded independent base-node registration with fresh native CRT/event owners.

Stops before the original CreateThread CALL. This is not the current terminal
scene, a native CRT worker, a resumed historical lifetime, or exit acceptance.
"""
from __future__ import annotations

import argparse
from collections import Counter
import copy
import gzip
import hashlib
import json
from pathlib import Path
import struct
import sys
import time

from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn import x86_const as x86
from tools import school_crt_init_fixture as fixture
from tools import school_retained_scheduler_platform as scheduler_platform
from tools.terminal_unit_frontends_trace import CPU_REGISTERS, MemoryDigest

ROOT = Path(__file__).resolve().parents[1]
MANAGER = 0x65001000
NODE = 0x65002000
CLEANUP_STACK = 0x65300000
CREATE_THREAD_CALL = 0x56E0BE
EVENT_TOKEN = 0x65010000
SLOTS = {**fixture.IMPORTS, 0x592274: ('CreateEventA', 16),
         0x592228: ('ResetEvent', 4), 0x59222C: ('SetEvent', 4),
         0x59226C: ('WaitForSingleObject', 8), 0x59221C: ('CreateThread', 24)}
SOURCE_SHA = '588b4288e4c737dc489d2b9bc0652cca85e3d668b1784942ef4b4bda916f1005'


def need(value, message):
    if not value:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def identity(path):
    path = Path(path)
    data = path.read_bytes()
    return dict(path=path.relative_to(ROOT).as_posix(), bytes=len(data), sha256=sha(data))


def implementation_files():
    paths = {Path(__file__).resolve()}
    for module in list(sys.modules.values()):
        name = getattr(module, '__file__', None)
        if name:
            path = Path(name).resolve()
            if path.suffix == '.py' and path.is_relative_to(ROOT/'tools'):
                paths.add(path)
    return {p.relative_to(ROOT).as_posix():identity(p) for p in sorted(paths)}


def full_cpu(uc):
    result = {}
    for key in CPU_REGISTERS:
        value = uc.reg_read(getattr(x86, 'UC_X86_REG_' + key))
        result[key] = list(value) if isinstance(value, tuple) else value
    return result


def memory(uc):
    return dict(digest=MemoryDigest(uc).capture(), regions=[
        dict(pointer=a, bytes=b-a+1, permission=p, sha256=sha(bytes(uc.mem_read(a, b-a+1))))
        for a, b, p in uc.mem_regions()])


def validate_thread_request(args, node, ptd, ptd_bytes):
    need(args == [0, 0, 0x56E110, ptd, 4, node+0x24], 'exact original suspended CreateThread ABI')
    expected = bytearray(116)
    for offset, value in ((4, 0xFFFFFFFF), (0x14, 1), (0x48, 0x421F50),
                          (0x4C, node), (0x50, 0x761D68)):
        struct.pack_into('<I', expected, offset, value)
    need(ptd_bytes == expected, 'complete original 116-byte CRT per-thread data')


class Guest(fixture.Guest):
    def __init__(self, crt, scheduler):
        self.scheduler_live = scheduler
        self.events = {}
        self.manager_lock_live = False
        self.manager_depth = 0
        self.pending = None
        super().__init__(crt, 0)
        self.u.mem_map(MANAGER, 4096)
        self.u.mem_map(NODE, 4096)
        self.u.mem_map(CLEANUP_STACK, 65536)
        self.u.mem_write(MANAGER, bytes([0xA5])*4096)
        self.u.mem_write(NODE, bytes([0xA5])*4096)
        self.declaration['independent_inputs'] = [
            dict(pointer=MANAGER, bytes=4096, fill=0xA5, purpose='new independent manager'),
            dict(pointer=NODE, bytes=4096, fill=0xA5, purpose='new base node, not terminal TASK'),
            dict(pointer=CLEANUP_STACK, bytes=65536, fill=0, purpose='separate supplemental cleanup roots')]
        for slot in SLOTS:
            target = fixture.word(self.read(slot))
            if not any(a <= target <= b for a, b, _ in self.u.mem_regions()):
                self.u.mem_map(target & -4096, 4096)
        self.declaration['initial_complete_CPU'] = full_cpu(self.u)
        self.declaration['initial_complete_memory'] = memory(self.u)
        self.declaration['current_terminal_state_loaded'] = False
        self.steps = []

    def api(self, slot):
        name, pop = SLOTS[slot]
        sp = self.cpu()['ESP']
        ret = fixture.word(self.read(sp))
        args = [fixture.word(self.read(sp+4+i)) for i in range(0, pop, 4)]
        manager_call = name in ('InitializeCriticalSection', 'DeleteCriticalSection',
                               'EnterCriticalSection', 'LeaveCriticalSection') and args == [MANAGER+0x100]
        event_call = name == 'CreateEventA' or name in ('CloseHandle', 'SetEvent', 'ResetEvent') and args[0] in self.events
        need(name not in ('CreateThread', 'WaitForSingleObject'), 'thread/wait native boundary forbidden in this probe')
        if not manager_call and not event_call:
            return super().api(slot)
        start = len(self.scheduler_live.trace)
        outputs = []
        if manager_call:
            op = {'InitializeCriticalSection':'initialize', 'DeleteCriticalSection':'delete',
                  'EnterCriticalSection':'enter', 'LeaveCriticalSection':'leave'}[name]
            need((not self.manager_lock_live) if op == 'initialize' else self.manager_lock_live,
                 'exact current manager lock lifetime')
            if op == 'delete':
                need(self.manager_depth == 0, 'unlocked source manager teardown')
            q = dict(guest=args[0])
            result = self.scheduler_live.request(op, **q)
            if op != 'delete':
                data = bytes.fromhex(result['hex'])
                need(len(data) == 24, 'complete actual manager critical section')
                self.u.mem_write(args[0], data)
                outputs.append(dict(pointer=args[0], hex=data.hex()))
            if op == 'initialize': self.manager_lock_live = True
            elif op == 'delete': self.manager_lock_live = False
            else:
                self.manager_depth += 1 if op == 'enter' else -1
                need(result['depth'] == self.manager_depth and 0 <= self.manager_depth <= 4,
                     'same native service thread owns balanced manager lock')
            value = 0
        elif name == 'CreateEventA':
            need(args == [0, 0, 0, 0] and ret in (0x421585, 0x42194D),
                 'original unnamed auto-reset nonsignaled event request')
            need(len(self.events) < 2, 'only manager and node events')
            op, q = 'create_event', {}
            result = self.scheduler_live.request(op)
            value = EVENT_TOKEN + len(self.events)*16
            need(result['handle'] and result['handle'] not in self.events.values(), 'separate actual event owners')
            self.events[value] = result['handle']
        else:
            op = {'CloseHandle':'close_event', 'SetEvent':'set', 'ResetEvent':'reset'}[name]
            q = dict(handle=self.events[args[0]])
            result = self.scheduler_live.request(op, **q)
            need(result == dict(value=1), 'actual owned event operation succeeded')
            value = result['value']
            if name == 'CloseHandle': del self.events[args[0]]
        self.api_calls.append(dict(kind='actual_scheduler_platform', name=name, import_slot=slot,
            target=fixture.word(self.read(slot)), sp=sp, return_va=ret, args=args, pop=pop,
            value=value, memory_outputs=outputs, new_mappings=[], native_op=op, native_request=q,
            native_result=result, wire_start=start, wire_end=len(self.scheduler_live.trace),
            void_return_normalized=manager_call))
        for key, value in dict(EAX=value, ESP=sp+4+pop, EIP=ret).items():
            self.u.reg_write(fixture.base.REGISTERS[key], value)

    def state(self):
        return dict(manager_hex=self.read(MANAGER, 0x200).hex(), node_hex=self.read(NODE, 0x80).hex(),
                    events=dict(self.events), manager_lock_live=self.manager_lock_live,
                    manager_depth=self.manager_depth, allocations=copy.deepcopy(self.allocations),
                    CRT_ledger=fixture.old.ledger(self))

    def root(self, label, entry, args=(), receiver=0, cdecl=True, stop=None, cleanup=False):
        need(len(self.steps) < 24, 'bounded independent roots')
        sp = (CLEANUP_STACK if cleanup else fixture.old.STACK) + 0xF000
        stack = struct.pack('<'+'I'*(len(args)+1), fixture.old.RETURN, *args)
        declaration = dict(va=entry, args=list(args), receiver=receiver, cdecl=cdecl,
                           stack_pointer=sp, return_address=fixture.old.RETURN,
                           stack_before_hex=self.read(sp, len(stack)).hex(), stack_after_hex=stack.hex(),
                           before_CPU=full_cpu(self.u), supplemental_cleanup=cleanup)
        self.u.mem_write(sp, stack)
        for key, value in dict(EIP=entry, ESP=sp, ECX=receiver, EFLAGS=0x202).items():
            self.u.reg_write(fixture.base.REGISTERS[key], value)
        before_cpu, before_memory = full_cpu(self.u), memory(self.u)
        before_state = self.state()
        counts, lengths = Counter(), {}
        ih, wh = hashlib.sha256(), hashlib.sha256()
        write_count = 0
        self.api_calls = []
        targets = {fixture.word(self.read(slot)):slot for slot in SLOTS}
        reached = None

        def code(uc, pc, size, _):
            nonlocal reached
            if pc == fixture.old.RETURN:
                reached = 'natural_root_return'
                uc.emu_stop()
                return
            if pc in targets:
                self.api(targets[pc])
                return
            raw = self.read(pc, size)
            need(0x400000 <= pc and pc+size <= 0x592000
                 and raw == self.image[pc-0x400000:pc-0x400000+size] and raw[0] != 0xCC,
                 'unmodified original instruction at '+hex(pc))
            if pc == stop:
                need(pc == CREATE_THREAD_CALL and raw == bytes.fromhex('ff151c225900'), 'only exact unexecuted CreateThread CALL')
                p = self.cpu()['ESP']
                argv = [fixture.word(self.read(p+i)) for i in range(0, 24, 4)]
                ptd = argv[3]
                owned, record = self.owned(ptd, 116)
                need(ptd == owned+32 and record['bytes'] == 160, 'current actual CRT PTD raw allocation')
                validate_thread_request(argv, NODE, ptd, self.read(ptd, 116))
                self.pending = dict(PC=pc, instruction_hex=raw.hex(), instruction_executed=False,
                    API_called=False, import_slot=0x59221C, import_target=fixture.word(self.read(0x59221C)),
                    args=argv, return_if_called=0x56E0C4, PTD_hex=self.read(ptd,116).hex(),
                    allocation=copy.deepcopy(record), complete_CPU=full_cpu(self.u), complete_memory=memory(self.u),
                    state=self.state(), stack_pointer=fixture.old.STACK+0xD000,
                    stack_hex=self.read(fixture.old.STACK+0xD000, 0x3000).hex())
                reached = 'unexecuted_CreateThread_CALL'
                uc.emu_stop()
                return
            need(sum_count[0] < 200000, '200000 original instruction root budget')
            sum_count[0] += 1
            counts[pc] += 1
            lengths[pc] = size
            ih.update(struct.pack('<I', pc)+raw)

        def write(uc, _access, address, size, value, _):
            nonlocal write_count
            need(not (address < 0x592000 and address+size > 0x400000), 'no original code writes')
            need(write_count < 200000, 'bounded original writes')
            pc = self.cpu()['EIP']
            write_count += 1
            wh.update(struct.pack('<III', pc, address, size))
            wh.update(self.read(address, size))
            wh.update((value & ((1 << (8*size))-1)).to_bytes(size, 'little'))

        sum_count = [0]
        h1 = self.u.hook_add(UC_HOOK_CODE, code)
        h2 = self.u.hook_add(UC_HOOK_MEM_WRITE, write)
        failure = None
        try:
            self.u.emu_start(entry, 0, timeout=30000000, count=0)
            need(reached is not None, 'root must reach declared boundary within30s')
            if stop is None:
                need(self.cpu()['EIP'] == fixture.old.RETURN and
                     self.cpu()['ESP'] == sp+4+(0 if cdecl else 4*len(args)), 'natural root return ABI')
            else:
                need(reached == 'unexecuted_CreateThread_CALL', 'exact CreateThread frontier')
        except BaseException as exc:
            failure = repr(exc)
            raise
        finally:
            self.u.hook_del(h1)
            self.u.hook_del(h2)
            self.steps.append(dict(label=label, root=declaration, before_CPU=before_cpu,
                before_memory=before_memory, before_state=before_state, after_CPU=full_cpu(self.u),
                after_memory=memory(self.u), after_state=self.state(), boundary=reached, error=failure,
                instructions=sum_count[0], instruction_sha256=ih.hexdigest(), writes=write_count,
                write_sha256=wh.hexdigest(), original_instruction_sites=[dict(PC=p,count=n,
                    hex=self.image[p-0x400000:p-0x400000+lengths[p]].hex()) for p,n in sorted(counts.items())],
                API_calls=copy.deepcopy(self.api_calls)))
        print(label, sum_count[0], 'instructions', write_count, 'writes', len(self.api_calls), 'OS leaves', flush=True)
        return self.cpu()['EAX']


def run(label):
    start = time.monotonic()
    # Authenticate the bounded 7MiB source before creating either native owner.
    fixture.inputs()
    need(sha(fixture.base.SOURCE.read_bytes()) == SOURCE_SHA, 'original executable identity')
    implementations = implementation_files()
    crt_path = ROOT/'.venv-audit'/(label+'-crt.exe')
    scheduler_path = ROOT/'.venv-audit'/(label+'-scheduler.exe')
    crt_path, crt_build = fixture.platform.build(crt_path)
    scheduler_path, scheduler_build = scheduler_platform.build(scheduler_path)
    crt = scheduler = guest = None
    error = None
    supplemental_close = None
    report = dict(schema_version=1, accepted=False, kind='fresh_independent_base_node_registration_probe',
                  implementation=identity(Path(__file__)), original=identity(fixture.base.SOURCE),
                  implementation_start=implementations,
                  native_builds=dict(CRT=crt_build, scheduler=scheduler_build),
                  unified_native_thread_owner=False,
                  native_original_executable_image=False,
                  next_native_dependency='CRT PTD and scheduler events are owned by separate headless helpers; unify executable image, pointers, events and TLS before any real original CreateThread/worker execution',
                  current_terminal_state_loaded=False, retained_heap_restored=False,
                  original_CRT_worker_created=False, original_MAIN_scheduler_connected=False,
                  cooperative_wait_executed=False, outer_result_consumed=False, complete_battle_exit=False,
                  rewards_or_school_executed=False, independent_full_replay=False)
    try:
        crt = fixture.platform.Live(crt_path)
        scheduler = scheduler_platform.Live(scheduler_path)
        report['native_owners'] = dict(CRT_pid=crt.process.pid, scheduler_pid=scheduler.process.pid,
                                      separate_processes=crt.process.pid != scheduler.process.pid)
        need(report['native_owners']['separate_processes'], 'distinct declared CRT and scheduler owners')
        report['hello'] = dict(CRT=copy.deepcopy(crt.hello), scheduler=copy.deepcopy(scheduler.hello))
        need(crt.hello['heap'] == crt.hello['critical'] == 0 and scheduler.hello['thread_created'] is False,
             'empty fresh native owners with no worker')
        guest = Guest(crt, scheduler)
        guest.root('original_heap_initialization', 0x57B9D0, (1,))
        guest.root('original_static_lock_initialization', 0x576F60)
        guest.root('original_manager_constructor', 0x421540, receiver=MANAGER, cdecl=False)
        guest.root('original_manager_buckets', 0x421660, receiver=MANAGER, cdecl=False)
        guest.root('original_base_node_constructor', 0x422290, receiver=NODE, cdecl=False)
        untouched_thread_fields = guest.read(NODE+0x20, 8)
        guest.root('original_base_node_registration', 0x4216C0, (NODE,0,0), MANAGER, False)
        guest.root('original_first_scan_to_CreateThread', 0x4217C0, receiver=MANAGER,
                   cdecl=False, stop=CREATE_THREAD_CALL)
        need(len(guest.allocations) == 1 and len(guest.events) == 2 and guest.manager_depth == 0,
             'complete original registration dependency resources')
        need(guest.read(NODE+0x20,8) == untouched_thread_fields,
             'thread handle/ID fields retain declared bytes until real CreateThread')
        report['uninitialized_thread_fields'] = dict(before_hex=untouched_thread_fields.hex(),
            pending_hex=guest.read(NODE+0x20,8).hex(), interpreted_as_live_handles=False)
        pending = copy.deepcopy(guest.pending)
        ptd = pending['args'][3]
        guest.root('supplemental_original_PTD_free', 0x56F3B0, (ptd,2), cleanup=True)
        guest.root('supplemental_original_node_unlink', 0x421D50, (NODE,), MANAGER, False, cleanup=True)
        token = fixture.word(guest.read(NODE+0x1C))
        native = guest.events[token]
        wire = len(scheduler.trace)
        result = scheduler.request('close_event', handle=native)
        need(result == dict(value=1), 'supplemental close of observed current unstarted node event')
        del guest.events[token]
        supplemental_close = dict(guest_token=token, native_handle=native, result=result, wire_index=wire,
            reason='no worker established; explicit owner cleanup, not original worker completion')
        guest.root('supplemental_original_base_destructor', 0x4222D0, receiver=NODE, cdecl=False, cleanup=True)
        guest.root('supplemental_original_manager_destructor', 0x4215F0, receiver=MANAGER, cdecl=False, cleanup=True)
        guest.root('original_static_lock_teardown', 0x576FA0, cleanup=True)
        guest.root('original_heap_teardown', 0x57BA60, cleanup=True)
        need(not guest.allocations and not guest.criticals and not guest.events and
             not guest.manager_lock_live and guest.manager_depth == 0, 'all current resources released by declared owners')
        need(guest.read(pending['stack_pointer'],0x3000).hex() == pending['stack_hex'],
             'suspended original scan stack unchanged by separate cleanup roots')
        report['mechanism_to_CreateThread_verified'] = True
        report['supplemental_cleanup_preserved_suspended_stack'] = True
    except BaseException as exc:
        error = repr(exc)
    finally:
        report['error'] = error
        report['supplemental_node_event_close'] = supplemental_close
        if guest is not None:
            report.update(declaration=guest.declaration, steps=guest.steps, frontier=guest.pending,
                          allocation_history=guest.history, final_state=guest.state())
        for key, live in (('CRT', crt), ('scheduler', scheduler)):
            if live is not None:
                try:
                    result = live.close()
                    need(result.get('forced_cleanup') is False, 'normal explicit native cleanup')
                    report[key+'_cleanup'] = result
                except BaseException as exc:
                    report[key+'_cleanup_error'] = repr(exc)
                    report['error'] = report['error'] or repr(exc)
                report[key+'_native_trace'] = live.trace
                report[key+'_exit'] = getattr(live, 'exit_code', None)
        report['normal_cleanup'] = report['error'] is None and all(
            report.get(k+'_cleanup',{}).get('all_owned_resources_released') is True for k in ('CRT','scheduler'))
        report['implementation_end'] = implementation_files()
        report['implementation_unchanged'] = all(report['implementation_end'].get(k) == v
                                                for k,v in implementations.items())
        if not report['implementation_unchanged']:
            report['error'] = report['error'] or 'loaded implementation changed during diagnostic'
            report['normal_cleanup'] = False
        report['duration_seconds'] = round(time.monotonic()-start,3)
    return report


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--label', required=True)
    p.add_argument('--out', required=True)
    a = p.parse_args()
    need(a.label and all(c.isalnum() or c in '-_' for c in a.label), 'simple fresh helper label')
    out = Path(a.out).resolve()
    need(out.is_relative_to(ROOT/'analysis') and not out.exists(), 'fresh local report path')
    result = run(a.label)
    raw = json.dumps(result,separators=(',',':')).encode('utf8')
    need(len(raw) <= 10*1024*1024, 'bounded uncompressed evidence')
    data = gzip.compress(raw, mtime=0)
    with out.open('xb') as stream: stream.write(data)
    print(json.dumps(dict(report=identity(out), normal_cleanup=result['normal_cleanup'], error=result['error'])), flush=True)
    if result['error']: raise SystemExit(1)


if __name__ == '__main__':
    main()
