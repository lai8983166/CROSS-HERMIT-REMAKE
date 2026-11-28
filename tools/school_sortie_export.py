"""Export scene8/17 using existing record, map and DxAnim decoders (no runtime backend)."""
import json
import struct
from copy import deepcopy
from pathlib import Path
from io import BytesIO
from tools.tactics_exit_emulation import ROOT, SOURCE, SOURCE_SHA256, BASE
from tools.school_enemy_records_catalog import source_catalog, expected_record
from tools.school_field_export import skin_inputs, digest
from tools.school_attack_inputs import source_rules, from_record
from tools.school_scene_map_catalog import logical_cells, map_textures, atlas_image
from tools.school_formation_placement_catalog import source_catalog as formation
from tools import dxanim_lib as dx

OUT = ROOT/'prototype/assets/school_sorties'
GAME = ROOT/'CROSS HERMIT/CROSS HERMIT'
ACTIONS = [('idle',1),('move',3),('cast',11),('attack',5),('recover',14)]


def parent_frames(include_sorties=False, include_seven=False, include_four=False, include_six=False, include_ten=False, include_thirteen=False, include_eighteen=False, include_nine=False, include_fourteen=False, include_twenty=False, include_late_roster=False, include_thirty_five=False):
    result={}
    for name in ('school_field','school_combat','school_reinforcements') + (('school_sorties',) if include_sorties else ()) + (('school_seven',) if include_seven else ()) + (('school_four',) if include_four else ()) + (('school_six',) if include_six else ()) + (('school_ten',) if include_ten else ()) + (('school_thirteen',) if include_thirteen else ()) + (('school_eighteen',) if include_eighteen else ()) + (('school_nine',) if include_nine else ()) + (('school_fourteen',) if include_fourteen else ()) + (('school_twenty',) if include_twenty else ()) + (('school_twenty_one','school_july_five') if include_late_roster else ()) + (('school_thirty_five',) if include_thirty_five else ()):
        path=ROOT/'prototype/assets'/name/'catalog.json'
        for value in json.loads(path.read_text(encoding='utf8'))['skins'].values():
            for frame in value['frames'].values():
                file=frame['file'] if frame['file'].startswith('res://') else 'res://assets/'+name+'/'+frame['file']
                disk=ROOT/'prototype'/file.removeprefix('res://')
                if digest(disk.read_bytes())!=frame['file_sha256']:raise ValueError('parent art changed')
                result.setdefault(frame['file_sha256'],file)
    return result


PARENT_FRAMES = None


def record_rules(sid, image):
    r = source_catalog()
    # Derive the pointer table from the already authenticated source instruction.
    pointer_table = next(c for c in r['code_inputs'] if c['va']=='0x45356b')
    from capstone import Cs, CS_ARCH_X86, CS_MODE_32
    md=Cs(CS_ARCH_X86,CS_MODE_32);md.detail=True
    table=next(md.disasm(bytes.fromhex(pointer_table['instruction_hex']),0x45356b)).operands[-1].mem.disp
    pointer=struct.unpack_from('<I',image,table-BASE+sid*4)[0]
    count=struct.unpack_from('<h',image,0x6a85ac-BASE+sid*2)[0]
    r['templates']=[image[pointer-BASE+i*84:pointer-BASE+(i+1)*84].hex() for i in range(count)]
    for template in r['templates']:
        role=struct.unpack_from('<h',bytes.fromhex(template))[0]
        if role>=r['profile_subtract']:
            at=r['profile_base']+(role-r['profile_subtract'])*r['profile_stride']
            r['profiles'][str(role)]={'pointer':at,'profile_hex':image[at-BASE:at-BASE+r['profile_stride']].hex()}
            job=struct.unpack_from('<h',image,at-BASE+2)[0]
        else:
            at=r['character_base']+role*r['character_stride']
            raw=image[at-BASE:at-BASE+r['character_stride']]
            r['character_definitions'][str(role)]={'pointer':at,'row_hex':raw.hex()}
            job=struct.unpack_from('<h',raw,6)[0]
        at=r['job_base']+job*64;j=image[at-BASE:at-BASE+64]
        r['jobs'][str(job)]={'pointer':at,'row_hex':j.hex()}
        attack=struct.unpack_from('<H',j,24)[0];at=r['archetype_base']+attack*72
        r['archetypes'][str(attack)]={'pointer':at,'row_hex':image[at-BASE:at-BASE+72].hex()}
    return r


