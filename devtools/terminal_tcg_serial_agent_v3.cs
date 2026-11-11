// Guest-only serial control, .NET Framework 4, x64, winexe.
using System;
using System.IO;
using System.IO.Ports;
using System.Text;
using System.Collections.Generic;
using System.Diagnostics;
using System.Runtime.InteropServices;
using System.Security.Cryptography;
using System.Threading;
using System.Web.Script.Serialization;
using Microsoft.Win32;
internal static class SerialAgentV3  {
    const string Root=@"C:\ChaomofaWorker\SerialV3", Uuid="626d1a20-6383-4cd3-85d5-6c9831d6f941", ProbeHash="a5aaf66a409ba15632bf7f6211552fa1f26335838957da5c7535ba74291caddc", SourceHash="490dd9ea43e5c0f73434bdba21d5ad1e8cee3587c829f6a27cdf7d332730839f";
    static readonly JavaScriptSerializer Json=new JavaScriptSerializer  {
        MaxJsonLength=262144
    }
    ;
    static readonly object JobLock=new object();
    static IntPtr CurrentJob;
    static string Key,Session=Guid.NewGuid().ToString("D"),Report;
    static long Next=1;
    static uint Nonce;
    static bool Hello,Begun,Sealed,Ran;
    static Dictionary<string,object> Identity;
    const string WinlogonPath=@"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon";
    const string OriginalUserinit=@"C:\Windows\system32\userinit.exe,";
    const string SeededUserinit=@"C:\Windows\system32\userinit.exe,C:\ChaomofaWorker\SerialV3\agent.exe,";
    static bool DiagnosticAllowed;
    static string Stage="entry";
    static readonly List<object> Stages=new List<object>();
    // Only fixed identity/path admission permits this single bounded local journal.
    // Never log request bodies, configuration bytes, exception messages or keys.
    static void RecordStage(string stage, object detail) {
        Stage=stage;
        if(!DiagnosticAllowed)return;
        // Preserve entry admission as well as the most recent parser/port stages.
        if(Stages.Count==32)Stages.RemoveAt(1);
        Stages.Add(D("stage",stage,"utc",DateTime.UtcNow.ToString("o"),"detail",detail));
        byte[] bytes=new UTF8Encoding(false).GetBytes(Json.Serialize(D("schema",2,"pid",Process.GetCurrentProcess().Id,"events",Stages)));
        Require(bytes.Length<=65536,"diagnostic budget");
        using(var f=new FileStream(Path.Combine(Root,"agent-stage.json"),FileMode.Create,FileAccess.Write,FileShare.Read)) {
            f.Write(bytes,0,bytes.Length);
            f.Flush(true);
        }
    }
    static void AdmitDiagnostic() {
        string exe=Process.GetCurrentProcess().MainModule.FileName;
        Require(Environment.MachineName.Equals("CHAOMOFA-WORKER",StringComparison.OrdinalIgnoreCase)
            &&exe.Equals(Path.Combine(Root,"agent.exe"),StringComparison.OrdinalIgnoreCase),"diagnostic admission");
        DiagnosticAllowed=true;
        RecordStage("diagnostic_admitted",D("computer_name",Environment.MachineName,"exe_sha256",FileHash(exe)));
    }
    static Dictionary<string,object> D(params object[] a) {
        var d=new Dictionary<string,object>();
        for(int i=0;i<a.Length;i+=2)d.Add((string)a[i],a[i+1]);
        return d;
    }
    static void Require(bool b,string m) {
        if(!b)throw new InvalidOperationException(m);
    }
    static string Hash(byte[] b) {
        using(var s=SHA256.Create())return BitConverter.ToString(s.ComputeHash(b)).Replace("-","").ToLowerInvariant();
    }
    static string FileHash(string p) {
        using(var f=File.OpenRead(p))using(var s=SHA256.Create())return BitConverter.ToString(s.ComputeHash(f)).Replace("-","").ToLowerInvariant();
    }
    static bool Eq(string a,string b) {
        if(a==null||b==null||a.Length!=b.Length)return false;
        int c=0;
        for(int i=0;i<a.Length;i++)c|=a[i]^b[i];
        return c==0;
    }
    static string Str(Dictionary<string,object>d,string k) {
        Require(d.ContainsKey(k)&&d[k] is string,"invalid "+k);
        return (string)d[k];
    }
    static long Num(Dictionary<string,object>d,string k) {
        Require(d.ContainsKey(k)&&(d[k] is int||d[k] is long),"invalid "+k);
        return Convert.ToInt64(d[k]);
    }
    static byte[] Firmware() {
        uint n=GetSystemFirmwareTable(0x52534d42,0,IntPtr.Zero,0);
        RecordStage("firmware_size",D("bytes",n,"win32",Marshal.GetLastWin32Error()));
        Require(n>=8&&n<=1048576,"SMBIOS size");
        IntPtr p=Marshal.AllocHGlobal((int)n);
        try {
            Require(GetSystemFirmwareTable(0x52534d42,0,p,n)==n,"SMBIOS read");
            byte[] b=new byte[n];
            Marshal.Copy(p,b,0,(int)n);
            return b;
        }
        finally {
            Marshal.FreeHGlobal(p);
        }
    }
    static string SmbString(byte[]b,int start,int end,int index) {
        if(index==0)return "";
        for(int at=start,i=1;at<end;i++) {
            int stop=at;
            while(stop<end&&b[stop]!=0)stop++;
            if(i==index)return Encoding.ASCII.GetString(b,at,stop-at);
            at=stop+1;
        }
        return "";
    }
    static void Guard() {
        string exe=Process.GetCurrentProcess().MainModule.FileName;
        bool machine=Environment.MachineName.Equals("CHAOMOFA-WORKER",StringComparison.OrdinalIgnoreCase),path=exe.Equals(Root+@"\agent.exe",StringComparison.OrdinalIgnoreCase);
        string manufacturer="",uuid="";
        byte[] type1=null,raw=Firmware();
        int length=BitConverter.ToInt32(raw,4);
        Require(length>=0&&length<=raw.Length-8,"SMBIOS length");
        int limit=8+length;
        RecordStage("firmware_read",D("bytes",raw.Length,"table_length",length,"major",raw[1],"minor",raw[2],"sha256",Hash(raw)));
        bool sawEnd=false;
        for(int at=8;at+4<=limit;) {
            int len=raw[at+1];
            Stage="smbios_structure";
            RecordStage(Stage,D("offset",at,"type",raw[at],"formatted_length",len));
            Require(len>=4&&at+len<=limit,"SMBIOS structure");
            int end=at+len;
            while(end+1<limit&&(raw[end]!=0||raw[end+1]!=0))end++;
            Require(end+1<limit,"SMBIOS strings");
            if(raw[at]==1) {
                Require(type1==null&&len>=25,"SMBIOS type1");
                type1=new byte[end+2-at];
                Buffer.BlockCopy(raw,at,type1,0,type1.Length);
                manufacturer=SmbString(raw,at+len,end+1,raw[at+4]);
                byte[] ub=new byte[16];
                Buffer.BlockCopy(raw,at+8,ub,0,16);
                if(raw[1]<2||(raw[1]==2&&raw[2]<6)) {
                    Array.Reverse(ub,0,4);
                    Array.Reverse(ub,4,2);
                    Array.Reverse(ub,6,2);
                }
                uuid=new Guid(ub).ToString("D");
            }
            // Type 127 ends the SMBIOS table. Firmware may leave padding after
            // its complete formatted section and double-NUL string terminator.
            // Never interpret that padding as another zero-length structure.
            if(raw[at]==127) {
                sawEnd=true;
                RecordStage("smbios_end",D("offset",at,"trailing_bytes",limit-(end+2)));
                break;
            }
            at=end+2;
        }
        Require(sawEnd,"SMBIOS end marker missing");
        bool vendor=manufacturer.Equals("QEMU",StringComparison.OrdinalIgnoreCase);
        uint own;
        bool sid=ProcessIdToSessionId((uint)Process.GetCurrentProcess().Id,out own);
        uint active=WTSGetActiveConsoleSessionId();
        Identity=D("computer_name",Environment.MachineName,"manufacturer",manufacturer,"uuid",uuid,"smbios_major",raw[1],"smbios_minor",raw[2],"smbios_type1_base64",type1==null?"":Convert.ToBase64String(type1),"smbios_sha256",Hash(raw),"pid",Process.GetCurrentProcess().Id,"session_id",own,"active_console_session_id",active,"exe_sha256",FileHash(exe));
        RecordStage("guard_identity",D("manufacturer",manufacturer,"uuid",uuid,"session_query",sid,"session_id",own,"active_console_session_id",active));
        if(!(machine&&path&&vendor&&uuid==Uuid&&sid&&own>0&&active!=0xffffffff&&own==active)) {
            if(machine&&path&&vendor)File.WriteAllText(Path.Combine(Root,"agent-failure.json"),Json.Serialize(D("guard_failed",true,"identity",Identity)),new UTF8Encoding(false));
            throw new InvalidOperationException("guest guard");
        }
    }
    static bool RestoreInitializationAndClearAutologon() {
        using(var k=Registry.LocalMachine.OpenSubKey(WinlogonPath,true)) {
            Require(k!=null,"Winlogon missing");
            Require(k.GetValueKind("Userinit")==RegistryValueKind.String
                &&Eq(k.GetValue("Userinit",null,RegistryValueOptions.DoNotExpandEnvironmentNames) as string,SeededUserinit),"initialization identity");
            RecordStage("initialization_restore_begin",null);
            k.SetValue("Userinit",OriginalUserinit,RegistryValueKind.String);
            k.Flush();
            Require(k.GetValueKind("Userinit")==RegistryValueKind.String
                &&Eq(k.GetValue("Userinit",null,RegistryValueOptions.DoNotExpandEnvironmentNames) as string,OriginalUserinit),"initialization readback");
            RecordStage("initialization_restored",D("readback",true));
            k.SetValue("AutoAdminLogon","0",RegistryValueKind.String);
            k.DeleteValue("DefaultPassword",false);
            k.DeleteValue("AutoLogonCount",false);
            k.Flush();
            return (string)k.GetValue("AutoAdminLogon",null)=="0"&&k.GetValue("DefaultPassword",null)==null&&k.GetValue("AutoLogonCount",null)==null;
        }
    }
    static bool BootstrapRestored() {
        using(var k=Registry.LocalMachine.OpenSubKey(WinlogonPath,false)) {
            return k!=null&&k.GetValueKind("Userinit")==RegistryValueKind.String
                &&Eq(k.GetValue("Userinit",null,RegistryValueOptions.DoNotExpandEnvironmentNames) as string,OriginalUserinit);
        }
    }
    [STAThread] static void Main() {
        try {
            AdmitDiagnostic();
            RecordStage("guard_begin",null);
            Guard();
            RecordStage("guard_passed",null);
            Stage="config_read";
            Key=File.ReadAllText(Path.Combine(Root,"CONFIG.TXT")).Trim();
            Require(Key.Length==64,"key length");
            foreach(char c in Key)Require(Uri.IsHexDigit(c),"key format");
            RecordStage("config_valid",null);
            using(var timer=new Timer(delegate {
                lock(JobLock) {
                    if(CurrentJob!=IntPtr.Zero)TerminateJobObject(CurrentJob,1460);
                }
                Environment.Exit(1460);
            }
            ,null,900000,Timeout.Infinite))using(var port=new SerialPort("COM1",115200,Parity.None,8,StopBits.One)) {
                port.Handshake=Handshake.None;
                port.DtrEnable=false;
                port.RtsEnable=false;
                port.ReadTimeout=250;
                port.WriteTimeout=5000;
                port.Encoding=new UTF8Encoding(false,true);
                RecordStage("port_open_begin",D("port","COM1","baud",115200));
                port.Open();
                RecordStage("port_opened",D("is_open",port.IsOpen));
                var line=new List<byte>();
                bool overflow=false,done=false;
                while(!done) {
                    int v;
                    try {
                        v=port.ReadByte();
                    }
                    catch(TimeoutException) {
                        continue;
                    }
                    if(v<0)continue;
                    if(v!=10) {
                        if(line.Count<8192&&!overflow)line.Add((byte)v);
                        else {
                            overflow=true;
                            line.Clear();
                        }
                        continue;
                    }
                    long seq=0;
                    object value=null;
                    bool ok=false;
                    try {
                        Require(!overflow,"line too long");
                        var d=Json.DeserializeObject(new UTF8Encoding(false,true).GetString(line.ToArray())) as Dictionary<string,object>;
                        Require(d!=null,"object required");
                        Require(Eq(Str(d,"key"),Key),"authentication");
                        seq=Num(d,"seq");
                        Require(seq==Next,"sequence");
                        string op=Str(d,"op");
                        foreach(string field in d.Keys)Require(field=="key"||field=="seq"||field=="session"||field=="op"||field=="nonce"||(op=="block"&&(field=="offset"||field=="data"||field=="sha256")),"unknown field");
                        long nonce=Num(d,"nonce");
                        Require(nonce>=0x40000000&&nonce<=0x5fffffff,"nonce");
                        Require(Hello?Str(d,"session")==Session&&nonce==Nonce:op=="hello"&&Str(d,"session")=="","session");
                        Next++;
                        if(!Hello)Nonce=(uint)nonce;
                        value=Dispatch(op,d);
                        ok=true;
                        done=op=="bye";
                    }
                    catch(Exception ex) {
                        value=D("error",ex is InvalidOperationException?ex.Message:ex.GetType().Name);
                    }
                    line.Clear();
                    overflow=false;
                    port.Write(Json.Serialize(D("seq",seq,"ok",ok,"session",Session,"value",value))+"\n");
                }
                port.Close();
                RecordStage("port_closed",D("is_open",port.IsOpen));
            }
        }
        catch(Exception ex) {
            // Failure persistence is allowed only after the narrow local
            // admission, including failures before complete firmware identity.
            try {RecordStage("fatal",D("failed_stage",Stage,"exception_type",ex.GetType().FullName,"hresult",Marshal.GetHRForException(ex)));}catch{}
            /* Fail closed; never use host fallback. */
        }
    }
    static object Dispatch(string op,Dictionary<string,object>d) {
        string probe=Path.Combine(Root,"probe.exe");
        switch(op) {
            case "hello":Require(!Hello,"hello already used");
            bool clear=RestoreInitializationAndClearAutologon();
            Require(clear,"autologon readback");
            Hello=true;
            return D("identity",Identity,"autologon_cleared",clear,"initialization_restored",true,"protocol",1);
            case "echo":return Child(Path.Combine(Environment.SystemDirectory,"cmd.exe"),"/d /c echo CMF-"+Nonce.ToString("x8"),30000);
            case "boot":return Child(Path.Combine(Environment.SystemDirectory,@"wbem\wmic.exe"),"os get LastBootUpTime /value",30000);
            case "begin":Require(!Begun&&!Sealed&&!Ran,"begin state");
            using(var f=new FileStream(probe,FileMode.CreateNew,FileAccess.Write,FileShare.None)) {
                f.Flush(true);
            }
            Begun=true;
            return D("offset_after",0);
            case "block":Require(Begun&&!Sealed&&!Ran,"block state");
            long offset=Num(d,"offset");
            byte[] data=Convert.FromBase64String(Str(d,"data"));
            Require(data.Length>0&&data.Length<=2048,"block size");
            Require(Hash(data)==Str(d,"sha256"),"block sha256");
            using(var f=new FileStream(probe,FileMode.Open,FileAccess.Write,FileShare.None)) {
                Require(f.Length==offset&&offset>=0&&offset+data.Length<=32768,"offset");
                f.Position=offset;
                f.Write(data,0,data.Length);
                f.Flush(true);
            }
            return D("offset_after",offset+data.Length,"prefix_sha256",FileHash(probe));
            case "seal":Require(Begun&&!Sealed&&!Ran,"seal state");
            Require(new FileInfo(probe).Length==32768&&FileHash(probe)==ProbeHash,"probe identity");
            Sealed=true;
            return D("length",32768,"sha256",ProbeHash);
            case "run":Require(Sealed&&!Ran,"run state");
            Require(new FileInfo(probe).Length==32768&&FileHash(probe)==ProbeHash,"probe identity");
            Report=Path.Combine(Root,"probe-"+Nonce.ToString("x8")+".json");
            Require(!File.Exists(Report),"report exists");
            Ran=true;
            return Child(probe,"\""+Report+"\" "+Nonce.ToString("x8")+" "+SourceHash,120000);
            case "read":Require(Ran&&Report!=null,"read state");
            Require(new FileInfo(Report).Length<=65536,"report size");
            byte[] report=File.ReadAllBytes(Report);
            Require(report.Length<=65536,"report grew");
            return D("data",Convert.ToBase64String(report),"sha256",Hash(report),"length",report.Length);
            case "bye":bool restored=BootstrapRestored();
            Require(restored,"initialization restore changed");
            return D("bootstrap_restored",restored,"channel_closing",true,"own_exit_observed",false);
            default:throw new InvalidOperationException("unknown op");
        }
    }
    [StructLayout(LayoutKind.Sequential)]struct SA {
        public int length;
        public IntPtr descriptor;
        [MarshalAs(UnmanagedType.Bool)]public bool inherit;
    }
    [StructLayout(LayoutKind.Sequential,CharSet=CharSet.Unicode)]struct SI {
        public int cb;
        public string reserved,desktop,title;
        public uint x,y,xsize,ysize,xchars,ychars,fill,flags;
        public short show,cbReserved;
        public IntPtr reserved2,stdin,stdout,stderr;
    }
    [StructLayout(LayoutKind.Sequential)]struct PI {
        public IntPtr process,thread;
        public uint pid,tid;
    }
    [StructLayout(LayoutKind.Sequential)]struct BasicLimit {
        public long processTime,jobTime;
        public uint flags;
        public UIntPtr min,max;
        public uint active;
        public UIntPtr affinity;
        public uint priority,scheduling;
    }
    [StructLayout(LayoutKind.Sequential)]struct IO {
        public ulong r,w,o,rb,wb,ob;
    }
    [StructLayout(LayoutKind.Sequential)]struct ExtendedLimit {
        public BasicLimit basic;
        public IO io;
        public UIntPtr processMemory,jobMemory,peakProcess,peakJob;
    }
    [StructLayout(LayoutKind.Sequential)]struct Accounting {
        public long user,kernel,periodUser,periodKernel;
        public uint faults,total,active,terminated;
    }
    static uint Active(IntPtr job) {
        Accounting a;
        Check(QueryInformationJobObject(job,1,out a,(uint)Marshal.SizeOf(typeof(Accounting)),IntPtr.Zero),"job accounting");
        return a.active;
    }
    static void Check(bool b,string label) {
        if(!b)throw new InvalidOperationException(label+" win32="+Marshal.GetLastWin32Error());
    }
    static void Close(ref IntPtr h,string label,Dictionary<string,object> results) {
        if(h!=IntPtr.Zero&&h!=new IntPtr(-1)) {
            bool ok=CloseHandle(h);
            results[label]=ok;
            h=IntPtr.Zero;
        }
    }
    static object Child(string exe,string args,int timeout) {
        IntPtr job=IntPtr.Zero,read=IntPtr.Zero,write=IntPtr.Zero,nul=IntPtr.Zero;
        PI pi=new PI();
        var closes=new Dictionary<string,object>();
        var output=new MemoryStream();
        bool assigned=false,timed=false,terminated=false,limitHit=false;
        uint exit=259,active=0xffffffff;
        string error=null;
        var watch=Stopwatch.StartNew();
        try {
            job=CreateJobObject(IntPtr.Zero,null);
            Check(job!=IntPtr.Zero,"create job");
            ExtendedLimit limits=new ExtendedLimit();
            limits.basic.flags=0x2000;
            Check(SetInformationJobObject(job,9,ref limits,(uint)Marshal.SizeOf(typeof(ExtendedLimit))),"job limits");
            lock(JobLock) {
                CurrentJob=job;
            }
            SA sa=new SA();
            sa.length=Marshal.SizeOf(typeof(SA));
            sa.inherit=true;
            Check(CreatePipe(out read,out write,ref sa,0),"pipe");
            Check(SetHandleInformation(read,1,0),"pipe inheritance");
            nul=CreateFile("NUL",0x80000000,3,ref sa,3,0,IntPtr.Zero);
            Check(nul!=new IntPtr(-1),"stdin NUL");
            SI si=new SI();
            si.cb=Marshal.SizeOf(typeof(SI));
            si.flags=0x101;
            si.show=0;
            si.stdin=nul;
            si.stdout=write;
            si.stderr=write;
            Check(CreateProcess(exe,new StringBuilder("\""+exe+"\" "+args),IntPtr.Zero,IntPtr.Zero,true,0x08000004,IntPtr.Zero,Root,ref si,out pi),"create suspended");
            Check(AssignProcessToJobObject(job,pi.process),"assign job");
            assigned=true;
            Check(ResumeThread(pi.thread)!=0xffffffff,"resume");
            Close(ref pi.thread,"thread",closes);
            Close(ref write,"pipe_write",closes);
            Close(ref nul,"stdin",closes);
            while(true) {
                Drain(read,output,ref limitHit);
                active=Active(job);
                if(active==0)break;
                if(watch.ElapsedMilliseconds>=timeout||limitHit) {
                    timed=watch.ElapsedMilliseconds>=timeout;
                    terminated=TerminateJobObject(job,1460);
                    Check(terminated,"terminate job");
                    break;
                }
                Thread.Sleep(10);
            }
        }
        catch(Exception ex) {
            error=ex.Message;
        }
        finally {
            if(pi.process!=IntPtr.Zero&&!assigned) {
                bool killed=TerminateProcess(pi.process,1460);
                closes["unassigned_process_terminated"]=killed;
                if(killed)closes["unassigned_process_exit_observed"]=WaitForSingleObject(pi.process,5000)==0;
            }
            if(job!=IntPtr.Zero) {
                try {
                    active=Active(job);
                    if(active!=0) {
                        bool killed=TerminateJobObject(job,1460);
                        terminated|=killed;
                        if(!killed)error="job termination failed";
                    }
                    var cleanup=Stopwatch.StartNew();
                    while(Active(job)!=0&&cleanup.ElapsedMilliseconds<5000) {
                        if(read!=IntPtr.Zero)Drain(read,output,ref limitHit);
                        Thread.Sleep(10);
                    }
                    active=Active(job);
                    if(active!=0)error="descendants survived cleanup";
                }
                catch(Exception ex) {
                    error="cleanup: "+ex.Message;
                    active=0xffffffff;
                }
            }
            if(read!=IntPtr.Zero) {
                try {
                    Drain(read,output,ref limitHit);
                }
                catch(Exception ex) {
                    error="pipe cleanup: "+ex.Message;
                }
            }
            if(pi.process!=IntPtr.Zero&&!GetExitCodeProcess(pi.process,out exit))error="exit code unavailable";
            Close(ref pi.thread,"thread",closes);
            Close(ref pi.process,"process",closes);
            Close(ref write,"pipe_write",closes);
            Close(ref read,"pipe_read",closes);
            Close(ref nul,"stdin",closes);
            lock(JobLock) {
                CurrentJob=IntPtr.Zero;
                Close(ref job,"job",closes);
            }
        }
        bool handles=true;
        foreach(object result in closes.Values)if(result is bool&&!(bool)result)handles=false;
        return D("output_base64",Convert.ToBase64String(output.ToArray()),"output_length",output.Length,"exit_code",exit,"timed_out",timed,"output_limit_exceeded",limitHit,"pid",pi.pid,"job_assigned_before_resume",assigned,"job_terminated",terminated,"active_processes_after",active,"handle_close",closes,"cleanup_ok",active==0&&handles,"error",error,"elapsed_ms",watch.ElapsedMilliseconds);
    }
    static void Drain(IntPtr pipe,MemoryStream output,ref bool hit) {
        for(int i=0;i<128;i++) {
            uint available;
            if(!PeekNamedPipe(pipe,IntPtr.Zero,0,IntPtr.Zero,out available,IntPtr.Zero)) {
                if(Marshal.GetLastWin32Error()==109)return;
                throw new InvalidOperationException("peek pipe");
            }
            if(available==0)return;
            byte[] b=new byte[Math.Min(4096,(int)available)];
            uint got;
            Check(ReadFile(pipe,b,(uint)b.Length,out got,IntPtr.Zero),"read pipe");
            int keep=(int)Math.Min(got,65536-output.Length);
            if(keep>0)output.Write(b,0,keep);
            if(keep<got)hit=true;
        }
    }
    [DllImport("kernel32.dll",SetLastError=true)]static extern uint GetSystemFirmwareTable(uint provider,uint id,IntPtr buffer,uint size);
    [DllImport("kernel32.dll",SetLastError=true)]static extern bool ProcessIdToSessionId(uint pid,out uint session);
    [DllImport("kernel32.dll")]static extern uint WTSGetActiveConsoleSessionId();
    [DllImport("kernel32.dll",CharSet=CharSet.Unicode,SetLastError=true)]static extern IntPtr CreateJobObject(IntPtr sa,string name);
    [DllImport("kernel32.dll",SetLastError=true)]static extern bool SetInformationJobObject(IntPtr job,int cls,ref ExtendedLimit info,uint size);
    [DllImport("kernel32.dll",SetLastError=true)]static extern bool QueryInformationJobObject(IntPtr job,int cls,out Accounting info,uint size,IntPtr ret);
    [DllImport("kernel32.dll",SetLastError=true)]static extern bool TerminateJobObject(IntPtr job,uint exit);
    [DllImport("kernel32.dll",SetLastError=true)]static extern bool AssignProcessToJobObject(IntPtr job,IntPtr process);
    [DllImport("kernel32.dll",SetLastError=true)]static extern bool CreatePipe(out IntPtr read,out IntPtr write,ref SA sa,uint size);
    [DllImport("kernel32.dll",SetLastError=true)]static extern bool SetHandleInformation(IntPtr handle,uint mask,uint flags);
    [DllImport("kernel32.dll",CharSet=CharSet.Unicode,SetLastError=true)]static extern IntPtr CreateFile(string path,uint access,uint share,ref SA sa,uint disposition,uint flags,IntPtr template);
    [DllImport("kernel32.dll",CharSet=CharSet.Unicode,SetLastError=true)]static extern bool CreateProcess(string app,StringBuilder command,IntPtr processSa,IntPtr threadSa,bool inherit,uint flags,IntPtr environment,string cwd,ref SI startup,out PI process);
    [DllImport("kernel32.dll",SetLastError=true)]static extern uint ResumeThread(IntPtr thread);
    [DllImport("kernel32.dll",SetLastError=true)]static extern bool CloseHandle(IntPtr handle);
    [DllImport("kernel32.dll",SetLastError=true)]static extern bool GetExitCodeProcess(IntPtr process,out uint exit);
    [DllImport("kernel32.dll",SetLastError=true)]static extern bool TerminateProcess(IntPtr process,uint exit);
    [DllImport("kernel32.dll",SetLastError=true)]static extern uint WaitForSingleObject(IntPtr handle,uint milliseconds);
    [DllImport("kernel32.dll",SetLastError=true)]static extern bool PeekNamedPipe(IntPtr pipe,IntPtr buffer,uint size,IntPtr read,out uint available,IntPtr left);
    [DllImport("kernel32.dll",SetLastError=true)]static extern bool ReadFile(IntPtr handle,byte[] buffer,uint size,out uint read,IntPtr overlap);
}
