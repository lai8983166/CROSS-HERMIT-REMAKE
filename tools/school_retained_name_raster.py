"""Continuous retained name raster with fresh, owned, offscreen Windows GDI.

The original DC accessor still returns its historical logical token. Only the
platform service translates that token to a new memory DC; it is never sent to
Windows. No guest game function, import table, CPU frame or derived state is
replaced. GPU creation is deliberately left unexecuted.
"""
import copy,gzip,hashlib,json,struct,types
from collections import Counter
from functools import lru_cache
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from tools import school_retained_portrait as portrait
from tools import school_retained_portrait_verification as previous
from tools import school_retained_keyboard as base
from tools.school_gdi_platform import WindowsGDI
from tools.school_font_raster_emulation import IMPORTS
from tools.school_character_name_catalog import TEXTURE,NODE,expected_raster

ROOT=base.ROOT;need=base.need;sha=base.sha;word=base.word;canonical=base.canonical
ACCEPTANCE='analysis/school-retained-portrait-acceptance-v1-20261022.json'
ACCEPTANCE_SHA='8322ecbd5a3d56b26e5e7426212f2aa9152d7c15ee6552c85853697d0f25fb29'
RASTER=0x3c000000
STOP=0x403bd0


@lru_cache(maxsize=1)
def inputs():
 a=json.loads(base.pinned(ACCEPTANCE,ACCEPTANCE_SHA));m={r['path']:r['sha256'] for r in a['artifact_manifest']};path=a['report'];b=base.pinned(path,m[path])
 return json.loads(gzip.decompress(b)),dict(acceptance=ACCEPTANCE,acceptance_sha256=ACCEPTANCE_SHA,report=path,report_sha256=sha(b))


@lru_cache(maxsize=2)
def boundary(name,scene):
 r,p=inputs();c=next(c for c in r['cases'] if (c['name'],c['scene_capture'])==(name,scene));observed=[]
 def capture(u):
  rows=base.memory_rows(u);observed.append((tuple((a,bytes(u.mem_read(a,b-a+1))) for a,b,_ in u.mem_regions()),u.context_save()));return rows
 proxy=types.SimpleNamespace(**dict(vars(base),memory_rows=capture))
 verify=types.FunctionType(previous.verify_case.__code__,dict(previous.verify_case.__globals__,parent=proxy),'observe_verified_font_boundary')
 checked=verify(c);need(len(observed)==1,'one fully independently verified font boundary')
 memory,cpu=observed[0]
 return memory,cpu,dict(source=p,name=name,scene_capture=scene,independent_parent_proof=checked,pending_font=c['pending_font'],final_memory=c['final_memory'],final_architectural_cpu=c['final_architectural_cpu'])


def text(g,p,n=None):
 if n is not None:
  need(0<n<=254,'bounded ANSI length');b=g.read(p,n);need(bytes(1) not in b,'nonempty ANSI span');return b
 b=bytearray()
 for i in range(255):
  c=g.read(p+i,1)
  if c==bytes(1):return bytes(b)
  b+=c
 raise ValueError('bounded terminated ANSI string')


