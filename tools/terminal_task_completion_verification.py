"""Independent original task phase4 resource release and phase5 handshake."""
from tools.terminal_script_exit_verification import *
from tools import terminal_script_exit_verification as previous_stage
from tools import terminal_task_completion_emulation as e
import ast,inspect,textwrap
ROOT=e.ROOT
PARENT_ACCEPTANCE=e.PARENT_ACCEPTANCE;PARENT_ACCEPTANCE_SHA=e.PARENT_ACCEPTANCE_SHA
PARENT_SOURCE=e.PARENT_SOURCE;PARENT_SOURCE_SHA=e.PARENT_SOURCE_SHA
PARENT_PROOF=e.PARENT_PROOF;PARENT_PROOF_SHA=e.PARENT_PROOF_SHA
IMPLEMENTATIONS=('tools/terminal_task_completion_emulation.py','tools/terminal_task_completion_verification.py','tools/terminal_task_completion_preservation.py','tools/tests/test_terminal_task_completion.py','tools/tests/test_terminal_task_completion_source.py')
load_report=previous_stage.load_report
native_previous_stage=previous_stage.previous_stage
EXTRA_RANGES=((0x454EE0,0x454F4D),)
GROUPS=tuple(i for i in range(10,89) if i!=20)
EVENT_ABI={0x497C50:(0,0),0x454EE0:(0,0),0x41F4E0:(1,4),0x41F2A0:(1,4),0x41F890:(0,0),0x56DE40:(4,16),0x428AD0:(1,0),0x403730:(0,0),0x403A00:(0,0),0x41F710:(0,0),0x454C40:(0,0),0x457830:(0,0),0x497AA0:(0,0),0x498310:(0,0)}

def new_resources(row):
 d=row['terminal_task_completion'];return [r for r in d['resources'] if r['create_wire_index']>=d['prefix']['GPU_wire']]

def branch(name):return dict(previous_stage.branch(name),role=None,commands=[])

@lru_cache(maxsize=1)
def parent_report():
 for path,want in ((PARENT_ACCEPTANCE,PARENT_ACCEPTANCE_SHA),(PARENT_PROOF,PARENT_PROOF_SHA),(PARENT_SOURCE,PARENT_SOURCE_SHA)):
  h=hashlib.sha256()
  with (ROOT/path).open('rb') as f:
   for block in iter(lambda:f.read(1048576),b''):h.update(block)
  need(h.hexdigest()==want,'fixed accepted script exit '+path)
 return load_report(ROOT/PARENT_SOURCE)

def parent_case(row):return next(x for x in parent_report()['cases'] if x['input']==row['input'])
def accepted_clock_inputs():return {r['input']['name']:[a['result'] for a in r['APIs'] if a['name']=='GetTickCount'] for r in parent_report()['cases']}

@lru_cache(maxsize=1)
def parent_trace_summaries():
 raw=(ROOT/PARENT_PROOF).read_bytes();need(sha(raw)==PARENT_PROOF_SHA,'fixed compact script exit proof')
 return {c['name']:c['forward_summary']['full_cumulative'] for c in json.loads(raw)['cases']}

def prefix_trace(row):
 d=row['terminal_task_completion'];name=row['input']['name'];want=parent_trace_summaries()[name]
 need(d['before']['trace']==want,'all four parent cumulative fields unchanged')
 need(d['prefix_preflight']==dict(case=name,fixed_proof_sha256=PARENT_PROOF_SHA,expected=want,actual=want),'entire fixed prefix preflight')

def forward_only(row):
 d=row['terminal_script_exit'];end=row['script_exit_cleanup'][0]['leaves'][0]
 return dict(d,leaves=d['leaves'][:end],GPU_APIs=[c for c in d['GPU_APIs'] if c['wire_index']<d['forward_wire_end']])

def prefix(row,old=None,replay=True):
 old=parent_case(row) if old is None else old;d=row['terminal_task_completion'];fixed=old['terminal_script_exit']['final']
 for key in ('memory','CPU','state','queue','trace'):need(d['before'][key]==fixed[key]==row['terminal_script_exit']['final'][key],'whole fixed original parent '+key)
 need(d['before']['local_trace']==mark_zero(),'new local trace starts at zero')
 need(guest(forward_only(row))==guest(forward_only(old)),'complete original script exit forward retained')
 need(all(row['blobs'].get(k)==old['blobs'][k] for k in page_keys(forward_only(old))),'every parent intermediate memory page retained')
 p=d['prefix'];need((p['GPU_wire'],p['CRT_wire'])==(old['terminal_script_exit']['forward_wire_end'],old['terminal_script_exit']['CRT_forward_wire_end']),'whole parent forward wire boundary')
 n=sum(a['wire_end']<=p['CRT_wire'] for a in old['CRT_APIs'])
 for key,length in dict(CRT_APIs=n,task_APIs=len(old['task_APIs']),task_calls=len(old['task_calls']),task_writes=len(old['task_writes']),APIs=len(old['APIs'])).items():need(p[key]==length and guest(row[key][:length])==guest(old[key][:length]),'complete original prefix '+key)
 need(p['resource_steps']==len(old['resource_initialization']) and guest(row['resource_initialization'][:p['resource_steps']])==guest(old['resource_initialization']) and p['extra_counts']==old['extra_original_instruction_counts'] and len(row['APIs'])==p['APIs'],'fixed complete initialization and clocks')
 prior=previous_stage.prefix(row,replay=replay);counts=previous_stage.execute_with_events(previous_stage.Replay(row)) if replay else None
 return dict(fixed_acceptance_sha256=PARENT_ACCEPTANCE_SHA,fixed_source_sha256=PARENT_SOURCE_SHA,fixed_proof_sha256=PARENT_PROOF_SHA,whole_parent_forward_equal=True,earlier=prior,independent_script_exit_forward=counts,no_historical_cleanup_projection=True)

