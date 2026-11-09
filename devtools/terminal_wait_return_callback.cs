// Owned process only; no debugger, game, injection, TEB writes, or input APIs.
// Build: Framework v4 csc /nologo /platform:x86 /r:System.Web.Extensions.dll /out:helper.exe this.cs
using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Runtime.InteropServices;
using System.Security.Cryptography;
using System.Threading;
using System.Web.Script.Serialization;

class OwnedWaitCallback
{
    [DllImport("kernel32.dll", SetLastError=true)] static extern IntPtr VirtualAlloc(IntPtr address, UIntPtr size, uint type, uint protection);
    [DllImport("kernel32.dll", SetLastError=true)] static extern bool VirtualProtect(IntPtr address, UIntPtr size, uint protection, out uint old);
    [DllImport("kernel32.dll", SetLastError=true)] static extern bool VirtualFree(IntPtr address, UIntPtr size, uint type);
    [DllImport("kernel32.dll")] static extern IntPtr GetCurrentProcess();
    [DllImport("kernel32.dll")] static extern uint GetCurrentThreadId();
    [DllImport("kernel32.dll", SetLastError=true)] static extern bool IsWow64Process(IntPtr process, out bool wow64);
    [DllImport("kernel32.dll", CharSet=CharSet.Unicode)] static extern IntPtr GetModuleHandle(string name);
    [DllImport("kernel32.dll", CharSet=CharSet.Ansi)] static extern IntPtr GetProcAddress(IntPtr module, string name);
    [DllImport("kernel32.dll", SetLastError=true)] static extern bool FlushInstructionCache(IntPtr process, IntPtr address, UIntPtr size);
    [DllImport("kernel32.dll", SetLastError=true)] static extern IntPtr CreateEvent(IntPtr attributes, bool manual, bool signaled, IntPtr name);
    [DllImport("kernel32.dll", SetLastError=true)] static extern bool SetEvent(IntPtr handle);
    [DllImport("kernel32.dll", SetLastError=true)] static extern uint WaitForSingleObject(IntPtr handle, uint ms);
    [DllImport("kernel32.dll", SetLastError=true)] static extern bool CloseHandle(IntPtr handle);
    [DllImport("ntdll.dll")] static extern uint NtSetInformationProcess(IntPtr process, uint type, IntPtr information, uint length);
    [UnmanagedFunctionPointer(CallingConvention.StdCall)] delegate uint WaitWrapper(IntPtr handle, IntPtr timeout);

    static uint Address(IntPtr p) { return unchecked((uint)p.ToInt32()); }
    static void Need(bool result, string message) { if (!result) throw new Exception(message+" Win32="+Marshal.GetLastWin32Error()); }
    static byte[] Read(IntPtr p, int count) { byte[] b=new byte[count]; Marshal.Copy(p,b,0,count); return b; }
    static string Hex(byte[] b) { return BitConverter.ToString(b).Replace("-", "").ToLowerInvariant(); }
    static string Hash(byte[] b) { using (SHA256 h=SHA256.Create()) return Hex(h.ComputeHash(b)); }
    static void U32(byte[] b, int offset, uint value) { Array.Copy(BitConverter.GetBytes(value),0,b,offset,4); }
    static readonly JavaScriptSerializer Json = new JavaScriptSerializer();

