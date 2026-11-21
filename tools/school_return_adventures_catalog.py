"""Source tables for the current 5/1 school continuation; no new runtime backend."""
import hashlib
import json
import struct

from tools.school_boot_fixture import source_rules
from tools.tactics_exit_emulation import ROOT, SOURCE, SOURCE_SHA256


def catalog(scene_ids=(8,17)):
    image=SOURCE.read_bytes()
    assert hashlib.sha256(image).hexdigest()==SOURCE_SHA256
    rows=source_rules()['adventures']
    for row in rows:
        at=0x73bed0+row['id']*256-0x400000
        raw=image[at:at+256]
        row['cooldown']=raw[4]
        row['rounds']=[dict(zip(('scene_id','selection_word'),struct.unpack_from('<HH',raw,16+k*4))) for k in range(raw[15])]
        row['sha256']=hashlib.sha256(raw).hexdigest()
    scenes={}
    for sid in scene_ids:
        config=image[0x6ad1d0+sid*42-0x400000:0x6ad1d0+(sid+1)*42-0x400000]
        resources=[]
        for k in range(4):
            p=struct.unpack_from('<I',image,0x6b13f0+sid*16+k*4-0x400000)[0]-0x400000
            name=image[p:image.index(0,p)].decode('ascii')
            path=ROOT/'CROSS HERMIT/CROSS HERMIT/DATA/TACTICS/MAP'/name.upper()
            raw=path.read_bytes()
            resources.append({'filename':name,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)})
        script=ROOT/f'CROSS HERMIT/CROSS HERMIT/DATA/TACTICS/SCRIPT/T{sid:04}.BIN'
        scenes[str(sid)]={'configuration_hex':config.hex(),'configuration_sha256':hashlib.sha256(config).hexdigest(),
            'map_resources':resources,'script':script.name,'script_sha256':hashlib.sha256(script.read_bytes()).hexdigest(),
            'template_count':struct.unpack_from('<h',image,0x6a85ac+sid*2-0x400000)[0]}
    return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'adventures':rows,'scenes':scenes,
        'functions':{'open':'0x4a17b0','prepend':'0x4a9d90','submit':'0x4a1920','remove':'0x4aa0e0','list':'0x4a1c70','prepare':'0x4a6a10'},
        'scope':'Complete catalog for the owned first-game 4/4 course -> 4/5 adventure5 -> 5/1 return. No imported arbitrary history or playable scene8/17 authority.'}


def mandatory_adventure(task_id):
    assert task_id in (4, 6, 7, 9, 10, 13, 14, 18)
    image = SOURCE.read_bytes()
    assert hashlib.sha256(image).hexdigest() == SOURCE_SHA256
    def values(address, count, fmt='h'):
        return list(struct.unpack_from('<'+fmt*count, image, address+task_id*256-0x400000))
    rewards = {'task_id': task_id, 'base_points': values(0x73BEF4,5,'i'),
               'unit_bonus': values(0x73BF08,1)[0], 'time_bonuses': values(0x73BF0A,3),
               'count_bonuses': values(0x73BF10,6),
               'loot_quotas': [values(0x73BF1A+14*i,7) for i in range(5)],
               'fixed_items': values(0x73BF60,8),
               'objective_rewards': [values(0x73BF70+6*i,3) for i in range(16)]}
    return {'source_image_sha256': SOURCE_SHA256, 'scene':catalog((task_id,))['scenes'][str(task_id)], 'rewards':rewards}


def mandatory_seven():
    return mandatory_adventure(7)


if __name__=='__main__':
    out=ROOT/'prototype/data/school_return_adventures.json'
    out.write_text(json.dumps(catalog(),ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
    print(out.name,out.stat().st_size,hashlib.sha256(out.read_bytes()).hexdigest())