def event_state(replay):
 return dict(VM_PC=num(replay.read(e.VM+28,4),0),VM_wait=num(replay.read(e.VM+32,2),0,'H'),VM_active=num(replay.read(e.VM+4,1),0,'B'),accounting=num(replay.read(0x765720,4),0),task_hex=replay.read(e.TASK+0x44,0x20).hex(),work_hex=replay.read(e.overlay.WORK,0x2500).hex(),task_full_hex=replay.read(e.TASK,0x190).hex(),resource_table_hex=replay.read(e.MAIN+0x844,0x800).hex())

def capture_query(replay,at,cpu):return dict(entry=at,CPU=cpu,receiver=cpu['ECX'],stack_hex=replay.read(cpu['ESP'],68).hex(),state=event_state(replay))
def capture_command(replay,p,op,n):return dict(PC=num(replay.read(e.VM+28,4),0),opcode=op,bytes=n,source_pointer=p,raw_hex=replay.read(p,n).hex())

def observer_code(fn,scope):
 text=textwrap.dedent(inspect.getsource(fn));original=ast.parse(text);changed=copy.deepcopy(original);edits={};masks=[]
 def payload(n):return n.func.value.id if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and isinstance(n.func.value,ast.Name) and n.func.value.id in ('queries','commands') and n.func.attr=='append' else None
 for n in ast.walk(changed):
  kind=payload(n)
  if kind:
   need(len(n.args)==1 and not n.keywords,'one exact observation payload');args=('self','at','cpu') if kind=='queries' else ('self','p','op','n');n.args=[ast.copy_location(ast.Call(func=ast.Name(id='capture_query' if kind=='queries' else 'capture_command',ctx=ast.Load()),args=[ast.Name(id=a,ctx=ast.Load()) for a in args],keywords=[]),n.args[0])];edits[kind]=edits.get(kind,0)+1
  if isinstance(n,ast.If) and any(isinstance(x,ast.Call) and isinstance(x.func,ast.Attribute) and isinstance(x.func.value,ast.Name) and x.func.value.id=='observed' and x.func.attr=='append' for x in ast.walk(ast.Module(body=n.body,type_ignores=[]))):
   # The single finite write observer additionally records the resource table.
   need('e.VM' in ast.unparse(n.test) and 'e.TASK' in ast.unparse(n.test),'exact inherited selected-write observer')
   masks.append(('write_observer',ast.dump(n.test,include_attributes=False)));n.test=ast.BoolOp(op=ast.Or(),values=[n.test,ast.parse('e.MAIN+0x844<=at<e.MAIN+0x1044',mode='eval').body]);edits['write_observer']=edits.get('write_observer',0)+1
  if isinstance(n,ast.Compare) and ast.unparse(n)=='len(bindings) == 3':
   masks.append(('input_partition',ast.dump(n,include_attributes=False)));n.comparators=[ast.Constant(value=0)];edits['input_partition']=edits.get('input_partition',0)+1
 need(edits==dict(queries=1,commands=1,write_observer=1,input_partition=1),'exact four declared stage observer/input adaptations')
 def normalized(tree):
  tree=copy.deepcopy(tree)
  for n in ast.walk(tree):
   if payload(n):n.args=[ast.Constant(value='DECLARED_PAYLOAD')]
   if isinstance(n,ast.If) and isinstance(n.test,ast.BoolOp) and 'observed.append' in ast.unparse(ast.Module(body=n.body,type_ignores=[])):n.test=ast.Constant(value='DECLARED_WRITE_OBSERVER')
   if isinstance(n,ast.Compare) and ast.unparse(n).startswith('len(bindings) == '):n.comparators=[ast.Constant(value='DECLARED_NO_INPUT_CONTRACT')]
  return ast.dump(tree,include_attributes=False)
 a,b=normalized(original),normalized(changed);need(a==b,'entire original replay AST equal outside four declared stage contract observations')
 scope.update(capture_query=capture_query,capture_command=capture_command);exec(compile(ast.fix_missing_locations(changed),__file__+':stage-observer','exec'),scope)
 return scope[fn.__name__].__code__,dict(frozen_source_sha256=sha(text.encode()),unchanged_execution_AST_sha256=sha(a.encode()),declared_changes=edits,zero_new_input_bindings=True,resource_table_write_observation_added=True,original_machine_events_filtered=False)

def cleanup_plan(row):
 old=parent_case(row);d=row['terminal_task_completion'];memory=d['final']['memory'];keys=('label','entry','args','receiver','cdecl');actual=[];skips=[]
 for r in old['cleanup_steps']:
  item={k:r[k] for k in keys}
  if r['entry']==0x41F4E0:
   slot=r['receiver']+r['args'][0]*8;raw=read(memory,slot,8)
   if raw==bytes(8):
    need(r['args'][0] in GROUPS,'only originally freed non20 containers skipped');skips.append(dict(item,slot=slot,slot_hex=raw.hex(),record_pointer=0,reason='original forward resource loop already cleared this container'));continue
  actual.append(item)
 need(row['task_completion_cleanup_skips']==skips,'every skipped container derived from fixed plan and actual final bytes')
 need([{k:r[k] for k in keys} for r in row['task_completion_cleanup']]==actual,'all actual cleanup roots exactly fixed plan minus proven already cleared banks')
 return dict(cleanup_steps=actual)