class Offscreen:
 """Own every native GDI object; translate just one historical logical DC."""
 def __init__(self,logical_dc):
  need(type(logical_dc)is int and 0<logical_dc<0xffffffff,'nonzero historical measurement DC token')
  self.gdi=WindowsGDI();self.logical=logical_dc;self.actual=self.gdi.dc();self.bitmap=None;self.raster_dc=None;self.font=None;self.measured=None;self.face=None;self.cleanup=None;self.selection_objects=set()
 def dc(self,h):
  if h==self.logical:return self.actual
  need(h in self.gdi.dcs,'owned fresh raster DC');return h
 def call(self,g,name,args):
  native=list(args);out=[];extra={};gd=self.gdi
  def put(p,b):g.u.mem_write(p,b);out.append(dict(pointer=p,hex=b.hex()))
  if name=='CreateFontA':
   face=text(g,args[-1]);result=gd.font(args[:-1],face);self.font=result;extra['face_hex']=face.hex()
  elif name=='lstrlenA':result=int(gd.k.lstrlenA(text(g,args[0])))
  elif name=='SelectObject':
   native[0]=self.dc(args[0]);need(args[1] in gd.fonts or args[1] in gd.bitmaps or args[1] in self.selection_objects,'owned or returned stock selection object');result=gd.select(*native);self.selection_objects.add(result)
  elif name=='GetTextExtentPoint32A':
   native[0]=self.dc(args[0]);raw=text(g,args[1],args[2]);size,face=gd.measure(native[0],raw);put(args[3],struct.pack('<2i',*size));result=1;self.measured=size;self.face=face;extra.update(measured=size,selected_face=face,text_hex=raw.hex())
  elif name=='CreateCompatibleDC':
   need(args==[0],'original private raster DC argument');result=gd.dc();self.raster_dc=result
  elif name=='CreateDIBSection':
   native[0]=self.dc(args[0]);need(args[2:3]==[0] and args[4:]==[0,0],'owned source DIB inputs');header=g.read(args[1],40);result=gd.dib(native[0],header);self.bitmap=result;size=gd.bitmaps[result]['bytes'];extent=(size+4095)&~4095
   need(all(not (a<RASTER+extent and RASTER<=b) for a,b,_ in g.u.mem_regions()),'fresh raster guest mapping');g.u.mem_map(RASTER,extent);put(args[3],struct.pack('<I',RASTER));extra.update(header_hex=header.hex(),guest_bits=RASTER,mapped_bytes=extent,native_bits=gd.bitmaps[result]['pointer'],bitmap_bytes=size)
  elif name=='GetStockObject':result=gd.handle(gd.g.GetStockObject(*args));self.selection_objects.add(result)
  elif name=='TextOutA':
   native[0]=self.dc(args[0]);raw=text(g,args[3],args[4]);result=int(gd.g.TextOutA(*native[:3],raw,args[4]));need(result==1,'actual offscreen TextOutA');extra['text_hex']=raw.hex()
  elif name in ('SetMapMode','PatBlt','SetBkMode','SetBkColor','SetTextAlign','SetTextColor'):
   native[0]=self.dc(args[0]);result=int(getattr(gd.g,name)(*native));need(result!=0xffffffff and (name not in ('SetMapMode','PatBlt','SetBkMode') or result!=0),'actual offscreen GDI state')
  else:raise ValueError('unsupported original GDI call '+name)
  if name in ('CreateFontA','CreateCompatibleDC','CreateDIBSection'):need(result!=self.logical,'fresh handle must not alias historical token')
  if name in ('PatBlt','TextOutA'):
   need(self.bitmap is not None,'owned current DIB');put(RASTER,gd.raster(self.bitmap))
  return dict(name=name,args=args,dc_translated_args=native,result=result,memory_outputs=out,**extra)
 def close(self):
  if self.cleanup is None:self.cleanup=self.gdi.close()
  return self.cleanup


