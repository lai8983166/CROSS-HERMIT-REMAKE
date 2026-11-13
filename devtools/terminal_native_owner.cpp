// Same-PID, x86 native platform leaves for an external original-code executor.
// This executable never loads/executes a game image or guest callback. The one
// suspended worker starts at WorkerDispatcher; guest entry/parameter are an
// explicit projection recorded in its response and WORKER_START notification.
// Build /MT /EHsc /std:c++17 /link /SUBSYSTEM:WINDOWS /ENTRY:wmainCRTStartup.
#define WIN32_LEAN_AND_MEAN
#define NOMINMAX
#include <windows.h>
#include <intrin.h>
#include <stdint.h>
#include <stdio.h>
#include <algorithm>
#include <array>
#include <deque>
#include <map>
#include <mutex>
#include <sstream>
#include <string>
#include <utility>
#include <vector>

static_assert(sizeof(void *) == 4, "The owner must be compiled for x86");
namespace {
using U32 = uint32_t;
constexpr U32 kMaxBlock = 1u << 20;
constexpr U32 kMaxMemory = 4u << 20;
constexpr U32 kMaxTransfer = 32768;
constexpr U32 kMaxQueue = 256;
constexpr U32 kMaxLine = 2 * kMaxTransfer + 256;
constexpr uint64_t kMaxOutput = 16u << 20;
constexpr uint64_t kMaxInput = 16u << 20;
constexpr U32 kMaxCommands = 100000;
constexpr U32 kMaxSleep = 100;
constexpr U32 kGuestWorkerEntry = 0x56e110;

struct Request { U32 id = 0, lane = 0; std::string op; std::vector<std::string> args; };
struct Queue {
    SRWLOCK lock = SRWLOCK_INIT;
    CONDITION_VARIABLE ready = CONDITION_VARIABLE_INIT;
    std::deque<Request> rows;
    bool eof = false;
};
struct Allocation { U32 base, size, heap, pins; bool virtualMemory; };
struct Heap { HANDLE handle; U32 allocations = 0; };
struct Handle { HANDLE handle; bool thread; U32 pins = 0; };
struct Critical { U32 address, references = 0, owner = 0, depth = 0; };
struct Tls { std::array<U32, 2> values = {0, 0}; };
struct Lane { U32 tid = 0, teb = 0, lastError = 0; };
struct Result {
    U32 value = 0, error = 0;
    bool ok = true, exitThread = false, shutdown = false;
    std::string extras;
};

Queue queues[2];
Lane lanes[2];
std::mutex stateMutex, outputMutex;
std::map<U32, Allocation> allocations;
std::map<U32, Heap> heaps;
std::map<U32, Handle> handles;
std::map<U32, Critical> criticals;
std::map<U32, Tls> tlsSlots;
U32 allocationBytes = 0;
DWORD workerTid = 0, readerTid = 0;
U32 workerHandle = 0, guestEntry = 0, guestParameter = 0, guestTidPointer = 0;
bool workerCreated = false, workerResumed = false, workerExitRequested = false;
bool workerTerminationObserved = false, workerHandleClosed = false;
U32 workerExitCode = STILL_ACTIVE;
HANDLE outputHandle = INVALID_HANDLE_VALUE;
uint64_t outputBytes = 0;

U32 ptr(const void *p) { return static_cast<U32>(reinterpret_cast<uintptr_t>(p)); }
void *pointer(U32 p) { return reinterpret_cast<void *>(static_cast<uintptr_t>(p)); }
HANDLE handle(U32 h) { return reinterpret_cast<HANDLE>(static_cast<uintptr_t>(h)); }
std::string number(U32 n) { return std::to_string(n); }

// Infrastructure failures are process failures. The controller's enclosing Job
// owns failure cleanup; this helper never fabricates normal resource release.
[[noreturn]] void fatal(U32 code) { ExitProcess(code); }
void emit(const std::string &line) {
    std::lock_guard<std::mutex> guard(outputMutex);
    const std::string row = line + "\n";
    if (outputBytes + row.size() > kMaxOutput) fatal(71);
    outputBytes += row.size();
    size_t offset = 0;
    while (offset != row.size()) {
        DWORD wrote = 0;
        const DWORD count = static_cast<DWORD>(row.size() - offset);
        if (!WriteFile(outputHandle, row.data() + offset, count, &wrote, nullptr) || !wrote) fatal(72);
        offset += wrote;
    }
}
void response(const Request &q, const Result &r) {
    const Lane &lane = lanes[q.lane];
    emit("R " + number(q.id) + " " + number(q.lane) + " " + number(lane.tid) + " " +
         number(r.error) + " " + (r.ok ? "1" : "0") + " " + number(r.value) +
         " teb=" + number(lane.teb) + (r.extras.empty() ? "" : " " + r.extras));
}
Result reject(const char *reason, U32 error = ERROR_INVALID_PARAMETER) {
    Result r; r.ok = false; r.error = error; r.extras = std::string("reason=") + reason; return r;
}
bool parseU32(const std::string &s, U32 &value) {
    if (s.empty() || s.size() > 10) return false;
    uint64_t n = 0;
    for (char c : s) {
        if (c < '0' || c > '9') return false;
        n = n * 10 + static_cast<unsigned>(c - '0');
        if (n > UINT32_MAX) return false;
    }
    value = static_cast<U32>(n); return true;
}
bool numeric(const Request &q, size_t count, std::vector<U32> &a) {
    if (q.args.size() != count) return false;
    for (const auto &s : q.args) { U32 n; if (!parseU32(s, n)) return false; a.push_back(n); }
    return true;
}
int nibble(char c) {
    if (c >= '0' && c <= '9') return c - '0';
    if (c >= 'a' && c <= 'f') return c - 'a' + 10;
    if (c >= 'A' && c <= 'F') return c - 'A' + 10;
    return -1;
}
bool decodeHex(const std::string &s, std::vector<unsigned char> &bytes) {
    if (s.empty() || s.size() % 2 || s.size() > 2 * kMaxTransfer) return false;
    for (size_t i = 0; i < s.size(); i += 2) {
        int a = nibble(s[i]), b = nibble(s[i + 1]);
        if (a < 0 || b < 0) return false;
        bytes.push_back(static_cast<unsigned char>((a << 4) | b));
    }
    return true;
}
std::string encodeHex(const void *memory, U32 size) {
    static const char digits[] = "0123456789abcdef";
    const auto *p = static_cast<const unsigned char *>(memory);
    std::string out; out.resize(static_cast<size_t>(size) * 2);
    for (U32 i = 0; i < size; ++i) { out[2 * i] = digits[p[i] >> 4]; out[2 * i + 1] = digits[p[i] & 15]; }
    return out;
}
Allocation *ownedRange(U32 address, U32 length) {
    if (!length || static_cast<uint64_t>(address) + length > 0x100000000ull) return nullptr;
    auto it = allocations.upper_bound(address);
    if (it == allocations.begin()) return nullptr;
    --it;
    Allocation &a = it->second;
    if (address >= a.base && static_cast<uint64_t>(address) + length <= static_cast<uint64_t>(a.base) + a.size) return &a;
    return nullptr;
}
bool overlapsCritical(U32 address, U32 length) {
    for (const auto &item : criticals) {
        const uint64_t start = item.first;
        if (address < start + sizeof(CRITICAL_SECTION) && start < static_cast<uint64_t>(address) + length) return true;
    }
    return false;
}
bool allocationInTls(const Allocation &a) {
    for (const auto &slot : tlsSlots) for (U32 value : slot.second.values)
        if (value >= a.base && static_cast<uint64_t>(value) < static_cast<uint64_t>(a.base) + a.size) return true;
    return false;
}
bool allocationInOtherTls(const Allocation &a, U32 lane) {
    for (const auto &slot : tlsSlots) {
        const U32 value = slot.second.values[1 - lane];
        if (value >= a.base && static_cast<uint64_t>(value) < static_cast<uint64_t>(a.base) + a.size) return true;
    }
    return false;
}
void push(Request q) {
    Queue &queue = queues[q.lane];
    AcquireSRWLockExclusive(&queue.lock);
    if (queue.eof || queue.rows.size() >= kMaxQueue) fatal(73);
    queue.rows.push_back(std::move(q));
    WakeConditionVariable(&queue.ready);
    ReleaseSRWLockExclusive(&queue.lock);
}
bool pop(U32 lane, Request &q) {
    Queue &queue = queues[lane];
    AcquireSRWLockExclusive(&queue.lock);
    while (queue.rows.empty() && !queue.eof)
        if (!SleepConditionVariableSRW(&queue.ready, &queue.lock, INFINITE, 0)) fatal(74);
    const bool available = !queue.rows.empty();
    if (available) { q = std::move(queue.rows.front()); queue.rows.pop_front(); }
    ReleaseSRWLockExclusive(&queue.lock);
    return available;
}
void finishInput() {
    for (Queue &queue : queues) {
        AcquireSRWLockExclusive(&queue.lock);
        queue.eof = true;
        WakeAllConditionVariable(&queue.ready);
        ReleaseSRWLockExclusive(&queue.lock);
    }
}
DWORD WINAPI WorkerDispatcher(void *parameter);

// Every API invocation is made here by its requested, permanently bound lane.
// Queueing/output/ownership bookkeeping may alter Win32 LastError. Restore the
// previous leaf's captured value immediately before the next real API call.
Result dispatch(const Request &q) {
    Result r; std::vector<U32> a;
    std::unique_lock<std::mutex> guard(stateMutex);
    const U32 savedError = lanes[q.lane].lastError;
    const auto begin = [&]() { SetLastError(savedError); };
    const auto capture = [&]() { r.error = GetLastError(); };
    const auto args = [&](size_t count) { return numeric(q, count, a); };

    if (q.op == "GetCurrentThreadId") {
        if (!args(0)) return reject("ARGUMENTS");
        begin(); r.value = GetCurrentThreadId(); capture();
    } else if (q.op == "GetLastError") {
        if (!args(0)) return reject("ARGUMENTS");
        begin(); r.value = GetLastError(); capture();
    } else if (q.op == "SetLastError") {
        if (!args(1)) return reject("ARGUMENTS");
        SetLastError(a[0]); capture(); r.extras = "void=1";
    } else if (q.op == "GetCurrentProcessId") {
        if (!args(0)) return reject("ARGUMENTS");
        begin(); r.value = GetCurrentProcessId(); capture();
    } else if (q.op == "GetTickCount") {
        if (!args(0)) return reject("ARGUMENTS");
        begin(); r.value = GetTickCount(); capture();
    } else if (q.op == "Sleep") {
        if (!args(1) || a[0] > kMaxSleep) return reject("BOUNDED_SLEEP");
        guard.unlock(); begin(); Sleep(a[0]); capture(); r.extras = "void=1";
    } else if (q.op == "HeapCreate") {
        if (!args(3) || a[0] != 0 || a[1] > kMaxMemory || a[2] > kMaxMemory || heaps.size() >= 8)
            return reject("HEAP_CREATE_LIMIT");
        begin(); HANDLE h = HeapCreate(a[0], a[1], a[2]); capture();
        r.value = ptr(h); if (h) heaps.emplace(r.value, Heap{h});
    } else if (q.op == "HeapAlloc") {
        if (!args(3) || (a[1] & ~HEAP_ZERO_MEMORY) || !a[2] || a[2] > kMaxBlock ||
            allocationBytes + a[2] > kMaxMemory || allocations.size() >= 128) return reject("HEAP_ALLOC_LIMIT");
        auto h = heaps.find(a[0]); if (h == heaps.end()) return reject("UNKNOWN_HEAP");
        begin(); void *p = HeapAlloc(h->second.handle, a[1], a[2]); capture(); r.value = ptr(p);
        if (p) {
            allocations.emplace(r.value, Allocation{r.value, a[2], a[0], 0, false});
            allocationBytes += a[2]; ++h->second.allocations;
        }
    } else if (q.op == "HeapFree") {
        if (!args(3) || a[1]) return reject("ARGUMENTS");
        auto h = heaps.find(a[0]); auto p = allocations.find(a[2]);
        if (h == heaps.end() || p == allocations.end() || p->second.virtualMemory || p->second.heap != a[0])
            return reject("UNKNOWN_HEAP_ALLOCATION");
        // Original 57553e frees this thread's PTD before 57554f clears its TLS.
        // Preserve that ordering; another lane's live TLS still forbids freeing.
        if (p->second.pins || allocationInOtherTls(p->second, q.lane)) return reject("ALLOCATION_IN_USE", ERROR_BUSY);
        const bool pendingTlsClear = allocationInTls(p->second);
        begin(); r.value = HeapFree(h->second.handle, a[1], pointer(a[2])); capture();
        if (r.value) {
            allocationBytes -= p->second.size; allocations.erase(p); --h->second.allocations;
            if (pendingTlsClear) r.extras = "tls_reference_pending_clear=1";
        }
    } else if (q.op == "HeapValidate") {
        if (!args(3) || a[1]) return reject("ARGUMENTS");
        auto h = heaps.find(a[0]); if (h == heaps.end()) return reject("UNKNOWN_HEAP");
        if (a[2]) { auto p = allocations.find(a[2]); if (p == allocations.end() || p->second.heap != a[0]) return reject("UNKNOWN_HEAP_ALLOCATION"); }
        begin(); r.value = HeapValidate(h->second.handle, a[1], pointer(a[2])); capture();
    } else if (q.op == "HeapDestroy") {
        if (!args(1)) return reject("ARGUMENTS");
        auto h = heaps.find(a[0]); if (h == heaps.end()) return reject("UNKNOWN_HEAP");
        if (h->second.allocations) return reject("HEAP_NOT_EMPTY", ERROR_BUSY);
        begin(); r.value = HeapDestroy(h->second.handle); capture(); if (r.value) heaps.erase(h);
    } else if (q.op == "MEM_ALLOC") {
        if (!args(1) || !a[0] || a[0] > kMaxBlock || allocationBytes + a[0] > kMaxMemory || allocations.size() >= 128)
            return reject("MEM_ALLOC_LIMIT");
        begin(); void *p = VirtualAlloc(nullptr, a[0], MEM_RESERVE | MEM_COMMIT, PAGE_READWRITE); capture(); r.value = ptr(p);
        if (p) { allocations.emplace(r.value, Allocation{r.value, a[0], 0, 0, true}); allocationBytes += a[0]; }
        r.extras = "infrastructure=1 native_last_error=" + number(r.error); r.error = savedError;
    } else if (q.op == "MEM_FREE") {
        if (!args(1)) return reject("ARGUMENTS");
        auto p = allocations.find(a[0]);
        if (p == allocations.end() || !p->second.virtualMemory) return reject("UNKNOWN_VIRTUAL_ALLOCATION");
        if (p->second.pins || allocationInTls(p->second)) return reject("ALLOCATION_IN_USE", ERROR_BUSY);
        begin(); r.value = VirtualFree(pointer(a[0]), 0, MEM_RELEASE); capture();
        if (r.value) { allocationBytes -= p->second.size; allocations.erase(p); }
        r.extras = "infrastructure=1 native_last_error=" + number(r.error); r.error = savedError;
    } else if (q.op == "MEM_READ") {
        if (!args(2) || !a[1] || a[1] > kMaxTransfer || !ownedRange(a[0], a[1]) || overlapsCritical(a[0], a[1]))
            return reject("READ_RANGE");
        r.value = a[1]; r.error = savedError; r.extras = "hex=" + encodeHex(pointer(a[0]), a[1]);
    } else if (q.op == "MEM_WRITE") {
        U32 address = 0; std::vector<unsigned char> bytes;
        if (q.args.size() != 2 || !parseU32(q.args[0], address) || !decodeHex(q.args[1], bytes) ||
            !ownedRange(address, static_cast<U32>(bytes.size())) || overlapsCritical(address, static_cast<U32>(bytes.size())))
            return reject("WRITE_RANGE");
        memcpy(pointer(address), bytes.data(), bytes.size()); r.value = static_cast<U32>(bytes.size()); r.error = savedError;
    } else if (q.op == "InitializeCriticalSection") {
        if (!args(1) || (a[0] & 3) || criticals.size() >= 64 || criticals.count(a[0]) ||
            !ownedRange(a[0], sizeof(CRITICAL_SECTION)) || overlapsCritical(a[0], sizeof(CRITICAL_SECTION)))
            return reject("CRITICAL_SECTION_RANGE");
        begin(); InitializeCriticalSection(static_cast<LPCRITICAL_SECTION>(pointer(a[0]))); capture();
        criticals.emplace(a[0], Critical{a[0]}); ++ownedRange(a[0], sizeof(CRITICAL_SECTION))->pins;
        r.extras = "void=1 hex=" + encodeHex(pointer(a[0]), sizeof(CRITICAL_SECTION));
    } else if (q.op == "EnterCriticalSection") {
        if (!args(1)) return reject("ARGUMENTS");
        auto cs = criticals.find(a[0]); if (cs == criticals.end()) return reject("UNKNOWN_CRITICAL_SECTION");
        ++cs->second.references; guard.unlock();
        begin(); EnterCriticalSection(static_cast<LPCRITICAL_SECTION>(pointer(a[0]))); capture();
        guard.lock(); cs = criticals.find(a[0]); --cs->second.references;
        if (cs->second.owner && cs->second.owner != lanes[q.lane].tid) fatal(75);
        cs->second.owner = lanes[q.lane].tid; ++cs->second.depth;
        r.extras = "void=1 hex=" + encodeHex(pointer(a[0]), sizeof(CRITICAL_SECTION));
    } else if (q.op == "LeaveCriticalSection") {
        if (!args(1)) return reject("ARGUMENTS");
        auto cs = criticals.find(a[0]); if (cs == criticals.end()) return reject("UNKNOWN_CRITICAL_SECTION");
        if (cs->second.owner != lanes[q.lane].tid || !cs->second.depth) return reject("CRITICAL_SECTION_WRONG_OWNER");
        begin(); LeaveCriticalSection(static_cast<LPCRITICAL_SECTION>(pointer(a[0]))); capture();
        if (--cs->second.depth == 0) cs->second.owner = 0;
        r.extras = "void=1 hex=" + encodeHex(pointer(a[0]), sizeof(CRITICAL_SECTION));
    } else if (q.op == "DeleteCriticalSection") {
        if (!args(1)) return reject("ARGUMENTS");
        auto cs = criticals.find(a[0]); if (cs == criticals.end()) return reject("UNKNOWN_CRITICAL_SECTION");
        if (cs->second.depth || cs->second.references) return reject("CRITICAL_SECTION_IN_USE", ERROR_BUSY);
        begin(); DeleteCriticalSection(static_cast<LPCRITICAL_SECTION>(pointer(a[0]))); capture();
        --ownedRange(a[0], sizeof(CRITICAL_SECTION))->pins; criticals.erase(cs); r.extras = "void=1";
    } else if (q.op == "CreateEventA") {
        if (!args(4) || a[0] || a[1] > 1 || a[2] > 1 || a[3] || handles.size() >= 64)
            return reject("UNNAMED_EVENT_ONLY");
        begin(); HANDLE h = CreateEventA(nullptr, a[1], a[2], nullptr); capture(); r.value = ptr(h);
        if (h) handles.emplace(r.value, Handle{h, false});
    } else if (q.op == "ResetEvent" || q.op == "SetEvent") {
        if (!args(1)) return reject("ARGUMENTS");
        auto h = handles.find(a[0]); if (h == handles.end() || h->second.thread) return reject("UNKNOWN_EVENT");
        begin(); r.value = q.op == "SetEvent" ? SetEvent(h->second.handle) : ResetEvent(h->second.handle); capture();
    } else if (q.op == "WaitForSingleObject") {
        if (!args(2) || (a[1] > 1000 && a[1] != INFINITE)) return reject("WAIT_LIMIT");
        auto h = handles.find(a[0]); if (h == handles.end()) return reject("UNKNOWN_WAIT_HANDLE");
        if (h->second.thread && q.lane == 1) return reject("SELF_THREAD_WAIT");
        ++h->second.pins; const bool thread = h->second.thread; HANDLE native = h->second.handle;
        guard.unlock(); begin(); r.value = WaitForSingleObject(native, a[1]); capture(); guard.lock();
        --handles.at(a[0]).pins;
        if (thread && r.value == WAIT_OBJECT_0) workerTerminationObserved = true;
    } else if (q.op == "CloseHandle") {
        if (!args(1)) return reject("ARGUMENTS");
        auto h = handles.find(a[0]); if (h == handles.end()) return reject("UNKNOWN_HANDLE");
        if (h->second.pins || (h->second.thread && !workerTerminationObserved)) return reject("HANDLE_IN_USE", ERROR_BUSY);
        const bool thread = h->second.thread;
        begin(); r.value = CloseHandle(h->second.handle); capture();
        if (r.value) { handles.erase(h); if (thread) workerHandleClosed = true; }
    } else if (q.op == "CreateThread") {
        if (!args(6) || q.lane != 0 || a[0] || a[1] > kMaxBlock || a[2] != kGuestWorkerEntry ||
            a[4] != CREATE_SUSPENDED || workerCreated || handles.size() >= 64 || !ownedRange(a[3], 116))
            return reject("SINGLE_SUSPENDED_WORKER_CONTRACT");
        U32 ptdEntry = 0, ptdNode = 0;
        memcpy(&ptdEntry, static_cast<unsigned char *>(pointer(a[3])) + 0x48, sizeof(ptdEntry));
        memcpy(&ptdNode, static_cast<unsigned char *>(pointer(a[3])) + 0x4c, sizeof(ptdNode));
        if (ptdEntry != 0x421f50 || !ptdNode || overlapsCritical(a[3], 116)) return reject("ORIGINAL_PTD_CALLBACK_CONTRACT");
        const std::string ptdBytes = encodeHex(pointer(a[3]), 116);
        // The native entry is deliberately not the guest entry; no executable
        // game bytes are installed in this process. guestTidPointer is metadata.
        guestEntry = a[2]; guestParameter = a[3]; guestTidPointer = a[5];
        begin(); HANDLE h = CreateThread(nullptr, a[1], WorkerDispatcher, pointer(a[3]), a[4], &workerTid); capture();
        r.value = ptr(h);
        if (h) {
            workerCreated = true; workerHandle = r.value; handles.emplace(r.value, Handle{h, true});
            r.extras = "worker_tid=" + number(workerTid) + " guest_entry=" + number(guestEntry) +
                " guest_param=" + number(guestParameter) + " native_entry=" + number(ptr(reinterpret_cast<void *>(&WorkerDispatcher))) +
                " guest_tid_ptr=" + number(guestTidPointer) + " ptd_entry=" + number(ptdEntry) +
                " ptd_node=" + number(ptdNode) + " ptd_hex=" + ptdBytes;
        }
    } else if (q.op == "ResumeThread") {
        if (!args(1) || q.lane != 0 || a[0] != workerHandle || !workerCreated || workerResumed || workerHandleClosed)
            return reject("SINGLE_RESUME_CONTRACT");
        begin(); r.value = ResumeThread(handle(a[0])); capture(); if (r.value != UINT32_MAX) workerResumed = true;
    } else if (q.op == "GetExitCodeThread") {
        if (!args(1) || a[0] != workerHandle || !workerCreated || workerHandleClosed) return reject("UNKNOWN_THREAD");
        DWORD code = 0; begin(); r.value = GetExitCodeThread(handle(a[0]), &code); capture();
        if (r.value) { workerExitCode = code; r.extras = "exit_code=" + number(code); }
    } else if (q.op == "ExitThread") {
        if (!args(1) || q.lane != 1 || workerExitRequested) return reject("WORKER_EXIT_ONLY");
        for (const auto &cs : criticals) if (cs.second.owner == lanes[1].tid) return reject("EXIT_WITH_HELD_CRITICAL_SECTION", ERROR_BUSY);
        for (const auto &slot : tlsSlots) if (slot.second.values[1]) return reject("EXIT_WITH_LIVE_TLS", ERROR_BUSY);
        workerExitRequested = true; r.value = a[0]; r.error = savedError; r.exitThread = true;
        r.extras = "exit_requested=1 termination_observed=0";
    } else if (q.op == "TlsAlloc") {
        if (!args(0) || tlsSlots.size() >= 16) return reject("TLS_LIMIT");
        begin(); r.value = TlsAlloc(); capture(); if (r.value != TLS_OUT_OF_INDEXES) tlsSlots.emplace(r.value, Tls{});
    } else if (q.op == "TlsSetValue") {
        if (!args(2)) return reject("ARGUMENTS");
        auto slot = tlsSlots.find(a[0]); if (slot == tlsSlots.end()) return reject("UNKNOWN_TLS_INDEX");
        if (a[1] && !ownedRange(a[1], 1)) return reject("TLS_VALUE_NOT_OWNED");
        begin(); r.value = TlsSetValue(a[0], pointer(a[1])); capture(); if (r.value) slot->second.values[q.lane] = a[1];
    } else if (q.op == "TlsGetValue") {
        if (!args(1) || !tlsSlots.count(a[0])) return reject("UNKNOWN_TLS_INDEX");
        begin(); r.value = ptr(TlsGetValue(a[0])); capture();
        r.extras = "tracked_value=" + number(tlsSlots.at(a[0]).values[q.lane]);
        if (r.value != tlsSlots.at(a[0]).values[q.lane]) fatal(76);
    } else if (q.op == "TlsFree") {
        if (!args(1)) return reject("ARGUMENTS");
        auto slot = tlsSlots.find(a[0]); if (slot == tlsSlots.end()) return reject("UNKNOWN_TLS_INDEX");
        if (slot->second.values[0] || slot->second.values[1]) return reject("TLS_SLOT_NOT_CLEARED", ERROR_BUSY);
        begin(); r.value = TlsFree(a[0]); capture(); if (r.value) tlsSlots.erase(slot);
    } else if (q.op == "IsBadReadPtr" || q.op == "IsBadWritePtr") {
        if (!args(2) || !a[1] || a[1] > kMaxTransfer || !ownedRange(a[0], a[1]) || overlapsCritical(a[0], a[1]))
            return reject("POINTER_PROBE_NOT_OWNED");
#pragma warning(push)
#pragma warning(disable: 4996)
        begin(); r.value = q.op == "IsBadReadPtr" ? IsBadReadPtr(pointer(a[0]), a[1]) : IsBadWritePtr(pointer(a[0]), a[1]); capture();
#pragma warning(pop)
    } else if (q.op == "GetVersionExA") {
        if (!args(1) || !ownedRange(a[0], sizeof(OSVERSIONINFOA)) || overlapsCritical(a[0], sizeof(OSVERSIONINFOA)))
            return reject("VERSION_RANGE");
        auto *version = static_cast<OSVERSIONINFOA *>(pointer(a[0]));
        if (version->dwOSVersionInfoSize != sizeof(OSVERSIONINFOA)) return reject("VERSION_SIZE_148_REQUIRED");
#pragma warning(push)
#pragma warning(disable: 4996)
        begin(); r.value = GetVersionExA(version); capture();
#pragma warning(pop)
    } else if (q.op == "GetCurrentDirectoryA") {
        if (!args(2) || !a[0] || a[0] > kMaxTransfer || !ownedRange(a[1], a[0]) || overlapsCritical(a[1], a[0]))
            return reject("DIRECTORY_RANGE");
        begin(); r.value = GetCurrentDirectoryA(a[0], static_cast<LPSTR>(pointer(a[1]))); capture();
    } else if (q.op == "STATUS" || q.op == "Shutdown") {
        if (!args(0) || q.lane != 0) return reject("MAIN_CONTROL_ONLY");
        r.error = savedError;
        r.extras = "allocations=" + number(static_cast<U32>(allocations.size())) + " memory_bytes=" + number(allocationBytes) +
            " heaps=" + number(static_cast<U32>(heaps.size())) + " handles=" + number(static_cast<U32>(handles.size())) +
            " criticals=" + number(static_cast<U32>(criticals.size())) + " tls_slots=" + number(static_cast<U32>(tlsSlots.size())) +
            " worker_created=" + number(workerCreated) + " worker_resumed=" + number(workerResumed) +
            " exit_requested=" + number(workerExitRequested) + " termination_observed=" + number(workerTerminationObserved) +
            " worker_handle_closed=" + number(workerHandleClosed) + " worker_exit_code=" + number(workerExitCode);
        if (q.op == "Shutdown") {
            if (!allocations.empty() || !heaps.empty() || !handles.empty() || !criticals.empty() || !tlsSlots.empty() ||
                (workerCreated && (!workerExitRequested || !workerTerminationObserved || !workerHandleClosed || workerExitCode == STILL_ACTIVE)))
                return reject("SHUTDOWN_RESOURCES_LIVE", ERROR_BUSY);
            r.shutdown = true; r.value = 1;
        }
    } else return reject("OPERATION_NOT_WHITELISTED", ERROR_NOT_SUPPORTED);
    return r;
}

DWORD WINAPI WorkerDispatcher(void *parameter) {
    lanes[1].tid = GetCurrentThreadId(); lanes[1].teb = __readfsdword(0x18); lanes[1].lastError = 0;
    {
        std::lock_guard<std::mutex> guard(stateMutex);
        if (!workerCreated || lanes[1].tid != workerTid || ptr(parameter) != guestParameter) fatal(77);
        emit("E WORKER_START worker_tid=" + number(workerTid) + " teb=" + number(lanes[1].teb) +
             " guest_entry=" + number(guestEntry) + " guest_param=" + number(guestParameter) +
             " native_entry=" + number(ptr(reinterpret_cast<void *>(&WorkerDispatcher))));
    }
    for (;;) {
        U32 exitCode = 0; bool exiting = false;
        {
            Request q;
            if (!pop(1, q)) fatal(78);
            Result r = dispatch(q);
            lanes[1].lastError = r.error; response(q, r);
            exiting = r.exitThread; exitCode = r.value;
        } // Destroy request/result before the actual non-returning OS leaf.
        if (exiting) { SetLastError(lanes[1].lastError); ExitThread(exitCode); }
    }
}
DWORD WINAPI Reader(void *) {
    HANDLE input = GetStdHandle(STD_INPUT_HANDLE);
    uint64_t inputBytes = 0; U32 previousId = 0, commands = 0;
    std::string line;
    for (;;) {
        char buffer[4096]; DWORD got = 0;
        if (!ReadFile(input, buffer, sizeof(buffer), &got, nullptr)) {
            if (GetLastError() == ERROR_BROKEN_PIPE) break;
            fatal(79);
        }
        if (!got) break;
        inputBytes += got; if (inputBytes > kMaxInput) fatal(80);
        for (DWORD i = 0; i < got; ++i) {
            const char c = buffer[i];
            if (c == '\r') continue;
            if (c != '\n') {
                if ((c < 32 && c != '\t') || c > 126 || line.size() >= kMaxLine) fatal(81);
                line.push_back(c); continue;
            }
            Request q; std::istringstream stream(line); std::string id, lane, arg;
            if (!(stream >> id >> lane >> q.op) || !parseU32(id, q.id) || !parseU32(lane, q.lane) ||
                !q.id || q.id <= previousId || q.lane > 1 || q.op.size() > 32 || ++commands > kMaxCommands) fatal(82);
            while (stream >> arg) { if (q.args.size() == 8) fatal(83); q.args.push_back(std::move(arg)); }
            previousId = q.id; const bool final = q.op == "Shutdown";
            push(std::move(q)); line.clear();
            if (final) { if (i + 1 != got) fatal(84); finishInput(); return 0; }
        }
    }
    if (!line.empty()) fatal(85);
    finishInput(); return 0;
}
} // namespace