def bind_replay(fn,mode):
 routing={'terminal_followup':'terminal_task_completion','followup_cleanup':'task_completion_cleanup','terminal_last_dialogue':'terminal_task_completion','last_dialogue_cleanup':'task_completion_cleanup','terminal_script_exit':'terminal_task_completion','script_exit_cleanup':'task_completion_cleanup'}
 def constants(code):return code.replace(co_consts=tuple(constants(v) if isinstance(v,types.CodeType) else routing.get(v,v) if type(v)is str else v for v in code.co_consts))
 scope=dict(fn.__globals__,**globals());scope['Uc']=source_image_uc;code=fn.__code__
 if mode=='execute':code,audit=observer_code(fn,scope);scope['OBSERVER_SCHEMA_AUDIT']=audit
 if mode=='cleanup':scope['parent_case']=cleanup_plan
 return types.FunctionType(constants(code),scope,closure=fn.__closure__)

class Replay(previous_stage.Replay):
 _initialize=bind_replay(previous_stage.Replay._initialize,'initialize')
 def __init__(self,row,refs=None):
  need(len(row['terminal_task_completion']['frames'])==2 and row['terminal_task_completion']['bindings']==[],'exact two-frame zero-new-input replay contract');partitions=source_image_partitions(row['terminal_task_completion']['before']['memory']);self._initialize(row,{} if refs is None else refs);self.u.mem_map=self.u._original_snapshot_map;del self.u._original_snapshot_map;self.u.mem_protect(SOURCE_IMAGE_BASE,(len(e.CODE)+4095)&~4095,5)
  for address,size in SOURCE_IMAGE_WRITABLE:self.u.mem_protect(address,size,3)
  for address,size,perms in partitions:self.u.mem_protect(address,size,perms)
  self.image_layout=dict(complete_image_mapped_first=True,one_original_image_RAM_backing=True,source_RX_RW_permissions=True,snapshot_partitions_preserved=True,original_events_filtered=False)

Replay.execute=bind_replay(previous_stage.followup_stage.Replay.execute,'execute')
Replay.cleanup=bind_replay(previous_stage.Replay.cleanup,'cleanup')

def execute_with_events(replay):
 need(e.EVENTS==EVENT_ABI,'all exact independently identified original call ABIs');observed=[];stack=[]
 def hook(u,at,size,_):
  sp=u.reg_read(x86.UC_X86_REG_ESP)
  while stack and (at,sp)==(stack[-1]['caller'],stack[-1]['return_ESP']):
   cpu=replay.cpu();r=stack.pop();r.update(after_CPU=cpu,after=event_state(replay),result=cpu['EAX'])
  if at in EVENT_ABI:
   cpu=replay.cpu();n,pop=EVENT_ABI[at];r=dict(entry=at,caller=num(replay.read(sp,4),0),receiver=cpu['ECX'],args=[num(replay.read(sp+4+j*4,4),0) for j in range(n)],return_ESP=sp+4+pop,before_CPU=cpu,before=event_state(replay));observed.append(r);stack.append(r)
 token=replay.u.hook_add(UC_HOOK_CODE,hook)
 try:counts=replay.execute()
 finally:replay.u.hook_del(token)
 need(not stack and observed==replay.row['terminal_task_completion']['events'],'all original call bytes full57CPU and natural return ABIs reexecuted')
 return dict(counts,original_call_events=len(observed),all_original_call_event_bytes_CPU_and_ABI_verified=True)


