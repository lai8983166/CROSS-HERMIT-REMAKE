"""Bounded local Unicorn register-semantics oracle; no VM, process or guest I/O.

Freeze this file and the DLL identities before execution. Every instruction
case uses Unicorn's count and time limits; output is evidence, not acceptance.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


def identity(path):
    path = Path(path).resolve()
    raw = path.read_bytes()
    return dict(path=str(path), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


def run():
    import unicorn
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_32, UC_HOOK_INTR
    from unicorn import x86_const as x

    def fresh():
        u = Uc(UC_ARCH_X86, UC_MODE_32)
        u.mem_map(0x1000, 0x3000)
        return u

    def read(u, name):
        value = u.reg_read(getattr(x, 'UC_X86_REG_' + name))
        return list(value) if isinstance(value, tuple) else value

    def write(u, name, value):
        u.reg_write(getattr(x, 'UC_X86_REG_' + name), value)

    def execute(u, code):
        events = []
        def interrupt(engine, number, user):
            events.append(dict(number=number, eip=read(engine, 'EIP')))
            engine.emu_stop()
        hook = u.hook_add(UC_HOOK_INTR, interrupt)
        u.mem_write(0x1000, code)
        error = None
        try:
            u.emu_start(0x1000, 0x1000 + len(code), timeout=100000, count=32)
        except unicorn.UcError as exc:
            error = dict(errno=exc.errno, text=str(exc))
        finally:
            u.hook_del(hook)
        return dict(code=code.hex(), events=events, error=error,
                    eax=read(u, 'EAX'), eip=read(u, 'EIP'))

    out = dict(schema='unicorn-canonical57-semantics-v1', accepted=False,
               version=unicorn.__version__, binding=identity(unicorn.__file__),
               oracle=identity(__file__), cases={})
    package = Path(unicorn.__file__).parent
    out['native_libraries'] = [identity(p) for p in (package/'lib').glob('*') if p.suffix in ('.dll', '.so')]
    u = fresh()
    names = 'FPCW FPSW FPTAG FIP FDP FCS FDS FOP MXCSR GDTR IDTR LDTR TR DR0 DR1 DR2 DR3 DR4 DR5 DR6 DR7'.split()
    out['cases']['defaults'] = {name: read(u, name) for name in names}
    fp = [(0x8000000000000000, 0x3fff), (0, 0), (0, 0x8000),
          (1, 0), (0x8000000000000000, 0x7fff),
          (0xc000000000000000, 0x7fff), (1, 0x3fff),
          (0x8000000000000000, 0)]
    for i, value in enumerate(fp):
        write(u, 'FP'+str(i), value)
    write(u, 'FPTAG', 0)
    tops = []
    for top in (0, 3, 7):
        write(u, 'FPSW', top << 11)
        tops.append(dict(top=top, fp=[read(u, 'FP'+str(i)) for i in range(8)],
                         fptag=read(u, 'FPTAG'), fpsw=read(u, 'FPSW')))
    out['cases']['physical_fp_top'] = dict(input=fp, observations=tops)
    tags = []
    for tag in (0, 0x5555, 0xaaaa, 0xffff, 0x300c):
        write(u, 'FPTAG', tag)
        tags.append(dict(written=tag, read=read(u, 'FPTAG'), fp=[read(u, 'FP'+str(i)) for i in range(8)]))
    out['cases']['tag_write_classification'] = tags
    # FX image is logical ST order; physical UC_FP slots must remain fixed.
    write(u, 'FPTAG', 0x300c)
    write(u, 'FPSW', 3 << 11)
    result = execute(u, bytes.fromhex('0fae0500200000'))
    result['image_hex'] = bytes(u.mem_read(0x2000, 512)).hex()
    result['physical_after'] = [read(u, 'FP'+str(i)) for i in range(8)]
    out['cases']['fxsave_top3'] = result
    # Plain register API exposes dr[4/5] padding, unlike MOV DR instructions.
    debug = []
    for de in (False, True):
        u = fresh()
        write(u, 'CR4', (read(u, 'CR4') & ~8) | (8 if de else 0))
        for name,value in [('DR4',0x12345678),('DR5',0x23456789),('DR6',0x3456789a),('DR7',0x400)]:
            write(u, name, value)
        initial = {name:read(u,name) for name in ('CR4','DR4','DR5','DR6','DR7')}
        for op in ('0f21e0','0f21e8'):
            debug.append(dict(de=de, initial=initial, execution=execute(u, bytes.fromhex(op))))
    out['cases']['debug_alias_instruction'] = debug
    descriptors = []
    for name in ('GDTR','IDTR','LDTR','TR'):
        for base in (0x234567, 0x100234567):
            u = fresh()
            desired = (0x28, base, 0x12345, 0xc09300)
            error = None
            try:
                write(u,name,desired)
            except unicorn.UcError as exc:
                error = dict(errno=exc.errno,text=str(exc))
            descriptors.append(dict(name=name, written=desired, read=read(u,name), error=error))
    out['cases']['descriptors'] = descriptors
    widths=[]
    for name,value in [('EAX',0x112345678),('EIP',0x112345678),('FIP',0x112345678),
                       ('FDP',0x112345678),('FCS',0x11234),('FDS',0x12345),('FOP',0xffff),
                       ('DR0',0x112345678),('CR2',0x112345678)]:
        u=fresh();error=None
        try:write(u,name,value)
        except unicorn.UcError as exc:error=dict(errno=exc.errno,text=str(exc))
        widths.append(dict(name=name,written=value,read=read(u,name),error=error))
    out['cases']['widths'] = widths
    return out


if __name__ == '__main__':
    path = Path(sys.argv[1]).resolve()
    if path.exists() or path.drive.lower() != 'f:':
        raise ValueError('fresh F-drive output required')
    path.write_text(json.dumps(run(), indent=2)+'\n', encoding='utf-8')
    print(path)