def skin(role,job,image,existing,output,actions=ACTIONS,extend_actions=False):
    pathptr,group,mode,variant=struct.unpack_from('<IhBb',image,6358328-BASE+job*8)
    path=GAME/image[pathptr-BASE:image.index(0,pathptr-BASE)].decode('ascii').replace('\\','/')
    if mode==2:
        p=struct.unpack_from('<b',image,6389904-BASE+job*40+role)[0];variant=p+1 if p else 0
    elif mode==0:variant=0
    key=f'job{job}_v{variant}'
    if key in existing and (not extend_actions or all(action in existing[key]['actions'] for action,_ in actions)):return key
    raw=path.read_bytes();o=dx.parse_dxanim(raw)
    table=struct.unpack_from('<I',image,6350928-BASE+(group+8)*4)[0]
    positions=struct.unpack_from('<I',image,6353008-BASE+(group+8)*4)[0]
    rows=[image[table-BASE+i*16:table-BASE+(i+1)*16].hex() for i in range(max(25,1+max(action for _,action in actions)))]
    n=max(bytes.fromhex(row)[i] for row in rows for i in range(0,16,2))+1
    rules={'source':{'local_file':path.relative_to(ROOT).as_posix(),'sha256':digest(raw)},
           'direction_map':[0,5,1,7,2,0,3,4,0,6],'action_rows':rows,
           'position_words':list(struct.unpack_from('<'+'H'*n,image,positions-BASE))}
    value,pixels=skin_inputs(role,job,rules,actions=actions,variant=variant)
    for frame in value['frames'].values():
        payload=BytesIO();pixels[frame['file']].save(payload,format='PNG');data=payload.getvalue();sha=digest(data)
        if sha in PARENT_FRAMES:
            frame['file']=PARENT_FRAMES[sha];frame['file_sha256']=sha;continue
        name=f'{key}/{Path(frame["file"]).name}';target=output/name
        target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
        frame['file']='res://assets/'+output.name+'/'+name;frame['file_sha256']=digest(target.read_bytes())
        PARENT_FRAMES[sha]=frame['file']
    existing[key]=value
    return key


def player_job(image, role, job):
    row = image[0x6b2d88-BASE+job*64:0x6b2d88-BASE+(job+1)*64]
    archetype = struct.unpack_from('<H', row, 24)[0]
    attack = image[0x6c2dc8-BASE+archetype*72:0x6c2dc8-BASE+(archetype+1)*72]
    return {'job':job, 'job_hex':row.hex(), 'archetype':archetype, 'attack_hex':attack.hex(),
             'family':row[2]-1, 'weapon_type':image[0x6f5088-BASE+role*1184+0x72]}


WINTER_ORDER = (32, 44, 29, 45)


def share_winter_frames(scene_id, skins):
    earlier = {}
    for other in WINTER_ORDER[:WINTER_ORDER.index(scene_id)]:
        path = OUT.parent/f'school_winter_{other}'/'catalog.json'
        for skin_data in json.loads(path.read_bytes())['skins'].values():
            for frame in skin_data['frames'].values():
                earlier.setdefault(frame['file_sha256'], frame['file'])
    for skin_data in skins.values():
        for frame in skin_data['frames'].values():
            if frame['file_sha256'] in earlier:
                frame['file'] = earlier[frame['file_sha256']]


