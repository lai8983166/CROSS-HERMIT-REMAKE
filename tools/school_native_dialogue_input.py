"""Reviewable held-scan-code backend. Not enabled without explicit user override.

No code executes on import. The guarded entry requires the live owned Job,
original process image, original window property and current foreground HWND.
The currently active computer-use skill restricts UI actions to its JS API;
this backend MUST NOT be invoked until the user explicitly authorizes the
exception. Tests use an inert API and never submit Windows input.
"""
import ctypes as C
import ctypes.wintypes as W
import time


class KEYBDINPUT(C.Structure):
 _fields_=[('wVk',W.WORD),('wScan',W.WORD),('dwFlags',W.DWORD),('time',W.DWORD),('dwExtraInfo',C.c_size_t)]


class MOUSEINPUT(C.Structure):
 _fields_=[('dx',W.LONG),('dy',W.LONG),('mouseData',W.DWORD),('dwFlags',W.DWORD),('time',W.DWORD),('dwExtraInfo',C.c_size_t)]


class INPUTUNION(C.Union):
 _fields_=[('ki',KEYBDINPUT),('mi',MOUSEINPUT)]


class INPUT(C.Structure):
 _fields_=[('type',W.DWORD),('data',INPUTUNION)]


def space_packet(release=False):
 p=INPUT();p.type=1;p.data.ki=KEYBDINPUT(0,0x39,8|(2 if release else 0),0,0)
 return p


def held_space(api,guard,hold_ms=120,clock=time.monotonic_ns,sleep=time.sleep):
 """Guarded algorithm; requires injected API so tests cannot inject real input."""
 if type(hold_ms)is not int or not 80<=hold_ms<=250:raise ValueError('bounded 80..250 ms space hold')
 receipt=dict(method='guarded Win32 SendInput held scan code',scan_code=0x39,hold_ms=hold_ms,input_returned=False,down_submitted=False,up_attempted=False)
 guard();receipt['start_ns']=clock();receipt['start_wall_time_ns']=time.time_ns();released=False
 try:
  # Guard AGAIN immediately before the one global keyboard-down operation.
  guard();down=api.submit(space_packet(False));receipt['down_result']=down
  if down!=1:raise RuntimeError('space down was not submitted')
  receipt['down_submitted']=True;receipt['down_ns']=clock();receipt['down_wall_time_ns']=time.time_ns()
  sleep(hold_ms/1000)
  receipt['up_attempted']=True;up=api.submit(space_packet(True));receipt['up_results']=[up];released=up==1
  if not released:raise RuntimeError('space up was not submitted')
  receipt['up_ns']=clock();receipt['up_wall_time_ns']=time.time_ns();guard();receipt['input_returned']=True
 except Exception as e:receipt['error']=repr(e)
 finally:
  # Release our scan code even if focus/ownership changes after key-down.
  if receipt['down_submitted'] and not released:
   receipt['up_attempted']=True;up=api.submit(space_packet(True));receipt.setdefault('up_results',[]).append(up);released=up==1
  receipt['released']=released;receipt['end_ns']=clock();receipt['end_wall_time_ns']=time.time_ns()
 return receipt


def owned_target_guard(c,hwnd,require_foreground=True):
 from tools.school_native_dialogue_desktop import require_unlocked
 require_unlocked()
 from pathlib import Path
 from tools.school_native_scene import APP,original,word,image_name
 if c.pid not in c.owned.members():raise ValueError('input process no longer belongs to the owned Job')
 pid=W.DWORD();original.ownerpid(hwnd,C.byref(pid))
 if pid.value!=c.pid or original.findwindow(b'Cross Hermit',None)!=hwnd:raise ValueError('input HWND ownership changed')
 main=word(c.get(0x7a4a00,4))
 if not main or original.getprop(hwnd,b'CPP_CLASS')!=main:raise ValueError('original window property/MAIN mismatch')
 name=C.create_unicode_buffer(32768);size=W.DWORD(len(name))
 if not image_name(c.h,0,name,C.byref(size)) or Path(name.value).resolve()!=APP.resolve():raise ValueError('only the exact private source image may receive input')
 if require_foreground and original.ubind('GetForegroundWindow',W.HWND,[])()!=hwnd:raise ValueError('owned original must already have foreground focus')


def focus_target(api,guard,hwnd):
 """Activate only the guarded target; never attach a foreign input queue."""
 guard();r=dict(hwnd=hwnd,before=api.foreground(),operations=[])
 if r['before']!=hwnd:
  guard();r['operations'].append(dict(name='SetForegroundWindow',result=bool(api.foreground_window(hwnd))))
 r['after']=api.foreground();guard()
 if r['after']!=hwnd:raise ValueError('owned window activation did not reach actual foreground')
 return r


def focus_owned_window(c,hwnd):
 from tools.school_native_scene import original
 class Api:
  foreground=staticmethod(original.ubind('GetForegroundWindow',W.HWND,[]))
  foreground_window=staticmethod(original.ubind('SetForegroundWindow',W.BOOL,[W.HWND]))
 return focus_target(Api(),lambda:owned_target_guard(c,hwnd,False),hwnd)


def owned_held_space(c,hwnd,hold_ms=120):
 """Production entry for explicitly authorized --held-input runs."""
 from tools.school_native_scene import APP,original
 def guard():owned_target_guard(c,hwnd)
 class Api:
  def __init__(self):self.send=original.ubind('SendInput',W.UINT,[W.UINT,C.POINTER(INPUT),C.c_int])
  def submit(self,packet):return self.send(1,C.byref(packet),C.sizeof(INPUT))
 receipt=held_space(Api(),guard,hold_ms)
 receipt.update(hwnd=hwnd,pid=c.pid,process_image=str(APP.resolve()),target='exact owned foreground original window',existing_process_memory_written=False)
 return receipt