def native(row, old=None):
    """Classify every current wire and original leaf by its actual lifetime."""
    old = parent_case(row) if old is None else old
    d = row['terminal_task_completion']
    gt = row['GPU_trace']
    ct = row['CRT_trace']
    contexts = gpu_mappings(row)
    oldcontexts = gpu_mappings(old)
    ledger = row['task_completion_resources_after_cleanup']
    by_create = {r['create_wire_index']: r for r in ledger}
    by_gen = {r['generation']: r for r in ledger}
    legacy = native_previous_stage.previous
    need(helper_contract() == e.helper_contract(), 'unchanged original native helper contract')
    need([(r['domain'], r['guest']) for r in row['typed_GPU_projection']] == [(r['domain'], r['guest']) for r in old['typed_GPU_projection']], 'all parent GPU identities and their original order unchanged')
    next_guest = max((r['guest'] for r in row['typed_GPU_projection'] if r['domain'].startswith('overlay-last-dialogue-'))) + 1048576
    need(d['GPU_projection_before'] == dict(next=next_guest, ledger=row['typed_GPU_projection']) and d['GPU_projection'] == row['typed_GPU_projection'] and (not any((c['op'] == 'create' for c in d['GPU_APIs']))), 'complete unchanged allocation cursor/ledger and no new native texture')
    actual_identities = {k: set() for k in contexts}

    def ids(t):
        return [t['pointer'], t['vtable']] + list(t['methods'].values())
    actual_identities['overlay'].update(ids(row['current_GPU_hello']['device']))
    for r in ledger:
        domain = resource_domain(row, r)
        t = gt[r['create_wire_index']]['reply']['result']['texture']
        values = ids(t)
        bridged = native_previous_stage.bridged_followup_pointer(row, r)
        if bridged:
            actual_identities[FOLLOWUP_POINTER_DOMAIN].add(values.pop(0))
        actual_identities[domain].update(values)
        locks = [t['reply']['result']['bits'] for (i, t) in enumerate(gt) if r['create_wire_index'] < i < r['release_wire_index'] and t['request']['op'] == 'lock' and (t['request']['pointer'] == r['native_pointer'])]
        need(len(locks) == 1, 'one actual original surface lock per creation')
        actual_identities[FOLLOWUP_BITS_DOMAIN if bridged else domain].add(locks[0])
    need(all((set(contexts[k]) == v for (k, v) in actual_identities.items())), 'each typed native identity belongs to its real device/create/lock receipt')
    need(row['current_GPU_hello']['max_textures'] == 10 and row['current_GPU_hello']['max_creates'] == 32 and (row['current_GPU_hello']['window_visible'] is False) and (row['current_GPU_hello']['pointer_bytes'] == row['current_CRT_hello']['pointer_bytes'] == 4) and (row['current_GPU_hello']['image_size'] == [512, 512]) and (row['current_CRT_hello']['GPU_created'] is False), 'actual bounded headless x86 native owners')
    n = 15 if row['input']['name'] == 'neutral_running' else 18
    need(len(by_create) == len(by_gen) == len(ledger) == len(d['resources']) == len(d['resources_before']) == n, 'all inherited creation generations without additions')
    need(d['resources_before'] == row['terminal_script_exit']['resources'] and sum((r['alive'] for r in d['resources_before'])) == 10, 'complete current parent resource ledger')
    for (before, after) in zip(d['resources_before'], d['resources']):
        for (k, v) in before.items():
            if k not in ('alive', 'release_wire_index', 'released_phase', 'alive_after_forward'):
                need(after[k] == v, 'unchanged inherited generation metadata ' + k)
        if not before['alive']:
            need(all((after.get(k) == before.get(k) for k in ('alive', 'release_wire_index', 'released_phase'))), 'no revival or repeated release of retired generation')
    need(d['GPU_APIs'] == [x['call'] for x in d['leaves'] if x['kind'] == 'GPU'] and d['calls'] == [] and (d['GDI_trace'] == []) and (not any((x['kind'] == 'GDI' for x in d['leaves']))), 'each new original GPU leaf once; no new GDI calls')
    need(row['CRT_APIs'][d['prefix']['CRT_APIs']:] == [x['call'] for x in d['leaves'] if x['kind'] == 'CRT'], 'complete current CRT leaves including actual late cleanup')
    for (label, trace) in (('GPU', gt), ('CRT', ct)):
        for (i, t) in enumerate(trace):
            need(t['request']['id'] == t['reply']['id'] == i + 1 and t['reply']['ok'] is True, 'complete ordered successful actual ' + label + ' wire')
    for (i, t) in enumerate(gt[:d['prefix']['GPU_wire']]):
        q = t['request']
        ptr = t['reply']['result']['texture']['pointer'] if q['op'] == 'create' else q.get('pointer')
        matches = [r for r in ledger if r['native_pointer'] == ptr and r['create_wire_index'] <= i <= r['release_wire_index']]
        need(len(matches) == 1, 'one actual inherited lifetime at every prefix wire')
        r = matches[0]
        o = next((r0 for r0 in old['script_exit_resources_after_cleanup'] if r0['generation'] == r['generation']))
        need(legacy.gpu_value(t, resource_context(row, r, contexts)) == legacy.gpu_value(old['GPU_trace'][i], resource_context(old, o, oldcontexts)), 'entire fixed parent GPU wire and guest identity in actual creation lifetime')
    live = {}
    logical = {}
    ci = readbacks = peak = 0
    calls = native_previous_stage.gpu_calls(row) + row['terminal_script_exit']['GPU_APIs'] + d['GPU_APIs']
    observers = {o['wire_index']: o for o in d['readback_observers']}
    need(len(observers) == len(d['readback_observers']), 'unique current observer provenance')
    for (i, t) in enumerate(gt):
        q = t['request']
        result = t['reply']['result']
        op = q['op']
        if op == 'close':
            need(i == len(gt) - 1 and (not live) and (result == row['GPU_cleanup']) and (not result['texture_releases']), 'normal native close after all actual original releases')
            continue
        if op == 'readback':
            need(q['pointer'] in live, 'no observer reads a retired generation')
            r = live[q['pointer']]
            raw = bytes.fromhex(r['upload_hex'])
            need(result['hex'] == raw.hex() and result['sha256'] == sha(raw) and (result['pitch'] == r['size'][0] * 2), 'every surviving surface retains every original texel')
            if i >= d['prefix']['GPU_wire']:
                need(i in observers and (observers[i]['generation'], observers[i]['record'], observers[i]['result']) == (r['generation'], r['record'], result), 'actual new observer tied to exact live creation')
            readbacks += 1
            continue
        need(ci < len(calls), 'no unclassified original COM operation')
        c = calls[ci]
        ci += 1
        generation = by_create[i]['generation'] if op == 'create' else c.get('generation')
        if generation is None:
            matches = [r for r in ledger if r['native_pointer'] == q['pointer'] and r['create_wire_index'] < i <= r['release_wire_index']]
            need(len(matches) == 1, 'one live inherited native generation')
            generation = matches[0]['generation']
        need(generation in by_gen, 'known original generation')
        context = resource_context(row, by_gen[generation], contexts)
        need(c.get('wire_index', i) == i and c['op'] == op and (c['native_result'] == result) and (c['result'] == legacy.gpu_value(result, context)) and (c['actual_API_executed'] is True), 'entire original COM output bound to exact current native wire and lifetime')
        expected = dict(id=i + 1, op=op)
        if op == 'create':
            need(i < d['prefix']['GPU_wire'] and i in by_create, 'creation belongs entirely to frozen parent')
            r = by_create[i]
            a = c['args']
            p = result['texture']['pointer']
            need(r['generation'] == i + 1 and r['native_pointer'] == p and (r['texture'] == c['result']['texture']) and (r['record'] == a[-1] - 44) and (r['size'] == a[1:3]) and (p not in live) and (r['texture']['pointer'] not in logical), 'original creation and simultaneous native/guest ownership')
            live[p] = r
            logical[r['texture']['pointer']] = r
            expected.update(width=a[1], height=a[2], levels=a[3], usage=a[4], format=a[5], pool=a[6])
            peak = max(peak, len(live))
        else:
            need(c['args'][0] in logical, 'original receiver has a live generation')
            r = logical[c['args'][0]]
            need(live.get(q['pointer']) is r, 'native and guest select the same live generation')
            expected['pointer'] = r['texture']['pointer']
            if op == 'lock':
                expected['flags'] = c['args'][-1]
                need(c['result'] == r['lock'], 'whole actual original lock input')
            elif op == 'unlock':
                expected['hex'] = r['upload_hex']
            elif op == 'release':
                need(r['release_wire_index'] == i and c['value'] == result['count'] == 0, 'exact original last release')
                del live[q['pointer']]
                del logical[r['texture']['pointer']]
            else:
                need(op == 'describe', 'only original finite COM operations')
        need(legacy.gpu_value(q, context) == expected, 'entire actual translated original COM request')
        if i >= d['prefix']['GPU_wire']:
            need(op in ('describe', 'release') and (c['generation'], c['record'], c['resource_kind'], c['resource_label'], c['phase']) == (r['generation'], r['record'], r['kind'], r['label'], 'forward' if i < d['forward_wire_end'] else 'cleanup'), 'actual destruction ABI and exact generation/record/phase')
    need(ci == len(calls) and peak == 10, 'every actual COM call and original capacity peak classified')
    need(sorted(observers) == [i for (i, t) in enumerate(gt) if i >= d['prefix']['GPU_wire'] and t['request']['op'] == 'readback'] and d['readbacks'] == d['readback_observers'], 'all new readbacks are the final surviving set')
    for (r, f) in zip(ledger, d['resources']):
        need(r['alive'] is False and r['release_wire_index'] is not None, 'every actual generation eventually originally released')
        want = copy.deepcopy(r)
        want['alive'] = r['release_wire_index'] >= d['forward_wire_end']
        if want['alive']:
            want['release_wire_index'] = None
            want.pop('released_phase', None)
        need(f == want and f['alive'] == r['alive_after_forward'], 'complete forward resource ledger frozen before actual supplemental cleanup')
    need({o['generation'] for o in d['readbacks']} == {r['generation'] for r in d['resources'] if r['alive']} and all((o['label'] == 'final' for o in d['readbacks'])), 'every actual survivor observed, with no preselected surviving count')
    covered = []
    for a in row['CRT_APIs']:
        need(0 <= a['wire_start'] < a['wire_end'] < len(ct) and CRT_IMPORTS[a['import_slot']] == (a['name'], a['pop']) and (e.CODE[a['import_slot'] - 4194304:a['import_slot'] - 4194304 + 4] == struct.pack('<I', a['target'])), 'original CRT IAT and exact actual wire interval')
        covered.extend(range(a['wire_start'], a['wire_end']))
        r = ct[a['wire_end'] - 1]['reply']['result']
        nm = a['name']
        outputs = []
        if nm in ('InitializeCriticalSection', 'EnterCriticalSection', 'LeaveCriticalSection'):
            raw = r['hex'] if nm == 'InitializeCriticalSection' else r['critical_hex']
            b = bytearray.fromhex(raw)
            need(len(b) == 24, 'whole current critical section')
            for off in (0, 12, 16):
                if num(b, off) not in (0, 4294967295):
                    struct.pack_into('<I', b, off, 1660944384 + off + (a['args'][0] - 8430720) * 256)
            outputs = [dict(pointer=a['args'][0], hex=b.hex(), native_hex=raw)]
            value = 0
        elif nm == 'HeapAlloc':
            outputs = [dict(pointer=a['value'], hex=r['hex'])]
            value = a['value']
            need(len(bytes.fromhex(r['hex'])) == a['args'][2] and a['new_mappings'] == [dict(pointer=value, bytes=a['args'][2] + 4095 & ~4095)], 'whole actual heap buffer including uninitialized bytes')
        elif nm == 'ReadFile':
            outputs = [dict(pointer=a['memory_outputs'][0]['pointer'], hex=r['after_hex']), dict(pointer=a['args'][3], hex=struct.pack('<I', r['read']).hex())]
            value = r['value']
        elif nm in ('GetVersionExA', 'GetCurrentDirectoryA'):
            outputs = [dict(pointer=a['args'][0 if nm == 'GetVersionExA' else 1], hex=r['hex'])]
            value = r['value']
        elif nm == 'CreateFileA':
            value = 1644171264
            need(a['native_handle'] == r['handle'], 'current actual read-only file owner')
        elif nm == 'HeapCreate':
            value = 1627394048
        elif nm == 'DeleteCriticalSection':
            value = 0
        else:
            value = r['value']
        need(a['memory_outputs'] == outputs and a['value'] == value, 'every actual complete CRT output retained')
    constructed = [row['terminal_portrait']['constructed']] + [r['constructed'] for stage in (followup_stage, next_stage) for r in stage.new_resources(row) if r['kind'] == 'portrait']
    for b in constructed:
        for x in b['native_allocation_readbacks']:
            i = x['wire_index']
            covered.extend((i - 1, i))
            a = ct[i - 1]
            z = ct[i]
            need(a['request']['op'] == 'sync' and a['request']['hex'] == a['reply']['result']['hex'] == x['result']['hex'] and (z['request'] == dict(id=i + 1, op='readback', pointer=x['result']['pointer'])) and (z['reply']['result'] == x['result']) and (len(bytes.fromhex(x['result']['hex'])) == x['bytes']), 'whole actual original file/vector mirror and current observer')
    need(sorted(covered) == list(range(len(ct) - 1)), 'each current CRT operation classified once')
    need(legacy.crt_semantics(row)[:d['prefix']['CRT_wire']] == legacy.crt_semantics(old)[:d['prefix']['CRT_wire']], 'complete fixed parent CRT control and initialized data; raw inputs independently executed')
    GDI = native_previous_stage.gdi_native(row, native_previous_stage.parent_case(row))
    need(d['prefix']['GDI_trace'] == GDI['calls'] and d['GDI_handle_projection'] == row['terminal_script_exit']['GDI_handle_projection'], 'whole current parent GDI lifetimes with no new call or handle')
    task_leaves = [x['call'] for x in d['leaves'] if x['kind'] == 'TASK']
    actual = row['task_APIs'][d['prefix']['task_APIs']:]
    need(len(task_leaves) == len(actual) and all((all((c[k] == value for (k, value) in a.items())) for (c, a) in zip(task_leaves, actual))), 'one actual current task API leaf per platform receipt')
    need(row['CRT_exit'] == row['GPU_exit'] == 0 and ct[-1]['request'] == dict(id=len(ct), op='close') and (ct[-1]['reply']['result'] == row['CRT_cleanup']) and row['CRT_cleanup']['all_owned_resources_released'] and (not row['CRT_cleanup']['forced_cleanup']), 'all current native owners close normally without fallback')
    return dict(current_COM_calls=ci, texture_generations=len(ledger), peak_live_textures=peak, forward_live_textures=sum((r['alive'] for r in d['resources'])), whole_readbacks=readbacks, current_CRT_operations=len(ct) - 1, current_GDI_calls=GDI['calls'], GDI_lifetime_audit=GDI, no_new_texture_or_GDI_creation=True, all_native_ownership_and_protocol_verified=True, raw_heap_and_surface_hex_never_address_normalized=True)

