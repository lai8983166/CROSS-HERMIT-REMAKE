"""Project only opaque GDI identities, retaining actual API payloads and lifetimes."""
import copy
import hashlib
import json
from functools import lru_cache

PLAN_PATH='analysis/terminal-last-dialogue-gdi-plan-v1-20261029.json'
PLAN_SHA256='39955b81bb8c7886c52beda6b8c39f3a6509eb3b42f10f3605ab9d465a7ffde8'
STRIDE=0x100000
CREATE_KINDS={'CreateFontA':'font','CreateCompatibleDC':'dc','CreateDIBSection':'bitmap'}
HANDLE_RESULTS=frozenset((*CREATE_KINDS,'GetStockObject','SelectObject'))

def need(ok,message):
 if not ok:raise ValueError(message)

def handle_indices(name):
 if name in ('CreateFontA','lstrlenA','CreateCompatibleDC','GetStockObject'):return ()
 return (0,1) if name=='SelectObject' else (0,)

@lru_cache(maxsize=1)
def fixed_plan(root):
 raw=(root/PLAN_PATH).read_bytes();need(hashlib.sha256(raw).hexdigest()==PLAN_SHA256,'fixed GDI identity-only plan bytes')
 plan=json.loads(raw)
 need(plan['schema_version']==1 and [(c['name'],len(c['calls'])) for c in plan['cases']]==[('neutral_running',297),('timeout_before_combat',324)],'two complete fixed parent GDI plans')
 return plan

def plan_reference(root):
 return dict(path=PLAN_PATH,sha256=PLAN_SHA256,source=copy.deepcopy(fixed_plan(root)['source']))

