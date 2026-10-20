"""Independent original-machine-code replay with recorded real platform outputs."""
import gzip,json,struct,hashlib,base64,zlib
from collections import Counter
from unicorn import Uc,UC_ARCH_X86,UC_MODE_32,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from tools.school_retained_rendering import ROOT,TASK,BASE,SOURCE,SOURCE_SHA256,AddressSpace
from tools.school_retained_rendering_verification import need,sha,canonical,word,source_image
from tools.school_vm_graphics_verification import load_verified_checkpoint
from tools.school_renderer_init_emulation import REGISTERS
from tools.school_world_mode_emulation import architectural_cpu
from PIL import Image
from tools.school_owner_startup import project_constructor
from tools.school_device_init import project_owner
from tools.school_device_init_verification import unpack as small_unpack

def verify_output(c):
 o=c['output'];m=o['metadata'];raw=unpack(o['pixels'])
 need((m['width'],m['height'],m['format'],m['pitch'])==(1024,768,22,4096) and len(raw)==3145728 and sha(raw)==m['sha256'],'complete actual X8R8G8B8 framebuffer')
 wire=[x['reply']['result'] for x in c['native_device_trace'] if x['request']['op']=='render_readback']
 need(len(wire)==1 and bytes.fromhex(wire[0]['hex'])==raw,'actual native framebuffer reply')
 image=ROOT/o['image'];need(sha(image.read_bytes())==o['image_sha256'],'actual PNG file identity')
 expected=Image.frombytes('RGB',(1024,768),raw,'raw','BGRX',4096)
 need(Image.open(image).convert('RGB').tobytes()==expected.tobytes(),'PNG retains all actual RGB pixels')
 textures={};locks={};bound=0;white=0;transparent=0;draws=0;rect=None;glyph_samples=[]
 for step in c['steps']:
  for a in step['result']['api_calls']:
   op=a.get('op');slot=a.get('slot')
   if op=='text_create':textures[a['result']['texture']['pointer']]=dict(width=a['request']['width'],height=a['request']['height'])
   if op=='text_lock':locks[a['request']['pointer']]=a['result']
   if op=='text_unlock':
    t=textures[a['request']['pointer']];t.update(pitch=locks[a['request']['pointer']]['pitch'],pixels=bytes.fromhex(a['request']['hex']))
   if a.get('key')!='device':continue
   if slot==61:bound=a['args'][2]
   if slot==72 and a['args'][4]==20:
    b=bytes.fromhex(a['request']['buffers'][0]['hex']);v=struct.unpack_from('<4fI',b)
    if (v[0],v[1])==(274,580):rect=v[4]
   if slot!=73:continue
   draws+=1;t=textures[bound];vbytes=bytes.fromhex(a['request']['buffers'][1]['hex']);vs=[struct.unpack_from('<4fI3f',vbytes,i*32) for i in range(a['args'][3])]
   indices=list(struct.unpack('<'+'H'*(a['args'][4]*3),bytes.fromhex(a['request']['buffers'][0]['hex'])))
   need(indices==[i+k for i in range(0,len(vs),4) for k in (0,1,2,1,3,2)],'original canonical text quad indices')
   need(rect==0xcc223438,'original fully opened rectangle color/opacity')
   bg=tuple(round(((rect>>s)&255)*(rect>>24)/255) for s in (16,8,0))
   for q in range(0,len(vs),4):
    v0,v1,v2,v3=vs[q:q+4];x=int(v0[0]+.5);y=int(v0[1]+.5);w=round(v1[0]-v0[0]);h=round(v2[1]-v0[1]);sx=round(v0[6]*t['width']);sy=round(v0[7]*t['height']);alpha=(v0[4]>>24)/255
    need(abs((v1[6]-v0[6])*t['width']-w)<.001 and abs((v2[7]-v0[7])*t['height']-h)<.001,'source texel-to-screen geometry')
    for yy in range(h):
     for xx in range(w):
      if not 282<=x+xx<743 or not 590<=y+yy<723:continue
      p=struct.unpack_from('<H',t['pixels'],(sy+yy)*t['pitch']+(sx+xx)*2)[0]
      actual=expected.getpixel((x+xx,y+yy))
      if p==65535:
       want=tuple(round(255*alpha+b*(1-alpha)) for b in bg)
       need(max(abs(a-b) for a,b in zip(actual,want))<=2,'visible actual glyph white/alpha-blend pixels')
       white+=1
       if len(glyph_samples)<10:glyph_samples.append(dict(x=x+xx,y=y+yy,expected=want,actual=actual))
      elif p==0:
       need(max(abs(a-b) for a,b in zip(actual,bg))<=1,'transparent glyph preserves original rectangle')
       transparent+=1
 need(draws==o['indexed_text_draws']==2 and white>=5 and transparent>1000,'two visible source text textures, glyph shape and transparency')
 return dict(indexed_text_draws=draws,white_glyph_pixels=white,transparent_glyph_pixels=transparent,blend_tolerance=2,glyph_samples=glyph_samples,actual_framebuffer_sha256=sha(raw))

