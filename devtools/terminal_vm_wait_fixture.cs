// Self-owned deterministic FX/wait fixture. No game, input or debugger APIs.
using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Runtime.InteropServices;
using System.Security.Cryptography;
using System.Threading;
using System.Web.Script.Serialization;
class VMWaitFixture {
 [DllImport("kernel32.dll",SetLastError=true)] static extern IntPtr VirtualAlloc(IntPtr a,UIntPtr n,uint t,uint p);
 [DllImport("kernel32.dll",SetLastError=true)] static extern bool VirtualProtect(IntPtr a,UIntPtr n,uint p,out uint old);
 [DllImport("kernel32.dll",SetLastError=true)] static extern bool VirtualFree(IntPtr a,UIntPtr n,uint t);
 [DllImport("kernel32.dll")] static extern IntPtr GetCurrentProcess();
 [DllImport("kernel32.dll")] static extern IntPtr GetCurrentThread();
 [DllImport("kernel32.dll")] static extern uint GetCurrentProcessId();
 [DllImport("kernel32.dll")] static extern uint GetCurrentThreadId();
 [DllImport("kernel32.dll",SetLastError=true)] static extern UIntPtr SetThreadAffinityMask(IntPtr t,UIntPtr m);
 [DllImport("kernel32.dll")] static extern bool IsWow64Process(IntPtr p,out bool w);
 [DllImport("kernel32.dll",CharSet=CharSet.Unicode)] static extern IntPtr GetModuleHandle(string n);
 [DllImport("kernel32.dll",CharSet=CharSet.Ansi)] static extern IntPtr GetProcAddress(IntPtr m,string n);
 [DllImport("kernel32.dll")] static extern bool FlushInstructionCache(IntPtr p,IntPtr a,UIntPtr n);
 [DllImport("kernel32.dll")] static extern IntPtr CreateEvent(IntPtr a,bool manual,bool initial,IntPtr name);
 [DllImport("kernel32.dll")] static extern bool SetEvent(IntPtr h);
 [DllImport("kernel32.dll")] static extern uint WaitForSingleObject(IntPtr h,uint ms);
 [DllImport("kernel32.dll")] static extern bool CloseHandle(IntPtr h);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] delegate uint WaitCall(IntPtr h,IntPtr timeout);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] delegate void CounterCall();
 static JavaScriptSerializer Json=new JavaScriptSerializer();
 static uint Addr(IntPtr p){return unchecked((uint)p.ToInt32());}
 static byte[] Read(IntPtr p,int n){byte[] b=new byte[n];Marshal.Copy(p,b,0,n);return b;}
 static string Hex(byte[] b){return BitConverter.ToString(b).Replace("-","").ToLowerInvariant();}
 static string Hash(byte[] b){using(SHA256 s=SHA256.Create())return Hex(s.ComputeHash(b));}
 static void Need(bool v,string s){if(!v)throw new Exception(s+" win32="+Marshal.GetLastWin32Error());}
 static void Save(string path,object r){using(FileStream f=new FileStream(path,FileMode.CreateNew))using(StreamWriter w=new StreamWriter(f))w.Write(Json.Serialize(r));}
 static void Gate(string path){DateTime start=DateTime.UtcNow;while(!File.Exists(path)){Need((DateTime.UtcNow-start).TotalSeconds<150,"bounded owned gate");Thread.Sleep(10);}}
 public static int Main(string[] args){
  if(args.Length!=2||args[0]!="--owned-vmm-fixture")return 2;
  string dir=Path.GetFullPath(args[1]);string output=Path.Combine(dir,"result.json");
  if(File.Exists(output)||File.Exists(Path.Combine(dir,"ready.json")))return 2;
  var report=new Dictionary<string,object>();report["kind"]="owned_wow64_vmm_wait_fixture";
  report["accepted"]=false;report["original_game_observed"]=false;report["error"]=null;
  var cleanup=new List<string>();report["cleanup_errors"]=cleanup;
  IntPtr data=IntPtr.Zero,code=IntPtr.Zero,timeout=IntPtr.Zero,request=IntPtr.Zero,response=IntPtr.Zero,nt=IntPtr.Zero;
  Thread peer=null;Thread[] counters=new Thread[2];UIntPtr previous=UIntPtr.Zero;
  bool stop=false,peerDone=false;int signals=0;string peerError=null;uint[] counterTids=new uint[2];
  ManualResetEvent done=new ManualResetEvent(false);
  Thread watchdog=new Thread(delegate(){if(!done.WaitOne(180000)){try{Save(output+".watchdog.json",new {accepted=false,forced_self_exit=true});}catch{}Environment.Exit(124);}});
  watchdog.IsBackground=true;watchdog.Start();
  try{
   bool wow;Need(IntPtr.Size==4&&IsWow64Process(GetCurrentProcess(),out wow)&&wow,"actual WOW64 helper");
   var manifest=Json.Deserialize<Dictionary<string,object>>(File.ReadAllText(Path.Combine(dir,"manifest.json")));
   byte[] template=File.ReadAllBytes(Path.Combine(dir,"fixture.bin"));byte[] source=File.ReadAllBytes(Path.Combine(dir,"terminal_vm_wait_fixture.cs"));
   Need(Hash(template)==(string)manifest["template_sha256"]&&Hash(source)==(string)manifest["source_sha256"],"exact fixture inputs");
   report["source_sha256"]=Hash(source);report["template_sha256"]=Hash(template);
   data=VirtualAlloc(IntPtr.Zero,(UIntPtr)16384,0x3000,4);code=VirtualAlloc(IntPtr.Zero,(UIntPtr)4096,0x3000,4);
   Need(data!=IntPtr.Zero&&code!=IntPtr.Zero,"private fixture buffers");
   nt=GetProcAddress(GetModuleHandle("ntdll.dll"),"NtWaitForSingleObject");Need(nt!=IntPtr.Zero,"actual NtWait export");
   byte[] stub=Read(nt,32);Need(Hex(stub).StartsWith("b804000d00")&&stub[12]==0xc2&&stub[13]==12,"unchanged selector13 NtWait");
   report["nt_wait_before"]=Hex(stub);
   byte[] machine=(byte[])template.Clone();
   foreach(object item in (ArrayList)manifest["patches"]){var p=(Dictionary<string,object>)item;uint v=((string)p["symbol"]=="data"?Addr(data):Addr(nt))+Convert.ToUInt32(p["addend"]);Array.Copy(BitConverter.GetBytes(v),0,machine,Convert.ToInt32(p["offset"]),4);}
   Marshal.Copy(machine,0,code,machine.Length);uint old;Need(VirtualProtect(code,(UIntPtr)4096,0x20,out old)&&old==4,"private code RX");
   Need(FlushInstructionCache(GetCurrentProcess(),code,(UIntPtr)machine.Length),"private instruction cache");
   for(int i=0;i<128;i++)Marshal.WriteByte(data,0x400+i,(byte)(i*3+7));
   request=CreateEvent(IntPtr.Zero,false,false,IntPtr.Zero);response=CreateEvent(IntPtr.Zero,false,false,IntPtr.Zero);
   Need(request!=IntPtr.Zero&&response!=IntPtr.Zero,"fresh owned events");timeout=Marshal.AllocHGlobal(8);
   WaitCall call=(WaitCall)Marshal.GetDelegateForFunctionPointer(code,typeof(WaitCall));
   previous=SetThreadAffinityMask(GetCurrentThread(),(UIntPtr)1);Need(previous!=UIntPtr.Zero,"pin tested thread to virtual CPU0");
   ArrayList offsets=(ArrayList)manifest["counter_offsets"];
   for(int j=0;j<2;j++){int index=j;CounterCall counter=(CounterCall)Marshal.GetDelegateForFunctionPointer(IntPtr.Add(code,Convert.ToInt32(offsets[j])),typeof(CounterCall));
    counters[j]=new Thread(delegate(){counterTids[index]=GetCurrentThreadId();UIntPtr prior=SetThreadAffinityMask(GetCurrentThread(),(UIntPtr)(1u<<index));if(prior==UIntPtr.Zero){peerError="counter affinity";return;}counter();SetThreadAffinityMask(GetCurrentThread(),prior);GC.KeepAlive(counter);});counters[j].IsBackground=true;counters[j].Start();}
   peer=new Thread(delegate(){try{for(int i=0;i<3;i++){uint w=WaitForSingleObject(request,150000);if(stop)return;Need(w==0,"peer request");Thread.Sleep(50);Need(SetEvent(response),"peer response");Interlocked.Increment(ref signals);}peerDone=true;}catch(Exception e){peerError=e.ToString();}});peer.IsBackground=true;peer.Start();
   Thread.Sleep(20);
   var ready=new Dictionary<string,object>();ready["pid"]=GetCurrentProcessId();ready["tid"]=GetCurrentThreadId();ready["counter_tids"]=counterTids;
   ready["nt_wait"]=Addr(nt);ready["return_pc"]=Addr(nt)+12;ready["nt_wait_before"]=Hex(stub);ready["data"]=Addr(data);ready["code"]=Addr(code);
   ready["code_hex"]=Hex(machine);ready["postcall_pc"]=Addr(code)+Convert.ToUInt32(manifest["postcall_offset"]);ready["event_handle"]=Addr(response);ready["timeout_pointer"]=Addr(timeout);
   ready["source_sha256"]=Hash(source);ready["template_sha256"]=Hash(template);ready["accepted"]=false;
   Save(Path.Combine(dir,"ready.json"),ready);report["ready"]=ready;Gate(Path.Combine(dir,"go"));
   var returns=new List<uint>();report["returns"]=returns;
   for(int i=0;i<4;i++){
    Marshal.WriteInt64(timeout,i==3?0:-20000000L);if(i<3)Need(SetEvent(request),"request signal");
    uint value=call(response,timeout);returns.Add(value);Need(value==(i==3?258u:0u),"actual original wait return");
    Save(Path.Combine(dir,"returned-"+i+".json"),new {index=i,value=value});Gate(Path.Combine(dir,"ack-"+i));
   }
   Need(peer.Join(2000)&&peerDone&&signals==3&&peerError==null,"three controlled peer responses");
   report["code_after"]=Hex(Read(code,machine.Length));GC.KeepAlive(call);
  }catch(Exception e){report["error"]=e.ToString();}
  finally{
   stop=true;if(request!=IntPtr.Zero)SetEvent(request);if(data!=IntPtr.Zero)Marshal.WriteInt32(data,0x308,1);
   if(peer!=null&&peer.IsAlive&&!peer.Join(2500))cleanup.Add("peer remains active");
   foreach(Thread c in counters)if(c!=null&&c.IsAlive&&!c.Join(2500))cleanup.Add("counter remains active");
   report["signals"]=signals;report["peer_completed"]=peerDone;report["peer_error"]=peerError;
   if(nt!=IntPtr.Zero)report["nt_wait_after"]=Hex(Read(nt,32));if(data!=IntPtr.Zero)report["data_hex"]=Hex(Read(data,16384));
   bool closed=true,released=true;if(cleanup.Count==0){if(request!=IntPtr.Zero)closed&=CloseHandle(request);if(response!=IntPtr.Zero)closed&=CloseHandle(response);
    if(code!=IntPtr.Zero)released&=VirtualFree(code,UIntPtr.Zero,0x8000);if(data!=IntPtr.Zero)released&=VirtualFree(data,UIntPtr.Zero,0x8000);if(timeout!=IntPtr.Zero)Marshal.FreeHGlobal(timeout);
   }else{closed=false;released=false;}
   if(previous!=UIntPtr.Zero)Need(SetThreadAffinityMask(GetCurrentThread(),previous)!=UIntPtr.Zero,"restore own affinity");
   report["handles_closed"]=closed;report["buffers_released"]=released;done.Set();watchdog.Join(1000);done.Dispose();report["watchdog_disarmed"]=true;
   Save(output,report);
  }
  return report["error"]==null&&cleanup.Count==0?0:1;
 }
}
