// Owned x86 fixture: an unchanged debugger parent, an ordinary TLS/file worker.
// The worker never notifies or waits for the observer. Only CreateFile may block.
using System;
using System.IO;
using System.Text;
using System.Threading;
using System.Diagnostics;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using System.Web.Script.Serialization;

class OplockFixture {
 [DllImport("kernel32.dll")] static extern uint GetCurrentProcessId();
 [DllImport("kernel32.dll")] static extern uint GetCurrentThreadId();
 [DllImport("kernel32.dll")] static extern uint TlsAlloc();
 [DllImport("kernel32.dll")] static extern bool TlsFree(uint i);
 [DllImport("kernel32.dll")] static extern bool TlsSetValue(uint i, IntPtr p);
 [DllImport("kernel32.dll")] static extern IntPtr TlsGetValue(uint i);
 [DllImport("kernel32.dll")] static extern IntPtr GetProcessHeap();
 [DllImport("kernel32.dll")] static extern IntPtr HeapAlloc(IntPtr h,uint f,UIntPtr n);
 [DllImport("kernel32.dll")] static extern bool HeapFree(IntPtr h,uint f,IntPtr p);
 [DllImport("kernel32.dll",EntryPoint="CreateFileA",SetLastError=true,CharSet=CharSet.Ansi)]
 static extern IntPtr OpenFile(string p,uint a,uint s,IntPtr sa,uint d,uint f,IntPtr t);
 [DllImport("kernel32.dll",SetLastError=true)] static extern bool ReadFile(IntPtr h,byte[] b,uint n,out uint got,IntPtr o);
 [DllImport("kernel32.dll",SetLastError=true)] static extern bool CloseHandle(IntPtr h);
 [DllImport("ntdll.dll")] static extern int NtQueryInformationProcess(IntPtr h,uint c,out IntPtr v,uint n,IntPtr r);
 [StructLayout(LayoutKind.Sequential,CharSet=CharSet.Unicode)] struct SI {
  public uint cb; public string reserved,desktop,title; public uint x,y,w,h,xc,yc,fill,flags;
  public ushort show,cb2; public IntPtr reserved2,input,output,error;
 }
 [StructLayout(LayoutKind.Sequential)] struct PI { public IntPtr process,thread; public uint pid,tid; }
 [DllImport("kernel32.dll",SetLastError=true,CharSet=CharSet.Unicode)]
 static extern bool CreateProcess(string app,StringBuilder cmd,IntPtr p,IntPtr t,bool inherit,uint flags,IntPtr env,string cwd,ref SI si,out PI pi);
 [DllImport("kernel32.dll",SetLastError=true)] static extern bool WaitForDebugEvent(IntPtr e,uint ms);
 [DllImport("kernel32.dll",SetLastError=true)] static extern bool ContinueDebugEvent(uint p,uint t,uint code);
 [DllImport("kernel32.dll")] static extern bool TerminateProcess(IntPtr h,uint code);
 [DllImport("kernel32.dll")] static extern uint WaitForSingleObject(IntPtr h,uint ms);
 [DllImport("kernel32.dll")] static extern bool GetExitCodeProcess(IntPtr h,out uint code);
 [DllImport("kernel32.dll",CharSet=CharSet.Unicode)] static extern IntPtr GetModuleHandle(string name);
 [DllImport("kernel32.dll",CharSet=CharSet.Ansi)] static extern IntPtr GetProcAddress(IntPtr m,string name);
 static uint U(IntPtr p) { return unchecked((uint)p.ToInt32()); }
 static void Check(bool v,string s) { if(!v)throw new Exception(s+":"+Marshal.GetLastWin32Error()); }
 static void Save(string path,object v) { File.WriteAllText(path,new JavaScriptSerializer().Serialize(v),new UTF8Encoding(false)); }
 static int Child(string dir) {
  uint index=TlsAlloc(); Check(index<64,"TLS slot"); Exception failure=null; object result=null;
  Thread worker=new Thread(delegate() {
   IntPtr heap=GetProcessHeap(),p=IntPtr.Zero,h=new IntPtr(-1); uint tid=GetCurrentThreadId(),pid=GetCurrentProcessId();
   bool cleared=false,freed=false; long ready=0,before=0,after=0,ended=0; uint got=0; byte[] read=new byte[64];
   try {
    p=HeapAlloc(heap,8,new UIntPtr(116));Check(p!=IntPtr.Zero,"allocate");
    byte[] bytes=new byte[116];for(int n=0;n<bytes.Length;n++)bytes[n]=(byte)((n*13+7)&255);
    uint[] words={0x544C5350,pid,tid,index,0x1234ABCD,U(p)};
    Buffer.BlockCopy(words,0,bytes,0,24);Marshal.Copy(bytes,0,p,116);
    IntPtr debug;Check(NtQueryInformationProcess(new IntPtr(-1),7,out debug,4,IntPtr.Zero)==0,"debug port query");
    uint ntCreate=U(GetProcAddress(GetModuleHandle("ntdll.dll"),"NtCreateFile"));Check(ntCreate!=0,"original NtCreateFile export");
    Save(Path.Combine(dir,"worker.json"),new {pid,tid,index,pointer=U(p),debug_port=U(debug),frequency=Stopwatch.Frequency,nt_create_file=ntCreate});
    Check(TlsSetValue(index,p),"TLS set");ready=Stopwatch.GetTimestamp();
    before=Stopwatch.GetTimestamp();h=OpenFile(Path.Combine(dir,"payload.bin"),0x80000000,1,IntPtr.Zero,3,1,IntPtr.Zero);
    after=Stopwatch.GetTimestamp();Check(h!=new IntPtr(-1),"ordinary read open");
    Check(ReadFile(h,read,64,out got,IntPtr.Zero)&&got==64,"read exact data");Check(CloseHandle(h),"close ordinary read");h=new IntPtr(-1);
   } catch(Exception e) {failure=e;}
   finally {
    if(h!=new IntPtr(-1)&&!CloseHandle(h)&&failure==null)failure=new Exception("cleanup read handle");
    cleared=TlsSetValue(index,IntPtr.Zero)&&TlsGetValue(index)==IntPtr.Zero;
    if(p!=IntPtr.Zero)freed=HeapFree(heap,0,p);ended=Stopwatch.GetTimestamp();
    result=new {pid,tid,index,pointer=U(p),ready,before,after,ended,frequency=Stopwatch.Frequency,
     data_hex=BitConverter.ToString(read).Replace("-","").ToLowerInvariant(),got,cleared,freed,error=failure==null?null:failure.ToString()};
   }
  });
  worker.Start();Check(worker.Join(12000),"bounded worker join");bool tlsFreed=TlsFree(index);
  Save(Path.Combine(dir,"child.json"),new {result,tls_freed=tlsFreed});return failure==null&&tlsFreed?0:2;
 }
 static int Parent(string dir) {
  PI pi=new PI();SI si=new SI();si.cb=(uint)Marshal.SizeOf(si);si.flags=1;si.show=0;
  bool created=false,exited=false,pending=false,forced=false;uint pendingPid=0,pendingTid=0,pendingStatus=0x10002;
  IntPtr buffer=Marshal.AllocHGlobal(96);var events=new List<object>();var cleanup=new List<string>();string error=null;uint exitCode=999;
  try {
   string exe=System.Reflection.Assembly.GetExecutingAssembly().Location;
   Check(CreateProcess(exe,new StringBuilder("\""+exe+"\" child \""+dir+"\""),IntPtr.Zero,IntPtr.Zero,false,0x08000002,IntPtr.Zero,dir,ref si,out pi),"create debug child");created=true;
   Save(Path.Combine(dir,"parent.json"),new {parent_pid=GetCurrentProcessId(),child_pid=pi.pid,child_main_tid=pi.tid});
   var clock=Stopwatch.StartNew();
   while(clock.ElapsedMilliseconds<15000&&events.Count<512) {
    if(!WaitForDebugEvent(buffer,100)){Check(Marshal.GetLastWin32Error()==121,"debug wait");continue;}
    uint code=(uint)Marshal.ReadInt32(buffer),pid=(uint)Marshal.ReadInt32(buffer,4),tid=(uint)Marshal.ReadInt32(buffer,8);
    uint value=(uint)Marshal.ReadInt32(buffer,12),status=0x10002;
    if(code==1)status=(value==0x80000003||value==0x4000001F)?0x10002u:0x80010001u;
    pending=true;pendingPid=pid;pendingTid=tid;pendingStatus=status;
    if((code==3||code==6)&&value!=0)Check(CloseHandle(new IntPtr(unchecked((int)value))),"debug file close");
    events.Add(new {code,pid,tid,value,status,qpc=Stopwatch.GetTimestamp()});
    Check(ContinueDebugEvent(pid,tid,status),"original parent continue");pending=false;
    if(code==5){exited=true;break;}
   }
   Check(exited&&WaitForSingleObject(pi.process,2000)==0,"normal child completion");Check(GetExitCodeProcess(pi.process,out exitCode),"child exit query");
  } catch(Exception e) {error=e.ToString();}
  finally {
   if(created&&!exited){
    forced=true;
    if(!TerminateProcess(pi.process,93))cleanup.Add("terminate child");
    if(pending&&!ContinueDebugEvent(pendingPid,pendingTid,pendingStatus))cleanup.Add("continue pending event");
    var drain=Stopwatch.StartNew();
    while(!exited&&drain.ElapsedMilliseconds<2000){
     if(!WaitForDebugEvent(buffer,50)){if(Marshal.GetLastWin32Error()!=121){cleanup.Add("drain wait");break;}continue;}
     uint c=(uint)Marshal.ReadInt32(buffer),p=(uint)Marshal.ReadInt32(buffer,4),t=(uint)Marshal.ReadInt32(buffer,8),v=(uint)Marshal.ReadInt32(buffer,12);
     uint s=c==1?0x80010001u:0x10002u;
     if((c==3||c==6)&&v!=0&&!CloseHandle(new IntPtr(unchecked((int)v))))cleanup.Add("drain file close");
     events.Add(new {code=c,pid=p,tid=t,value=v,status=s,qpc=Stopwatch.GetTimestamp(),drain=true});
     if(!ContinueDebugEvent(p,t,s)){cleanup.Add("drain continue");break;}
     exited=c==5;
    }
    if(!exited||WaitForSingleObject(pi.process,250)!=0)cleanup.Add("child not drained/signaled");
   }
   if(created){if(!CloseHandle(pi.thread))cleanup.Add("parent thread handle");if(!CloseHandle(pi.process))cleanup.Add("parent process handle");}Marshal.FreeHGlobal(buffer);
   Save(Path.Combine(dir,"debugger.json"),new {parent_pid=GetCurrentProcessId(),child_pid=pi.pid,exited,exit_code=exitCode,events,error,forced,cleanup});
  }
  return error==null&&exitCode==0?0:3;
 }
 [STAThread] static int Main(string[] args) {
  try {if(args.Length!=2)return 4;return args[0]=="child"?Child(args[1]):Parent(args[1]);}
  catch(Exception e) {if(args.Length==2)Save(Path.Combine(args[1],"fatal.json"),new {error=e.ToString()});return 5;}
 }
}
