"""Independent Efct image entries and first animation/work inputs."""
import argparse
from copy import deepcopy
import hashlib
import json
import struct
from capstone import Cs, CS_ARCH_X86, CS_MODE_32
from capstone.x86_const import X86_OP_IMM, X86_OP_MEM
from tools.school_unit_asset_catalog import effect_metadata
from tools.school_unit_assets_emulation import effect_resource
from tools.school_tactical_resource_catalog import texture_inputs
from tools.dxanim_lib import parse_program_blocks
from tools.tactics_exit_emulation import ROOT, SOURCE, SOURCE_SHA256, BASE, report_text
from tools.school_course_unlock_emulation import AUTHORITY

EVIDENCE = ROOT/'analysis/school-effect-initialization-v1-20261010.json'
EVIDENCE_SHA256 = 'c48758d10d6fa1c88615f912db0db37fb682d1949dc063542953d2247c5de981'


def effect_texture_inputs(raw):
    if len(raw)<12 or struct.unpack_from('<I',raw)[0] != len(raw):
        raise ValueError('effect image container length')
    count = struct.unpack_from('<I',raw,4)[0]
    if count != 1959 or 8+count*4 > len(raw):
        raise ValueError('effect image count')
    offsets = list(struct.unpack_from('<1959I',raw,8))+[len(raw)]
    if offsets[0] != 8+count*4 or any(a >= b for a,b in zip(offsets,offsets[1:])):
        raise ValueError('effect image offset order/bounds')
    entries = []
    for index,(start,end) in enumerate(zip(offsets,offsets[1:])):
        chunk = raw[start:end]
        # Reuse strict image-header validation with a bounded single-entry
        # container. The historical parser's 580-entry maximum stays intact.
        single = struct.pack('<III',12+len(chunk),1,12)+chunk
        entry = texture_inputs(single)[0]
        entry.update({'index':index,'offset':start,'file_offset':77212+start})
        entries.append(entry)
    return entries


def source_catalog():
    image = SOURCE.read_bytes()
    if hashlib.sha256(image).hexdigest() != SOURCE_SHA256:
        raise ValueError('effect initialization source image differs')
    md = Cs(CS_ARCH_X86,CS_MODE_32)
    md.detail = True
    code_inputs = []
    def source_value(va,mnemonic):
        ins = next(md.disasm(image[va-BASE:va-BASE+16],va,count=1))
        if ins.mnemonic != mnemonic:
            raise ValueError('effect source instruction differs')
        operand = ins.operands[-1]
        if operand.type not in (X86_OP_IMM,X86_OP_MEM):
            raise ValueError('effect source instruction is not a constant')
        value = operand.imm if operand.type==X86_OP_IMM else operand.mem.disp
        code_inputs.append({'va':hex(va),'instruction_hex':ins.bytes.hex(),'mnemonic':ins.mnemonic,'operands':ins.op_str,'value':value})
        return value
    groups = []
    for offset_va,count_va,stride_va,prefix in ((0x466161,0x466182,0x46618B,0),
            (0x466520,0x466553,0x46655C,0),(0x4937E8,0x4937CF,0x4937DF,None)):
        offset = source_value(offset_va,'lea' if prefix is None else 'add')
        if prefix is None:
            prefix = source_value(0x493804,'lea')-offset
        groups.append({'offset':hex(offset),'count':source_value(count_va,'cmp'),
                       'stride':source_value(stride_va,'imul'),'prefix':prefix,'animation_offset':0x48})
    slot = source_value(0x4660FC,'mov')
    block,animation,flags = [source_value(va,'push') for va in (0x466216,0x466214,0x466212)]
    raw,identity = effect_resource()
    metadata = effect_metadata(raw)
    entries = effect_texture_inputs(raw[metadata['metadata_bytes']:])
    first = parse_program_blocks(raw)[block][animation][0]
    first_offset = metadata['sections'][block]['offset']+metadata['sections'][block]['entry_offsets'][animation]
    descriptor = first['descriptors'][0]
    descriptor_offset = metadata['sections'][4]['offset']+descriptor*10
    if descriptor_offset+10 > metadata['sections'][5]['offset']:
        raise ValueError('initial effect descriptor bounds')
    return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'effect_source':identity,
            'metadata_sha256':metadata['metadata_sha256'],'texture_entries':entries,
            'work_groups':groups,'texture_slot':slot,'code_inputs':code_inputs,
            'initial_animation':{'block':block,'animation':animation,'flags':flags,'metadata_offset':first_offset,
                'instruction':first,'descriptor_index':descriptor,'descriptor_offset':descriptor_offset,
                'descriptor_hex':raw[descriptor_offset:descriptor_offset+10].hex(),'descriptor_value':raw[descriptor_offset+8]},
            'scope':'Original resource bytes and initialization inputs; GPU upload, playback and battle state are not asserted.',**AUTHORITY}


def native_fixture():
    raw = EVIDENCE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != EVIDENCE_SHA256:
        raise ValueError('frozen effect initialization report differs')
    data = json.loads(raw)
    fields = ('name','ready','effect_initialized','effect_initialization','effect_entries','effect_boundaries',
              'effect_resets','effect_work_calls','effect_vector','effect_graphics_input','asset_allocations','stop_reason',
              'persistent_ranges_unchanged','current_combat_records_unchanged','battle_world_constructed')
    return {'schema_version':1,'source_report_sha256':EVIDENCE_SHA256,
            'cases':[{k:deepcopy(c[k]) for k in fields if k in c} for c in data['cases']],**AUTHORITY}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--rules-out',required=True)
    p.add_argument('--fixture-out',required=True)
    args = p.parse_args()
    for name,data in [(args.rules_out,source_catalog()),(args.fixture_out,native_fixture())]:
        (ROOT/name).write_text(report_text(data),encoding='utf-8',newline='\n')