class LifetimeGDI:
 """Current native owners and fixed-prefix guest roles, never historical handles.

 ``ledger`` describes the latest lifetime assigned to each guest slot. Historical
 native values may recur there; only ``lifetimes`` and ``calls`` establish which
 owner was live at a particular call. Neither statuses nor pixel data are planned.
 """
 def __init__(self,platform,case_plan,plan_ref,allow_new=lambda:False):
  need(not platform.trace,'install GDI projection before the first original call')
  self.platform=platform;self.service=platform.service;self.trace=platform.trace
  self.plan=copy.deepcopy(case_plan['calls']);self.plan_ref=copy.deepcopy(plan_ref);self.allow_new=allow_new
  self.lifetimes=[];self.calls=[];self._active_native={};self._active_guest={};self._slots={};self._stocks={};self._selected={};self._counts={k:0 for k in CREATE_KINDS.values()}
  self.next=max([case_plan['initial_measurement_dc']['guest']]+[c['result_handle']['guest'] for c in self.plan if 'result_handle' in c])+STRIDE
  initial=case_plan['initial_measurement_dc'];need(initial==dict(guest=platform.measure,role='measurement_dc'),'fixed initial measurement DC identity')
  self._bind(self.service.actual,initial['guest'],'measurement_dc','dc',True,-1)
  self.owner_cleanup=None;platform.space=self;platform.call=self.call;platform.close=self.close

 def _bind(self,native,guest,role,kind,owned,ordinal):
  need(type(native)is int and native not in (0,0xffffffff),'successful real GDI handle')
  need(native not in self._active_native,'native GDI handle already has a live owner')
  need(guest not in self._active_guest,'guest GDI handle already has a live owner')
  row=dict(id=len(self.lifetimes),role=role,kind=kind,owned=owned,guest=guest,native=native,created_call=ordinal,deleted_call=None,alive=True)
  self.lifetimes.append(row);self._active_native[native]=row;self._active_guest[guest]=row;self._slots[guest]=row
  if not owned:self._stocks[role]=row
  return row

 def _fresh(self):
  guest=self.next;need(guest<0x70000000,'bounded fresh post-prefix GDI address space');self.next+=STRIDE;return guest

 def native(self,domain,guest):
  need(domain=='GDI' and guest in self._active_guest,'live declared owned/stock GDI identity')
  return self._active_guest[guest]['native']

 @property
 def guest_to_native(self):return {g:('GDI',r['native']) for g,r in self._active_guest.items()}

 def ledger(self):return [dict(domain='GDI',native=r['native'],guest=g) for g,r in self._slots.items()]

 def _binding(self,row,index=None):
  out={k:row[k] for k in ('role','guest','native')};out['lifetime']=row['id']
  if index is not None:out['index']=index
  return out

 def _check_result(self,row,expected):
  if expected is not None:need(expected==dict(guest=row['guest'],role=row['role']),'observed GDI owner matches fixed parent role/guest')
  return row

 def _stock(self,native,role,kind,ordinal,expected):
  if native in self._active_native:
   row=self._active_native[native];need(not row['owned'] and row['role']==role and row['kind']==kind,'actual stock GDI role remains consistent')
  else:
   need(role not in self._stocks,'one stable current native identity per stock role')
   guest=expected['guest'] if expected is not None else self._fresh();row=self._bind(native,guest,role,kind,False,ordinal)
  return self._check_result(row,expected)

 def _result(self,name,args,native_result,ordinal,expected,bindings):
  if name in CREATE_KINDS:
   kind=CREATE_KINDS[name];role='owned_'+kind+'_'+str(self._counts[kind]);self._counts[kind]+=1
   need(expected is None or expected['role']==role,'fixed original GDI creation ordinal')
   guest=expected['guest'] if expected is not None else self._fresh()
   return self._bind(native_result,guest,role,kind,True,ordinal)
  if name=='GetStockObject':
   need(args==[4],'original stock brush role')
   return self._stock(native_result,'stock_object_4','brush',ordinal,expected)
  dc,obj=bindings;need(dc['kind']=='dc' and obj['kind'] in ('font','bitmap','brush'),'typed original SelectObject owners')
  key=(dc['id'],obj['kind']);previous=self._selected.get(key)
  if previous is not None:
   need(previous['alive'] and previous['native']==native_result,'SelectObject actually returned the previously selected live owner')
   row=self._check_result(previous,expected)
  else:row=self._stock(native_result,'default_'+obj['kind'],obj['kind'],ordinal,expected)
  self._selected[key]=obj;return row

 def _delete(self,row,ordinal,name):
  need(row['owned'] and (row['kind']=='dc')==(name=='DeleteDC'),'delete only a current owned GDI object of the correct kind')
  if name=='DeleteDC':self._selected={k:v for k,v in self._selected.items() if k[0]!=row['id']}
  else:need(all(v is not row for v in self._selected.values()),'successfully deleted GDI object is no longer selected')
  row.update(alive=False,deleted_call=ordinal);del self._active_native[row['native']];del self._active_guest[row['guest']]

 def call(self,g,name,args,ret):
  ordinal=len(self.calls);planned=ordinal<len(self.plan);entry=self.plan[ordinal] if planned else None
  need(planned or self.allow_new(),'fixed parent GDI prefix fully consumed before new stage')
  if planned:need(entry['ordinal']==ordinal and entry['name']==name,'fixed original GDI call order')
  native=list(args);indices=handle_indices(name);bindings=[]
  for index in indices:
   need(args[index] in self._active_guest,'GDI argument refers to a live lifetime')
   row=self._active_guest[args[index]];bindings.append(row);native[index]=row['native']
  if planned:need(entry['argument_handles']==[dict(index=i,guest=r['guest'],role=r['role']) for i,r in zip(indices,bindings)],'fixed parent GDI argument roles/guests')
  row=self.service.call(g,name,native,ret);observed=copy.deepcopy(row);value=row['result'];result_binding=None;deleted=None
  if name in HANDLE_RESULTS:
   expected=entry.get('result_handle') if planned else None
   result_binding=self._result(name,list(args),value,ordinal,expected,bindings);value=result_binding['guest']
  elif name in ('DeleteObject','DeleteDC') and value:
   deleted=bindings[0]['id'];self._delete(bindings[0],ordinal,name)
  event=dict(ordinal=ordinal,name=name,planned=planned,argument_bindings=[self._binding(r,i) for i,r in zip(indices,bindings)],result_binding=self._binding(result_binding) if result_binding is not None else None,deleted_lifetime=deleted)
  self.calls.append(event)
  # This is the original NativeGDI transport behavior. The observed native row,
  # actual raster writes, heap contents, statuses and all padding stay untouched.
  row.update(args=list(args),result=value,actual_API_executed=True)
  row.pop('dc_translated_args',None);row.pop('native_bits',None)
  self.trace.append(dict(name=name,args=list(args),native_args=native,logical_result=value,native_result=observed))
  return row

 def report(self):
  return dict(schema_version=1,plan=copy.deepcopy(self.plan_ref),planned_calls=len(self.plan),observed_calls=len(self.calls),planned_calls_consumed=min(len(self.calls),len(self.plan)),next_fresh_guest=self.next,lifetimes=copy.deepcopy(self.lifetimes),calls=copy.deepcopy(self.calls),latest_guest_slots=self.ledger(),owner_cleanup=copy.deepcopy(self.owner_cleanup))

 def close(self):
  result=self.service.close()
  if self.owner_cleanup is None:
   retired=[]
   for row in list(self._active_guest.values()):
    if row['owned']:
     row.update(alive=False,retired_by='service.close');retired.append(row['id']);del self._active_native[row['native']];del self._active_guest[row['guest']]
   self.owner_cleanup=dict(after_call=len(self.calls),retired_lifetimes=retired,native_result=copy.deepcopy(result))
  return result

def install(machine,root):
 plan=fixed_plan(root);case=next(c for c in plan['cases'] if c['name']==machine.live_input['name'])
 return LifetimeGDI(machine.name_platform,case,plan_reference(root),lambda:machine.last_dialogue_ready)