def unpack(e):
 b=zlib.decompress(base64.b64decode(e['zlib_base64']));need(len(b)==e['bytes']<=0x2000000 and sha(b)==e['sha256'],'bounded complete buffer identity');return b

class Replay:
 def __init__(self,c,payload):
  self.c=c;self.u=Uc(UC_ARCH_X86,UC_MODE_32);self.image=SOURCE.read_bytes();self.objects={};self.locks={}
  overlays=c['reconstruction']['overlays'];proof=[]
  for at,raw in payload['memory']:
   b=bytearray(raw)
   for row in overlays:
    lo=max(at,row['pointer']);hi=min(at+len(b),row['pointer']+row['bytes'])
    if lo<hi:b[lo-at:hi-at]=bytes.fromhex(row['hex'])[lo-row['pointer']:hi-row['pointer']]
   self.put(at,bytes(b));proof.append(dict(pointer=at,bytes=len(raw),parent_sha256=sha(raw),reconstructed_sha256=sha(b)))
  need(proof==c['reconstruction']['full_parent_maps'],'all retained/reconstructed memory hashes')
  for q in c['startup']['startup_return']['queues']:self.put(q['pointer']-q['guard_bytes'],unpack(q['buffer']))
  self.put(0x21000000,bytes(65536))
  self.put(0x32000000,b'\xc3')
  # Only interfaces actually observed before VM continuation are installed.
  for r in c['device_proxy_trace']:
   if r['op']=='render_prepare':self.identities(r['result']);break
   self.identities(r['result'])
  self.u.context_restore(payload['cpu'])
  need(canonical(architectural_cpu(self.u))==canonical(c['reconstruction']['architectural_restore_recheck']['actual']),'entire original typed CPU context')
 def put(self,at,b):
  cur=at&~4095;end=(at+len(b)+4095)&~4095
  for lo,hi,_ in sorted(self.u.mem_regions()):
   if hi<cur:continue
   if lo>=end:break
   if cur<lo:self.u.mem_map(cur,min(lo,end)-cur)
   cur=max(cur,hi+1)
   if cur>=end:break
  if cur<end:self.u.mem_map(cur,end-cur)
  self.u.mem_write(at,b)
 def identities(self,r):
  if not isinstance(r,dict):return
  if {'pointer','vtable','methods'}<=r.keys() and r['pointer']:
   self.objects[r['pointer']]=r;self.put(r['pointer'],struct.pack('<I',r['vtable']))
   for off,target in r['methods'].items():self.put(r['vtable']+int(off),struct.pack('<I',target));self.put(target,b'\xc3')
  for v in r.values():
   if isinstance(v,dict):self.identities(v)
 def read(self,p,n=4):return bytes(self.u.mem_read(p,n))
 def cpu(self):return {k:self.u.reg_read(v) for k,v in REGISTERS.items()}
 def api(self,a):
  sp=self.u.reg_read(REGISTERS['ESP']);need(a['sp']==sp and a['return_va']==word(self.read(sp)),'source platform call stack/return')
  if a['key']=='textGDI':
   r=a['call'];args=r['args'];need(list(struct.unpack('<'+'I'*len(args),self.read(sp+4,4*len(args))))==args,'full original GDI arguments')
   for row in r['memory_outputs']:self.put(row['pointer'],bytes.fromhex(row['hex']))
   result=r['result'];pop=len(args)*4
  else:
   args=a['args'];need(list(struct.unpack('<'+'I'*len(args),self.read(sp+4,4*len(args))))==args,'full original D3D arguments')
   r=a['result'];op=a['op'];request=a['request'];pointer=args[0]
   if op=='render_call':
    need(args[1:]==request['args'],'all source device scalar arguments')
    for row in request['buffers']:
     need(self.read(args[row['index']+1],len(bytes.fromhex(row['hex']))).hex()==row['hex'],'original-generated GPU geometry/index data')
   elif op=='text_create':
    need(args[1:-1]==[request[k] for k in ['width','height','levels','usage','format','pool']],'source texture dimensions/format')
    self.identities(r);self.put(args[-1],struct.pack('<I',r['texture']['pointer']))
   elif op=='text_desc':self.put(args[2],bytes.fromhex(r['hex']))
   elif op=='text_lock':
    self.put(r['bits'],bytes.fromhex(r['before_hex']));self.put(args[2],bytes.fromhex(r['locked_hex']));self.locks[pointer]=r
   elif op=='text_unlock':
    lock=self.locks[pointer];need(self.read(lock['bits'],len(bytes.fromhex(request['hex']))).hex()==request['hex'] and sha(bytes.fromhex(request['hex']))==r['uploaded_sha256'],'original full pixel converter/upload bytes')
   elif op=='render_vb_lock':
    self.put(r['bits'],bytes.fromhex(r['before_hex']));self.put(args[3],struct.pack('<I',r['bits']));self.locks[pointer]=r
   elif op=='render_vb_unlock':need(self.read(self.locks[pointer]['bits'],len(bytes.fromhex(request['hex']))).hex()==request['hex'],'source font VB data')
   elif op!='text_release':raise ValueError('unknown platform operation')
   result=r['hr'] if 'hr' in r else r['count'];pop=len(args)*4
  self.u.reg_write(REGISTERS['EAX'],result&0xffffffff);self.u.reg_write(REGISTERS['ESP'],sp+4+pop);self.u.reg_write(REGISTERS['EIP'],a['return_va'])
 def step(self,step):
  a=step['result'];root=step['root']
  from tools.school_font_raster_emulation import IMPORTS
  imports={name:slot for slot,(name,caller,pop) in IMPORTS.items()};imports.update(DeleteObject=0x5920c4,DeleteDC=0x592060)
  for call in a['api_calls']:
   if call['key']=='textGDI':
    need(word(self.read(imports[call['call']['name']]))==call['va'],'source IAT actual platform target')
    self.put(call['va'],b'\xc3')
  if root:
   self.put(root['sp'],struct.pack('<'+'I'*(1+len(root['args'])),root['return_va'],*root['args']))
   for k,v in dict(EIP=root['va'],ESP=root['sp'],ECX=root['receiver'],EFLAGS=0x202).items():self.u.reg_write(REGISTERS[k],v)
  need(self.cpu()==a['before_cpu'],'original complete continuation CPU before '+step['label'])
  calls=iter(a['api_calls']);next_api=next(calls,None);counts=Counter();ih=hashlib.sha256();wh=hashlib.sha256();writes=0
  def code(u,at,n,_):
   nonlocal next_api
   if at==a['boundary']:u.emu_stop();return
   if next_api and at==next_api['va']:self.api(next_api);next_api=next(calls,None);return
   need(BASE<=at<0x592000,'unobserved external/game substitute')
   b=self.read(at,n);need(b==self.image[at-BASE:at-BASE+n],'original instruction identity');counts[at]+=1;ih.update(struct.pack('<I',at)+b)
  def write(u,access,at,n,value,_):
   nonlocal writes
   writes+=1;wh.update(struct.pack('<IIQ',at,n,value&0xffffffffffffffff))
  h=self.u.hook_add(UC_HOOK_CODE,code);w=self.u.hook_add(UC_HOOK_MEM_WRITE,write)
  try:self.u.emu_start(a['before_cpu']['EIP'],0,count=2000000,timeout=120_000_000)
  except Exception as exc:raise RuntimeError(step['label']+' at '+hex(self.u.reg_read(REGISTERS['EIP']))) from exc
  finally:self.u.hook_del(h);self.u.hook_del(w)
  need(self.cpu()==a['cpu'] and next_api is None,'complete original CPU/API natural boundary')
  need([dict(va=at,count=n) for at,n in sorted(counts.items())]==a['instruction_counts'] and ih.hexdigest()==a['instruction_sha256'],'independent original instruction stream')
  need(writes==a['writes'] and wh.hexdigest()==a['write_sha256'],'independent complete original writes')
  return sum(counts.values())

