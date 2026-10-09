"""Execute original date-based course unlock on bounded, declared work buffers."""
import argparse
from copy import deepcopy
import hashlib
import struct

from unicorn import UC_HOOK_MEM_WRITE

from tools.tactics_exit_emulation import (
    ExitEmulator, ROOT, SOURCE, SOURCE_SHA256, STACK, report_text)

NATIVE = ((0x4A24A0, 0x4A2700), (0x4A2BA0, 0x4A2D60))
FLAGS, RECORDS, COUNTS = 0x7A5B64, 0x7A5BCA, 0x7AA9EA
AUTHORITY = {k:False for k in ('school_initialized','interactive_school_ready',
                              'live_witness','authorizes_persistent_write')}


def source_rules():
    image = SOURCE.read_bytes()
    if hashlib.sha256(image).hexdigest() != SOURCE_SHA256:
        raise ValueError('original source differs')
    templates = []
    for identity in range(1,101):
        base = 0x74BED0-0x400000+identity*96
        metadata,category,key = struct.unpack_from('<hhh',image,base+4)
        templates.append({'work_id':identity,'month':image[base+2],'week':image[base+3],
                          'metadata':metadata,'category':category,'key':key,
                          'teacher_mask':list(image[base+58:base+78])})
    encoded = ''.join(':'.join(map(str,[r[k] for k in
        ('work_id','month','week','metadata','category','key')]+r['teacher_mask']))+';'
        for r in templates)
    return {'source_image_sha256':SOURCE_SHA256,'templates':templates,
            'template_fields_sha256':hashlib.sha256(encoded.encode()).hexdigest()}


def source_provenance():
    image = SOURCE.read_bytes()
    calls = []
    for address in range(0x49E930,0x49EE30):
        offset = address-0x400000
        if image[offset] == 0xE8 and address+5+struct.unpack_from('<i',image,offset+1)[0] == 0x4D3E90:
            calls.append({'call_va':hex(address),'argument_setup_va':hex(address-11),
                          'instruction_bytes':image[offset-11:offset+5].hex()})
    if len(calls) != 4 or bytes.fromhex(calls[0]['instruction_bytes'])[:6] != bytes.fromhex('6aff6a006a65'):
        raise ValueError('new-game teacher argument setup differs')
    return {'evidence_kind':'original_call_bytes_not_full_initialization',
            'initializer_va':'0x49e930','join_va':'0x4d3e90',
            'teacher_id':101,'group':0,'slot':-1,'calls':calls,
            'chapter012_teacher117':'existing_join_prefix_not_chronological_completion',
            'current_demo_teacher_count':0,'roster_migration_authorized_by_evidence':False}


class CourseUnlockEmulator(ExitEmulator):
    def __init__(self, month, week, *, marked=(), seeded=False):
        super().__init__()
        self._function_ranges = NATIVE
        self._stubs = {0x56CE80:('debug_stack_check',0)}
        self.uc.mem_write(FLAGS,bytes(101))
        self.uc.mem_write(RECORDS,bytes(20000))
        self.uc.mem_write(COUNTS,bytes(40))
        self.write(0x7A528E,month,'h')
        self.write(0x7A5290,week,'h')
        self.write(0x7A528A,0,'h')
        self.uc.mem_write(0x7A5262,bytes([255])*40)
        self.uc.mem_write(0x7A5120,bytes(121))
        self.write(0x7A511C,12345,'i')
        for identity,value in marked:
            self.write(FLAGS+identity,value,'B')
        if seeded:
            # Physical opaque bytes stay with slots, including inactive destinations.
            for slot in range(6):
                self.uc.mem_write(RECORDS+16000+10*slot+8,bytes([70+slot,90+slot]))
            self.uc.mem_write(RECORDS+16000,struct.pack('<BBhhh',2,3,22,-7,123))
            self.uc.mem_write(RECORDS+16010,struct.pack('<BBhhh',1,0,13,9,45))
            self.write(COUNTS+32,2,'h')
        self.visited.clear()
        self.stub_calls.clear()
        self.writes = []
        self._audit_write_hooks.append(self.uc.hook_add(UC_HOOK_MEM_WRITE,self._write_hook))

    def _write_hook(self,uc,access,address,size,value,context):
        if STACK <= address and address+size <= STACK+0x10000:
            return
        permitted = FLAGS+1 <= address and address+size <= FLAGS+101
        permitted |= COUNTS <= address and address+size <= COUNTS+40
        if RECORDS <= address and address+size <= RECORDS+20000:
            permitted |= (address-RECORDS)%10+size <= 8
        if not permitted:
            raise RuntimeError(f'course write outside finite field guard: {address:#x}/{size}')
        self.writes.append({'address':hex(address),'size':size,
                            'value':value & ((1 << (size*8))-1)})

    def snapshot(self):
        buffers = []
        for teacher in range(20):
            rows = []
            for slot in range(100):
                raw = bytes(self.uc.mem_read(RECORDS+teacher*1000+slot*10,10))
                if any(raw):
                    rows.append([slot,*struct.unpack('<BBhhhBB',raw)])
            buffers.append(rows)
        return {'month':self.read(0x7A528E,'h'),'week':self.read(0x7A5290,'h'),
                'course_unlocked_flags':list(self.uc.mem_read(FLAGS,101)),
                'course_counts':[self.read(COUNTS+2*i,'h') for i in range(20)],
                'course_buffers':buffers,'teacher_count':self.read(0x7A528A,'h'),
                'teacher_ids':[self.read(0x7A5262+2*i,'h') for i in range(20)],
                'availability':list(self.uc.mem_read(0x7A5120,121)),
                'global_total_511c':self.read(0x7A511C,'i')}

    def unlock(self):
        before = self.snapshot()
        self.visited.clear()
        self.stub_calls.clear()
        self.writes.clear()
        self.call(0x4A2BA0)
        after = self.snapshot()
        addresses = sorted(self.visited)
        return {'changed_fields':{k:deepcopy(v) for k,v in after.items() if before[k] != v},
                'visited_function_entries':[hex(a) for a,b in NATIVE if a in self.visited],
                'visited_instruction_count':len(addresses),
                'visited_addresses_sha256':hashlib.sha256(report_text(addresses).encode()).hexdigest(),
                'native_writes':deepcopy(self.writes),'stub_calls':dict(self.stub_calls),
                'raw_buffers_sha256':hashlib.sha256(bytes(self.uc.mem_read(RECORDS,20000))).hexdigest()}


