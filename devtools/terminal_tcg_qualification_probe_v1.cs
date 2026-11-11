// Dedicated QEMU qualification only. No host execution, fallback renderer, or game acceptance.
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Management;
using System.Runtime.InteropServices;
using System.Security.Cryptography;
using System.Threading;
using System.Text;
using System.Web.Script.Serialization;

class TerminalTcgQualificationProbeV1 {
 [UnmanagedFunctionPointer(CallingConvention.Winapi)] delegate IntPtr WndProc(IntPtr h,uint m,IntPtr w,IntPtr l);
 [StructLayout(LayoutKind.Sequential,CharSet=CharSet.Unicode)] struct WC {public uint size,style;public WndProc proc;public int clsExtra,wndExtra;public IntPtr instance,icon,cursor,background;public string menu,name;public IntPtr smallIcon;}
 [StructLayout(LayoutKind.Sequential)] struct Point {public int x,y;}
 [StructLayout(LayoutKind.Sequential)] struct Msg {public IntPtr hwnd;public uint message;public IntPtr wParam,lParam;public uint time;public Point pt;}
 [StructLayout(LayoutKind.Explicit,Size=28)] struct Input {
  [FieldOffset(0)]public uint type;[FieldOffset(4)]public int dx;[FieldOffset(8)]public int dy;
  [FieldOffset(16)]public uint mouseFlags;[FieldOffset(24)]public uint mouseExtra;
  [FieldOffset(4)]public ushort vk;[FieldOffset(6)]public ushort scan;
  [FieldOffset(8)]public uint keyFlags;[FieldOffset(16)]public uint keyExtra;
 }
 [DllImport("user32.dll",CharSet=CharSet.Unicode)] static extern ushort RegisterClassExW(ref WC wc);
 [DllImport("user32.dll",CharSet=CharSet.Unicode)] static extern IntPtr CreateWindowExW(uint ex,string cls,string title,uint style,int x,int y,int width,int height,IntPtr parent,IntPtr menu,IntPtr instance,IntPtr param);
 [DllImport("user32.dll")] static extern IntPtr DefWindowProcW(IntPtr h,uint m,IntPtr w,IntPtr l);
 [DllImport("user32.dll")] static extern bool ShowWindow(IntPtr h,int command);
 [DllImport("user32.dll")] static extern bool SetForegroundWindow(IntPtr h);
 [DllImport("user32.dll")] static extern IntPtr GetForegroundWindow();
 [DllImport("user32.dll")] static extern uint GetWindowThreadProcessId(IntPtr h,out uint pid);
 [DllImport("user32.dll",CharSet=CharSet.Unicode)] static extern int GetWindowTextW(IntPtr h,StringBuilder value,int count);
 [DllImport("user32.dll")] static extern IntPtr GetThreadDesktop(uint tid);
 [DllImport("user32.dll",CharSet=CharSet.Unicode)] static extern bool GetUserObjectInformationW(IntPtr h,int index,StringBuilder text,uint bytes,out uint needed);
 [DllImport("kernel32.dll")] static extern uint GetCurrentThreadId();
 [DllImport("user32.dll",SetLastError=true)] static extern IntPtr OpenInputDesktop(uint flags,bool inherit,uint access);
 [DllImport("user32.dll",SetLastError=true)] static extern bool CloseDesktop(IntPtr desktop);
 [DllImport("kernel32.dll")] static extern void SetLastError(uint error);
 [DllImport("user32.dll")] static extern bool AttachThreadInput(uint from,uint to,bool attach);
 [DllImport("user32.dll")] static extern bool DestroyWindow(IntPtr h);
 [DllImport("user32.dll")] static extern bool PeekMessageW(out Msg msg,IntPtr h,uint min,uint max,uint remove);
 [DllImport("user32.dll")] static extern bool TranslateMessage(ref Msg msg);
 [DllImport("user32.dll")] static extern IntPtr DispatchMessageW(ref Msg msg);
 [DllImport("user32.dll")] static extern uint SendInput(uint count,Input[] values,int bytes);
 [DllImport("user32.dll")] static extern IntPtr GetMessageExtraInfo();
 [DllImport("user32.dll")] static extern bool GetCursorPos(out Point point);
 [DllImport("user32.dll")] static extern int GetSystemMetrics(int index);
 [DllImport("kernel32.dll",CharSet=CharSet.Unicode)] static extern IntPtr GetModuleHandleW(string name);
 [DllImport("kernel32.dll")] static extern uint WTSGetActiveConsoleSessionId();
 [DllImport("d3d8.dll",SetLastError=true)] static extern IntPtr Direct3DCreate8(uint sdk);
 [StructLayout(LayoutKind.Sequential)] struct Present {public uint Width,Height,Format,Count,Multisample,Swap;public IntPtr Window;public int Windowed,AutoDepth;public uint DepthFormat,Flags,Refresh,Interval;}
 [StructLayout(LayoutKind.Sequential)] struct Mode {public uint Width,Height,Refresh,Format;}
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] delegate uint Release(IntPtr self);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] delegate int DisplayMode(IntPtr self,uint adapter,out Mode mode);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] delegate int CreateDevice(IntPtr self,uint adapter,uint type,IntPtr window,uint flags,ref Present p,out IntPtr device);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] delegate int Clear(IntPtr self,uint count,IntPtr rect,uint flags,uint color,float z,uint stencil);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] delegate int PresentFrame(IntPtr self,IntPtr source,IntPtr destination,IntPtr overrideWindow,IntPtr dirty);
 static bool qualifiedGuest=false;static readonly List<object> inputGuards=new List<object>();static uint nonce;static IntPtr window;static readonly List<object> events=new List<object>();static int invalidEvents=0;
 static readonly WndProc procedure=Window;
 static IntPtr Window(IntPtr h,uint m,IntPtr w,IntPtr l) {
  if(m==0x100 || m==0x101 || m==0x201 || m==0x202){
   uint extra=unchecked((uint)GetMessageExtraInfo().ToInt32());bool foreground=GetForegroundWindow()==h;
   events.Add(new {message=m,extra=extra,foreground=foreground});if(extra!=nonce || !foreground)invalidEvents++;
  }
  return DefWindowProcW(h,m,w,l);
 }
 static void Need(bool yes,string message){if(!yes)throw new InvalidOperationException(message);}
 static object Foreground(){IntPtr h=GetForegroundWindow();uint pid;uint tid=GetWindowThreadProcessId(h,out pid);var title=new StringBuilder(256);GetWindowTextW(h,title,title.Capacity);var desktop=new StringBuilder(256);uint needed;bool queried=GetUserObjectInformationW(GetThreadDesktop(GetCurrentThreadId()),2,desktop,512,out needed);return new{hwnd=h.ToInt64(),pid=pid,tid=tid,title=title.ToString(),own_desktop=desktop.ToString(),own_desktop_query_succeeded=queried,own_window=window.ToInt64(),own_pid=Process.GetCurrentProcess().Id,own_tid=GetCurrentThreadId()};}
 static T Method<T>(IntPtr obj,int index)where T:class{return Marshal.GetDelegateForFunctionPointer(Marshal.ReadIntPtr(Marshal.ReadIntPtr(obj),index*IntPtr.Size),typeof(T))as T;}
 static void Pump(int milliseconds){var clock=Stopwatch.StartNew();while(clock.ElapsedMilliseconds<milliseconds){Msg m;while(PeekMessageW(out m,IntPtr.Zero,0,0,1)){TranslateMessage(ref m);DispatchMessageW(ref m);}Thread.Sleep(2);}}
 static object CheckInputContext(){
  Need(qualifiedGuest,"dedicated guest guard previously passed");
  int session=Process.GetCurrentProcess().SessionId;uint active=WTSGetActiveConsoleSessionId();
  Need(session>0 && (uint)session==active,"current own active console session");
  IntPtr desktop=OpenInputDesktop(0,false,1);Need(desktop!=IntPtr.Zero,"open actual input desktop");
  string name=null;bool queried=false,closed=false;
  try{var text=new StringBuilder(256);uint needed;queried=GetUserObjectInformationW(desktop,2,text,512,out needed);name=text.ToString();}
  finally{closed=CloseDesktop(desktop);}
  Need(queried && name=="Default" && closed,"current input desktop Default and desktop handle closed");
  return new {session=session,active_console_session=active,input_desktop=name,input_desktop_query_succeeded=queried,input_desktop_closed=closed};
 }
 static void Send(Input value){var context=CheckInputContext();Need(GetForegroundWindow()==window,"guest probe still owns foreground");inputGuards.Add(context);Need(SendInput(1,new Input[]{value},Marshal.SizeOf(typeof(Input)))==1,"one guest input delivered");Pump(80);}
 static void MachineInto(Dictionary<string,object> r){
  r["computer_name"]=Environment.MachineName;r["session"]=Process.GetCurrentProcess().SessionId;r["active_console_session"]=WTSGetActiveConsoleSessionId();
  using(var q=new ManagementObjectSearcher("SELECT Manufacturer,Model,NumberOfLogicalProcessors,TotalPhysicalMemory FROM Win32_ComputerSystem"))
   foreach(ManagementObject o in q.Get()){r["manufacturer"]=o["Manufacturer"];r["model"]=o["Model"];r["logical_processors"]=Convert.ToInt32(o["NumberOfLogicalProcessors"]);r["memory_bytes"]=Convert.ToUInt64(o["TotalPhysicalMemory"]);}
  using(var q=new ManagementObjectSearcher("SELECT UUID FROM Win32_ComputerSystemProduct"))foreach(ManagementObject o in q.Get())r["uuid"]=o["UUID"];
  using(var q=new ManagementObjectSearcher("SELECT LastBootUpTime FROM Win32_OperatingSystem"))foreach(ManagementObject o in q.Get())r["boot_utc"]=ManagementDateTimeConverter.ToDateTime((string)o["LastBootUpTime"]).ToUniversalTime().ToString("o");
  r["computer_name"]=Environment.MachineName;r["session"]=Process.GetCurrentProcess().SessionId;r["active_console_session"]=WTSGetActiveConsoleSessionId();
 }
 static void Guard(Dictionary<string,object> r){
  Need((string)r["computer_name"]=="CHAOMOFA-WORKER" && (string)r["manufacturer"]=="QEMU" && new Guid((string)r["uuid"])==new Guid("626d1a20-6383-4cd3-85d5-6c9831d6f941"),"only dedicated QEMU UUID may send input");
  Need((int)r["logical_processors"]==2 && (ulong)r["memory_bytes"]>=3UL*1024*1024*1024 && (ulong)r["memory_bytes"]<=4UL*1024*1024*1024,"requested two CPUs and four GiB");
  Need((int)r["session"]>0 && (uint)(int)r["session"]==(uint)r["active_console_session"],"own active console");qualifiedGuest=true;
 }
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] delegate uint AdapterCount(IntPtr self);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] delegate int AdapterIdentifier(IntPtr self,uint adapter,uint flags,IntPtr identifier);
 static object Graphics(bool fullscreen){
  IntPtr factory=IntPtr.Zero,device=IntPtr.Zero;var r=new Dictionary<string,object>();r["fullscreen"]=fullscreen;
  try{
   r["sdk_version"]=220;r["device_type"]=1;r["behavior_flags"]=36;r["fallback_attempted"]=false;
   r["factory_attempted"]=true;SetLastError(0);factory=Direct3DCreate8(220);r["factory_last_error"]=Marshal.GetLastWin32Error();r["factory_created"]=factory!=IntPtr.Zero;
   Need(factory!=IntPtr.Zero,"original D3D8 Direct3DCreate8 returned NULL");
   uint adapters=Method<AdapterCount>(factory,4)(factory);r["adapter_count"]=adapters;Need(adapters>0,"D3D8 adapter count");
   IntPtr identifier=Marshal.AllocHGlobal(1100);
   try{for(int i=0;i<1100;i++)Marshal.WriteByte(identifier,i,0);int ihr=Method<AdapterIdentifier>(factory,5)(factory,0,0,identifier);r["adapter_identifier_hr"]=ihr;
    if(ihr>=0)r["adapter_identifier"]=new {driver=Marshal.PtrToStringAnsi(identifier),description=Marshal.PtrToStringAnsi(IntPtr.Add(identifier,512)),driver_version=Marshal.ReadInt64(identifier,1024),vendor_id=Marshal.ReadInt32(identifier,1032),device_id=Marshal.ReadInt32(identifier,1036),subsystem_id=Marshal.ReadInt32(identifier,1040),revision=Marshal.ReadInt32(identifier,1044)};
   }finally{Marshal.FreeHGlobal(identifier);r["adapter_identifier_buffer_freed"]=true;}
   Mode mode;
   int hr=Method<DisplayMode>(factory,8)(factory,0,out mode);r["display_mode_hr"]=hr;Need(hr>=0,"current display mode");
   Present pp=new Present{Width=1024,Height=768,Format=mode.Format,Count=1,Swap=1,Window=window,Windowed=fullscreen?0:1};
   hr=Method<CreateDevice>(factory,15)(factory,0,1,window,36,ref pp,out device);r["create_hr"]=hr;r["device_created"]=device!=IntPtr.Zero;r["format"]=mode.Format;
   Need(hr>=0 && device!=IntPtr.Zero,"HAL D3D8 device; no reference-renderer fallback");
   hr=Method<Clear>(device,36)(device,0,IntPtr.Zero,1,0xFF204060,1,0);r["clear_hr"]=hr;Need(hr>=0,"D3D8 Clear");
   hr=Method<PresentFrame>(device,15)(device,IntPtr.Zero,IntPtr.Zero,IntPtr.Zero,IntPtr.Zero);r["present_hr"]=hr;Need(hr>=0,"D3D8 Present");Pump(100);
  }catch(Exception e){r["error"]=e.ToString();r["exception_type"]=e.GetType().FullName;r["exception_hresult"]=e.HResult;}
  finally{
   if(device!=IntPtr.Zero)try{r["device_release"]=Method<Release>(device,2)(device);}catch(Exception e){r["error"]="device release: "+e.ToString();}
   if(factory!=IntPtr.Zero)try{r["factory_release"]=Method<Release>(factory,2)(factory);}catch(Exception e){r["error"]="factory release: "+e.ToString();}
  }
  r["passed"]=!r.ContainsKey("error") && r.ContainsKey("device_release") && r.ContainsKey("factory_release") && Convert.ToUInt32(r["device_release"])==0 && Convert.ToUInt32(r["factory_release"])==0;return r;
 }
 static int Main(string[] args){
  var report=new Dictionary<string,object>();report["schema"]="terminal-tcg-qualification-guest-v1";report["input_guards"]=inputGuards;report["graphics"]=new List<object>();report["accepted"]=false;report["game_executed"]=false;report["events"]=events;int exit=1;string output=null;
  try{
   Need(args.Length==3,"new output path, challenge nonce, source SHA256 required");
   string candidate=Path.GetFullPath(args[0]);Need(candidate.StartsWith(@"C:\ChaomofaWorker\",StringComparison.OrdinalIgnoreCase) && !File.Exists(candidate),"new guest-owned output");output=candidate;
   report["machine"]=new Dictionary<string,object>();MachineInto((Dictionary<string,object>)report["machine"]);
   nonce=Convert.ToUInt32(args[1],16);Need(nonce>=0x40000000 && nonce<=0x5fffffff,"challenge domain");report["nonce"]=nonce;
   Need(System.Text.RegularExpressions.Regex.IsMatch(args[2],"^[0-9a-f]{64}$"),"source SHA256");report["source_sha256"]=args[2];report["pid"]=Process.GetCurrentProcess().Id;
   using(SHA256 sha=SHA256.Create())report["executable_sha256"]=BitConverter.ToString(sha.ComputeHash(File.ReadAllBytes(System.Reflection.Assembly.GetExecutingAssembly().Location))).Replace("-","").ToLowerInvariant();
   Guard((Dictionary<string,object>)report["machine"]);report["guest_guard_passed"]=true;
   Need(IntPtr.Size==4 && Marshal.SizeOf(typeof(Present))==52,"original x86 presentation ABI");
   report["initial_input_context"]=CheckInputContext();
   var wc=new WC{size=(uint)Marshal.SizeOf(typeof(WC)),proc=procedure,instance=GetModuleHandleW(null),name="ChaomofaInputIsolationProbe"};
   Need(RegisterClassExW(ref wc)!=0,"register guest-only window");
   window=CreateWindowExW(0,wc.name,"Dedicated guest input preflight",0x10CF0000,40,40,1100,850,IntPtr.Zero,IntPtr.Zero,wc.instance,IntPtr.Zero);
   Need(window!=IntPtr.Zero,"guest window");report["foreground_before"]=Foreground();ShowWindow(window,5);
   bool focused=SetForegroundWindow(window);report["set_foreground_result"]=focused;
   if(!focused){
    IntPtr foregroundWindow=GetForegroundWindow();uint foregroundPid;uint foregroundTid=GetWindowThreadProcessId(foregroundWindow,out foregroundPid);uint ownTid=GetCurrentThreadId();
    int targetSession=Process.GetProcessById((int)foregroundPid).SessionId;int ownSession=Process.GetCurrentProcess().SessionId;
    report["guest_queue_binding"]=new{own_tid=ownTid,target_hwnd=foregroundWindow.ToInt64(),target_pid=foregroundPid,target_tid=foregroundTid,target_session=targetSession,own_session=ownSession};
    Need(foregroundTid!=0 && foregroundTid!=ownTid && targetSession==ownSession,"foreground queue belongs to this guest console session");
    bool attached=AttachThreadInput(ownTid,foregroundTid,true);report["guest_queue_attached"]=attached;Need(attached,"temporarily attach guest foreground queue");
    try{report["attached_set_foreground_result"]=SetForegroundWindow(window);}
    finally{bool detached=AttachThreadInput(ownTid,foregroundTid,false);report["guest_queue_detached"]=detached;Need(detached,"detach guest foreground queue");}
   }
   Pump(300);report["foreground_after"]=Foreground();Need(GetForegroundWindow()==window,"guest foreground acquired");
   Send(new Input{type=0,dx=(int)((180.5*65536)/GetSystemMetrics(0)),dy=(int)((180.5*65536)/GetSystemMetrics(1)),mouseFlags=0x8001,mouseExtra=nonce});
   Point cursor;Need(GetCursorPos(out cursor) && cursor.x==180 && cursor.y==180,"exact guest cursor target");
   Send(new Input{type=0,mouseFlags=2,mouseExtra=nonce});Send(new Input{type=0,mouseFlags=4,mouseExtra=nonce});
   Send(new Input{type=1,vk=0x87,keyExtra=nonce});Send(new Input{type=1,vk=0x87,keyFlags=2,keyExtra=nonce});
   Need(events.Count==4 && invalidEvents==0,"exact tagged mouse and F24 message pairs in guest foreground");
   report["input_messages_received"]=true;
   var graphics=(List<object>)report["graphics"];
   foreach(bool fullscreen in new bool[]{false,true}){var test=(Dictionary<string,object>)Graphics(fullscreen);graphics.Add(test);}
   foreach(Dictionary<string,object> test in graphics)Need((bool)test["passed"],"HAL D3D8 qualification failed; see bounded call results");
   report["preflight_passed"]=true;exit=0;
  }catch(Exception e){report["error"]=e.ToString();report["preflight_passed"]=false;}
  finally{if(window!=IntPtr.Zero){
   try{report["cleanup_input_context"]=CheckInputContext();Need(GetForegroundWindow()==window,"cleanup only while own foreground");report["cleanup_foreground_owned"]=true;
    report["cleanup_release_submissions"]=SendInput(2,new Input[]{new Input{type=0,mouseFlags=4,mouseExtra=nonce},new Input{type=1,vk=0x87,keyFlags=2,keyExtra=nonce}},Marshal.SizeOf(typeof(Input)));
   }catch(Exception e){report["cleanup_input_error"]=e.ToString();}
   report["window_destroyed"]=DestroyWindow(window);
  }}
  if(output!=null)using(var f=new FileStream(output,FileMode.CreateNew,FileAccess.Write))using(var w=new StreamWriter(f))w.Write(new JavaScriptSerializer().Serialize(report));return exit;
 }
}
