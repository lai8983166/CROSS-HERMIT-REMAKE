"""Disclosed scalar-only verifier view; never writes the actual emulator or raw evidence."""
import copy
import hashlib
import json
from tools.school_window_module import geometry,store,dword,BASE
from tools.school_main_context_emulation import initial_cpu,initial_stack
from tools.school_window_geometry_verification import verify_case as verify_legacy_geometry
from tools.school_renderer_init_emulation import buffer_evidence
from tools.school_renderer_init_verification import verify_buffer
from tools.school_device_init_verification import unpack

window=geometry.window
parent=geometry.parent
PHASES=('allocation','constructor','publication','tasks','query','branch','rect','adjust','class')


def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def legacy_prefix_view(c):
    module=c['hello']['resource_module']['pointer'];legacy=window.HINSTANCE;view=copy.deepcopy(c);changes=[]
    declared=bytearray(initial_stack(c['fill']));store(declared,parent.TOP+4-parent.STACK,module)
    inp=c['module_input']
    expected=dict(root_va='0x49ddc9',before_first_original_instruction=True,slot=parent.TOP+4,value=module,
        cpu=initial_cpu(),initial_stack=inp['initial_stack'],source='owned actual resource module in helper hello')
    if inp!=expected:raise ValueError('module genuine instance declared at root before execution')
    verify_buffer(inp['initial_stack'],declared)
    def scalar(obj,key,path):
        if obj[key]!=module:raise ValueError('module source-derived actual instance at '+path)
        obj[key]=legacy;changes.append(dict(path=path,before=module,after=legacy,kind='declared-instance scalar only'))
    def stack_buffer(node,phase):
        before=unpack(node['state']['stack']);after=bytearray(before)
        positions=[parent.TOP+4]
        if phase=='class':positions += [geometry.CLASS_AT+20,geometry.FRAME_SP-8]
        for p in positions:
            if dword(before,p-parent.STACK)!=module:raise ValueError('module actual instance at exact source-derived stack slot')
            store(after,p-parent.STACK,legacy)
        node['state']['stack']=buffer_evidence(bytes(after))
        changes.append(dict(path=phase+'.state.stack',before_sha256=hashlib.sha256(before).hexdigest(),after_sha256=hashlib.sha256(after).hexdigest(),
            dword_positions=positions,kind='enumerated instance stack slots only'))
    calls=c['constructor']['platform_calls']
    for phase in PHASES:
        actual=c[phase];node=view[phase];stack_buffer(node,phase)
        if phase in ('allocation','constructor','publication'):
            old_image=parent.project_image(phase,calls);actual_image=old_image
        else:
            old_image=window.project_image(parent.project_image('publication',calls),'tasks' if phase=='tasks' else 'branch')
            actual_image=bytearray(old_image);store(actual_image,window.INSTANCE-BASE,module);actual_image=bytes(actual_image)
        if actual['state']['image_sha256']!=hashlib.sha256(actual_image).hexdigest():raise ValueError('module complete raw source image with genuine published instance')
        node['state']['image_sha256']=hashlib.sha256(old_image).hexdigest()
        if phase not in ('allocation','constructor','publication'):
            changes.append(dict(path=phase+'.state.image_sha256',before=actual['state']['image_sha256'],after=node['state']['image_sha256'],kind='original49DE26 instance global only'))
        if phase in ('tasks','query'):
            scalar(node['cpu'],'EDX',phase+'.cpu.EDX')
        if phase in ('query','branch'):
            scalar(node['before_cpu'],'EDX',phase+'.before_cpu.EDX')
        if phase in ('tasks','query','branch'):
            scalar(node['state'],'instance_value',phase+'.state.instance_value')
        if phase=='tasks':
            rows=[w for w in node['native_writes'] if w['pc']==0x49DE26]
            if len(rows)!=1 or rows[0]['pointer']!=window.INSTANCE or rows[0]['bytes']!=4:raise ValueError('module actual original instance publication write')
            scalar(rows[0],'value','tasks.native_write49DE26.value')
        if phase=='class':
            for k in ('ECX','EDX'):scalar(node['cpu'],k,'class.cpu.'+k)
            if node['pending']['stack_args']!=[module,157]:raise ValueError('module actual source icon argument preparation')
            node['pending']['stack_args'][0]=legacy
            changes.append(dict(path='class.pending.stack_args[0]',before=module,after=legacy,kind='original instance argument'))
            cls=unpack(node['state']['class_structure']);new_cls=bytearray(cls)
            if dword(cls,20)!=module:raise ValueError('module actual class hInstance')
            store(new_cls,20,legacy);node['state']['class_structure']=buffer_evidence(bytes(new_cls))
            changes.append(dict(path='class.state.class_structure',before_sha256=hashlib.sha256(cls).hexdigest(),after_sha256=hashlib.sha256(new_cls).hexdigest(),dword_offset=20,kind='class hInstance only'))
            for pc,pointer in ((0x4503F7,geometry.CLASS_AT+20),(0x450415,geometry.FRAME_SP-8)):
                rows=[w for w in node['native_writes'] if w['pc']==pc]
                if len(rows)!=1 or rows[0]['pointer']!=pointer or rows[0]['bytes']!=4:raise ValueError('module exact source class/argument instance store')
                scalar(rows[0],'value','class.native_write'+hex(pc)+'.value')
    for phase,previous in (('query','tasks'),('rect','branch')):
        a=c[phase]['import_admission'];v=view[phase]['import_admission'];p=c[previous];vp=view[previous]
        if a['before_cpu']!=p['cpu'] or a['after_cpu']!=p['cpu'] or a['retained_stack_sha256']!=p['state']['stack']['sha256'] or a['retained_image_sha256']!=p['state']['image_sha256']:
            raise ValueError('module exact raw import-admission continuity before verifier view')
        v['before_cpu']=copy.deepcopy(vp['cpu']);v['after_cpu']=copy.deepcopy(vp['cpu'])
        v['retained_stack_sha256']=vp['state']['stack']['sha256'];v['retained_image_sha256']=vp['state']['image_sha256']
        changes.append(dict(path=phase+'.import_admission',kind='same enumerated instance-derived CPU/stack/image fields',before_sha256=digest(a),after_sha256=digest(v)))
    verify_legacy_geometry(view)
    raw_prefix={k:c[k] for k in PHASES};old_prefix={k:view[k] for k in PHASES}
    proof=dict(actual_module=module,legacy_verifier_scalar=legacy,raw_prefix_sha256=digest(raw_prefix),validation_view_sha256=digest(old_prefix),
        substitutions=changes,actual_raw_snapshots_modified=False,emulator_mutated=False,legacy_validator_completed=True)
    return view,proof
