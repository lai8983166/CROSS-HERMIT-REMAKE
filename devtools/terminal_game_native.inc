// Fixed original GAME startup COM leaves. Inserted after the frozen window bridge.
static_assert(sizeof(GUID)==16 && sizeof(HRESULT)==4 && sizeof(INITCOMMONCONTROLSEX)==8, "original x86 ABI");
static_assert(offsetof(IMediaControlVtbl,Stop)==36, "original MediaControl slot9");
static_assert(offsetof(IMediaEventExVtbl,SetNotifyWindow)==52, "original EventEx slot13");
enum GameKind : U32 { Perf8=1, Loader8=2, AudioPath=3, GraphBuilder=4,
    MediaControl=5, MediaSeeking=6, MediaPosition=7, MediaEventEx=8, BasicAudio=9 };
struct GameGuid { U32 guest; GUID value; };
const GameGuid gameGuids[] = { @@GAME_GUIDS@@ };
struct GameInterface { U32 kinds=0, refs=0, group=0; };
struct GameGroup {
    U32 kind=0, refs=0, queries=0, notifyOwner=0;
    bool audioNeedsClose=false, audioInitialized=false, stopCalled=false;
};
bool gameGate=false, gameBusy=false;
U32 gameComBalance=0, gameCoInitCalls=0, gameControlsCalls=0, gameNextGroup=0;
U32 gamePerfCreates=0, gameLoaderCreates=0, gameGraphCreates=0;
std::map<U32,GameInterface> gameInterfaces;
std::map<U32,GameGroup> gameGroups;

