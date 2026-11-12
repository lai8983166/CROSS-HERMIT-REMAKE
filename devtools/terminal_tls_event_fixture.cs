// Owned WOW64 positive/negative controls. Not original CRT or game code.
// No sleep, polling, ready/ack wait, UI, breakpoint or register instrumentation.
using System;
using System.Runtime.InteropServices;
using System.Threading;
class TlsEventFixture {
    [DllImport("kernel32.dll")] static extern uint GetCurrentProcessId();
    [DllImport("kernel32.dll")] static extern uint GetCurrentThreadId();
    [DllImport("kernel32.dll")] static extern uint TlsAlloc();
    [DllImport("kernel32.dll")] static extern bool TlsFree(uint index);
    [DllImport("kernel32.dll")] static extern bool TlsSetValue(uint index, IntPtr value);
    [DllImport("kernel32.dll")] static extern IntPtr TlsGetValue(uint index);
    [DllImport("kernel32.dll")] static extern IntPtr GetProcessHeap();
    [DllImport("kernel32.dll")] static extern IntPtr HeapAlloc(IntPtr heap, uint flags, UIntPtr size);
    [DllImport("kernel32.dll")] static extern bool HeapFree(IntPtr heap, uint flags, IntPtr value);
    [DllImport("kernel32.dll")] static extern bool QueryPerformanceCounter(out long value);
    [DllImport("kernel32.dll")] static extern bool QueryPerformanceFrequency(out long value);
    [DllImport("kernel32.dll", CharSet=CharSet.Ansi)] static extern void OutputDebugStringA(string text);
    static uint index, pid, tid, address;
    static long frequency, begun, ready, cleared, ended;
    static bool notify, freed, zero, failed;
    static long Now() { long n; if(!QueryPerformanceCounter(out n))throw new Exception(); return n; }
    static void Need(bool b) { if(!b)throw new Exception("fixture contract"); }
    static void Emit(string stage, uint id, uint ptr) {
        OutputDebugStringA("TLS1 "+stage+" "+pid+" "+id+" "+index+" "+ptr+" "+Now()+" "+frequency);
    }
    static void Worker() {
        IntPtr value=IntPtr.Zero;
        try {
            tid=GetCurrentThreadId(); begun=Now();
            value=HeapAlloc(GetProcessHeap(),0,new UIntPtr(116)); Need(value!=IntPtr.Zero);
            address=unchecked((uint)value.ToInt32());
            for(int i=0;i<116;i++)Marshal.WriteByte(value,i,(byte)((i*13+7)&255));
            Marshal.WriteInt32(value,0,0x544C5350); Marshal.WriteInt32(value,4,unchecked((int)pid));
            Marshal.WriteInt32(value,8,unchecked((int)tid)); Marshal.WriteInt32(value,12,unchecked((int)index));
            Marshal.WriteInt32(value,16,0x1234ABCD); Marshal.WriteInt32(value,20,unchecked((int)address));
            Need(TlsSetValue(index,value) && TlsGetValue(index)==value); ready=Now();
            if(notify)Emit("live",tid,address); // Cooperative positive control, not a game hook.
            Need(TlsSetValue(index,IntPtr.Zero));zero=TlsGetValue(index)==IntPtr.Zero;Need(zero);cleared=Now();
            if(notify)Emit("clear",tid,address);
            freed=HeapFree(GetProcessHeap(),0,value);Need(freed);value=IntPtr.Zero;ended=Now();
        } catch { failed=true; }
        finally {
            TlsSetValue(index,IntPtr.Zero);
            if(value!=IntPtr.Zero)HeapFree(GetProcessHeap(),0,value);
        }
    }
    static int Main(string[] args) {
        try {
            Need(IntPtr.Size==4 && args.Length==1 && (args[0]=="notified" || args[0]=="silent"));
            notify=args[0]=="notified";pid=GetCurrentProcessId();Need(QueryPerformanceFrequency(out frequency));
            index=TlsAlloc();Need(index<1088);Need(TlsSetValue(index,IntPtr.Zero));
            Emit("config",GetCurrentThreadId(),0);
            Thread worker=new Thread(Worker);worker.Start();Need(worker.Join(5000));
            Need(!failed && freed && zero && begun<=ready && ready<=cleared && cleared<=ended);
            OutputDebugStringA("TLS1 done "+pid+" "+tid+" "+index+" "+address+" "+Now()+" "+frequency+
                " "+begun+" "+ready+" "+cleared+" "+ended);
            Need(TlsFree(index));return 0;
        } catch { return 3; }
    }
}