def winter_patrol_routes(image, sid, actors):
    table = struct.unpack_from('<I', image, 0x6acb88-BASE+sid*4)[0]
    indices = {bytes.fromhex(actor['record_hex'])[0xa2] for actor in actors} - {0}
    routes = {}
    while indices:
        index = indices.pop()
        count, pointer = struct.unpack_from('<II', image, table-BASE+index*8)
        # Unused template selectors on MAP32 extend beyond the route table.
        if not 0 < count <= 255 or not BASE <= pointer <= BASE+len(image)-12*count:
            continue
        rows = [list(struct.unpack_from('<BB2xIb3x', image, pointer-BASE+i*12))
                for i in range(count)]
        routes[str(index)] = rows
        indices.update(row[3] for row in rows if row[3]>0 and str(row[3]) not in routes)
    return dict(sorted(routes.items(), key=lambda pair:int(pair[0])))


def export(seven=False, four=False, six=False, ten=False, thirteen=False, eighteen=False, nine=False, fourteen=False, twenty=False, twenty_one=False, thirty_five=False, twenty_two=False, twenty_four=False, forty_one=False, thirty_one=False, winter=0, early_scene=0):
    global PARENT_FRAMES
    if winter and winter not in (32, 44, 29, 45):
        raise ValueError(winter)
    if early_scene not in (0, 2, 3):
        raise ValueError(early_scene)
    full_roster=early_scene or thirty_five or twenty_two or twenty_four or forty_one or thirty_one or winter
    late=twenty or twenty_one or full_roster
    output=OUT.parent/{2:'school_two',3:'school_three'}[early_scene] if early_scene else OUT.parent/f'school_winter_{winter}' if winter else OUT.parent/'school_thirty_one' if thirty_one else OUT.parent/'school_forty_one' if forty_one else OUT.parent/'school_twenty_four' if twenty_four else OUT.parent/'school_twenty_two' if twenty_two else OUT.parent/'school_thirty_five' if thirty_five else OUT.parent/'school_twenty_one' if twenty_one else OUT.parent/'school_twenty' if twenty else OUT.parent/'school_fourteen' if fourteen else OUT.parent/'school_nine' if nine else OUT.parent/'school_eighteen' if eighteen else OUT.parent/'school_thirteen' if thirteen else OUT.parent/'school_ten' if ten else OUT.parent/'school_six' if six else OUT.parent/'school_four' if four else OUT.parent/'school_seven' if seven else OUT
    PARENT_FRAMES=parent_frames(seven or four or six or ten or thirteen or eighteen or nine or fourteen or late,four or six or ten or thirteen or eighteen or nine or fourteen or late,six or ten or thirteen or eighteen or nine or fourteen or late,ten or thirteen or eighteen or nine or fourteen or late,thirteen or eighteen or nine or fourteen or late,eighteen or nine or fourteen or late,nine or fourteen or late,fourteen or late,late,twenty_one or full_roster,full_roster,twenty_two or twenty_four or forty_one or thirty_one or winter)
    if twenty_four or forty_one or thirty_one or winter:
        parents = ('school_twenty_two','school_twenty_two_actions') + (('school_twenty_four',) if forty_one or thirty_one or winter else ()) + (('school_forty_one',) if thirty_one or winter else ()) + (('school_thirty_one',) if winter else ())
        if winter:
            parents += tuple(f'school_winter_{n}' for n in WINTER_ORDER[:WINTER_ORDER.index(winter)])
        for directory in parents:
            data=json.loads((OUT.parent/directory/'catalog.json').read_bytes())
            for value in data.get('skins',data).values():
                for frame in value['frames'].values():
                    path=ROOT/'prototype'/frame['file'].removeprefix('res://')
                    assert digest(path.read_bytes())==frame['file_sha256']
                    PARENT_FRAMES.setdefault(frame['file_sha256'],frame['file'])
    image=SOURCE.read_bytes();assert digest(image)==SOURCE_SHA256
    output.mkdir(parents=True,exist_ok=True)
    old=formation();terrain=bytes.fromhex(old['terrain_hex'])
    grid=[list(v[:3]) for v in struct.iter_unpack('<bbHH',bytes.fromhex(old['grid_hex']))]
    skins={};scenes={}
    for sid in ((early_scene,) if early_scene else (winter,) if winter else (31,) if thirty_one else (41,) if forty_one else (24,) if twenty_four else (22,) if twenty_two else (35,) if thirty_five else (21,) if twenty_one else (20,) if twenty else (14,) if fourteen else (9,) if nine else (18,) if eighteen else (13,) if thirteen else (10,) if ten else (6,) if six else (4,) if four else (7,) if seven else (8,17)):
        r=record_rules(sid,image);actors=[]
        for ordinal,t in enumerate(r['templates']):
            value=expected_record(t,rules=r);raw=bytes.fromhex(value['record_hex']);job=value['job']
            j=bytes.fromhex(r['jobs'][str(job)]['row_hex']);aid=struct.unpack_from('<H',j,24)[0]
            attack=bytes.fromhex(r['archetypes'][str(aid)]['row_hex'])
            actions=ACTIONS+[('summon_prepare',12),('summon',17)] if (four or ten or nine or fourteen or late) and raw[0x96]==2 else ACTIONS
            if (twenty_four or forty_one or thirty_one or winter) and aid not in (0,511):
                timing=image[0x611538-BASE+16*aid:0x611538-BASE+16*aid+3]
                actions=[(name,timing[('cast','attack','recover').index(name)] if name in ('cast','attack','recover') else action) for name,action in actions]
            actors.append({'instance_id':1249-ordinal,'work_index':249-ordinal,**value,
                'character_id':value['identity'],'cell':value['coordinates'],'skin_key':skin(value['identity'],job,image,skins,output,actions,extend_actions=late),
                'movement_type':raw[48], 'limits':{k:value[k] for k in ('hp_max','mp_max')},
                'combat':{**from_record(raw),'attack_id':aid,'attack_class':attack[5],'target_filter':attack[25]}})
            actors[-1]['limits'].update(hp=value['hp_max'],mp=value['mp_max'])
            if (four or ten or nine or fourteen or late) and raw[0x96]==2:actors[-1]['summon_interval']=struct.unpack_from('<I',bytes.fromhex(t),52)[0]
            if twenty_four or forty_one or thirty_one or winter:
                actors[-1]['search_mode']=bytes.fromhex(t)[0x24]
                actors[-1]['vision']=raw[0x2c]
                actors[-1]['poison_modifier']=struct.unpack_from('<b',j,34)[0]
            actors[-1].pop('profile_hex');actors[-1].pop('profile_pointer')
        logical=(GAME/f'DATA/TACTICS/MAP/MAP{sid:02}.BIN').read_bytes()
        graphics=(GAME/f'DATA/TACTICS/MAP/MAP{sid:02}.MAP').read_bytes()
        layout=logical_cells(logical);atlas=output/f'map{sid:02}.png'
        atlas_image(graphics,layout,map_textures(graphics,layout)).save(atlas)
        config=image[0x6ad1d0-BASE+sid*42:0x6ad1d0-BASE+(sid+1)*42]
        scenes[str(sid)]={'scene_id':sid,'configuration_hex':config.hex(),'origin':list(config[7:9]),
            'formation_radius':config[15],'formation_grid':grid,'initial_rotation':0,'permutation_size':5,'rotation_multiplier':3,
            'cells':layout['cells'],'passability':[[int(mode==4 or struct.unpack_from('<i',terrain,c[0]*76+mode*16+12)[0]!=0) for c in layout['cells']] for mode in range(5)],
            'actors':actors,'atlas':'res://assets/'+output.name+'/'+atlas.name,'atlas_sha256':digest(atlas.read_bytes()),
            'interaction':{'logic_hz':30,'move_interval':12,'delta_cap':0.2},'player_skins':{}}
        if early_scene==2:
            scenes[str(sid)]['regions']={str(n):[i for i in range(len(layout['cells'])) if logical[18+i*6]==n] for n in (1,2)}
        if sid==17:scenes[str(sid)]['exit_cells']=[i for i in range(len(layout['cells'])) if logical[18+i*6]==1]
    attack=source_rules()
    players=((3,10),(4,6),(9,7),(5,4))
    if seven or four or six or ten or thirteen or eighteen or nine or fourteen or late:players+=((8,8),)
    if four or six or ten or thirteen or eighteen or nine or fourteen or late:players+=((1,6),(6,2))
    if six or ten or thirteen or eighteen or nine or fourteen or late:players+=((2,4),)
    if full_roster:
        players+=tuple((role,struct.unpack_from('<H',image,0x6f5088-BASE+role*1184+6)[0]) for role in (13,16,17))
    if forty_one:
        players = tuple(pair for pair in players if pair[0] != 2)
        players += tuple((role, struct.unpack_from('<H', image, 0x6f5088-BASE+role*1184+6)[0])
                         for role in (11, 14, 15, 18, 32))
    if thirty_one or winter:
        players = tuple(pair for pair in players if pair[0] != 4)
        players += tuple((role, struct.unpack_from('<H', image, 0x6f5088-BASE+role*1184+6)[0])
                         for role in (7, 11, 14, 15, 18, 28, 32))
    if winter:
        existing = {role for role, _ in players}
        players += tuple((role, struct.unpack_from('<H',image,0x6f5088-BASE+role*1184+6)[0])
                         for role in ((19,20,21) if winter==32 else (4,19,20,21,22,23,24) if winter in (44,29) else (4,10,12,19,20,21,22,23,24,25,26,27,29,30,31,33)) if role not in existing)
    if early_scene:
        players = tuple((role, struct.unpack_from('<H', image, 0x6f5088-BASE+role*1184+6)[0])
                        for role in (10,6,5,4,3,7,9,11,2,1,12,14,15,17,18,13,16,20,21,23))
        for path in sorted(OUT.parent.glob('school_*/catalog.json')):
            if path.parent.name in ('school_two','school_three'):
                continue
            data = json.loads(path.read_bytes())
            for skin_data in data.get('skins', {}).values():
                for frame in skin_data['frames'].values():
                    PARENT_FRAMES.setdefault(frame['file_sha256'], frame['file'])
    for role,job in players:
        actions=ACTIONS
        if full_roster:
            # 477980 selects cast/release/recovery from each skill's 611538 row.
            basic=struct.unpack_from('<H',image,0x6b2d88-BASE+64*job+24)[0]
            actions=list(ACTIONS)
            for skill in [basic]+{3:[57,59],4:[20],5:[11],9:[31]}.get(role,[]):
                row=image[0x611538-BASE+16*skill:0x611538-BASE+16*skill+3]
                prefix='basic' if skill==basic else str(skill)
                actions.extend((prefix+'_'+name,action) for name,action in zip(('cast','attack','recover'),row))
        key=skin(role,job,image,skins,output,actions,extend_actions=full_roster)
        for scene in scenes.values():scene['player_skins'][str(role)]=key
        attack['jobs'][str(job)]=player_job(image,role,job)
    result={'schema_version':1,'source_image_sha256':SOURCE_SHA256,'scenes':scenes,'skins':skins,'attack_rules':attack}
    if seven or four or six or ten or thirteen or eighteen or nine or fourteen or late:
        from tools.school_adventure_scene_rules import catalog as scene_rules
        rules=scene_rules((sid,),(112,146,159,161) if winter else (146,) if forty_one or thirty_one else (112,146,159) if twenty_four else (146,161) if twenty_one else (146,) if fourteen else (112,146) if ten else (130,146,161) if eighteen else ())['scenes'][str(sid)]
        scene=scenes[str(sid)]
        scene['scripts']=rules['scripts']
        scene['script_sha256']=rules['script_sha256']
        if seven or ten or thirteen:scene['regions']={str(n):[i for i in range(len(layout['cells'])) if logical[18+i*6]==n] for n in (range(1,10) if thirteen else range(1,7) if ten else (1,2))}
    if twenty_four:
        numbers=struct.unpack_from('<6h',image,0x5ff83c-BASE)
        assert numbers==(2,3,4,5,6,-1)
        scene['grade_objects']=list(numbers[:-1])
        scene['regions']={'1':[i for i in range(len(layout['cells'])) if logical[18+i*6]==1]}
        table=struct.unpack_from('<I',image,0x6acb88-BASE+sid*4)[0]
        scene['patrol_routes']={}
        for index in range(1,13):
            count,ptr=struct.unpack_from('<II',image,table-BASE+index*8)
            scene['patrol_routes'][str(index)]=[list(struct.unpack_from('<BB2xIb3x',image,ptr-BASE+i*12)) for i in range(count)]
    if forty_one:
        numbers = struct.unpack_from('<2h', image, 0x5ff898-BASE)
        assert numbers == (2,-1)
        scene['grade_objects'] = [numbers[0]]
        table = struct.unpack_from('<I',image,0x6acb88-BASE+sid*4)[0]
        scene['patrol_routes'] = {}
        for index in (1,2,3):
            count, ptr = struct.unpack_from('<II',image,table-BASE+index*8)
            scene['patrol_routes'][str(index)] = [
                list(struct.unpack_from('<BB2xIb3x',image,ptr-BASE+i*12)) for i in range(count)]
    if thirty_one:
        scene['grade_objects'] = list(struct.unpack_from('<3h',image,0x5ff880-BASE))
        scene['regions'] = {'1': [y*layout['cell_size'][0]+x for x,y in rules['event1_cells']]}
        table = struct.unpack_from('<I',image,0x6acb88-BASE+sid*4)[0]
        scene['patrol_routes'] = {}
        for index in sorted({bytes.fromhex(a['record_hex'])[0xa2] for a in actors} - {0}):
            count, ptr = struct.unpack_from('<II',image,table-BASE+index*8)
            scene['patrol_routes'][str(index)] = [
                list(struct.unpack_from('<BB2xIb3x',image,ptr-BASE+i*12)) for i in range(count)]
    if winter:
        scene['cell_size'] = layout['cell_size']
        scene['regions'] = {str(region): [i for i in range(len(layout['cells'])) if logical[18+i*6]==region]
                            for region in sorted(set(logical[18::6]) - {0})}
        scene['patrol_routes'] = winter_patrol_routes(image, sid, actors)
    if twenty_two:
        numbers=struct.unpack_from('<2h',image,0x5ff838-BASE)
        assert numbers==(2,-1)
        scene['grade_objects']=list(numbers[:-1])
    if twenty:
        numbers=struct.unpack_from('<6h',image,0x5ff804-BASE)
        assert numbers[-1]==-1
        scene['grade_objects']=list(numbers[:-1])
    if fourteen:
        scene['regions']={'1':[i for i in range(len(layout['cells'])) if logical[18+i*6]==1]}
    if twenty_one:
        # T0021:1F8 jumps directly from the opening setup to the timer slots.
        script=(GAME/'DATA/TACTICS/SCRIPT/T0021.BIN').read_bytes()
        assert struct.unpack_from('<HHI',script,0x1f8)==(11,8,0xba)
        assert struct.unpack_from('<H',script,0x1c4+0xba)[0]==124
        scene['scripts'][0]['pages']=[]
        scene['grade_groups']=[]
        for address,count in ((0x5ff810,4),(0x5ff81c,13)):
            numbers=struct.unpack_from(f'<{count+1}h',image,address-BASE)
            assert numbers[-1]==-1
            scene['grade_groups'].append(list(numbers[:-1]))
        routes=struct.unpack_from('<I',image,0x6acb88-BASE+sid*4)[0]
        scene['patrol_routes']={}
        for index in range(1,28):
            count,ptr=struct.unpack_from('<II',image,routes-BASE+index*8)
            scene['patrol_routes'][str(index)]=[list(struct.unpack_from('<BB2xIb3x',image,ptr-BASE+i*12)) for i in range(count)]
    if fourteen or twenty:
        table=struct.unpack_from('<I',image,0x6acb88-BASE+sid*4)[0]
        scene['patrol_goals']=[]
        for index in range(1,5 if twenty else 7):
            count,ptr=struct.unpack_from('<II',image,table-BASE+index*8)
            x,y,wait,link=struct.unpack_from('<BB2xIb3x',image,ptr-BASE)
            assert (count,wait,link)==(1,0,-1)
            scene['patrol_goals'].append([x,y])
    if eighteen:
        scene['grade_objects']=list(struct.unpack_from('<3h',image,0x5ff7fc-BASE))
    if six or ten:
        objective_numbers=struct.unpack_from('<7h' if ten else '<5h',image,(0x5ff79c if ten else 0x5ff774)-BASE)
        assert objective_numbers[-1]==-1
        scene['grade_objects']=list(objective_numbers[:-1])
    if ten:
        # 4DA7F0 -> 47A800 -> 47ED90/47F090. Field +8 links patrol lists.
        routes=struct.unpack_from('<I',image,0x6acb88-BASE+sid*4)[0]
        route=bytes.fromhex(actors[0]['record_hex'])[0xa2]
        scene['elder_route']=[]
        while route>0:
            count,ptr=struct.unpack_from('<II',image,routes-BASE+route*8)
            rows=[list(struct.unpack_from('<BB2xIb3x',image,ptr-BASE+i*12)) for i in range(count)]
            assert len(scene['elder_route'])<100 and all(row[3]==0 for row in rows[:-1])
            scene['elder_route'].extend(row[:3] for row in rows)
            route=rows[-1][3]
        assert route==-1
    if four or six or ten or thirteen or eighteen or nine or fourteen or late:
        from tools.school_map_common_catalog import map_common_inputs
        from tools.school_map_common_emulation import map_common_resource
        common,_=map_common_resource()
        entries=map_common_inputs(common)['first_section_entries']
        masks={}
        for radius in (range(33) if late else range(3,21)):
            size=(2*radius+1)**2
            start=entries[radius]['file_offset']
            masks[str(radius)]=common[start:start+size].hex()
        scene['spells']={'rows':{str(i):image[0x6c2dc8-BASE+i*72:0x6c2dc8-BASE+(i+1)*72].hex() for i in ((57,59,31,11,20) if full_roster else (57,59,31) if twenty_one else (57,59))},'masks':masks}
        scene['bow189_hex']=image[0x6d5118-BASE+189*56:0x6d5118-BASE+190*56].hex()
    if winter:
        share_winter_frames(winter, skins)
    target=output/'catalog.json';target.write_text(json.dumps(result,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')
    print(target.stat().st_size,digest(target.read_bytes()),'actors',[(s,len(v['actors'])) for s,v in scenes.items()])

def export_twenty_two_actions():
    """Add the three differing attack timelines without changing battle input data."""
    global PARENT_FRAMES
    image=SOURCE.read_bytes()
    assert digest(image)==SOURCE_SHA256
    base=json.loads((OUT.parent/'school_twenty_two/catalog.json').read_bytes())
    output=OUT.parent/'school_twenty_two_actions'
    output.mkdir(parents=True,exist_ok=True)
    PARENT_FRAMES=parent_frames(True,True,True,True,True,True,True,True,True,True,True,True)
    for source in base['skins'].values():
        for frame in source['frames'].values():
            PARENT_FRAMES.setdefault(frame['file_sha256'],frame['file'])
    skins={}
    for actor in base['scenes']['22']['actors']:
        if actor['character_id']==406:continue
        attack=actor['combat']['attack_id']
        timing=image[0x611538-BASE+16*attack:0x611538-BASE+16*attack+3]
        if list(timing)==[11,5,14]:continue
        key=skin(actor['identity'],actor['job'],image,skins,output,
                 list(zip(('basic_cast','basic_attack','basic_recover'),timing)))
        assert key==actor['skin_key']
    delta={}
    for key,value in skins.items():
        delta[key]={'actions':value['actions'],'frames':{
            index:frame for index,frame in value['frames'].items() if index not in base['skins'][key]['frames']}}
    target=output/'catalog.json'
    target.write_bytes((json.dumps(delta,ensure_ascii=False,separators=(',',':'))+chr(10)).encode('utf8'))
    print(target.stat().st_size,digest(target.read_bytes()),list(delta))


def export_may_five():
    """Only the new player's attack inputs. Both player skins already ship with scene 7."""
    image = SOURCE.read_bytes()
    assert digest(image) == SOURCE_SHA256
    role, job = 6, 2
    rules = player_job(image, role, job)
    path = ROOT/'prototype/data/school_may_five_sortie_job.json'
    path.write_bytes((json.dumps(rules, separators=(",", ":"))+'\n').encode("utf8"))


def export_july_five():
    """Add the two Chapter304 recruits to scene 17 without re-exporting the map."""
    global PARENT_FRAMES
    image=SOURCE.read_bytes()
    assert digest(image)==SOURCE_SHA256
    output=OUT.parent/'school_july_five'
    output.mkdir(parents=True,exist_ok=True)
    PARENT_FRAMES=parent_frames(True,True,True,True,True,True,True,True,True)
    data={'source_image_sha256':SOURCE_SHA256,'player_skins':{},'skins':{},'jobs':{}}
    for role in (16,17):
        job=struct.unpack_from('<H',image,0x6f5088-BASE+role*1184+6)[0]
        data['player_skins'][str(role)]=skin(role,job,image,data['skins'],output)
        rules=player_job(image,role,job)
        assert data['jobs'].get(str(job),rules)==rules
        data['jobs'][str(job)]=rules
    (output/'catalog.json').write_bytes((json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n').encode('utf8'))


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--winter',type=int,choices=(32,44,29,45))
    parser.add_argument('--seven',action='store_true')
    parser.add_argument('--four',action='store_true')
    parser.add_argument('--thirty-one',action='store_true')
    parser.add_argument('--forty-one',action='store_true')
    parser.add_argument('--twenty-four',action='store_true')
    parser.add_argument('--twenty-two-actions',action='store_true')
    parser.add_argument('--twenty-two',action='store_true')
    parser.add_argument('--thirty-five',action='store_true')
    parser.add_argument('--twenty-one',action='store_true')
    parser.add_argument('--twenty',action='store_true')
    parser.add_argument('--fourteen',action='store_true')
    parser.add_argument('--nine',action='store_true')
    parser.add_argument('--eighteen',action='store_true')
    parser.add_argument('--thirteen',action='store_true')
    parser.add_argument('--ten',action='store_true')
    parser.add_argument('--six',action='store_true')
    parser.add_argument('--may-five',action='store_true')
    parser.add_argument('--july-five',action='store_true')
    parser.add_argument("--early-scene",type=int,choices=(2,3))
    args=parser.parse_args()
    if args.early_scene: export(early_scene=args.early_scene)
    elif args.winter: export(winter=args.winter)
    elif args.twenty_two_actions: export_twenty_two_actions()
    elif args.july_five: export_july_five()
    elif args.may_five: export_may_five()
    else: export(args.seven,args.four,args.six,args.ten,args.thirteen,args.eighteen,args.nine,args.fourteen,args.twenty,args.twenty_one,args.thirty_five,args.twenty_two,args.twenty_four,args.forty_one,args.thirty_one)
