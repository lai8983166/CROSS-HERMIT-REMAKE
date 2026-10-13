"""Independent layer5 text2 raster, texture, presentation and natural wait rules."""
from tools.school_character_animation_catalog import *
from tools.school_character_animation_catalog import source_rules as animation_rules
from tools.school_character_animation_verification import EVIDENCE_SHA256 as PREFIX_SHA
from tools.school_font_raster_catalog import geometry,convert_surface,source_catalog as raster_rules
from tools.school_second_live_text_catalog import bands,source_catalog as band_rules
from tools.school_texture_contract import power_of_two
from tools.school_dialogue_wait_catalog import readiness,source_catalog as wait_rules

TEXTURE=OBJECT+0x28;RASTER=0x3E000000;MIRROR=0x3F000000

def source_rules():
 a=animation_rules();script,layout=script_layout()
 if struct.unpack_from('<2H',script,738)!=(50,4) or struct.unpack_from('<2H',script,742)!=(51,4):raise ValueError('third wait/confirmation source order')
 return {'source_image_sha256':SOURCE_SHA256,'parent_prefix_sha256':PREFIX_SHA,'text_index':2,'layer':5,'texture_record':TEXTURE,'raster':RASTER,'mirror':MIRROR,
  'raster_code_inputs':raster_rules()['code_inputs'],'band_code_inputs':band_rules()['band_code_inputs'],'wait_code_inputs':wait_rules()['code_inputs'],
  'font_args':text_rules()['first_font_arguments'],'text':a['third_text'],'handler_return_PC':286,'readiness_release_PC':290,
  'scope':'Third actual host GDI and fifth actual texture, original one-line fade/readiness; explicit no-input buffers, terminal draw adapters, no GPU/world.'}

def raster_state(before,measured,renderer):
 source_rules();m=memory_regions(before);v=m[VM];t=TEXTURE-VM;cfg=geometry(measured)
 if struct.unpack_from('<I3H',v,28)!=(280,0,17,6) or v[0x1CC]!=5 or struct.unpack_from('<H',v,OBJECT-VM+22)[0] or struct.unpack_from('<2I',v,t+0x2C)!=(0,0):raise ValueError('third actual empty font parent')
 if type(renderer)is not int or not renderer:raise ValueError('third actual renderer binding')
 struct.pack_into('<I',v,t+0x28,0);struct.pack_into('<I',v,t+0x4C,renderer);v[t+0x64:t+0x68]=b'\xff'*4
 struct.pack_into('<I',v,t+0x34,25);struct.pack_into('<2H',v,t+0x38,*cfg['texture_size']);struct.pack_into('<2H',v,t+0x40,*cfg['raster_size'])
 return {'after':regions(m),**cfg}

def presentation(prefix):return third_prefix(prefix['before'],prefix['script_pointer'])['activation']['presentation']

def update_texts(m):
 v=m[VM];draws=[];updates=[];raws=[]
 for node,obj in ((NODE,OBJECT),(NODE7,OBJECT7)):
  origin=list(struct.unpack_from('<2H',v,node-VM+30));off=obj-VM;raw=bytes(v[off:off+BYTES]);e=expected_update(raw,origin,obj)
  v[off:off+BYTES]=bytes.fromhex(e['after_hex']);draws+=e['draws'];raws.append({'receiver':obj,'before_hex':raw.hex(),'after_hex':e['after_hex']})
  updates.append({'receiver':obj,'args':[(node&0xFFFF0000)|origin[0],origin[1]],'return_va':'0x4cd541'})
  struct.pack_into('<H',v,node-VM+4,2)
 return {'text_draws':draws,'text_updates':updates,'objects':raws}

def complete_state(before,device,texture):
 m=memory_regions(before);v=m[VM];t=TEXTURE-VM
 if any(type(p)is not int or not 0<p<0xFFFFFFFF for p in (device,texture)) or struct.unpack_from('<2I',v,t+0x2C)!=(0,0) or struct.unpack_from('<I3H',v,28)!=(280,0,17,6):raise ValueError('third fresh texture and pending handler')
 width,height=[power_of_two(x) for x in struct.unpack_from('<2H',v,t+0x38)]
 struct.pack_into('<2I',v,t+0x28,device,texture);struct.pack_into('<2H',v,t+0x3C,width,height)
 struct.pack_into('<H',v,t+0x44,struct.unpack_from('<H',v,t+0x44)[0]|6);struct.pack_into('<H',v,OBJECT-VM+22,1)
 text=update_texts(m);struct.pack_into('<I',v,28,286)
 return {'after':regions(m),'texture_size':[width,height],**text,'natural_return':{'va':RETURN,'sp':STACK+0xFF04,'eax':1}}

def advance_wait(before,index,prefix):
 source_rules();m=memory_regions(before);v=m[VM];counter=m[0x7A4E18];predicates=[];handlers=[];inputs=[]
 if type(index)is not int or not 0<=index<80 or v[0x1CC]!=5 or struct.unpack_from('<H',v,OBJECT-VM+22)[0]!=1 or struct.unpack_from('<H',v,OBJECT7-VM+22)[0]!=2:raise ValueError('third bounded dual-object wait parent')
 if index==0:
  if struct.unpack_from('<I3H',v,28)!=(286,0,17,6):raise ValueError('third natural handler return')
  struct.pack_into('<I3H',v,28,290,1,50,4);struct.pack_into('<2I',counter,0,struct.unpack_from('<I',counter)[0]+1,0)
  handlers=[{'va':'0x4c5260','receiver':VM,'args':[0,prefix['script_pointer']+738,1],'return_va':'0x4cf020'}]
 else:
  if struct.unpack_from('<I3H',v,28)!=(290,1,50,4):raise ValueError('third held opcode50 parent')
  struct.pack_into('<2I',counter,0,0,struct.unpack_from('<I',counter,4)[0]+1)
  predicates=[{'receiver':VM+0x430+j*0xAB8,'return_value':int(readiness(bytes(v[0x430+j*0xAB8:0x430+(j+1)*0xAB8])))} for j in range(10)]
  if all(p['return_value'] for p in predicates):struct.pack_into('<H',v,32,0)
  output=STACK+0xFF00-4-136-32
  inputs=[{'kind':'mouse','va':'0x4d5ec0','receiver':0x7E1110,'args':[output,0,0,1024,768],'return_va':'0x4cd402','output':output,'return_eax':0,'output_hex':'0000000000000000000000000100'},
   {'kind':'keyboard','va':'0x4128f0','receiver':TASK+0x10B8,'args':[57,0],'return_va':'0x4cd432','return_eax':0}]
 v[0x93E2]=0;text=update_texts(m)
 return {'index':index,'after':regions(m),'predicates':predicates,'handlers':handlers,'input_calls':inputs,'presentation':presentation(prefix),**text,'natural_return':{'va':RETURN,'sp':STACK+0xFF04,'eax':1}}

if __name__=='__main__':
 import sys
 sys.stdout.reconfigure(encoding='utf-8');print(report_text(source_rules()),end='')
