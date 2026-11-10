"""High-pointer FXSAVE64/FXRSTOR64 subset; reuses bounded process supervision."""
import argparse
import struct
from pathlib import Path
from devtools.terminal_tcg_longmode_image import image
from devtools.terminal_tcg_roundtrip_probe import run


def validate(raw, expected, states, result):
    if len(raw) != expected['output_bytes']:
        raise ValueError('long mode output size')
    a, b, c = raw[:512], raw[512:1024], raw[1024:1536]
    s = states[0]
    checks = {}
    checks['roundtrip_written_fields'] = all(a[x:y]==b[x:y] for x,y in expected['fxsave64_written_spans'])
    checks['high_pointers'] = (struct.unpack_from('<Q',b,8)[0]==int(s['fip'],16)==expected['fip']
                              and struct.unpack_from('<Q',b,16)[0]==int(s['fdp'],16)==expected['fdp'])
    checks['opcode_and_cleared_selectors'] = struct.unpack_from('<H',b,6)[0]==s['fop']==4 and s['fcs']==s['fds']==0
    checks['legacy_pointer_format'] = (struct.unpack_from('<I',c,8)[0]==expected['fip']&0xffffffff
                                       and struct.unpack_from('<I',c,16)[0]==expected['fdp']&0xffffffff
                                       and struct.unpack_from('<H',c,12)[0]==struct.unpack_from('<H',c,20)[0]==0)
    checks['controls'] = (s['fp_control']==struct.unpack_from('<H',b,0)[0]==expected['fp_control']
                          and s['fp_status']==struct.unpack_from('<H',b,2)[0]==expected['fp_status']
                          and s['fp_empty_mask']==(b[4]^0xff)==expected['fp_empty_mask']
                          and s['top']==7 and s['mxcsr']==struct.unpack_from('<I',b,24)[0]==expected['mxcsr'])
    checks['physical_fp'] = all(s['fp_physical_low64_high16'][(i+7)&7]==
        [f'{struct.unpack_from("<Q",b,32+i*16)[0]:016x}',f'{struct.unpack_from("<H",b,40+i*16)[0]:016x}'] for i in range(8))
    checks['actual_arithmetic_result'] = s['fp_physical_low64_high16'][7] == [f'{x:016x}' for x in expected['physical_st7_low64_high16']]
    checks['xmm_all_lanes'] = all(s['xmm_low64_high64'][i]==
        [f'{struct.unpack_from("<Q",b,160+i*16+j*8)[0]:016x}' for j in range(2)] for i in range(16))
    checks['distinct_xmm_restored'] = all(b[160+int(i)*16:176+int(i)*16].hex()==pattern
                                         for i,pattern in expected['xmm_patterns'].items())
    cpuid1=struct.unpack_from('<4I',raw,1536)
    cpuid7=struct.unpack_from('<4I',raw,1552)
    ext=struct.unpack_from('<4I',raw,1568)
    required=expected['requires_actual_cpuid']
    checks['actual_features']=(cpuid1[3]&required['leaf1_edx_set']==required['leaf1_edx_set']
                               and ext[3]&required['leaf80000001_edx_set']==required['leaf80000001_edx_set']
                               and cpuid7[1]&required['leaf7_0_ebx_clear']==0)
    cr0,cr3,cr4,efer=struct.unpack_from('<4Q',raw,1584)
    checks['actual_longmode_controls']=(cr0&expected['required_cr0_set']==expected['required_cr0_set']
        and cr0&expected['required_cr0_clear']==0 and cr3==expected['cr3']
        and cr4&expected['required_cr4_set']==expected['required_cr4_set']
        and efer&expected['required_efer_set']==expected['required_efer_set'])
    seg=s['segments_es_cs_ss_ds_fs_gs_ldt_tr_gdt_idt']
    checks['high_fs_base_and_cs']=(int(seg[4][1],16)==expected['fs_base']
                                   and int(seg[4][0],16)==expected['fs_selector'] and int(seg[1][0],16)==expected['cs'])
    checks['exact_stop']=int(s['eip'],16)==expected['stop']
    checks['all_vps_stopped']=s['cpu']==0 and sorted(s.get('vp_stopped',[]),key=lambda v:v['cpu'])==[dict(cpu=0,stopped=True),dict(cpu=1,stopped=True)]
    checks['stable_reads']=states[0]==states[1]
    checks['clean_exit']=result['exit_code']==33 and result['invalid_cpu_rejected'] and not result['errors']
    result.update(checks=checks,cpuid=dict(leaf1=cpuid1,leaf7=cpuid7,extended=ext))
    return all(checks.values())


if __name__=='__main__':
    p=argparse.ArgumentParser()
    for name in ('binary','firmware','output'):p.add_argument('--'+name,type=Path,required=True)
    raise SystemExit(not run(p.parse_args(),image_builder=image,validator=validate))