U32 gameBit(U32 kind) { return 1u << kind; }
const GUID *gameGuid(U32 guest) {
    for(const auto &g:gameGuids) if(g.guest==guest) return &g.value;
    return nullptr;
}
bool gameOp(const std::string &op) {
    static const char *const ops[]={"GAME_GATE","CoInitialize","CoUninitialize","InitCommonControlsEx",
        "CoCreateInstance","COM_QUERY","COM_RELEASE","COM_INFO","DM_INIT_AUDIO","DM_GET_DEFAULT_AUDIO_PATH",
        "DM_LOADER_SEARCH","DM_SET_VOLUME","DM_STOP","DM_CLOSE_DOWN","DS_SET_NOTIFY","DS_STOP","MultiByteToWideChar"};
    for(const char *name:ops) if(op==name) return true;
    return false;
}
bool gameEmpty() { return !gameComBalance && gameInterfaces.empty() && gameGroups.empty() && !gameBusy; }
std::string gameStatus() {
    U32 refs=0,audio=0,pending=0,notifications=0;
    for(const auto &p:gameInterfaces) refs+=p.second.refs;
    for(const auto &p:gameGroups) { audio+=p.second.audioInitialized; pending+=p.second.audioNeedsClose; notifications+=p.second.notifyOwner!=0; }
    return "game_gate="+number(gameGate)+" com_balance="+number(gameComBalance)+
        " com_interfaces="+number(static_cast<U32>(gameInterfaces.size()))+" com_refs="+number(refs)+
        " com_groups="+number(static_cast<U32>(gameGroups.size()))+" audio_initialized="+number(audio)+
        " audio_pending_close="+number(pending)+" graph_notifications="+number(notifications)+
        " game_call_active="+number(gameBusy)+" common_controls_calls="+number(gameControlsCalls);
}
// COM may pump synchronous messages. Preserve the same parent-request and MAIN
// callback bridge while releasing stateMutex. Other-lane writes are refused by
// the dispatch guard during this interval; callback leaves remain the old list.
struct GameCallScope {
    std::unique_lock<std::mutex> &guard; U32 previous;
    GameCallScope(std::unique_lock<std::mutex> &g,U32 request):guard(g),previous(windowParentRequest) {
        if(gameBusy) fatal(108);
        gameBusy=true; windowParentRequest=request; guard.unlock();
    }
    ~GameCallScope() { guard.lock(); windowParentRequest=previous; gameBusy=false; }
};
U32 gameMethod(U32 object,U32 slot) { return static_cast<U32 **>(pointer(object))[0][slot]; }
bool gameHas(U32 object,U32 kind) {
    auto i=gameInterfaces.find(object);
    return i!=gameInterfaces.end() && i->second.refs && (i->second.kinds&gameBit(kind));
}
bool gameOutput(U32 output) {
    return !(output&3) && windowRange(output,4) && *static_cast<U32 *>(pointer(output))==0;
}
U32 gameFirstKind(U32 mask) { for(U32 k=1;k<=9;++k) if(mask&gameBit(k)) return k; return 0; }
std::string gameInfo(U32 object,U32 kind) {
    const auto &owned=gameInterfaces.at(object); const U32 mask=owned.kinds;
    std::string result="object="+number(object)+" kind="+number(kind)+" kind_mask="+number(mask)+
        " vtable="+number(*static_cast<U32 *>(pointer(object)))+" method0="+number(gameMethod(object,0))+
        " method2="+number(gameMethod(object,2))+" owned_refs="+number(owned.refs)+" group="+number(owned.group);
    if(mask&gameBit(Perf8)) for(U32 slot:{5u,34u,38u,44u,51u}) result+=" method"+number(slot)+"="+number(gameMethod(object,slot));
    else if(mask&gameBit(Loader8)) result+=" method5="+number(gameMethod(object,5));
    if(mask&gameBit(MediaControl)) result+=" method9="+number(gameMethod(object,9));
    if(mask&gameBit(MediaEventEx)) result+=" method13="+number(gameMethod(object,13));
    return result;
}
void gameOwn(U32 object,U32 kind,U32 group) {
    auto found=gameInterfaces.find(object);
    if(!object || (found!=gameInterfaces.end() && found->second.group!=group)) fatal(109);
    if(found==gameInterfaces.end()) found=gameInterfaces.emplace(object,GameInterface{0,0,group}).first;
    found->second.kinds|=gameBit(kind); ++found->second.refs; ++gameGroups.at(group).refs;
}
U32 gameQueryKind(U32 iid) {
    switch(iid) { case 0x5cef3c:return MediaControl; case 0x5ce8dc:return MediaSeeking;
        case 0x5cef0c:return MediaPosition; case 0x5cef1c:return MediaEventEx; case 0x5ceefc:return BasicAudio; default:return 0; }
}
Result gameDispatch(const Request &q,std::unique_lock<std::mutex> &guard,U32 savedError) {
    Result r; r.error=savedError; std::vector<U32> a;
    const auto args=[&](size_t n) { return numeric(q,n,a); };
    const auto begin=[&]() { SetLastError(savedError); };
    const auto capture=[&]() { r.error=GetLastError(); };
    if(q.lane || GetCurrentThreadId()!=lanes[0].tid || __readfsdword(0x18)!=lanes[0].teb || !windowCallbacks.empty())
        return reject("GAME_MAIN_OUTSIDE_CALLBACK_ONLY");
    if(q.op=="GAME_GATE") {
        if(!args(1) || a[0]>1 || !gameEmpty() || (a[0] && (!windowGate || !ownedWindow))) return reject("GAME_GATE_QUIESCENT_OWNED_WINDOW");
        gameGate=a[0]!=0; r.value=1; r.extras="infrastructure=1 "+gameStatus(); return r;
    }
    if(!gameGate) return reject("GAME_GATE_CLOSED",ERROR_ACCESS_DENIED);
    if(q.op=="CoInitialize") {
        if(!args(1) || a[0] || gameCoInitCalls) return reject("ORIGINAL_COINITIALIZE_NULL_ONCE");
        ++gameCoInitCalls;
        { GameCallScope call(guard,q.id); begin(); r.value=static_cast<U32>(CoInitialize(nullptr)); capture(); }
        if(static_cast<LONG>(r.value)>=0) ++gameComBalance;
        r.extras="com_balance="+number(gameComBalance)+" native_return_type=HRESULT"; return r;
    }
    if(q.op=="CoUninitialize") {
        if(!args(0) || gameComBalance!=1 || !gameInterfaces.empty() || !gameGroups.empty()) return reject("COM_REFERENCES_MUST_BE_RELEASED");
        { GameCallScope call(guard,q.id); begin(); CoUninitialize(); capture(); }
        --gameComBalance; r.extras="void=1 com_balance=0"; return r;
    }
    if(!gameComBalance) return reject("CURRENT_MAIN_COM_APARTMENT_REQUIRED");
    if(q.op=="InitCommonControlsEx") {
        if(!args(1) || !windowRange(a[0],8) || gameControlsCalls) return reject("OWNED_COMMON_CONTROLS8_ONCE");
        const auto *ic=static_cast<INITCOMMONCONTROLSEX *>(pointer(a[0]));
        if(ic->dwSize!=8 || ic->dwICC!=0x800) return reject("ORIGINAL_COMMON_CONTROLS_USEREX");
        ++gameControlsCalls;
        { GameCallScope call(guard,q.id); begin(); r.value=InitCommonControlsEx(ic); capture(); }
        r.extras="structure_hex="+encodeHex(ic,8)+" process_registration_no_owned_handle=1"; return r;
    }
    if(q.op=="MultiByteToWideChar") {
        if(!args(6) || a[0] || a[1] || a[3]!=UINT32_MAX || a[5]!=260 || !windowRange(a[4],520)) return reject("ORIGINAL_MULTIBYTE_TO_WIDE_ARGS");
        U32 n=0; for(;n<260;++n) { if(!windowRange(a[2]+n,1)) return reject("BOUNDED_ANSI_INPUT"); if(!*static_cast<char *>(pointer(a[2]+n))) break; }
        if(n==260 || (static_cast<uint64_t>(a[2])<static_cast<uint64_t>(a[4])+520 && static_cast<uint64_t>(a[4])<static_cast<uint64_t>(a[2])+n+1)) return reject("STRING_OVERLAP_OR_UNTERMINATED");
        begin(); r.value=MultiByteToWideChar(0,0,static_cast<LPCCH>(pointer(a[2])),-1,static_cast<LPWSTR>(pointer(a[4])),260); capture(); return r;
    }
    if(q.op=="CoCreateInstance") {
        if(!args(5) || a[1] || a[2]!=3 || !gameOutput(a[4]) || gameInterfaces.size()>=24) return reject("ORIGINAL_COM_CREATE_ARGUMENTS");
        U32 kind=0;
        if(a[0]==0x5cb3ec && a[3]==0x5caf0c && !gamePerfCreates) { kind=Perf8; ++gamePerfCreates; }
        else if(a[0]==0x5cb37c && a[3]==0x5caf1c && !gameLoaderCreates) { kind=Loader8; ++gameLoaderCreates; }
        else if(a[0]==0x5cfd7c && a[3]==0x5ce80c && gameGraphCreates<2) { kind=GraphBuilder; ++gameGraphCreates; }
        else return reject("FIXED_ORIGINAL_CLSID_IID_PAIR_ONLY");
        const GUID *cls=gameGuid(a[0]),*iid=gameGuid(a[3]);
        { GameCallScope call(guard,q.id); begin(); r.value=static_cast<U32>(CoCreateInstance(*cls,nullptr,3,*iid,static_cast<void **>(pointer(a[4])))); capture(); }
        const U32 object=*static_cast<U32 *>(pointer(a[4]));
        if(static_cast<LONG>(r.value)>=0) {
            if(!object) fatal(110);
            const U32 group=++gameNextGroup; gameGroups.emplace(group,GameGroup{kind}); gameOwn(object,kind,group); r.extras=gameInfo(object,kind);
        } else { if(object) fatal(111); r.extras="object=0 kind="+number(kind); }
        r.extras+=" clsid_guest="+number(a[0])+" iid_guest="+number(a[3])+" output="+number(a[4])+" native_return_type=HRESULT"; return r;
    }
    if(q.op=="COM_QUERY") {
        if(!args(3) || !gameHas(a[0],GraphBuilder) || !gameOutput(a[2])) return reject("OWNED_GRAPH_QUERY_ONLY");
        U32 kind=gameQueryKind(a[1]); auto &group=gameGroups.at(gameInterfaces.at(a[0]).group);
        if(!kind || group.queries&gameBit(kind) || gameInterfaces.size()>=24) return reject("ONE_FIXED_GRAPH_INTERFACE_QUERY");
        group.queries|=gameBit(kind); const GUID *iid=gameGuid(a[1]);
        using Fn=HRESULT (STDMETHODCALLTYPE *)(void *,const GUID &,void **);
        const auto fn=reinterpret_cast<Fn>(gameMethod(a[0],0));
        { GameCallScope call(guard,q.id); begin(); r.value=static_cast<U32>(fn(pointer(a[0]),*iid,static_cast<void **>(pointer(a[2])))); capture(); }
        const U32 object=*static_cast<U32 *>(pointer(a[2]));
        if(static_cast<LONG>(r.value)>=0) { if(!object) fatal(112); gameOwn(object,kind,gameInterfaces.at(a[0]).group); r.extras=gameInfo(object,kind); }
        else { if(object) fatal(113); r.extras="object=0 kind="+number(kind); }
        r.extras+=" iid_guest="+number(a[1])+" output="+number(a[2])+" method="+number(ptr(reinterpret_cast<void *>(fn))); return r;
    }
    if(q.op=="COM_INFO") {
        if(!args(1) || !gameInterfaces.count(a[0])) return reject("OWNED_COM_REFERENCE_REQUIRED");
        r.value=a[0]; r.extras="infrastructure=1 "+gameInfo(a[0],gameFirstKind(gameInterfaces.at(a[0]).kinds)); return r;
    }
    if(q.op=="COM_RELEASE") {
        if(!args(1) || !gameInterfaces.count(a[0])) return reject("OWNED_COM_REFERENCE_REQUIRED");
        auto &owned=gameInterfaces.at(a[0]); auto &group=gameGroups.at(owned.group);
        if((owned.kinds&gameBit(Perf8) && group.audioNeedsClose) || (owned.kinds&gameBit(MediaEventEx) && group.notifyOwner)) return reject("COM_EXPLICIT_DEVICE_CLEANUP_REQUIRED");
        using Fn=ULONG (STDMETHODCALLTYPE *)(void *); const auto fn=reinterpret_cast<Fn>(gameMethod(a[0],2));
        const U32 groupId=owned.group;
        { GameCallScope call(guard,q.id); begin(); r.value=fn(pointer(a[0])); capture(); }
        --owned.refs; --group.refs; const U32 remaining=owned.refs;
        if(!r.value && remaining) fatal(114);
        if(!remaining) gameInterfaces.erase(a[0]);
        if(!group.refs) gameGroups.erase(groupId);
        r.extras="object="+number(a[0])+" released_owned_ref=1 remaining_owned_refs="+number(remaining)+" native_return_type=ULONG"; return r;
    }
    if(q.op=="DM_INIT_AUDIO") {
        if(!args(8) || !gameHas(a[0],Perf8) || a[1] || a[2] || !ownedWindow || a[3]!=ptr(ownedWindow) || a[4]!=8 || a[5]!=64 || a[6]!=63 || a[7]) return reject("ORIGINAL_INIT_AUDIO8_ARGS");
        auto &group=gameGroups.at(gameInterfaces.at(a[0]).group);
        if(group.audioNeedsClose) return reject("ONE_AUDIO_INIT_ATTEMPT");
        group.audioNeedsClose=true;
        using Fn=HRESULT (STDMETHODCALLTYPE *)(void *,void **,void **,HWND,DWORD,DWORD,DWORD,void *);
        const auto fn=reinterpret_cast<Fn>(gameMethod(a[0],44));
        { GameCallScope call(guard,q.id); begin(); r.value=static_cast<U32>(fn(pointer(a[0]),nullptr,nullptr,ownedWindow,8,64,63,nullptr)); capture(); }
        group.audioInitialized=static_cast<LONG>(r.value)>=0; r.extras="method_slot=44 audio_initialized="+number(group.audioInitialized); return r;
    }
    if(q.op=="DM_GET_DEFAULT_AUDIO_PATH") {
        if(!args(2) || !gameHas(a[0],Perf8) || !gameOutput(a[1])) return reject("OWNED_PERFORMANCE_PATH_OUTPUT");
        auto &group=gameGroups.at(gameInterfaces.at(a[0]).group);
        if(!group.audioInitialized || group.queries&gameBit(AudioPath)) return reject("ONE_INITIALIZED_DEFAULT_PATH");
        group.queries|=gameBit(AudioPath); using Fn=HRESULT (STDMETHODCALLTYPE *)(void *,void **); const auto fn=reinterpret_cast<Fn>(gameMethod(a[0],51));
        { GameCallScope call(guard,q.id); begin(); r.value=static_cast<U32>(fn(pointer(a[0]),static_cast<void **>(pointer(a[1])))); capture(); }
        U32 object=*static_cast<U32 *>(pointer(a[1]));
        if(static_cast<LONG>(r.value)>=0) { if(!object) fatal(115); gameOwn(object,AudioPath,gameInterfaces.at(a[0]).group); r.extras=gameInfo(object,AudioPath); }
        else { if(object) fatal(116); r.extras="object=0 kind=3"; }
        r.extras+=" output="+number(a[1])+" method_slot=51"; return r;
    }
    if(q.op=="DM_LOADER_SEARCH") {
        if(!args(4) || !gameHas(a[0],Loader8) || a[1]!=0x5cb2fc || a[3] || !windowRange(a[2],6) || memcmp(pointer(a[2]),L".\\",6)) return reject("ORIGINAL_LOADER_DOT_DIRECTORY");
        using Fn=HRESULT (STDMETHODCALLTYPE *)(void *,const GUID &,WCHAR *,BOOL); const auto fn=reinterpret_cast<Fn>(gameMethod(a[0],5));
        { GameCallScope call(guard,q.id); begin(); r.value=static_cast<U32>(fn(pointer(a[0]),*gameGuid(a[1]),static_cast<WCHAR *>(pointer(a[2])),FALSE)); capture(); }
        r.extras="method_slot=5 directory_hex="+encodeHex(pointer(a[2]),6); return r;
    }
    if(q.op=="DM_SET_VOLUME") {
        if(!args(4) || !gameHas(a[0],Perf8) || a[1]!=0x5cb08c || a[3]!=4 || !windowRange(a[2],4)) return reject("ORIGINAL_MASTER_VOLUME4");
        const LONG volume=*static_cast<LONG *>(pointer(a[2]));
        if(volume < -20000 || volume > 2000 || !gameGroups.at(gameInterfaces.at(a[0]).group).audioInitialized) return reject("ORIGINAL_VOLUME_CLAMP");
        using Fn=HRESULT (STDMETHODCALLTYPE *)(void *,const GUID &,void *,DWORD); const auto fn=reinterpret_cast<Fn>(gameMethod(a[0],34));
        { GameCallScope call(guard,q.id); begin(); r.value=static_cast<U32>(fn(pointer(a[0]),*gameGuid(a[1]),pointer(a[2]),4)); capture(); }
        r.extras="method_slot=34 volume_bits="+number(static_cast<U32>(volume)); return r;
    }
    if(q.op=="DM_STOP") {
        if(!args(5) || !gameHas(a[0],Perf8) || a[1] || a[2] || a[3] || a[4]) return reject("ORIGINAL_STOP_ALL_ZERO_ARGS");
        using Fn=HRESULT (STDMETHODCALLTYPE *)(void *,void *,void *,LONG,DWORD); const auto fn=reinterpret_cast<Fn>(gameMethod(a[0],5));
        { GameCallScope call(guard,q.id); begin(); r.value=static_cast<U32>(fn(pointer(a[0]),nullptr,nullptr,0,0)); capture(); }
        gameGroups.at(gameInterfaces.at(a[0]).group).stopCalled=true; r.extras="method_slot=5"; return r;
    }
    if(q.op=="DM_CLOSE_DOWN") {
        if(!args(1) || !gameHas(a[0],Perf8) || !gameGroups.at(gameInterfaces.at(a[0]).group).stopCalled) return reject("ORIGINAL_AUDIO_STOP_BEFORE_CLOSE");
        using Fn=HRESULT (STDMETHODCALLTYPE *)(void *); const auto fn=reinterpret_cast<Fn>(gameMethod(a[0],38));
        { GameCallScope call(guard,q.id); begin(); r.value=static_cast<U32>(fn(pointer(a[0]))); capture(); }
        auto &group=gameGroups.at(gameInterfaces.at(a[0]).group);
        if(static_cast<LONG>(r.value)>=0) { group.audioNeedsClose=false; group.audioInitialized=false; }
        r.extras="method_slot=38 audio_pending_close="+number(group.audioNeedsClose); return r;
    }
    if(q.op=="DS_SET_NOTIFY") {
        if(!args(4) || !gameHas(a[0],MediaEventEx)) return reject("OWNED_MEDIA_EVENT_INTERFACE");
        auto &group=gameGroups.at(gameInterfaces.at(a[0]).group);
        const bool clear=!a[1] && !a[2] && !a[3];
        if(!clear && (!ownedWindow || a[1]!=ptr(ownedWindow) || a[2]!=0x464 || a[3]<0x10000 || group.notifyOwner)) return reject("ORIGINAL_OWNED_NOTIFY_WINDOW");
        using Fn=HRESULT (STDMETHODCALLTYPE *)(void *,LONG_PTR,LONG,LONG_PTR); const auto fn=reinterpret_cast<Fn>(gameMethod(a[0],13));
        { GameCallScope call(guard,q.id); begin(); r.value=static_cast<U32>(fn(pointer(a[0]),a[1],a[2],a[3])); capture(); }
        if(static_cast<LONG>(r.value)>=0) group.notifyOwner=a[3];
        r.extras="method_slot=13 opaque_guest_owner="+number(a[3])+" notification_active="+number(group.notifyOwner!=0); return r;
    }
    if(q.op=="DS_STOP") {
        if(!args(1) || !gameHas(a[0],MediaControl)) return reject("OWNED_MEDIA_CONTROL_INTERFACE");
        using Fn=HRESULT (STDMETHODCALLTYPE *)(void *); const auto fn=reinterpret_cast<Fn>(gameMethod(a[0],9));
        { GameCallScope call(guard,q.id); begin(); r.value=static_cast<U32>(fn(pointer(a[0]))); capture(); }
        gameGroups.at(gameInterfaces.at(a[0]).group).stopCalled=true; r.extras="method_slot=9"; return r;
    }
    return reject("GAME_OPERATION_NOT_ADMITTED");
}