def source(row):
 need(e.NEW_MUTABLE==((e.TASK+0x171,e.TASK+0x173),),'only two original task-completion flag bytes newly writable')
 need(e.EXTRA_RANGES==EXTRA_RANGES and e.RANGES==e.parent.RANGES+EXTRA_RANGES and e.ALLOWED==frozenset(a for lo,hi in e.RANGES for a in range(lo,hi)),'one exact original resource-loop extent added')
 need(e.TaskCompletionMachine.source_code.__code__ is e.parent.ScriptExitMachine.source_code.__code__,'unchanged original source instruction guard algorithm')
 need(e.GROUPS==GROUPS and tuple(e.QUERIES)==(0x497C50,0x454EE0,0x41F4E0,0x41F2A0,0x41F710),'all five exact original observation entries')
 from capstone import Cs,CS_ARCH_X86,CS_MODE_32
 md=Cs(CS_ARCH_X86,CS_MODE_32)
 expected={0x454E18:('call','0x497c50'),0x454E24:('call','0x454ee0'),0x454E34:('mov','byte ptr [edx], cl'),0x454E3B:('mov','byte ptr [eax + 0x15], 3'),0x454E42:('cmp','dword ptr [ecx + 0x4c], 1'),0x454E4B:('mov','byte ptr [edx + 0x171], 1'),0x454E55:('mov','byte ptr [eax + 0x172], 1'),0x454E99:('call','0x41f710'),0x454E9E:('mov','eax, 1'),0x454E5F:('mov','dl, byte ptr [ecx]'),0x454E61:('add','dl, 1'),0x454E67:('mov','byte ptr [eax], dl'),0x454E72:('jne','0x454e86'),0x454E81:('call','0x467850'),0x454E89:('mov','byte ptr [edx + 0x43], 0'),0x454E6E:('cmp','dword ptr [ecx + 0x54], 1'),0x454E3F:('mov','ecx, dword ptr [ebp - 4]'),0x454EAF:('xor','eax, eax')}
 expected.update({0x454E1F:('jne','0x454e36'),0x454E46:('jne','0x454e6b'),0x454E69:('jmp','0x454e8d'),0x454E93:('add','ecx, 0x844'),0x454E48:('mov','edx, dword ptr [ebp - 4]'),0x454F13:('je','0x454f3c'),0x454F1B:('cmp','dword ptr [ebp - 0xc], 0x14'),0x454F23:('jmp','0x454f06'),0x454F35:('call','0x41f4e0'),0x41F4FD:('mov','eax, dword ptr [ebp + 8]'),0x41F514:('cmp','dword ptr [edx + 4], 0'),0x41F543:('mov','ecx, dword ptr [ebp - 0xc]'),0x41F548:('call','0x403730'),0x41F566:('call','0x41f2a0'),0x41F57A:('mov','dword ptr [eax], 0'),0x41F583:('mov','dword ptr [ecx + 4], 0'),0x41F59C:('ret','4'),0x41F72D:('jmp','0x41f811')})
 for at,want in expected.items():
  i=next(md.disasm(e.CODE[at-0x400000:at-0x400000+16],at));need((i.mnemonic,i.op_str)==want,'exact independently derived original handshake instruction '+hex(at))
 for a,b in EXTRA_RANGES:
  seq=list(md.disasm(e.CODE[a-0x400000:b-0x400000],a));need(seq[0].mnemonic=='push' and seq[0].op_str=='ebp' and seq[-1].mnemonic=='ret' and seq[-1].address+seq[-1].size==b,'original full function extent')
 return dict(groups=list(GROUPS),skipped_group=20,original_instruction_checks=len(expected),phase4_query=0x497C50,phase4_destructor=0x454EE0,phase5_status=3,phase5_flags=[0x171,0x172],following_battle_stage_executed=False)

