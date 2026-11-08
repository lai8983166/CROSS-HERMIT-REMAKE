// Mute only the dedicated guest before starting any original game audio.
using System;
using System.Collections.Generic;
using System.IO;
using System.Management;
using System.Runtime.InteropServices;
using System.Web.Script.Serialization;
class IsolatedGuestAudio {
 [DllImport("ole32.dll")]static extern int CoInitializeEx(IntPtr reserved,uint mode);
 [DllImport("ole32.dll")]static extern void CoUninitialize();
 [DllImport("ole32.dll")]static extern int CoCreateInstance(ref Guid cls,IntPtr outer,uint context,ref Guid iid,out IntPtr obj);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)]delegate int DefaultEndpoint(IntPtr self,int flow,int role,out IntPtr device);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)]delegate int Activate(IntPtr self,ref Guid iid,uint context,IntPtr parameters,out IntPtr result);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)]delegate int SetMute(IntPtr self,int mute,ref Guid context);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)]delegate int GetMute(IntPtr self,out int mute);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)]delegate int SetScalar(IntPtr self,float value,ref Guid context);
 [UnmanagedFunctionPointer(CallingConvention.StdCall)]delegate int GetScalar(IntPtr self,out float value);
 static T Method<T>(IntPtr p,int slot)where T:class{return Marshal.GetDelegateForFunctionPointer(Marshal.ReadIntPtr(Marshal.ReadIntPtr(p),slot*IntPtr.Size),typeof(T))as T;}
 static void Check(int h,string label){if(h<0)throw new InvalidOperationException(label+" HRESULT "+unchecked((uint)h).ToString("x8"));}
 static int Main(string[] args){
  IntPtr enumerator=IntPtr.Zero,device=IntPtr.Zero,volume=IntPtr.Zero;bool initialized=false;string output=null;int exit=1;
  var r=new Dictionary<string,object>();r["schema_version"]=1;r["host_audio_changed"]=false;
  try{
   if(args.Length!=1 || Environment.MachineName!="CHAOMOFA-WORKER")throw new InvalidOperationException("dedicated guest only");
   int machines=0;using(var q=new ManagementObjectSearcher("SELECT Manufacturer,Model FROM Win32_ComputerSystem"))
    foreach(ManagementObject o in q.Get()){machines++;if(!Convert.ToString(o["Manufacturer"]).Contains("VMware") || !Convert.ToString(o["Model"]).Contains("Virtual"))throw new InvalidOperationException("VMware guest required");}
   if(machines!=1)throw new InvalidOperationException("one actual guest machine required");
   string candidate=Path.GetFullPath(args[0]);if(!candidate.StartsWith(@"C:\ChaomofaWorker\",StringComparison.OrdinalIgnoreCase)||File.Exists(candidate))throw new InvalidOperationException("new guest evidence path");output=candidate;
   Check(CoInitializeEx(IntPtr.Zero,0),"COM init");initialized=true;
   Guid cls=new Guid("BCDE0395-E52F-467C-8E3D-C4579291692E"),iid=new Guid("A95664D2-9614-4F35-A746-DE8DB63617E6");
   Check(CoCreateInstance(ref cls,IntPtr.Zero,23,ref iid,out enumerator),"endpoint enumerator");
   Check(Method<DefaultEndpoint>(enumerator,4)(enumerator,0,0,out device),"guest render endpoint");
   iid=new Guid("5CDF2C82-841E-4546-9722-0CF74078229A");Check(Method<Activate>(device,3)(device,ref iid,23,IntPtr.Zero,out volume),"endpoint volume");
   Guid context=Guid.Empty;Check(Method<SetMute>(volume,14)(volume,1,ref context),"guest mute");
   Check(Method<SetScalar>(volume,7)(volume,0,ref context),"guest silent master level");
   int muted;float level;Check(Method<GetMute>(volume,15)(volume,out muted),"read guest mute");Check(Method<GetScalar>(volume,9)(volume,out level),"read guest level");
   if(muted!=1 || level!=0)throw new InvalidOperationException("guest audio must be silent before game launch");
   r["muted"]=true;r["master_scalar"]=level;exit=0;
  }catch(Exception e){r["error"]=e.ToString();}
  finally{
   int releases=0;foreach(IntPtr p in new IntPtr[]{volume,device,enumerator})if(p!=IntPtr.Zero){Marshal.Release(p);releases++;}
   r["caller_COM_references_released"]=releases;if(initialized)CoUninitialize();
  }
  if(output!=null)using(var f=new FileStream(output,FileMode.CreateNew,FileAccess.Write))using(var w=new StreamWriter(f))w.Write(new JavaScriptSerializer().Serialize(r));return exit;
 }
}
