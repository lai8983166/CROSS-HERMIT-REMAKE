"""Pinned complete portrait containers and historical native name texture replies."""
import gzip,hashlib,json,struct
from collections import Counter
from functools import lru_cache
from pathlib import Path
from tools import school_retained_name_raster as name
from tools.school_retained_portrait_catalog import INSTALLED,PRIVATE

ROOT=name.ROOT;need=name.need;sha=name.sha
ACCEPTANCE='analysis/school-retained-name-acceptance-v1-20261022.json'
ACCEPTANCE_SHA='3d71a54fb3798de59f16f8464c36a580bbfcd3eca3503ff92d7c15c2c675bc88'
NATIVE='analysis/school-character-name-texture-v3-20261013.json'
NATIVE_SHA='de5d82eda44a0d3e773140c400bdacefd2fb4c06459fbc778b7de7ccf305ec56'


@lru_cache(maxsize=1)
def contracts():
 accepted=json.loads(name.base.pinned(ACCEPTANCE,ACCEPTANCE_SHA));manifest={r['path']:r['sha256'] for r in accepted['artifact_manifest']};path=accepted['report'];report=json.loads(gzip.decompress(name.base.pinned(path,manifest[path])));old=json.loads(name.base.pinned(NATIVE,NATIVE_SHA));c=old['cases'][0];texture=c['name_texture'];need(sha(bytes.fromhex(c['name_raster']['raster']['hex']))==accepted['raster']['sha256'],'identical actual name raster in historical native experiment')
 need([x['offset'] for x in texture['COM_calls']]==[80,56,64,68] and texture['COM_calls'][0]['args'][1:7]==[128,32,1,0,25,1] and all(x['result']['hr']==0 for x in texture['COM_calls']),'four observed successful native texture calls')
 need([x['name'] for x in texture['GDI_cleanup_calls']]==['SelectObject','DeleteObject','DeleteDC','DeleteObject'] and all(x['result']==1 for x in texture['GDI_cleanup_calls'][1:]),'observed original successful GDI cleanup')
 return report,texture,dict(acceptance=ACCEPTANCE,acceptance_sha256=ACCEPTANCE_SHA,report=path,report_sha256=manifest[path],native_texture_report=NATIVE,native_texture_report_sha256=NATIVE_SHA,native_case=old['cases'][0]['name'],identical_name_raster_sha256=accepted['raster']['sha256'],mode='recorded native D3D/GDI replies only; no fresh GPU or expired native handles')


