# -*- coding: utf-8 -*-
"""在脱壳镜像中定位字符串 VA 并列出引用它的反编译函数"""
import sys, os, re, glob

EXE = 'analysis/hermit_game.exe'
BS = chr(92)  # backslash

def find_all(d, s):
    out, o = [], d.find(s)
    while o >= 0:
        out.append(o + 0x400000)
        o = d.find(s, o + 1)
    return out

if __name__ == '__main__':
    d = open(EXE, 'rb').read()
    targets = sys.argv[1:]
    va_list = []
    for t in targets:
        s = t.replace('<BS>', BS).encode('latin1')
        vas = find_all(d, s)
        for v in vas:
            print(f'{v:#x}  {t}')
            va_list.append(v)
    if not va_list:
        sys.exit(0)
    # 在反编译语料中找引用 (DAT_00xxxxxx / 0xxxxxxx 形式)
    print('--- 引用函数 ---')
    hits = {}
    for f in glob.glob('analysis/decomp_all/*.c'):
        txt = open(f, encoding='utf-8', errors='replace').read()
        for v in va_list:
            h = f'{v:x}'
            if h in txt:
                hits.setdefault(v, []).append(os.path.basename(f)[:-2])
    for v, fs in hits.items():
        print(f'{v:#x}: {" ".join(fs[:12])}')
