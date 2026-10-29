// Owned live x86 Direct3D8 bridge. External objects remain in this process.
using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.InteropServices;
using System.Security.Cryptography;
using System.Text;
using System.Web.Script.Serialization;

class TerminalPortraitD3D8Bridge {
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
 class Resource { public IntPtr Ptr;public Locked Storage;public bool Locked;public int Width,Height; }
 static IntPtr factory,device,window;static long sequence;static int issued;
 static Dictionary<uint,Resource> resources=new Dictionary<uint,Resource>();
 static List<uint> order=new List<uint>();static HashSet<uint> retired=new HashSet<uint>();
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
 static Resource Owned(Dictionary<string,object> r) {
  uint key=Number(r,"pointer");Resource t;
  if(!resources.TryGetValue(key,out t))throw new ArgumentException("foreign or stale texture");return t;
 }
 static Dictionary<string,object> Cleanup() {
  var c=new Dictionary<string,object>();var releases=new List<object>();bool ok=true;
  for(int i=order.Count-1;i>=0;i--) {
   uint key=order[i];Resource t=resources[key];int un=0;
   if(t.Locked){un=Method<Unlock>(t.Ptr,17)(t.Ptr,0);t.Locked=false;if(un<0)ok=false;}
   uint count=Method<Release>(t.Ptr,2)(t.Ptr);if(count!=0)ok=false;
   releases.Add(new {pointer=key,unlock_hr=un,count=count});retired.Add(key);
  }
  resources.Clear();order.Clear();c["texture_releases"]=releases;
  if(device!=IntPtr.Zero){uint n=Method<Release>(device,2)(device);c["device_release_count"]=n;if(n!=0)ok=false;device=IntPtr.Zero;}
  if(factory!=IntPtr.Zero){uint n=Method<Release>(factory,2)(factory);c["factory_release_count"]=n;if(n!=0)ok=false;factory=IntPtr.Zero;}
  if(window!=IntPtr.Zero){bool n=DestroyWindow(window);c["window_destroyed"]=n;if(!n)ok=false;window=IntPtr.Zero;}
  c["all_owned_resources_released"]=ok;return c;
 }
 static object Dispatch(Dictionary<string,object> r) {
  string op=(string)r["op"];
  if(op=="create") {
   Keys(r,"id","op","width","height","levels","usage","format","pool");
   if(resources.Count>=11 || issued>=32)throw new ArgumentException("bounded multi texture capacity");
   uint w=Number(r,"width"),h=Number(r,"height");
   if(w<1||w>1024||h<1||!(h<=256||((w==256||w==512)&&h==512))||(w&(w-1))!=0||(h&(h-1))!=0||Number(r,"levels")!=1||Number(r,"usage")!=0||Number(r,"format")!=25||Number(r,"pool")!=1)throw new ArgumentException("exact bounded original texture request");
   IntPtr ptr;int hr=Method<CreateTexture>(device,20)(device,w,h,1,0,25,1,out ptr);
   if(hr<0){if(ptr!=IntPtr.Zero)Method<Release>(ptr,2)(ptr);HR(hr,"CreateTexture");}
   if(ptr==IntPtr.Zero)throw new InvalidOperationException("missing actual texture");
   uint key=unchecked((uint)ptr.ToInt32());
   if(resources.ContainsKey(key)){Method<Release>(ptr,2)(ptr);throw new ArgumentException("duplicate live texture address");}
   resources.Add(key,new Resource{Ptr=ptr,Width=(int)w,Height=(int)h});order.Add(key);issued++;
   return new {hr=hr,texture=Identity(ptr,new int[]{2,14,16,17})};
  }
  if(op=="close"){Keys(r,"id","op");return Cleanup();}
  if(op=="describe") {
   Keys(r,"id","op","pointer");Resource t=Owned(r);Desc d;int hr=Method<LevelDesc>(t.Ptr,14)(t.Ptr,0,out d);HR(hr,"GetLevelDesc");
   IntPtr p=Marshal.AllocHGlobal(32);byte[] bytes=new byte[32];try{Marshal.StructureToPtr(d,p,false);Marshal.Copy(p,bytes,0,32);}finally{Marshal.FreeHGlobal(p);}
   return new {hr=hr,hex=Hex(bytes),width=d.Width,height=d.Height,size=d.Size};
  }
  if(op=="lock") {
   Keys(r,"id","op","pointer","flags");Resource t=Owned(r);uint flags=Number(r,"flags");if(t.Locked || flags!=0x800)throw new ArgumentException("original unlocked NO_SYSLOCK texture required");
   int hr=Method<Lock>(t.Ptr,16)(t.Ptr,0,out t.Storage,IntPtr.Zero,flags);HR(hr,"LockRect");t.Locked=true;ReadRows(t.Storage,t.Width,t.Height);
   byte[] bytes=new byte[t.Storage.Pitch*t.Height];Marshal.Copy(t.Storage.Bits,bytes,0,bytes.Length);
   return new {hr=hr,pitch=t.Storage.Pitch,bits=unchecked((uint)t.Storage.Bits.ToInt32()),hex=Hex(bytes)};
  }
  if(op=="unlock") {
   Keys(r,"id","op","pointer","hex");Resource t=Owned(r);if(!t.Locked)throw new ArgumentException("live locked texture required");byte[] bytes=ParseHex((string)r["hex"]);
   if(bytes.Length!=t.Storage.Pitch*t.Height)throw new ArgumentException("exact complete locked buffer required");Marshal.Copy(bytes,0,t.Storage.Bits,bytes.Length);
   int hr=Method<Unlock>(t.Ptr,17)(t.Ptr,0);HR(hr,"UnlockRect");t.Locked=false;return new {hr=hr,uploaded_sha256=Hash(bytes)};
  }
  if(op=="readback") {
   Keys(r,"id","op","pointer");Resource t=Owned(r);if(t.Locked)throw new ArgumentException("unlocked texture required");Locked p;int hr=Method<Lock>(t.Ptr,16)(t.Ptr,0,out p,IntPtr.Zero,16);HR(hr,"read LockRect");t.Storage=p;t.Locked=true;ReadRows(p,t.Width,t.Height);
   byte[] bytes=new byte[p.Pitch*t.Height];Marshal.Copy(p.Bits,bytes,0,bytes.Length);int un=Method<Unlock>(t.Ptr,17)(t.Ptr,0);HR(un,"read UnlockRect");t.Locked=false;
   return new {hr=hr,unlock_hr=un,pitch=p.Pitch,hex=Hex(bytes),sha256=Hash(bytes)};
  }
  if(op=="release") {
   Keys(r,"id","op","pointer");Resource t=Owned(r);if(t.Locked)throw new ArgumentException("unlocked texture required");uint key=Number(r,"pointer");uint count=Method<Release>(t.Ptr,2)(t.Ptr);
   resources.Remove(key);order.Remove(key);retired.Add(key);return new {count=count};
  }
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
   Emit(new {ok=true,id=0,hello=new {pointer_bytes=4,sdk=220,max_textures=11,max_creates=32,image_size=new int[]{512,512},device=Identity(device,new int[]{20}),factory=Identity(factory,new int[]{15}),attempts=attempts,window_visible=false,window_size=new int[]{256,256},runtime_path=dll,runtime_sha256=Hash(File.ReadAllBytes(dll))}});
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
