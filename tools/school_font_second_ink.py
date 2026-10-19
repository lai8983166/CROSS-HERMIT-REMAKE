"""Inspect actual ABC overhang without changing original advance-width UVs."""
import struct

REFERENCE='https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-getcharabcwidthsa'


def ink_rectangles(rows,inspection):
    raw=bytes.fromhex(inspection['hex'])
    if len(rows)!=95 or len(raw)!=1140 or inspection!=dict(native_requested=False,method='GetCharABCWidthsA',first=32,last=126,result=1,hex=raw.hex()):
        raise ValueError('second ink exact inspection-only95 ABC records')
    bounds=[]
    for n,row in enumerate(rows):
        a,b,c=struct.unpack_from('<iIi',raw,n*12)
        if not -256<=a<=256 or not 0<=b<=256 or not -256<=c<=256 or a+b+c!=row['width']:
            raise ValueError('second ink ABC advance must match original measured width')
        left=min(row['x'],row['x']+a);right=max(row['x']+row['width'],row['x']+a+b)
        if not 0<=left<=right<=256 or not 0<=row['y']<=row['y']+row['height']<=256:
            raise ValueError('second ink actual bounded glyph cell and horizontal ink')
        bounds.append(dict(character=row['character'],left=left,right=right,top=row['y'],bottom=row['y']+row['height'],A=a,B=b,C=c))
    return bounds
