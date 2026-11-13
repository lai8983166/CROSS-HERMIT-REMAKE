// Owned x86 processes only. The parent debugger is never debugged or instrumented.
// The child's VEH gates a one-shot execution #DB after unchanged NtWait returns.
// No game, arbitrary PID, GUI, global input, code patch or EFLAGS/RF modification.
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <intrin.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

struct Values { DWORD input, consumed, status, count; };
struct Record {
    DWORD index, tid, teb, tls_index, tls_value;
    DWORD blocked_stack[4], pre_count, post_count, status, value;
    DWORD exception_code, exception_address, exception_first_consumer;
    DWORD guard_error, context_unchanged_except_DR, debug_port;
    CONTEXT blocked, armed, trapped, resumed, after;
};
struct Receipt {
    DWORD magic, version, bytes, context_bytes, pid, tid, gated, error;
    DWORD rounds, handler_calls, handler_removed, handles_closed, memory_freed;
    DWORD peer_signals, worker_exit, code_unchanged, nt_unchanged;
    DWORD code_base, consumer, nt_wait, code_size, tls_freed;
    BYTE code_before[64], code_after[64], nt_before[32], nt_after[32];
    Record records[4];
};
static Receipt result;
static Values values;
static HANDLE begin_event, go_event, done_event, response_event;
static volatile LONG round_number, stop_requested, captured_state, ack_state;
static DWORD worker_tid, tls_index;
static BYTE *code;
static DWORD consumer;
static bool gated;
static CONTEXT saved_debug;
typedef LONG (NTAPI *QueryProcess)(HANDLE, ULONG, PVOID, ULONG, PULONG);
typedef DWORD (__stdcall *Wrapper)(HANDLE, Values *, const LONGLONG *);

