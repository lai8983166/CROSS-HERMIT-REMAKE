"""Build and audit the bounded real32-bit Direct3D8 helper; never patch native VM."""
import argparse,hashlib,json,os,struct,subprocess,tempfile
from pathlib import Path
from tools.school_texture_contract import ROOT,power_of_two,source_catalog,AUTHORITY,report_text
from tools.school_font_raster_catalog import native_fixture,convert_surface

CS=ROOT/'tools/school_d3d8_platform.cs'
COMPILER=Path(os.environ.get('WINDIR','C:/Windows'))/'Microsoft.NET/Framework/v4.0.30319/csc.exe'

def sha(raw):return hashlib.sha256(raw).hexdigest()

def machine(path):
 raw=Path(path).read_bytes();at=struct.unpack_from('<I',raw,0x3C)[0]
 if raw[:2]!=b'MZ' or raw[at:at+4]!=b'PE\0\0':raise ValueError('platform PE identity')
 return struct.unpack_from('<H',raw,at+4)[0]

def build_helper(path):
 if os.name!='nt':raise RuntimeError('real Windows x86 Direct3D8 platform required')
 path=Path(path).resolve();path.parent.mkdir(parents=True,exist_ok=True)
 p=subprocess.run([str(COMPILER),'/nologo','/platform:x86','/r:System.Web.Extensions.dll','/out:'+str(path),str(CS)],capture_output=True,timeout=30,creationflags=subprocess.CREATE_NO_WINDOW)
 if p.returncode:raise RuntimeError((p.stdout+p.stderr).decode('cp936',errors='replace'))
 if machine(path)!=0x14C:raise RuntimeError('helper is not x86')
 return {'source_path':CS.relative_to(ROOT).as_posix(),'source_sha256':sha(CS.read_bytes()),'compiler_path':str(COMPILER),
  'compiler_sha256':sha(COMPILER.read_bytes()),'helper_sha256':sha(path.read_bytes()),'helper_machine':0x14C}

def validate_input(raw,size):
 if not isinstance(size,list) or len(size)!=2 or any(type(v)is not int for v in size):raise ValueError('platform size shape')
 w,h=size
 if not 1<=w<=1024 or not 1<=h<=256 or power_of_two(w)!=w or power_of_two(h)!=h:raise ValueError('platform bounded power-of-two size')
 if not isinstance(raw,bytes) or len(raw)!=2*w*h:raise ValueError('platform exact16-bit rows')

def run_probe(helper,raw,size):
 validate_input(raw,size)
 if machine(helper)!=0x14C:raise ValueError('x86 platform helper required')
 with tempfile.TemporaryDirectory(prefix='school-d3d8-',dir=ROOT/'.venv-audit') as folder:
  folder=Path(folder);input_file=folder/'input.bin';output=folder/'report.json';input_file.write_bytes(raw)
  p=subprocess.run([str(Path(helper).resolve()),str(input_file),*[str(v) for v in size],str(output)],capture_output=True,timeout=30,creationflags=subprocess.CREATE_NO_WINDOW)
  result=json.loads(output.read_text('utf-8'))
  if p.returncode:raise RuntimeError(result)
 validate_result(result,raw,size)
 return result

