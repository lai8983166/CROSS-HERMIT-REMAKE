"""All 21 pinned source names through real owned offscreen ANSI GDI.

This corpus experiment is separate from the six continuous original-code
branches: it exercises source text/font bytes, not script reachability.
"""
import ctypes as C,gzip,json,struct
from tools import school_retained_name_raster as work
from tools.school_gdi_platform import WindowsGDI
from tools.school_font_raster_catalog import geometry

CATALOG='analysis/school-retained-portrait-catalog-v3-20261022.json'


def source_names():
 a=json.loads(work.base.pinned(work.ACCEPTANCE,work.ACCEPTANCE_SHA));m={r['path']:r['sha256'] for r in a['artifact_manifest']};b=work.base.pinned(CATALOG,m[CATALOG]);r=json.loads(b)
 from tools.school_retained_portrait_verification import verify_catalog
 checked=verify_catalog(r);return r,dict(path=CATALOG,sha256=work.sha(b),independent_catalog=checked)


def raster_name(raw,args,face):
 gd=WindowsGDI();result=None
 try:
  dc=gd.dc();font=gd.font(args,face);gd.select(dc,font);measured,selected=gd.measure(dc,raw);cfg=geometry(measured);bitmap=gd.dib(dc,bytes.fromhex(cfg['header_hex']));gd.select(dc,bitmap)
  brush=gd.handle(gd.g.GetStockObject(4));gd.select(dc,brush);w,h=cfg['raster_size']
  calls=[dict(name='CreateCompatibleDC',args=[0],result=dc),dict(name='CreateFontA',args=args,face_hex=face.hex(),result=font),dict(name='GetTextExtentPoint32A',text_hex=raw.hex(),result=measured)]
  for name,values in [('SetMapMode',[dc,1]),('PatBlt',[dc,0,0,w,h,0xf00021]),('SetBkMode',[dc,1]),('SetBkColor',[dc,0]),('SetTextAlign',[dc,0])]:
   value=int(getattr(gd.g,name)(*values));work.need(value!=0xffffffff and (name not in ('SetMapMode','PatBlt','SetBkMode') or value!=0),'corpus actual GDI state');calls.append(dict(name=name,args=values,result=value))
  stages=[dict(name='clear',hex=gd.raster(bitmap).hex())];p=cfg['padding']
  for color,xy in [(0x080808,[2*p,2*p]),(0xffffff,[p,p])]:
   value=int(gd.g.SetTextColor(dc,color));work.need(value!=0xffffffff,'corpus text color');calls.append(dict(name='SetTextColor',args=[dc,color],result=value));value=int(gd.g.TextOutA(dc,*xy,raw,len(raw)));work.need(value==1,'corpus actual glyph output');calls.append(dict(name='TextOutA',point=xy,text_hex=raw.hex(),result=value));stages.append(dict(name='shadow' if color==0x080808 else 'foreground',hex=gd.raster(bitmap).hex()))
  pixels=gd.raster(bitmap);work.need(any(pixels),'nonempty corpus glyph bitmap');result=dict(text_hex=raw.hex(),ACP=gd.acp,measured=measured,selected_face=selected,geometry=cfg,raster_hex=pixels.hex(),raster_sha256=work.sha(pixels),nonzero_bytes=sum(bool(x) for x in pixels),stages=stages,calls=calls)
 finally:cleanup=gd.close()
 result['cleanup']=cleanup;return result


def run():
 catalog,provenance=source_names();source=work.portrait.selected_source();args=source['font_args'];face=work.base.SOURCE.read_bytes()[args[-1]-work.base.BASE:];face=face[:face.index(0)];cases=[]
 for key,role in sorted(catalog['roles'].items(),key=lambda kv:int(kv[0])):
  c=raster_name(bytes.fromhex(role['name_hex']),args[:-1],face);c.update(role=int(key),source_name=role);cases.append(c);print('offscreen source name',key,role['name_big5'],c['measured'],flush=True)
 return dict(schema_version=1,source_catalog=provenance,font_args=args,face_hex=face.hex(),cases=cases,source_name_count=21,separate_corpus_experiment=True,script_reachability_verified=False,guest_original_code_executed=False,ANSI_encoding_fixed=False,new_window=False,new_OS_input=False,new_GPU=False)


if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();out=work.ROOT/a.out
 if out.exists():p.error('fresh immutable corpus report required')
 r=run();out.write_bytes(gzip.compress(json.dumps(r,separators=(',',':')).encode(),mtime=0))
