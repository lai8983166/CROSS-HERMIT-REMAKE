// Additive synchronous, same-MAIN WNDPROC bridge. No guest code executes here.
constexpr U32 kWindowGuestEntry = 0x424980;
constexpr U32 kMaxCallbacks = 128, kMaxCallbackDepth = 8;
constexpr U32 kWindowGuestClass = 0x7a2628;
const wchar_t kResourcePath[] = L"@@RESOURCE_PATH@@";
const char kResourceHex[] = "@@RESOURCE_HEX@@";
const char kWindowClass[] = "Cross Hermit";
const char kWindowProperty[] = "CPP_CLASS";
bool windowGate = false, creatingWindow = false, destroyingWindow = false;
HMODULE windowModule = nullptr;
ATOM windowClassAtom = 0;
HWND ownedWindow = nullptr, retiredWindow = nullptr;
U32 windowGuestOwner = 0, windowParentRequest = 0, callbackSequence = 0;
HICON windowIcons[2] = {nullptr, nullptr}; U32 windowIconLoads = 0;
HCURSOR windowCursor = nullptr; HGDIOBJ windowBrush = nullptr;
struct WindowCallback {
    U32 id, parentRequest, parentCallback, depth, entryError;
    HWND hwnd; UINT message; WPARAM w; LPARAM l;
};
std::vector<WindowCallback> windowCallbacks;
LRESULT CALLBACK OriginalWindowBridge(HWND, UINT, WPARAM, LPARAM);
Result windowDispatch(const Request &, std::unique_lock<std::mutex> &, U32);

