"""Owned actual Windows read-only sc004 file APIs with bounded identity."""
import ctypes as C
from ctypes import wintypes as W
from tools.school_character_image_catalog import RESOURCE,RESOURCE_SHA,hashlib

class WindowsImageFile:
 def __init__(self):
  self.k=C.WinDLL('kernel32',use_last_error=True);self.handles=set();self.closed_count=0
  definitions={'CreateFileA':([C.c_char_p,W.DWORD,W.DWORD,C.c_void_p,W.DWORD,W.DWORD,W.HANDLE],W.HANDLE),
   'GetFileSize':([W.HANDLE,C.POINTER(W.DWORD)],W.DWORD),'ReadFile':([W.HANDLE,C.c_void_p,W.DWORD,C.POINTER(W.DWORD),C.c_void_p],W.BOOL),'CloseHandle':([W.HANDLE],W.BOOL)}
  for name,(args,result) in definitions.items():getattr(self.k,name).argtypes=args;getattr(self.k,name).restype=result
 def open(self,flags):
  if flags!=[0x80000000,1,0,3,1,0] or self.handles:raise ValueError('single actual read-only image file')
  h=self.k.CreateFileA(str(RESOURCE.resolve()).encode('ascii'),*flags)
  if not h or h==C.c_void_p(-1).value:raise OSError(C.get_last_error(),'actual image open')
  if h>=0xFFFFFFFF:self.k.CloseHandle(h);raise RuntimeError('actual 32-bit representable file handle')
  self.handles.add(h);return h
 def size(self,h):
  if h not in self.handles:raise ValueError('owned image file size handle')
  n=int(self.k.GetFileSize(h,None))
  if n!=262168:raise ValueError('actual pinned image byte length')
  return n
 def read(self,h,n):
  if h not in self.handles or n!=262168:raise ValueError('owned image read bounds')
  buf=C.create_string_buffer(n);written=W.DWORD()
  if not self.k.ReadFile(h,buf,n,C.byref(written),None) or written.value!=n:raise OSError(C.get_last_error(),'actual image complete read')
  raw=buf.raw
  if hashlib.sha256(raw).hexdigest()!=RESOURCE_SHA:raise ValueError('actual read pinned image identity')
  return raw
 def release(self,h):
  if h not in self.handles:raise ValueError('owned image close handle')
  if not self.k.CloseHandle(h):raise OSError(C.get_last_error(),'actual image close')
  self.handles.remove(h);self.closed_count+=1;return 1
 def close(self):
  for h in list(self.handles):self.release(h)
  return {'actual_handles_closed':self.closed_count,'open_handles':len(self.handles),'all_owned_files_closed':True}
