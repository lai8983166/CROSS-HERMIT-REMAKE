"""Independent chronological audit of real GDI receipts and opaque identities."""
import copy
import hashlib
import json

def need(ok,message):
 if not ok:raise ValueError(message)

def positions(name):
 if name in ('CreateFontA','lstrlenA','CreateCompatibleDC','GetStockObject'):return []
 return [0,1] if name=='SelectObject' else [0]

CREATIONS={'CreateFontA':'font','CreateCompatibleDC':'dc','CreateDIBSection':'bitmap'}
HANDLES=set(CREATIONS)|{'GetStockObject','SelectObject'}

def audit(calls,traces,declared,projection,old_calls,plan_bytes,plan_path,parent_reference,case_name):
 """Derive lifetimes from ABI results; source lifetime annotations are assertions.

 The fixed parent supplies only guest identities for opaque handles. Native
 integers, API statuses, buffers and pixels always come from current receipts.
 """
 plan=json.loads(plan_bytes);need(plan['source']==parent_reference,'GDI plan fixed source identity')
 case=next(c for c in plan['cases'] if c['name']==case_name);pc=case['calls'];n=len(old_calls)
 need(case['initial_measurement_dc']==dict(guest=0x6A001000,role='measurement_dc') and len(pc)==n,'entire fixed parent GDI plan')
 for i,(p,c) in enumerate(zip(pc,old_calls)):
  need(p['ordinal']==i and p['name']==c['name'] and [(x['index'],x['guest']) for x in p['argument_handles']]==[(j,c['args'][j]) for j in positions(c['name'])],'plan handles independently equal canonical parent call')
  need(('result_handle' in p)==(c['name'] in HANDLES) and (c['name'] not in HANDLES or p['result_handle']['guest']==c['result']),'plan result independently equals canonical parent handle')
 need(declared['schema_version']==1 and declared['plan']==dict(path=plan_path,sha256=hashlib.sha256(plan_bytes).hexdigest(),source=parent_reference),'current lifetime report binds independently checked plan')
 need(len(calls)==len(traces)==declared['observed_calls'] and declared['planned_calls']==declared['planned_calls_consumed']==n and len(calls)>n,'complete parent and new GDI chronology')
 need(len(declared['calls'])==len(calls),'one binding event per actual API')
 # Initial HDC is a current method input, observed as the first selection target.
 first=next(t for t in traces if t['name']=='SelectObject');initial_native=first['native_args'][0]
 records=[];live_guest={};live_native={};slots={};stocks={};selected={};counts={k:0 for k in CREATIONS.values()}
 def add(g,native,role,kind,owned,i):
  need(type(g)is int and 0<g<2**32 and type(native)is int and native not in (0,0xffffffff) and 0<native<2**64,'actual valid GDI identity')
  need(g not in live_guest and native not in live_native,'no simultaneously live GDI guest/native alias')
  r=dict(id=len(records),role=role,kind=kind,owned=owned,guest=g,native=native,created_call=i,deleted_call=None,alive=True)
  records.append(r);live_guest[g]=r;live_native[native]=r;slots[g]=r
  if not owned:need(role not in stocks,'stable current stock role');stocks[role]=r
  return r
 def binding(r,index=None):
  b=dict(lifetime=r['id'],role=r['role'],guest=r['guest'],native=r['native'])
  if index is not None:b['index']=index
  return b
 add(0x6A001000,initial_native,'measurement_dc','dc',True,-1)
 fresh=max([0x6A001000]+[p['result_handle']['guest'] for p in pc if 'result_handle' in p])+0x100000
 for i,(c,t,event) in enumerate(zip(calls,traces,declared['calls'])):
  nm=c['name'];args=c['args'];nr=t['native_result'];ids=positions(nm);bound=[];native=list(args)
  if 'GDI_trace_index' in c:need(c['GDI_trace_index']==i,'absolute actual GDI trace ordinal')
  for j in ids:
   need(args[j] in live_guest,'no retired or undeclared guest GDI argument');r=live_guest[args[j]];bound.append(r);native[j]=r['native']
  need(t['name']==nm and t['args']==args and t['native_args']==nr['args']==native and t['logical_result']==c['result'] and c['actual_API_executed'] is True,'entire actual GDI native ABI and receipt')
  if i<n:
   p=pc[i];need(p['name']==nm and p['argument_handles']==[dict(index=j,guest=r['guest'],role=r['role']) for j,r in zip(ids,bound)],'current parent handle arguments and roles fixed')
  result=None;deleted=None
  if nm in HANDLES:
   guest=c['result'];native_result=nr['result'];expected=pc[i]['result_handle'] if i<n else None
   if nm in CREATIONS:
    kind=CREATIONS[nm];role='owned_'+kind+'_'+str(counts[kind]);counts[kind]+=1
    if i>=n:need(guest==fresh and guest<0x70000000,'fresh per-creation post-prefix GDI identity');fresh+=0x100000
    result=add(guest,native_result,role,kind,True,i)
   else:
    if nm=='GetStockObject':need(args==[4],'original stock brush index');kind='brush';role='stock_object_4';prior=None
    else:
     dc,obj=bound;need(dc['kind']=='dc' and obj['kind'] in ('font','bitmap','brush'),'typed DC and selected object');kind=obj['kind'];role='default_'+kind;prior=selected.get((dc['id'],kind))
    if prior is not None:
     need(prior['alive'] and prior['native']==native_result and prior['guest']==guest,'SelectObject returns actual previously selected live object');result=prior
    elif native_result in live_native:
     result=live_native[native_result];need(not result['owned'] and result['kind']==kind and result['role']==role and result['guest']==guest,'actual persistent stock/default identity')
    else:
     if i>=n:need(guest==fresh and guest<0x70000000,'fresh first observed stock identity');fresh+=0x100000
     result=add(guest,native_result,role,kind,False,i)
    if nm=='SelectObject':selected[(dc['id'],kind)]=obj
   if expected is not None:need(expected==dict(guest=result['guest'],role=result['role']),'canonical parent result role and guest')
  else:
   need(c['result']==nr['result'],'non-handle API result never projected')
   if nm in ('DeleteObject','DeleteDC') and nr['result']:
    r=bound[0];need(r['owned'] and (r['kind']=='dc')==(nm=='DeleteDC'),'delete exact owned object kind')
    if nm=='DeleteDC':selected={k:v for k,v in selected.items() if k[0]!=r['id']}
    else:need(all(v['id']!=r['id'] for v in selected.values()),'delete only after actual deselection/DC release')
    deleted=r['id'];r.update(alive=False,deleted_call=i);del live_guest[r['guest']];del live_native[r['native']]
  want=dict(ordinal=i,name=nm,planned=i<n,argument_bindings=[binding(r,j) for j,r in zip(ids,bound)],result_binding=binding(result) if result is not None else None,deleted_lifetime=deleted)
  need(event==want,'each source lifetime event independently derived from current API chronology')
  output=copy.deepcopy(nr);output.pop('dc_translated_args',None);output.pop('native_bits',None);output.update(args=args,result=c['result'],actual_API_executed=True)
  need(all(c[k]==v for k,v in output.items()),'every actual API output/status/buffer preserved')
 need(declared['next_fresh_guest']==fresh,'complete fresh GDI allocation cursor')
 need([r['id'] for r in live_guest.values() if r['owned']]==[0],'only declared measurement DC remains owned at service close')
 cleanup=declared['owner_cleanup'];need(cleanup is not None and cleanup['after_call']==len(calls) and cleanup['retired_lifetimes']==[0],'separate actual measurement owner cleanup')
 records[0].update(alive=False,retired_by='service.close')
 need(declared['lifetimes']==records,'all creation/selection/deletion lifetimes exact with no hidden owner')
 latest=[dict(domain='GDI',native=r['native'],guest=g) for g,r in slots.items()]
 need(projection==declared['latest_guest_slots']==latest,'guest slot ledger reflects last actual lifetime rather than native integer uniqueness')
 return dict(calls=len(calls),fixed_parent_calls=n,lifetimes=len(records),native_value_reissues=len(records)-len({r['native'] for r in records}),all_argument_and_result_lifetimes_verified=True,all_actual_API_outputs_preserved=True)
