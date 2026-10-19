// Owned x86 original font-cache requirements/texture interfaces; no drawing/Present.
using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Runtime.InteropServices;
using System.Security.Cryptography;
using System.Text;
using System.Web.Script.Serialization;

class SchoolStartupReturnDevice {
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
 [DllImport("kernel32.dll",CharSet=CharSet.Ansi)] static extern IntPtr GetProcAddress(IntPtr module,string name);
 [UnmanagedFunctionPointer(CallingConvention.Cdecl)] delegate void DebugMute(int value);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] delegate int GetFactory(IntPtr self,out IntPtr factory);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] delegate int CreateTexture(IntPtr self,uint width,uint height,uint levels,uint usage,uint format,uint pool,out IntPtr texture);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] delegate int GetSurface(IntPtr self,uint level,out IntPtr surface);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] delegate int LevelDesc(IntPtr self,uint level,IntPtr output);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] delegate int LockRect(IntPtr self,uint level,IntPtr output,IntPtr rectangle,uint flags);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] delegate int UnlockRect(IntPtr self,uint level);
 static bool secondLocked,secondUploaded;static int secondPitch;static IntPtr secondPixelBits;static byte[] secondBefore;
 static bool atlasLocked,atlasUploaded;static int atlasPitch;static IntPtr atlasPixelBits;static byte[] atlasBefore;
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] delegate int CreateVertexBuffer(IntPtr self,uint length,uint usage,uint fvf,uint pool,out IntPtr buffer);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] delegate int BeginBlock(IntPtr self);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] delegate int EndBlock(IntPtr self,out uint token);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] delegate int TokenCall(IntPtr self,uint token);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] delegate int TextureCall(IntPtr self,uint stage,IntPtr texture);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] delegate int RenderCall(IntPtr self,uint state,uint value);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] delegate int StageCall(IntPtr self,uint stage,uint type,uint value);

 [DllImport("user32.dll")] static extern IntPtr GetDC(IntPtr window);
 [DllImport("user32.dll")] static extern int ReleaseDC(IntPtr window,IntPtr dc);
 [DllImport("gdi32.dll")] static extern bool GetDeviceGammaRamp(IntPtr dc,IntPtr ramp);
 [DllImport("gdi32.dll")] static extern bool SetDeviceGammaRamp(IntPtr dc,IntPtr ramp);
 [DllImport("kernel32.dll")] static extern IntPtr VirtualAlloc(IntPtr address,UIntPtr size,uint kind,uint protect);
 [DllImport("kernel32.dll")] static extern bool VirtualFree(IntPtr address,UIntPtr size,uint kind);
 [DllImport("kernel32.dll")] static extern IntPtr GetCurrentProcess();
 [DllImport("kernel32.dll")] static extern bool FlushInstructionCache(IntPtr process,IntPtr address,UIntPtr size);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] delegate void GammaSet(IntPtr self,uint flags,IntPtr ramp);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] delegate void GammaGet(IntPtr self,IntPtr ramp);
 // This delegate calls our forwarding thunk, whose return is the observed EAX bits.
 // The actual device target remains a void API, with no HRESULT or defined return.
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] delegate uint GammaCapture(IntPtr self,uint flags,IntPtr ramp);
 static bool gammaPrepared,gammaCalled;static byte[] savedDeviceGamma,savedDesktopGamma;
 static int gammaDCsAcquired,gammaDCsReleased;
 static byte[] DeviceGammaRead(){IntPtr p=Marshal.AllocHGlobal(1536);try{
  Marshal.Copy(new byte[1536],0,p,1536);Method<GammaGet>(device,19)(device,p);return Bytes(p,1536);
 }finally{Marshal.FreeHGlobal(p);}}
 static byte[] DesktopGamma(bool write,byte[] value){
  IntPtr dc=GetDC(IntPtr.Zero);if(dc==IntPtr.Zero)throw new InvalidOperationException("desktop gamma DC unavailable");gammaDCsAcquired++;
  IntPtr p=Marshal.AllocHGlobal(1536);try{
   Marshal.Copy(write?value:new byte[1536],0,p,1536);
   bool ok=write?SetDeviceGammaRamp(dc,p):GetDeviceGammaRamp(dc,p);
   if(!ok)throw new InvalidOperationException(write?"desktop gamma restore failed":"desktop gamma snapshot unavailable");
   return Bytes(p,1536);
  }finally{Marshal.FreeHGlobal(p);if(ReleaseDC(IntPtr.Zero,dc)!=1)throw new InvalidOperationException("desktop gamma DC release failed");gammaDCsReleased++;}
 }
 static void RestoreGamma(Dictionary<string,object> r){
  if(gammaCalled){
   bool deviceOK=false,desktopOK=false;
   try{IntPtr p=Marshal.AllocHGlobal(1536);try{
    Marshal.Copy(savedDeviceGamma,0,p,1536);Method<GammaSet>(device,18)(device,0,p);
   }finally{Marshal.FreeHGlobal(p);}deviceOK=Hash(DeviceGammaRead())==Hash(savedDeviceGamma);
   }catch(Exception e){r["gamma_device_restore_error"]=e.Message;}
   try{byte[] now=DesktopGamma(false,null);bool changed=Hash(now)!=Hash(savedDesktopGamma);
    r["gamma_desktop_restore_write_required"]=changed;
    if(changed)DesktopGamma(true,savedDesktopGamma);
    desktopOK=Hash(DesktopGamma(false,null))==Hash(savedDesktopGamma);
   }catch(Exception e){r["gamma_desktop_restore_error"]=e.Message;}
   r["gamma_native_calls"]=1;r["gamma_device_restored"]=deviceOK;r["gamma_desktop_restored"]=desktopOK;
  }
  if(gammaDCsAcquired>0){r["gamma_DCs_acquired"]=gammaDCsAcquired;r["gamma_DCs_released"]=gammaDCsReleased;r["gamma_DCs_balanced"]=gammaDCsAcquired==gammaDCsReleased;}
 }
 static object GammaInvoke(byte[] b){
  savedDesktopGamma=DesktopGamma(false,null);savedDeviceGamma=DeviceGammaRead();
  IntPtr target=Marshal.ReadIntPtr(Marshal.ReadIntPtr(device),72);
  byte[] prefix=Parse("558becff7510ff750cff7508b8",13),suffix=Parse("ffd08be55dc20c00",8);
  byte[] code=new byte[25];Array.Copy(prefix,code,13);Array.Copy(BitConverter.GetBytes(Pointer(target)),0,code,13,4);Array.Copy(suffix,0,code,17,8);
  IntPtr thunk=VirtualAlloc(IntPtr.Zero,(UIntPtr)25,0x3000,0x40);
  if(thunk==IntPtr.Zero)throw new InvalidOperationException("owned gamma forwarding allocation failed");
  IntPtr p=Marshal.AllocHGlobal(1536);uint eax=0;byte[] after=null;bool freed=false;
  try{Marshal.Copy(code,0,thunk,25);if(!FlushInstructionCache(GetCurrentProcess(),thunk,(UIntPtr)25))throw new InvalidOperationException("owned gamma forwarding cache flush failed");
   Marshal.Copy(b,0,p,1536);gammaCalled=true;
   GammaCapture invoke=Marshal.GetDelegateForFunctionPointer(thunk,typeof(GammaCapture)) as GammaCapture;
   eax=invoke(device,1,p);after=Bytes(p,1536);
  }finally{Marshal.FreeHGlobal(p);freed=VirtualFree(thunk,UIntPtr.Zero,0x8000);if(!freed)throw new InvalidOperationException("owned gamma forwarding release failed");}
  return new {native_return_type="void",eax_bits_observed=eax,eax_is_status=false,method_pointer=Pointer(target),input_after_hex=Hex(after),
   forwarder_hex=Hex(code),forwarder_freed=freed,inspection=new {native_requested=false,device_before_hex=Hex(savedDeviceGamma),device_after_hex=Hex(DeviceGammaRead()),
    desktop_before_hex=Hex(savedDesktopGamma),desktop_after_hex=Hex(DesktopGamma(false,null))}};
 }

 static IntPtr secondVB;static bool secondRecording;static int secondFontStep;static List<uint> secondTokens=new List<uint>();
 static IntPtr fontVB;static bool fontRecording;static int fontStep;static List<uint> fontTokens=new List<uint>();
 class Step {public string method;public uint[] args;public Step(string m,params uint[] a){method=m;args=a;}}
 static List<Step> FontPlan(){var p=new List<Step>();for(int block=0;block<2;block++){
  p.Add(new Step("begin"));p.Add(new Step("texture",0));
  p.Add(new Step("render",27,1));
  p.Add(new Step("render",19,5));
  p.Add(new Step("render",20,6));
  p.Add(new Step("render",15,1));
  p.Add(new Step("render",24,8));
  p.Add(new Step("render",25,5));
  p.Add(new Step("render",8,3));
  p.Add(new Step("render",52,0));
  p.Add(new Step("render",136,1));
  p.Add(new Step("render",40,0));
  p.Add(new Step("render",152,0));
  p.Add(new Step("render",151,0));
  p.Add(new Step("render",167,0));
  p.Add(new Step("render",28,0));
  p.Add(new Step("stage",0,1,4));
  p.Add(new Step("stage",0,2,2));
  p.Add(new Step("stage",0,3,0));
  p.Add(new Step("stage",0,4,4));
  p.Add(new Step("stage",0,5,2));
  p.Add(new Step("stage",0,6,0));
  p.Add(new Step("stage",0,17,1));
  p.Add(new Step("stage",0,16,1));
  p.Add(new Step("stage",0,18,0));
  p.Add(new Step("stage",0,11,0));
  p.Add(new Step("stage",0,24,0));
  p.Add(new Step("stage",1,1,1));
  p.Add(new Step("stage",1,4,1));
  p.Add(new Step("end"));}return p;}
 static List<Step> fontPlan=FontPlan();
 static IntPtr atlasTexture,secondTexture;
 static IntPtr window,factory,device,surface,texture,levelSurface;
 static int spriteStep;static bool borrowedFactory;static int muteBalance,muteCalls,textureQueries;
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
 static object FirstTextureSnapshot() {
  IntPtr p=Marshal.AllocHGlobal(8);try {
   Marshal.Copy(new byte[8],0,p,8);int hr=Method<LockRect>(atlasTexture,16)(atlasTexture,0,p,IntPtr.Zero,16);
   if(hr<0)throw new InvalidOperationException("retained first texture readonly lock failed");atlasLocked=true;
   int pitch=Marshal.ReadInt32(p);IntPtr bits=Marshal.ReadIntPtr(p,4);
   if(pitch<512 || pitch>1024 || bits==IntPtr.Zero)throw new InvalidOperationException("bounded first texture readback required");
   byte[] value=Bytes(bits,pitch*256);int unlock=Method<UnlockRect>(atlasTexture,17)(atlasTexture,0);
   if(unlock<0)throw new InvalidOperationException("retained first texture readonly unlock failed");atlasLocked=false;
   return new {native_requested=false,method="LockRect(first texture readonly)/UnlockRect",pointer=Pointer(atlasTexture),flags=16,lock_hr=hr,unlock_hr=unlock,pitch=pitch,bits=Pointer(bits),hex=Hex(value)};
  }finally{Marshal.FreeHGlobal(p);}
 }
 static object VertexDescription(IntPtr obj) {
  IntPtr p=Marshal.AllocHGlobal(24);try {
   Marshal.Copy(new byte[24],0,p,24);int hr=Method<GetDesc>(obj,13)(obj,p);
   if(hr<0)throw new InvalidOperationException("retained actual VB description failed");
   return new {hr=hr,hex=Hex(Bytes(p,24))};
  }finally{Marshal.FreeHGlobal(p);}
 }
 static Dictionary<string,object> Cleanup() {
  var r=new Dictionary<string,object>();
  RestoreGamma(r);
  if(secondLocked){int hr=Method<UnlockRect>(secondTexture,17)(secondTexture,0);r["abandoned_second_atlas_unlock_hr"]=hr;secondLocked=false;}
  if(secondRecording){uint token;int hr=Method<EndBlock>(device,53)(device,out token);r["abandoned_second_font_end_hr"]=hr;if(hr>=0)r["abandoned_second_font_delete_hr"]=Method<TokenCall>(device,56)(device,token);secondRecording=false;}
  if(secondTokens.Count>0){var results=new List<int>();foreach(uint token in secondTokens)results.Add(Method<TokenCall>(device,56)(device,token));r["second_font_state_block_delete_results"]=results;secondTokens.Clear();}
  if(fontRecording){uint token;int hr=Method<EndBlock>(device,53)(device,out token);r["abandoned_font_end_hr"]=hr;if(hr>=0)r["abandoned_font_delete_hr"]=Method<TokenCall>(device,56)(device,token);fontRecording=false;}
  if(fontTokens.Count>0){var results=new List<int>();foreach(uint token in fontTokens)results.Add(Method<TokenCall>(device,56)(device,token));r["font_state_block_delete_results"]=results;fontTokens.Clear();}
  if(secondVB!=IntPtr.Zero){r["second_font_texture_unbind_hr"]=Method<TextureCall>(device,61)(device,0,IntPtr.Zero);r["second_font_vertex_buffer_release_count"]=Method<Release>(secondVB,2)(secondVB);secondVB=IntPtr.Zero;}
  if(fontVB!=IntPtr.Zero){r["font_texture_unbind_hr"]=Method<TextureCall>(device,61)(device,0,IntPtr.Zero);r["font_vertex_buffer_release_count"]=Method<Release>(fontVB,2)(fontVB);fontVB=IntPtr.Zero;}
  if(atlasLocked){int hr=Method<UnlockRect>(atlasTexture,17)(atlasTexture,0);r["abandoned_atlas_unlock_hr"]=hr;atlasLocked=false;}
  if(secondTexture!=IntPtr.Zero){r["second_atlas_texture_release_count"]=Method<Release>(secondTexture,2)(secondTexture);secondTexture=IntPtr.Zero;}
  if(atlasTexture!=IntPtr.Zero){r["atlas_texture_release_count"]=Method<Release>(atlasTexture,2)(atlasTexture);atlasTexture=IntPtr.Zero;}
  if(levelSurface!=IntPtr.Zero){r["texture_surface_release_count"]=Method<Release>(levelSurface,2)(levelSurface);levelSurface=IntPtr.Zero;}
  if(texture!=IntPtr.Zero){r["texture_release_count"]=Method<Release>(texture,2)(texture);texture=IntPtr.Zero;}
  if(borrowedFactory){r["borrowed_factory_release_count"]=Method<Release>(factory,2)(factory);borrowedFactory=false;}
  if(extraReferences>0){var counts=new List<uint>();while(extraReferences>0){counts.Add(Method<Release>(device,2)(device));extraReferences--;}r["extra_reference_release_counts"]=counts;}
  if(surface!=IntPtr.Zero){r["surface_release_count"]=Method<Release>(surface,2)(surface);surface=IntPtr.Zero;}
  if(device!=IntPtr.Zero){r["device_release_count"]=Method<Release>(device,2)(device);device=IntPtr.Zero;}
  if(factory!=IntPtr.Zero){r["factory_release_count"]=Method<Release>(factory,2)(factory);factory=IntPtr.Zero;}
  if(window!=IntPtr.Zero){r["window_destroyed"]=DestroyWindow(window);window=IntPtr.Zero;}
  bool ok=true;foreach(string key in new string[]{"device_release_count","factory_release_count","atlas_texture_release_count","font_vertex_buffer_release_count","second_atlas_texture_release_count","second_font_vertex_buffer_release_count"})if(r.ContainsKey(key) && (uint)r[key]!=0)ok=false;
  if(r.ContainsKey("window_destroyed") && !(bool)r["window_destroyed"])ok=false;
  foreach(string key in new string[]{"font_texture_unbind_hr","abandoned_font_end_hr","abandoned_font_delete_hr","abandoned_atlas_unlock_hr","abandoned_second_atlas_unlock_hr","second_font_texture_unbind_hr","abandoned_second_font_end_hr","abandoned_second_font_delete_hr"})if(r.ContainsKey(key) && (int)r[key]<0)ok=false;
  if(r.ContainsKey("font_state_block_delete_results"))foreach(int value in (List<int>)r["font_state_block_delete_results"])if(value<0)ok=false;
  if(r.ContainsKey("second_font_state_block_delete_results"))foreach(int value in (List<int>)r["second_font_state_block_delete_results"])if(value<0)ok=false;
  foreach(string key in new string[]{"gamma_device_restored","gamma_desktop_restored","gamma_DCs_balanced"})if(r.ContainsKey(key) && !(bool)r[key])ok=false;
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
   return new {factory=Identity(factory,2,8,10,15),runtime_path=physical,runtime_sha256=sha};
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
    return new {hr=hr,presentation_hex=Hex(Bytes(p,52)),device=Identity(device,1,6,7,8,9,16,20,23,40,50,51,52,53,56,61,63)};
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

  if(op=="gamma_prepare"){
   Keys(r,"id","op","pointer");Owned(r,device);
   if(gammaPrepared || gammaCalled || secondFontStep!=60 || secondRecording || fontRecording || secondTokens.Count!=2 || fontTokens.Count!=2)throw new ArgumentException("gamma admission after both fonts only");
   gammaPrepared=true;return new {native_requested=false,method="Read owned device vtable+72",device=Identity(device,18)};
  }
  if(op=="gamma_set"){
   Keys(r,"id","op","pointer","flags","hex");Owned(r,device);
   if(!gammaPrepared || gammaCalled || secondFontStep!=60 || Number(r,"flags")!=1)throw new ArgumentException("one original gamma call with flags1");
   byte[] b=Parse((string)r["hex"],1536);
   for(int channel=0;channel<3;channel++)for(int i=0;i<256;i++)if(BitConverter.ToUInt16(b,channel*512+i*2)!=(i<<8))throw new ArgumentException("exact original identity gamma ramp");
   return GammaInvoke(b);
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
  if(op=="debug_mute") {
   Keys(r,"id","op","value");uint value=Number(r,"value");
   if(cacheStep!=3 || muteCalls>=4 || value!=(muteBalance==0?1u:0u))throw new ArgumentException("bounded original debug pair");
   IntPtr module=GetModuleHandleW("d3d8.dll"),symbol=GetProcAddress(module,"DebugSetMute");
   if(symbol==IntPtr.Zero)throw new InvalidOperationException("actual debug export required");
   var method=Marshal.GetDelegateForFunctionPointer(symbol,typeof(DebugMute)) as DebugMute;method((int)value);
   muteCalls++;muteBalance=(int)value;return new {module_pointer=Pointer(module),export_pointer=Pointer(symbol),return_value_defined=false};
  }
  if(op=="texture_factory") {
   Keys(r,"id","op","pointer");Owned(r,device);if(cacheStep!=3 || muteBalance!=1 || borrowedFactory)throw new ArgumentException("one borrowed factory inside debug pair");
   IntPtr value;int hr=Method<GetFactory>(device,6)(device,out value);
   if(hr>=0){if(value!=factory)throw new InvalidOperationException("owned factory identity");borrowedFactory=true;}
   return new {hr=hr,factory=Identity(value,2,8,10,15)};
  }
  if(op=="texture_caps") {
   Keys(r,"id","op","pointer");Owned(r,device);if(cacheStep!=3 || textureQueries++>=4)throw new ArgumentException("bounded original texture caps queries");
   return RawQuery(device,212,"caps");
  }
  if(op=="texture_mode") {
   Keys(r,"id","op","pointer");Owned(r,device);if(!borrowedFactory || muteBalance!=1)throw new ArgumentException("original mode query sequence");
   return RawQuery(device,16,"device_mode");
  }
  if(op=="texture_format") {
   Keys(r,"id","op","pointer","adapter","type","adapter_format","usage","resource_type","format");Owned(r,factory);
   uint adapter=Number(r,"adapter"),type=Number(r,"type"),af=Number(r,"adapter_format"),usage=Number(r,"usage"),rt=Number(r,"resource_type"),format=Number(r,"format");
   uint[] allowed={20,21,22,23,24,40,41,25,26,27,28,29,30,31,34,50,51,52,60,61,62,63,64,65,67,1498831189,844715353,827611204,844388420,861165636,877942852,894720068,70,71,73,75,80,77,79,909200416,909200449,909201952,909201985};
   if(!borrowedFactory || muteBalance!=1 || adapter!=0 || type!=1 || af!=displayFormat || usage!=512 || rt!=3 || Array.IndexOf(allowed,format)<0)throw new ArgumentException("original cache texture format query");
   return new {hr=Method<CheckFormat>(factory,10)(factory,adapter,type,af,usage,rt,format)};
  }
  if(op=="texture_factory_release") {
   Keys(r,"id","op","pointer");Owned(r,factory);if(!borrowedFactory)throw new ArgumentException("borrowed factory required");
   uint count=Method<Release>(factory,2)(factory);borrowedFactory=false;return new {count=count};
  }
  if(op=="texture_create") {
   Keys(r,"id","op","pointer","width","height","levels","usage","format","pool");Owned(r,device);
   if(cacheStep!=3 || borrowedFactory || muteBalance!=0 || texture!=IntPtr.Zero || Number(r,"width")!=64 || Number(r,"height")!=16 || Number(r,"levels")!=1 || Number(r,"usage")!=512 || Number(r,"format")!=21 || Number(r,"pool")!=0)throw new ArgumentException("bounded original cache texture");
   int hr=Method<CreateTexture>(device,20)(device,64,16,1,512,21,0,out texture);
   return new {hr=hr,texture=Identity(texture,2,15)};
  }
  if(op=="texture_surface") {
   Keys(r,"id","op","pointer","level");Owned(r,texture);if(Number(r,"level")!=0 || levelSurface!=IntPtr.Zero)throw new ArgumentException("one original level0 surface");
   int hr=Method<GetSurface>(texture,15)(texture,0,out levelSurface);
   return new {hr=hr,surface=Identity(levelSurface,2,8),inspection=new {native_requested=false,method="GetDesc",result=RawQuery(levelSurface,32,"desc")}};
  }
  if(op=="sprite_addref" || op=="font_addref") {
   Keys(r,"id","op","pointer");Owned(r,device);
   if(texture==IntPtr.Zero || levelSurface==IntPtr.Zero || (op=="sprite_addref"?(spriteStep!=0 || extraReferences!=1):(spriteStep!=3 || extraReferences!=2)))throw new ArgumentException("bounded original sprite/font reference");
   uint count=Method<Release>(device,1)(device);extraReferences++;spriteStep=op=="sprite_addref"?1:4;return new {count=count};
  }
  if(op=="sprite_caps") {
   Keys(r,"id","op","pointer");Owned(r,device);if(spriteStep!=1)throw new ArgumentException("original sprite caps order");
   object result=RawQuery(device,212,"caps");spriteStep=2;return result;
  }
  if(op=="sprite_creation") {
   Keys(r,"id","op","pointer");Owned(r,device);if(spriteStep!=2)throw new ArgumentException("original sprite creation order");
   IntPtr p=Marshal.AllocHGlobal(16);try {
    Marshal.Copy(new byte[16],0,p,16);int hr=Method<GetCaps>(device,9)(device,p);spriteStep=3;return new {hr=hr,hex=Hex(Bytes(p,16))};
   }finally{Marshal.FreeHGlobal(p);}
  }
  if(op=="second_atlas_create") {
   Keys(r,"id","op","pointer","width","height","levels","usage","format","pool");Owned(r,device);
   if(fontRecording || fontStep!=60 || fontTokens.Count!=2 || !atlasUploaded || atlasTexture==IntPtr.Zero || fontVB==IntPtr.Zero || secondTexture!=IntPtr.Zero || Number(r,"width")!=256 || Number(r,"height")!=256 || Number(r,"levels")!=1 || Number(r,"usage")!=0 || Number(r,"format")!=26 || Number(r,"pool")!=1)throw new ArgumentException("second atlas requires complete first font and exact source arguments");
   int hr=Method<CreateTexture>(device,20)(device,256,256,1,0,26,1,out secondTexture);
   if(hr<0 || secondTexture==IntPtr.Zero || secondTexture==atlasTexture)throw new InvalidOperationException("actual distinct second atlas failed");
   IntPtr p=Marshal.AllocHGlobal(32);try {
    Marshal.Copy(new byte[32],0,p,32);int descHr=Method<LevelDesc>(secondTexture,14)(secondTexture,0,p);string secondDesc=Hex(Bytes(p,32));
    Marshal.Copy(new byte[32],0,p,32);int firstHr=Method<LevelDesc>(atlasTexture,14)(atlasTexture,0,p);string firstDesc=Hex(Bytes(p,32));
    if(descHr<0 || firstHr<0)throw new InvalidOperationException("actual two atlas descriptions failed");
    return new {hr=hr,texture=Identity(secondTexture,2,14,16,17),inspection=new {native_requested=false,method="GetLevelDesc",level=0,result=new {hr=descHr,hex=secondDesc}},
     retention_inspection=new {native_requested=false,method="GetLevelDesc(first texture)/GetDesc(first vertex buffer)",first_texture=new {pointer=Pointer(atlasTexture),hr=firstHr,hex=firstDesc},first_vertex=new {pointer=Pointer(fontVB),result=VertexDescription(fontVB)}},
     retained_state_tokens=fontTokens.ToArray(),retained_state_tokens_are_ownership_metadata=true};
   }finally{Marshal.FreeHGlobal(p);}
  }
  if(op=="atlas_create") {
   Keys(r,"id","op","pointer","width","height","levels","usage","format","pool");Owned(r,device);
   if(spriteStep!=4 || atlasTexture!=IntPtr.Zero || Number(r,"width")!=256 || Number(r,"height")!=256 || Number(r,"levels")!=1 || Number(r,"usage")!=0 || Number(r,"format")!=26 || Number(r,"pool")!=1)throw new ArgumentException("bounded original additional atlas texture");
   int hr=Method<CreateTexture>(device,20)(device,256,256,1,0,26,1,out atlasTexture);
   if(hr<0 || atlasTexture==IntPtr.Zero)throw new InvalidOperationException("actual additional atlas texture failed");
   IntPtr p=Marshal.AllocHGlobal(32);try {
    Marshal.Copy(new byte[32],0,p,32);int descHr=Method<LevelDesc>(atlasTexture,14)(atlasTexture,0,p);
    if(descHr<0)throw new InvalidOperationException("actual atlas description failed");
    return new {hr=hr,texture=Identity(atlasTexture,2,14,16,17),inspection=new {native_requested=false,method="GetLevelDesc",level=0,result=new {hr=descHr,hex=Hex(Bytes(p,32))}}};
   }finally{Marshal.FreeHGlobal(p);}
  }
  if(op=="atlas_lock") {
   Keys(r,"id","op","pointer","level","rect","flags");Owned(r,atlasTexture);
   if(atlasLocked || atlasUploaded || Number(r,"level")!=0 || Number(r,"rect")!=0 || Number(r,"flags")!=0)throw new ArgumentException("bounded original atlas lock");
   IntPtr p=Marshal.AllocHGlobal(8);try {
    Marshal.Copy(new byte[8],0,p,8);int hr=Method<LockRect>(atlasTexture,16)(atlasTexture,0,p,IntPtr.Zero,0);
    if(hr<0)throw new InvalidOperationException("actual atlas lock failed");atlasLocked=true;atlasPitch=Marshal.ReadInt32(p);atlasPixelBits=Marshal.ReadIntPtr(p,4);
    if(atlasPitch<512 || atlasPitch>1024 || atlasPixelBits==IntPtr.Zero)throw new InvalidOperationException("actual bounded atlas lock buffer required");
    atlasBefore=Bytes(atlasPixelBits,atlasPitch*256);return new {hr=hr,locked_hex=Hex(Bytes(p,8)),pitch=atlasPitch,bits=Pointer(atlasPixelBits),before_hex=Hex(atlasBefore)};
   }finally{Marshal.FreeHGlobal(p);}
  }
  if(op=="atlas_unlock") {
   Keys(r,"id","op","pointer","level","bytes_hex");Owned(r,atlasTexture);
   if(!atlasLocked || atlasUploaded || Number(r,"level")!=0)throw new ArgumentException("one original atlas unlock after lock");
   byte[] value=Parse((string)r["bytes_hex"],atlasPitch*256);
   if(Hex(Bytes(atlasPixelBits,atlasPitch*256))!=Hex(atlasBefore))throw new InvalidOperationException("owned locked bytes changed outside native transfer");
   Marshal.Copy(value,0,atlasPixelBits,value.Length);int hr=Method<UnlockRect>(atlasTexture,17)(atlasTexture,0);
   if(hr<0)throw new InvalidOperationException("actual atlas unlock failed");atlasLocked=false;atlasUploaded=true;
   IntPtr p=Marshal.AllocHGlobal(8);try {
    Marshal.Copy(new byte[8],0,p,8);int readHr=Method<LockRect>(atlasTexture,16)(atlasTexture,0,p,IntPtr.Zero,16);
    if(readHr<0)throw new InvalidOperationException("actual readonly atlas readback failed");atlasLocked=true;
    int pitch=Marshal.ReadInt32(p);IntPtr bits=Marshal.ReadIntPtr(p,4);if(pitch!=atlasPitch || bits==IntPtr.Zero)throw new InvalidOperationException("actual readonly atlas buffer mismatch");
    byte[] actual=Bytes(bits,pitch*256);int unlockHr=Method<UnlockRect>(atlasTexture,17)(atlasTexture,0);
    if(unlockHr<0)throw new InvalidOperationException("actual readonly unlock failed");atlasLocked=false;
    return new {hr=hr,inspection=new {native_requested=false,method="LockRect(readonly)/UnlockRect",flags=16,lock_hr=readHr,unlock_hr=unlockHr,pitch=pitch,bits=Pointer(bits),hex=Hex(actual)}};
   }finally{Marshal.FreeHGlobal(p);}
  }
  if(op=="second_atlas_lock") {
   Keys(r,"id","op","pointer","level","rect","flags");Owned(r,secondTexture);
   if(secondLocked || secondUploaded || Number(r,"level")!=0 || Number(r,"rect")!=0 || Number(r,"flags")!=0)throw new ArgumentException("bounded original atlas lock");
   IntPtr p=Marshal.AllocHGlobal(8);try {
    Marshal.Copy(new byte[8],0,p,8);int hr=Method<LockRect>(secondTexture,16)(secondTexture,0,p,IntPtr.Zero,0);
    if(hr<0)throw new InvalidOperationException("actual atlas lock failed");secondLocked=true;secondPitch=Marshal.ReadInt32(p);secondPixelBits=Marshal.ReadIntPtr(p,4);
    if(secondPitch<512 || secondPitch>1024 || secondPixelBits==IntPtr.Zero)throw new InvalidOperationException("actual bounded atlas lock buffer required");
    secondBefore=Bytes(secondPixelBits,secondPitch*256);return new {hr=hr,locked_hex=Hex(Bytes(p,8)),pitch=secondPitch,bits=Pointer(secondPixelBits),before_hex=Hex(secondBefore)};
   }finally{Marshal.FreeHGlobal(p);}
  }
  if(op=="second_atlas_unlock") {
   Keys(r,"id","op","pointer","level","bytes_hex");Owned(r,secondTexture);
   if(!secondLocked || secondUploaded || Number(r,"level")!=0)throw new ArgumentException("one original atlas unlock after lock");
   byte[] value=Parse((string)r["bytes_hex"],secondPitch*256);
   if(Hex(Bytes(secondPixelBits,secondPitch*256))!=Hex(secondBefore))throw new InvalidOperationException("owned locked bytes changed outside native transfer");
   Marshal.Copy(value,0,secondPixelBits,value.Length);int hr=Method<UnlockRect>(secondTexture,17)(secondTexture,0);
   if(hr<0)throw new InvalidOperationException("actual atlas unlock failed");secondLocked=false;secondUploaded=true;
   IntPtr p=Marshal.AllocHGlobal(8);try {
    Marshal.Copy(new byte[8],0,p,8);int readHr=Method<LockRect>(secondTexture,16)(secondTexture,0,p,IntPtr.Zero,16);
    if(readHr<0)throw new InvalidOperationException("actual readonly atlas readback failed");secondLocked=true;
    int pitch=Marshal.ReadInt32(p);IntPtr bits=Marshal.ReadIntPtr(p,4);if(pitch!=secondPitch || bits==IntPtr.Zero)throw new InvalidOperationException("actual readonly atlas buffer mismatch");
    byte[] actual=Bytes(bits,pitch*256);int unlockHr=Method<UnlockRect>(secondTexture,17)(secondTexture,0);
    if(unlockHr<0)throw new InvalidOperationException("actual readonly unlock failed");secondLocked=false;
    return new {hr=hr,inspection=new {native_requested=false,method="LockRect(readonly)/UnlockRect",flags=16,lock_hr=readHr,unlock_hr=unlockHr,pitch=pitch,bits=Pointer(bits),hex=Hex(actual)},retained_first_texture_inspection=FirstTextureSnapshot()};
   }finally{Marshal.FreeHGlobal(p);}
  }
  if(op=="font_vb") {
   Keys(r,"id","op","pointer","args");Owned(r,device);IList args=r["args"] as IList;uint[] expected={8400,520,0,0};
   if(!atlasUploaded || fontVB!=IntPtr.Zero || args==null || args.Count!=4)throw new ArgumentException("bounded original font VB prerequisites");
   for(int i=0;i<4;i++)if(Convert.ToInt64(args[i])!=expected[i])throw new ArgumentException("original font VB arguments");
   int hr=Method<CreateVertexBuffer>(device,23)(device,8400,520,0,0,out fontVB);if(hr<0 || fontVB==IntPtr.Zero)throw new InvalidOperationException("actual font VB failed");
   IntPtr p=Marshal.AllocHGlobal(24);try{Marshal.Copy(new byte[24],0,p,24);int descHr=Method<GetDesc>(fontVB,13)(fontVB,p);return new {hr=hr,buffer=Identity(fontVB,2,13),inspection=new {native_requested=false,method="GetDesc(vertex buffer)",result=new {hr=descHr,hex=Hex(Bytes(p,24))}}};}finally{Marshal.FreeHGlobal(p);}
  }
  if(op=="font_state") {
   Keys(r,"id","op","pointer","method","args");Owned(r,device);string method=(string)r["method"];IList args=r["args"] as IList;
   if(fontVB==IntPtr.Zero || fontStep>=fontPlan.Count || method!=fontPlan[fontStep].method || args==null)throw new ArgumentException("original bounded font state order");
   uint[] expected=fontPlan[fontStep].args;int count=method=="texture"?2:expected.Length;if(args.Count!=count)throw new ArgumentException("original font state arguments");
   for(int i=0;i<expected.Length;i++)if(Convert.ToInt64(args[i])!=expected[i])throw new ArgumentException("original font state values");
   if(method=="texture" && Convert.ToInt64(args[1])!=Pointer(atlasTexture))throw new ArgumentException("original owned atlas binding");
   int hr;uint token=0;
   if(method=="begin"){hr=Method<BeginBlock>(device,52)(device);if(hr>=0)fontRecording=true;}
   else if(method=="texture")hr=Method<TextureCall>(device,61)(device,0,atlasTexture);
   else if(method=="render")hr=Method<RenderCall>(device,50)(device,expected[0],expected[1]);
   else if(method=="stage")hr=Method<StageCall>(device,63)(device,expected[0],expected[1],expected[2]);
   else {hr=Method<EndBlock>(device,53)(device,out token);if(hr>=0){fontRecording=false;fontTokens.Add(token);}}
   if(hr<0)throw new InvalidOperationException("actual font state call failed");fontStep++;if(method=="end")return new {hr=hr,token=token};return new {hr=hr};
  }
  if(op=="second_font_vb") {
   Keys(r,"id","op","pointer","args");Owned(r,device);IList args=r["args"] as IList;uint[] expected={8400,520,0,0};
   if(fontStep!=60 || !secondUploaded || secondVB!=IntPtr.Zero || args==null || args.Count!=4)throw new ArgumentException("bounded original font VB prerequisites");
   for(int i=0;i<4;i++)if(Convert.ToInt64(args[i])!=expected[i])throw new ArgumentException("original font VB arguments");
   int hr=Method<CreateVertexBuffer>(device,23)(device,8400,520,0,0,out secondVB);if(hr<0 || secondVB==IntPtr.Zero || secondVB==fontVB)throw new InvalidOperationException("actual font VB failed");
   IntPtr p=Marshal.AllocHGlobal(24);try{Marshal.Copy(new byte[24],0,p,24);int descHr=Method<GetDesc>(secondVB,13)(secondVB,p);return new {hr=hr,buffer=Identity(secondVB,2,13),inspection=new {native_requested=false,method="GetDesc(vertex buffer)",result=new {hr=descHr,hex=Hex(Bytes(p,24))}}};}finally{Marshal.FreeHGlobal(p);}
  }
  if(op=="second_font_state") {
   Keys(r,"id","op","pointer","method","args");Owned(r,device);string method=(string)r["method"];IList args=r["args"] as IList;
   if(secondVB==IntPtr.Zero || secondFontStep>=fontPlan.Count || method!=fontPlan[secondFontStep].method || args==null)throw new ArgumentException("original bounded font state order");
   uint[] expected=fontPlan[secondFontStep].args;int count=method=="texture"?2:expected.Length;if(args.Count!=count)throw new ArgumentException("original font state arguments");
   for(int i=0;i<expected.Length;i++)if(Convert.ToInt64(args[i])!=expected[i])throw new ArgumentException("original font state values");
   if(method=="texture" && Convert.ToInt64(args[1])!=Pointer(secondTexture))throw new ArgumentException("original owned atlas binding");
   int hr;uint token=0;
   if(method=="begin"){hr=Method<BeginBlock>(device,52)(device);if(hr>=0)secondRecording=true;}
   else if(method=="texture")hr=Method<TextureCall>(device,61)(device,0,secondTexture);
   else if(method=="render")hr=Method<RenderCall>(device,50)(device,expected[0],expected[1]);
   else if(method=="stage")hr=Method<StageCall>(device,63)(device,expected[0],expected[1],expected[2]);
   else {hr=Method<EndBlock>(device,53)(device,out token);if(hr>=0){secondRecording=false;secondTokens.Add(token);}}
   if(hr<0)throw new InvalidOperationException("actual font state call failed");secondFontStep++;if(method=="end")return new {hr=hr,token=token};return new {hr=hr};
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
