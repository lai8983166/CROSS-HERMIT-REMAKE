"""Fresh early unit inputs and original terminal frontend continuation.

Old validators remain frozen. Their fixed cumulative-prefix observations are
explicitly rebased here because the declared initial record/resources change;
they are not reported as old-digest matches. The new transaction proof must
independently replay the entire new original execution before acceptance.
"""
import ast
import contextlib
import copy
import hashlib
import importlib
import inspect
import json
import struct
import sys
import textwrap
import types
from unittest.mock import patch

from tools import terminal_battle_exit_emulation as previous
from tools import terminal_unit_frontends_records as records
from tools import terminal_unit_frontends_images as images
from tools import terminal_unit_frontends_minimap as minimap
from tools.terminal_unit_frontends_trace import Recorder

ROOT = previous.ROOT
WAIT = 0x422360
UNIT_FRAME_GEOMETRY = 0x41ED00
UNIT_LIST_CURSOR = previous.CTRL + 0x1160C0
APPLICATION_INPUT = images.PATH_OWNER + 0x180
LEGACY_INPUT = previous.INPUT
CLOCK_INPUT_PATH = 'analysis/terminal-unit-frontends-clock-inputs-v1-20261103.json'
CLOCK_INPUT_SHA = '31e76e5ea16c43a038ba0e916a6b6da521120205ed89d1fc734c8a1de73a4d48'
PREFLIGHT_MODULES = tuple('tools.terminal_' + name + '_emulation' for name in (
    'next_dialogue', 'multiline', 'last_dialogue', 'script_exit',
    'task_completion', 'battle_stage_handoff', 'battle_exit'))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def clock_inputs():
    raw = (ROOT / CLOCK_INPUT_PATH).read_bytes()
    if sha(raw) != CLOCK_INPUT_SHA:
        raise ValueError('fixed captured raw clock inputs changed')
    return json.loads(raw)['cases']


def original_post_unit_resource_initializer():
    """Move exactly two original CRT roots earlier; retain the rest verbatim."""
    original = previous.overlay.OverlayMachine.initialize_resources
    text = textwrap.dedent(inspect.getsource(original))
    tree = ast.parse(text)
    function = tree.body[0]
    labels = []
    for stmt in function.body[:2]:
        if not isinstance(stmt, ast.Expr) or not isinstance(stmt.value, ast.Call):
            raise ValueError('expected the two original CRT root expressions')
        call = stmt.value
        if not isinstance(call.func, ast.Attribute) or call.func.attr != 'resource_root':
            raise ValueError('only original resource roots may move')
        labels.append(ast.literal_eval(call.args[0]))
    if labels != ['original_heap_initialization', 'original_lock_initialization']:
        raise ValueError('unexpected original CRT initialization order')
    function.body = function.body[2:]
    scope = dict(original.__globals__)
    exec(compile(ast.fix_missing_locations(tree), __file__ + ':moved-CRT-roots', 'exec'), scope)
    return scope['initialize_resources'], dict(original_source_sha256=sha(text.encode()),
                                              roots_moved_before_first_binding=labels,
                                              remaining_original_statements_unchanged=True)


