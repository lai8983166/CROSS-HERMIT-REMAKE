"""Independent next-world prefix through natural state4 and student dispatch."""
import hashlib,struct
from copy import deepcopy
from functools import lru_cache
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from tools.tactics_exit_emulation import SOURCE,SOURCE_SHA256,BASE
from tools.school_world_map import project_map_frame
from tools.school_world_lists import project as list_project
from tools.school_world_command import normalize_selection,STRIDE,COUNT

FUNCTIONS=(0x48D720,0x48E2A0,0x475700,0x4751F0,0x4697F0)
NAMES=['task','control','clock','map_slots','map_state','fog_history','fog_current','fog_previous','minimap_globals',
       'window','visible','categories','works','selection','cursor','scratch','queue','occupancy','current_work']


@lru_cache(maxsize=1)
def source_contract():
    raw=SOURCE.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA256:raise ValueError('second world source identity')
    md=Cs(CS_ARCH_X86,CS_MODE_32);functions=[]
    for a in FUNCTIONS:
        end=next((i.address+i.size for i in md.disasm(raw[a-BASE:a-BASE+8192],a) if i.mnemonic=='ret'),None)
        if end is None:raise ValueError('second world complete source range')
        functions.append({'va':hex(a),'end':hex(end),'sha256':hashlib.sha256(raw[a-BASE:end-BASE]).hexdigest()})
    checks={0x49A038:('mov','byte ptr [edx + 0x170], 0'),0x49A042:('mov','byte ptr [eax + 0x108b34], 1'),
      0x49A058:('push','0xb4'),0x49A063:('call','0x415070'),0x49A06B:('mov','word ptr [ecx + 0xe], ax'),
      0x46B7B1:('and','al, 0x7f'),0x46B7C4:('call','0x48d720'),0x46B7D0:('call','0x48e2a0'),0x46B7DC:('call','0x475700'),
      0x48D740:('movsx','ecx, byte ptr [eax + 0x108b35]'),0x48D74B:('jmp','0x48dc2d'),
      0x47572F:('call','0x4751f0'),0x47573B:('call','0x4697f0'),0x46986E:('movsx','ecx, byte ptr [eax + 0x2a7]'),
      0x47579E:('call','0x475d60')}
    proof=[]
    for a,wanted in checks.items():
        i=next(md.disasm(raw[a-BASE:a-BASE+16],a))
        if (i.mnemonic,i.op_str)!=wanted:raise ValueError('second world exact source operand '+hex(a))
        proof.append({'va':hex(a),'hex':i.bytes.hex(),'mnemonic':i.mnemonic,'operands':i.op_str})
    target=struct.unpack_from('<I',raw,0x475C6B-BASE+25*4)[0]
    if target!=0x475797:raise ValueError('second world source mode25 dispatch')
    return {'source_image_sha256':SOURCE_SHA256,'functions':functions,'instructions':proof,'first_work_mode':25,'mode25_target':hex(target),
       'next_controller_state':5,'native_delay':180,'next_handler':'0x475d60','next_return':'0x4757a3',
       'scope':'Declared second world call, natural enabled action prefix; stops before first student handler, no180 ticks/VM/AI completion'}


def ranges():return tuple((int(r['va'],16),int(r['end'],16)) for r in source_contract()['functions'])


def project(inputs,before):
    source_contract();out=deepcopy(before)
    if [r['name'] for r in out]!=NAMES:raise ValueError('second world full region order')
    data={r['name']:bytearray.fromhex(r['hex']) for r in out}
    if any(len(data[r['name']])!=r['bytes'] for r in out):raise ValueError('second world complete byte lengths')
    task,ctrl,works=data['task'],data['control'],data['works']
    if len(task)!=400 or len(ctrl)!=50 or len(works)!=STRIDE*COUNT or len(data['selection'])!=1016 or len(data['cursor'])!=10 or len(data['scratch'])!=2048:raise ValueError('second world complete owned sizes')
    if task[0x170]!=1 or task[0x171] or task[0x43] or struct.unpack_from('<I',task,0x38)[0]!=5:raise ValueError('second world actual task request/phase')
    if ctrl[26]!=4 or struct.unpack_from('<h',ctrl,28)[0] or ctrl[24]!=1 or ctrl[11]!=255 or struct.unpack_from('<h',ctrl,2)[0]!=1 or any(ctrl[i] for i in (4,5,6,8,9,10)):raise ValueError('second world state4 locked opening scope')
    if inputs['mouse']!=[0,0] or inputs['map_state']!=0 or inputs['task_input']!=[0,0,0] or inputs['ctrl_keys']!=[0,0]:raise ValueError('second world no-command input')
    if data['queue'][8:]!=bytes(12) or len(data['queue'])!=20:raise ValueError('second world empty queue')
    if struct.unpack_from('<h',works)[0]==0 or works[0x290]!=25 or works[0x292] or works[0x2A7] or struct.unpack_from('<I',works,0x518)[0]:raise ValueError('second world first student mode/pending/command scope')
    task[0x170]=0;ctrl[4]=1;ctrl[26]=5;struct.pack_into('<h',ctrl,28,180)
    maps=project_map_frame(out[3:9],inputs['mouse'])
    for row in maps:data[row['name']][:]=bytes.fromhex(row['hex'])
    slots=struct.unpack('<3I',data['map_slots']);by_pointer={r['pointer']:r for r in out}
    def row(name,pointer):
        source=by_pointer[pointer];return {'name':name,'pointer':pointer,'bytes':source['bytes'],'hex':data[source['name']].hex()}
    list_inputs=deepcopy(inputs['lists'])
    if list_inputs['opening']!=1 or list_inputs['event']!=0:raise ValueError('second world source list gates')
    list_before=[row('window',out[9]['pointer']),row('fog_current',slots[1]),row('fog_history',slots[0]),row('visible',out[10]['pointer']),row('categories',out[11]['pointer'])]
    listed=list_project(list_inputs,list_before)
    for changed in listed['after']:data[by_pointer[changed['pointer']]['name']][:]=bytes.fromhex(changed['hex'])
    records=[bytes.fromhex(r['record_hex']) if r['record_hex'] else None for r in list_inputs['works']]
    selected,indices,kind=normalize_selection(works,records,list_inputs['team']);works[:]=selected
    struct.pack_into('<2I',data['selection'],0,len(indices),kind)
    for n,i in enumerate(indices):struct.pack_into('<I',data['selection'],16+n*4,list_inputs['works'][i]['pointer'])
    data['cursor'][:]=bytes(6)+b'\xff\xff'+bytes(2);data['scratch'][:]=bytes(2048)
    works[8]&=127;struct.pack_into('<I',data['current_work'],0,list_inputs['works'][0]['pointer'])
    for r in out:r['hex']=data[r['name']].hex()
    return {'after':out,'display_indices':listed['display_indices'],'category_counts':listed['category_counts'],
            'selected_indices':indices,'selection_kind':kind,'controller_state':5,'delay':180,'action':1,'tested_indices':[0],
            'next_handler':'0x475d60','handler_executed':False}
