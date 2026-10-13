"""Original T0005 opening layer projection and lossless RGB555 art for Godot."""
import argparse,hashlib,json,struct
from pathlib import Path
from PIL import Image
from tools.school_character_animation_catalog import ROOT,SOURCE,BASE,source_rules,script_layout,text_rules
from tools.school_character_prefix_catalog import source_catalog as character_rules
from tools.school_board_opening_catalog import source_catalog as board_rules

GAME=ROOT/'CROSS HERMIT/CROSS HERMIT/DATA/ADV/BIN'

def dx_image(raw):
 if len(raw)<24 or struct.unpack_from('<3I',raw)!=(len(raw),1,12):raise ValueError('one-entry source image container')
 magic,mode,w,h,sw,sh=struct.unpack_from('<6H',raw,12)
 if (magic,mode)!=(0x5844,2) or (w,h)!=(sw,sh) or len(raw)!=24+w*h*2:raise ValueError('exact RGB555 source geometry')
 pixels=struct.unpack_from('<'+'H'*(w*h),raw,24);im=Image.new('RGBA',(w,h))
 im.putdata([(((v>>10)&31)*255//31,((v>>5)&31)*255//31,(v&31)*255//31,255 if v&0x8000 else 0) for v in pixels]);return im

def projection():
 source_rules();character_rules();board_rules();raw=SOURCE.read_bytes();script,layout=script_layout();entries=text_rules()['entries']
 def string(at,encoding):return raw[at-BASE:raw.index(0,at-BASE)].decode(encoding)
 configs={}
 for ident in (4,7,8):
  w=list(struct.unpack_from('<19h',raw,0x624520-BASE+ident*38));style=w[18];at=struct.unpack_from('<I',raw,0x624834-BASE+style*4)[0];pieces=[]
  for index in range(16):
   row=list(struct.unpack_from('<6h',raw,at-BASE+index*12))
   if row[0]==-1:break
   if row[2]<0 or row[3]<0 or min(row[4:])<=0 or row[2]+row[4]>512 or row[3]+row[5]>512:raise ValueError('frame atlas bounds')
   pieces.append(row)
  else:raise ValueError('frame sentinel')
  configs[str(ident)]={'layer':w[0],'frame_origin':w[1:3],'fill_rect':[w[1]+w[14],w[2]+w[15],w[16],w[17]],'text_origin':w[7:9],'text_width':w[9]-w[7],
   'name_origin':w[12:14],'actor_origin':w[5:7],'frame_style':style,'pieces':pieces}
 actors={}
 for ident in (4,9):
  at=0x622668+ident*60;ptr=struct.unpack_from('<I',raw,at-BASE)[0];name_ptr=struct.unpack_from('<I',raw,0x621F2C-BASE+ident*4)[0]
  w,h,index,x,y=struct.unpack_from('<5H',raw,at-BASE+8)
  if (w,h,index,x,y)!=(108,108,0,0,296):raise ValueError('selected source face variant')
  actors[str(ident)]={'name':string(name_ptr,'cp950'),'filename':string(ptr,'ascii').upper(),'body_rect':[0,0,256,296],'face_rect':[x,y,w,h]}
 current=4;active=[4];selected={};texts={4:[]};pages=[];at=660
 while at<868:
  op,n=struct.unpack_from('<2H',script,at)
  if n<4 or at+n>len(script):raise ValueError('opening command bounds')
  args=[v&0xFFFFFFF for v in struct.unpack_from('<'+'I'*((n-4)//4),script,at+4)] if n!=6 else []
  if op==30:
   cfg,actor,variant,delay=args
   if cfg not in (7,8) or actor not in (4,9) or variant or delay!=30:raise ValueError('unsupported source actor command')
   if cfg not in active:active.append(cfg)
   selected[cfg]=actor;texts.setdefault(cfg,[])
  elif op==43:
   current=args[0]
   if current not in (4,7,8):raise ValueError('unsupported source text target')
  elif op==44:texts[current]=[]
  elif op==17:
   index=struct.unpack_from('<H',script,at+4)[0];texts[current].append(index)
   pages.append({'text_index':index,'config':current,'text':entries[index]['text'],'layers':[{'config':cfg,'actor':selected.get(cfg,0),'text_indices':list(texts[cfg])} for cfg in sorted(active,key=lambda c:configs[str(c)]['layer'])]})
  elif op not in (27,50,51):raise ValueError('unexpected opening command '+str(op))
  at+=n
 if [p['text_index'] for p in pages]!=list(range(10)):raise ValueError('opening source page order')
 return {'schema_version':1,'scene_id':5,'source_image_sha256':source_rules()['source_image_sha256'],'source_script_sha256':layout['source_script_sha256'],
  'mode':'read_only_graphical_opening','logical_size':[1024,768],'configs':configs,'actors':actors,'pages':pages,'timing':{'presentation_hz':60,'background_limit':60,'frame_delay':30,'frame_limit':45,'text_limit':24},
  'authority':'Source script/table projection; first three native text and character transitions verified. Later pages are source projection, not full native VM/world playback.'}

def export(out):
 p=projection();out.mkdir(parents=True,exist_ok=True);p['sources']={};p['outputs']={}
 for name in ('GYBC_00.BIN','SC004.BIN','SC009.BIN'):
  raw=(GAME/name).read_bytes();image=dx_image(raw);filename=name.lower().replace('.bin','.png');image.save(out/filename)
  p['sources'][name]=hashlib.sha256(raw).hexdigest();p['outputs'][filename]={'sha256':hashlib.sha256((out/filename).read_bytes()).hexdigest(),'size':list(image.size)}
 (out/'catalog.json').write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n');return p

def native_visual_fixture():
 from tools.school_character_animation_verification import fixture,EVIDENCE_SHA256
 from tools.school_third_live_text_verification import fixture as third_fixture,EVIDENCE_SHA256 as third_sha
 case=fixture()['cases'][0];points=[]
 for tick in (0,30,31,45,60,61,76,77):
  records=case['character_animation']['steps'][tick]['presentation']
  body=next(r for r in records if r['return_va']=='0x4c9778')
  frame=next((r for r in records if r['va']=='0x4cbdb0' and r['args'][:2]==[254,368]),None)
  fill=next((r for r in records if r['va']=='0x410310' and r['args'][:2]==[277,381]),None)
  points.append({'tick':tick,'actor_alpha':body['args'][2]&255,'frame_alpha':0 if frame is None else frame['args'][2]&255,'fill_alpha':0 if fill is None else fill['args'][5]>>24,'name_visible':any(r['va']=='0x408f90' for r in records)})
 third=third_fixture()['cases'][0];text=[]
 for index in (0,1,12,23,24,25):
  draw=next(r for r in third['third_text_wait']['steps'][index]['text_draws'] if r['args'][0]==0x7DB618)
  text.append({'tick':79+index,'alpha':draw['args'][4]&255})
 return {'native_animation_sha256':EVIDENCE_SHA256,'native_third_text_sha256':third_sha,'character_points':points,'text_points':text,'runtime_fixture':False}

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,default=ROOT/'prototype/assets/school_opening');args=parser.parse_args();export(args.out)
