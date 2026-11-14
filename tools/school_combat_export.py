"""Source initial scene actors and current-squad attack presentation for the trial."""
import argparse
import json
import struct
from copy import deepcopy
from pathlib import Path
from tools.school_field_export import skin_inputs, digest, ROOT, SKINS
from tools.school_current_units_catalog import source_catalog as current_source
from tools.school_scene_unit_work_catalog import source_catalog as prefix_source
from tools.school_scene_unit_constructor_catalog import source_catalog as npc_source
from tools.school_scene_second_constructor_catalog import source_catalog as second_source
from tools.school_scene_batch_catalog import source_catalog as batch_source
from tools.school_scene_remaining_catalog import source_catalog as remaining_source
from tools.school_enemy_records_catalog import source_catalog as record_source, expected_record
from tools.school_attack_inputs import from_record

OUTPUT = ROOT/'prototype/assets/school_combat'
ACTIONS = [('idle',1),('move',3),('cast',11),('attack',5),('recover',14)]


def source_inputs(*, reinforcements=False):
    current = current_source(); prefix = prefix_source(); records = record_source()
    constructors = {'4':npc_source()['constructor'],'387':second_source()['constructor']}
    constructors.update(batch_source()['constructors']); constructors.update(remaining_source()['constructors'])
    actors = []; skins = {}; images = {}
    for identity,job in ({} if reinforcements else SKINS).items():
        skin,pixels = skin_inputs(identity,job,current['jobs'][str(job)],actions=ACTIONS)
        skins[str(identity)] = skin; images.update(pixels)
    for ordinal,template in enumerate(records['templates']):
        record = expected_record(template,rules=records)
        if (record['state'] != 1) != reinforcements: continue
        role,job = record['identity'],record['job']; selection = prefix['jobs'][str(job)]
        variant = 0 if selection['mode']==0 else selection['fixed_variant'] if selection['mode']==1 else (
            selection['palettes_by_character'][role]+1 if selection['palettes_by_character'][role] else 0)
        key = 'scene_%d_v%d' % (job,variant)
        if key not in skins:
            actions = ACTIONS + [('summon_prepare',12),('summon',17),('summon_recover',15)] if reinforcements else ACTIONS
            skin,pixels = skin_inputs(role,job,constructors[str(job)],actions=actions if record['category']==5 else [('idle',1)],variant=variant)
            mapped = {}
            for frame in skin['frames'].values():
                old = frame['file']; new = key+'/'+Path(old).name
                mapped[new] = pixels[old]; frame['file'] = new
            skins[key] = skin; images.update(mapped)
        raw = bytes.fromhex(record['record_hex']); j = bytes.fromhex(records['jobs'][str(job)]['row_hex'])
        attack_id = struct.unpack_from('<H',j,24)[0]; w = bytes.fromhex(records['archetypes'][str(attack_id)]['row_hex'])
        actors.append({'instance_id':1000+249-ordinal,'work_index':249-ordinal,'ordinal':ordinal,
            'character_id':role,'job':job,'category':record['category'],'cell':record['coordinates'],
            'record_hex':record['record_hex'],'skin_key':key,'movement_type':raw[48],
            'limits':{'hp':record['hp_max'],'hp_max':record['hp_max'],'mp':record['mp_max'],'mp_max':record['mp_max']},
            'combat':{**from_record(raw),'attack_id':attack_id,'attack_class':w[5],'target_filter':w[25]}})
    if reinforcements:
        if len(actors) != 24 or any(a['category']!=5 for a in actors):
            raise ValueError('deferred scene templates differ')
        # The last sub20 ownership request makes the already present pupil5 an ally.
        # Reuse her original role art without rewriting the frozen initial catalog.
        variant=prefix['jobs']['4']['palettes_by_character'][5]+1
        skin,pixels = skin_inputs(5,4,constructors['4'],actions=ACTIONS,variant=variant)
        mapped={}
        for frame in skin['frames'].values():
            old=frame['file'];new='scene_4_v%d/'%variant+Path(old).name
            mapped[new]=pixels[old];frame['file']=new
        skins['scene_4_v%d'%variant]=skin;images.update(mapped)
    elif len(actors) != 11 or sum(a['category']==5 for a in actors) != 7:
        raise ValueError('initial scene activity differs')
    return {'schema_version':1,'scene_id':5,'source_image_sha256':records['source_image_sha256'],
        'source_template_count':len(records['templates']),'actors':actors,'skins':skins,
        'scope':'Source initial active records and art; no inactive/deferred wave activation or original AI/world/HP/settlement execution.',
        'trial_policy':{'seed':20261014,'move_interval':12,'enemy_scheduling':'declared_nearest_player_bfs',
            'range_metric':'declared_four_neighbour_manhattan','HP_application':'declared_scalar_damage_only',
            'death_presentation':'declared_fade_and_removal','victory_or_reward_authority':False}},images