def validate_result(result,raw,size):
 validate_input(raw,size)
 if result.get('pointer_bytes')!=4 or not result.get('real_device_and_texture_executed') or not result.get('all_pixels_equal'):raise ValueError('actual x86 platform completion required')
 if result.get('input_sha256')!=sha(raw) or result.get('readback_sha256')!=sha(raw) or bytes.fromhex(result.get('readback_hex',''))!=raw:raise ValueError('entire real texture differs')
 if result.get('cleanup')!={'texture_release_count':0,'device_release_count':0,'factory_release_count':0,'window_destroyed':True,'all_owned_resources_released':True}:raise ValueError('platform cleanup incomplete')
 if result.get('window_visible') is not False or any(result.get(k) is not False for k in ('native_renderer_patched','original_GPU_executed','native_VM_continuation_executed','drawing_or_present_executed')):raise ValueError('platform scope differs')
 for k in ('window_pointer','factory_pointer','device_pointer','texture_pointer'):
  if not 0<int(result[k],16)<0xFFFFFFFF:raise ValueError('actual32-bit pointer required')
 desc=result['description'];w,h=size
 if desc!={'width':w,'height':h,'format':25,'type':1,'usage':0,'pool':1,'size':2*w*h,'multisample':0}:raise ValueError('real texture descriptor differs')
 calls=result['calls'];names=[c['name'] for c in calls];n=names.count('CreateDevice')
 if names!=['GetAdapterDisplayMode']+['CreateDevice']*n+['CreateTexture','GetLevelDesc','LockRect','UnlockRect','LockRect','UnlockRect'] or not 1<=n<=4:raise ValueError('actual platform call order')
 for c,pair in zip(calls[1:1+n],source_catalog()['device_fallbacks']):
  if [c['type'],c['flags']]!=pair or c['adapter']!=0 or c['windowed']!=1:raise ValueError('source device fallback order')
 if any(c['hr']<0 for i,c in enumerate(calls) if not 1<=i<n):raise ValueError('platform HRESULT')
 if calls[1+n]!={'name':'CreateTexture','hr':0,'width':w,'height':h,'levels':1,'usage':0,'format':25,'pool':1}:raise ValueError('original texture parameters')
 if calls[2+n:]!=[{'name':'GetLevelDesc','hr':0,'level':0},{'name':'LockRect','hr':0,'level':0,'flags':0},
  {'name':'UnlockRect','hr':0},{'name':'LockRect','hr':0,'level':0,'flags':16},{'name':'UnlockRect','hr':0}]:raise ValueError('exact real texture descriptor/lock calls')
 for k in ('write_pitch','read_pitch'):
  pitch=result[k]
  if type(pitch)is not int or not 2*w<=pitch<=4096 or pitch%2:raise ValueError('actual bounded pitch')
 physical=Path(result['physical_runtime_path'])
 if machine(physical)!=0x14C or sha(physical.read_bytes())!=result['runtime_sha256']:raise ValueError('actual runtime identity')

def original_upload(case):
 r=case['font_raster']['raster'];raw=bytes.fromhex(r['hex']);w,h=r['size'];size=[power_of_two(w),power_of_two(h)]
 validate_input(bytes(2*size[0]*size[1]),size)
 # Independently verify every byte against the captured original405A80 conversion.
 pixel_bytes=(ROOT/'analysis/school-text-pixels-v1-20261012.json').read_bytes()
 if sha(pixel_bytes)!='e969ad431ae28920e00d7c065d91046633a66b58b0681739d78ee1c6def094d2':raise ValueError('original pixel evidence identity')
 pixels=json.loads(pixel_bytes);native=next(c['conversion'] for c in pixels['cases'] if c['name']==case['name'])
 expected=convert_surface(raw,[w,h],[0,0,w,h],bytes(2*size[0]*size[1]),2*size[0],[0,0])
 actual=bytearray(len(expected));converted=bytes.fromhex(native['after_hex'])
 for y in range(h):actual[y*2*size[0]:y*2*size[0]+2*w]=converted[(y+1)*native['destination_pitch']:(y+1)*native['destination_pitch']+2*w]
 if bytes(actual)!=expected:raise ValueError('original pixel input differs from independent conversion')
 return expected,size

def report(helper,build):
 cases=[]
 for c in native_fixture()['cases']:
  raw,size=original_upload(c);cases.append({'name':c['name'],'input_source':'captured original405A80 output, zero allocation padding declared','input_sha256':sha(raw),'platform':run_probe(helper,raw,size)})
 return {'schema_version':1,'source_contract':source_catalog(),'build':build,'cases':cases,'runtime_fixture':False,**AUTHORITY}

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--helper',default='.venv-audit/school-d3d8-helper.exe');p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('use new immutable evidence path')
 helper=ROOT/a.helper;build=build_helper(helper);out.write_text(report_text(report(helper,build)),encoding='utf-8',newline='\n')
