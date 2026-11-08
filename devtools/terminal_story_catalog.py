"""Identify live ADV code against retained immutable assets without copying code."""
import hashlib
import gzip
import json
from pathlib import Path
import struct

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'CROSS HERMIT/CROSS HERMIT/DATA/ADV/DAT'
GAME_ROOT=ROOT/'CROSS HERMIT/CROSS HERMIT'
PARENT=ROOT/'analysis/terminal-scene-preflight-v3-20261107.json.gz'
PARENT_SHA='3a028556e6e0141746df00573766332ee91ec34bb7a6c19ba4e182724ff4d7ff'


def code_block(data):
    if not 8<=len(data)<=1024*1024:raise ValueError('bounded original ADV container')
    count=struct.unpack_from('<I',data)[0]
    if not 2<=count<=8:raise ValueError('original ADV block count')
    offsets=struct.unpack_from('<%dI'%count,data,4)
    if not (4+4*count<=offsets[0]<offsets[1]<=len(data)):raise ValueError('original ADV code bounds')
    return offsets[0],data[offsets[0]:offsets[1]]


def tactics_blocks(data):
    def u32(at):
        if not 0<=at<=len(data)-4:raise ValueError('bounded tactics header')
        return struct.unpack_from('<I',data,at)[0]
    count=u32(4)
    if not 1<=count<=64:raise ValueError('bounded tactics block count')
    for block in range(count):
        start=u32(8+4*block);records=u32(start+4)
        if not 1<=records<=1024:raise ValueError('bounded tactics subrecord count')
        for record in range(records):
            delta=u32(start+8+4*record)
            if not delta:continue
            sub=start+delta
            if u32(sub)!=4:continue
            first=sub+u32(sub+4);end=sub+u32(sub+8)
            if not sub+20<=first<end<=len(data):raise ValueError('bounded tactics code block')
            yield first,data[first:end],block,record


class Catalog:
    def __init__(self):
        self.entries={}
        packed=PARENT.read_bytes()
        if hashlib.sha256(packed).hexdigest()!=PARENT_SHA:raise ValueError('fixed asset inventory identity')
        inventory={r['path'].upper():r for r in json.loads(gzip.decompress(packed))['runtime']['immutable_files']}
        def add(path,data,offset,code,**extra):
            digest=hashlib.sha256(code).hexdigest();asset_sha=hashlib.sha256(data).hexdigest()
            relative=path.relative_to(GAME_ROOT).as_posix();expected=inventory[relative.upper()]
            if (len(data),asset_sha)!=(expected['bytes'],expected['sha256']):raise ValueError('original catalog asset identity')
            row=dict(path=path.relative_to(ROOT).as_posix(),bytes=len(data),sha256=asset_sha,
                     code_offset=offset,code_bytes=len(code),code_sha256=digest,**extra)
            self.entries.setdefault((len(code),digest),[]).append(row)
        for path in sorted(ASSETS.glob('*.YBC')):
            data=path.read_bytes();offset,code=code_block(data)
            add(path,data,offset,code)
        path=GAME_ROOT/'DATA/TACTICS/SCRIPT/T0001.BIN';data=path.read_bytes()
        for offset,code,block,record in tactics_blocks(data):add(path,data,offset,code,block=block,record=record)
        if not self.entries:raise ValueError('nonempty original ADV catalog')

    def observe(self,get,vm):
        start,end=struct.unpack_from('<II',vm,16)
        if not (0x10000<=start<end<0x80000000 and 4<=end-start<=1024*1024):
            return dict(matched=False,reason='program fields not yet bounded',pointer=start,end=end)
        code=get(start,end-start);digest=hashlib.sha256(code).hexdigest()
        assets=self.entries.get((len(code),digest),[])
        return dict(matched=bool(assets),pointer=start,bytes=len(code),sha256=digest,
                    assets=assets,live_bytes_compared_via_sha256=True,raw_bytes_available_from_fixed_assets=True)