static bool DebugEqual(const CONTEXT &a, const CONTEXT &b) {
    return a.Dr0==b.Dr0 && a.Dr1==b.Dr1 && a.Dr2==b.Dr2 && a.Dr3==b.Dr3 &&
           a.Dr6==b.Dr6 && a.Dr7==b.Dr7;
}
static void RestoreDebug(CONTEXT *c) {
    c->Dr0=saved_debug.Dr0; c->Dr1=saved_debug.Dr1; c->Dr2=saved_debug.Dr2;
    c->Dr3=saved_debug.Dr3; c->Dr6=saved_debug.Dr6; c->Dr7=saved_debug.Dr7;
}
static DWORD DebugPort() {
    DWORD port=0;
    QueryProcess query=(QueryProcess)GetProcAddress(GetModuleHandleW(L"ntdll.dll"),"NtQueryInformationProcess");
    if (!query || query(GetCurrentProcess(),7,&port,sizeof(port),NULL)!=0) return 0;
    return port;
}
static LONG CALLBACK Observe(EXCEPTION_POINTERS *p) {
    if ((p->ExceptionRecord->ExceptionCode!=EXCEPTION_SINGLE_STEP &&
         p->ExceptionRecord->ExceptionCode!=0x4000001e) ||
        __readfsdword(0x24)!=worker_tid || p->ContextRecord->Eip!=consumer ||
        (DWORD)(uintptr_t)p->ExceptionRecord->ExceptionAddress!=consumer ||
        (p->ContextRecord->Dr6&0xe00f)!=1 || p->ContextRecord->Dr0!=consumer ||
        (p->ContextRecord->Dr7&0x000f0003)!=1 || captured_state) return EXCEPTION_CONTINUE_SEARCH;
    LONG n=round_number;
    if (n<0 || n>=4 || !gated) return EXCEPTION_CONTINUE_SEARCH;
    Record &r=result.records[n];
    InterlockedIncrement((volatile LONG *)&result.handler_calls);
    r.trapped=*p->ContextRecord;
    r.exception_code=p->ExceptionRecord->ExceptionCode;
    r.exception_address=(DWORD)(uintptr_t)p->ExceptionRecord->ExceptionAddress;
    r.exception_first_consumer=p->ContextRecord->Eip;
    r.pre_count=values.count;
    // No allocations, synchronization-object waits or CRT logging inside VEH.
    // A preallocated atomic ACK plus a finite spin budget holds this exact fault.
    InterlockedExchange(&captured_state,1);
    DWORD spins=0;
    for (;spins<100000000 && !InterlockedCompareExchange(&ack_state,0,0);++spins) YieldProcessor();
    if (spins==100000000) r.guard_error=1;
    // Restore only our temporary debug-register state. Leave EIP, RF, all GPRs,
    // floats, segments, flags and the real native return value exactly supplied.
    RestoreDebug(p->ContextRecord);
    r.resumed=*p->ContextRecord;
    CONTEXT expected=r.trapped; RestoreDebug(&expected);
    r.context_unchanged_except_DR=memcmp(&expected,&r.resumed,sizeof(expected))==0;
    return EXCEPTION_CONTINUE_EXECUTION;
}
static DWORD WINAPI Worker(void *) {
    worker_tid=GetCurrentThreadId(); result.tid=worker_tid;
    BYTE tls_payload[116]={0};
    if (!TlsSetValue(tls_index,tls_payload)) return 21;
    for (int i=0;i<4;i++) {
        if (WaitForSingleObject(go_event,2000)!=WAIT_OBJECT_0 || stop_requested) return 22;
        Record &r=result.records[i]; r.index=i; r.tid=worker_tid;
        r.teb=__readfsdword(0x18); r.tls_index=tls_index;
        r.tls_value=(DWORD)(uintptr_t)TlsGetValue(tls_index);
        LONGLONG timeout=-2000000LL; // The fourth wait really blocks then times out.
        if (!SetEvent(begin_event)) return 23;
        DWORD status=((Wrapper)code)(response_event,&values,i==3?&timeout:NULL);
        r.status=status; r.value=values.consumed; r.post_count=values.count;
        if (status!=(i==3?WAIT_TIMEOUT:WAIT_OBJECT_0) || values.status!=status ||
            values.count!=1 || values.consumed!=values.input) return 24;
        if (!SetEvent(done_event)) return 25;
    }
    // Keep the fourth round alive for the same actual DR readback as rounds 0-2.
    if (WaitForSingleObject(go_event,2000)!=WAIT_OBJECT_0 || stop_requested) return 27;
    if (!TlsSetValue(tls_index,NULL)) return 26;
    return 0;
}
static bool Save(const wchar_t *folder,const wchar_t *name,const void *p,DWORD size) {
    wchar_t path[MAX_PATH]; if (swprintf_s(path,L"%s\\%s",folder,name)<0) return false;
    HANDLE h=CreateFileW(path,GENERIC_WRITE,0,NULL,CREATE_NEW,FILE_ATTRIBUTE_NORMAL,NULL);
    if (h==INVALID_HANDLE_VALUE) return false;
    DWORD wrote=0; bool ok=WriteFile(h,p,size,&wrote,NULL)&&wrote==size;
    return CloseHandle(h)&&ok;
}
static int Child(const wchar_t *folder,bool observe) {
    result.magic=0x56454831; result.version=2; result.bytes=sizeof(result);
    result.context_bytes=sizeof(CONTEXT); result.pid=GetCurrentProcessId(); result.gated=observe;
    gated=observe; tls_index=TLS_OUT_OF_INDEXES;
    HANDLE thread=NULL; PVOID veh=NULL; DWORD error=0, old=0;
    bool suspended=false, armed=false;
    FARPROC nt=GetProcAddress(GetModuleHandleW(L"ntdll.dll"),"NtWaitForSingleObject");
    do {
        BOOL wow=FALSE;
        if (sizeof(void*)!=4 || sizeof(CONTEXT)!=716 || !IsWow64Process(GetCurrentProcess(),&wow) || !wow ||
            !nt || DebugPort()!=0xffffffff) {error=1;break;}
        result.nt_wait=(DWORD)(uintptr_t)nt;
        memcpy(result.nt_before,nt,32);
        if (result.nt_before[0]!=0xb8 || result.nt_before[10]!=0xff || result.nt_before[11]!=0xd2 ||
            memcmp(result.nt_before+12,"\xc2\x0c\x00",3)) {error=2;break;}
        code=(BYTE*)VirtualAlloc(NULL,4096,MEM_COMMIT|MEM_RESERVE,PAGE_READWRITE);
        if (!code) {error=3;break;}
        // push ebp; frame; preserve ebx; ebx=Values; timeout,false,event; NtWait.
        BYTE prefix[]={0x55,0x8b,0xec,0x53,0x8b,0x5d,0x0c,0xff,0x75,0x10,0x6a,0,
                       0xff,0x75,8,0xb8,0,0,0,0,0xff,0xd0};
        memcpy(prefix+16,&nt,4);
        // First instruction is the real consumer. No callback is in this path.
        BYTE tail[]={0x8b,0x13,0x89,0x53,4,0x89,0x43,8,0xff,0x43,12,0x5b,0x5d,0xc2,12,0};
        memcpy(code,prefix,sizeof(prefix)); memcpy(code+sizeof(prefix),tail,sizeof(tail));
        consumer=(DWORD)(uintptr_t)(code+sizeof(prefix)); result.consumer=consumer;
        result.code_base=(DWORD)(uintptr_t)code; result.code_size=sizeof(prefix)+sizeof(tail);
        memcpy(result.code_before,code,result.code_size);
        if (!VirtualProtect(code,4096,PAGE_EXECUTE_READ,&old) || old!=PAGE_READWRITE ||
            !FlushInstructionCache(GetCurrentProcess(),code,result.code_size)) {error=4;break;}
        begin_event=CreateEventW(NULL,FALSE,FALSE,NULL); go_event=CreateEventW(NULL,FALSE,FALSE,NULL);
        done_event=CreateEventW(NULL,FALSE,FALSE,NULL); response_event=CreateEventW(NULL,FALSE,FALSE,NULL);
        if (!begin_event||!go_event||!done_event||!response_event) {error=5;break;}
        tls_index=TlsAlloc(); if (tls_index==TLS_OUT_OF_INDEXES) {error=6;break;}
        if (gated) {veh=AddVectoredExceptionHandler(1,Observe);if (!veh) {error=7;break;}}
        thread=CreateThread(NULL,0,Worker,NULL,0,NULL);if (!thread) {error=8;break;}
        for (int i=0;i<4;i++) {
            round_number=i; values.input=0x12340000+i; values.consumed=0xcccccccc;
            values.status=0xcccccccc; values.count=0;
            InterlockedExchange(&captured_state,0); InterlockedExchange(&ack_state,0);
            if (!SetEvent(go_event)||WaitForSingleObject(begin_event,2000)!=WAIT_OBJECT_0) {error=9;break;}
            Sleep(40); // One bounded pending-wait check; no polling/retry on a miss.
            DWORD previous= SuspendThread(thread);
            if (previous==0xffffffff) {error=10;break;}
            suspended=true;
            if (previous!=0) {error=10;break;}
            Record &r=result.records[i]; r.blocked.ContextFlags=CONTEXT_ALL;
            if (!GetThreadContext(thread,&r.blocked)) {error=11;break;}
            memcpy(r.blocked_stack,(void*)(uintptr_t)r.blocked.Esp,sizeof(r.blocked_stack));
            if (r.blocked.Eip!=result.nt_wait+12 || r.blocked_stack[0]!=consumer ||
                r.blocked_stack[1]!=(DWORD)(uintptr_t)response_event || r.blocked_stack[2]!=0 ||
                (i<3?r.blocked_stack[3]!=0:r.blocked_stack[3]==0) || values.count!=0 ||
                r.blocked.Dr0||r.blocked.Dr1||r.blocked.Dr2||r.blocked.Dr3||(r.blocked.Dr7&255)||
                (r.blocked.EFlags&0x10100)) {error=12;break;}
            saved_debug=r.blocked;
            r.debug_port=DebugPort();
            if (gated) {
                CONTEXT debug=saved_debug;debug.ContextFlags=CONTEXT_DEBUG_REGISTERS;
                debug.Dr0=consumer;debug.Dr6=0;debug.Dr7=(debug.Dr7&~0x000f0003u)|1;
                armed=true;if (!SetThreadContext(thread,&debug)) {error=13;break;}
            }
            r.armed.ContextFlags=CONTEXT_ALL;
            if (!GetThreadContext(thread,&r.armed)) {error=35;break;}
            CONTEXT ordinary=r.armed; RestoreDebug(&ordinary);
            if (memcmp(&ordinary,&r.blocked,sizeof(ordinary)) ||
                (gated?(r.armed.Dr0!=consumer || (r.armed.Dr6&0xe00f)!=0 ||
                         r.armed.Dr7!=((saved_debug.Dr7&~0x000f0003u)|1) ||
                         r.armed.Dr1!=saved_debug.Dr1 || r.armed.Dr2!=saved_debug.Dr2 ||
                         r.armed.Dr3!=saved_debug.Dr3):!DebugEqual(r.armed,saved_debug))) {error=36;break;}
            if (ResumeThread(thread)!=1) {error=14;break;} suspended=false;
            if (i<3) {if (!SetEvent(response_event)) {error=15;break;} ++result.peer_signals;}
            if (gated) {
                ULONGLONG until=GetTickCount64()+2000;
                while (!InterlockedCompareExchange(&captured_state,0,0)&&GetTickCount64()<until) Sleep(1);
                if (!captured_state) {error=16;break;}
                // The first read cannot execute while the same worker is in VEH.
                if (values.count || values.consumed!=0xcccccccc || r.pre_count ||
                    r.trapped.Eax!=(i==3?WAIT_TIMEOUT:0) || r.debug_port!=0xffffffff) {error=17;break;}
                InterlockedExchange(&ack_state,1);
            }
            if (WaitForSingleObject(done_event,2000)!=WAIT_OBJECT_0) {error=19;break;}
            armed=false;
            previous=SuspendThread(thread);
            if (previous==0xffffffff) {error=30;break;}
            suspended=true;
            if (previous!=0) {error=30;break;}
            r.after.ContextFlags=CONTEXT_ALL;
            if (!GetThreadContext(thread,&r.after)||!DebugEqual(r.after,saved_debug)) {error=31;break;}
            if (ResumeThread(thread)!=1) {error=32;break;} suspended=false;
            if (i==3 && !SetEvent(go_event)) {error=37;break;}
            ++result.rounds;
        }
        if (error) break;
        if (WaitForSingleObject(thread,2000)!=WAIT_OBJECT_0 ||
            !GetExitCodeThread(thread,&result.worker_exit)||result.worker_exit!=0) {error=33;break;}
    } while(false);
    // Failure is contained by the parent/outer Job. Never free a live callback.
    InterlockedExchange(&stop_requested,1);
    InterlockedExchange(&ack_state,1); if (go_event) SetEvent(go_event); if (response_event) SetEvent(response_event);
    if (thread && armed) {
        if (!suspended && SuspendThread(thread)==0) suspended=true;
        if (suspended) {CONTEXT d=saved_debug;d.ContextFlags=CONTEXT_DEBUG_REGISTERS;SetThreadContext(thread,&d);}
    }
    if (thread && suspended) ResumeThread(thread);
    bool ended=!thread||WaitForSingleObject(thread,2500)==WAIT_OBJECT_0;
    if (!ended) error=error?error:34;
    if (ended) {
        if (thread && !GetExitCodeThread(thread,&result.worker_exit)) error=error?error:38;
        result.handler_removed=!veh||RemoveVectoredExceptionHandler(veh)!=0;
        if (nt) {memcpy(result.nt_after,nt,32);result.nt_unchanged=memcmp(result.nt_before,result.nt_after,32)==0;}
        if (code) {memcpy(result.code_after,code,result.code_size);result.code_unchanged=memcmp(result.code_before,result.code_after,result.code_size)==0;}
        result.memory_freed=!code||VirtualFree(code,0,MEM_RELEASE);
        result.tls_freed=tls_index==TLS_OUT_OF_INDEXES||TlsFree(tls_index);
        result.handles_closed=1;
        HANDLE handles[]={thread,begin_event,go_event,done_event,response_event};
        for (HANDLE h:handles) if (h&&!CloseHandle(h)) result.handles_closed=0;
    }
    result.error=error;
    if (!Save(folder,L"child.bin",&result,sizeof(result))) return 40;
    return error?41:0;
}
static int Parent(const wchar_t *folder) {
    wchar_t self[MAX_PATH],command[2*MAX_PATH],mode_path[MAX_PATH];
    DWORD self_len=GetModuleFileNameW(NULL,self,MAX_PATH);
    if (!self_len || self_len>=MAX_PATH || swprintf_s(mode_path,L"%s\\gated",folder)<0) return 54;
    bool observe=GetFileAttributesW(mode_path)!=INVALID_FILE_ATTRIBUTES;
    if (swprintf_s(command,L"\"%s\" child \"%s\" %d",self,folder,observe?1:0)<0) return 54;
    STARTUPINFOW si={sizeof(si)};PROCESS_INFORMATION pi={};
    si.dwFlags=STARTF_USESHOWWINDOW;si.wShowWindow=SW_HIDE;
    if (!CreateProcessW(self,command,NULL,NULL,FALSE,DEBUG_ONLY_THIS_PROCESS|CREATE_NO_WINDOW,NULL,folder,&si,&pi)) return 50;
    DWORD exit_code=STILL_ACTIVE,guards=0,steps=0,events=0,unhandled=0,continue_error=0;
    bool exited=false,forced=false,initial_break=false,ntdll_loaded=false;
    BYTE *ntdll=(BYTE*)GetModuleHandleW(L"ntdll.dll");
    IMAGE_DOS_HEADER *dos=(IMAGE_DOS_HEADER*)ntdll;
    IMAGE_NT_HEADERS *pe=(IMAGE_NT_HEADERS*)(ntdll+dos->e_lfanew);
    DWORD ntdll_size=pe->OptionalHeader.SizeOfImage;
    struct Event {DWORD pid,tid,type,exception,address,first,reply;} rows[128]={};
    ULONGLONG deadline=GetTickCount64()+15000;
    while (GetTickCount64()<deadline && events<128) {
        DEBUG_EVENT e={};if (!WaitForDebugEvent(&e,100)) continue;
        Event &r=rows[events++];r.pid=e.dwProcessId;r.tid=e.dwThreadId;r.type=e.dwDebugEventCode;
        DWORD reply=DBG_CONTINUE;
        if (e.dwDebugEventCode==EXCEPTION_DEBUG_EVENT) {
            r.exception=e.u.Exception.ExceptionRecord.ExceptionCode;
            r.address=(DWORD)(uintptr_t)e.u.Exception.ExceptionRecord.ExceptionAddress;r.first=e.u.Exception.dwFirstChance;
            reply=DBG_EXCEPTION_NOT_HANDLED;
            // Only the first main-thread loader INT3 in the child's observed
            // same-base ntdll mapping is the debugger's startup exception.
            // A later or foreign breakpoint retains the NOT_HANDLED policy.
            BYTE instruction=0;SIZE_T read=0;
            if ((r.exception==EXCEPTION_BREAKPOINT||r.exception==0x4000001f)&&!initial_break&&r.first&&
                e.dwThreadId==pi.dwThreadId&&ntdll_loaded&&
                r.address>=(DWORD)(uintptr_t)ntdll&&r.address-(DWORD)(uintptr_t)ntdll<ntdll_size&&
                ReadProcessMemory(pi.hProcess,(void*)(uintptr_t)r.address,&instruction,1,&read)&&
                read==1&&instruction==0xcc) {initial_break=true;reply=DBG_CONTINUE;}
            if (r.exception==EXCEPTION_SINGLE_STEP||r.exception==0x4000001e) ++steps;
            if (r.exception==STATUS_GUARD_PAGE_VIOLATION) ++guards;
            if (reply==DBG_EXCEPTION_NOT_HANDLED) ++unhandled;
        } else if (e.dwDebugEventCode==CREATE_PROCESS_DEBUG_EVENT && e.u.CreateProcessInfo.hFile) CloseHandle(e.u.CreateProcessInfo.hFile);
        else if (e.dwDebugEventCode==LOAD_DLL_DEBUG_EVENT) {
            if (e.u.LoadDll.lpBaseOfDll==ntdll) ntdll_loaded=true;
            if (e.u.LoadDll.hFile) CloseHandle(e.u.LoadDll.hFile);
        }
        else if (e.dwDebugEventCode==EXIT_PROCESS_DEBUG_EVENT) {exit_code=e.u.ExitProcess.dwExitCode;exited=true;}
        r.reply=reply;
        if (!ContinueDebugEvent(e.dwProcessId,e.dwThreadId,reply)) {continue_error=GetLastError();break;}
        if (exited) break;
    }
    bool signaled=WaitForSingleObject(pi.hProcess,exited&&!continue_error?1000:0)==WAIT_OBJECT_0;
    if (!exited||continue_error||!signaled) {
        forced=true;TerminateProcess(pi.hProcess,52);
        ULONGLONG cleanup_deadline=GetTickCount64()+2000;
        while (GetTickCount64()<cleanup_deadline && !signaled) {
            DEBUG_EVENT e={};
            if (WaitForDebugEvent(&e,50)) {
                if (e.dwDebugEventCode==CREATE_PROCESS_DEBUG_EVENT&&e.u.CreateProcessInfo.hFile) CloseHandle(e.u.CreateProcessInfo.hFile);
                if (e.dwDebugEventCode==LOAD_DLL_DEBUG_EVENT&&e.u.LoadDll.hFile) CloseHandle(e.u.LoadDll.hFile);
                ContinueDebugEvent(e.dwProcessId,e.dwThreadId,DBG_CONTINUE);
            }
            signaled=WaitForSingleObject(pi.hProcess,0)==WAIT_OBJECT_0;
        }
    }
    bool closed_thread=CloseHandle(pi.hThread)!=0;
    bool closed_process=CloseHandle(pi.hProcess)!=0;
    bool closed=closed_thread&&closed_process;
    char text[20000];int n=sprintf_s(text,"{\"pid\":%lu,\"child_pid\":%lu,\"exit_code\":%lu,\"exited\":%s,\"forced\":%s,\"handles_closed\":%s,\"child_signaled\":%s,\"continue_error\":%lu,\"initial_break\":%s,\"ntdll_loaded\":%s,\"ntdll_base\":%lu,\"ntdll_size\":%lu,\"single_steps\":%lu,\"guards\":%lu,\"unhandled\":%lu,\"events\":[",GetCurrentProcessId(),pi.dwProcessId,exit_code,exited?"true":"false",forced?"true":"false",closed?"true":"false",signaled?"true":"false",continue_error,initial_break?"true":"false",ntdll_loaded?"true":"false",(DWORD)(uintptr_t)ntdll,ntdll_size,steps,guards,unhandled);
    for (DWORD i=0;i<events;i++) {Event &r=rows[i];n+=sprintf_s(text+n,sizeof(text)-n,"%s{\"pid\":%lu,\"tid\":%lu,\"type\":%lu,\"exception\":%lu,\"address\":%lu,\"first\":%lu,\"reply\":%lu}",i?",":"",r.pid,r.tid,r.type,r.exception,r.address,r.first,r.reply);}
    n+=sprintf_s(text+n,sizeof(text)-n,"]}\n");bool saved=Save(folder,L"debugger.json",text,n);
    return !forced&&exited&&exit_code==0&&closed&&signaled&&initial_break&&saved?0:53;
}
int wmain(int argc,wchar_t **argv) {
    if (argc==3&&!wcscmp(argv[1],L"parent")) return Parent(argv[2]);
    if (argc==4&&!wcscmp(argv[1],L"child")&&(!wcscmp(argv[3],L"0")||!wcscmp(argv[3],L"1"))) return Child(argv[2],argv[3][0]=='1');
    return 60;
}
