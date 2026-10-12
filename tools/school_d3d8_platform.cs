// Real x86 Direct3D8 resource probe. No original CPU or renderer state is patched.
using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.InteropServices;
using System.Security.Cryptography;
using System.Text;
using System.Web.Script.Serialization;

class SchoolD3D8Platform {
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
 static int Main(string[] args) {
  var report=new Dictionary<string,object>();var trace=new List<object>();var cleanup=new Dictionary<string,object>();
  report["schema_version"]=1;report["scope"]="declared_real_host_x86_Direct3D8_resource_probe_not_native_VM_continuation";
  report["platform_calls_started"]=false;report["native_renderer_patched"]=false;report["original_GPU_executed"]=false;
  report["native_VM_continuation_executed"]=false;report["drawing_or_present_executed"]=false;report["calls"]=trace;report["cleanup"]=cleanup;
  IntPtr factory=IntPtr.Zero,device=IntPtr.Zero,texture=IntPtr.Zero,window=IntPtr.Zero;bool locked=false;string output=null;int exit=2;
  try {
   if(args.Length!=4)throw new ArgumentException("input, power-of-two width, height, new output path required");
   int width,height;
   if(!int.TryParse(args[1],out width)||!int.TryParse(args[2],out height)||width<1||width>1024||height<1||height>256||(width&(width-1))!=0||(height&(height-1))!=0)throw new ArgumentException("bounded texture dimensions");
   if(File.Exists(args[3]) || Directory.Exists(args[3]) || !Directory.Exists(Path.GetDirectoryName(Path.GetFullPath(args[3]))))throw new ArgumentException("new output file in existing directory required");
   output=args[3];if(new FileInfo(args[0]).Length!=2*width*height)throw new ArgumentException("exact16-bit input size required");
   byte[] input=File.ReadAllBytes(args[0]);if(input.Length!=2*width*height)throw new ArgumentException("exact16-bit input size required");
   if(IntPtr.Size!=4 || Marshal.SizeOf(typeof(Present))!=52 || Marshal.SizeOf(typeof(Desc))!=32 || Marshal.SizeOf(typeof(Locked))!=8)throw new InvalidOperationException("required x86 layout");
   report["pointer_bytes"]=IntPtr.Size;report["input_sha256"]=Hash(input);report["requested_size"]=new int[]{width,height};report["sdk_version"]=220;
   report["platform_calls_started"]=true;
   window=CreateWindowExW(0,"STATIC","Cross Hermit bounded texture audit",0x80000000,0,0,width,height,IntPtr.Zero,IntPtr.Zero,IntPtr.Zero,IntPtr.Zero);
   if(window==IntPtr.Zero || IsWindowVisible(window))throw new InvalidOperationException("hidden window creation");report["window_visible"]=false;report["window_pointer"]=Pointer(window);
   factory=Direct3DCreate8(220);if(factory==IntPtr.Zero)throw new InvalidOperationException("Direct3DCreate8 returned null");report["factory_pointer"]=Pointer(factory);
   var dll=new StringBuilder(1024);if(GetModuleFileNameW(GetModuleHandleW("d3d8.dll"),dll,dll.Capacity)==0)throw new InvalidOperationException("actual runtime provenance");
   report["runtime_path"]=dll.ToString();report["runtime_sha256"]=Hash(File.ReadAllBytes(dll.ToString()));
   string physical=Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.Windows),"SysWOW64","d3d8.dll");
   if(Hash(File.ReadAllBytes(physical))!=(string)report["runtime_sha256"])throw new InvalidOperationException("WOW64 runtime identity mismatch");
   report["physical_runtime_path"]=physical;
   Mode mode;int hr=Method<DisplayMode>(factory,8)(factory,0,out mode);HR(hr,"GetAdapterDisplayMode");
   trace.Add(new {name="GetAdapterDisplayMode",hr=hr,format=mode.Format});
   uint[][] attempts=new uint[][]{new uint[]{1,68},new uint[]{1,36},new uint[]{2,68},new uint[]{2,36}};
   foreach(uint[] attempt in attempts) {
    Present pp=new Present{Width=(uint)width,Height=(uint)height,Format=mode.Format,Count=1,Swap=1,Window=window,Windowed=1};
    hr=Method<CreateDevice>(factory,15)(factory,0,attempt[0],window,attempt[1],ref pp,out device);
    trace.Add(new {name="CreateDevice",hr=hr,adapter=0,type=attempt[0],flags=attempt[1],windowed=1,presentation_format=mode.Format});
    if(hr>=0 && device!=IntPtr.Zero)break;
    if(device!=IntPtr.Zero){Method<Release>(device,2)(device);device=IntPtr.Zero;}
   }
   HR(hr,"CreateDevice");if(device==IntPtr.Zero)throw new InvalidOperationException("device pointer");report["device_pointer"]=Pointer(device);
   hr=Method<CreateTexture>(device,20)(device,(uint)width,(uint)height,1,0,25,1,out texture);
   trace.Add(new {name="CreateTexture",hr=hr,width=width,height=height,levels=1,usage=0,format=25,pool=1});HR(hr,"CreateTexture");
   if(texture==IntPtr.Zero)throw new InvalidOperationException("texture pointer");report["texture_pointer"]=Pointer(texture);
   Desc desc;hr=Method<LevelDesc>(texture,14)(texture,0,out desc);trace.Add(new {name="GetLevelDesc",hr=hr,level=0});HR(hr,"GetLevelDesc");
   if(desc.Width!=(uint)width||desc.Height!=(uint)height||desc.Format!=25||desc.Pool!=1||desc.Usage!=0||desc.Type!=1)throw new InvalidOperationException("real texture description mismatch");
   report["description"]=new {width=desc.Width,height=desc.Height,format=desc.Format,type=desc.Type,usage=desc.Usage,pool=desc.Pool,size=desc.Size,multisample=desc.Multisample};
   Locked first;hr=Method<Lock>(texture,16)(texture,0,out first,IntPtr.Zero,0);trace.Add(new {name="LockRect",hr=hr,level=0,flags=0});HR(hr,"LockRect");locked=true;
   ReadRows(first,width,height);report["write_pitch"]=first.Pitch;
   for(int y=0;y<height;y++)Marshal.Copy(input,y*width*2,IntPtr.Add(first.Bits,y*first.Pitch),width*2);
   hr=Method<Unlock>(texture,17)(texture,0);trace.Add(new {name="UnlockRect",hr=hr});HR(hr,"UnlockRect");locked=false;
   Locked second;hr=Method<Lock>(texture,16)(texture,0,out second,IntPtr.Zero,16);trace.Add(new {name="LockRect",hr=hr,level=0,flags=16});HR(hr,"readonly LockRect");locked=true;
   byte[] readback=ReadRows(second,width,height);report["read_pitch"]=second.Pitch;report["readback_hex"]=Hex(readback);report["readback_sha256"]=Hash(readback);
   if(Hex(readback)!=Hex(input))throw new InvalidOperationException("entire texture roundtrip differs");
   hr=Method<Unlock>(texture,17)(texture,0);trace.Add(new {name="UnlockRect",hr=hr});HR(hr,"readonly UnlockRect");locked=false;
   report["all_pixels_equal"]=true;report["real_device_and_texture_executed"]=true;exit=0;
  } catch(Exception e){report["error"]=e.GetType().Name+": "+e.Message;}
  finally {
   if(locked && texture!=IntPtr.Zero){cleanup["emergency_unlock_hr"]=Method<Unlock>(texture,17)(texture,0);locked=false;}
   if(texture!=IntPtr.Zero)cleanup["texture_release_count"]=Method<Release>(texture,2)(texture);
   if(device!=IntPtr.Zero)cleanup["device_release_count"]=Method<Release>(device,2)(device);
   if(factory!=IntPtr.Zero)cleanup["factory_release_count"]=Method<Release>(factory,2)(factory);
   if(window!=IntPtr.Zero)cleanup["window_destroyed"]=DestroyWindow(window);
   bool released=true;
   foreach(string key in new string[]{"texture_release_count","device_release_count","factory_release_count"})if(cleanup.ContainsKey(key) && (uint)cleanup[key]!=0)released=false;
   if(cleanup.ContainsKey("window_destroyed") && !(bool)cleanup["window_destroyed"])released=false;
   cleanup["all_owned_resources_released"]=released;if(!released)exit=2;
  }
  string json=new JavaScriptSerializer{MaxJsonLength=4*1024*1024}.Serialize(report);
  if(output!=null)File.WriteAllText(output,json+"\n",new UTF8Encoding(false));
  Console.WriteLine(json);return exit;
 }
}