class RasterGuest(base.Guest):
 def execute_raster(self,service):
  before=self.cpu();counts=Counter();ih=hashlib.sha256();wh=hashlib.sha256();writes=0;apis=[];bindings={word(self.read(slot)):(slot,*v) for slot,v in IMPORTS.items()}
  need(len(bindings)==len(IMPORTS),'distinct original import target bindings');original_iat={slot:self.read(slot).hex() for slot in IMPORTS}
  def code(u,at,n,_):
   if at==STOP:u.emu_stop();return
   if at in bindings:
    slot,name,caller,pop=bindings[at];sp=self.cpu()['ESP'];ret=word(self.read(sp));args=[word(self.read(sp+4+4*i)) for i in range(pop//4)]
    if caller is not None:need(ret==(0x4ca7cb if name=='CreateFontA' else caller),'exact original GDI caller')
    row=service.call(self,name,args);row.update(import_slot=slot,target=at,sp=sp,return_va=ret,pop=pop);apis.append(row)
    u.reg_write(base.REGISTERS['EAX'],row['result']);u.reg_write(base.REGISTERS['ESP'],sp+4+pop);u.reg_write(base.REGISTERS['EIP'],ret);return
   need(base.BASE<=at<0x592000 and self.read(at,n)==self.source[at-base.BASE:at-base.BASE+n],'only original game/CRT instruction '+hex(at))
   counts[at]+=1;ih.update(struct.pack('<I',at)+self.read(at,n))
  def write(u,access,at,n,value,_):
   nonlocal writes
   need(not base.BASE<=at<0x592000,'no original code writes');writes+=1;wh.update(struct.pack('<IIQ',at,n,value&0xffffffffffffffff))
  # lstrlenA is a real system API, with a declared signature in this process.
  import ctypes as C
  service.gdi.k.lstrlenA.argtypes=[C.c_char_p];service.gdi.k.lstrlenA.restype=C.c_int
  c=self.u.hook_add(UC_HOOK_CODE,code);w=self.u.hook_add(UC_HOOK_MEM_WRITE,write)
  try:
   self.u.ctl_remove_cache(before['EIP'],before['EIP']+1);self.u.emu_start(before['EIP'],0,count=2000000,timeout=120000000)
  finally:self.u.hook_del(c);self.u.hook_del(w)
  need(self.cpu()['EIP']==STOP,'natural name texture entry reached');need(original_iat=={slot:self.read(slot).hex() for slot in IMPORTS},'all source IAT entries unchanged')
  return dict(label='continuous_original_name_font_and_raster',before_cpu=before,cpu=self.cpu(),boundary=STOP,instruction_counts=[dict(va=a,count=n) for a,n in sorted(counts.items())],instruction_sha256=ih.hexdigest(),writes=writes,write_sha256=wh.hexdigest(),api_calls=apis,source_IAT_unchanged=True)


def pending(g,initial):
 sp=g.cpu()['ESP'];bp=g.cpu()['EBP'];namebp=initial['frames'][0]['bp'];need((sp,bp,word(g.read(sp)),g.cpu()['ECX'])==(namebp-0x2d8,namebp-0x1d4,0x405779,TEXTURE),'natural name raster texture frame')
 args=[word(g.read(sp+4)),word(g.read(sp+8))];graphics=word(g.read(0x7a49fc));need(args==[word(g.read(graphics+0xb210)),0],'original texture device arguments, not a live native device')
 frames=[];p=bp
 for label,ret in [('raster',0x408e81),('texture_wrapper',0x4ca82c),*[(f['label'],f['return_va']) for f in initial['frames']]]:
  actual=word(g.read(p+4));need(actual==ret,'original '+label+' caller retained');frames.append(dict(label=label,bp=p,return_va=actual));p=word(g.read(p))
 need(frames[2:]==initial['frames'],'five outer original frames preserved')
 return dict(va=STOP,sp=sp,bp=bp,receiver=TEXTURE,args=args,return_va=word(g.read(sp)),frames=frames,first_instruction_executed=False)


def run_case(name,scene):
 restored=boundary(name,scene);g=RasterGuest(restored);initial=restored[2]['pending_font'];need(g.cpu()['EIP']==initial['target'],'verified unexecuted font API');before=portrait.regions(g);graphics=word(g.read(0x7a49fc));logical=word(g.read(graphics+0xb208));service=Offscreen(logical)
 try:
  step=g.execute_raster(service);raster=service.gdi.raster(service.bitmap);expected=expected_raster(before,service.measured,graphics,service.font);after=portrait.regions(g);need(after==expected['after'],'independent entire name raster region projection');need(g.read(RASTER,len(raster))==raster,'guest contains actual owned GDI bitmap')
  result=dict(name=name,scene_capture=scene,parent_boundary=restored[2],before=before,after=after,step=step,pending_texture=pending(g,initial),offscreen=dict(logical_measurement_dc=logical,fresh_owned_measurement_dc=service.actual,translation_only_at_API=True,ACP=service.gdi.acp,measured=service.measured,selected_face=service.face,font=service.font,bitmap=service.bitmap,raster_dc=service.raster_dc),raster=dict(pointer=RASTER,bytes=len(raster),hex=raster.hex(),sha256=sha(raster),nonzero_bytes=sum(bool(v) for v in raster)),geometry=expected,final_memory=base.memory_rows(g.u),final_architectural_cpu=base.architectural_cpu(g.u))
 finally:cleanup=service.close()
 result['cleanup']=cleanup;return result


def run():
 cases=[]
 for name in ('initial','student9_waiting','fifth_class'):
  for scene in (76,77):
   c=run_case(name,scene);cases.append(c);print(name,scene,'fresh offscreen name raster',c['offscreen']['measured'],len(c['step']['api_calls']),'platform calls',flush=True)
 return dict(schema_version=1,cases=cases,new_game_roots=0,game_function_substitutions=0,IAT_rebindings=0,fresh_native_offscreen_GDI=True,measurement_context_reconstructed=True,same_native_lifetime=False,new_OS_input=False,new_window=False,new_GPU=False,image_loader_executed=False,texture_create_executed=False,R3_complete=False)


if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('fresh immutable report path required')
 r=run();out.write_bytes(gzip.compress(json.dumps(r,separators=(',',':')).encode(),mtime=0));print('retained name raster bytes',out.stat().st_size,flush=True)
