// Own headless x86 synchronization leaves; no game callback or thread substitutes.
using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using System.Web.Script.Serialization;
class RetainedSchedulerPlatform {
 [DllImport("kernel32.dll")] static extern void InitializeCriticalSection(IntPtr p);
 [DllImport("kernel32.dll")] static extern void EnterCriticalSection(IntPtr p);
 [DllImport("kernel32.dll")] static extern void LeaveCriticalSection(IntPtr p);
 [DllImport("kernel32.dll")] static extern void DeleteCriticalSection(IntPtr p);
 [DllImport("kernel32.dll",SetLastError=true)] static extern IntPtr CreateEventA(IntPtr security,bool manual,bool initial,IntPtr name);
 [DllImport("kernel32.dll",SetLastError=true)] static extern bool SetEvent(IntPtr h);
 [DllImport("kernel32.dll",SetLastError=true)] static extern bool ResetEvent(IntPtr h);
 [DllImport("kernel32.dll",SetLastError=true)] static extern bool CloseHandle(IntPtr h);
 [DllImport("kernel32.dll",SetLastError=true)] static extern uint WaitForSingleObject(IntPtr h,uint milliseconds);
 static JavaScriptSerializer json=new JavaScriptSerializer();
 static Dictionary<uint,IntPtr> criticals=new Dictionary<uint,IntPtr>();
 static Dictionary<uint,int> depths=new Dictionary<uint,int>();
 static HashSet<uint> events=new HashSet<uint>();
 static uint U(IntPtr p){return unchecked((uint)p.ToInt32());}
 static IntPtr P(uint p){return new IntPtr(unchecked((int)p));}
 static uint N(Dictionary<string,object> q,string k){return Convert.ToUInt32(q[k]);}
 static void Need(bool b,string m){if(!b)throw new InvalidOperationException(m);}
 static string Hex(IntPtr p){byte[] b=new byte[24];Marshal.Copy(p,b,0,24);return BitConverter.ToString(b).Replace("-","").ToLowerInvariant();}
 static object Run(Dictionary<string,object> q){string op=(string)q["op"];
  if(op=="initialize"){uint g=N(q,"guest");Need(g==0x65001100 && criticals.Count==0,"one declared fresh manager lock");IntPtr p=Marshal.AllocHGlobal(24);InitializeCriticalSection(p);criticals.Add(g,p);depths.Add(g,0);return new {pointer=U(p),hex=Hex(p)};}
  if(op=="enter" || op=="leave" || op=="delete"){uint g=N(q,"guest");Need(criticals.ContainsKey(g),"live own manager critical");IntPtr p=criticals[g];if(op=="enter"){Need(depths[g]<4,"bounded recursion");EnterCriticalSection(p);depths[g]++;}else if(op=="leave"){Need(depths[g]>0,"balanced leave");LeaveCriticalSection(p);depths[g]--;}else{Need(depths[g]==0,"unlocked delete");DeleteCriticalSection(p);Marshal.FreeHGlobal(p);criticals.Remove(g);depths.Remove(g);return new {value=1};}return new {depth=depths[g],hex=Hex(p)};}
  if(op=="create_event"){Need(events.Count<2,"only source manager/node events");IntPtr h=CreateEventA(IntPtr.Zero,false,false,IntPtr.Zero);Need(h!=IntPtr.Zero,"CreateEventA failed");events.Add(U(h));return new {handle=U(h)};}
  if(op=="set" || op=="reset" || op=="wait" || op=="close_event"){uint h=N(q,"handle");Need(events.Contains(h),"live own event only");if(op=="wait"){uint ms=N(q,"milliseconds");Need(ms<=1000,"bounded actual event observation");return new {value=WaitForSingleObject(P(h),ms)};}bool ok=op=="set"?SetEvent(P(h)):op=="reset"?ResetEvent(P(h)):CloseHandle(P(h));Need(ok,"event operation failed");if(op=="close_event")events.Remove(h);return new {value=1};}
  if(op=="close"){Need(events.Count==0 && criticals.Count==0,"original/supplemental owners must close all resources");return new {all_owned_resources_released=true,events=0,criticals=0,forced_cleanup=false,window_created=false,thread_created=false};}
  throw new InvalidOperationException("unsupported scheduler leaf");
 }
 static void Send(object r){Console.WriteLine(json.Serialize(r));Console.Out.Flush();}
 static int Main(){try{Need(IntPtr.Size==4,"x86 only");Send(new {id=0,ok=true,hello=new {pointer_bytes=4,window_created=false,GPU_created=false,thread_created=false,directory=System.IO.Directory.GetCurrentDirectory()}});string line;while((line=Console.ReadLine())!=null){Need(line.Length<65536,"bounded request");var q=json.Deserialize<Dictionary<string,object>>(line);object result;try{result=Run(q);}catch(Exception e){Send(new {id=q["id"],ok=false,error=e.Message});continue;}Send(new {id=q["id"],ok=true,result=result});if((string)q["op"]=="close")return 0;}return 2;}catch(Exception e){Console.Error.WriteLine(e);return 3;}finally{foreach(uint h in events)CloseHandle(P(h));foreach(uint g in criticals.Keys){while(depths[g]>0){LeaveCriticalSection(criticals[g]);depths[g]--;}DeleteCriticalSection(criticals[g]);Marshal.FreeHGlobal(criticals[g]);}}}
}
