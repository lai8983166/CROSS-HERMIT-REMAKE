"""Independent source replay, platform contracts and fresh corpus reproduction."""
import gzip,json,struct
from unicorn import Uc,UC_ARCH_X86,UC_MODE_32
from tools import school_retained_name_raster as work
from tools import school_retained_name_corpus as corpus
from tools.school_retained_render_pipeline_verification import Replay as SourceReplay
from tools.school_font_raster_catalog import geometry
from tools.school_character_name_catalog import expected_raster,TEXTURE

ROOT=work.ROOT;base=work.base;need=work.need;word=work.word;sha=work.sha;canonical=work.canonical
NAMES=['CreateFontA','lstrlenA','SelectObject','lstrlenA','GetTextExtentPoint32A','SelectObject','CreateCompatibleDC','CreateDIBSection','SelectObject','SetMapMode','GetStockObject','SelectObject','PatBlt','SelectObject','SetBkMode','SetBkColor','SetTextAlign','SetTextColor','lstrlenA','TextOutA','SetTextColor','lstrlenA','TextOutA']


def protocol(c,reference):
 need(c['name'] in ('initial','student9_waiting','fifth_class') and c['scene_capture'] in (76,77),'known retained branch')
 s=c['step'];o=c['offscreen'];r=c['raster'];cfg=geometry(o['measured']);raw=bytes.fromhex(r['hex'])
 need(s['label']=='continuous_original_name_font_and_raster' and s['boundary']==work.STOP and 'root' not in s and s['source_IAT_unchanged'] is True,'continuous source protocol without new root/bindings')
 need([a['name'] for a in s['api_calls']]==NAMES,'all and only 23 original platform calls')
 need(c['cleanup']==dict(fonts=1,bitmaps=1,dcs=2,all_resources_released=True),'all newly owned GDI resources released')
 need(o['translation_only_at_API'] is True and type(o['logical_measurement_dc'])is int and o['logical_measurement_dc']>0 and o['fresh_owned_measurement_dc']!=o['logical_measurement_dc'],'explicit fresh measurement-context reconstruction')
 need((o['ACP'],o['measured'],o['selected_face'])==(reference['ACP'],reference['measured'],reference['selected_face']),'same independently exercised name/ANSI platform')
 need(r['pointer']==work.RASTER and r['bytes']==len(raw)==cfg['raster_size'][0]*cfg['raster_size'][1]*4 and r['sha256']==sha(raw) and r['nonzero_bytes']==sum(bool(x) for x in raw)>0,'bounded complete nonempty actual glyph raster')
 need(r['hex']==reference['raster_hex'],'continuous source pixels match separate actual GDI corpus experiment')
 need(c['pending_texture']['first_instruction_executed'] is False and c['pending_texture']['va']==work.STOP,'texture/GPU entry remains unexecuted')
 for a in s['api_calls']:
  need(work.IMPORTS[a['import_slot']][0]==a['name'] and a['pop']==work.IMPORTS[a['import_slot']][2] and len(a['args'])*4==a['pop'],'exact original platform ABI')


