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


def source_inputs():
    current = current_source(); prefix = prefix_source(); records = record_source()
    constructors = {'4':npc_source()['constructor'],'387':second_source()['constructor']}
    constructors.update(batch_source()['constructors']); constructors.update(remaining_source()['constructors'])
    actors = []; skins = {}; images = {}
    for identity,job in SKINS.items():
        skin,pixels = skin_inputs(identity,job,current['jobs'][str(job)],actions=ACTIONS)
        skins[str(identity)] = skin; images.update(pixels)
    for ordinal,template in enumerate(records['templates']):
        record = expected_record(template,rules=records)
        if record['state'] != 1: continue
        role,job = record['identity'],record['job']; selection = prefix['jobs'][str(job)]
        variant = 0 if selection['mode']==0 else selection['fixed_variant'] if selection['mode']==1 else (
            selection['palettes_by_character'][role]+1 if selection['palettes_by_character'][role] else 0)
        key = 'scene_%d_v%d' % (job,variant)
        if key not in skins:
            skin,pixels = skin_inputs(role,job,constructors[str(job)],actions=ACTIONS if record['category']==5 else [('idle',1)],variant=variant)
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
    if len(actors) != 11 or sum(a['category']==5 for a in actors) != 7:
        raise ValueError('initial scene activity differs')
    return {'schema_version':1,'scene_id':5,'source_image_sha256':records['source_image_sha256'],
        'source_template_count':len(records['templates']),'actors':actors,'skins':skins,
        'scope':'Source initial active records and art; no inactive/deferred wave activation or original AI/world/HP/settlement execution.',
        'trial_policy':{'seed':20261014,'move_interval':12,'enemy_scheduling':'declared_nearest_player_bfs',
            'range_metric':'declared_four_neighbour_manhattan','HP_application':'declared_scalar_damage_only',
            'death_presentation':'declared_fade_and_removal','victory_or_reward_authority':False}},images


def export(destination=OUTPUT):
    catalog,images = source_inputs()
    for filename,image in images.items():
        target=destination/filename;target.parent.mkdir(parents=True,exist_ok=True);image.save(target)
    for skin in catalog['skins'].values():
        for frame in skin['frames'].values():
            frame['file_sha256']=digest((destination/frame['file']).read_bytes())
            frame['file']='res://assets/school_combat/'+frame['file']
    (destination/'catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8',newline='\n')
    return catalog


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--out',type=Path,default=OUTPUT)
    args=parser.parse_args();catalog=export(args.out)
    print('Source initial actors=%d; enemy actors=%d; directional skins=%d; frames=%d' % (
        len(catalog['actors']),sum(a['category']==5 for a in catalog['actors']),len(catalog['skins']),sum(len(s['frames']) for s in catalog['skins'].values())))
