// Owned x86 class adapter. Guest424980 is transported, never executed as host code.
using System;
using System.Collections;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using System.Web.Script.Serialization;

class SchoolWindowClassPlatform {
 [DllImport("user32.dll",ExactSpelling=true,SetLastError=true)] static extern int GetClassInfoExA(IntPtr module,IntPtr name,IntPtr output);
 [DllImport("user32.dll",ExactSpelling=true,SetLastError=true)] static extern int UnregisterClassA(IntPtr name,IntPtr module);
 [DllImport("kernel32.dll")] static extern void SetLastError(uint error);
 [UnmanagedFunctionPointer(CallingConvention.StdCall,SetLastError=true)] delegate uint AtomCapture(IntPtr pointer);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] delegate IntPtr WndProc(IntPtr hwnd,uint message,IntPtr wParam,IntPtr lParam);
 static WndProc callbackRoot;static IntPtr callbackPointer,classStorage;static uint classAtom;
 static uint[] iconHandles=new uint[2];static uint cursorHandle,brushHandle;
 static int registrationCalls,inspectionCalls,unregistrationCalls,callbackCalls;
 static object unregisterProof;
 static IntPtr Ptr(uint value){return new IntPtr(unchecked((int)value));}
 static void Put(byte[] bytes,int offset,uint value){Array.Copy(BitConverter.GetBytes(value),0,bytes,offset,4);}
 static IntPtr Callback(IntPtr hwnd,uint message,IntPtr wParam,IntPtr lParam){
  int callbackId=++callbackCalls;
  Emit(new {event_kind="wndproc",callback_id=callbackId,guest_entry=0x424980,hwnd=Pointer(hwnd),message=message,wParam=Pointer(wParam),lParam=Pointer(lParam)});
  // No fallback game body or DefWindowProc. A future original-guest dispatcher must reply.
  try{string line=Console.ReadLine();if(line==null || line.Length>8192)throw new InvalidOperationException("bounded original callback response required");
   var r=json.Deserialize<Dictionary<string,object>>(line);Keys(r,"op","callback_id","result");
   if((string)r["op"]!="callback_return" || Number(r,"callback_id")!=callbackId)throw new InvalidOperationException("matching original guest callback result required");
   return Ptr(Number(r,"result"));
  }catch(Exception e){Environment.FailFast("original callback transport refused: "+e.Message);throw;}
 }
 static object InspectClass(IntPtr key){
  byte[] before=new byte[48];Put(before,0,48);IntPtr a=Buffer(before);
  try{SetLastError(0);int result=GetClassInfoExA(resourceModule,key,IntPtr.Add(a,32));int error=Marshal.GetLastWin32Error();inspectionCalls++;Guard(a,48);
   byte[] b=Bytes(IntPtr.Add(a,32),48);string name=result==0?null:Marshal.PtrToStringAnsi(Ptr(BitConverter.ToUInt32(b,40)));
   return new {result=unchecked((uint)result),last_error=error,hex=Hex(b),class_name=name,guards_unchanged=true};
  }finally{Marshal.FreeHGlobal(a);}
 }
 static uint RegisterCaptured(IntPtr p,out string codeHex,out int error){
  IntPtr target=GetProcAddress(userLibrary,"RegisterClassExA");if(target==IntPtr.Zero)throw new InvalidOperationException("real registration export missing");
  byte[] code=Parse("558becff7508b800000000ffd08be55dc20400",19);Array.Copy(BitConverter.GetBytes(Pointer(target)),0,code,7,4);codeHex=Hex(code);
  IntPtr thunk=VirtualAlloc(IntPtr.Zero,(UIntPtr)19,0x3000,0x40);if(thunk==IntPtr.Zero)throw new InvalidOperationException("registration forwarding allocation failed");
  try{Marshal.Copy(code,0,thunk,19);if(!FlushInstructionCache(GetCurrentProcess(),thunk,(UIntPtr)19))throw new InvalidOperationException("registration forwarding flush failed");
   AtomCapture call=(AtomCapture)Marshal.GetDelegateForFunctionPointer(thunk,typeof(AtomCapture));SetLastError(0);uint eax=call(p);error=Marshal.GetLastWin32Error();return eax;
  }finally{if(!VirtualFree(thunk,UIntPtr.Zero,0x8000))throw new InvalidOperationException("registration forwarding release failed");}
 }
 static object UnregisterOwned(){
  if(classAtom==0)throw new ArgumentException("owned registered class required");uint atom=classAtom;
  SetLastError(0);int result=UnregisterClassA(Ptr(atom),resourceModule);int error=Marshal.GetLastWin32Error();unregistrationCalls++;
  if(result==0)throw new InvalidOperationException("owned class unregistration failed: "+error);
  classAtom=0;object after=InspectClass(Ptr(atom));
  Guard(classStorage,titleBytes.Length);Marshal.FreeHGlobal(classStorage);classStorage=IntPtr.Zero;
  callbackRoot=null;callbackPointer=IntPtr.Zero;
  unregisterProof=new {atom=atom,result=unchecked((uint)result),last_error=error,query_after=after,callback_retained_until_unregister=true,class_storage_freed=true};
  return unregisterProof;
 }
 static object Register(Dictionary<string,object> r){
  Keys(r,"id","op","class_hex","class_name_hex");
  if(brushCalls!=1 || registrationCalls!=0 || (string)r["class_name_hex"]!=Hex(titleBytes))throw new ArgumentException("one original ready class required");
  byte[] guest=Parse((string)r["class_hex"],48);uint[] wanted={48,0,0x424980,0,0,Pointer(resourceModule),iconHandles[0],cursorHandle,brushHandle,0,0x7a2628,iconHandles[1]};
  for(int i=0;i<12;i++)if(BitConverter.ToUInt32(guest,i*4)!=wanted[i])throw new ArgumentException("exact original guest class required");
  classStorage=Buffer(titleBytes);callbackRoot=new WndProc(Callback);callbackPointer=Marshal.GetFunctionPointerForDelegate(callbackRoot);
  byte[] host=(byte[])guest.Clone();Put(host,8,Pointer(callbackPointer));Put(host,40,Pointer(IntPtr.Add(classStorage,32)));
  IntPtr a=Buffer(host);bool retained=false;
  try{object preflight=InspectClass(IntPtr.Add(classStorage,32));
   // Own module/name only. Never unregister a preexisting foreign class.
   var before=json.Deserialize<Dictionary<string,object>>(json.Serialize(preflight));if(Convert.ToUInt32(before["result"])!=0)throw new InvalidOperationException("class already exists");
   string code;int error;uint eax=RegisterCaptured(IntPtr.Add(a,32),out code,out error);registrationCalls++;classAtom=eax&65535;retained=classAtom!=0;
   Guard(a,48);Guard(classStorage,titleBytes.Length);if(Hex(Bytes(IntPtr.Add(a,32),48))!=Hex(host))throw new InvalidOperationException("registration modified const class");
   object byAtom=null,byName=null;
   if(classAtom!=0){retained=true;byAtom=InspectClass(Ptr(classAtom));byName=InspectClass(IntPtr.Add(classStorage,32));}
   return new {result=eax,atom=classAtom,last_error=error,native_return_type="ATOM",eax_bits_observed=eax,
    guest_hex=Hex(guest),host_hex=Hex(host),class_name_hex=Hex(titleBytes),
    pointer_translations=new object[]{new {offset=8,guest=0x424980,host=Pointer(callbackPointer)},new {offset=40,guest=0x7a2628,host=Pointer(IntPtr.Add(classStorage,32))}},
    preflight=preflight,by_atom=byAtom,by_name=byName,forwarder_hex=code,forwarder_freed=true,guards_unchanged=true,
    guest_class_unchanged=true,callback_transport="stdcall IPC requires original guest result; no fallback",callback_calls=callbackCalls,window_created=false};
  }finally{Marshal.FreeHGlobal(a);if(!retained){if(classStorage!=IntPtr.Zero){Marshal.FreeHGlobal(classStorage);classStorage=IntPtr.Zero;}callbackRoot=null;callbackPointer=IntPtr.Zero;}}
 }
 [DllImport("kernel32.dll",CharSet=CharSet.Unicode)] static extern IntPtr GetModuleHandle(string name);
 [DllImport("kernel32.dll",CharSet=CharSet.Ansi,ExactSpelling=true)] static extern IntPtr GetProcAddress(IntPtr module,string name);
 [DllImport("kernel32.dll",CharSet=CharSet.Unicode)] static extern uint GetModuleFileName(IntPtr module,System.Text.StringBuilder name,int count);
 [DllImport("kernel32.dll")] static extern uint GetACP();
 [DllImport("kernel32.dll")] static extern void DeleteCriticalSection(IntPtr pointer);
 [DllImport("kernel32.dll",ExactSpelling=true)] static extern IntPtr CreateEventA(IntPtr security,bool manual,bool signaled,IntPtr name);
 [DllImport("kernel32.dll")] static extern bool CloseHandle(IntPtr handle);
 [DllImport("kernel32.dll",ExactSpelling=true)] static extern uint GetCurrentDirectoryA(uint count,IntPtr output);
 [DllImport("shlwapi.dll",ExactSpelling=true)] static extern IntPtr PathAddBackslashA(IntPtr path);
 [DllImport("kernel32.dll",ExactSpelling=true)] static extern IntPtr lstrcpyA(IntPtr destination,IntPtr source);
 [DllImport("kernel32.dll",ExactSpelling=true)] static extern IntPtr lstrcatA(IntPtr destination,IntPtr source);
 [DllImport("kernel32.dll")] static extern IntPtr VirtualAlloc(IntPtr address,UIntPtr size,uint kind,uint protect);
 [DllImport("kernel32.dll")] static extern bool VirtualFree(IntPtr address,UIntPtr size,uint kind);
 [DllImport("kernel32.dll")] static extern IntPtr GetCurrentProcess();
 [DllImport("kernel32.dll")] static extern bool FlushInstructionCache(IntPtr process,IntPtr address,UIntPtr size);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] delegate uint VoidCapture(IntPtr pointer);
 [DllImport("user32.dll",ExactSpelling=true)] static extern IntPtr FindWindowA(IntPtr className,IntPtr windowName);
 [DllImport("kernel32.dll",CharSet=CharSet.Unicode)] static extern IntPtr LoadLibrary(string name);
 [DllImport("kernel32.dll")] static extern bool FreeLibrary(IntPtr module);
 [DllImport("user32.dll",ExactSpelling=true)] static extern int SetRect(IntPtr rectangle,int left,int top,int right,int bottom);
 [DllImport("user32.dll",ExactSpelling=true)] static extern int AdjustWindowRect(IntPtr rectangle,uint style,int menu);
 [DllImport("kernel32.dll",CharSet=CharSet.Unicode)] static extern IntPtr FindResourceEx(IntPtr module,IntPtr type,IntPtr name,ushort language);
 [DllImport("kernel32.dll")] static extern IntPtr LoadResource(IntPtr module,IntPtr resource);
 [DllImport("kernel32.dll")] static extern IntPtr LockResource(IntPtr resource);
 [DllImport("kernel32.dll")] static extern uint SizeofResource(IntPtr module,IntPtr resource);
 [DllImport("user32.dll",ExactSpelling=true)] static extern IntPtr LoadIconA(IntPtr module,IntPtr id);
 [DllImport("user32.dll",ExactSpelling=true)] static extern IntPtr LoadCursorA(IntPtr module,IntPtr id);
 [DllImport("gdi32.dll")] static extern IntPtr GetStockObject(int id);
 static IntPtr resourceModule,gdiLibrary;static int iconCalls,cursorCalls,brushCalls;static object moduleProof;
 static string Hash(byte[] b){using(var h=System.Security.Cryptography.SHA256.Create())return Hex(h.ComputeHash(b));}
 static object InspectResource(int type,int id,int expectedSize,string expectedHash){
  IntPtr r=FindResourceEx(resourceModule,(IntPtr)type,(IntPtr)id,1041);if(r==IntPtr.Zero || SizeofResource(resourceModule,r)!=(uint)expectedSize)throw new InvalidOperationException("actual resource identity/size missing");
  IntPtr data=LockResource(LoadResource(resourceModule,r));if(data==IntPtr.Zero)throw new InvalidOperationException("actual resource bytes unavailable");byte[] b=Bytes(data,expectedSize);
  if(Hash(b)!=expectedHash)throw new InvalidOperationException("actual loaded resource bytes differ");return new {type_id=type,id=id,language=1041,bytes=b.Length,sha256=Hash(b),hex=Hex(b)};
 }
 static int geometryStep;static uint foundWindow;static byte[] clientRectangle;
 static IntPtr userLibrary;static bool titleCopied,queried;
 static byte[] titleBytes=Parse("43726f7373204865726d697400",13);
 static JavaScriptSerializer json=new JavaScriptSerializer();
 static List<IntPtr> sections=new List<IntPtr>();
 static IntPtr eventHandle;static byte[] directory,path;
 static int copies,concats;static long sequence;
 static uint Pointer(IntPtr p){return unchecked((uint)p.ToInt32());}
 static string Hex(byte[] b){return BitConverter.ToString(b).Replace("-","").ToLowerInvariant();}
 static byte[] Bytes(IntPtr p,int n){byte[] b=new byte[n];Marshal.Copy(p,b,0,n);return b;}
 static byte[] Parse(string s,int n){if(s.Length!=n*2)throw new ArgumentException("exact bounded buffer required");byte[] b=new byte[n];for(int i=0;i<n;i++)b[i]=Convert.ToByte(s.Substring(i*2,2),16);return b;}
 static int Length(byte[] b){int n=Array.IndexOf(b,(byte)0);if(n<0)throw new ArgumentException("terminated ANSI buffer required");return n;}
 static uint Number(Dictionary<string,object> r,string key){object o=r[key];if(!(o is int) && !(o is long))throw new ArgumentException("integer required");long n=Convert.ToInt64(o);if(n<0 || n>uint.MaxValue)throw new ArgumentException("uint32 required");return (uint)n;}
 static void Keys(Dictionary<string,object> r,params string[] keys){if(r.Count!=keys.Length)throw new ArgumentException("request shape");foreach(string k in keys)if(!r.ContainsKey(k))throw new ArgumentException("request shape");}
 static IntPtr Buffer(byte[] b){byte[] all=new byte[b.Length+64];for(int i=0;i<all.Length;i++)all[i]=0xa5;Array.Copy(b,0,all,32,b.Length);IntPtr p=Marshal.AllocHGlobal(all.Length);Marshal.Copy(all,0,p,all.Length);return p;}
 static void Guard(IntPtr allocation,int n){byte[] b=Bytes(allocation,n+64);for(int i=0;i<32;i++)if(b[i]!=0xa5 || b[n+32+i]!=0xa5)throw new InvalidOperationException("owned buffer guard modified");}
 static string Module(string name){IntPtr m=GetModuleHandle(name);if(m==IntPtr.Zero)throw new InvalidOperationException("system module missing");var s=new System.Text.StringBuilder(1024);if(GetModuleFileName(m,s,s.Capacity)==0)throw new InvalidOperationException("module path missing");return s.ToString();}
 static uint Initialize(IntPtr p,out string codeHex){
  IntPtr target=GetProcAddress(GetModuleHandle("kernel32.dll"),"InitializeCriticalSection");if(target==IntPtr.Zero)throw new InvalidOperationException("real critical section target missing");
  byte[] code=Parse("558becff7508b800000000ffd08be55dc20400",19);Array.Copy(BitConverter.GetBytes(Pointer(target)),0,code,7,4);codeHex=Hex(code);
  IntPtr thunk=VirtualAlloc(IntPtr.Zero,(UIntPtr)19,0x3000,0x40);if(thunk==IntPtr.Zero)throw new InvalidOperationException("owned forwarding allocation failed");
  try{Marshal.Copy(code,0,thunk,19);if(!FlushInstructionCache(GetCurrentProcess(),thunk,(UIntPtr)19))throw new InvalidOperationException("owned forwarding flush failed");
   return ((VoidCapture)Marshal.GetDelegateForFunctionPointer(thunk,typeof(VoidCapture)))(p);
  }finally{if(!VirtualFree(thunk,UIntPtr.Zero,0x8000))throw new InvalidOperationException("owned forwarding release failed");}
 }
 static object Cleanup(){int cs=0,events=0;bool ok=true;
  if(classAtom!=0)UnregisterOwned();
  if(eventHandle!=IntPtr.Zero){bool released=CloseHandle(eventHandle);ok&=released;if(released)events++;eventHandle=IntPtr.Zero;}
  foreach(IntPtr a in sections){DeleteCriticalSection(IntPtr.Add(a,32));Guard(a,24);Marshal.FreeHGlobal(a);cs++;}sections.Clear();
  int refs=0;if(userLibrary!=IntPtr.Zero){bool released=FreeLibrary(userLibrary);ok&=released;if(released)refs++;userLibrary=IntPtr.Zero;}
  int resourceRefs=0,gdiRefs=0;
  if(resourceModule!=IntPtr.Zero){bool released=FreeLibrary(resourceModule);ok&=released;if(released)resourceRefs++;resourceModule=IntPtr.Zero;}
  if(gdiLibrary!=IntPtr.Zero){bool released=FreeLibrary(gdiLibrary);ok&=released;if(released)gdiRefs++;gdiLibrary=IntPtr.Zero;}
  return new {registration_calls=registrationCalls,inspection_calls=inspectionCalls,unregistration_calls=unregistrationCalls,callback_calls=callbackCalls,unregistration=unregisterProof,window_created=false,
   resource_module_refs_released=resourceRefs,gdi32_module_refs_released=gdiRefs,icon_load_calls=iconCalls,cursor_load_calls=cursorCalls,stock_brush_calls=brushCalls,
   shared_icons_destroyed=0,shared_cursor_destroyed=false,stock_brush_deleted=false,critical_sections_deleted=cs,event_handles_closed=events,user32_module_refs_released=refs,set_rect_calls=geometryStep>=1?1:0,adjust_window_rect_calls=geometryStep>=2?1:0,all_owned_resources_released=ok};
 }
 static object Dispatch(Dictionary<string,object> r){string op=(string)r["op"];
  if(op=="register_class")return Register(r);
  if(op=="unregister_class"){
   Keys(r,"id","op","atom","module");if(classAtom==0 || Number(r,"atom")!=classAtom || Number(r,"module")!=Pointer(resourceModule))throw new ArgumentException("owned class identity required");
   return UnregisterOwned();
  }
  if(op=="InitializeCriticalSection"){
   Keys(r,"id","op","index","before_hex");if(sections.Count>=2 || Number(r,"index")!=sections.Count)throw new ArgumentException("next owned critical section required");
   byte[] b=Parse((string)r["before_hex"],24);IntPtr a=Buffer(b);bool initialized=false;
   try{string code;uint eax=Initialize(IntPtr.Add(a,32),out code);initialized=true;Guard(a,24);b=Bytes(IntPtr.Add(a,32),24);sections.Add(a);
    return new {hex=Hex(b),native_return_type="void",eax_bits_observed=eax,eax_is_status=false,forwarder_hex=code,forwarder_freed=true,guards_unchanged=true};
   }catch{if(initialized)DeleteCriticalSection(IntPtr.Add(a,32));Marshal.FreeHGlobal(a);throw;}
  }
  if(op=="CreateEventA"){
   Keys(r,"id","op","args");IList a=r["args"] as IList;if(sections.Count!=2 || eventHandle!=IntPtr.Zero || a==null || a.Count!=4)throw new ArgumentException("original event creation order/shape");
   foreach(object v in a)if(Convert.ToInt64(v)!=0)throw new ArgumentException("null unnamed auto-reset unsignaled event arguments");
   eventHandle=CreateEventA(IntPtr.Zero,false,false,IntPtr.Zero);if(eventHandle==IntPtr.Zero)throw new InvalidOperationException("real event creation failed");return new {result=Pointer(eventHandle)};
  }
  if(op=="GetCurrentDirectoryA"){
   Keys(r,"id","op","before_hex");if(eventHandle==IntPtr.Zero || directory!=null)throw new ArgumentException("one directory query after event required");
   byte[] b=Parse((string)r["before_hex"],525);IntPtr a=Buffer(b);try{uint n=GetCurrentDirectoryA(525,IntPtr.Add(a,32));Guard(a,525);b=Bytes(IntPtr.Add(a,32),525);
    if(n==0 || n>=250 || Length(b)!=n)throw new InvalidOperationException("bounded actual game directory required");directory=b;return new {result=n,hex=Hex(b),guards_unchanged=true};
   }finally{Marshal.FreeHGlobal(a);}
  }
  if(op=="PathAddBackslashA"){
   Keys(r,"id","op","before_hex");byte[] b=Parse((string)r["before_hex"],525);if(directory==null || path!=null || Hex(b)!=Hex(directory))throw new ArgumentException("exact owned directory before suffix required");
   IntPtr a=Buffer(b);try{IntPtr p=IntPtr.Add(a,32),result=PathAddBackslashA(p);Guard(a,525);b=Bytes(p,525);int n=Length(b);
    if(result!=IntPtr.Add(p,n) || b[n-1]!=92)throw new InvalidOperationException("real backslash result required");path=b;return new {return_offset=n,hex=Hex(b),guards_unchanged=true};
   }finally{Marshal.FreeHGlobal(a);}
  }
  if(op=="lstrcpyA" || op=="lstrcatA"){
   Keys(r,"id","op","before_hex","source_hex");if(path==null || (op=="lstrcpyA"?copies>=7:copies!=7 || concats!=0))throw new ArgumentException("original ANSI copy/concat sequence required");
   byte[] b=Parse((string)r["before_hex"],260),source=Parse((string)r["source_hex"],((string)r["source_hex"]).Length/2);
   byte[] wanted=op=="lstrcpyA"?new byte[Length(path)+1]:System.Text.Encoding.ASCII.GetBytes("SaveData\\\0");if(op=="lstrcpyA")Array.Copy(path,wanted,wanted.Length);
   if(Hex(source)!=Hex(wanted) || source.Length+(op=="lstrcatA"?Length(b):0)>260)throw new ArgumentException("original bounded ANSI source required");
   if(op=="lstrcatA" && Hex(b).Substring(0,(Length(path)+1)*2)!=Hex(path).Substring(0,(Length(path)+1)*2))throw new ArgumentException("original save directory prefix required");
   IntPtr a=Buffer(b),s=Buffer(source);try{IntPtr p=IntPtr.Add(a,32),sp=IntPtr.Add(s,32),result=op=="lstrcpyA"?lstrcpyA(p,sp):lstrcatA(p,sp);Guard(a,260);Guard(s,source.Length);
    if(result!=p || Hex(Bytes(sp,source.Length))!=Hex(source))throw new InvalidOperationException("original ANSI return/source preservation");
    if(op=="lstrcpyA")copies++;else concats++;return new {return_offset=0,hex=Hex(Bytes(p,260)),guards_unchanged=true,source_unchanged=true};
   }finally{Marshal.FreeHGlobal(a);Marshal.FreeHGlobal(s);}
  }
  if(op=="copy_title"){
   Keys(r,"id","op","before_hex","source_hex");if(sections.Count!=2 || eventHandle==IntPtr.Zero || concats!=1 || titleCopied || (string)r["source_hex"]!=Hex(titleBytes))throw new ArgumentException("original title copy order/source required");
   byte[] before=Parse((string)r["before_hex"],256);IntPtr a=Buffer(before),s=Buffer(titleBytes);
   try{IntPtr p=IntPtr.Add(a,32),sp=IntPtr.Add(s,32);IntPtr result=lstrcpyA(p,sp);Guard(a,256);Guard(s,titleBytes.Length);
    if(result!=p || Hex(Bytes(sp,titleBytes.Length))!=Hex(titleBytes))throw new InvalidOperationException("title return/source preservation");
    titleCopied=true;return new {return_offset=0,hex=Hex(Bytes(p,256)),guards_unchanged=true,source_unchanged=true};
   }finally{Marshal.FreeHGlobal(a);Marshal.FreeHGlobal(s);}
  }
  if(op=="find_window"){
   Keys(r,"id","op","class_hex","window_name");if(!titleCopied || queried || Number(r,"window_name")!=0 || (string)r["class_hex"]!=Hex(titleBytes))throw new ArgumentException("one original class/null-title query required");
   IntPtr a=Buffer(titleBytes);try{IntPtr p=IntPtr.Add(a,32),result=FindWindowA(p,IntPtr.Zero);queried=true;foundWindow=Pointer(result);Guard(a,titleBytes.Length);
    if(Hex(Bytes(p,titleBytes.Length))!=Hex(titleBytes))throw new InvalidOperationException("query input preservation");
    return new {result=Pointer(result),guards_unchanged=true,class_unchanged=true,window_owned=false,window_manipulated=false};
   }finally{Marshal.FreeHGlobal(a);}
  }
  if(op=="set_rect"){
   Keys(r,"id","op","before_hex","args");if(!queried || foundWindow!=0 || geometryStep!=0)throw new ArgumentException("actual absent-window gate and first geometry call required");
   IList args=r["args"] as IList;int[] expected={0,0,1024,768};if(args==null || args.Count!=4)throw new ArgumentException("original rectangle coordinates required");
   for(int i=0;i<4;i++)if(!(args[i] is int) && !(args[i] is long) || Convert.ToInt64(args[i])!=expected[i])throw new ArgumentException("original rectangle coordinates required");
   byte[] before=Parse((string)r["before_hex"],16);IntPtr a=Buffer(before);try{
    int result=SetRect(IntPtr.Add(a,32),0,0,1024,768);Guard(a,16);if(result==0)throw new InvalidOperationException("actual SetRect failed");
    clientRectangle=Bytes(IntPtr.Add(a,32),16);geometryStep=1;return new {result=unchecked((uint)result),hex=Hex(clientRectangle),guards_unchanged=true};
   }finally{Marshal.FreeHGlobal(a);}
  }
  if(op=="adjust_window_rect"){
   Keys(r,"id","op","before_hex","style","menu");byte[] before=Parse((string)r["before_hex"],16);
   if(geometryStep!=1 || Number(r,"style")!=0x90000000 || Number(r,"menu")!=0 || Hex(before)!=Hex(clientRectangle))throw new ArgumentException("original copied rectangle/style/no-menu required");
   IntPtr a=Buffer(before);try{int result=AdjustWindowRect(IntPtr.Add(a,32),0x90000000,0);Guard(a,16);if(result==0)throw new InvalidOperationException("actual AdjustWindowRect failed");
    byte[] after=Bytes(IntPtr.Add(a,32),16);geometryStep=2;return new {result=unchecked((uint)result),hex=Hex(after),guards_unchanged=true};
   }finally{Marshal.FreeHGlobal(a);}
  }
  if(op=="load_icon"){
   Keys(r,"id","op","module","id_value");if(geometryStep!=2 || iconCalls>=2 || Number(r,"module")!=Pointer(resourceModule) || Number(r,"id_value")!=157)throw new ArgumentException("owned original module/icon157 sequence required");
   IntPtr icon=LoadIconA(resourceModule,(IntPtr)157);if(icon==IntPtr.Zero)throw new InvalidOperationException("actual original icon load failed");iconCalls++;
   iconHandles[iconCalls-1]=Pointer(icon);return new {result=Pointer(icon),module=Pointer(resourceModule),resource_id=157,shared=true,destroy_permitted=false};
  }
  if(op=="load_cursor"){
   Keys(r,"id","op","module","id_value");if(iconCalls!=2 || cursorCalls!=0 || Number(r,"module")!=0 || Number(r,"id_value")!=32512)throw new ArgumentException("original system arrow sequence required");
   IntPtr cursor=LoadCursorA(IntPtr.Zero,(IntPtr)32512);if(cursor==IntPtr.Zero)throw new InvalidOperationException("actual system arrow load failed");cursorCalls++;
   cursorHandle=Pointer(cursor);return new {result=Pointer(cursor),shared=true,destroy_permitted=false};
  }
  if(op=="stock_brush"){
   Keys(r,"id","op","id_value");if(cursorCalls!=1 || brushCalls!=0 || Number(r,"id_value")!=4)throw new ArgumentException("original stock brush sequence required");
   IntPtr brush=GetStockObject(4);if(brush==IntPtr.Zero)throw new InvalidOperationException("actual stock brush unavailable");brushCalls++;
   brushHandle=Pointer(brush);return new {result=Pointer(brush),stock=true,delete_permitted=false};
  }
  if(op=="close"){Keys(r,"id","op");return Cleanup();}throw new ArgumentException("unsupported main-context operation");
 }
 static void Emit(object r){Console.WriteLine(json.Serialize(r));Console.Out.Flush();}
 static int Main(){try{
  if(IntPtr.Size!=4)throw new InvalidOperationException("x86 required");
  // Force the actual SHLWAPI module to load without changing any process-global directory.
  IntPtr a=Buffer(new byte[260]);try{PathAddBackslashA(IntPtr.Add(a,32));Guard(a,260);}finally{Marshal.FreeHGlobal(a);}
  userLibrary=LoadLibrary("user32.dll");if(userLibrary==IntPtr.Zero)throw new InvalidOperationException("owned user32 reference missing");
  string[] args=Environment.GetCommandLineArgs();if(args.Length!=2)throw new ArgumentException("one owned resource DLL path required");
  byte[] moduleFile=System.IO.File.ReadAllBytes(args[1]);if(Hash(moduleFile)!="1c2efa226cb52e97696477964d85bb6f0b94f727c8c3c550ef57da41beb009d7")throw new InvalidOperationException("owned resource module file SHA");
  resourceModule=LoadLibrary(args[1]);if(resourceModule==IntPtr.Zero)throw new InvalidOperationException("owned resource DLL loading failed");
  int pe=Marshal.ReadInt32(resourceModule,60);if(Marshal.ReadInt32(resourceModule,pe+24+16)!=0)throw new InvalidOperationException("resource module must have no entry");
  object icon=InspectResource(3,5,2216,"b048b9bcbddaa020bc7cd2ef2170348cabbea661307a0b257585e32df623ac47"),group=InspectResource(14,157,20,"d3f19e69796c48eac50b0b7669644b97eeb3b6c55e01d3d34e76b51b1460569b");
  var moduleName=new System.Text.StringBuilder(1024);if(GetModuleFileName(resourceModule,moduleName,1024)==0)throw new InvalidOperationException("loaded resource module path missing");
  moduleProof=new {pointer=Pointer(resourceModule),path=moduleName.ToString(),sha256=Hash(moduleFile),entry_point=0,auxiliary_resource_inspection=true,resources=new object[]{icon,group}};
  gdiLibrary=LoadLibrary("gdi32.dll");if(gdiLibrary==IntPtr.Zero)throw new InvalidOperationException("owned GDI module reference failed");
  Emit(new {ok=true,id=0,hello=new {pointer_bytes=4,acp=GetACP(),working_directory=Environment.CurrentDirectory,kernel32_path=Module("kernel32.dll"),shlwapi_path=Module("shlwapi.dll"),user32_path=Module("user32.dll"),gdi32_path=Module("gdi32.dll"),resource_module=moduleProof,owned_user32_module_reference=true,auxiliary_empty_path_module_probe=true,window_created=false}});
  string line;while((line=Console.ReadLine())!=null){long id=0;string op="";try{
   if(line.Length>8192)throw new ArgumentException("bounded request");var r=json.Deserialize<Dictionary<string,object>>(line);id=Number(r,"id");op=(string)r["op"];if(id!=sequence+1)throw new ArgumentException("sequence");sequence=id;
   object result=Dispatch(r);Emit(new {ok=true,id=id,result=result});if(op=="close")break;
  }catch(Exception e){Emit(new {ok=false,id=id,error=e.GetType().Name+": "+e.Message});}}
  return 0;
 }catch(Exception e){Emit(new {ok=false,id=0,error=e.GetType().Name+": "+e.Message});return 2;}finally{Cleanup();}}
}