POST_UNIT_RESOURCES, CRT_ROOT_MOVE = original_post_unit_resource_initializer()
# Instruction blocks observed after the first v5 scene guard. The disposable
# continuation verified fetched bytes and stopped before the cooperative wait.
SCENE_TAIL_RANGES = (
    (0x40A330, 0x40A387), (0x40A390, 0x40A3F7), (0x427B70, 0x427B98),
    (0x427BC7, 0x427BE6), (0x427BF0, 0x427C1A), (0x427C35, 0x427C3C),
    (0x454F50, 0x454F94), (0x456650, 0x45668B), (0x45679E, 0x4567AF),
    (0x466910, 0x46696E), (0x46697F, 0x4669BF), (0x466A68, 0x466AAB),
    (0x46DA80, 0x46DB1B), (0x46DB20, 0x46DB4D), (0x46DB52, 0x46DB62),
    (0x46DB67, 0x46DB73), (0x46DB78, 0x46DB8B), (0x46DB90, 0x46DC1D),
    (0x46DD7E, 0x46DD90), (0x46DE24, 0x46DE44), (0x46DEB1, 0x46DEB3),
    (0x46DEF3, 0x46DF6F), (0x46E0F0, 0x46E123), (0x46E128, 0x46E13B),
    (0x46E140, 0x46E253), (0x46E2C8, 0x46E2D3), (0x46E348, 0x46E358),
    (0x46E38B, 0x46E3C9), (0x46E3D0, 0x46E400), (0x46E405, 0x46E417),
    (0x46E41C, 0x46E46E), (0x46E486, 0x46E4B8), (0x46E4C0, 0x46E51B),
    (0x472A70, 0x472A9C), (0x472AAB, 0x472AAD), (0x472B14, 0x472B27),
    (0x481B90, 0x481BBB), (0x481BBF, 0x481BD7), (0x481BD9, 0x481BDD),
    (0x481BE2, 0x481BE9), (0x482150, 0x482186), (0x4821F7, 0x482208),
    (0x491680, 0x4916B4), (0x491882, 0x491895), (0x4936A0, 0x4936D5),
    (0x493B80, 0x493BCD), (0x493C2A, 0x493C40), (0x4944A0, 0x4944DD),
    (0x494501, 0x494553), (0x494597, 0x4945AC), (0x497C90, 0x497CC7),
    (0x497CFB, 0x497D0E), (0x499B80, 0x499BB7), (0x499C72, 0x499C83),
    (0x49A600, 0x49A63B), (0x49A99D, 0x49A9AE), (0x49AB60, 0x49AB8E),
    (0x49AD2E, 0x49AD41), (0x49BEB0, 0x49BEE1), (0x49BEE6, 0x49BF17),
    (0x49C302, 0x49C311), (0x49C370, 0x49C37F), (0x49C3DE, 0x49C3E0),
    (0x49C3E5, 0x49C3F9), (0x49C850, 0x49C881), (0x49C998, 0x49C9A9),
    (0x49CCE0, 0x49CD1A), (0x49CD26, 0x49CD41), (0x49CD4B, 0x49CD61),
    (0x49CD90, 0x49CDA1), (0x49CDC0, 0x49CE33), (0x49CE3B, 0x49CE4F),
    (0x49CE61, 0x49CE89), (0x49D160, 0x49D1A3), (0x49D9AB, 0x49D9C1),
)

# Original scene descendants after the unit image lookup and MP division.
# Keep the missing-table and null-unit assertion branches outside these ranges.
RANGES = previous.RANGES + images.EXTRA_RANGES + minimap.EXTRA_RANGES + (
    # 40B305 reads the current frame geometry.
    (UNIT_FRAME_GEOMETRY, 0x41ED26), (0x41ED57, 0x41ED76),
    # 46D03D checks unit status, then 46D052 may submit a COMMON icon packet.
    (0x469510, 0x469523), (0x469547, 0x4695A8), (0x46D210, 0x46D335),
    # 46D1AF submits the unit marker to the minimap.
    (0x440FE0, 0x441153),
) + SCENE_TAIL_RANGES
ALLOWED = frozenset(at for lo, hi in RANGES for at in range(lo, hi))
REFERENCE = types.FunctionType(previous.REFERENCE.__code__,
                              dict(previous.REFERENCE.__globals__, RANGES=RANGES))


class UnitPhaseObservers:
    """Use the frozen platform/base guards when terminal observers are inactive.

    Unit loading/destruction precedes or follows terminal execution. Original
    guest code, global instruction/write guards and platform dispatch remain;
    no inactive dialogue observer can alter guest execution in these phases.
    """
    def code(self, uc, at, size, context):
        if (getattr(self, 'unit_phase', None) or getattr(self,'minimap_initializing',False)
                or getattr(self,'minimap_cleaning',False)):
            if at == 0x424F80:
                raise ValueError('original assertion in unit resource phase')
            return previous.overlay.OverlayMachine.code(self, uc, at, size, context)
        return super().code(uc, at, size, context)

    def write_hook(self, uc, access, at, size, value, context):
        if (getattr(self, 'unit_phase', None) or getattr(self,'minimap_initializing',False)
                or getattr(self,'minimap_cleaning',False)):
            return previous.overlay.OverlayMachine.write_hook(self, uc, access, at, size, value, context)
        return super().write_hook(uc, access, at, size, value, context)


