"""Independent original mapcom offsets and current-record preparation policy."""
import argparse
from copy import deepcopy
import hashlib
import json
import struct
from capstone import Cs, CS_ARCH_X86, CS_MODE_32
from capstone.x86_const import X86_OP_IMM, X86_OP_MEM
from tools.school_map_common_emulation import map_common_resource, UNITS
from tools.school_tactical_resource_catalog import container_sections
from tools.tactics_exit_emulation import ROOT, SOURCE, SOURCE_SHA256, BASE, report_text
from tools.school_course_unlock_emulation import AUTHORITY

EVIDENCE = ROOT/'analysis/school-map-common-v1-20261010.json'
EVIDENCE_SHA256 = 'ccaf87f94cfb5c1382168f67af75ece728d8bbae7b6cc593cacbdc82ed08368c'


def map_common_inputs(raw):
    sections = container_sections(raw)
    if len(sections) != 4:
        raise ValueError('mapcom top-level count')
    first = sections[0]
    entries = container_sections(raw[first['offset']:first['offset']+first['bytes']])
    if len(entries) != 33:
        raise ValueError('mapcom nested count')
    for entry in entries:
        entry['file_offset'] = first['offset']+entry['offset']
    return {'sections':sections,'first_section_entries':entries,
            'scope':'Original container offsets/hashes only; payload semantics and placement are not asserted.'}


def source_policy():
    image = SOURCE.read_bytes()
    if hashlib.sha256(image).hexdigest() != SOURCE_SHA256:
        raise ValueError('map common source image differs')
    md = Cs(CS_ARCH_X86,CS_MODE_32)
    md.detail = True
    inputs = []
    def instruction(va,mnemonic,expected=None):
        ins = next(md.disasm(image[va-BASE:va-BASE+16],va,count=1))
        if ins.mnemonic != mnemonic:
            raise ValueError('map common source instruction differs')
        if expected is not None and ins.op_str != expected:
            raise ValueError('map common source operands differ')
        inputs.append({'va':hex(va),'instruction_hex':ins.bytes.hex(),
                       'mnemonic':ins.mnemonic,'operands':ins.op_str})
        return ins
    def operand(va,mnemonic,index=-1):
        ins = instruction(va,mnemonic)
        op = ins.operands[index]
        if op.type not in (X86_OP_IMM,X86_OP_MEM):
            raise ValueError('map common constant operand differs')
        return op.imm if op.type==X86_OP_IMM else op.mem.disp
    flag_a = operand(0x4531A8,'movsx')
    flag_b = operand(0x4531B7,'movsx')
    count_address = operand(0x4531D8,'movsx')
    flag_c = operand(0x4532FF,'movsx')
    selected = operand(0x4533AE,'mov',-1)
    stride = operand(0x4531EB,'imul')
    class_offset = operand(0x4531F3,'mov')-UNITS
    max_class = operand(0x4531F9,'cmp')
    state_offset = operand(0x45320B,'mov')-UNITS
    reset_limit = operand(0x45321A,'cmp')
    reset_extra = operand(0x453220,'cmp')
    dead_state = operand(0x453249,'cmp')
    recovery_offset = operand(0x453257,'mov')-UNITS
    recovery_delta = operand(0x45325D,'add')
    recovery_limit = operand(0x453284,'mov')-UNITS
    fallback_state = operand(0x453374,'mov')
    # Independently validate branch structure, not just convenient constants.
    for va,mnemonic,target in ((0x4531B1,'je',0x4532FF),(0x4531C0,'je',0x4532B7),
            (0x4531FC,'jge',0x4532B0),(0x45321E,'jbe',0x453228),
            (0x453224,'je',0x453228),(0x45324C,'je',0x4532B0),
            (0x453290,'jge',0x4532B0),(0x453308,'je',0x453315),
            (0x453313,'je',0x453337),(0x4533B6,'jne',0x453402)):
        if operand(va,mnemonic) != target:
            raise ValueError('map common preparation branch differs')
    instruction(0x453231,'mov','byte ptr [eax + 0x7f4527], 0')
    instruction(0x4532F4,'mov','byte ptr [ecx + 0x7f4527], 0')
    instruction(0x4533E0,'call','0x56d4d0')
    instruction(0x4533F5,'call','0x4680b0')
    instruction(0x453467,'call','0x56d4d0')
    instruction(0x45347C,'call','0x4680b0')
    return {'flag_a_address':hex(flag_a),'flag_b_address':hex(flag_b),'flag_c_address':hex(flag_c),
            'count_address':hex(count_address),'selected_class_address':hex(selected),
            'record_bytes':stride,'class_offset':class_offset,'class_upper_exclusive':max_class,
            'state_offset':state_offset,'reset_states':list(range(reset_limit+1))+[reset_extra],
            'excluded_recovery_state':dead_state,'recovery_offset':recovery_offset,
            'recovery_limit_offset':recovery_limit,'recovery_increment':recovery_delta,
            'fallback_state':fallback_state,'code_inputs':inputs}