    public static int Main(string[] args)
    {
        if (args.Length != 2 || args[0] != "--owned-helper-only") return 2;
        string output=Path.GetFullPath(args[1]);
        if (File.Exists(output) || File.Exists(output+".watchdog.json")) return 2;
        string dir=AppDomain.CurrentDomain.BaseDirectory;
        Dictionary<string,object> report=new Dictionary<string,object>();
        report["kind"]="owned_wow64_wait_callback_preflight";
        report["accepted"]=false; report["full_original_abi"]=false;
        report["uninstrumented_ecx_observed"]=false; report["original_program_observed"]=false;
        report["callback_overwrites_ecx"]=true; report["error"]=null;
        report["pointer_size"]=IntPtr.Size;
        List<string> cleanup=new List<string>(); report["cleanup_errors"]=cleanup;
        report["buffers_released"]=false; report["handles_closed"]=false;
        report["watchdog_disarmed"]=false;
        IntPtr code=IntPtr.Zero, data=IntPtr.Zero, info=IntPtr.Zero, timeout=IntPtr.Zero;
        IntPtr request=IntPtr.Zero, response=IntPtr.Zero, wait=IntPtr.Zero;
        bool registered=false, peerDone=false; int stop=0;
        int signals=0; string peerError=null; Thread peer=null;
        ManualResetEvent watchdogDone=new ManualResetEvent(false);
        Thread watchdog=new Thread(delegate() {
            if (!watchdogDone.WaitOne(15000)) {
                try { File.WriteAllText(output+".watchdog.json", "{\"kind\":\"owned_helper_watchdog\",\"accepted\":false,\"normal_cleanup\":false,\"forced_self_exit\":true}"); } catch {}
                Environment.Exit(124);
            }
        });
        watchdog.IsBackground=true; watchdog.Start();
        try {
            Need(IntPtr.Size==4,"x86 helper required");
            bool wow; Need(IsWow64Process(GetCurrentProcess(),out wow) && wow,"WOW64 required"); report["wow64"]=wow;
            byte[] source=File.ReadAllBytes(Path.Combine(dir,"terminal_wait_return_callback.cs"));
            byte[] template=File.ReadAllBytes(Path.Combine(dir,"callback.bin"));
            Dictionary<string,object> manifest=Json.Deserialize<Dictionary<string,object>>(File.ReadAllText(Path.Combine(dir,"manifest.json")));
            Need(Hash(source)==(string)manifest["source_sha256"] && Hash(template)==(string)manifest["template_sha256"],"frozen deployment identities");
            report["source_sha256"]=Hash(source); report["template_sha256"]=Hash(template);
            report["helper_sha256"]=Hash(File.ReadAllBytes(System.Reflection.Assembly.GetExecutingAssembly().Location));
            report["manifest_sha256"]=Hash(File.ReadAllBytes(Path.Combine(dir,"manifest.json")));
            report["os_version"]=Environment.OSVersion.Version.ToString();
            wait=GetProcAddress(GetModuleHandle("ntdll.dll"),"NtWaitForSingleObject"); Need(wait!=IntPtr.Zero,"NtWait export");
            byte[] before=Read(wait,32);
            Need(before[0]==0xb8 && before[5]==0xba && before[10]==0xff && before[11]==0xd2 && before[12]==0xc2 && before[13]==12 && before[14]==0,"fixed unpatched NtWait+12 stub");
            report["nt_wait_before"]=Hex(before); report["nt_wait"]=Address(wait);
            data=VirtualAlloc(IntPtr.Zero,(UIntPtr)32768,0x3000,4); Need(data!=IntPtr.Zero,"owned RW records");
            code=VirtualAlloc(IntPtr.Zero,(UIntPtr)4096,0x3000,4); Need(code!=IntPtr.Zero,"owned code staging");
            uint tid=GetCurrentThreadId(); report["target_tid"]=tid;
            report["record_base"]=Address(data); report["code_base"]=Address(code);
            Dictionary<string,uint> values=new Dictionary<string,uint>();
            values["record_base"]=Address(data); values["target_tid"]=tid;
            values["nt_wait"]=Address(wait); values["nt_return_pc"]=Address(wait)+12;
            byte[] machine=(byte[])template.Clone();
            values["caller_return_pc"]=Address(code)+Convert.ToUInt32(manifest["wrapper_postcall_offset"]);
            foreach (object item in (IEnumerable)manifest["patches"]) {
                Dictionary<string,object> patch=(Dictionary<string,object>)item;
                U32(machine,Convert.ToInt32(patch["offset"]),values[(string)patch["symbol"]]+Convert.ToUInt32(patch["addend"]));
            }
            Marshal.Copy(machine,0,code,machine.Length);
            uint old; Need(VirtualProtect(code,(UIntPtr)4096,0x20,out old) && old==4,"RW to RX only owned code");
            Need(FlushInstructionCache(GetCurrentProcess(),code,(UIntPtr)machine.Length),"flush owned code");
            report["code_protection"]="PAGE_EXECUTE_READ"; report["record_protection"]="PAGE_READWRITE";
            report["code_before"]=Hex(Read(code,machine.Length));
            request=CreateEvent(IntPtr.Zero,false,false,IntPtr.Zero); response=CreateEvent(IntPtr.Zero,false,false,IntPtr.Zero);
            Need(request!=IntPtr.Zero && response!=IntPtr.Zero,"fresh nonsignaled auto reset events");
            report["event_handle"]=Address(response);
            timeout=Marshal.AllocHGlobal(8); info=Marshal.AllocHGlobal(12);
            report["timeout_pointer"]=Address(timeout);
            Marshal.WriteInt32(info,0,code.ToInt32()); Marshal.WriteInt32(info,4,0); Marshal.WriteInt32(info,8,code.ToInt32());
            WaitWrapper run=(WaitWrapper)Marshal.GetDelegateForFunctionPointer(IntPtr.Add(code,Convert.ToInt32(manifest["wrapper_offset"])),typeof(WaitWrapper));
            peer=new Thread(delegate() {
                try {
                    for (int i=0;i<3;i++) {
                        uint r=WaitForSingleObject(request,2000);
                        if (Interlocked.CompareExchange(ref stop,0,0)!=0) return;
                        if (r!=0) throw new Exception("peer request wait "+r);
                        Need(SetEvent(response),"peer real SetEvent"); Interlocked.Increment(ref signals);
                    }
                    peerDone=true;
                } catch (Exception e) { peerError=e.ToString(); }
            }); peer.IsBackground=true; peer.Start();
            uint status=NtSetInformationProcess(GetCurrentProcess(),40,info,12);
            report["registration_status"]=status;
            Need(status==0,"single WOW64 callback registration; no retry"); registered=true;
            List<uint> returns=new List<uint>(); report["returns"]=returns;
            for(int i=0;i<3;i++) {
                Marshal.WriteInt64(timeout,-20000000L); // real two-second native timeout
                Need(SetEvent(request),"main request SetEvent");
                uint r=run(response,timeout); returns.Add(r); Need(r==0,"actual handshake wait return");
            }
            Need(peer.Join(2500),"bounded peer completion");
            Need(peerDone && peerError==null && signals==3,"peer completed three handshakes");
            Marshal.WriteInt64(timeout,0); // event was consumed by auto reset; no fourth signal exists
            uint negative=run(response,timeout); returns.Add(negative); Need(negative==0x102,"real nonsignaled timeout counterexample");
            report["code_after"]=Hex(Read(code,machine.Length));
            GC.KeepAlive(run);
        }
        catch(Exception e) { report["error"]=e.ToString(); }
        finally {
            if(registered) {
                try {
                    Marshal.WriteInt32(info,0,0); Marshal.WriteInt32(info,4,0); Marshal.WriteInt32(info,8,0);
                    uint status=NtSetInformationProcess(GetCurrentProcess(),40,info,12);
                    report["unregistration_status"]=status;
                    if(status==0) registered=false; else cleanup.Add("callback removal status "+status);
                } catch(Exception e) {cleanup.Add("remove callback "+e.Message);}
            }
            Interlocked.Exchange(ref stop,1);
            if(request!=IntPtr.Zero) SetEvent(request);
            if(peer!=null && peer.IsAlive && !peer.Join(2500)) cleanup.Add("peer did not stop");
            report["peer_completed"]=peerDone; report["peer_signals"]=signals; report["peer_error"]=peerError;
            if(wait!=IntPtr.Zero) report["nt_wait_after"]=Hex(Read(wait,32));
            if(data!=IntPtr.Zero) report["records_hex"]=Hex(Read(data,32768));
            if(!registered && (peer==null || !peer.IsAlive)) {
                bool handles=true, buffers=true;
                if(request!=IntPtr.Zero) handles &= CloseHandle(request);
                if(response!=IntPtr.Zero) handles &= CloseHandle(response);
                if(code!=IntPtr.Zero) buffers &= VirtualFree(code,UIntPtr.Zero,0x8000);
                if(data!=IntPtr.Zero) buffers &= VirtualFree(data,UIntPtr.Zero,0x8000);
                if(info!=IntPtr.Zero) Marshal.FreeHGlobal(info);
                if(timeout!=IntPtr.Zero) Marshal.FreeHGlobal(timeout);
                report["handles_closed"]=handles; report["buffers_released"]=buffers;
                if(!handles || !buffers) cleanup.Add("owned resource release failed");
            } else { cleanup.Add("active callback or peer: allocations retained until self process exit"); }
            watchdogDone.Set(); Need(watchdog.Join(1000),"watchdog stopped"); watchdogDone.Dispose();
            report["watchdog_disarmed"]=true;
            File.WriteAllText(output,Json.Serialize(report));
        }
        return report["error"]==null && cleanup.Count==0 ? 0 : 1;
    }
}
