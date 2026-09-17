# -*- coding: utf-8 -*-
"""CROSS HERMIT TACTICS SCRIPT (T*.BIN) 反汇编器
YBC32 VM 字节码 (dispatcher 0x4CE8F0):
  文件  {u32 len; u32 nblocks; u32 block_off[nblocks]}
  块    {u32 size; u32 rcnt(=101); u32 sub_off[rcnt]}     子记录位于 块+off
  子记录 {u32 type=4; u32 code_off; u32 data_off[3]}      代码=子+code_off, 数据=子+data_off[0]
  代码  [u16 op][u16 adv][payload(adv-4)]  ... 直到 op19 (CODE_END)
  操作数 cell = u32 type<<28|value  (t0=变量引用, t2=立即数)
  跳转目标 = u32 相对代码基
  文本池 @data_off: {u32 count; u16 off0...} + NUL 结尾 Big5 字符串
op 名 = 编译器名表 VA 0x624850 (索引 == 操作码)
"""
import struct, sys, os, re, json

EXE = 'analysis/hermit_game.exe'
SCDIR = r'CROSS HERMIT/CROSS HERMIT/DATA/TACTICS/SCRIPT'

OPMAP = {int(k): tuple(v) for k, v in json.load(open('analysis/ybc32_opmap.json')).items()}

TEXT_ENC = 'big5'   # 文本池编码; 日文原版 (无 BIG5 副本的文件) 为 shift_jis

def load_names():
    data = open(EXE, 'rb').read()
    names = {}
    for i in range(150):
        v = struct.unpack_from('<I', data, 0x224850 + i*4)[0]
        if 0x400000 <= v < 0x600000:
            end = data.index(b'\0', v - 0x400000)
            raw = data[v-0x400000:end].decode('ascii', 'replace')
            m = re.search(r'CODE_(\w+)', raw)
            if m: names[i] = m.group(1)
    return names

NAMES = load_names()

# op 150+ 无名表 —— 由处理器反编译定名 (ComYken.cpp 单元工作区族 / VM 寄存器 / 子脚本)
NAMES.update({
    158: 'UNITWK_GET32', 159: 'UNITWK_GET16', 160: 'UNITWK_GET8', 161: 'UNITWK_GETBIT',
    162: 'UNITWK_PUT32', 163: 'UNITWK_PUT16', 164: 'UNITWK_PUT8', 165: 'UNITWK_PUTBIT',
    166: 'REG_PUT', 167: 'REG_GET', 172: 'SCRIPT_LOAD',
})

def opname(op):
    if op in NAMES: return NAMES[op].replace('CODE_', '')
    if op in OPMAP: return f'OP_{op}'
    return f'OP_{op}_?'

def cellstr(c):
    t, v = c >> 28, c & 0x0FFFFFFF
    if t == 2:  return f'{v}'                      # 立即数
    if t == 0:  return f'v{v:#x}'                  # 变量引用
    return f't{t}:{v:#x}'

def decode_text(bs):
    try: return bs.decode(TEXT_ENC)
    except UnicodeDecodeError: return bs.decode(TEXT_ENC, 'replace')

def parse(data):
    """返回 [ (block_idx, sub_idx, code_abs, pool_abs|None) ]"""
    out = []
    ln, nb = struct.unpack_from('<II', data, 0)
    boffs = [struct.unpack_from('<I', data, 8 + 4*i)[0] for i in range(nb)]
    for bi, boff in enumerate(boffs):
        if boff + 8 > len(data): continue
        bsize, rcnt = struct.unpack_from('<II', data, boff)
        for si in range(rcnt):
            p = boff + 8 + 4*si
            if p + 4 > len(data): break
            soff = struct.unpack_from('<I', data, p)[0]
            sub = boff + soff
            if soff == 0 or sub + 8 > len(data): continue
            tag, = struct.unpack_from('<I', data, sub)
            if tag == 0x00666D64 or tag != 4: continue     # dmf 填充 / 非代码记录
            code_off, = struct.unpack_from('<I', data, sub + 4)
            data_off, = struct.unpack_from('<I', data, sub + 8)
            code = sub + code_off
            pool = sub + data_off if data_off and sub + data_off < len(data) else None
            # 校验数据池头
            if pool is not None:
                n, = struct.unpack_from('<I', data, pool)
                if n > 4096: pool = None
            out.append((bi, si, code, pool))
    return out

