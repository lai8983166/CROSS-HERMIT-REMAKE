// Owned WOW64 fixture. No game process, registry changes or injected code.
using System;
using System.Runtime.InteropServices;
using System.Threading;
class HeapFixture {
    [DllImport("kernel32.dll")] static extern uint GetCurrentProcessId();
    [DllImport("kernel32.dll")] static extern uint GetCurrentThreadId();
    [DllImport("kernel32.dll")] static extern IntPtr GetCurrentProcess();
    [DllImport("kernel32.dll", SetLastError=true)] static extern bool IsWow64Process(IntPtr p, out bool value);
    [DllImport("kernel32.dll")] static extern void GetSystemTimePreciseAsFileTime(out long value);
    [DllImport("kernel32.dll", SetLastError=true)] static extern IntPtr HeapCreate(uint f, UIntPtr initial, UIntPtr maximum);
    [DllImport("kernel32.dll", SetLastError=true)] static extern IntPtr HeapAlloc(IntPtr h, uint f, UIntPtr n);
    [DllImport("kernel32.dll", SetLastError=true)] static extern bool HeapFree(IntPtr h, uint f, IntPtr p);
    [DllImport("kernel32.dll", SetLastError=true)] static extern bool HeapDestroy(IntPtr h);
    static long Now() { long n; GetSystemTimePreciseAsFileTime(out n); return n; }
    static uint Ptr(IntPtr p) { return unchecked((uint)p.ToInt32()); }
    static void Emit(string s) { Console.WriteLine(s); Console.Out.Flush(); }
    static void Need(bool v) { if (!v) throw new InvalidOperationException("fixture contract"); }
    static int Main() {
        IntPtr heap=IntPtr.Zero, freed=IntPtr.Zero, live=IntPtr.Zero;
        // Last resort for a vanished controller; normal cleanup is explicit below.
        using (Timer watchdog=new Timer(delegate(object ignored) { Environment.Exit(9); }, null, 25000, Timeout.Infinite)) {
            try {
                bool wow; Need(IntPtr.Size==4 && IsWow64Process(GetCurrentProcess(),out wow) && wow);
                uint pid=GetCurrentProcessId(),tid=GetCurrentThreadId();
                Emit("{\"stage\":\"ready\",\"pid\":"+pid+",\"tid\":"+tid+",\"pointer_size\":4,\"wow64\":true,\"filetime\":"+Now()+"}");
                Need(Console.ReadLine()=="allocate");
                long begin=Now(); heap=HeapCreate(0,new UIntPtr(4096),UIntPtr.Zero); Need(heap!=IntPtr.Zero);
                freed=HeapAlloc(heap,0,new UIntPtr(152)); Need(freed!=IntPtr.Zero);
                live=HeapAlloc(heap,0,new UIntPtr(296)); Need(live!=IntPtr.Zero && live!=freed);
                uint address=Ptr(freed); bool result=HeapFree(heap,0,freed); Need(result); freed=IntPtr.Zero;
                Emit("{\"stage\":\"live\",\"pid\":"+pid+",\"tid\":"+tid+",\"heap\":"+Ptr(heap)+",\"freed_address\":"+address+",\"live_address\":"+Ptr(live)+",\"freed_size\":152,\"live_size\":296,\"free_result\":true,\"live_not_freed\":true,\"begin_filetime\":"+begin+",\"end_filetime\":"+Now()+"}");
                Need(Console.ReadLine()=="cleanup");
                long cleanupBegin=Now(); bool freeLive=HeapFree(heap,0,live); Need(freeLive); live=IntPtr.Zero;
                bool destroyed=HeapDestroy(heap); Need(destroyed); heap=IntPtr.Zero;
                Emit("{\"stage\":\"closed\",\"live_free_result\":true,\"heap_destroy_result\":true,\"begin_filetime\":"+cleanupBegin+",\"end_filetime\":"+Now()+"}");
                return 0;
            } catch(Exception e) { Console.Error.WriteLine(e.GetType().Name+": "+e.Message); return 3; }
            finally {
                if (heap!=IntPtr.Zero) { if(freed!=IntPtr.Zero)HeapFree(heap,0,freed); if(live!=IntPtr.Zero)HeapFree(heap,0,live); HeapDestroy(heap); }
            }
        }
    }
}
