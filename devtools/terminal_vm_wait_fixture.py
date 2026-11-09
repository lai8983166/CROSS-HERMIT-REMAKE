"""Self-owned x86 wait/FX fixture for an external VMM state preflight only."""
import argparse,hashlib,json,struct
from pathlib import Path
from devtools.terminal_wait_return_callback import Asm


def image():
    a=Asm();a.b('55 8b ec 53 56 57')
    a.b('0f ae 05');a.imm('data',0) # retain caller FX state
    a.b('db e3 d9 e8 d9 eb') # known x87 1 and pi, self-owned only
    for i in range(8):
        a.b('f3 0f 6f '+format(5+i*8,'02x'));a.imm('data',0,0x400+16*i)
    a.b('bb 22 22 11 11 be 44 44 33 33 bf 66 66 55 55')
    a.b('ff 75 0c 6a 00 ff 75 08 b8');a.imm('nt_wait',0);a.b('ff d0')
    post=len(a.code)
    a.b('9c 60 a1');a.imm('data',0,0x200)
    a.b('69 c0 00 04 00 00 05');a.imm('data',0,0x1000)
    a.b('89 c2 0f ae 02 89 e6 8d ba 00 02 00 00 b9 09 00 00 00 fc f3 a5')
    a.b('ff 05');a.imm('data',0,0x200)
    a.b('61 9d 0f ae 0d');a.imm('data',0)
    a.b('5f 5e 5b 5d c2 08 00')
    offsets=[]
    for i in range(2):
        offsets.append(len(a.code));a.label('counter'+str(i))
        a.b('ff 05');a.imm('data',0,0x300+4*i)
        a.b('83 3d');a.imm('data',0,0x308);a.b('00')
        a.branch('0f 84','counter'+str(i));a.b('c3')
    return a.finish(),dict(patches=a.patches,postcall_offset=post,counter_offsets=offsets,
        data_bytes=16384,post_record_start=0x1000,post_record_stride=0x400,post_frame_offset=0x200,
        scope='owned test helper only; no original game execution or instrumentation')


def prepare(path):
    if path.exists():raise ValueError('new fixture directory')
    raw,meta=image();source=Path(__file__).with_suffix('.cs').read_bytes()
    import capstone
    ins=list(capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_32).disasm(raw,0))
    if sum(i.size for i in ins)!=len(raw):raise ValueError('complete bounded instruction decode')
    meta.update(source_sha256=hashlib.sha256(source).hexdigest(),template_sha256=hashlib.sha256(raw).hexdigest(),
                instructions=[dict(offset=i.address,hex=i.bytes.hex(),instruction=i.mnemonic+' '+i.op_str)for i in ins])
    path.mkdir()
    for name,data in [('fixture.bin',raw),('manifest.json',json.dumps(meta,indent=2).encode()),('terminal_vm_wait_fixture.cs',source)]:
        with(path/name).open('xb')as f:f.write(data)
    return meta


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();m=prepare(a.out)
    print(json.dumps(dict(code_bytes=len(image()[0]),template_sha256=m['template_sha256'])))