def load_pool(data, pool):
    """返回 [(off, param, 字符串)] —— entry = u16 off + u16 param(疑语音ID)"""
    if pool is None or pool + 4 > len(data): return []   # offs[2]==len 时无 block2
    n, = struct.unpack_from('<I', data, pool)
    if n == 0 or n > 4096: return []
    out = []
    for i in range(n):
        off, prm = struct.unpack_from('<HH', data, pool + 4 + 4*i)
        if off < 4 + 4*n or pool + off >= len(data): return []
        e = data.find(b'\0', pool + off)
        out.append((off, prm, decode_text(data[pool+off:e]) if e > 0 else ''))
    return out

JUMPS = {8: 'if', 11: 'goto', 52: 'mousegoto', 53: 'mousegoto_tbl', 54: 'mousegoto_end'}

def disasm_code(data, code_base, pool, out):
    strs = load_pool(data, pool)
    pc = code_base
    labels = set()
    insns = []
    while pc + 4 <= len(data):
        op, adv = struct.unpack_from('<HH', data, pc)
        insns.append((pc, op, adv))
        if op == 19: break
        if adv < 4 or pc + adv > len(data): break
        pc += adv
    # 第一遍: 收集跳转目标作为标号
    for pc, op, adv in insns:
        if op == 11 and adv >= 8:
            labels.add(code_base + struct.unpack_from('<I', data, pc+4)[0])
        elif op == 8 and adv >= 0x14:
            labels.add(code_base + struct.unpack_from('<I', data, pc+0x10)[0])
    for pc, op, adv in insns:
        rel = pc - code_base
        lbl = f'L_{rel:04x}' if pc in labels else '        '
        nm = opname(op)
        payload = data[pc+4:pc+adv]
        arg = ''
        if op == 19:  arg = '; END'
        elif op == 17 and adv >= 6:                    # TEXT
            tid, = struct.unpack_from('<H', data, pc+4)
            s = strs[tid][2] if tid < len(strs) else '?'
            arg = f'#{tid} "{s}"'
        elif op == 11 and adv >= 8:                    # GOTO
            tgt, = struct.unpack_from('<I', data, pc+4)
            arg = f'L_{tgt:04x}'
        elif op == 8 and adv >= 0x14:                  # IFGOTO
            cond = data[pc+4]
            c1, c2 = struct.unpack_from('<II', data, pc+8)
            tgt, = struct.unpack_from('<I', data, pc+0x10)
            arg = f'cond={cond} {cellstr(c1)} cmp {cellstr(c2)} -> L_{tgt:04x}'
        elif 158 <= op <= 165 and adv >= 16:           # UNITWK 族
            c0, c1, c2 = struct.unpack_from('<III', data, pc+4)
            w = ('u32', 'u16', 'u8', 'bit')[(op - 158 - 4*(op >= 162)) % 4]
            u, o = cellstr(c1), cellstr(c2)
            if op < 162: arg = f'{cellstr(c0)} <- UNITWK[{u}].{o} ({w})'
            else:        arg = f'{cellstr(c0)} -> UNITWK[{u}].{o} ({w})'
        elif op in (166, 167) and adv >= 8:
            arg = cellstr(struct.unpack_from('<I', data, pc+4)[0])
        elif adv == 4: pass
        else:
            cells = [struct.unpack_from('<I', data, pc+4+4*i)[0]
                     for i in range((adv-4)//4)]
            arg = ' '.join(cellstr(c) for c in cells)
            if (adv-4) % 4: arg += ' +' + data[pc+4+4*((adv-4)//4):pc+adv].hex()
        out.append(f'{pc:06x}: {lbl} {op:5d} {nm:<24} adv={adv:<3} {arg}')
    return len(insns)

def disasm_file(path):
    data = open(path, 'rb').read()
    lines = [f'; {os.path.basename(path)}  len={len(data):#x}']
    texts = []
    for bi, si, code, pool in parse(data):
        strs = load_pool(data, pool)
        lines.append(f'; ── block{bi} sub{si} code@{code:#x} pool@{pool:#x} ({len(strs)} strings)')
        for i, (off, prm, s) in enumerate(strs):
            lines.append(f';   #{i} off={off:#x} prm={prm:#x} "{s}"')
            texts.append(s)
        n = disasm_code(data, code, pool, lines)
        lines.append(f';   ({n} insns)')
    return '\n'.join(lines), texts


def disasm_ybc_file(path):
    """ADV 事件脚本 (.YBC): {u32 n; u32 off[n]} 容器 (同 4cd700)
    block0 = YBC32 代码 (同一 VM 4CE8F0), block1 = 0x30 定长记录 (路径/资源引用),
    block2 = TEXT 文本池 (4c4b80 经 4c2120 读 VM+0x18=block2 基址)"""
    data = open(path, 'rb').read()
    lines = [f'; {os.path.basename(path)}  len={len(data):#x}  [ADV YBC]']
    texts = []
    n, = struct.unpack_from('<I', data, 0)
    if not 1 <= n <= 8:
        return f'; {os.path.basename(path)}: nblocks={n} 非法, 跳过', texts
    offs = struct.unpack_from(f'<{n}I', data, 4)
    lines.append(f'; nblocks={n} offs={[hex(o) for o in offs]}')
    code, rec1, pool = offs[0], (offs[1] if n > 1 else 0), (offs[2] if n > 2 else 0)
    # block1: 0x30 定长记录 → 尽量按路径串显示
    if n > 1:
        end = offs[2] if n > 2 else len(data)
        if end > rec1:
            for k in range((end - rec1) // 0x30):
                r = data[rec1 + k*0x30: rec1 + (k+1)*0x30]
                e = r.find(b'\0')
                s = r[:e if e >= 0 else 0x30]
                if s:
                    try: t = s.decode(TEXT_ENC)
                    except UnicodeDecodeError: t = s.decode('latin1')
                    lines.append(f'; rec1[{k}] = "{t}"')
    strs = load_pool(data, pool) if pool else []
    for i, (off, prm, s) in enumerate(strs):
        lines.append(f';   txt#{i} off={off:#x} prm={prm:#x} "{s}"')
        texts.append(s)
    cnt = disasm_code(data, code, pool, lines)
    lines.append(f'; ({cnt} insns)')
    return '\n'.join(lines), texts

def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('paths', nargs='*', help='T*.BIN 或 .YBC 文件/目录')
    ap.add_argument('-o', '--outdir', default='analysis/script_disasm')
    ap.add_argument('-e', '--encoding', default='big5',
                    help='文本池编码 (日文原版用 shift_jis)')
    args = ap.parse_args()
    global TEXT_ENC
    TEXT_ENC = args.encoding
    os.makedirs(args.outdir, exist_ok=True)
    import glob as _g
    files = []
    for p in args.paths:
        files += sorted(_g.glob(p)) if any(c in p for c in '*?') else [p]
    if not files:
        files = sorted(_g.glob(os.path.join(SCDIR, 'T*.BIN')))
    alltext = {}
    bad = 0
    for f in files:
        isybc = f.lower().endswith('.ybc')
        try:
            txt, texts = (disasm_ybc_file if isybc else disasm_file)(f)
        except Exception as e:
            print(f'{os.path.basename(f)}: FAIL {e}'); bad += 1; continue
        open(os.path.join(args.outdir, os.path.basename(f) + '.txt'), 'w', encoding='utf-8').write(txt)
        alltext[os.path.basename(f)] = texts
    suffix = '_texts.json'
    json.dump(alltext, open(os.path.join(args.outdir, suffix), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    print(f'done {len(files)-bad}/{len(files)} -> {args.outdir}')

if __name__ == '__main__':
    main()
