"""Declared two-record CPU diagnostic for native cache reuse, not school evidence."""
import argparse
import struct
from unicorn.x86_const import UC_X86_REG_ECX,UC_X86_REG_EIP,UC_X86_REG_ESP
from tools.school_current_units_emulation import (
    SchoolCurrentUnitsEmulator,ROOT,UNITCTRL,RECORD_OFFSET,COUNTER_OFFSET,POOL,UNITS,TASK,STACK,RETURN,
    FILE_IMPORTS,FILE_API,report_text,AUTHORITY)


class DeclaredCacheProbe(SchoolCurrentUnitsEmulator):
    def _hook(self,uc,address,size,context):
        if self.current_loading and address==0x4533FA and self.current_phase=='tail':
            self.finish_current(address);self.stop_reason = 'declared_cache_constructor_return';uc.emu_stop();return
        return super()._hook(uc,address,size,context)


def report():
    e = DeclaredCacheProbe();e.stage = 'tactical_startup';e.combat_records = [{},{}]
    e.original_animation_allocations = []
    e.write(0x7A49FC,TASK);e.write(0x7A4A00,TASK+0x80000);e.texture_table = TASK+0x844
    e.write(UNITCTRL+COUNTER_OFFSET,111)
    raw = bytearray(176);struct.pack_into('<H',raw,2,4);struct.pack_into('<H',raw,12,6);raw[15] = 1
    e.write(UNITCTRL+0x2A304,POOL+0x100000);e.write(POOL+0x100004,64,'H');e.write(POOL+0x100006,96,'H')
    e.write(UNITCTRL+0x2A308,POOL+0x101000);e.write(POOL+0x101000,POOL+0x102000)
    for i,(slot,_) in enumerate(FILE_IMPORTS.items()):e.write(slot,FILE_API+i*16)
    for index in (0,1):
        # Declared inputs: direct copied records and a bounded zero scratch map.
        e.uc.mem_write(UNITCTRL+RECORD_OFFSET+index*176,bytes(raw));e.uc.mem_write(UNITS+index*176,bytes(raw))
        sp = STACK+0xFF00;e.write(sp,0x4533FA);e.write(sp+4,index)
        e.uc.reg_write(UC_X86_REG_ESP,sp);e.uc.reg_write(UC_X86_REG_ECX,UNITCTRL);e.uc.reg_write(UC_X86_REG_EIP,0x4680B0)
        e.current_pending = index;e.current_loading = True;e.stop_reason = None;e.clear_trace('tactical_startup')
        batches = 0
        while True:
            e.uc.emu_start(e.uc.reg_read(UC_X86_REG_EIP),RETURN,timeout=30_000_000,count=12_000_000)
            if e.stop_reason=='declared_cache_constructor_return':break
            if e.stop_reason is None:
                batches += 1
                if batches>8:raise RuntimeError(f'declared cache CPU exceeded finite batches at {e.uc.reg_read(UC_X86_REG_EIP):#x} phase {e.current_phase}')
                continue
            if e.stop_reason!='first_unit_texture_vector':raise RuntimeError(f'declared cache CPU missed boundary {e.stop_reason}')
            target,stride,count,ctor = e.vector_pending
            cpu,stack = e.uc.context_save(),bytes(e.uc.mem_read(STACK,0x10000))
            for i in range(count):
                e.call(ctor,receiver=target+i*stride);e.animation_vector['native_constructors_completed'] += 1
            e.uc.mem_write(STACK,stack);e.uc.context_restore(cpu);e._stub_return(0,20);e.stop_reason = None
    return {'schema_version':1,'evidence_kind':'declared_two_identical_job6_records_native_cache_diagnostic',
        'declared_inputs':{'role':4,'job':6,'indices':[0,1],'initial_counter':111,'initial_cache_zero':True,
            'initial_work_zero':True,'map_dimensions':[64,96],'map_count_zero':True,'renderer_device':0,
            'entry':'direct4680B0 calls with declared4533FA return stop; school loop and record copying are not witnessed'},
        'units':e.current_units,'file_events':e.file_events,
        'controller_allocations':e.current_controller_allocations,'animation_allocations':e.current_animation_allocations,
        'counter':e.read(UNITCTRL+COUNTER_OFFSET),'source_image_sha256':e.current_rules['source_image_sha256'],**AUTHORITY}


if __name__=='__main__':
    p = argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);args = p.parse_args()
    path = ROOT/args.out
    if path.exists():p.error('use a new immutable evidence path')
    path.write_text(report_text(report()),encoding='utf-8',newline='\n')
