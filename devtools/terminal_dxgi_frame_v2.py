"""Build/offline verification and explicitly authorized DXGI qualification.

Building is noninteractive. Selftest shows only its own 256x192 pattern window.
Monitor texture stays on GPU; only the owned window crop is copied to CPU/disk.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

ROOT=Path(__file__).resolve().parents[1]
WORK=ROOT/'.venv-audit/host-frame-v2'
SOURCE=ROOT/'devtools/terminal_dxgi_frame_v2.cpp'
EXE=WORK/'bin/terminal_dxgi_frame.exe'
BUILD=WORK/'build.json'


def identity(path):
    p=Path(path)
    return dict(path=str(p),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())


def build():
    compiler=Path('C:/Program Files/Microsoft Visual Studio/2022/Community/VC/Tools/MSVC/14.44.35207')
    sdk=Path('C:/Program Files (x86)/Windows Kits/10'); version='10.0.22621.0'
    cl=compiler/'bin/Hostx64/x64/cl.exe'
    for directory in (WORK,WORK/'bin',WORK/'temp'):directory.mkdir(parents=True,exist_ok=True)
    if EXE.exists() or BUILD.exists():raise ValueError('fresh build required; do not overwrite a running/qualified binary')
    env=dict(os.environ,TEMP=str(WORK/'temp'),TMP=str(WORK/'temp'))
    env['INCLUDE']=';'.join(str(p) for p in [compiler/'include']+[sdk/'Include'/version/x for x in ('ucrt','shared','um','winrt')])
    env['LIB']=';'.join(str(p) for p in [compiler/'lib/x64']+[sdk/'Lib'/version/x/'x64' for x in ('ucrt','um')])
    obj=WORK/'bin/terminal_dxgi_frame.obj'
    command=[str(cl),'/nologo','/std:c++17','/EHsc','/W4','/O2','/MT',str(SOURCE),
             '/Fo'+str(obj),'/Fe'+str(EXE),'/link','d3d11.lib','dxgi.lib','dwmapi.lib','user32.lib','gdi32.lib']
    run=subprocess.run(command,cwd=WORK,env=env,capture_output=True,timeout=120,creationflags=subprocess.CREATE_NO_WINDOW)
    (WORK/'build.log').write_bytes(run.stdout+run.stderr)
    if run.returncode:raise RuntimeError('compiler failed; see '+str(WORK/'build.log'))
    receipt=dict(source=identity(SOURCE),compiler=identity(cl),sdk_version=version,
        sdk_headers=[identity(sdk/'Include'/version/part/name) for part,name in
                     (('shared','dxgi1_2.h'),('um','d3d11.h'),('winrt','wrl/client.h'))],
        executable=identity(EXE),object=identity(obj),command=command,desktop_actions=False)
    BUILD.write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf8')
    return receipt


def authenticate_build():
    receipt=json.loads(BUILD.read_text(encoding='utf8'))
    if receipt['source']!=identity(SOURCE) or receipt['executable']!=identity(EXE):
        raise ValueError('capture source/executable identity changed')
    return receipt


def verify_patterns(directory, report):
    from PIL import Image
    if not report.get('owned_window_destroyed') or not report.get('all_capture_scopes_released'):
        raise ValueError('helper cleanup incomplete')
    frames=report['frames']
    if len(frames)!=2 or [f['seed'] for f in frames]!=[1,2]:raise ValueError('two ordered patterns required')
    palette=[(255,0,0),(0,255,0),(0,0,255),(255,255,0),(255,0,255),(0,255,255),(0,0,0),(255,255,255)]
    images=[]
    for f in frames:
        if f['mismatched_pixels']!=0 or f['present_qpc']<=f['request_qpc'] or f['accumulated_frames']<1:
            raise ValueError('unqualified stale or incorrect frame')
        p=Path(directory)/('pattern-'+str(f['seed'])+'.bmp')
        if p.stat().st_size>256*192*4+128:raise ValueError('unexpected image size')
        with Image.open(p) as im:
            if im.size!=(256,192):raise ValueError('exact pattern dimensions required')
            expected=bytes(c for y in range(192) for x in range(256)
                           for c in palette[(x//32+3*(y//32)+f['seed'])%8])
            if im.convert('RGB').tobytes()!=expected:raise ValueError('independent pixel comparison failed')
        images.append(identity(p))
    if frames[1]['present_qpc']<=frames[0]['present_qpc']:raise ValueError('frame order')
    return images


def qualify(directory, *, desktop_until, explicit_monitor_capture=False):
    if explicit_monitor_capture is not True:raise PermissionError('explicit monitor-frame capture and desktop window required')
    remaining=desktop_until-time.time()
    if not 15<=remaining<=60:raise ValueError('fresh bounded 15..60-second desktop authorization required')
    receipt=authenticate_build()
    directory=Path(directory).resolve()
    if not directory.is_relative_to(ROOT/'analysis') or directory.exists():raise ValueError('fresh analysis directory')
    directory.mkdir()
    from devtools.terminal_host_desktop import guarded_run
    def action():
        run=subprocess.run([str(EXE),'--selftest',str(directory)],capture_output=True,
            timeout=min(25,remaining-5),creationflags=subprocess.CREATE_NO_WINDOW)
        (directory/'helper.stdout').write_bytes(run.stdout)
        (directory/'helper.stderr').write_bytes(run.stderr)
        if run.returncode:raise RuntimeError('independent frame qualification failed: '+run.stderr.decode('utf8','replace'))
        report=json.loads(run.stdout)
        images=verify_patterns(directory,report)
        authenticate_build()
        return dict(helper=report,images=images)
    result=guarded_run(action,directory/'desktop.json')
    result.update(build=receipt,desktop_restored=True,pattern_capture_qualified=True,
                  desktop_receipt=identity(directory/'desktop.json'),
                  orchestrator=identity(Path(__file__)),game_capture_qualified=False,accepted=False)
    (directory/'qualification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8')
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--build',action='store_true')
    a=p.parse_args()
    print(json.dumps(build() if a.build else dict(mode='plan_only',desktop_actions=False,
        build_exists=BUILD.exists(),selftest_requires_new_desktop_authorization=True),indent=2))