class UnitFrontendMachine(minimap.MinimapMixin, images.ImagesMixin, UnitPhaseObservers, previous.BattleExitMachine):
    source_code = types.FunctionType(previous.BattleExitMachine.source_code.__code__,
                                   dict(previous.BattleExitMachine.source_code.__globals__,
                                        ALLOWED=ALLOWED, REFERENCE=REFERENCE))

    def __init__(self, *args, **kwargs):
        self.snapshot_values = {}
        self.execution_recorder = None
        self.rebased_prefixes = []
        self.unit_CRT_prepared = False
        self.unit_cleanup_in_progress = False
        self.unit_cleanup_done = False
        self.application_text_query_count = 0
        self.application_text_receivers = {}
        super().__init__(*args, **kwargs)
        pointer = previous.terminal.RECORD + 0x100
        existing = self.read(pointer, 0x100)
        derived = records.derive_target_record(self.combat_input['job'])
        overlay = records.apply_declared_record_fields(bytes.fromhex(derived['record_hex']),
                                                       existing, records.recommended_target_spans())
        self.uc.mem_write(pointer, bytes.fromhex(overlay['record_hex']))
        self.unit_record_input = dict(pointer=pointer, derivation=derived, declared_fields=overlay,
                                      applied_before_first_original_binding=True)
        legacy_space = self.space
        self.configure_unit_inputs()
        # The frozen terminal namespaces describe their own GPU identities.
        # Unit caches use a disjoint typed pool and retain a separate complete
        # ledger; their COM methods are dispatched through the same actual CPU.
        # Copy only the small initial device ledger, never textures or memory.
        legacy_space.native_to_guest = dict(legacy_space.native_to_guest)
        legacy_space.guest_to_native = dict(legacy_space.guest_to_native)
        self.space = legacy_space
        self.unit_input_contract['separate_unit_identity_owner'] = True
        self.configure_minimap_inputs()
        self.mutable.append((UNIT_LIST_CURSOR, UNIT_LIST_CURSOR+4))
        declared_input = self.read(LEGACY_INPUT, 0x680)
        if self.read(APPLICATION_INPUT, 0x680) != bytes(0x680):
            raise ValueError('fresh separated application input extent')
        self.uc.mem_write(APPLICATION_INPUT, declared_input)
        self.application_text_contract = dict(application_global=0x7A4A00,
            application=images.PATH_OWNER,input_subobject=APPLICATION_INPUT,
            buffer=images.PATH_OWNER+0x6A8,original_this_local=-4,
            original_member_offset=0x528,original_caller=0x425A7E,
            import_slot=0x5922C4,declared_initial_empty=True,
            declared_initial_input_bytes=len(declared_input),
            declared_initial_input_sha256=sha(declared_input),
            former_aliased_input=LEGACY_INPUT, reset_receiver=APPLICATION_INPUT,
            request_member_offset=0x630, original_request=0x425ED0,
            original_frame_reset=0x425DE0,
            full_original_application_or_input_constructor_executed=False,
            nonempty_or_active_IME_path_supported=False)
        self.application_text_target = self.get(0x5922C4)
        self.initial_platform = copy.deepcopy(dict(CRT=self.live.hello,
                                                   GPU=self.gpu.hello,
                                                   device=self.gpu.device))

    def snapshot(self):
        # Read current bytes every time; immutable cached strings avoid retaining
        # hundreds of identical copies of newly resident unit surfaces in RAM.
        # This is content reuse, never a dirty-bit shortcut or a restored state.
        rows = []
        for a, b, permission in self.uc.mem_regions():
            raw = bytes(self.uc.mem_read(a, b-a+1))
            key = (a, len(raw), sha(raw))
            value = self.snapshot_values.get(key)
            if value is None:
                value = raw.hex()
                self.snapshot_values[key] = value
            rows.append(dict(pointer=a, bytes=len(raw), hex=value))
        return rows

    def code(self, uc, at, size, context):
        rec = self.execution_recorder
        if rec is not None and not rec.begin_code(at):
            return
        try:
            if (at == self.application_text_target and self.get(self.getreg('ESP')) == 0x425A7E):
                sp,bp = self.getreg('ESP'),self.getreg('EBP')
                actual_this = self.get(bp-4)
                if (self.get(0x5922C4) != at or actual_this != self.get(0x7A4A00)+0x180 or
                        self.get(sp+4) != actual_this+0x528 or
                        self.read(actual_this+0x528,1) != b'\0'):
                    raise ValueError('original application input receiver/member query contract')
                super().code(uc, at, size, context)
                self.application_text_query_count += 1
                key=hex(actual_this)
                self.application_text_receivers[key]=self.application_text_receivers.get(key,0)+1
            else:
                super().code(uc, at, size, context)
        finally:
            if rec is not None:
                rec.end_code(at)

    def write_hook(self, uc, access, at, size, value, context):
        if at < UNIT_LIST_CURSOR+4 and at+size > UNIT_LIST_CURSOR:
            if (at, size, self.getreg('EIP')) != (UNIT_LIST_CURSOR, 4, 0x427BD0):
                raise ValueError('original unit list iteration cursor write')
        rec = self.execution_recorder
        if rec is not None:
            rec.guest_write(self.getreg('EIP'), at, size, value)
        super().write_hook(uc, access, at, size, value, context)

    def initialize_resources(self):
        if not self.unit_CRT_prepared:
            raise ValueError('original CRT roots must run before natural unit loading')
        return POST_UNIT_RESOURCES(self)

    def boundary_wire_counts(self):
        native = getattr(self, 'native', None)
        return dict(CRT=len(self.live.trace), GPU=len(self.gpu.trace),
                    GDI=len(self.name_platform.trace), TLS=len(native.trace) if native else 0)

    def boundary_identity(self, pc):
        # This label is diagnostic. The independent validator must establish
        # the actual import/COM caller and arguments from replay RAM/CPU.
        if pc in self.api_targets:
            return dict(kind='CRT', import_slot=self.api_targets[pc])
        if pc in self.methods:
            return dict(kind='GPU', vtable_slot=self.methods[pc])
        if pc in self.gdi_targets:
            return dict(kind='GDI', import_slot=self.gdi_targets[pc])
        return dict(kind='input_or_legacy_platform', pc=pc)

    def resource_root(self, label, entry, args=(), receiver=0, cdecl=False):
        if label == 'supplemental_original_group20_destructor' and not self.unit_cleanup_done:
            if self.unit_cleanup_in_progress:
                raise ValueError('recursive unit teardown')
            self.unit_cleanup_in_progress = True
            try:
                self.destroy_minimap()
                self.destroy_unit_images()
                self.unit_cleanup_done = True
            finally:
                self.unit_cleanup_in_progress = False
        return super().resource_root(label, entry, args, receiver, cdecl)

    def bex_segment(self, label, entry, stop=previous.RETURN, root=None):
        if label == 'original_scene_loop':
            if entry != 0x4539B0:
                raise ValueError('only the original scene loop resumes to wait')
            stop = WAIT
        return super().bex_segment(label, entry, stop, root)

    def capture_frontier(self):
        sp, bp = self.getreg('ESP'), self.getreg('EBP')
        outer = previous.STACK + 0xF000 - 4
        if (self.getreg('EIP'), self.get(sp), self.getreg('ECX')) != (WAIT, 0x453CB5, previous.TASK):
            raise ValueError('expected natural first scene cooperative wait CALL/receiver')
        if self.get(outer-8) != 1 or self.get(outer+4) != previous.RETURN:
            raise ValueError('original saved scene result and outer return must remain suspended')
        return dict(kind='cooperative_wait', entry=WAIT, first_instruction_executed=False,
                    original_wait_reached=True, original_wait_body_executed=False,
                    frame_EBP=bp, outer_frame_EBP=outer, caller=self.get(sp),
                    args=[self.get(sp+4)], local_result=1,
                    root_return_address=previous.RETURN, stack_pointer=previous.STACK,
                    stack_bytes=0x20000, stack_hex=self.read(previous.STACK,0x20000).hex(),
                    outer_result_consumed=False, terminal_battle_exit_executed=False)

    def prepare_and_run(self):
        rec = Recorder(self)
        self.execution_recorder = rec
        try:
            self.initialize_unit_CRT()
            self.unit_CRT_prepared = True
            self.initialize_minimap()
            with application_input_binding():
                row = self.run()
            row['unit_frontends'] = dict(record_input=self.unit_record_input,
                                         image_input=self.unit_image_result(),
                                         minimap_input=self.minimap_result(),
                                         application_text=dict(contract=self.application_text_contract,
                                                               calls=self.application_text_query_count,
                                                               receivers=self.application_text_receivers),
                                         CRT_root_move=CRT_ROOT_MOVE,
                                         rebased_prefixes=self.rebased_prefixes,
                                         execution=rec.finish(),
                                         initial_platform=self.initial_platform,
                                         old_cumulative_digests_reused=False)
            return row
        finally:
            self.execution_recorder = None
            rec.detach()


