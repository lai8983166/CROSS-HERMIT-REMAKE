"""FNSTENV masking and FLDENV metadata restoration, owned protected-mode guest."""
import argparse
import ast
import struct
from pathlib import Path
from devtools.terminal_tcg_roundtrip_probe import run


def image(root):
    tree=ast.parse((root/'devtools/terminal_tcg_predecessor_probe_v3.py').read_text())
    fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='image')
    scope={'struct':struct}
    exec(compile(ast.Module(body=[fn],type_ignores=[]),'<pure-elf>','exec'),scope)
    elf=bytearray(scope['image']())
    def w(x):return struct.pack('<I',x)
    code=bytes.fromhex('66b810008ed88ec08ed0bc004010000f20c083e0f383c8220f22c0')
    code+=bytes.fromhex('dbe3d92d')+w(0x100908)+bytes.fromhex('d905')+w(0x100900)
    fip=0x100120+len(code)
    code+=bytes.fromhex('d805')+w(0x100904)
    code+=bytes.fromhex('d935')+w(0x102000) # save old masks, then mask all
    code+=bytes.fromhex('d93d')+w(0x102080) # observe changed CW
    code+=bytes.fromhex('dbe3d925')+w(0x102000) # reset, then load environment
    stop=0x100120+len(code)
    code+=bytes.fromhex('d935')+w(0x102020)
    for address,count in((0x102000,28),(0x102020,28),(0x102080,2)):
        code+=b'\xbe'+w(address)+b'\xb9'+w(count)+bytes.fromhex('ace6e9e2fb')
    code+=bytes.fromhex('dbe3b810000000e7f4f4ebfd')
    elf[4096+0x120:4096+0x120+len(code)]=code
    elf[4096+0x900:4096+0x90a]=struct.pack('<ffH',1.,2.,0x037e)
    return bytes(elf),dict(fip=fip,fdp=0x100904,fop=5,fcs=8,fds=16,stop=stop)


def validate(raw,e,states,result):
    if len(raw)!=58:raise ValueError('environment output size')
    before,after=raw[:28],raw[28:56]
    s=states[0]
    checks=dict(environment_roundtrip=before==after,
        old_mask_saved=struct.unpack_from('<H',before)[0]==0x037e,
        actual_mask_side_effect=struct.unpack_from('<H',raw,56)[0]==0x037f,
        unmasked_control_restored=s['fp_control']==0x037e,
        status_and_tag=struct.unpack_from('<H',after,4)[0]==s['fp_status']==0x3800 and struct.unpack_from('<H',after,8)[0]==0x3fff and s['fp_empty_mask']==0x7f,
        fip=struct.unpack_from('<I',after,12)[0]==int(s['fip'],16)==e['fip'],
        fdp=struct.unpack_from('<I',after,20)[0]==int(s['fdp'],16)==e['fdp'],
        fop=struct.unpack_from('<H',after,18)[0]==s['fop']==5,
        fcs=struct.unpack_from('<H',after,16)[0]==s['fcs']==8,
        fds=struct.unpack_from('<H',after,24)[0]==s['fds']==16,
        arithmetic=s['fp_physical_low64_high16'][7]==['c000000000000000','0000000000004000'],
        stop=int(s['eip'],16)==e['stop'],stable=states[0]==states[1],
        all_vps=s['cpu']==0 and sorted(s.get('vp_stopped',[]),key=lambda v:v['cpu'])==[dict(cpu=0,stopped=True),dict(cpu=1,stopped=True)],
        clean=result['exit_code']==33 and result['invalid_cpu_rejected']and not result['errors'])
    result['checks']=checks
    return all(checks.values())


if __name__=='__main__':
    p=argparse.ArgumentParser()
    for name in('binary','firmware','output'):p.add_argument('--'+name,type=Path,required=True)
    raise SystemExit(not run(p.parse_args(),image_builder=image,validator=validate))
