"""Finite single-attack world cycles against a declared non-active living target."""
from copy import deepcopy
from tools.battle_world_update import corpus as world_corpus
from tools.battle_combat_aftermath import validate as validate_aftermath
from tools.battle_pathfinding_emulation import need,sha


def corpus():
    return [dict(name=c['name'],aftermath=deepcopy(c['aftermath']),budget=192) for c in world_corpus() if c['world_enabled']]


def validate(c):
    need(set(c)=={'name','aftermath','budget'},'exact world combat input')
    validate_aftermath(c['aftermath']);need(isinstance(c['name'],str) and c['name'] and type(c['budget']) is int and 1<=c['budget']<=192,'bounded world combat budget')


def pages(value,blobs=None):
    """Lossless 4096-byte page references; the independent oracle uses no sink."""
    if isinstance(value,dict):return {k:pages(v,blobs) for k,v in value.items()}
    if isinstance(value,list):return [pages(v,blobs) for v in value]
    if isinstance(value,str) and len(value)>=4096:
        raw=bytes.fromhex(value);ids=[]
        for start in range(0,len(raw),4096):
            b=raw[start:start+4096];key=sha(b);ids.append(key)
            if blobs is not None:blobs[key]=b.hex()
        return dict(bytes=len(raw),pages=ids)
    return value


def expand(value,blobs):
    if isinstance(value,dict):
        if set(value)=={'bytes','pages'}:
            need(type(value['bytes']) is int and value['bytes']>=2048 and isinstance(value['pages'],list),'page reference shape')
            chunks=[]
            for i,key in enumerate(value['pages']):
                need(key in blobs,'every referenced page retained');b=bytes.fromhex(blobs[key]);need(sha(b)==key,'original page identity')
                need(len(b)==min(4096,value['bytes']-i*4096) and len(b)>0,'exact ordered page size');chunks.append(b)
            raw=b''.join(chunks);need(len(raw)==value['bytes'],'entire paged field retained');return raw.hex()
        return {k:expand(v,blobs) for k,v in value.items()}
    if isinstance(value,list):return [expand(v,blobs) for v in value]
    return value


def validate_pages(value,blobs):
    if isinstance(value,dict):
        if set(value)=={'bytes','pages'}:
            n=value['bytes'];ids=value['pages'];need(type(n) is int and n>=2048 and isinstance(ids,list) and len(ids)==(n+4095)//4096,'full paged byte extent')
            for i,key in enumerate(ids):need(key in blobs and len(blobs[key])==2*min(4096,n-i*4096),'every exact ordered page retained')
        else:
            for k,v in value.items():
                if k!='blobs':validate_pages(v,blobs)
    elif isinstance(value,list):
        for v in value:validate_pages(v,blobs)


def settled(get,record_alive,hit_seen,stopped):
    return bool(hit_seen and stopped and get(0x11080AEC+0x290,'B')==5 and not get(0x11080AEC+0x292,'B') and
                get(0x1108100C+0x290,'B') in (5,11) and not get(0x1108100C+0x292,'B') and not get(0x1108100C+0x2A6,'B') and
                not get(0x1108100C+0xA0+0x20,'I') and record_alive in (1,3,4))