@contextlib.contextmanager
def rebased_source_observers():
    """Record old/new prefix values explicitly, without forging an old match."""
    with contextlib.ExitStack() as stack:
        for name in PREFLIGHT_MODULES:
            module = importlib.import_module(name)
            old = module.validate_parent_prefix

            def observe(machine, module=module, old=old):
                case = machine.live_input['name']
                frozen = module.fixed_parent_forward_summaries()[case]
                actual = machine.mark()
                record = dict(case=case, fixed_proof_sha256=module.PARENT_PROOF_SHA,
                              expected=frozen, actual=actual, old_digest_reused=False,
                              observation_adapter='new early source-derived inputs require new proof',
                              original_observer_source_sha256=sha(inspect.getsource(old).encode()))
                machine.rebased_prefixes.append(dict(stage=module.__name__, **record))
                return record

            stack.enter_context(patch.object(module, 'validate_parent_prefix', observe))
        yield


@contextlib.contextmanager
def application_input_binding():
    """Use the original application subobject for both request and reset.

    Rebind the inherited host root/observer address throughout this lifetime.
    The original 425ED0 request and 425DE0 reset instructions write the byte.
    """
    modules = [module for name,module in list(sys.modules.items())
               if name.startswith('tools.terminal_') and module is not None
               and getattr(module,'INPUT',None)==LEGACY_INPUT]
    with contextlib.ExitStack() as stack:
        for module in modules:
            stack.enter_context(patch.object(module,'INPUT',APPLICATION_INPUT))
        yield