class Replay(SourceReplay):
 def api(self,a):
  need(a['key']=='retained_name_GDI','no game-function substitution');r=a['call'];sp=self.cpu()['ESP'];ret=word(self.read(sp));args=[word(self.read(sp+4+4*i)) for i in range(r['pop']//4)];slot=r['import_slot'];name=r['name'];o=self.case['offscreen'];frame=self.cpu()['EBP'];out=[];expect={}
  need(r['sp']==sp and r['return_va']==ret and r['args']==args and word(self.read(slot))==r['target']==a['va'] and work.IMPORTS[slot][0]==name,'original IAT, caller stack and every API argument')
  if work.IMPORTS[slot][1] is not None:need(ret==(0x4ca7cb if name=='CreateFontA' else work.IMPORTS[slot][1]),'exact source API return site')
  translated=list(args)
  if name not in ('CreateFontA','lstrlenA','CreateCompatibleDC','GetStockObject'):
   need(args[0] in (o['logical_measurement_dc'],o['raster_dc']),'only source measurement or owned raster DC')
   if args[0]==o['logical_measurement_dc']:translated[0]=o['fresh_owned_measurement_dc']
  need(r['dc_translated_args']==translated,'only declared historical DC token translated')
  def output(p,b):out.append(dict(pointer=p,hex=b.hex()))
  if name=='CreateFontA':
   need(args==self.case['parent_boundary']['pending_font']['args'] and r['face_hex']==work.text(self,args[-1]).hex() and r['result']==o['font'],'exact source font/face and recorded fresh font')
  elif name=='lstrlenA':
   need(ret in (0x4051ba,0x405230,0x405676,0x4056c7) and args==[self.local_text] and r['result']==len(self.raw),'exact original formatted name length')
  elif name=='SelectObject':
   expect={0x4051ea:[o['logical_measurement_dc'],o['font']],0x40528a:[o['logical_measurement_dc'],self.old_font],0x40541b:[o['raster_dc'],o['bitmap']],0x405485:[o['raster_dc'],self.brush],0x4054c6:[o['raster_dc'],o['font']]}
   need(ret in expect and args==expect[ret] and 0<r['result']<0xffffffff,'original owned/stock selections')
   if ret==0x4051ea:self.old_font=r['result']
  elif name=='GetTextExtentPoint32A':
   need(args==[o['logical_measurement_dc'],self.local_text,len(self.raw),frame-0x54] and r['measured']==o['measured'] and r['selected_face']==o['selected_face'] and r['text_hex']==self.raw.hex() and r['result']==1,'exact ANSI measurement inputs/results');output(args[3],struct.pack('<2i',*o['measured']))
  elif name=='CreateCompatibleDC':need(args==[0] and r['result']==o['raster_dc'],'fresh private raster DC')
  elif name=='CreateDIBSection':
   header=bytes.fromhex(self.cfg['header_hex']);size=len(bytes.fromhex(self.reference['raster_hex']));extent=(size+4095)&~4095
   need(args==[o['raster_dc'],frame-0x38,0,frame-0x3c,0,0] and self.read(args[1],40)==header and r['header_hex']==header.hex() and r['guest_bits']==work.RASTER and r['mapped_bytes']==extent and r['bitmap_bytes']==size and r['native_bits']>0 and r['result']==o['bitmap'],'exact source DIB header/extent/mapping')
   need(all(not(a<work.RASTER+extent and work.RASTER<=b) for a,b,_ in self.u.mem_regions()),'independent fresh raster mapping');self.u.mem_map(work.RASTER,extent);output(args[3],struct.pack('<I',work.RASTER))
  elif name=='GetStockObject':need(args==[4] and 0<r['result']<0xffffffff,'source stock black brush');self.brush=r['result']
  elif name=='TextOutA':
   p=self.cfg['padding'];idx=1 if ret==0x40569c else 2;xy=[2*p,2*p] if idx==1 else [p,p]
   need(ret in (0x40569c,0x4056e7) and args==[o['raster_dc'],*xy,self.local_text,len(self.raw)] and r['text_hex']==self.raw.hex() and r['result']==1,'exact original two-pass shadow/foreground output');output(work.RASTER,bytes.fromhex(self.reference['stages'][idx]['hex']))
  else:
   w,h=self.cfg['raster_size'];expect={'SetMapMode':[o['raster_dc'],1],'PatBlt':[o['raster_dc'],0,0,w,h,0xf00021],'SetBkMode':[o['raster_dc'],1],'SetBkColor':[o['raster_dc'],0],'SetTextAlign':[o['raster_dc'],0],'SetTextColor':[o['raster_dc'],0x080808 if ret==0x405663 else 0xffffff]}
   need(name in expect and args==expect[name] and r['result']!=0xffffffff and (name not in ('SetMapMode','PatBlt','SetBkMode') or r['result']!=0),'exact source raster GDI state')
   if name=='PatBlt':output(work.RASTER,bytes.fromhex(self.reference['stages'][0]['hex']))
  need(out==r['memory_outputs'],'independent complete API outputs including actual corpus pixels')
  for row in out:self.u.mem_write(row['pointer'],bytes.fromhex(row['hex']))
  self.u.reg_write(base.REGISTERS['EAX'],r['result']);self.u.reg_write(base.REGISTERS['ESP'],sp+4+r['pop']);self.u.reg_write(base.REGISTERS['EIP'],ret)


def verify_case(c,reference):
 protocol(c,reference);memory,cpu,provenance=work.boundary(c['name'],c['scene_capture']);need(canonical(c['parent_boundary'])==canonical(provenance),'full pinned verified portrait boundary');r=Replay.__new__(Replay);r.u=Uc(UC_ARCH_X86,UC_MODE_32);r.image=base.SOURCE.read_bytes();r.objects={};r.locks={};r.case=c;r.reference=reference;r.cfg=geometry(c['offscreen']['measured']);r.old_font=0;r.brush=0
 for at,b in memory:r.u.mem_map(at,len(b));r.u.mem_write(at,b)
 r.u.context_restore(cpu);font=provenance['pending_font'];r.local_text=font['frames'][0]['bp']-0x108;r.raw=bytes.fromhex(work.portrait.selected_source()['name']['hex'])
 need(work.portrait.regions(r)==c['before'] and r.cpu()['EIP']==font['target'],'independent entire pre-state/current source font boundary');graphics=word(r.read(0x7a49fc));need(word(r.read(graphics+0xb208))==c['offscreen']['logical_measurement_dc'],'historical logical DC comes from original reconstructed owner');iat={slot:r.read(slot) for slot in work.IMPORTS}
 s=c['step'];calls=[dict(key='retained_name_GDI',va=a['target'],call=a) for a in s['api_calls']];n=r.step(dict(label=s['label'],root=None,result=dict(s,api_calls=calls)))
 need(iat=={slot:r.read(slot) for slot in work.IMPORTS},'no IAT rewrites');expected=expected_raster(c['before'],c['offscreen']['measured'],graphics,c['offscreen']['font']);need(expected==c['geometry'] and work.portrait.regions(r)==c['after']==expected['after'],'independent full source state projection')
 need(r.read(work.RASTER,c['raster']['bytes']).hex()==c['raster']['hex'],'actual glyph bytes through entire source continuation')
 sp=r.cpu()['ESP'];bp=r.cpu()['EBP'];nbp=font['frames'][0]['bp'];frames=[];p=bp
 for label,ret in [('raster',0x408e81),('texture_wrapper',0x4ca82c),*[(f['label'],f['return_va']) for f in font['frames']]]:
  need(word(r.read(p+4))==ret,'independent original '+label+' return');frames.append(dict(label=label,bp=p,return_va=ret));p=word(r.read(p))
 pending=dict(va=work.STOP,sp=sp,bp=bp,receiver=TEXTURE,args=[word(r.read(graphics+0xb210)),0],return_va=0x405779,frames=frames,first_instruction_executed=False)
 need((sp,bp,r.cpu()['ECX'],word(r.read(sp)))==(nbp-0x2d8,nbp-0x1d4,TEXTURE,0x405779) and c['pending_texture']==pending,'full seven-layer natural task/VM/portrait/font/raster stack')
 need(base.memory_rows(r.u)==c['final_memory'] and canonical(base.architectural_cpu(r.u))==canonical(c['final_architectural_cpu']),'all final maps and complete architectural CPU')
 visited={i['va'] for i in s['instruction_counts']};need({0x56d810,0x575940,0x414440,0x405160}<=visited and work.STOP not in visited,'original formatter/DC accessor/raster bodies, no game substitute or GPU instruction')
 return dict(name=c['name'],scene_capture=c['scene_capture'],new_original_instructions_replayed=n,original_writes=s['writes'],platform_calls=len(calls),full_memory_regions=len(c['final_memory']),natural_stack_layers=len(frames),raster_sha256=c['raster']['sha256'],new_game_roots=0,R3_complete=False)


def verify_corpus(r):
 catalog,source=corpus.source_names();need(r['source_catalog']==source and r['schema_version']==1 and r['source_name_count']==len(r['cases'])==21,'pinned entire source-name corpus');need(r['font_args']==work.portrait.selected_source()['font_args'],'original font arguments')
 source_image=base.SOURCE.read_bytes();face=source_image[r['font_args'][-1]-base.BASE:];face=face[:face.index(0)];need(r['face_hex']==face.hex(),'original raw ANSI font face')
 need([c['role'] for c in r['cases']]==sorted(map(int,catalog['roles'])),'all and only 21 source names exactly once')
 for key in ('script_reachability_verified','guest_original_code_executed','ANSI_encoding_fixed','new_window','new_OS_input','new_GPU'):need(r[key] is False,'honest separate corpus scope '+key)
 need(r['separate_corpus_experiment'] is True,'separate actual GDI experiment, not original VM samples')
 from tools.school_gdi_platform import WindowsGDI
 for c in r['cases']:
  need(c['source_name']==catalog['roles'][str(c['role'])] and c['text_hex']==c['source_name']['name_hex'],'exact original raw name bytes');raw=bytes.fromhex(c['text_hex']);cfg=geometry(c['measured']);pixels=bytes.fromhex(c['raster_hex'])
  need([a['name'] for a in c['calls']]==['CreateCompatibleDC','CreateFontA','GetTextExtentPoint32A','SetMapMode','PatBlt','SetBkMode','SetBkColor','SetTextAlign','SetTextColor','TextOutA','SetTextColor','TextOutA'],'complete separate corpus API summary');need(c['calls'][1]['args']==r['font_args'][:-1] and c['calls'][1]['face_hex']==r['face_hex'] and c['calls'][2]['text_hex']==c['text_hex'] and c['calls'][2]['result']==c['measured'],'corpus font/name/measurement trace identity')
  need(c['geometry']==cfg and len(pixels)==cfg['raster_size'][0]*cfg['raster_size'][1]*4 and sha(pixels)==c['raster_sha256'] and sum(bool(v) for v in pixels)==c['nonzero_bytes']>0 and c['cleanup']==dict(fonts=1,bitmaps=1,dcs=1,all_resources_released=True),'complete corpus raster, geometry and cleanup')
  need([s['name'] for s in c['stages']]==['clear','shadow','foreground'] and c['stages'][0]['hex']==bytes(len(pixels)).hex() and c['stages'][-1]['hex']==c['raster_hex'],'all three actual corpus stages')
  # Independent fresh native repetition: raw source bytes and original font,
  # separate implementation, no producer raster method or historical handles.
  gd=WindowsGDI()
  try:
   dc=gd.dc();font=gd.font(r['font_args'][:-1],bytes.fromhex(r['face_hex']));gd.select(dc,font);measured,face=gd.measure(dc,raw);need((gd.acp,measured,face)==(c['ACP'],c['measured'],c['selected_face']),'fresh native corpus metrics/face');dib=gd.dib(dc,bytes.fromhex(cfg['header_hex']));gd.select(dc,dib);gd.select(dc,gd.handle(gd.g.GetStockObject(4)));w,h=cfg['raster_size'];p=cfg['padding']
   for name,args in [('SetMapMode',[dc,1]),('PatBlt',[dc,0,0,w,h,0xf00021]),('SetBkMode',[dc,1]),('SetBkColor',[dc,0]),('SetTextAlign',[dc,0])]:
    value=int(getattr(gd.g,name)(*args));need(value!=0xffffffff and (name not in ('SetMapMode','PatBlt','SetBkMode') or value!=0),'fresh corpus GDI setup')
   need(gd.raster(dib).hex()==c['stages'][0]['hex'],'fresh actual clear pixels')
   for index,color,xy in [(1,0x080808,[2*p,2*p]),(2,0xffffff,[p,p])]:
    need(int(gd.g.SetTextColor(dc,color))!=0xffffffff and int(gd.g.TextOutA(dc,*xy,raw,len(raw)))==1,'fresh actual corpus glyph draw');need(gd.raster(dib).hex()==c['stages'][index]['hex'],'fresh independently reproduced actual glyph pixels')
  finally:cleanup=gd.close()
  need(cleanup==c['cleanup'],'fresh independent owned-resource cleanup')
 return dict(source_name_count=21,fresh_native_offscreen_corpus_reproduced=True,all_three_pixel_stages_reproduced=True,ANSI_encoding_fixed=False,script_reachability_verified=False)


def verify(r,names):
 need(r['schema_version']==1 and r['new_game_roots']==r['game_function_substitutions']==r['IAT_rebindings']==0,'no source/stack/resource shortcuts')
 for k in ('same_native_lifetime','new_OS_input','new_window','new_GPU','image_loader_executed','texture_create_executed','R3_complete'):need(r[k] is False,'honest reconstructed offscreen scope '+k)
 need(r['fresh_native_offscreen_GDI'] is r['measurement_context_reconstructed'] is True,'explicit fresh resource reconstruction')
 need([(c['name'],c['scene_capture']) for c in r['cases']]==[(n,s) for n in ('initial','student9_waiting','fifth_class') for s in (76,77)],'six complete retained cases');corpus_proof=verify_corpus(names);reference=next(c for c in names['cases'] if c['role']==4)
 for c in r['cases']:protocol(c,reference)
 return dict(schema_version=1,corpus=corpus_proof,cases=[verify_case(c,reference) for c in r['cases']],six_continuous_source_name_rasters_verified=True,source_replay_uses_recorded_platform_outputs=True,corpus_repetition_uses_fresh_native_offscreen_GDI=True,new_window_or_input_or_GPU=False,R3_complete=False)


if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('report');p.add_argument('--corpus',required=True);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('fresh immutable proof path required')
 r=json.loads(gzip.decompress((ROOT/a.report).read_bytes()));names=json.loads(gzip.decompress((ROOT/a.corpus).read_bytes()));checked=verify(r,names);out.write_text(json.dumps(checked,indent=2)+chr(10),encoding='utf8',newline=chr(10));print('six source name rasters and all 21 native corpus names independently verified',flush=True)
