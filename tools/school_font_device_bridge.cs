// Forked owned x86 startup and three original font-cache device calls. No drawing/Present.
using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.InteropServices;
using System.Security.Cryptography;
using System.Text;
using System.Web.Script.Serialization;

class SchoolFontDeviceBridge {
 [DllImport("d3d8.dll",CallingConvention=CallingConvention.StdCall)] static extern IntPtr Direct3DCreate8(uint sdk);
 [DllImport("user32.dll",CharSet=CharSet.Unicode)] static extern IntPtr CreateWindowExW(uint ex,string cls,string title,uint style,int x,int y,int w,int h,IntPtr parent,IntPtr menu,IntPtr instance,IntPtr param);
 [DllImport("user32.dll")] static extern bool DestroyWindow(IntPtr window);
 [DllImport("user32.dll")] static extern bool IsWindowVisible(IntPtr window);
 [DllImport("kernel32.dll",CharSet=CharSet.Unicode)] static extern IntPtr GetModuleHandleW(string name);
 [DllImport("kernel32.dll",CharSet=CharSet.Unicode)] static extern uint GetModuleFileNameW(IntPtr module,StringBuilder name,int count);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] delegate uint Release(IntPtr self);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] delegate int DisplayMode(IntPtr self,uint adapter,IntPtr output);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] delegate int CreateDevice(IntPtr self,uint adapter,uint type,IntPtr window,uint flags,IntPtr pp,out IntPtr device);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] delegate int GetCaps(IntPtr self,IntPtr output);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] delegate int BackBuffer(IntPtr self,uint index,uint type,out IntPtr surface);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] delegate int GetDesc(IntPtr self,IntPtr output);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] delegate int CheckFormat(IntPtr self,uint adapter,uint type,uint adapterFormat,uint usage,uint resourceType,uint format);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] delegate int SetViewport(IntPtr self,IntPtr viewport);
 static IntPtr window,factory,device,surface;
 static uint width,height,displayFormat;static int attempt,cacheStep,extraReferences;static long sequence;
 static JavaScriptSerializer json=new JavaScriptSerializer{MaxJsonLength=1024*1024};
 static T Method<T>(IntPtr obj,int index) where T:class {
  if(obj==IntPtr.Zero)throw new ArgumentException("live owned COM object required");
  return Marshal.GetDelegateForFunctionPointer(Marshal.ReadIntPtr(Marshal.ReadIntPtr(obj),index*4),typeof(T)) as T;
 }
 static uint Pointer(IntPtr p){return unchecked((uint)p.ToInt32());}
 static string Hex(byte[] b){return BitConverter.ToString(b).Replace("-","").ToLowerInvariant();}
 static string Hash(byte[] b){using(SHA256 h=SHA256.Create())return Hex(h.ComputeHash(b));}
 static byte[] Bytes(IntPtr p,int count){byte[] b=new byte[count];Marshal.Copy(p,b,0,count);return b;}
 static byte[] Parse(string value,int count) {
  if(value.Length!=count*2)throw new ArgumentException("exact raw buffer size required");
  byte[] b=new byte[count];for(int i=0;i<count;i++)b[i]=Convert.ToByte(value.Substring(i*2,2),16);return b;
 }
 static uint Number(Dictionary<string,object> r,string key) {
  object o=r[key];if(!(o is int) && !(o is long))throw new ArgumentException("integer required");
  long n=Convert.ToInt64(o);if(n<0 || n>uint.MaxValue)throw new ArgumentException("uint32 required");return (uint)n;
 }
 static void Keys(Dictionary<string,object> r,params string[] keys) {
  if(r.Count!=keys.Length)throw new ArgumentException("request shape");foreach(string k in keys)if(!r.ContainsKey(k))throw new ArgumentException("request shape");
 }
 static void Owned(Dictionary<string,object> r,IntPtr p) {
  if(p==IntPtr.Zero || Number(r,"pointer")!=Pointer(p))throw new ArgumentException("foreign or expired object");
 }
 static object Identity(IntPtr p,params int[] slots) {
  if(p==IntPtr.Zero)return null;IntPtr table=Marshal.ReadIntPtr(p);var methods=new Dictionary<string,object>();
  foreach(int slot in slots)methods[(slot*4).ToString()]=Pointer(Marshal.ReadIntPtr(table,slot*4));
  return new {pointer=Pointer(p),vtable=Pointer(table),methods=methods};
 }
 static object RawQuery(IntPtr obj,int count,string kind) {
  IntPtr p=Marshal.AllocHGlobal(count);
  try {Marshal.Copy(new byte[count],0,p,count);int hr;
   if(kind=="mode")hr=Method<DisplayMode>(obj,8)(obj,0,p);
   else if(kind=="caps")hr=Method<GetCaps>(obj,7)(obj,p);
   else hr=Method<GetDesc>(obj,8)(obj,p);
   byte[] b=Bytes(p,count);if(kind=="mode" && hr>=0)displayFormat=BitConverter.ToUInt32(b,12);
   return new {hr=hr,hex=Hex(b)};
  }finally{Marshal.FreeHGlobal(p);}
 }
 static Dictionary<string,object> Cleanup() {
  var r=new Dictionary<string,object>();
  if(extraReferences>0){var counts=new List<uint>();while(extraReferences>0){counts.Add(Method<Release>(device,2)(device));extraReferences--;}r["extra_reference_release_counts"]=counts;}
  if(surface!=IntPtr.Zero){r["surface_release_count"]=Method<Release>(surface,2)(surface);surface=IntPtr.Zero;}
  if(device!=IntPtr.Zero){r["device_release_count"]=Method<Release>(device,2)(device);device=IntPtr.Zero;}
  if(factory!=IntPtr.Zero){r["factory_release_count"]=Method<Release>(factory,2)(factory);factory=IntPtr.Zero;}
  if(window!=IntPtr.Zero){r["window_destroyed"]=DestroyWindow(window);window=IntPtr.Zero;}
  bool ok=true;foreach(string key in new string[]{"device_release_count","factory_release_count"})if(r.ContainsKey(key) && (uint)r[key]!=0)ok=false;
  if(r.ContainsKey("window_destroyed") && !(bool)r["window_destroyed"])ok=false;
  r["all_owned_resources_released"]=ok;return r;
 }
 static object Dispatch(Dictionary<string,object> r) {
  string op=(string)r["op"];
  if(op=="factory") {
   Keys(r,"id","op","sdk");if(factory!=IntPtr.Zero || Number(r,"sdk")!=220)throw new ArgumentException("single original factory SDK required");
   factory=Direct3DCreate8(220);if(factory==IntPtr.Zero)throw new InvalidOperationException("real factory unavailable");
   var path=new StringBuilder(1024);if(GetModuleFileNameW(GetModuleHandleW("d3d8.dll"),path,path.Capacity)==0)throw new InvalidOperationException("loaded runtime identity");
   string physical=Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.Windows),"SysWOW64","d3d8.dll");
   string sha=Hash(File.ReadAllBytes(path.ToString()));if(sha!=Hash(File.ReadAllBytes(physical)))throw new InvalidOperationException("WOW64 runtime identity");
   return new {factory=Identity(factory,8,10,15),runtime_path=physical,runtime_sha256=sha};
  }
  if(op=="display_mode") {Keys(r,"id","op","pointer");Owned(r,factory);return RawQuery(factory,16,"mode");}
  if(op=="create_device") {
   Keys(r,"id","op","pointer","type","flags","presentation_hex");Owned(r,factory);
   if(device!=IntPtr.Zero || attempt>=4)throw new ArgumentException("bounded device attempts");
   uint type=Number(r,"type"),flags=Number(r,"flags");uint[][] pairs={new uint[]{1,68},new uint[]{1,36},new uint[]{2,68},new uint[]{2,36}};
   if(type!=pairs[attempt][0] || flags!=pairs[attempt][1])throw new ArgumentException("original attempt ordering");
   byte[] b=Parse((string)r["presentation_hex"],52);uint[] expected={width,height,displayFormat,1,0,1,Pointer(window),1,0,0,0,0,0};
   for(int i=0;i<13;i++)if(BitConverter.ToUInt32(b,i*4)!=expected[i])throw new ArgumentException("original windowed presentation required");
   IntPtr p=Marshal.AllocHGlobal(52);try {
    Marshal.Copy(b,0,p,52);attempt++;int hr=Method<CreateDevice>(factory,15)(factory,0,type,window,flags,p,out device);
    if(hr<0 && device!=IntPtr.Zero)throw new InvalidOperationException("unexpected device on failed call");
    return new {hr=hr,presentation_hex=Hex(Bytes(p,52)),device=Identity(device,1,7,9,16,40)};
   }finally{Marshal.FreeHGlobal(p);}
  }
  if(op=="caps") {Keys(r,"id","op","pointer");Owned(r,device);return RawQuery(device,212,"caps");}
  if(op=="backbuffer") {
   Keys(r,"id","op","pointer");Owned(r,device);if(surface!=IntPtr.Zero)throw new ArgumentException("one surface reference");
   int hr=Method<BackBuffer>(device,16)(device,0,0,out surface);return new {hr=hr,surface=Identity(surface,2,8)};
  }
  if(op=="describe_surface") {Keys(r,"id","op","pointer");Owned(r,surface);return RawQuery(surface,32,"desc");}
  if(op=="release_surface") {
   Keys(r,"id","op","pointer");Owned(r,surface);uint count=Method<Release>(surface,2)(surface);surface=IntPtr.Zero;return new {count=count};
  }
  if(op=="check_format") {
   Keys(r,"id","op","pointer","adapter","type","adapter_format","format");Owned(r,factory);
   uint adapter=Number(r,"adapter"),type=Number(r,"type"),format=Number(r,"format"),af=Number(r,"adapter_format");
   uint[] allowed={25,24,23,21,20,22,26,27,28,29,30,40,41,50,51,52,60,61,62,63,64,65};
   if(adapter!=0 || (type!=1 && type!=2) || af!=displayFormat || Array.IndexOf(allowed,format)<0)throw new ArgumentException("bounded original format query");
   int hr=Method<CheckFormat>(factory,10)(factory,adapter,type,af,1,1,format);return new {hr=hr};
  }
  if(op=="viewport") {
   Keys(r,"id","op","pointer","hex");Owned(r,device);byte[] b=Parse((string)r["hex"],24);uint[] expected={0,0,width,height,0,0x3f800000};
   for(int i=0;i<6;i++)if(BitConverter.ToUInt32(b,i*4)!=expected[i])throw new ArgumentException("original viewport");
   IntPtr p=Marshal.AllocHGlobal(24);try{Marshal.Copy(b,0,p,24);int hr=Method<SetViewport>(device,40)(device,p);return new {hr=hr};}finally{Marshal.FreeHGlobal(p);}
  }
  if(op=="cache_addref") {
   Keys(r,"id","op","pointer");Owned(r,device);if(cacheStep!=0)throw new ArgumentException("one original cache reference");
   uint count=Method<Release>(device,1)(device);extraReferences++;cacheStep=1;return new {count=count};
  }
  if(op=="cache_caps") {
   Keys(r,"id","op","pointer");Owned(r,device);if(cacheStep!=1)throw new ArgumentException("cache query sequence");
   object result=RawQuery(device,212,"caps");cacheStep=2;return result;
  }
  if(op=="cache_creation") {
   Keys(r,"id","op","pointer");Owned(r,device);if(cacheStep!=2)throw new ArgumentException("cache query sequence");
   IntPtr p=Marshal.AllocHGlobal(16);try {
    Marshal.Copy(new byte[16],0,p,16);int hr=Method<GetCaps>(device,9)(device,p);cacheStep=3;
    return new {hr=hr,hex=Hex(Bytes(p,16))};
   }finally{Marshal.FreeHGlobal(p);}
  }
  if(op=="close"){Keys(r,"id","op");return Cleanup();}
  throw new ArgumentException("unsupported device startup operation");
 }
 static void Emit(object r){Console.WriteLine(json.Serialize(r));Console.Out.Flush();}
 static int Main(string[] args) {
  try {
   if(IntPtr.Size!=4 || args.Length!=2 || !uint.TryParse(args[0],out width) || !uint.TryParse(args[1],out height) || width<64 || width>1280 || height<64 || height>800)throw new ArgumentException("bounded x86 window dimensions");
   window=CreateWindowExW(0,"STATIC","Cross Hermit native device startup audit",0x80000000,0,0,(int)width,(int)height,IntPtr.Zero,IntPtr.Zero,IntPtr.Zero,IntPtr.Zero);
   if(window==IntPtr.Zero || IsWindowVisible(window))throw new InvalidOperationException("hidden owned window");
   Emit(new {ok=true,id=0,hello=new {pointer_bytes=4,window=Pointer(window),window_visible=false,width=width,height=height}});
   string line;while((line=Console.ReadLine())!=null) {
    long id=0;string op="";
    try {
     if(line.Length>1024*1024)throw new ArgumentException("bounded request");var r=json.Deserialize<Dictionary<string,object>>(line);id=Number(r,"id");op=(string)r["op"];
     if(id!=sequence+1)throw new ArgumentException("request sequence");sequence=id;
     object result=Dispatch(r);Emit(new {ok=true,id=id,result=result});if(op=="close")break;
    }catch(Exception e){Emit(new {ok=false,id=id,error=e.GetType().Name+": "+e.Message});}
   }
   return 0;
  }catch(Exception e){Emit(new {ok=false,id=0,error=e.GetType().Name+": "+e.Message});return 2;}
  finally{Cleanup();}
 }
}
