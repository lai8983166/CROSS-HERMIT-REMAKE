// Runs only inside the dedicated VMware Windows guest; never sends host input.
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

class IsolatedGuestPreflight {
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
 [DllImport("d3d8.dll")] static extern IntPtr Direct3DCreate8(uint sdk);
 [StructLayout(LayoutKind.Sequential)] struct Present {public uint Width,Height,Format,Count,Multisample,Swap;public IntPtr Window;public int Windowed,AutoDepth;public uint DepthFormat,Flags,Refresh,Interval;}
 [StructLayout(LayoutKind.Sequential)] struct Mode {public uint Width,Height,Refresh,Format;}
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] delegate uint Release(IntPtr self);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] delegate int DisplayMode(IntPtr self,uint adapter,out Mode mode);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] delegate int CreateDevice(IntPtr self,uint adapter,uint type,IntPtr window,uint flags,ref Present p,out IntPtr device);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] delegate int Clear(IntPtr self,uint count,IntPtr rect,uint flags,uint color,float z,uint stencil);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] delegate int PresentFrame(IntPtr self,IntPtr source,IntPtr destination,IntPtr overrideWindow,IntPtr dirty);
 static uint nonce;static IntPtr window;static readonly List<object> events=new List<object>();static int invalidEvents=0;
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
 static void Send(Input value){Need(GetForegroundWindow()==window,"guest probe still owns foreground");Need(SendInput(1,new Input[]{value},Marshal.SizeOf(typeof(Input)))==1,"one guest input delivered");Pump(80);}
 static Dictionary<string,object> Machine(){
  var r=new Dictionary<string,object>();
  using(var q=new ManagementObjectSearcher("SELECT Manufacturer,Model,NumberOfLogicalProcessors,TotalPhysicalMemory FROM Win32_ComputerSystem"))
   foreach(ManagementObject o in q.Get()){r["manufacturer"]=o["Manufacturer"];r["model"]=o["Model"];r["logical_processors"]=Convert.ToInt32(o["NumberOfLogicalProcessors"]);r["memory_bytes"]=Convert.ToUInt64(o["TotalPhysicalMemory"]);}
  using(var q=new ManagementObjectSearcher("SELECT UUID FROM Win32_ComputerSystemProduct"))foreach(ManagementObject o in q.Get())r["uuid"]=o["UUID"];
  using(var q=new ManagementObjectSearcher("SELECT LastBootUpTime FROM Win32_OperatingSystem"))foreach(ManagementObject o in q.Get())r["boot_utc"]=ManagementDateTimeConverter.ToDateTime((string)o["LastBootUpTime"]).ToUniversalTime().ToString("o");
  r["computer_name"]=Environment.MachineName;r["session"]=Process.GetCurrentProcess().SessionId;r["active_console_session"]=WTSGetActiveConsoleSessionId();
  Need(Environment.MachineName=="CHAOMOFA-WORKER" && ((string)r["manufacturer"]).Contains("VMware") && ((string)r["model"]).Contains("Virtual"),"only the dedicated VMware guest may send input");
  Need((int)r["logical_processors"]==2 && (ulong)r["memory_bytes"]>=3UL*1024*1024*1024 && (ulong)r["memory_bytes"]<=4UL*1024*1024*1024,"requested two CPUs and four GiB");
  Need((int)r["session"]>0 && (uint)(int)r["session"]==WTSGetActiveConsoleSessionId(),"guest logged-in interactive console, never service desktop");
  return r;
 }
 static object Graphics(bool fullscreen){
  IntPtr factory=IntPtr.Zero,device=IntPtr.Zero;var r=new Dictionary<string,object>();r["fullscreen"]=fullscreen;
  try{
   factory=Direct3DCreate8(220);Need(factory!=IntPtr.Zero,"original D3D8 factory");Mode mode;
   int hr=Method<DisplayMode>(factory,8)(factory,0,out mode);Need(hr>=0,"current display mode");
   Present pp=new Present{Width=1024,Height=768,Format=mode.Format,Count=1,Swap=1,Window=window,Windowed=fullscreen?0:1};
   hr=Method<CreateDevice>(factory,15)(factory,0,1,window,36,ref pp,out device);r["create_hr"]=hr;r["format"]=mode.Format;
   Need(hr>=0 && device!=IntPtr.Zero,"HAL D3D8 device; no reference-renderer fallback");
   hr=Method<Clear>(device,36)(device,0,IntPtr.Zero,1,0xFF204060,1,0);r["clear_hr"]=hr;Need(hr>=0,"D3D8 Clear");
   hr=Method<PresentFrame>(device,15)(device,IntPtr.Zero,IntPtr.Zero,IntPtr.Zero,IntPtr.Zero);r["present_hr"]=hr;Need(hr>=0,"D3D8 Present");Pump(100);
  }catch(Exception e){r["error"]=e.Message;}
  finally{
   if(device!=IntPtr.Zero)r["device_release"]=Method<Release>(device,2)(device);
   if(factory!=IntPtr.Zero)r["factory_release"]=Method<Release>(factory,2)(factory);
  }
  r["passed"]=!r.ContainsKey("error") && r.ContainsKey("device_release") && r.ContainsKey("factory_release") && Convert.ToUInt32(r["device_release"])==0 && Convert.ToUInt32(r["factory_release"])==0;return r;
 }
 static int Main(string[] args){
  var report=new Dictionary<string,object>();report["schema_version"]=1;report["accepted"]=false;report["game_executed"]=false;report["events"]=events;int exit=1;string output=null;
  try{
   Need(args.Length==2,"new output path and host challenge nonce required");nonce=Convert.ToUInt32(args[1],16);
   Need(IntPtr.Size==4 && Marshal.SizeOf(typeof(Present))==52,"original x86 presentation ABI");
   report["machine"]=Machine();report["nonce"]=nonce;report["pid"]=Process.GetCurrentProcess().Id;
   string candidate=Path.GetFullPath(args[0]);Need(candidate.StartsWith(@"C:\ChaomofaWorker\",StringComparison.OrdinalIgnoreCase) && !File.Exists(candidate),"new guest-owned output");output=candidate;
   using(SHA256 sha=SHA256.Create())report["executable_sha256"]=BitConverter.ToString(sha.ComputeHash(File.ReadAllBytes(System.Reflection.Assembly.GetExecutingAssembly().Location))).Replace("-","").ToLowerInvariant();
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
   var graphics=new List<object>();report["graphics"]=graphics;
   foreach(bool fullscreen in new bool[]{false,true}){var test=(Dictionary<string,object>)Graphics(fullscreen);graphics.Add(test);Need((bool)test["passed"],"D3D8 graphics preflight failed; see bounded call results");}
   report["preflight_passed"]=true;exit=0;
  }catch(Exception e){report["error"]=e.ToString();report["preflight_passed"]=false;}
  finally{if(window!=IntPtr.Zero){
   report["cleanup_release_submissions"]=SendInput(2,new Input[]{new Input{type=0,mouseFlags=4,mouseExtra=nonce},new Input{type=1,vk=0x87,keyFlags=2,keyExtra=nonce}},Marshal.SizeOf(typeof(Input)));
   report["window_destroyed"]=DestroyWindow(window);
  }}
  if(output!=null)using(var f=new FileStream(output,FileMode.CreateNew,FileAccess.Write))using(var w=new StreamWriter(f))w.Write(new JavaScriptSerializer().Serialize(report));return exit;
 }
}