def parse(raw):
 need(isinstance(raw,bytes) and len(raw)==262168,'complete referenced portrait byte extent');need(struct.unpack_from('<3I',raw)==(len(raw),1,12),'one exact portrait container entry');need(struct.unpack_from('<6H',raw,12)==(0x5844,2,256,512,256,512),'source raw DX2 A1R5G5B5 geometry');pixels=raw[24:];values=[v for (v,) in struct.iter_unpack('<H',pixels)];opaque=[i for i,v in enumerate(values) if v&0x8000];bbox=None
 if opaque:bbox=[min(i%256 for i in opaque),min(i//256 for i in opaque),max(i%256 for i in opaque)+1,max(i//256 for i in opaque)+1]
 return dict(bytes=len(raw),entries=1,offset=12,header_hex=raw[12:24].hex(),format=25,size=[256,512],pixel_offset=24,pixel_bytes=len(pixels),pixel_count=len(values),pixel_sha256=sha(pixels),row_sha256=[sha(pixels[i:i+512]) for i in range(0,len(pixels),512)],opaque_pixels=len(opaque),transparent_pixels=len(values)-len(opaque),zero_RGB_opaque=sum(v==0x8000 for v in values),unique_pixel_values=len(set(values)),opaque_bbox=bbox)


def run():
 from tools.school_retained_name_corpus import source_names
 catalog,source=source_names();rows=[]
 for key,role in sorted(catalog['roles'].items(),key=lambda kv:int(kv[0])):
  p=ROOT/role['image_path'];raw=p.read_bytes();private=PRIVATE/p.relative_to(INSTALLED);need(raw==private.read_bytes() and sha(raw)==role['image_sha256'],'source/private complete image identity');rows.append(dict(role=int(key),path=role['image_path'],private_path=private.relative_to(ROOT).as_posix(),source_sha256=sha(raw),container=parse(raw)))
 _,texture,platform=contracts()
 return dict(schema_version=1,source_catalog=source,platform_contract=platform,images=rows,summary=dict(files=len(rows),complete_file_bytes=sum(r['container']['bytes'] for r in rows),pixels=sum(r['container']['pixel_count'] for r in rows),rows=sum(len(r['container']['row_sha256']) for r in rows),formats=[25],DX_modes=[2]),whole_pixel_corpus_checked=True,script_reachability_verified=False,new_GPU=False)


def verify(r):
 from tools.school_retained_name_corpus import source_names
 import array,sys
 catalog,source=source_names();need(r['schema_version']==1 and r['source_catalog']==source and r['platform_contract']==contracts()[2],'pinned source and historical platform contracts');need([x['role'] for x in r['images']]==sorted(map(int,catalog['roles'])),'all and only 21 referenced source images');total=0
 for row in r['images']:
  role=catalog['roles'][str(row['role'])];p=ROOT/role['image_path'];b=p.read_bytes();need(row['path']==role['image_path'] and row['private_path']==(PRIVATE/p.relative_to(INSTALLED)).relative_to(ROOT).as_posix() and b==(ROOT/row['private_path']).read_bytes() and sha(b)==row['source_sha256']==role['image_sha256'],'independent source/private image identity')
  u=lambda at,n:int.from_bytes(b[at:at+n],'little');need(len(b)==u(0,4)==262168 and [u(4,4),u(8,4)]==[1,12] and [u(12+2*i,2) for i in range(6)]==[0x5844,2,256,512,256,512],'independent exact source container/header byte reader');pixels=b[24:];values=array.array('H',pixels)
  if sys.byteorder!='little':values.byteswap()
  lo_x=256;lo_y=512;hi_x=hi_y=0;opaque=black=0;unique=set()
  for i,v in enumerate(values):
   unique.add(v);black+=v==0x8000
   if v>>15:opaque+=1;x=i%256;y=i//256;lo_x=min(lo_x,x);lo_y=min(lo_y,y);hi_x=max(hi_x,x+1);hi_y=max(hi_y,y+1)
  expected=dict(bytes=len(b),entries=1,offset=12,header_hex=b[12:24].hex(),format=25,size=[256,512],pixel_offset=24,pixel_bytes=len(pixels),pixel_count=len(values),pixel_sha256=sha(pixels),row_sha256=[sha(b[24+512*i:24+512*(i+1)]) for i in range(512)],opaque_pixels=opaque,transparent_pixels=len(values)-opaque,zero_RGB_opaque=black,unique_pixel_values=len(unique),opaque_bbox=[lo_x,lo_y,hi_x,hi_y] if opaque else None)
  need(row['container']==expected,'independent every-row/pixel/alpha/bounds contract');total+=len(values)
 need(r['summary']==dict(files=21,complete_file_bytes=21*262168,pixels=total,rows=21*512,formats=[25],DX_modes=[2]) and r['whole_pixel_corpus_checked'] is True and r['script_reachability_verified'] is r['new_GPU'] is False,'honest complete source resource scope')
 return dict(schema_version=1,source_image_files=21,complete_pixels=total,complete_rows=10752,independent_container_pixel_contracts_verified=True,script_reachability_verified=False,new_GPU=False)


if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('fresh immutable catalog required')
 r=run();out.write_bytes(gzip.compress(json.dumps(r,separators=(',',':')).encode(),mtime=0));print(verify(r),flush=True)
