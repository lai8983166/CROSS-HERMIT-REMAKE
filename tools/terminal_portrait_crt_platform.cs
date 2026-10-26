// Headless x86 API owner. No windows, input, game memory or GPU interfaces.
using System;
using System.IO;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using System.Web.Script.Serialization;
class TerminalPortraitCrtPlatform {
 [DllImport("kernel32.dll",SetLastError=true)] static extern IntPtr HeapCreate(uint f,UIntPtr initial,UIntPtr maximum);
 [DllImport("kernel32.dll",SetLastError=true)] static extern IntPtr HeapAlloc(IntPtr h,uint f,UIntPtr n);
 [DllImport("kernel32.dll",SetLastError=true)] static extern bool HeapValidate(IntPtr h,uint f,IntPtr p);
 [DllImport("kernel32.dll",SetLastError=true)] static extern bool HeapFree(IntPtr h,uint f,IntPtr p);
 [DllImport("kernel32.dll",SetLastError=true)] static extern bool HeapDestroy(IntPtr h);
 [DllImport("kernel32.dll")] static extern void InitializeCriticalSection(IntPtr p);
 [DllImport("kernel32.dll")] static extern void EnterCriticalSection(IntPtr p);
 [DllImport("kernel32.dll")] static extern void LeaveCriticalSection(IntPtr p);
 [DllImport("kernel32.dll")] static extern void DeleteCriticalSection(IntPtr p);
 [DllImport("kernel32.dll")] static extern bool IsBadReadPtr(IntPtr p,UIntPtr n);
 [DllImport("kernel32.dll")] static extern bool IsBadWritePtr(IntPtr p,UIntPtr n);
 [DllImport("kernel32.dll",CharSet=CharSet.Ansi,SetLastError=true)] static extern IntPtr CreateFileA(string p,uint a,uint s,IntPtr sec,uint d,uint f,IntPtr t);
 [DllImport("kernel32.dll",SetLastError=true)] static extern uint GetFileSize(IntPtr h,IntPtr high);
 [DllImport("kernel32.dll",SetLastError=true)] static extern bool ReadFile(IntPtr h,IntPtr b,uint n,out uint read,IntPtr over);
 [DllImport("kernel32.dll",SetLastError=true)] static extern bool CloseHandle(IntPtr h);
 [DllImport("kernel32.dll",CharSet=CharSet.Ansi)] static extern uint GetCurrentDirectoryA(uint n,System.Text.StringBuilder b);
 static IntPtr heap,critical; static int depth; static bool initialized; static uint expectedFileBytes;
 static Dictionary<uint,int> blocks=new Dictionary<uint,int>(); static HashSet<uint> files=new HashSet<uint>();
 static Dictionary<uint,IntPtr> criticalInputs=new Dictionary<uint,IntPtr>();
 [DllImport("kernel32.dll",SetLastError=true)] static extern bool GetVersionExA(IntPtr p);
 static JavaScriptSerializer json=new JavaScriptSerializer {MaxJsonLength=4000000};
 static uint U(IntPtr p){return unchecked((uint)p.ToInt32());} static IntPtr P(uint p){return new IntPtr(unchecked((int)p));}
 static uint N(Dictionary<string,object> q,string k){return Convert.ToUInt32(q[k]);}
 static void Need(bool b,string m){if(!b)throw new InvalidOperationException(m);}
 static byte[] Bytes(IntPtr p,int n){byte[] b=new byte[n];Marshal.Copy(p,b,0,n);return b;}
 static string Hex(byte[] b){return BitConverter.ToString(b).Replace("-","").ToLowerInvariant();}
 static byte[] Unhex(string s){Need(s.Length%2==0 && s.Length<=2097152,"bounded hex");byte[] b=new byte[s.Length/2];for(int i=0;i<b.Length;i++)b[i]=Convert.ToByte(s.Substring(i*2,2),16);return b;}
 static uint Owned(Dictionary<string,object> q){uint p=N(q,"pointer");Need(blocks.ContainsKey(p),"owned allocation required");return p;}
 static IntPtr Range(Dictionary<string,object> q,out uint p,out int n){p=Owned(q);uint o=N(q,"offset"),z=N(q,"bytes");Need(z<=1048576 && (ulong)o+z<=(ulong)blocks[p],"owned range required");n=(int)z;return IntPtr.Add(P(p),(int)o);}
 static object Run(Dictionary<string,object> q){string op=(string)q["op"];
  if(op=="heap_create"){Need(heap==IntPtr.Zero && N(q,"flags")==0 && N(q,"initial")==4096 && N(q,"maximum")==0,"original heap init only");heap=HeapCreate(0,(UIntPtr)4096,UIntPtr.Zero);Need(heap!=IntPtr.Zero,"HeapCreate failed");return new {pointer=U(heap)};}
  if(op=="version"){byte[] b=Unhex((string)q["hex"]);Need(b.Length==148 && BitConverter.ToUInt32(b,0)==148,"source OSVERSIONINFOA");IntPtr p=Marshal.AllocHGlobal(148);try{Marshal.Copy(b,0,p,148);bool v=GetVersionExA(p);Need(v,"GetVersionExA failed");return new {value=1,hex=Hex(Bytes(p,148))};}finally{Marshal.FreeHGlobal(p);}}
  if(op=="initialize"){uint guest=N(q,"guest");Need((guest==0x80a480 || guest==0x80a498 || guest==0x80a4b0 || guest==0x80a4c8) && !criticalInputs.ContainsKey(guest),"source static lock only");IntPtr p=Marshal.AllocHGlobal(24);InitializeCriticalSection(p);criticalInputs.Add(guest,p);if(guest==0x80a4b0){critical=p;initialized=true;}return new {pointer=U(p),hex=Hex(Bytes(p,24))};}
  if(op=="delete"){uint guest=N(q,"guest");Need(criticalInputs.ContainsKey(guest) && N(q,"pointer")==U(criticalInputs[guest]) && depth==0,"owned source lock teardown");IntPtr p=criticalInputs[guest];DeleteCriticalSection(p);Marshal.FreeHGlobal(p);criticalInputs.Remove(guest);if(p==critical){critical=IntPtr.Zero;initialized=false;}return new {value=1};}
  if(op=="heap_destroy"){Need(N(q,"heap")==U(heap) && heap!=IntPtr.Zero && blocks.Count==0 && depth==0,"owned empty source heap");Need(HeapDestroy(heap),"HeapDestroy failed");heap=IntPtr.Zero;return new {value=1};}
  if(op=="enter" || op=="leave") {Need(N(q,"critical")==U(critical),"owned critical section");if(op=="enter"){Need(depth<4,"bounded recursion");EnterCriticalSection(critical);depth++;}else{Need(depth>0,"balanced leave");LeaveCriticalSection(critical);depth--;}return new {depth=depth,critical_hex=Hex(Bytes(critical,24))};}
  if(op=="alloc"){Need(N(q,"heap")==U(heap) && N(q,"flags")==0 && depth>0,"owned locked heap");uint n=N(q,"bytes");Need(n>0 && n<=1048576 && blocks.Count<6,"bounded allocation");IntPtr p=HeapAlloc(heap,0,(UIntPtr)n);Need(p!=IntPtr.Zero,"HeapAlloc failed");blocks.Add(U(p),(int)n);return new {pointer=U(p),bytes=n,hex=Hex(Bytes(p,(int)n))};}
  if(op=="sync"){uint p=Owned(q);byte[] b=Unhex((string)q["hex"]);Need(b.Length==blocks[p],"complete source buffer required");Marshal.Copy(b,0,P(p),b.Length);return new {pointer=p,hex=Hex(Bytes(P(p),b.Length))};}
  if(op=="readback"){uint p=Owned(q);return new {pointer=p,hex=Hex(Bytes(P(p),blocks[p]))};}
  if(op=="badread" || op=="badwrite"){uint p;int n;IntPtr a=Range(q,out p,out n);bool v=op=="badread"?IsBadReadPtr(a,(UIntPtr)(uint)n):IsBadWritePtr(a,(UIntPtr)(uint)n);return new {value=v?1:0,pointer=p,offset=N(q,"offset"),bytes=n};}
  if(op=="validate" || op=="free"){uint p=Owned(q);Need(N(q,"heap")==U(heap) && N(q,"flags")==0 && depth>0,"owned locked heap operation");string b=Hex(Bytes(P(p),blocks[p]));bool v=op=="validate"?HeapValidate(heap,0,P(p)):HeapFree(heap,0,P(p));Need(v,"native heap operation failed");if(op=="free")blocks.Remove(p);return new {value=1,pointer=p,before_hex=b};}
  if(op=="directory"){Need(N(q,"bytes")==260,"source MAX_PATH");var b=new System.Text.StringBuilder(260);uint v=GetCurrentDirectoryA(260,b);Need(v>0 && v<260,"bounded directory");return new {value=v,hex=Hex(System.Text.Encoding.Default.GetBytes(b.ToString()+"\0"))};}
  if(op=="open"){string path=(string)q["path"]; Need((path=="data\\adv\\bin\\Gybc_00.bin" || path=="data\\adv\\bin\\sc001.bin" || path=="data\\adv\\bin\\sc002.bin") && files.Count==0,"only exact original overlay or terminal portraits"); expectedFileBytes=path.EndsWith("Gybc_00.bin")?524312u:262168u;Need(N(q,"access")==0x80000000 && N(q,"share")==1 && N(q,"security")==0 && N(q,"disposition")==3 && N(q,"attributes")==1 && N(q,"template")==0,"source read-only file ABI");IntPtr h=CreateFileA((string)q["path"],0x80000000,1,IntPtr.Zero,3,1,IntPtr.Zero);Need(h!=new IntPtr(-1),"CreateFileA failed");files.Add(U(h));return new {handle=U(h)};}
  if(op=="size" || op=="file_close" || op=="read"){uint h=N(q,"handle");Need(files.Contains(h),"owned file required");if(op=="size"){Need(N(q,"high")==0,"source null high");uint n=GetFileSize(P(h),IntPtr.Zero);Need(n==expectedFileBytes,"exact source file extent");return new {value=n};}if(op=="file_close"){Need(CloseHandle(P(h)),"CloseHandle failed");files.Remove(h);return new {value=1};}uint p;int count;IntPtr a=Range(q,out p,out count);Need(N(q,"overlapped")==0,"synchronous read");string before=Hex(Bytes(P(p),blocks[p]));uint read;bool ok=ReadFile(P(h),a,(uint)count,out read,IntPtr.Zero);Need(ok && read==count,"complete ReadFile required");return new {value=1,read=read,pointer=p,before_hex=before,after_hex=Hex(Bytes(P(p),blocks[p]))};}
  if(op=="close"){Need(depth==0 && blocks.Count==0 && files.Count==0,"source must release all allocations and files");Need(heap==IntPtr.Zero && criticalInputs.Count==0,"original source must destroy heap and all locks");return new {all_owned_resources_released=true,heap_destroyed=true,critical_deleted=true,open_files=0,allocations=0,depth=0,forced_cleanup=false};}
  throw new InvalidOperationException("unknown operation");
 }
 static void Send(object o){Console.WriteLine(json.Serialize(o));Console.Out.Flush();}
 static int Main(){try{Need(IntPtr.Size==4,"x86 only");Send(new {id=0,ok=true,hello=new {pointer_bytes=4,heap=U(heap),critical=U(critical),critical_hex="",directory=Directory.GetCurrentDirectory(),window_created=false,GPU_created=false}});string line;while((line=Console.ReadLine())!=null){Need(line.Length<=3000000,"bounded request");var q=json.Deserialize<Dictionary<string,object>>(line);object r;try{r=Run(q);}catch(Exception e){Send(new {id=q["id"],ok=false,error=e.Message});continue;}Send(new {id=q["id"],ok=true,result=r});if((string)q["op"]=="close")return 0;}return 2;}catch(Exception e){Console.Error.WriteLine(e);return 3;}finally{foreach(uint h in files)CloseHandle(P(h));foreach(uint p in blocks.Keys)HeapFree(heap,0,P(p));while(depth>0){LeaveCriticalSection(critical);depth--;}foreach(IntPtr p in criticalInputs.Values){DeleteCriticalSection(p);Marshal.FreeHGlobal(p);}if(heap!=IntPtr.Zero)HeapDestroy(heap);}}
}
