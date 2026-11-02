"""Bounded report/protocol/mutation preflight before expensive original replay."""
import argparse,copy,gc
from tools import terminal_battle_exit_verification as v

def reject(fn,label):
 try:fn()
 except ValueError:return label
 raise ValueError('mutation unexpectedly accepted: '+label)

def audit(path):
 stream=v.parent.stream_report(v.ROOT/path);cases=[];pcs=set();footer=None
 try:
  kind,header=next(stream);v.need(kind=='header','full source header');assembly=v.corpus_provenance(header);declared=header['source_contract'];static=copy.deepcopy(declared)
  for item in static['new_mutable']:item['write_PCs']=[]
  v.need(static==v.e.source_contract(),'full source static contract before original replay')
  for kind,row in stream:
   if kind=='footer':footer=row;break
   d=row['terminal_battle_exit_prefix'];v.need(row['input']==v.e.overlay.parent.corpus()[len(cases)],'complete source case order');print('data preflight',row['input']['name'],flush=True)
   view,view_audit=v.parent_view(row);del view
   data=dict(parent_protocol_view=view_audit,name=row['input']['name'],protocol=v.protocol(row),observed_tasks=v.task_observations(row),native=v.common_native(row),marker_strings=v.common_strings(row),CRT=v.validate_current_CRT(row));mutations=[]
   changes=[('original_wait_reached',True)]
   if d['freeze']['kind']=='unavailable_unit_graphics':changes += [('call_instruction_executed',True),('args',[0,d['freeze']['args'][1]+1]),('resource_slot_hex','01'+bytes(7).hex())]
   else:changes += [('idiv_instruction_executed',True),('maximum_MP',1),('frame_return_address',0x46CF72)]
   for field,value in changes:
    saved=d['freeze'][field];d['freeze'][field]=value
    try:mutations.append(reject(lambda:v.protocol(row),field))
    finally:d['freeze'][field]=saved
   res=d['common_resources'][0];saved=res['upload_hex'];res['upload_hex']=('00' if saved[:2]!='00' else '01')+saved[2:]
   try:mutations.append(reject(lambda:v.common_native(row),'actual whole pixel upload'))
   finally:res['upload_hex']=saved
   saved=d['complete_tasks'];d['complete_tasks']-=349
   try:mutations.append(reject(lambda:v.task_observations(row),'observed complete task count'))
   finally:d['complete_tasks']=saved
   for resource in d['common_resources']:
    v.need(resource['conversion']['args'][3]==0,'every actual default source palette')
   pcs.update(w['pc'] for w in d['writes']);data['rejected_real_report_mutations']=mutations;cases.append(data);del row,d;gc.collect()
  v.need(len(cases)==2 and footer is not None,'both complete source cases and footer')
  v.need(all(m['write_PCs']==sorted(pcs) for m in declared['new_mutable']),'declared write-PC lists equal actual runtime writes')
 finally:stream.close()
 return dict(schema_version=1,source_report=v.file_ref(v.ROOT/path),corpus_assembly=assembly,cases=cases,actual_write_PCs=sorted(pcs),expensive_original_instruction_replay=False,acceptance=False)

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',required=True);p.add_argument('--out',required=True);a=p.parse_args();v.need(not(v.ROOT/a.out).exists(),'fresh immutable report preflight');v.e.terminal.save(a.out,audit(a.report))
