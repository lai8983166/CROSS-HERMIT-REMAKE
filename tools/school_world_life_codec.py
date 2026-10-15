"""Lossless full-hex report encoding; bounded, exact single-stream decoding."""
import zlib

MARKER='$full_hex_zlib'
LIMIT=1024*1024


def pack(value,key=None):
    if isinstance(value,dict):return {k:pack(v,k) for k,v in value.items()}
    if isinstance(value,list):return [pack(v) for v in value]
    if key=='hex' and isinstance(value,str) and len(value)>=1024:
        raw=bytes.fromhex(value)
        if len(raw)>LIMIT:raise ValueError('life region larger than declared encoding bound')
        return {MARKER:zlib.compress(raw,6).hex(),'bytes':len(raw)}
    return value


def unpack(value):
    if isinstance(value,dict):
        if MARKER in value:
            if set(value)!={MARKER,'bytes'} or type(value['bytes']) is not int or not 0<=value['bytes']<=LIMIT:raise ValueError('life exact encoded region schema/size')
            encoded=value[MARKER]
            if not isinstance(encoded,str) or len(encoded)>LIMIT*2:raise ValueError('life encoded region bound/type')
            try:
                obj=zlib.decompressobj();raw=obj.decompress(bytes.fromhex(encoded),value['bytes']+1)
            except (ValueError,zlib.error) as exc:raise ValueError('life invalid compressed region') from exc
            if len(raw)!=value['bytes'] or not obj.eof or obj.unused_data or obj.unconsumed_tail:raise ValueError('life complete exact compressed region stream')
            return raw.hex()
        return {k:unpack(v) for k,v in value.items()}
    if isinstance(value,list):return [unpack(v) for v in value]
    return value