def capture_boundary(full,compact):
 for key in ('CPU','state','queue','trace','local_trace'):need(full[key]==compact[key],'whole named/frame capture '+key)
 hashes=[]
 for r in full['memory']:
  raw=bytes.fromhex(r['hex']);need(len(raw)==r['bytes'],'full named capture region bytes');hashes.append(dict(pointer=r['pointer'],bytes=r['bytes'],sha256=sha(raw)))
 need(hashes==compact['memory'],'every full named boundary region equals original compact frame SHA')
 return True

def protocol(row):
 d=row['terminal_task_completion'];frames=d['frames'];before=d['before']['state'];final=d['final'];need(len(frames)==2 and not d['bindings'] and not d['commands'] and not d['calls'] and not d['conversions'] and not d['GDI_trace'],'exactly two full task frames without new input or VM/render commands')
 need([f['phase'] for f in frames]==['original_phase4_resource_groups','original_phase5_completion_handshake'],'two exact original phase boundaries')
 initial_task=bytes.fromhex(before['task']);need(initial_task[0x44]==4 and initial_task[0x59]==2 and num(initial_task,0x4C)==1 and initial_task[0x171:0x173]==bytes(2),'fixed original selected terminal task awaiting completion')
 prior=d['before']
 for i,f in enumerate(frames):
  need(f['index']==i and f['complete'] is True and f['before']==prior['state'] and f['queue_before']==prior['queue'] and f['capture']['state']==f['after'] and f['queue_after']==f['capture']['queue'],'every full frame state/queue continuity')
  task=bytearray(initial_task);task[0x44]=5+i
  if i==1:task[0x59]=3;task[0x171:0x173]=b'\x01\x01'
  need(f['after']['task']==task.hex(),'whole original task bytes match phase/status/flag transition')
  need(f['after']['VM']==before['VM'] and f['after']['work']==before['work'] and f['after']['remaining']==before['remaining'] and f['after']['elapsed']==before['elapsed'],'stopped VM, completed work and paused clock stay unchanged')
  need(f['capture']['CPU']['EAX']==i and f['capture']['CPU']['EIP']==e.RETURN and f['capture']['CPU']['ESP']==e.STACK+0xF004,'each complete task naturally returns original0 then1 at exact root ABI')
  prior=f['capture']
 capture_boundary(d['phase4'],frames[0]['capture']);capture_boundary(final,frames[-1]['capture'])
 events=d['events'];groups=[r for r in events if r['entry']==0x41F4E0]
 need([r['args'] for r in groups]==[[g] for g in GROUPS] and all(r['caller']==0x454F3A and r['receiver']==e.MAIN+0x844 for r in groups),'all78 natural resource-group calls exact order caller/receiver')
 loops=[r for r in events if r['entry']==0x454EE0];need(len(loops)==1 and loops[0]['caller']==0x454E29 and loops[0]['receiver']==e.TASK,'one natural phase4 loop, never a supplemental forward root')
 expected_destructors=[];expected_arrays=[]
 table=bytes.fromhex(loops[0]['before']['resource_table_hex']);need(len(table)==0x800,'complete manager table')
 initial_table=read(d['before']['memory'],e.MAIN+0x844,0x800);need(table==initial_table,'loop starts at whole accepted table')
 for g,r in zip(GROUPS,groups):
  need(r['before']['resource_table_hex']==table.hex(),'complete contiguous resource table at group entry')
  z=bytearray(table);ptr,count=struct.unpack_from('<II',z,g*8)
  if count:
   if ptr:expected_destructors.extend(ptr+j*0x54 for j in range(count));expected_arrays.append(ptr)
   struct.pack_into('<II',z,g*8,0,0)
  need(r['after']['resource_table_hex']==z.hex() and r['result']==0,'whole table original per-group pointer/count semantics including empty slots')
  table=bytes(z)
 destructors=[r for r in events if r['entry']==0x403730 and r['caller']==0x41F54D];need([r['receiver'] for r in destructors]==expected_destructors and all(r['args']==[] for r in destructors),'every original 54h resource record destructor from the exact accepted arrays')
 arrays=[r for r in events if r['entry']==0x41F2A0 and r['caller']==0x41F56B];need([r['receiver'] for r in arrays]==expected_arrays and all(r['args']==[3] for r in arrays),'each original nonempty array deleted once with its exact vector-delete flags')
 need(loops[0]['after']['resource_table_hex']==table.hex() and read(d['phase4']['memory'],e.MAIN+0x844,0x800)==table and read(final['memory'],e.MAIN+0x844,0x800)==table,'complete manager table after loop and task handoff')
 need(table[20*8:21*8]==initial_table[20*8:21*8] and num(table,20*8+4)>0,'original group20 remains owned and unchanged')
 for g in GROUPS:need(table[g*8:g*8+8]==bytes(8),'every processed accepted bank ends empty')
 debug=[r for r in events if r['entry']==0x41F710];need(len(debug)==1 and debug[0]['caller']==0x454E9E and debug[0]['receiver']==e.MAIN+0x844 and debug[0]['before']==debug[0]['after'],'original debug function skips its unreachable body without manager mutation')
 ready=[r for r in events if r['entry']==0x497C50];need(len(ready)==1 and ready[0]['caller']==0x454E1D and ready[0]['result']==0,'original work readiness query naturally permits phase4')
 for r in events:need(r['before']['VM_active']==r['after']['VM_active']==0 and r['before']['VM_PC']==r['after']['VM_PC']==branch(row['input']['name'])['final_PC'],'all original nested events retain stopped VM')
 need(d['VM_script_stopped'] is True and d['terminal_task_completion_executed'] is True and d['terminal_battle_exit_executed'] is False and d['rewards_or_school_executed'] is False,'task handshake and future battle exit separated')
 need(d['accounting']==num(read(final['memory'],0x765720,4),0)==row['accounting_baseline']['texture_bytes']+sum(r['size'][0]*r['size'][1]*2 for r in d['resources'] if r['alive']),'actual surviving texture accounting')
 return dict(complete_frames=2,VM_PC=branch(row['input']['name'])['final_PC'],VM_active=0,VM_wait=0,task_phase=6,task_status=3,task_return=1,completion_flags=[1,1],original_group_calls=78,skipped_group=20,new_input_bindings=0,battle_exit_consumer_executed=False)

