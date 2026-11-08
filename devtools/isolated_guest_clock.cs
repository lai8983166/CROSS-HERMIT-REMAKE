// Guest-only timing diagnostic; no input and no access to game memory.
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Management;
using System.Runtime.InteropServices;
using System.Web.Script.Serialization;
class IsolatedGuestClock {
 [UnmanagedFunctionPointer(CallingConvention.StdCall)] delegate ulong ReadTsc();
 [DllImport("kernel32.dll")] static extern IntPtr VirtualAlloc(IntPtr address,UIntPtr size,uint type,uint protection);
 [DllImport("kernel32.dll")] static extern bool VirtualProtect(IntPtr address,UIntPtr size,uint protection,out uint old);
 [DllImport("kernel32.dll")] static extern bool VirtualFree(IntPtr address,UIntPtr size,uint type);
 [DllImport("kernel32.dll")] static extern IntPtr GetCurrentProcess();
 [DllImport("kernel32.dll")] static extern bool FlushInstructionCache(IntPtr process,IntPtr address,UIntPtr size);
 [DllImport("kernel32.dll")] static extern IntPtr GetCurrentThread();
 [DllImport("kernel32.dll")] static extern UIntPtr SetThreadAffinityMask(IntPtr thread,UIntPtr mask);
 static void Need(bool yes,string message){if(!yes)throw new InvalidOperationException(message);}
 static int Main(string[] args){
  Need(IntPtr.Size==4 && Environment.MachineName=="CHAOMOFA-WORKER","dedicated x86 guest probe only");
  using(var q=new ManagementObjectSearcher("SELECT Manufacturer,Model,NumberOfLogicalProcessors FROM Win32_ComputerSystem")){
   int count=0;foreach(ManagementObject o in q.Get()){
    Need(((string)o["Manufacturer"]).Contains("VMware") && ((string)o["Model"]).Contains("Virtual") && Convert.ToInt32(o["NumberOfLogicalProcessors"])==2,"only dedicated two CPU VMware guest");count++;
   }Need(count==1,"one guest machine");
  }
  Need(args.Length==1,"new guest output required");string output=Path.GetFullPath(args[0]);
  Need(output.StartsWith(@"C:\ChaomofaWorker\",StringComparison.OrdinalIgnoreCase) && !File.Exists(output),"new guest output");
  var report=new Dictionary<string,object>();report["accepted"]=false;report["utc_start"]=DateTime.UtcNow.ToString("o");report["qpc_frequency"]=Stopwatch.Frequency;
  IntPtr code=IntPtr.Zero;UIntPtr original=UIntPtr.Zero;int exit=1;
  try{
   // LFENCE; RDTSC; RET. x86 unsigned 64-bit return uses EDX:EAX.
   byte[] bytes={0x0f,0xae,0xe8,0x0f,0x31,0xc3};
   code=VirtualAlloc(IntPtr.Zero,(UIntPtr)4096,0x3000,4);Need(code!=IntPtr.Zero,"own diagnostic code allocation");
   Marshal.Copy(bytes,0,code,bytes.Length);uint old;Need(VirtualProtect(code,(UIntPtr)4096,0x20,out old),"own diagnostic read/execute page");
   Need(FlushInstructionCache(GetCurrentProcess(),code,(UIntPtr)bytes.Length),"published diagnostic instruction bytes");
   var read=(ReadTsc)Marshal.GetDelegateForFunctionPointer(code,typeof(ReadTsc));
   original=SetThreadAffinityMask(GetCurrentThread(),(UIntPtr)1);Need(original!=UIntPtr.Zero,"save and bind guest thread affinity");
   var rows=new List<object>();report["processors"]=rows;
   for(int cpu=0;cpu<2;cpu++){
    Need(SetThreadAffinityMask(GetCurrentThread(),(UIntPtr)(1u<<cpu))!=UIntPtr.Zero,"bind selected virtual CPU");
    long q0=Stopwatch.GetTimestamp(),qp=q0;ulong first=read(),previous=first,last=first,min=ulong.MaxValue,max=0;long count=0,zeros=0,backwards=0,qBackwards=0;
    int tickStart=Environment.TickCount;
    do{last=read();long q=Stopwatch.GetTimestamp();if(last<previous)backwards++;else if(last==previous)zeros++;else{ulong delta=last-previous;min=Math.Min(min,delta);max=Math.Max(max,delta);}if(q<qp)qBackwards++;previous=last;qp=q;count++;}while(qp-q0<Stopwatch.Frequency/2 && count<10000000 && unchecked((uint)(Environment.TickCount-tickStart))<2000);
    double elapsed=(double)(qp-q0)/Stopwatch.Frequency;
    rows.Add(new{cpu=cpu,samples=count,zero_deltas=zeros,backwards=backwards,qpc_backwards=qBackwards,first_tsc=first,last_tsc=last,min_positive_delta=min,max_delta=max,elapsed_seconds=elapsed,tsc_hz=(last-first)/elapsed});
    Need(count>=1000 && elapsed>=0.5 && elapsed<2 && first>0 && backwards==0 && zeros==0 && qBackwards==0 && last>first,"bounded advancing TSC and monotonic QPC on each virtual CPU");
   }
   ulong prev=read();int crossBackwards=0;
   for(int i=0;i<256;i++){Need(SetThreadAffinityMask(GetCurrentThread(),(UIntPtr)(1u<<(i%2)))!=UIntPtr.Zero,"cross CPU affinity");ulong now=read();if(now<prev)crossBackwards++;prev=now;}
   report["cross_cpu_samples"]=256;report["cross_cpu_backwards"]=crossBackwards;Need(crossBackwards==0,"monotonic cross CPU TSC");
   report["timing_probe_passed"]=true;exit=0;
  }catch(Exception e){report["error"]=e.ToString();report["timing_probe_passed"]=false;}
  finally{
   if(original!=UIntPtr.Zero)report["affinity_restored"]=SetThreadAffinityMask(GetCurrentThread(),original)!=UIntPtr.Zero;
   if(code!=IntPtr.Zero)report["own_code_released"]=VirtualFree(code,UIntPtr.Zero,0x8000);
   report["utc_end"]=DateTime.UtcNow.ToString("o");
  }
  if(!report.ContainsKey("affinity_restored") || !(bool)report["affinity_restored"] || !report.ContainsKey("own_code_released") || !(bool)report["own_code_released"]){report["timing_probe_passed"]=false;report["cleanup_error"]="affinity or own executable page cleanup failed";exit=1;}
  using(var f=new FileStream(output,FileMode.CreateNew,FileAccess.Write))using(var w=new StreamWriter(f))w.Write(new JavaScriptSerializer().Serialize(report));return exit;
 }
}
