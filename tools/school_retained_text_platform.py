"""Real process-owned GDI calls for naturally continued original text code."""
import ctypes as C,struct,hashlib
from ctypes import wintypes as W
from tools.school_gdi_platform import WindowsGDI
from tools.school_retained_rendering import MappedPlatform

class RetainedTextGDI(WindowsGDI):
 def __init__(self):
  super().__init__();self.user=C.WinDLL('user32',use_last_error=True)
  self.user.GetDC.argtypes=[W.HWND];self.user.GetDC.restype=W.HDC
  self.user.ReleaseDC.argtypes=[W.HWND,W.HDC];self.user.ReleaseDC.restype=C.c_int
  self.k.lstrlenA.argtypes=[C.c_char_p];self.k.lstrlenA.restype=C.c_int
  self.screen=None;self.screen_native=None;self.trace=[];self.cleanup=None;self.dib_guest={}
 def screen_dc(self):
  if self.screen is not None:raise ValueError('screen DC acquired once by original constructor')
  self.screen_native=self.user.GetDC(None);self.screen=self.handle(self.screen_native);self.dcs.add(self.screen);self.selections[self.screen]={}
  self.trace.append(dict(name='GetDC',args=[0],result=self.screen,native_result=self.screen_native,thread=int(self.k.GetCurrentThreadId()),ACP=self.acp));return self.screen
 def close(self):
  if self.closed:return self.cleanup
  released=None
  if self.screen is not None:
   for old in self.selections.pop(self.screen).values():
    if not self.g.SelectObject(self.screen,old):raise RuntimeError('restore actual screen selections')
   self.dcs.remove(self.screen);released=int(self.user.ReleaseDC(None,self.screen_native))
   if released!=1:raise RuntimeError('release original borrowed screen DC')
  self.cleanup=dict(super().close(),screen_ReleaseDC=released);return self.cleanup
 def invoke(self,e,name,args):
  extra={};outputs=[]
  def put(at,raw):e.uc.mem_write(at,raw);outputs.append(dict(pointer=at,hex=raw.hex()))
  def text(p,n=None):
   if n is not None:
    if not 0<n<=254:raise ValueError('bounded original ANSI text')
    return bytes(e.uc.mem_read(p,n))
   b=bytearray()
   for i in range(255):
    c=bytes(e.uc.mem_read(p+i,1))
    if c==b'\0':return bytes(b)
    b+=c
   raise ValueError('terminated original ANSI string')
  if name=='CreateFontA':result=self.font(args[:-1],text(args[-1]));extra['face_hex']=text(args[-1]).hex()
  elif name=='lstrlenA':result=int(self.k.lstrlenA(text(args[0])))
  elif name=='SelectObject':result=self.select(*args)
  elif name=='GetTextExtentPoint32A':
   raw=text(args[1],args[2]);size,face=self.measure(args[0],raw);put(args[3],struct.pack('<2i',*size));result=1;extra.update(size=size,face=face,text_hex=raw.hex())
  elif name=='CreateCompatibleDC':
   if args!=[0]:raise ValueError('source private DC input')
   result=self.dc()
  elif name=='CreateDIBSection':
   if args[2]!=0 or args[4:]!=[0,0]:raise ValueError('source DIB ownership inputs')
   header=bytes(e.uc.mem_read(args[1],40));result=self.dib(args[0],header)
   obj=self.bitmaps[result];guest=e.bridge.space.guest('textGDI',obj['pointer']);self.dib_guest[result]=guest
   e.map_missing(guest,obj['bytes']);put(args[3],struct.pack('<I',guest))
   extra.update(header_hex=header.hex(),guest_bits=guest,bytes=obj['bytes'])
  elif name=='GetStockObject':result=self.handle(self.g.GetStockObject(*args))
  elif name=='TextOutA':
   raw=text(args[3],args[4]);result=int(self.g.TextOutA(*args[:3],raw,args[4]));extra['text_hex']=raw.hex()
   if not result:raise RuntimeError('actual TextOutA failed')
  elif name=='DeleteObject':result=self.delete_object(*args)
  elif name=='DeleteDC':result=self.delete_dc(*args)
  elif name in ('SetMapMode','PatBlt','SetBkMode','SetBkColor','SetTextAlign','SetTextColor'):
   if args[0] not in self.dcs:raise ValueError('source owned GDI DC')
   result=int(getattr(self.g,name)(*args))
   if result==-1 or name in ('SetMapMode','PatBlt','SetBkMode') and not result:raise RuntimeError('actual GDI state call failed')
  else:raise ValueError('unimplemented actual GDI API '+name)
  # The source consumes the actual DIB after rasterization, without a helper
  # substituting a pixel converter or changing its original registers.
  for bitmap,guest in self.dib_guest.items():
   if bitmap in self.bitmaps:put(guest,self.raster(bitmap))
  row=dict(name=name,args=args,result=result,memory_outputs=outputs,**extra);self.trace.append(row);return result,row

class StartupGDI(MappedPlatform):
 def __init__(self,platform,space,text):super().__init__(platform,space,'GDI');self.text=text
 def request(self,op,**request):
  if op=='GetDC':
   # The historical atlas helper owns a separate auxiliary DC for its cache
   # protocol. The original owner receives the real DC of the text process.
   auxiliary=super().request(op,**request)
   result=self.text.screen_dc()
   return dict(auxiliary,result=result)
  return super().request(op,**request)