def final_summary(row):
 d=row['terminal_task_completion'];memory=d['final']['memory'];t=e.terminal;s=expand(row['final_state']['terminal_state'],row['blobs'])
 want=dict(task=read(memory,e.TASK,0x190).hex(),records=[read(memory,t.RECORD+i*256,256).hex() for i in (0,1)],counters=read(memory,t.CTRL+0x2EF14,0x31).hex(),remaining=num(read(memory,t.CTRL+0x2E6F4,4),0,'i'),elapsed=num(read(memory,t.CTRL+0x2E6F8,4),0,'i'),result=read(memory,0x7F4000,0x2000).hex(),work=read(memory,t.WORK,3).hex(),VM=read(memory,e.VM,0x9400).hex(),units=[read(memory,p,0x520).hex() for p in (t.UNIT,t.TARGET)])
 need(s==want,'all final terminal summary pages equal independently verified full memory')
 return True

def verify_case(row,old=None):
 prefix_trace(row);provenance=source(row);timed=protocol(row);platform=native(row,old);plan=cleanup_plan(row);replay=Replay(row);counts=execute_with_events(replay);prior=prefix(row,old);d=row['terminal_task_completion'];equal(row['final'],d['final']['memory'],'complete final mapped memory')
 need(row['pending_CPU']==d['final']['CPU'] and row['image_before']==row['image_after'],'all57 finalCPU and original code/IAT unchanged')
 need((row['instructions'],row['writes'],row['code_trace_sha256'],row['write_trace_sha256'])==tuple(d['final']['trace'][k] for k in ('instructions','writes','code_sha256','write_sha256')),'all original cumulative source fields')
 summary_checked=final_summary(row);cleanup=replay.cleanup();summary=dict(full_cumulative=d['final']['trace'],mapped_regions=len(d['final']['memory']),CPU_registers=len(d['final']['CPU']),complete_tasks=(760 if row['input']['name']=='neutral_running' else 787)+2,pending_tasks=0,live_textures=sum(r['alive'] for r in d['resources']),new_textures=[],task_phase=6)
 return dict(name=row['input']['name'],prefix=prior,source=provenance,helper=e.helper_contract(),native=platform,timing=timed,added=counts,cleanup=cleanup,cleanup_plan_derived_from_fixed_roots_and_final_memory=plan,forward_summary=summary,independent_source_image_layout=replay.image_layout,independent_replay_observer_adaptation=Replay.execute.__globals__['OBSERVER_SCHEMA_AUDIT'],current_terminal_summary_pages_equal_verified_final_memory=summary_checked,whole_memory_CPU_original_events_and_trace_verified=True,no_historical_cleanup_CPU_or_SHA_projection=True,terminal_task_completion_executed=True,terminal_battle_exit_executed=False,rewards_complete=False)