def export(destination=OUTPUT, *, reinforcements=False):
    catalog,images = source_inputs(reinforcements=reinforcements)
    asset_dir = 'school_reinforcements' if reinforcements else 'school_combat'
    if reinforcements:
        from tools.ybc32_disasm import parse, load_pool
        script = (ROOT/'CROSS HERMIT/CROSS HERMIT/DATA/TACTICS/SCRIPT/T0005.BIN').read_bytes()
        if digest(script) != '44ca546b5ea90ec23a4bc7d8dffeac6547a44bfd035383c91983f7c13ae72a52':
            raise ValueError('T0005 identity')
        _,_,pc,pool = next(row for row in parse(script) if row[:2]==(0,20))
        texts = load_pool(script,pool); pages=[]; current=[]
        while True:
            opcode,advance = struct.unpack_from('<HH',script,pc)
            if opcode==17:
                index, = struct.unpack_from('<H',script,pc+4)
                current.append({'text_index':index,'text':texts[index][2],'source_offset':pc})
            if opcode==51:
                pages.append(current); current=[]
            if opcode==19:break
            if advance<4:raise ValueError('event instruction bounds')
            pc+=advance
        if current or sum(map(len,pages))!=58:raise ValueError('event20 dialogue sequence')
        catalog['event20_dialogue']=pages
        from tools.school_map_common_catalog import map_common_inputs
        from tools.school_map_common_emulation import map_common_resource
        common,identity=map_common_resource()
        entry=map_common_inputs(common)['first_section_entries'][5]
        mask=common[entry['file_offset']:entry['file_offset']+entry['bytes']]
        if len(mask)!=124 or any(mask[121:]):raise ValueError('capture mask bounds')
        catalog['capture_mask']={'width':11,'height':11,'hex':mask[:121].hex(),
            'source':identity,'entry':entry}
        catalog['source_script_sha256']=digest(script)
        catalog['scope']='Source inactive records, art and event20 text; activation timing is the explicitly declared remake scheduler.'
    for filename,image in images.items():
        target=destination/filename;target.parent.mkdir(parents=True,exist_ok=True);image.save(target)
    for skin in catalog['skins'].values():
        for frame in skin['frames'].values():
            frame['file_sha256']=digest((destination/frame['file']).read_bytes())
            frame['file']='res://assets/'+asset_dir+'/'+frame['file']
    (destination/'catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8',newline='\n')
    return catalog


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--out',type=Path)
    parser.add_argument('--reinforcements',action='store_true')
    args=parser.parse_args();catalog=export(args.out or (ROOT/'prototype/assets/school_reinforcements' if args.reinforcements else OUTPUT),reinforcements=args.reinforcements)
    print('Source initial actors=%d; enemy actors=%d; directional skins=%d; frames=%d' % (
        len(catalog['actors']),sum(a['category']==5 for a in catalog['actors']),len(catalog['skins']),sum(len(s['frames']) for s in catalog['skins'].values())))