def run_case(case, CRT_helper, GPU_helper, ticks=None, scene_failure=None):
    """Own a new native lifetime; failures retain only bounded caller context."""
    fixed = clock_inputs()[case['name']]
    ticks = list(fixed) if ticks is None else ticks
    if ticks != fixed:
        raise ValueError('only the pinned captured clock input stream is admitted')
    live = images.CRTLive(CRT_helper)
    gpu = None
    machine = None
    try:
        gpu = previous.overlay.platform.OverlayGPU(GPU_helper)
        machine = UnitFrontendMachine(case, live, gpu, ticks)
        with rebased_source_observers():
            row = machine.prepare_and_run()
        row['GDI_trace'] = machine.name_platform.trace
        row.update(CRT_cleanup=live.close(), GPU_cleanup=gpu.close(),
                   CRT_trace=live.trace, GPU_trace=gpu.trace,
                   CRT_exit=live.exit_code, GPU_exit=gpu.process.returncode)
        return row
    except Exception as error:
        # A caller may serialize this small context. Never attach full memory,
        # texture pixels, whole case rows or recursively nested parent reports.
        error.unit_frontends_context = dict(
            case=case['name'], CPU=machine.cpu() if machine else None,
            last_CRT=[dict(slot=r.get('slot'), return_va=r.get('return_va'))
                      for r in getattr(machine, 'crt_apis', [])[-3:]],
            resources=[r.get('label') for r in getattr(machine, 'resource_steps', [])[-5:]],
            native_operations=dict(CRT=len(live.trace), GPU=len(gpu.trace) if gpu else 0))
        if machine is not None:
            sp=error.unit_frontends_context['CPU']['ESP']
            if previous.STACK <= sp <= previous.STACK+0x20000-64:
                error.unit_frontends_context['stack_head_hex']=machine.read(sp,64).hex()
            error.unit_frontends_context['input_requests']={
                hex(pointer):machine.get(pointer+0x630,'B')
                for pointer in (LEGACY_INPUT,APPLICATION_INPUT)}
            if scene_failure is not None and machine.bex_active and machine.bex_label == 'original_scene_loop':
                try:
                    scene_failure(machine)
                except Exception as checkpoint_error:
                    error.unit_frontends_context['checkpoint_error'] = repr(checkpoint_error)
        raise
    finally:
        if machine is not None:
            machine.name_platform.close()
        if not live.closed:
            live._terminate()
        if gpu is not None and not gpu.closed:
            gpu._terminate()