def verify(c):
 need(c['source_sha256']==SOURCE_SHA256==sha(SOURCE.read_bytes()),'original source identity')
 startup=c['startup'];api={r['name']:r['result'] for r in startup['constructor']['platform_calls']}
 need(api['GetDC']['result']==c['text_GDI_trace'][0]['result'] and c['text_GDI_trace'][0]['name']=='GetDC','actual source constructor receives process-owned text DC')
 owner=project_constructor(bytes([startup['fill']])*0xc000,api)
 need(small_unpack(startup['constructor']['state']['owner'])==owner,'independent entire original constructor')
 need(small_unpack(startup['device']['state']['owner'])==project_owner(owner,1024,768,startup['hello']['window'],startup['device']['native']['live_results']),'independent original live device initialization')
 final=small_unpack(startup['startup_return']['state']['owner']);image=source_image(api)
 expected=[('original_manager_fonts',TASK+0x1058,final[0x1058:0x10b8]),('original_renderer',TASK+0xb180,final[0xb180:0xba20])]
 for name,at,n in [('original_constructor_table',0x765728,0x2c002),('original_timer',0x799ae0,16),('original_constructor_scalar',0x5ff530,4),('original_CRT_counter',0x79fc74,4),('original_cache_head',0x80a398,4)]:expected.append((name,at,image[at-BASE:at-BASE+n]))
 need(c['reconstruction']['overlays']==[dict(name=name,pointer=at,bytes=len(b),hex=b.hex()) for name,at,b in expected],'only actual source-initialization overlays')
 need(word(final,0x1058)==TASK and word(final,0x105c)==word(final,0xb210) and word(final,0xb208)==api['GetDC']['result'] and struct.unpack_from('<H',final,0xb28e)[0]==1 and startup['startup_return']['full413450_returned'],'original owner/device/DC/gate initialization and full natural return')
 payload,cp=load_verified_checkpoint(c['name'],'rectangle');need(cp==c['reconstruction']['checkpoint'],'pinned logical ancestor')
 space=AddressSpace()
 for row in c['address_translation']:need(space.guest(row['domain'],row['native'])==row['guest'],'typed address translation')
 for row in c['device_proxy_trace']:
  matches=[x for x in c['native_device_trace'] if x['request']==dict(id=x['request']['id'],op=row['op'],**row['native_request']) and x['reply'].get('ok') and x['reply']['result']==row['native_result']]
  need(matches and canonical(space.result('device',row['native_result']))==canonical(row['result']),'actual native API reply/pointer translation')
 runner=Replay(c,payload);n=sum(runner.step(s) for s in c['steps'])
 output=c['output'];pixels=unpack(output['pixels']);need(sha(pixels)==output['metadata']['sha256'],'actual framebuffer readback identity')
 for k in ['backbuffer_hr','desc_hr','image_hr','copy_hr','lock_hr','unlock_hr']:need(output['metadata'][k]==0,'actual framebuffer copy success')
 need(c['device_process_exit_code']==c['GDI_process_exit_code']==0 and c['device_cleanup']['all_owned_resources_released'] and c['GDI_cleanup']['all_owned_resources_released'] and c['text_GDI_cleanup']['all_resources_released'] and c['text_GDI_cleanup']['screen_ReleaseDC']==1,'all three owned platform lifetimes normally closed')
 need(c['device_cleanup']['text_texture_release_counts']==[0,0] and c['device_cleanup']['gamma_device_restored'] and c['device_cleanup']['gamma_desktop_restored'],'text textures and gamma cleaned')
 return dict(case=c['name'],original_instructions_replayed=n,declared_roots=sum(s['root']is not None for s in c['steps']),steps=len(c['steps']),output=verify_output(c),full_outer_world_frame=False)

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('report');p.add_argument('--out',required=True);a=p.parse_args()
 c=json.loads(gzip.decompress((ROOT/a.report).read_bytes()))['case'];result=verify(c);(ROOT/a.out).write_text(json.dumps(result,indent=2)+'\n',encoding='utf8',newline='\n');print(result)
