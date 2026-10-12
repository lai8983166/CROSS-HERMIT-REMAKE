// Owned live x86 Direct3D8 bridge. External objects remain in this process.
using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.InteropServices;
using System.Security.Cryptography;
using System.Text;
using System.Web.Script.Serialization;

class SchoolD3D8Bridge {
 [DllImport("d3d8.dll",CallingConvention=CallingConvention.StdCall)] static extern IntPtr Direct3DCreate8(uint sdk);
 [DllImport("user32.dll",CharSet=CharSet.Unicode,SetLastError=true)] static extern IntPtr CreateWindowExW(uint ex,string cls,string title,uint style,int x,int y,int w,int h,IntPtr parent,IntPtr menu,IntPtr instance,IntPtr param);
 [DllImport("user32.dll")] static extern bool DestroyWindow(IntPtr hwnd);
 [DllImport("user32.dll")] static extern bool IsWindowVisible(IntPtr hwnd);
 [DllImport("kernel32.dll",CharSet=CharSet.Unicode)] static extern IntPtr GetModuleHandleW(string name);
 [DllImport("kernel32.dll",CharSet=CharSet.Unicode)] static extern uint GetModuleFileNameW(IntPtr module,StringBuilder name,int count);
 [StructLayout(LayoutKind.Sequential)] struct Present {public uint Width,Height,Format,Count,Multisample,Swap;public IntPtr Window;public int Windowed,AutoDepth;public uint DepthFormat,Flags,Refresh,Interval;}
 [StructLayout(LayoutKind.Sequential)] struct Mode {public uint Width,Height,Refresh,Format;}
 [StructLayout(LayoutKind.Sequential)] struct Desc {public uint Format,Type,Usage,Pool,Size,Multisample,Width,Height;}
 [StructLayout(LayoutKind.Sequential)] struct Locked {public int Pitch;public IntPtr Bits;}
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] delegate uint Release(IntPtr self);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] delegate int DisplayMode(IntPtr self,uint adapter,out Mode mode);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] delegate int CreateDevice(IntPtr self,uint adapter,uint type,IntPtr window,uint flags,ref Present p,out IntPtr device);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] delegate int CreateTexture(IntPtr self,uint w,uint h,uint levels,uint usage,uint format,uint pool,out IntPtr texture);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] delegate int LevelDesc(IntPtr self,uint level,out Desc desc);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] delegate int Lock(IntPtr self,uint level,out Locked locked,IntPtr rect,uint flags);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] delegate int Unlock(IntPtr self,uint level);
 static T Method<T>(IntPtr obj,int index) where T:class {
  if(obj==IntPtr.Zero)throw new InvalidOperationException("null owned COM object");
  IntPtr table=Marshal.ReadIntPtr(obj),fn=Marshal.ReadIntPtr(table,index*4);
  if(table==IntPtr.Zero || fn==IntPtr.Zero)throw new InvalidOperationException("null COM method");
  return Marshal.GetDelegateForFunctionPointer(fn,typeof(T)) as T;
 }
 static string Pointer(IntPtr value){return "0x"+unchecked((uint)value.ToInt32()).ToString("x8");}
 static string Hex(byte[] bytes){return BitConverter.ToString(bytes).Replace("-","").ToLowerInvariant();}
 static string Hash(byte[] bytes){using(SHA256 h=SHA256.Create())return Hex(h.ComputeHash(bytes));}
 static void HR(int hr,string name){if(hr<0)throw new InvalidOperationException(name+" HRESULT 0x"+unchecked((uint)hr).ToString("x8"));}
 static byte[] ReadRows(Locked p,int width,int height) {
  if(p.Bits==IntPtr.Zero || p.Pitch<width*2 || p.Pitch>4096 || (p.Pitch&1)!=0)throw new InvalidOperationException("bounded real lock pitch");
  byte[] result=new byte[width*height*2];
  for(int y=0;y<height;y++)Marshal.Copy(IntPtr.Add(p.Bits,y*p.Pitch),result,y*width*2,width*2);
  return result;
 }
 static IntPtr factory,device,texture,window;static Locked storage;static bool locked;static int width,height;static long sequence;
 static JavaScriptSerializer serializer=new JavaScriptSerializer{MaxJsonLength=3*1024*1024};
 static uint Number(Dictionary<string,object> r,string name) {
  object v=r[name];if(!(v is int) && !(v is long))throw new ArgumentException("integer "+name);
  long n=Convert.ToInt64(v);if(n<0 || n>uint.MaxValue)throw new ArgumentException("integer range "+name);return (uint)n;
 }
 static void Keys(Dictionary<string,object> r,params string[] keys) {
  if(r.Count!=keys.Length)throw new ArgumentException("request shape");foreach(string key in keys)if(!r.ContainsKey(key))throw new ArgumentException("request shape");
 }
 static byte[] ParseHex(string s) {
  if(s.Length>2*1024*1024 || (s.Length&1)!=0)throw new ArgumentException("bounded hex");byte[] b=new byte[s.Length/2];
  for(int i=0;i<b.Length;i++)b[i]=Convert.ToByte(s.Substring(i*2,2),16);return b;
 }
 static object Identity(IntPtr obj,int[] methods) {
  if(obj==IntPtr.Zero)throw new InvalidOperationException("dead owned object");IntPtr table=Marshal.ReadIntPtr(obj);if(table==IntPtr.Zero)throw new InvalidOperationException("actual vtable");
  var slots=new Dictionary<string,object>();foreach(int slot in methods)slots[(slot*4).ToString()]=unchecked((uint)Marshal.ReadIntPtr(table,slot*4).ToInt32());
  return new {pointer=unchecked((uint)obj.ToInt32()),vtable=unchecked((uint)table.ToInt32()),methods=slots};
 }
 static void Owned(Dictionary<string,object> r) {
  if(texture==IntPtr.Zero || Number(r,"pointer")!=unchecked((uint)texture.ToInt32()))throw new ArgumentException("foreign or stale texture");
 }
 static Dictionary<string,object> Cleanup() {
  var c=new Dictionary<string,object>();
  if(locked && texture!=IntPtr.Zero){c["unlock_hr"]=Method<Unlock>(texture,17)(texture,0);locked=false;}
  if(texture!=IntPtr.Zero){c["texture_release_count"]=Method<Release>(texture,2)(texture);texture=IntPtr.Zero;}
  if(device!=IntPtr.Zero){c["device_release_count"]=Method<Release>(device,2)(device);device=IntPtr.Zero;}
  if(factory!=IntPtr.Zero){c["factory_release_count"]=Method<Release>(factory,2)(factory);factory=IntPtr.Zero;}
  if(window!=IntPtr.Zero){c["window_destroyed"]=DestroyWindow(window);window=IntPtr.Zero;}
  bool ok=true;foreach(string key in new string[]{"texture_release_count","device_release_count","factory_release_count"})if(c.ContainsKey(key) && (uint)c[key]!=0)ok=false;
  if(c.ContainsKey("window_destroyed") && !(bool)c["window_destroyed"])ok=false;c["all_owned_resources_released"]=ok;return c;
 }
 static object Dispatch(Dictionary<string,object> r) {
  string op=(string)r["op"];
  if(op=="create") {
   Keys(r,"id","op","width","height","levels","usage","format","pool");if(texture!=IntPtr.Zero)throw new ArgumentException("one owned live texture required");
   uint w=Number(r,"width"),h=Number(r,"height");
   if(w<1||w>1024||h<1||h>256||(w&(w-1))!=0||(h&(h-1))!=0||Number(r,"levels")!=1||Number(r,"usage")!=0||Number(r,"format")!=25||Number(r,"pool")!=1)throw new ArgumentException("exact bounded original texture request");
   int hr=Method<CreateTexture>(device,20)(device,w,h,1,0,25,1,out texture);HR(hr,"CreateTexture");width=(int)w;height=(int)h;
   return new {hr=hr,texture=Identity(texture,new int[]{2,14,16,17})};
  }
  if(op=="describe") {
   Keys(r,"id","op","pointer");Owned(r);Desc d;int hr=Method<LevelDesc>(texture,14)(texture,0,out d);HR(hr,"GetLevelDesc");
   IntPtr p=Marshal.AllocHGlobal(32);byte[] bytes=new byte[32];try{Marshal.StructureToPtr(d,p,false);Marshal.Copy(p,bytes,0,32);}finally{Marshal.FreeHGlobal(p);}
   return new {hr=hr,hex=Hex(bytes),width=d.Width,height=d.Height,size=d.Size};
  }
  if(op=="lock") {
   Keys(r,"id","op","pointer","flags");Owned(r);uint flags=Number(r,"flags");if(locked || flags!=0x800)throw new ArgumentException("original unlocked NO_SYSLOCK texture required");
   int hr=Method<Lock>(texture,16)(texture,0,out storage,IntPtr.Zero,flags);HR(hr,"LockRect");locked=true;ReadRows(storage,width,height);
   byte[] bytes=new byte[storage.Pitch*height];Marshal.Copy(storage.Bits,bytes,0,bytes.Length);
   return new {hr=hr,pitch=storage.Pitch,bits=unchecked((uint)storage.Bits.ToInt32()),hex=Hex(bytes)};
  }
  if(op=="unlock") {
   Keys(r,"id","op","pointer","hex");Owned(r);if(!locked)throw new ArgumentException("live locked texture required");byte[] bytes=ParseHex((string)r["hex"]);
   if(bytes.Length!=storage.Pitch*height)throw new ArgumentException("exact complete locked buffer required");Marshal.Copy(bytes,0,storage.Bits,bytes.Length);
   int hr=Method<Unlock>(texture,17)(texture,0);HR(hr,"UnlockRect");locked=false;return new {hr=hr,uploaded_sha256=Hash(bytes)};
  }
  if(op=="readback") {
   Keys(r,"id","op","pointer");Owned(r);if(locked)throw new ArgumentException("unlocked texture required");Locked p;int hr=Method<Lock>(texture,16)(texture,0,out p,IntPtr.Zero,16);HR(hr,"read LockRect");storage=p;locked=true;ReadRows(p,width,height);
   byte[] bytes=new byte[p.Pitch*height];Marshal.Copy(p.Bits,bytes,0,bytes.Length);int un=Method<Unlock>(texture,17)(texture,0);HR(un,"read UnlockRect");locked=false;
   return new {hr=hr,unlock_hr=un,pitch=p.Pitch,hex=Hex(bytes),sha256=Hash(bytes)};
  }
  if(op=="release") {
   Keys(r,"id","op","pointer");Owned(r);if(locked)throw new ArgumentException("unlocked texture required");uint count=Method<Release>(texture,2)(texture);texture=IntPtr.Zero;return new {count=count};
  }
  if(op=="close"){Keys(r,"id","op");return Cleanup();}
  throw new ArgumentException("unsupported operation");
 }
 static void Emit(object r){Console.WriteLine(serializer.Serialize(r));Console.Out.Flush();}
 static int Main() {
  try {
   if(IntPtr.Size!=4 || Marshal.SizeOf(typeof(Present))!=52 || Marshal.SizeOf(typeof(Desc))!=32)throw new InvalidOperationException("x86 ABI required");
   window=CreateWindowExW(0,"STATIC","Cross Hermit live texture audit",0x80000000,0,0,256,256,IntPtr.Zero,IntPtr.Zero,IntPtr.Zero,IntPtr.Zero);
   if(window==IntPtr.Zero || IsWindowVisible(window))throw new InvalidOperationException("hidden window");factory=Direct3DCreate8(220);if(factory==IntPtr.Zero)throw new InvalidOperationException("real factory");
   Mode mode;HR(Method<DisplayMode>(factory,8)(factory,0,out mode),"GetAdapterDisplayMode");int hr=-1;var attempts=new List<object>();
   foreach(uint[] pair in new uint[][]{new uint[]{1,68},new uint[]{1,36},new uint[]{2,68},new uint[]{2,36}}) {
    Present pp=new Present{Width=256,Height=256,Format=mode.Format,Count=1,Swap=1,Window=window,Windowed=1};
    hr=Method<CreateDevice>(factory,15)(factory,0,pair[0],window,pair[1],ref pp,out device);attempts.Add(new {type=pair[0],flags=pair[1],hr=hr});if(hr>=0 && device!=IntPtr.Zero)break;
    if(device!=IntPtr.Zero){Method<Release>(device,2)(device);device=IntPtr.Zero;}
   }
   HR(hr,"CreateDevice");if(device==IntPtr.Zero)throw new InvalidOperationException("live device");
   string dll=Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.Windows),"SysWOW64","d3d8.dll");
   Emit(new {ok=true,id=0,hello=new {pointer_bytes=4,sdk=220,device=Identity(device,new int[]{20}),factory=Identity(factory,new int[]{15}),attempts=attempts,window_visible=false,window_size=new int[]{256,256},runtime_path=dll,runtime_sha256=Hash(File.ReadAllBytes(dll))}});
   string line;while((line=Console.ReadLine())!=null) {
    long id=0;string op="";try {
     if(line.Length>3*1024*1024)throw new ArgumentException("bounded request");var r=serializer.Deserialize<Dictionary<string,object>>(line);id=Number(r,"id");op=(string)r["op"];
     if(id!=sequence+1)throw new ArgumentException("sequence");sequence=id;object result=Dispatch(r);Emit(new {ok=true,id=id,result=result});if(op=="close")break;
    }catch(Exception e){Emit(new {ok=false,id=id,error=e.GetType().Name+": "+e.Message});}
   }
   return 0;
  }catch(Exception e){Emit(new {ok=false,id=0,error=e.GetType().Name+": "+e.Message});return 2;}
  finally{Cleanup();}
 }
}