bool windowOp(const std::string &op) {
    static const char *const names[] = {"WINDOW_GATE", "WINDOW_MODULE", "WINDOW_MODULE_CLOSE",
        "FindWindowA", "SetRect", "AdjustWindowRect", "LoadIconA", "LoadCursorA", "GetStockObject",
        "RegisterClassExA", "CreateWindowExA", "ShowWindow", "UpdateWindow", "GetClientRect", "GetWindowRect",
        "GetWindowLongA", "SetWindowLongA", "DestroyWindow", "UnregisterClassA",
        "CB_GET_PROP", "CB_SET_PROP", "CB_GET_LONG", "CB_DEFAULT", "CB_RETURN", "CB_REMOVE_PROP", "CB_POST_QUIT"};
    for (const char *name : names) if (op == name) return true;
    return false;
}
bool callbackOp(const std::string &op) {
    return op == "CB_GET_PROP" || op == "CB_SET_PROP" || op == "CB_GET_LONG" ||
        op == "CB_DEFAULT" || op == "CB_RETURN" || op == "CB_REMOVE_PROP" || op == "CB_POST_QUIT";
}
bool windowRange(U32 address, U32 length) {
    return ownedRange(address, length) && !overlapsCritical(address, length);
}
bool windowString(U32 address, const char *expected) {
    const U32 length = static_cast<U32>(strlen(expected)) + 1;
    return windowRange(address, length) && !memcmp(pointer(address), expected, length);
}
U32 callbackBytes(const WindowCallback &c) {
    if (c.message == WM_NCCREATE || c.message == WM_CREATE) return sizeof(CREATESTRUCTA);
    if (c.message == WM_NCCALCSIZE) {
        if (c.w) fatal(90); // Pointer-bearing NCCALCSIZE_PARAMS is not this startup contract.
        return sizeof(RECT);
    }
    if (c.message == WM_WINDOWPOSCHANGING || c.message == WM_WINDOWPOSCHANGED) return sizeof(WINDOWPOS);
    if (c.message == WM_GETMINMAXINFO) return sizeof(MINMAXINFO);
    return 0;
}
const char *callbackKind(const WindowCallback &c) {
    if (c.message == WM_NCCREATE || c.message == WM_CREATE) return "CREATESTRUCTA";
    if (c.message == WM_NCCALCSIZE) return "RECT";
    if (c.message == WM_WINDOWPOSCHANGING || c.message == WM_WINDOWPOSCHANGED) return "WINDOWPOS";
    if (c.message == WM_GETMINMAXINFO) return "MINMAXINFO";
    return "opaque";
}
std::string callbackData(const WindowCallback &c) {
    U32 bytes = callbackBytes(c);
    if (bytes && !c.l) fatal(91);
    return bytes ? encodeHex(reinterpret_cast<const void *>(c.l), bytes) : "-";
}
// Every potentially synchronous Win32 call releases stateMutex before entering
// USER32. The callback consumes the same MAIN queue and reacquires it per leaf.
struct WindowCallScope {
    std::unique_lock<std::mutex> &guard;
    U32 previous;
    WindowCallScope(std::unique_lock<std::mutex> &g, U32 request) : guard(g), previous(windowParentRequest) {
        windowParentRequest = request; guard.unlock();
    }
    ~WindowCallScope() { guard.lock(); windowParentRequest = previous; }
};
U32 registerClassEax(const WNDCLASSEXA *wc) {
    U32 result;
    __asm { mov eax, wc
            push eax
            call RegisterClassExA
            mov result, eax }
    return result;
}
std::string callbackTls(U32 savedError) {
    std::lock_guard<std::mutex> guard(stateMutex);
    if (tlsSlots.size() > 1) fatal(101);
    U32 slot = UINT32_MAX, value = 0, tracked = 0, error = 0, bytes = 0;
    std::string data = "-";
    if (!tlsSlots.empty()) {
        slot = tlsSlots.begin()->first; tracked = tlsSlots.begin()->second.values[0];
        SetLastError(0); value = ptr(TlsGetValue(slot)); error = GetLastError();
        if (value != tracked || error) fatal(102);
        if (value) {
            if (!windowRange(value,116)) fatal(103);
            bytes = 116; data = encodeHex(pointer(value),bytes);
        }
    }
    SetLastError(savedError);
    return " tls_slot=" + number(slot) + " tls_value=" + number(value) +
        " tls_tracked_value=" + number(tracked) + " tls_error=" + number(error) +
        " ptd_bytes=" + number(bytes) + " ptd_hex=" + data;
}
LRESULT CALLBACK OriginalWindowBridge(HWND hwnd, UINT message, WPARAM w, LPARAM l) {
    const U32 entryError = GetLastError();
    WindowCallback c{};
    {
        std::lock_guard<std::mutex> guard(stateMutex);
        if (!windowGate || GetCurrentThreadId() != lanes[0].tid || __readfsdword(0x18) != lanes[0].teb ||
            !windowParentRequest || windowCallbacks.size() >= kMaxCallbackDepth || callbackSequence >= kMaxCallbacks) fatal(92);
        if (creatingWindow && !ownedWindow) ownedWindow = hwnd;
        if (!hwnd || hwnd != ownedWindow) fatal(93);
        const U32 parentCallback = windowCallbacks.empty() ? 0 : windowCallbacks.back().id;
        c = WindowCallback{++callbackSequence, windowParentRequest, parentCallback,
            static_cast<U32>(windowCallbacks.size()) + 1, entryError, hwnd, message, w, l};
        windowCallbacks.push_back(c); lanes[0].lastError = entryError;
    } // callbackTls takes its own short lock; never hold it across transport.
    const U32 bytes = callbackBytes(c);
    const std::string tls = callbackTls(entryError);
    emit("C callback_id=" + number(c.id) + " parent_request=" + number(c.parentRequest) +
         " parent_callback_id=" + number(c.parentCallback) + " depth=" + number(c.depth) +
         " lane=0 tid=" + number(lanes[0].tid) + " teb=" + number(lanes[0].teb) +
         " guest_entry=" + number(kWindowGuestEntry) + " hwnd=" + number(ptr(hwnd)) +
         " message=" + number(message) + " wParam=" + number(static_cast<U32>(w)) +
         " lParam=" + number(static_cast<U32>(l)) + " last_error=" + number(entryError) +
         " data_kind=" + callbackKind(c) + " data_bytes=" + number(bytes) + " data_hex=" + callbackData(c) + tls);
    for (;;) {
        Request q; if (!pop(0, q)) fatal(94);
        std::unique_lock<std::mutex> guard(stateMutex);
        if (q.lane || !callbackOp(q.op)) fatal(95);
        const bool returning = q.op == "CB_RETURN";
        Result r = windowDispatch(q, guard, lanes[0].lastError);
        r.extras += " callback_id=" + number(c.id) + " parent_request=" + number(c.parentRequest) + " depth=" + number(c.depth);
        lanes[0].lastError = r.error; response(q, r);
        if (!r.ok) fatal(96); // No fabricated callback fallback or continuation after a mismatched return.
        if (returning) {
            if (windowCallbacks.empty() || windowCallbacks.back().id != c.id) fatal(97);
            windowCallbacks.pop_back();
            if (message == WM_NCDESTROY) { retiredWindow = hwnd; ownedWindow = nullptr; }
            U32 result = 0; if (!parseU32(q.args[1],result)) fatal(104);
            const U32 error = r.error;
            guard.unlock(); SetLastError(error); return static_cast<LRESULT>(result);
        }
    }
}
Result windowDispatch(const Request &q, std::unique_lock<std::mutex> &guard, U32 savedError) {
    Result r; r.error = savedError; std::vector<U32> a;
    const auto args = [&](size_t n) { return numeric(q, n, a); };
    const auto begin = [&]() { SetLastError(savedError); };
    const auto capture = [&]() { r.error = GetLastError(); };
    if (q.lane || GetCurrentThreadId() != lanes[0].tid || __readfsdword(0x18) != lanes[0].teb)
        return reject("WINDOW_MAIN_LANE_ONLY");
    if (q.op == "WINDOW_GATE") {
        if (!args(1) || a[0] > 1 || !windowCallbacks.empty() || ownedWindow || windowClassAtom || windowModule)
            return reject("WINDOW_GATE_QUIESCENT_ONLY");
        windowGate = a[0] != 0; r.value = 1; r.extras = "infrastructure=1 ui_gate=" + number(windowGate); return r;
    }
    if (!windowGate) return reject("WINDOW_GATE_CLOSED", ERROR_ACCESS_DENIED);
    if (callbackOp(q.op)) {
        if (windowCallbacks.empty()) return reject("ACTIVE_CALLBACK_REQUIRED");
        const WindowCallback c = windowCallbacks.back();
        const size_t count = q.op == "CB_SET_PROP" || q.op == "CB_GET_LONG" ? 3 : q.op == "CB_DEFAULT" ? 5 : 2;
        if (!args(count) || a[0] != c.id) return reject("MATCHING_CALLBACK_ID_REQUIRED");
        if (q.op == "CB_RETURN") { r.value = 1; r.extras = "callback_result=" + number(a[1]); return r; }
        if (q.op == "CB_POST_QUIT") {
            if (a[1] || c.message != WM_DESTROY || !destroyingWindow) return reject("ORIGINAL_DESTROY_QUIT_ONLY");
            begin(); PostQuitMessage(0); capture(); r.extras = "void=1"; return r;
        }
        if (a[1] != ptr(c.hwnd)) return reject("ACTIVE_CALLBACK_HWND_REQUIRED");
        if (q.op == "CB_GET_PROP") {
            begin(); r.value = ptr(GetPropA(c.hwnd, kWindowProperty)); capture(); return r;
        }
        if (q.op == "CB_SET_PROP") {
            if (!windowGuestOwner || a[2] != windowGuestOwner || (c.message != WM_NCCREATE && c.message != WM_CREATE))
                return reject("ORIGINAL_CREATION_GUEST_OWNER_REQUIRED");
            begin(); r.value = SetPropA(c.hwnd, kWindowProperty, handle(a[2])); capture();
            SetLastError(0); const U32 observed = ptr(GetPropA(c.hwnd,kWindowProperty)); const U32 error = GetLastError();
            SetLastError(r.error); r.extras = "observed_property=" + number(observed) +
                " observed_property_error=" + number(error) + " auxiliary_readback=1"; return r;
        }
        if (q.op == "CB_REMOVE_PROP") {
            if (!destroyingWindow || (c.message != WM_DESTROY && c.message != WM_NCDESTROY))
                return reject("ORIGINAL_DESTROY_PROPERTY_ONLY");
            begin(); r.value = ptr(RemovePropA(c.hwnd, kWindowProperty)); capture();
            SetLastError(0); const U32 observed = ptr(GetPropA(c.hwnd,kWindowProperty)); const U32 error = GetLastError();
            SetLastError(r.error); r.extras = "observed_property=" + number(observed) +
                " observed_property_error=" + number(error) + " auxiliary_readback=1"; return r;
        }
        if (q.op == "CB_GET_LONG") {
            const LONG index = static_cast<LONG>(a[2]);
            if (index != 4 && index != GWL_WNDPROC) return reject("CALLBACK_WINDOW_LONG_INDEX");
            begin(); U32 actual = static_cast<U32>(GetWindowLongA(c.hwnd, index)); capture();
            const bool translated = index == GWL_WNDPROC && actual == ptr(reinterpret_cast<void *>(&OriginalWindowBridge));
            r.value = translated ? kWindowGuestEntry : actual;
            r.extras = "host_result=" + number(actual) + " reverse_translated=" + number(translated) +
                " guest_callback=" + number(kWindowGuestEntry) + " native_callback=" + number(ptr(reinterpret_cast<void *>(&OriginalWindowBridge)));
            return r;
        }
        if (a[2] != c.message || a[3] != static_cast<U32>(c.w) || a[4] != static_cast<U32>(c.l))
            return reject("ORIGINAL_DEFAULT_ARGUMENTS_REQUIRED");
        const std::string before = callbackData(c);
        { WindowCallScope call(guard, q.id); begin(); r.value = static_cast<U32>(DefWindowProcA(c.hwnd, c.message, c.w, c.l)); capture(); }
        r.extras = "before_hex=" + before + " after_hex=" + callbackData(c) + " data_bytes=" + number(callbackBytes(c)); return r;
    }
    if (!windowCallbacks.empty()) return reject("MAIN_LEAF_FORBIDDEN_IN_CALLBACK");
    if (q.op == "WINDOW_MODULE") {
        if (!args(0) || windowModule) return reject("ONE_RESOURCE_MODULE_ONLY");
        std::vector<unsigned char> expected;
        if (!decodeHex(kResourceHex, expected) || expected.size() != 3072) fatal(98);
        begin(); HANDLE file = CreateFileW(kResourcePath, GENERIC_READ, FILE_SHARE_READ, nullptr, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, nullptr); capture();
        if (file == INVALID_HANDLE_VALUE) return r;
        LARGE_INTEGER size{}; std::vector<unsigned char> data(expected.size()); DWORD read = 0;
        const bool exact = GetFileSizeEx(file, &size) && size.QuadPart == static_cast<LONGLONG>(expected.size()) &&
            ReadFile(file, data.data(), static_cast<DWORD>(data.size()), &read, nullptr) && read == expected.size() && data == expected;
        if (!exact) { const BOOL closed = CloseHandle(file); (void)closed; return reject("RESOURCE_MODULE_BYTES_CHANGED"); }
        begin(); windowModule = LoadLibraryExW(kResourcePath, nullptr, LOAD_LIBRARY_SEARCH_DLL_LOAD_DIR | LOAD_LIBRARY_SEARCH_SYSTEM32); capture();
        const BOOL closed = CloseHandle(file); if (!closed) fatal(99);
        r.value = ptr(windowModule); r.extras = "resource_bytes=3072 resource_entry=0 file_closed=1"; return r;
    }
    if (q.op == "WINDOW_MODULE_CLOSE") {
        if (!args(1) || !windowModule || a[0] != ptr(windowModule) || windowClassAtom || ownedWindow)
            return reject("RESOURCE_MODULE_STILL_IN_USE");
        begin(); r.value = FreeLibrary(windowModule); capture();
        if (r.value) { windowModule = nullptr; windowIcons[0] = windowIcons[1] = nullptr; windowIconLoads = 0; windowCursor = nullptr; windowBrush = nullptr; }
        return r;
    }
    if (q.op == "FindWindowA") {
        if (!args(2) || !windowString(a[0], kWindowClass) || a[1]) return reject("ORIGINAL_FIND_WINDOW_ARGS");
        { WindowCallScope call(guard, q.id); begin(); r.value = ptr(FindWindowA(kWindowClass, nullptr)); capture(); }
        r.extras = "returned_window_owned=0"; return r;
    }
    if (q.op == "SetRect") {
        if (!args(5) || !windowRange(a[0],16) || a[1] || a[2] || a[3] != 1024 || a[4] != 768) return reject("ORIGINAL_RECTANGLE_ARGS");
        begin(); r.value = SetRect(static_cast<LPRECT>(pointer(a[0])),0,0,1024,768); capture(); return r;
    }
    if (q.op == "AdjustWindowRect") {
        if (!args(3) || !windowRange(a[0],16) || a[1] != 0x90000000 || a[2]) return reject("ORIGINAL_RECTANGLE_STYLE");
        begin(); r.value = AdjustWindowRect(static_cast<LPRECT>(pointer(a[0])),a[1],FALSE); capture(); return r;
    }
    if (q.op == "LoadIconA") {
        if (!args(2) || !windowModule || a[0] != ptr(windowModule) || a[1] != 157 || windowIconLoads >= 2) return reject("ORIGINAL_MODULE_ICON157_ONLY");
        begin(); HICON icon = LoadIconA(windowModule, MAKEINTRESOURCEA(157)); capture(); r.value = ptr(icon);
        if (icon) windowIcons[windowIconLoads++] = icon; r.extras = "shared=1 destroy_permitted=0"; return r;
    }
    if (q.op == "LoadCursorA") {
        if (!args(2) || a[0] || a[1] != 32512 || windowCursor) return reject("ORIGINAL_SYSTEM_ARROW_ONLY");
        begin(); windowCursor = LoadCursorA(nullptr, MAKEINTRESOURCEA(32512)); capture(); r.value = ptr(windowCursor);
        r.extras = "shared=1 destroy_permitted=0"; return r;
    }
    if (q.op == "GetStockObject") {
        if (!args(1) || a[0] != 4 || windowBrush) return reject("ORIGINAL_STOCK_BRUSH_ONLY");
        begin(); windowBrush = GetStockObject(4); capture(); r.value = ptr(windowBrush); r.extras = "stock=1 delete_permitted=0"; return r;
    }
    if (q.op == "RegisterClassExA") {
        if (!args(1) || !windowRange(a[0],48) || !windowModule || windowClassAtom || windowIconLoads != 2 || !windowCursor || !windowBrush)
            return reject("ORIGINAL_READY_CLASS_REQUIRED");
        WNDCLASSEXA wc = *static_cast<const WNDCLASSEXA *>(pointer(a[0]));
        if (wc.cbSize != 48 || wc.style || ptr(reinterpret_cast<void *>(wc.lpfnWndProc)) != kWindowGuestEntry || wc.cbClsExtra || wc.cbWndExtra ||
            wc.hInstance != windowModule || wc.hIcon != windowIcons[0] || wc.hIconSm != windowIcons[1] || wc.hCursor != windowCursor ||
            ptr(wc.hbrBackground) != ptr(windowBrush) || wc.lpszMenuName || !windowString(ptr(wc.lpszClassName), kWindowClass)) return reject("ORIGINAL_CLASS_BYTES_REQUIRED");
        wc.lpfnWndProc = OriginalWindowBridge; wc.lpszClassName = kWindowClass;
        WNDCLASSEXA prior{}; prior.cbSize = sizeof(prior);
        if (GetClassInfoExA(windowModule,kWindowClass,&prior)) return reject("PREEXISTING_CLASS_NOT_OWNED");
        begin(); r.value = registerClassEax(&wc); capture(); windowClassAtom = static_cast<ATOM>(r.value);
        r.extras = "atom=" + number(windowClassAtom) + " guest_callback=" + number(kWindowGuestEntry) +
            " native_callback=" + number(ptr(reinterpret_cast<void *>(&OriginalWindowBridge))) + " host_class_hex=" + encodeHex(&wc,48); return r;
    }
    if (q.op == "CreateWindowExA") {
        if (!args(12) || !windowClassAtom || ownedWindow || retiredWindow || a[0] || a[1] != kWindowGuestClass ||
            a[2] != kWindowGuestClass || a[3] != 0x90000000 || a[4] != 16 || a[5] != 16 || a[6] != 1024 || a[7] != 768 ||
            a[8] || a[9] || a[10] != ptr(windowModule) || !a[11]) return reject("ORIGINAL_CREATE_WINDOW12_ARGS");
        windowGuestOwner = a[11]; creatingWindow = true;
        HWND result;
        { WindowCallScope call(guard,q.id); begin(); result=CreateWindowExA(0,kWindowClass,kWindowClass,a[3],16,16,1024,768,nullptr,nullptr,windowModule,pointer(a[11])); capture(); }
        creatingWindow = false; r.value = ptr(result);
        if (result && result != ownedWindow) fatal(100);
        if (!result && ownedWindow) return reject("FAILED_CREATION_LEFT_OWNED_WINDOW");
        r.extras = "callbacks=" + number(callbackSequence) + " guest_owner=" + number(windowGuestOwner) +
            " guest_class=" + number(kWindowGuestClass) + " native_class=" + number(ptr(kWindowClass)) +
            " guest_title=" + number(kWindowGuestClass) + " native_title=" + number(ptr(kWindowClass)); return r;
    }
    if (q.op == "UnregisterClassA") {
        if (!args(2) || !windowClassAtom || a[0] != windowClassAtom || a[1] != ptr(windowModule) || ownedWindow)
            return reject("OWNED_CLASS_WITHOUT_WINDOW_REQUIRED");
        begin(); r.value=UnregisterClassA(MAKEINTATOM(windowClassAtom),windowModule); capture(); if(r.value) windowClassAtom=0; return r;
    }
    const size_t count = q.op == "ShowWindow" || q.op == "GetClientRect" || q.op == "GetWindowRect" || q.op == "GetWindowLongA" ? 2 : q.op == "SetWindowLongA" ? 3 : 1;
    if (!args(count) || !ownedWindow || a[0] != ptr(ownedWindow)) return reject("CURRENT_OWNED_WINDOW_REQUIRED");
    if (q.op == "GetClientRect" || q.op == "GetWindowRect") {
        if (!windowRange(a[1],16)) return reject("RECT_OUTPUT_OWNED16_REQUIRED");
        begin(); r.value=q.op=="GetClientRect" ? GetClientRect(ownedWindow,static_cast<LPRECT>(pointer(a[1]))) : GetWindowRect(ownedWindow,static_cast<LPRECT>(pointer(a[1]))); capture(); return r;
    }
    if (q.op == "GetWindowLongA" || q.op == "SetWindowLongA") {
        const LONG index=static_cast<LONG>(a[1]);
        if(index != GWL_STYLE && index != GWL_EXSTYLE && index != GWL_USERDATA) return reject("OWNED_WINDOW_LONG_INDEX");
        if(q.op == "SetWindowLongA" && (index != GWL_USERDATA || (a[2] && a[2] != windowGuestOwner))) return reject("OPAQUE_OWNER_USERDATA_ONLY");
        begin(); r.value=static_cast<U32>(q.op=="GetWindowLongA" ? GetWindowLongA(ownedWindow,index) : SetWindowLongA(ownedWindow,index,static_cast<LONG>(a[2]))); capture(); return r;
    }
    if (q.op == "ShowWindow") {
        if (a[1] > SW_SHOWDEFAULT) return reject("BOUNDED_SHOW_COMMAND");
        { WindowCallScope call(guard,q.id); begin(); r.value=ShowWindow(ownedWindow,static_cast<int>(a[1])); capture(); } return r;
    }
    if (q.op == "UpdateWindow") {
        { WindowCallScope call(guard,q.id); begin(); r.value=UpdateWindow(ownedWindow); capture(); } return r;
    }
    if (q.op == "DestroyWindow") {
        HWND target=ownedWindow; destroyingWindow=true;
        { WindowCallScope call(guard,q.id); begin(); r.value=DestroyWindow(target); capture(); }
        destroyingWindow=false; const DWORD saved=GetLastError(); const BOOL still=IsWindow(target); SetLastError(saved);
        r.extras="is_window_after="+number(still)+" ncdestroy_observed="+number(retiredWindow==target);
        if(r.value && (still || ownedWindow || retiredWindow!=target)) return reject("WINDOW_DESTRUCTION_NOT_OBSERVED");
        return r;
    }
    return reject("WINDOW_OPERATION_NOT_ADMITTED");
}
