# -*- coding: utf-8 -*-
"""偏移表档案容器条目枚举器
容器: [u32 总长][u32 条目数 N][u32 偏移×(N+1)]  (formats.md §2)
对每个条目: 尺寸 + 内容指纹 (BMP/DX图像/裸像素/文本/其他)
"""
import struct, sys, os, glob, json

def classify(data, off, end):
    """返回 (类别, 说明)"""
    b = data[off:off+64]
    if end - off < 8:
        return ('tiny', f'{end-off}B')
    if b[:2] == b'BM':
        w, h = struct.unpack_from('<ii', data, off+18)
        bpp, = struct.unpack_from('<H', data, off+28)
        return ('BMP', f'{w}x{h}x{bpp}')
    if b[:4] == b'DX\x02\x00' or b[8:12] == b'DX\x02\x00':
        total, n = struct.unpack_from('<II', data, off)
        # DX 图像: 0x0C 起 "DX"02 00 + 参数
        p = off + (0xC if b[8:12] == b'DX\x02\x00' else 0)
        pa, pb = struct.unpack_from('<II', data, p+4)
        pixsz = end - off - 0x18
        return ('DXIMG', f'n={n} parm={pa:08x}/{pb:08x} pix={pixsz}')
    if b[:16].startswith(b'MapEditFlIDCode'):
        return ('MAPEDIT', '编辑器数据')
    # 嵌套容器?
    t, n = struct.unpack_from('<II', data, off)
    if t == end - off and 0 < n < 0x10000:
        off2, = struct.unpack_from('<I', data, off+8)
        if off2 == 8 + 4*(n+1):
            return ('CONTAINER', f'nested n={n}')
    # u16 像素流? 统计 bit15
    n16 = min(1024, (end-off)//2)
    if n16 > 100:
        px = struct.unpack_from(f'<{n16}H', data, off)
        a = sum(1 for p in px if p & 0x8000) / n16
        if a > 0.9:
            return ('RAW555?', f'bit15={a:.0%}')
    # 文本?
    printable = sum(1 for c in b if 32 <= c < 127 or c in (0, 0x0a, 0x0d)) / len(b)
    if printable > 0.85:
        return ('TEXT', b[:24].decode('ascii', 'replace').strip() or 'ascii')
    return ('?', b[:12].hex())

def enum_container(path):
    data = open(path, 'rb').read()
    total, n = struct.unpack_from('<II', data, 0)
    out = {'file': os.path.basename(path), 'size': len(data),
           'hdr_total': total, 'n': n, 'ok': False, 'entries': []}
    if total != len(data) or not 0 < n < 0x10000 or 8 + 4*n + 8 > len(data):
        return out
    offs = list(struct.unpack_from(f'<{n}I', data, 8))
    if offs[0] != 8 + 4*n:          # 首条目紧跟偏移表
        return out
    if any(offs[i] >= offs[i+1] for i in range(n-1)) or offs[-1] >= total:
        return out
    bounds = offs + [total]
    out['ok'] = True
    for i in range(n):
        kind, desc = classify(data, bounds[i], bounds[i+1])
        out['entries'].append({'i': i, 'off': bounds[i], 'size': bounds[i+1] - bounds[i],
                               'kind': kind, 'desc': desc})
    return out

if __name__ == '__main__':
    roots = sys.argv[1:] or ['CROSS HERMIT/CROSS HERMIT/DATA']
    results = []
    for root in roots:
        for f in sorted(glob.glob(root + '/**/*.BIN', recursive=True)) + \
                    sorted(glob.glob(root + '/MENU*')) + sorted(glob.glob(root + '/OP*')):
            sz = os.path.getsize(f)
            if sz < 16:
                continue
            r = enum_container(f)
            if r['ok']:
                results.append(r)
    from collections import Counter
    kinds = Counter(e['kind'] for r in results for e in r['entries'])
    print(f'containers parsed OK: {len(results)}')
    print('entry kinds:', dict(kinds))
    json.dump(results, open('analysis/container_enum.json', 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    for r in results[:20]:
        kc = Counter(e['kind'] for e in r['entries'])
        print(f"  {r['file']}: n={r['n']} {dict(kc)}")