def report():
    cases = []
    for month,week in [(0,0),(4,2),(4,3),(4,4),(5,0),(5,1),(5,2),(5,3),(6,5),(9,3),(14,2)]:
        emulator = CourseUnlockEmulator(month,week)
        cases.append({'name':f'date_{month}_{week}','before':emulator.snapshot(),
                      'steps':[emulator.unlock(),emulator.unlock()]})
    emulator = CourseUnlockEmulator(4,3,seeded=True)
    cases.append({'name':'existing_progress_and_physical_opaque','before':emulator.snapshot(),
                  'steps':[emulator.unlock(),emulator.unlock()]})
    emulator = CourseUnlockEmulator(5,1,marked=[(0,9),(1,7),(2,255),(14,2)])
    cases.append({'name':'nonzero_flags_skip','before':emulator.snapshot(),'steps':[emulator.unlock()]})
    emulator = CourseUnlockEmulator(4,2)
    before = emulator.snapshot()
    steps = [emulator.unlock()]
    for month,week in [(4,3),(5,1),(4,2),(5,2)]:
        emulator.write(0x7A528E,month,'h')
        emulator.write(0x7A5290,week,'h')
        steps.append({'declared_date':[month,week],**emulator.unlock()})
    cases.append({'name':'forward_repeat_and_earlier_date','before':before,'steps':steps})
    emulator = CourseUnlockEmulator(4,3)
    emulator.write(COUNTS+32,97,'h')
    cases.append({'name':'capacity_exact_100','before':emulator.snapshot(),'steps':[emulator.unlock()]})
    return {'schema_version':1,'evidence_kind':'isolated_original_course_date_unlock',
            'source_image_sha256':SOURCE_SHA256,'rules':source_rules(),
            'teacher_provenance':source_provenance(),'cases':cases,
            'limitations':['Date, global flags, existing records and zero teacher roster are declared inputs.',
                'Only 4A2BA0/4A24A0 execute; debug stack check is a declared boundary.',
                'No full school boot, work-view refresh, teacher registration or course execution.',
                'Record capacity overflow is not executed; pure operation must refuse it.',
                'New-game teacher101 call bytes do not prove full initialization or current chronology.'],
            **AUTHORITY}


def fixture(data):
    result = deepcopy(data)
    result['source_report_sha256'] = hashlib.sha256(report_text(data).encode()).hexdigest()
    for case in result['cases']:
        for step in case['steps']:
            for key in ('native_writes','visited_function_entries','visited_instruction_count',
                        'visited_addresses_sha256','stub_calls','raw_buffers_sha256'):
                step.pop(key)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=str,required=True)
    parser.add_argument('--godot-out',type=str,required=True)
    args = parser.parse_args()
    paths = [ROOT/args.out,ROOT/args.godot_out]
    if paths[0].resolve() == paths[1].resolve() or any(p.exists() for p in paths):
        parser.error('refusing existing or identical output paths')
    data = report()
    for path,result in zip(paths,[data,fixture(data)]):
        path.write_bytes(report_text(result).encode())
    print(f'{len(data["cases"])} native cases exported; rules {data["rules"]["template_fields_sha256"]}')


if __name__ == '__main__':
    main()