def fresh_case(case,ch,gh,ticks):
 need(ticks==accepted_clock_inputs()[case['name']],'fresh original fixed clock input');return e.run_case(case,ch,gh,ticks)

def verify(path):
 accepted_clock_inputs();data=load_report(path);need(data['schema_version']==1 and data['source_contract']==e.source_contract() and [r['input'] for r in data['cases']]==e.overlay.parent.corpus(),'both selected source cases and full source contract')
 need(Path(data['helper_build']['GPU']['source']).as_posix()=='tools/terminal_followup_d3d8_platform.cs' and data['helper_build']['GPU']['source_sha256']==e.helper_contract()['current']['sha256'] and data['helper_build']['GPU']['machine']==0x14C,'same bounded x86 native helper')
 helpers=e.helpers('terminal-task-completion-proof');rows=[]
 for row in data['cases']:
  old=parent_case(row);proof=verify_case(row,old);other=None
  try:
   ticks=[a['result'] for a in old['APIs'] if a['name']=='GetTickCount'];other=fresh_case(row['input'],helpers[0],helpers[1],ticks);verify_case(other,old)
   for key in ('initial','final'):equal(row[key],other[key],'fresh entire '+key+' memory')
   for key in ('pending_CPU','instructions','writes','code_trace_sha256','write_trace_sha256','cleanup_steps','cleanup_state','resource_initialization','world_frames','events','commands','task_calls','task_writes','admission'):need(row[key]==other[key],'fresh all cumulative and original boundary '+key)
   for key in ('terminal_task_completion','task_completion_cleanup','task_completion_cleanup_skips','task_completion_resources_after_cleanup'):need(guest(row[key])==guest(other[key]),'fresh whole current stage '+key)
  except Exception as error:
   if other is not None:
    name='analysis/terminal-task-completion-diagnostic-fresh-'+row['input']['name']+'-20261030-'+str(time.time_ns())+'.json.gz';e.save_source(name,dict(schema_version=1,source_report=e.terminal.ref(path.relative_to(ROOT).as_posix()),error=str(error),fresh_original_case=other));print('full fresh failure preserved locally',name,flush=True)
   raise
  proof.update(current_native_resources_recreated=True,complete_cumulative_digests_reproduced_by_new_full_original_instance=True);rows.append(proof);print('independent task completion',row['input']['name'],'all current original lifetimes verified',flush=True);del other;gc.collect()
 return dict(schema_version=1,source_report=e.terminal.ref(path.relative_to(ROOT).as_posix()),implementation_sha256={p:sha((ROOT/p).read_bytes()) for p in IMPLEMENTATIONS},cases=rows,whole_current_native_protocol_independently_verified=True,current_native_resources_recreated=True,complete_cumulative_digests_reproduced=True,cumulative_digest_reconstructed=False,historical_cleanup_projection=False,terminal_task_completion_executed=True,terminal_battle_exit_executed=False,new_OS_input=False,draw_or_Present=False,terminal_presentation_complete=False,rewards_complete=False,R3_complete=False,R4_complete=False,R5_complete=False,R6_complete=False)

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',required=True);p.add_argument('--out',required=True);a=p.parse_args();need(not(ROOT/a.out).exists(),'fresh immutable task completion proof');e.terminal.save(a.out,verify(ROOT/a.report))
