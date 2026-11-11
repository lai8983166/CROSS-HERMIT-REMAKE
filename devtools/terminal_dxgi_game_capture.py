"""Own-game crop through authenticated, independently tested DXGI helper."""
import hashlib
import json
from pathlib import Path
import subprocess
import time
from devtools import terminal_dxgi_frame_v2 as backend


def qualify_current(path):
    path=Path(path).resolve()
    if not path.is_relative_to(backend.ROOT/'analysis') or path.stat().st_size>65536:
        raise ValueError('bounded local qualification required')
    q=json.loads(path.read_text(encoding='utf8'));build=backend.authenticate_build()
    if q['build']!=build or q['orchestrator']!=backend.identity(Path(backend.__file__)):
        raise ValueError('qualified implementation changed')
    if q.get('pattern_capture_qualified') is not True or q.get('accepted') is not False:
        raise ValueError('pattern qualification missing')
    if q['helper']!=json.loads((path.parent/'helper.stdout').read_bytes()):
        raise ValueError('helper receipt changed')
    if backend.verify_patterns(path.parent,q['helper'])!=q['images']:
        raise ValueError('qualification images changed')
    dp=path.parent/'desktop.json'
    if backend.identity(dp)!=q['desktop_receipt']:raise ValueError('desktop receipt changed')
    desktop=json.loads(dp.read_text(encoding='utf8'))
    if not desktop['restored'] or desktop['checks']!=[[],[]]:raise ValueError('qualification desktop not restored')
    age=time.time_ns()-desktop['after'][-1]['time_ns']
    if not 0<=age<=45*60*1000000000:raise ValueError('recent qualification required (45 minutes)')
    return q


def capture_owned(c,hwnd,output,*,qualification,explicit_capture_override=False,timeout=8):
    if explicit_capture_override is not True:raise PermissionError('explicit presented-frame capture authorization required')
    if not 0<timeout<=8:raise ValueError('bounded helper deadline')
    q=qualify_current(qualification)
    from tools.school_native_dialogue_input import owned_target_guard
    from tools.school_native_scene import APP
    owned_target_guard(c,hwnd)
    output=Path(output).resolve();bmp=Path(str(output)+'.bmp');meta=Path(str(output)+'.frame.json')
    if not output.is_relative_to(backend.ROOT/'analysis') or any(p.exists() for p in (output,bmp,meta)):
        raise ValueError('fresh owned capture output family')
    started=time.monotonic()
    run=subprocess.run([str(backend.EXE),'--window',str(hwnd),str(c.pid),str(c.main),str(APP.resolve()),str(bmp)],
        capture_output=True,timeout=timeout,creationflags=subprocess.CREATE_NO_WINDOW)
    owned_target_guard(c,hwnd)
    if run.returncode:raise RuntimeError('DXGI capture failed: '+run.stderr.decode('utf8','replace')[-1500:])
    receipt=json.loads(run.stdout)
    if not receipt['all_capture_scopes_released'] or receipt['accumulated_frames']<1:
        raise ValueError('capture frame/cleanup missing')
    from PIL import Image
    with Image.open(bmp) as im:
        if im.size!=(receipt['width'],receipt['height']):raise ValueError('actual crop dimensions mismatch')
        frame=im.convert('RGB');extrema=frame.getextrema()
        frame.save(output,format='PNG')
    receipt.update(qualification=backend.identity(Path(qualification)),bitmap=backend.identity(bmp),
                   rgb_extrema=extrema,uniform=all(a==b for a,b in extrema),
                   actual_game_rendering_visually_verified=False)
    receipt['bitmap'].update(retained=False,replaced_by=str(output),retention='RGB preserved losslessly in PNG; unused alpha not retained')
    meta.write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf8')
    # Exact PNG keeps all RGB bytes. Alpha in the desktop BMP is not a game ABI.
    bmp.unlink()
    return dict(path=output.relative_to(backend.ROOT).as_posix(),bytes=output.stat().st_size,
        sha256=hashlib.sha256(output.read_bytes()).hexdigest(),elapsed=time.monotonic()-started,
        pid=c.pid,hwnd=hwnd,backend='DXGI presented-frame own-window crop',
        visually_reviewed=False,graphics_qualified=False,input_sent=False,frame_receipt=str(meta))
