"""Run the original complete 4D3510 on the replayed campaign's current students."""
import hashlib
import json
import struct

from tools.battle_preparation_emulation import CHAR_BASE, CHAR_STRIDE, PACKAGE_BASE, PACKAGE_STRIDE
from tools.school_job_menu_export import source_menu
from tools.week_settlement_emulation import WeekSettlementEmulator

# The offsets are the same native record fields used by WeekSettlementEmulator.
FIELDS = (
    ('attributes', CHAR_BASE, CHAR_STRIDE, 0x0c, 8, 7, 'B'),
    ('job_progress', PACKAGE_BASE, PACKAGE_STRIDE, 0xd7, 1, 31, 'b'),
    ('unlock_flags', PACKAGE_BASE, PACKAGE_STRIDE, 0xf9, 1, 30, 'B'),
    ('skill_statuses', CHAR_BASE, CHAR_STRIDE, 0xb8, 12, 84, 'B'),
    ('equipped_skills', CHAR_BASE, CHAR_STRIDE, 0x52, 2, 8, 'h'),
    ('equipped_items', CHAR_BASE, CHAR_STRIDE, 0x62, 2, 8, 'h'),
)
FLAGS = (0x7A55FA, 0x7A4E62, 0x7A55F6, 0x7E11A0)


def digest(data):
    return hashlib.sha256(json.dumps(data,ensure_ascii=False,separators=(',',':'),sort_keys=True).encode()).hexdigest()


class PlayedWeek(WeekSettlementEmulator):
    def __init__(self, before):
        super().__init__()
        roster = [r['character_id'] for r in before['participants']]
        if len(roster)!=len(set(roster)) or not 1<=len(roster)<=40 or any(not 1<=i<=44 for i in roster):
            raise ValueError('invalid played school roster')
        if set(roster)!={i for i,v in enumerate(before['availability']) if v==1}:
            raise ValueError('active students differ from the week roster')
        self.write(0x7A5260,len(roster),'h')
        self.uc.mem_write(0x7A5210,struct.pack('<'+'h'*len(roster),*roster))
        self.write(0x7A528E,before['month'],'h')
        self.write(0x7A5290,before['week'],'h')
        self.uc.mem_write(0x7A5120,bytes(before['availability']))
        self.uc.mem_write(0x7AACAC,struct.pack('<360H',*before['item_flags']))
        for address in FLAGS:
            self.write(address,before['flags'][hex(address)],'h')
        for record in before['participants']:
            for key,base,stride,offset,step,count,kind in FIELDS:
                if len(record[key])!=count:raise ValueError(f'invalid {key} array')
                address=base+record['character_id']*stride+offset
                for i,value in enumerate(record[key]):
                    self.write(address+i*step,value,kind)

    def week_snapshot(self):
        size=self.read(0x7A5260,'h')
        roster=struct.unpack('<'+'h'*size,self.uc.mem_read(0x7A5210,2*size))
        rows=[]
        for identity in roster:
            row={'character_id':identity}
            for key,base,stride,offset,step,count,kind in FIELDS:
                address=base+identity*stride+offset
                row[key]=[self.read(address+i*step,kind) for i in range(count)]
            rows.append(row)
        return {'month':self.read(0x7A528E,'h'),'week':self.read(0x7A5290,'h'),
                'flags':{hex(a):self.read(a,'h') for a in FLAGS},'participants':rows,
                'availability':list(self.uc.mem_read(0x7A5120,45)),
                'item_flags':list(struct.unpack('<360H',self.uc.mem_read(0x7AACAC,720)))}


def verify(case):
    before=case['before']
    cpu=PlayedWeek(before)
    cpu.call_week()
    if cpu.week_entry_snapshot!=before:raise ValueError('original week entry differs from command replay')
    after=cpu.week_snapshot()
    actual=digest(after)
    if actual!=case['expected_sha256']:raise ValueError(f"original week output differs at {after['month']}/{after['week']}")
    calls=[e['character_id'] for e in cpu.week_events if e['va']=='0x4d3aa0']
    if calls!=[row['character_id'] for row in after['participants']]:raise ValueError('incorrect qualification visit order')
    probes=[(r['character_id'],[i+1 for i,flag in enumerate(r['unlock_flags']) if flag==1]) for r in after['participants']]
    selectable={str(row['member']):row['selectable_jobs'] for row in source_menu(probes)['lookup_probes']}
    if case['selectable_jobs']!=selectable:raise ValueError('personal job menu differs from original 4B12A0')
    return {'date':[after['month'],after['week']],'native_state_sha256':actual,
            'menu_cells_compared':15*len(calls),'selectable_jobs_sha256':digest(selectable),
            'roster':calls,'qualification_bytes_compared':30*len(calls),
            'qualification_sha256':digest([r['unlock_flags'] for r in after['participants']])}