int wmain() {
    SetErrorMode(SEM_FAILCRITICALERRORS | SEM_NOGPFAULTERRORBOX | SEM_NOOPENFILEERRORBOX);
    outputHandle = GetStdHandle(STD_OUTPUT_HANDLE);
    HANDLE input = GetStdHandle(STD_INPUT_HANDLE);
    if (!input || input == INVALID_HANDLE_VALUE || !outputHandle || outputHandle == INVALID_HANDLE_VALUE ||
        GetFileType(input) != FILE_TYPE_PIPE || GetFileType(outputHandle) != FILE_TYPE_PIPE) return 60;
    // No console, GUI, arbitrary process attachment, file, desktop or input APIs.
    lanes[0].tid = GetCurrentThreadId(); lanes[0].teb = __readfsdword(0x18);
    HANDLE reader = CreateThread(nullptr, 0, Reader, nullptr, CREATE_SUSPENDED, &readerTid);
    if (!reader) return 61;
    emit("E READY version=1 pid=" + number(GetCurrentProcessId()) + " main_tid=" + number(lanes[0].tid) +
         " main_teb=" + number(lanes[0].teb) + " reader_tid=" + number(readerTid) + " pointer_bits=32");
    if (ResumeThread(reader) != 1) return 62;
    bool shutdown = false;
    for (;;) {
        Request q; if (!pop(0, q)) break;
        Result r = dispatch(q); lanes[0].lastError = r.error; response(q, r);
        if (r.shutdown) { shutdown = true; break; }
    }
    if (!shutdown) return 63;
    if (WaitForSingleObject(reader, 1000) != WAIT_OBJECT_0 || !CloseHandle(reader)) return 64;
    return 0;
}
