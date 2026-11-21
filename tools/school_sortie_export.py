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


def parent_frames(include_sorties=False, include_seven=False, include_four=False, include_six=False, include_ten=False, include_thirteen=False, include_eighteen=False, include_nine=False, include_fourteen=False):
    result={}
    for name in ('school_field','school_combat','school_reinforcements') + (('school_sorties',) if include_sorties else ()) + (('school_seven',) if include_seven else ()) + (('school_four',) if include_four else ()) + (('school_six',) if include_six else ()) + (('school_ten',) if include_ten else ()) + (('school_thirteen',) if include_thirteen else ()) + (('school_eighteen',) if include_eighteen else ()) + (('school_nine',) if include_nine else ()) + (('school_fourteen',) if include_fourteen else ()):
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
    rows=[image[table-BASE+i*16:table-BASE+(i+1)*16].hex() for i in range(25)]
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


def export(seven=False, four=False, six=False, ten=False, thirteen=False, eighteen=False, nine=False, fourteen=False, twenty=False):
    global PARENT_FRAMES
    output=OUT.parent/'school_twenty' if twenty else OUT.parent/'school_fourteen' if fourteen else OUT.parent/'school_nine' if nine else OUT.parent/'school_eighteen' if eighteen else OUT.parent/'school_thirteen' if thirteen else OUT.parent/'school_ten' if ten else OUT.parent/'school_six' if six else OUT.parent/'school_four' if four else OUT.parent/'school_seven' if seven else OUT
    PARENT_FRAMES=parent_frames(seven or four or six or ten or thirteen or eighteen or nine or fourteen or twenty,four or six or ten or thirteen or eighteen or nine or fourteen or twenty,six or ten or thirteen or eighteen or nine or fourteen or twenty,ten or thirteen or eighteen or nine or fourteen or twenty,thirteen or eighteen or nine or fourteen or twenty,eighteen or nine or fourteen or twenty,nine or fourteen or twenty,fourteen or twenty,twenty)
    image=SOURCE.read_bytes();assert digest(image)==SOURCE_SHA256
    output.mkdir(parents=True,exist_ok=True)
    old=formation();terrain=bytes.fromhex(old['terrain_hex'])
    grid=[list(v[:3]) for v in struct.iter_unpack('<bbHH',bytes.fromhex(old['grid_hex']))]
    skins={};scenes={}
    for sid in ((20,) if twenty else (14,) if fourteen else (9,) if nine else (18,) if eighteen else (13,) if thirteen else (10,) if ten else (6,) if six else (4,) if four else (7,) if seven else (8,17)):
        r=record_rules(sid,image);actors=[]
        for ordinal,t in enumerate(r['templates']):
            value=expected_record(t,rules=r);raw=bytes.fromhex(value['record_hex']);job=value['job']
            j=bytes.fromhex(r['jobs'][str(job)]['row_hex']);aid=struct.unpack_from('<H',j,24)[0]
            attack=bytes.fromhex(r['archetypes'][str(aid)]['row_hex'])
            actions=ACTIONS+[('summon_prepare',12),('summon',17)] if (four or ten or nine or fourteen or twenty) and raw[0x96]==2 else ACTIONS
            actors.append({'instance_id':1249-ordinal,'work_index':249-ordinal,**value,
                'character_id':value['identity'],'cell':value['coordinates'],'skin_key':skin(value['identity'],job,image,skins,output,actions,extend_actions=twenty),
                'movement_type':raw[48], 'limits':{k:value[k] for k in ('hp_max','mp_max')},
                'combat':{**from_record(raw),'attack_id':aid,'attack_class':attack[5],'target_filter':attack[25]}})
            actors[-1]['limits'].update(hp=value['hp_max'],mp=value['mp_max'])
            if (four or ten or nine or fourteen or twenty) and raw[0x96]==2:actors[-1]['summon_interval']=struct.unpack_from('<I',bytes.fromhex(t),52)[0]
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
        if sid==17:scenes[str(sid)]['exit_cells']=[i for i in range(len(layout['cells'])) if logical[18+i*6]==1]
    attack=source_rules()
    players=((3,10),(4,6),(9,7),(5,4))
    if seven or four or six or ten or thirteen or eighteen or nine or fourteen or twenty:players+=((8,8),)
    if four or six or ten or thirteen or eighteen or nine or fourteen or twenty:players+=((1,6),(6,2))
    if six or ten or thirteen or eighteen or nine or fourteen or twenty:players+=((2,4),)
    for role,job in players:
        key=skin(role,job,image,skins,output)
        for scene in scenes.values():scene['player_skins'][str(role)]=key
        attack['jobs'][str(job)]=player_job(image,role,job)
    result={'schema_version':1,'source_image_sha256':SOURCE_SHA256,'scenes':scenes,'skins':skins,'attack_rules':attack}
    if seven or four or six or ten or thirteen or eighteen or nine or fourteen or twenty:
        from tools.school_adventure_scene_rules import catalog as scene_rules
        rules=scene_rules((sid,),(146,) if fourteen else (112,146) if ten else (130,146,161) if eighteen else ())['scenes'][str(sid)]
        scene=scenes[str(sid)]
        scene['scripts']=rules['scripts']
        scene['script_sha256']=rules['script_sha256']
        if seven or ten or thirteen:scene['regions']={str(n):[i for i in range(len(layout['cells'])) if logical[18+i*6]==n] for n in (range(1,10) if thirteen else range(1,7) if ten else (1,2))}
    if twenty:
        numbers=struct.unpack_from('<6h',image,0x5ff804-BASE)
        assert numbers[-1]==-1
        scene['grade_objects']=list(numbers[:-1])
    if fourteen:
        scene['regions']={'1':[i for i in range(len(layout['cells'])) if logical[18+i*6]==1]}
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
    if four or six or ten or thirteen or eighteen or nine or fourteen or twenty:
        from tools.school_map_common_catalog import map_common_inputs
        from tools.school_map_common_emulation import map_common_resource
        common,_=map_common_resource()
        entries=map_common_inputs(common)['first_section_entries']
        masks={}
        for radius in (range(33) if twenty else range(3,21)):
            size=(2*radius+1)**2
            start=entries[radius]['file_offset']
            masks[str(radius)]=common[start:start+size].hex()
        scene['spells']={'rows':{str(i):image[0x6c2dc8-BASE+i*72:0x6c2dc8-BASE+(i+1)*72].hex() for i in (57,59)},'masks':masks}
        scene['bow189_hex']=image[0x6d5118-BASE+189*56:0x6d5118-BASE+190*56].hex()
    target=output/'catalog.json';target.write_text(json.dumps(result,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')
    print(target.stat().st_size,digest(target.read_bytes()),'actors',[(s,len(v['actors'])) for s,v in scenes.items()])

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
    parser.add_argument('--seven',action='store_true')
    parser.add_argument('--four',action='store_true')
    parser.add_argument('--twenty',action='store_true')
    parser.add_argument('--fourteen',action='store_true')
    parser.add_argument('--nine',action='store_true')
    parser.add_argument('--eighteen',action='store_true')
    parser.add_argument('--thirteen',action='store_true')
    parser.add_argument('--ten',action='store_true')
    parser.add_argument('--six',action='store_true')
    parser.add_argument('--may-five',action='store_true')
    parser.add_argument('--july-five',action='store_true')
    args=parser.parse_args()
    if args.july_five: export_july_five()
    elif args.may_five: export_may_five()
    else: export(args.seven,args.four,args.six,args.ten,args.thirteen,args.eighteen,args.nine,args.fourteen,args.twenty)