def prepare_current_records(header,records,policy=None):
    p = source_policy() if policy is None else policy
    addresses = [p[k] for k in ('flag_a_address','flag_b_address','flag_c_address','count_address','selected_class_address')]
    if any(a not in header or type(header[a]) is not int or not 0 <= header[a] <= 255 for a in addresses):
        raise ValueError('current preparation header bytes')
    count = header[p['count_address']]
    if count >= 128 or count != len(records):
        raise ValueError('current preparation signed count')
    current = []
    for raw in records:
        try:
            record = bytearray.fromhex(raw)
        except (TypeError,ValueError) as error:
            raise ValueError('current preparation record encoding') from error
        if len(record) != p['record_bytes']:
            raise ValueError('current preparation record size')
        current.append(record)
    a,b,c = [header[p[k]] for k in ('flag_a_address','flag_b_address','flag_c_address')]
    state = p['state_offset']
    for record in current:
        if record[p['class_offset']] >= p['class_upper_exclusive']:
            continue
        if a:
            if b:
                if record[state] in p['reset_states']:
                    record[state] = 0
                if record[state] != p['excluded_recovery_state']:
                    value = (struct.unpack_from('<I',record,p['recovery_offset'])[0]+p['recovery_increment']) & 0xFFFFFFFF
                    signed = value if value < 0x80000000 else value-0x100000000
                    limit = struct.unpack_from('<i',record,p['recovery_limit_offset'])[0]
                    struct.pack_into('<i',record,p['recovery_offset'],min(signed,limit))
            else:
                record[state] = 0
        elif c and not b:
            record[state] = p['fallback_state']
    selected = header[p['selected_class_address']]
    order = [i for i,r in enumerate(current) if r[p['class_offset']]==selected]
    order += [i for i,r in enumerate(current) if r[p['class_offset']]!=selected]
    return {'after_records':[r.hex() for r in current],'construction_order':order}


def source_catalog():
    raw,identity = map_common_resource()
    return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'map_common_source':identity,
            **map_common_inputs(raw),'current_preparation_policy':source_policy(),**AUTHORITY}


def native_fixture():
    raw = EVIDENCE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != EVIDENCE_SHA256:
        raise ValueError('frozen map common evidence differs')
    data = json.loads(raw)
    fields = ('name','ready','map_common_loaded','map_common','current_record_preparation',
              'current_copies','current_constructor_input','current_combat_records_unchanged',
              'map_common_persistent_and_effect_bytes_unchanged','persistent_ranges_unchanged',
              'battle_world_constructed','stop_reason')
    return {'schema_version':1,'source_report_sha256':EVIDENCE_SHA256,
            'cases':[{k:deepcopy(c[k]) for k in fields if k in c} for c in data['cases']],**AUTHORITY}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--rules-out',required=True)
    p.add_argument('--fixture-out',required=True)
    args = p.parse_args()
    for name,data in [(args.rules_out,source_catalog()),(args.fixture_out,native_fixture())]:
        (ROOT/name).write_text(report_text(data),encoding='utf-8',newline='\n')
