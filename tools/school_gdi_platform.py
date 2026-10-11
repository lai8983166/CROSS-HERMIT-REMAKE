"""Real Windows offscreen GDI adapter; never fabricates handles or metrics."""
import ctypes as C
import os
from ctypes import wintypes as W

class BitmapInfoHeader(C.Structure):
 _fields_=[('size',W.DWORD),('width',W.LONG),('height',W.LONG),('planes',W.WORD),
  ('bits',W.WORD),('compression',W.DWORD),('image_size',W.DWORD),('xppm',W.LONG),
  ('yppm',W.LONG),('used',W.DWORD),('important',W.DWORD)]

class WindowsGDI:
 def __init__(self):
  if os.name!='nt':raise RuntimeError('real Windows GDI required')
  self.g=C.WinDLL('gdi32',use_last_error=True);self.k=C.WinDLL('kernel32',use_last_error=True)
  definitions={
   'CreateFontA':([C.c_int]*5+[W.DWORD]*8+[C.c_char_p],W.HANDLE),
   'CreateCompatibleDC':([W.HDC],W.HDC),'SelectObject':([W.HDC,W.HANDLE],W.HANDLE),
   'GetTextExtentPoint32A':([W.HDC,C.c_char_p,C.c_int,C.POINTER(W.SIZE)],W.BOOL),
   'CreateDIBSection':([W.HDC,C.c_void_p,W.UINT,C.POINTER(C.c_void_p),W.HANDLE,W.DWORD],W.HANDLE),
   'SetMapMode':([W.HDC,C.c_int],C.c_int),'GetStockObject':([C.c_int],W.HANDLE),
   'PatBlt':([W.HDC,C.c_int,C.c_int,C.c_int,C.c_int,W.DWORD],W.BOOL),
   'SetBkMode':([W.HDC,C.c_int],C.c_int),'SetBkColor':([W.HDC,W.DWORD],W.DWORD),
   'SetTextAlign':([W.HDC,W.UINT],W.UINT),'SetTextColor':([W.HDC,W.DWORD],W.DWORD),
   'TextOutA':([W.HDC,C.c_int,C.c_int,C.c_char_p,C.c_int],W.BOOL),
   'GetTextFaceW':([W.HDC,C.c_int,C.c_wchar_p],C.c_int),
   'GetObjectType':([W.HANDLE],W.DWORD),'DeleteObject':([W.HANDLE],W.BOOL),
   'DeleteDC':([W.HDC],W.BOOL),'GdiFlush':([],W.BOOL)}
  for name,(args,result) in definitions.items():
   fn=getattr(self.g,name);fn.argtypes=args;fn.restype=result
  self.fonts=set();self.dcs=set();self.bitmaps={};self.selections={};self.closed=False
  self.k.GetACP.restype=W.UINT;self.acp=int(self.k.GetACP())

 @staticmethod
 def handle(value):
  if not value:raise RuntimeError('GDI nonzero 32-bit handle required')
  value=int(value)
  # Win64 may sign-extend the shared 32-bit GDI handle into HANDLE.
  if value>>32 not in (0,0xFFFFFFFF) or not value&0xFFFFFFFF:raise RuntimeError('GDI nonzero 32-bit handle required')
  return value&0xFFFFFFFF

 @staticmethod
 def string(raw):
  if not isinstance(raw,bytes) or not raw or len(raw)>254 or b'\0' in raw:raise ValueError('bounded nonempty ANSI text required')
  return raw

 def font(self,args,face):
  if self.closed or not isinstance(args,list) or len(args)!=13 or any(type(v)is not int for v in args):raise ValueError('GDI font arguments')
  h=self.handle(self.g.CreateFontA(*args,self.string(face)));self.fonts.add(h);return h

 def dc(self):
  if self.closed:raise RuntimeError('GDI adapter closed')
  h=self.handle(self.g.CreateCompatibleDC(None));self.dcs.add(h);self.selections[h]={};return h

 def select(self,dc,obj):
  if self.closed or dc not in self.dcs:raise ValueError('GDI owned DC')
  old=self.handle(self.g.SelectObject(dc,obj));kind=int(self.g.GetObjectType(obj))
  if not kind:raise RuntimeError('GDI selected object type')
  self.selections[dc].setdefault(kind,old);return old

 def measure(self,dc,raw):
  if self.closed or dc not in self.dcs:raise ValueError('GDI owned measurement DC')
  raw=self.string(raw);size=W.SIZE()
  if not self.g.GetTextExtentPoint32A(dc,raw,len(raw),C.byref(size)) or size.cx<=0 or size.cy<=0:raise RuntimeError('real GDI measurement failed')
  face=C.create_unicode_buffer(128)
  if not self.g.GetTextFaceW(dc,128,face):raise RuntimeError('real selected font name failed')
  return [int(size.cx),int(size.cy)],face.value

 def dib(self,dc,header):
  if self.closed or dc not in self.dcs or not isinstance(header,bytes) or len(header)!=40:raise ValueError('GDI DIB header')
  h=BitmapInfoHeader.from_buffer_copy(header)
  if (h.size,h.planes,h.bits,h.compression)!=(40,1,32,0) or not 0<h.width<=1024 or not -256<=h.height<0:raise ValueError('GDI bounded top-down 32-bit DIB')
  pointer=C.c_void_p();info=C.create_string_buffer(header+b'\0'*4)
  obj=self.handle(self.g.CreateDIBSection(dc,info,0,C.byref(pointer),None,0))
  if not pointer.value:
   self.g.DeleteObject(obj);raise RuntimeError('GDI missing DIB memory')
  self.bitmaps[obj]={'pointer':pointer.value,'bytes':h.width*(-h.height)*4,'size':[h.width,-h.height]};return obj

 def raster(self,obj):
  if self.closed or obj not in self.bitmaps:raise ValueError('GDI owned DIB')
  if not self.g.GdiFlush():raise RuntimeError('GDI flush failed')
  b=self.bitmaps[obj];return C.string_at(b['pointer'],b['bytes'])

 def close(self):
  if self.closed:return {'already_closed':True,'all_resources_released':True}
  errors=[]
  for dc,objects in self.selections.items():
   for old in objects.values():
    if not self.g.SelectObject(dc,old):errors.append('restore selection')
  counts={'fonts':len(self.fonts),'bitmaps':len(self.bitmaps),'dcs':len(self.dcs)}
  for obj in [*self.bitmaps,*self.fonts]:
   if not self.g.DeleteObject(obj):errors.append('DeleteObject')
  for dc in self.dcs:
   if not self.g.DeleteDC(dc):errors.append('DeleteDC')
  self.closed=True
  if errors:raise RuntimeError('GDI cleanup failed: '+','.join(errors))
  return {**counts,'all_resources_released':True}

 def __enter__(self):return self
 def __exit__(self,*ignored):self.close()
