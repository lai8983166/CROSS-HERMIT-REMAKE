"""Read-only input-desktop preflight; never operate LockApp or a secure desktop."""
import ctypes as C,ctypes.wintypes as W
from pathlib import PureWindowsPath


def classify(input_desktop,observer_desktop,foreground_image):
 image=PureWindowsPath(foreground_image or '').name.casefold()
 if image in ('lockapp.exe','logonui.exe','credentialuibroker.exe'):return 'locked_foreground'
 if not input_desktop or not observer_desktop:return 'input_desktop_unavailable'
 if input_desktop.casefold()!=observer_desktop.casefold():return 'different_input_desktop'
 return 'ready'


def desktop_status():
 u=C.WinDLL('user32',use_last_error=True);k=C.WinDLL('kernel32',use_last_error=True)
 def bind(lib,name,result,args):
  f=getattr(lib,name);f.restype=result;f.argtypes=args;return f
 foreground=bind(u,'GetForegroundWindow',W.HWND,[])();pid=W.DWORD();bind(u,'GetWindowThreadProcessId',W.DWORD,[W.HWND,C.POINTER(W.DWORD)])(foreground,C.byref(pid))
 image=None;ph=bind(k,'OpenProcess',W.HANDLE,[W.DWORD,W.BOOL,W.DWORD])(0x1000,False,pid.value)
 if ph:
  try:
   b=C.create_unicode_buffer(32768);size=W.DWORD(len(b))
   if bind(k,'QueryFullProcessImageNameW',W.BOOL,[W.HANDLE,W.DWORD,W.LPWSTR,C.POINTER(W.DWORD)])(ph,0,b,C.byref(size)):image=b.value
  finally:bind(k,'CloseHandle',W.BOOL,[W.HANDLE])(ph)
 namefn=bind(u,'GetUserObjectInformationW',W.BOOL,[W.HANDLE,C.c_int,W.LPVOID,W.DWORD,C.POINTER(W.DWORD)])
 def name(handle):
  b=C.create_unicode_buffer(512);size=W.DWORD();return b.value if handle and namefn(handle,2,b,C.sizeof(b),C.byref(size)) else None
 tid=bind(k,'GetCurrentThreadId',W.DWORD,[])();observer=name(bind(u,'GetThreadDesktop',W.HANDLE,[W.DWORD])(tid));C.set_last_error(0)
 inp=bind(u,'OpenInputDesktop',W.HANDLE,[W.DWORD,W.BOOL,W.DWORD])(0,False,1);error=C.get_last_error() if not inp else 0;input_name=None
 if inp:
  try:input_name=name(inp)
  finally:bind(u,'CloseDesktop',W.BOOL,[W.HANDLE])(inp)
 reason=classify(input_name,observer,image)
 return dict(schema_version=1,ready=reason=='ready',reason=reason,input_desktop=input_name,observer_desktop=observer,open_input_desktop_error=error,foreground_hwnd=foreground or 0,foreground_pid=pid.value,foreground_image=image,desktop_or_window_state_written=False,input_submitted=False)


def require_unlocked():
 s=desktop_status()
 if not s['ready']:raise RuntimeError('desktop preflight: '+s['reason']+'; user must unlock the interactive desktop')
 return s
