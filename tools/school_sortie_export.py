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


def parent_frames(include_sorties=False):
    result={}
    for name in ('school_field','school_combat','school_reinforcements') + (('school_sorties',) if include_sorties else ()):
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


def skin(role,job,image,existing,output):
    pathptr,group,mode,variant=struct.unpack_from('<IhBb',image,6358328-BASE+job*8)
    path=GAME/image[pathptr-BASE:image.index(0,pathptr-BASE)].decode('ascii').replace('\\','/')
    if mode==2:
        p=struct.unpack_from('<b',image,6389904-BASE+job*40+role)[0];variant=p+1 if p else 0
    elif mode==0:variant=0
    key=f'job{job}_v{variant}'
    if key in existing:return key
    raw=path.read_bytes();o=dx.parse_dxanim(raw)
    table=struct.unpack_from('<I',image,6350928-BASE+(group+8)*4)[0]
    positions=struct.unpack_from('<I',image,6353008-BASE+(group+8)*4)[0]
    rows=[image[table-BASE+i*16:table-BASE+(i+1)*16].hex() for i in range(25)]
    n=max(bytes.fromhex(row)[i] for row in rows for i in range(0,16,2))+1
    rules={'source':{'local_file':path.relative_to(ROOT).as_posix(),'sha256':digest(raw)},
           'direction_map':[0,5,1,7,2,0,3,4,0,6],'action_rows':rows,
           'position_words':list(struct.unpack_from('<'+'H'*n,image,positions-BASE))}
    value,pixels=skin_inputs(role,job,rules,actions=ACTIONS,variant=variant)
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


def export(seven=False):
    global PARENT_FRAMES
    output=OUT.parent/'school_seven' if seven else OUT
    PARENT_FRAMES=parent_frames(seven)
    image=SOURCE.read_bytes();assert digest(image)==SOURCE_SHA256
    output.mkdir(parents=True,exist_ok=True)
    old=formation();terrain=bytes.fromhex(old['terrain_hex'])
    grid=[list(v[:3]) for v in struct.iter_unpack('<bbHH',bytes.fromhex(old['grid_hex']))]
    skins={};scenes={}
    for sid in ((7,) if seven else (8,17)):
        r=record_rules(sid,image);actors=[]
        for ordinal,t in enumerate(r['templates']):
            value=expected_record(t,rules=r);raw=bytes.fromhex(value['record_hex']);job=value['job']
            j=bytes.fromhex(r['jobs'][str(job)]['row_hex']);aid=struct.unpack_from('<H',j,24)[0]
            attack=bytes.fromhex(r['archetypes'][str(aid)]['row_hex'])
            actors.append({'instance_id':1249-ordinal,'work_index':249-ordinal,**value,
                'character_id':value['identity'],'cell':value['coordinates'],'skin_key':skin(value['identity'],job,image,skins,output),
                'movement_type':raw[48], 'limits':{k:value[k] for k in ('hp_max','mp_max')},
                'combat':{**from_record(raw),'attack_id':aid,'attack_class':attack[5],'target_filter':attack[25]}})
            actors[-1]['limits'].update(hp=value['hp_max'],mp=value['mp_max'])
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
    for role,job in ((3,10),(4,6),(9,7),(5,4)) + (((8,8),) if seven else ()):
        key=skin(role,job,image,skins,output)
        for scene in scenes.values():scene['player_skins'][str(role)]=key
        attack['jobs'][str(job)]=player_job(image,role,job)
    result={'schema_version':1,'source_image_sha256':SOURCE_SHA256,'scenes':scenes,'skins':skins,'attack_rules':attack}
    if seven:
        from tools.school_adventure_scene_rules import catalog as scene_rules
        rules=scene_rules((7,))['scenes']['7']
        scene=scenes['7']
        scene['scripts']=rules['scripts']
        scene['script_sha256']=rules['script_sha256']
        scene['regions']={str(n):[i for i in range(len(layout['cells'])) if logical[18+i*6]==n] for n in (1,2)}
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


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--seven',action='store_true')
    parser.add_argument('--may-five',action='store_true')
    args=parser.parse_args()
    if args.may_five: export_may_five()
    else: export(args.seven)
