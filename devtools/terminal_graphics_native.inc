// Fixed D3D8/startup font ABI. No arbitrary slots, native addresses or desktop pixels.
enum GfxKind : U32 { GfxFactory=10,GfxDevice=11,GfxSurface=12,GfxTexture=13,GfxVertex=14 };
struct GfxObject { U32 kind=0,refs=0,parent=0,width=0,height=0,format=0,pitch=0,bits=0; bool locked=false; };
struct GfxDC { U32 bitmap=0,font=0,oldBitmap=0,oldFont=0; };
struct GfxBitmap { U32 bits=0,bytes=0; bool deleteIssued=false; };
std::map<U32,GfxObject> gfxObjects;
std::map<U32,GfxDC> gfxDCs;
std::map<U32,GfxBitmap> gfxBitmaps;
std::map<U32,bool> gfxFonts;
std::map<U32,U32> gfxBlocks;
std::vector<std::array<U32,4>> gfxModes;
bool gfxGate=false,gfxBaseline=false,gfxRecording=false,gfxGammaSaved=false,gfxGammaDirty=false,gfxResidual=false;
HMODULE gfxModule=nullptr;
std::vector<HMODULE> gfxExtraModules;
std::map<U32,bool> gfxKnownModules;
std::map<U32,U32> gfxDebugProcs;
std::map<U32,U32> gfxMuteStates;
std::map<U32,U32> gfxMuteCounts;
U32 gfxModuleLoads=0;
U32 gfxFactory=0,gfxDevice=0,gfxAttempts=0,gfxModeCount=0,gfxMute=0,gfxMuteCalls=0,gfxAtlasCreates=0,gfxVBcreates=0;
U32 gfxFontStep=0,gfxBoundTexture=0,gfxCalls=0;
std::array<unsigned char,32> gfxBaselineToken{};
std::array<unsigned char,1536> gfxOriginalGamma{};
static_assert(sizeof(BITMAPINFOHEADER)==40 && sizeof(LOGFONTA)==60 && sizeof(SIZE)==8,"original GDI x86 ABI");
constexpr bool gfxMuteAllowed(U32 previous,U32 value,U32 moduleCalls,U32 totalCalls) {
 return value<=1&&value!=previous&&moduleCalls<4&&totalCalls<8;
}
constexpr bool gfxTwoModuleMutePlan() {
 U32 states[2]={0,0},counts[2]={0,0},total=0;
 const U32 modules[]={0,1,0,1,0,1,0,1},values[]={1,1,0,0,1,1,0,0};
 for(U32 i=0;i<8;++i){U32 m=modules[i];if(!gfxMuteAllowed(states[m],values[i],counts[m],total))return false;states[m]=values[i];++counts[m];++total;}
 return !states[0]&&!states[1]&&counts[0]==4&&counts[1]==4&&!gfxMuteAllowed(states[0],1,counts[0],total);
}
static_assert(gfxTwoModuleMutePlan(),"both original DLLs accept two independent mute pairs");
static_assert(!gfxMuteAllowed(0,1,4,4),"third pair rejected even with only one DLL");
static_assert(!gfxMuteAllowed(1,1,1,1)&&!gfxMuteAllowed(0,0,0,0)&&!gfxMuteAllowed(0,2,0,0),"each DLL requires alternating BOOL transitions");
bool gfxHas(U32 obj,U32 kind) { auto p=gfxObjects.find(obj);return p!=gfxObjects.end()&&p->second.refs&&p->second.kind==kind; }
bool gfxResourcesEmpty() { return gfxObjects.empty()&&gfxDCs.empty()&&gfxBitmaps.empty()&&gfxFonts.empty()&&gfxBlocks.empty()&&!gfxRecording&&!gfxGammaDirty&&!gfxMute&&!gfxResidual; }
bool gfxEmpty() { return gfxResourcesEmpty()&&!gfxModule&&gfxExtraModules.empty()&&!gfxBaseline; }
bool gfxOutput(U32 p) { return !(p&3)&&windowRange(p,4); }
bool gfxDisjoint(U32 a,U32 an,U32 b,U32 bn) { return static_cast<uint64_t>(a)+an<=b||static_cast<uint64_t>(b)+bn<=a; }
constexpr bool gfxSpanFits(U32 offset,U32 size,U32 total) { return size&&size<=32768&&static_cast<uint64_t>(offset)+size<=total; }
constexpr bool gfxFullscreenPP(const std::array<U32,13> &p,U32 hwnd) {
 return p[0]==1024&&p[1]==768&&p[3]==1&&!p[4]&&p[5]==1&&p[6]==hwnd&&!p[7]&&!p[8]&&!p[9]&&!p[10]&&!p[11]&&!p[12];
}
static_assert(gfxFullscreenPP({1024,768,25,1,0,1,123,0,0,0,0,0,0},123),"original fullscreen shape");
static_assert(!gfxFullscreenPP({1024,768,25,1,0,1,123,1,0,0,0,0,0},123),"windowed substitution refused");
static_assert(!gfxFullscreenPP({1024,768,25,1,0,1,124,0,0,0,0,0,0},123),"foreign HWND refused");
static_assert(gfxSpanFits(32768,32768,131072)&&!gfxSpanFits(UINT32_MAX,32768,131072)&&!gfxSpanFits(0,32769,131072),"locked transfers bounded without wrap");
std::string gfxStatus() {
 U32 refs=0,locks=0;for(const auto &p:gfxObjects){refs+=p.second.refs;locks+=p.second.locked;}
 return "gfx_gate="+number(gfxGate)+" gfx_baseline="+number(gfxBaseline)+" gfx_modules="+number(static_cast<U32>(gfxExtraModules.size())+(gfxModule!=nullptr))+
  " gfx_interfaces="+number(static_cast<U32>(gfxObjects.size()))+" gfx_refs="+number(refs)+" gfx_locks="+number(locks)+
  " gfx_blocks="+number(static_cast<U32>(gfxBlocks.size()))+" gfx_recording="+number(gfxRecording)+" gfx_gamma_dirty="+number(gfxGammaDirty)+
  " gfx_dcs="+number(static_cast<U32>(gfxDCs.size()))+" gfx_bitmaps="+number(static_cast<U32>(gfxBitmaps.size()))+
  " gfx_fonts="+number(static_cast<U32>(gfxFonts.size()))+" gfx_mute="+number(gfxMute)+" gfx_unresolved_refs="+number(gfxResidual);
}
std::string gfxInfo(U32 obj) {
 const auto &p=gfxObjects.at(obj);std::string s="object="+number(obj)+" kind="+number(p.kind)+" kind_mask="+number(1u<<p.kind)+
  " vtable="+number(*static_cast<U32 *>(pointer(obj)))+" owned_refs="+number(p.refs)+" group="+number(p.parent)+" method1="+number(gameMethod(obj,1))+" method2="+number(gameMethod(obj,2));
 std::vector<U32> slots;
 if(p.kind==GfxFactory)slots={6,7,8,10,15};
 if(p.kind==GfxDevice)slots={6,7,8,9,16,18,19,20,23,40,50,51,52,53,56,61,63};
 if(p.kind==GfxSurface)slots={8};
 if(p.kind==GfxTexture)slots={14,15,16,17};
 if(p.kind==GfxVertex)slots={13};
 for(U32 n:slots)s+=" method"+number(n)+"="+number(gameMethod(obj,n));return s;
}
void gfxOwn(U32 obj,U32 kind,U32 owner=0) {
 if(!obj)fatal(120);auto p=gfxObjects.find(obj);
 if(p!=gfxObjects.end()){if(p->second.kind!=kind||p->second.parent!=owner)fatal(121);++p->second.refs;}
 else gfxObjects.emplace(obj,GfxObject{kind,1,owner});
}
void gfxOutputResult(Result &r,U32 output,U32 kind,U32 owner=0) {
 U32 obj=*static_cast<U32 *>(pointer(output));
 if(static_cast<LONG>(r.value)>=0){gfxOwn(obj,kind,owner);r.extras=gfxInfo(obj);}
 else {r.extras="object="+number(obj)+" kind="+number(kind)+" output_interface_owned=0";}
 r.extras+=" output="+number(output);
}
bool gfxAllowedFormat(U32 value) {
 static const U32 values[]={20,21,22,23,24,40,41,25,26,27,28,29,30,31,34,50,51,52,60,61,62,63,64,65,67,1498831189,844715353,827611204,844388420,861165636,877942852,894720068,70,71,73,75,80,77,79,909200416,909200449,909201952,909201985};
 return std::find(std::begin(values),std::end(values),value)!=std::end(values);
}
struct GfxStep { U32 op,a,b,c; };
const GfxStep gfxFontPlan[]={ {0,0,0,0},{1,0,0,0},{2,27,1,0},{2,19,5,0},{2,20,6,0},{2,15,1,0},{2,24,8,0},{2,25,5,0},{2,8,3,0},{2,52,0,0},{2,136,1,0},{2,40,0,0},{2,152,0,0},{2,151,0,0},{2,167,0,0},{2,28,0,0},
 {3,0,1,4},{3,0,2,2},{3,0,3,0},{3,0,4,4},{3,0,5,2},{3,0,6,0},{3,0,17,1},{3,0,16,1},{3,0,18,0},{3,0,11,0},{3,0,24,0},{3,1,1,1},{3,1,4,1},{4,0,0,0} };
static_assert(sizeof(gfxFontPlan)/sizeof(gfxFontPlan[0])==30,"two state blocks per font");
// The ABI declares void; this x86 forwarding routine captures actual target EAX.
U32 gfxVoidGamma(U32 method,U32 object,U32 flags,const void *data) {
 U32 value;
 __asm {
  push data
  push flags
  push object
  call method
  mov value,eax
 }
 return value;
}
U32 gfxVoidMute(U32 method,U32 value) {
 U32 observed;
 __asm {
  push value
  call method
  add esp,4
  mov observed,eax
 }
 return observed;
}
U32 gfxReadGamma(U32 device,void *output) {
 U32 method=gameMethod(device,19),observed;
 __asm {
  push output
  push device
  call method
  mov observed,eax
 }
 return observed;
}
std::string gfxSweepGDI() {
 std::vector<U32> bitmaps,deletedFonts;BOOL flushed=GdiFlush();
 if(!flushed)return "retirement_flush=0 retired_bitmaps_hex=- retired_fonts_hex=-";
 unsigned char probe[60]{};
 for(auto i=gfxBitmaps.begin();i!=gfxBitmaps.end();) {
  if(i->second.deleteIssued && GetObjectType(handle(i->first))==0 && GetObjectA(handle(i->first),60,probe)==0){bitmaps.push_back(i->first);i=gfxBitmaps.erase(i);}else ++i;
 }
 for(auto i=gfxFonts.begin();i!=gfxFonts.end();) {
  if(i->second && GetObjectType(handle(i->first))==0 && GetObjectA(handle(i->first),60,probe)==0){fonts.erase(i->first);retiredFonts[i->first]=true;deletedFonts.push_back(i->first);i=gfxFonts.erase(i);}else ++i;
 }
 return "retirement_flush=1 retired_bitmaps_hex="+(bitmaps.empty()?std::string("-"):encodeHex(bitmaps.data(),static_cast<U32>(bitmaps.size()*4)))+
  " retired_fonts_hex="+(deletedFonts.empty()?std::string("-"):encodeHex(deletedFonts.data(),static_cast<U32>(deletedFonts.size()*4)));
}
bool gfxOp(const std::string &op) { return op.size()>4&&op.compare(0,4,"GFX_")==0; }
Result gfxDispatch(const Request &q,std::unique_lock<std::mutex> &guard,U32 savedError) {
 Result r;r.error=savedError;std::vector<U32>a;const auto args=[&](size_t n){return numeric(q,n,a);};
 const auto begin=[&](){SetLastError(savedError);};const auto capture=[&](){r.error=GetLastError();};
 if(q.lane || GetCurrentThreadId()!=lanes[0].tid || __readfsdword(0x18)!=lanes[0].teb || !windowCallbacks.empty())return reject("GFX_CURRENT_MAIN_OUTSIDE_CALLBACK");
 if(++gfxCalls>16000)return reject("GFX_BOUNDED_STARTUP_REQUESTS");
 if(q.op=="GFX_GATE"){
  if(!args(1)||a[0]>1||!gfxEmpty()||(a[0]&&(!gameGate||!ownedWindow)))return reject("GFX_GATE_EMPTY_CURRENT_WINDOW");
  gfxGate=a[0]!=0;r.value=1;r.extras=gfxStatus();return r;
 }
 if(!gfxGate)return reject("GFX_GATE_CLOSED",ERROR_ACCESS_DENIED);
 if(q.op=="GFX_BASELINE"){
  if(!args(1)||gfxBaseline||gfxModule||!windowRange(a[0],32))return reject("ONE_REGISTERED_RECOVERY_BASELINE");
  const auto *p=static_cast<unsigned char *>(pointer(a[0]));if(std::all_of(p,p+32,[](unsigned char c){return c==0;}))return reject("NONZERO_BASELINE_TOKEN");
  memcpy(gfxBaselineToken.data(),p,32);gfxBaseline=true;r.value=1;r.extras="baseline_token_hex="+encodeHex(p,32)+" pid="+number(GetCurrentProcessId())+" hwnd="+number(ptr(ownedWindow))+" registration_only=1";return r;
 }
 if(q.op=="GFX_BASELINE_CLEAR"){
  if(!args(0)||!gfxBaseline||!gfxResourcesEmpty()||gfxModule||!gfxExtraModules.empty())return reject("GFX_CLEAR_AFTER_ALL_RESOURCES");gfxBaseline=false;gfxBaselineToken.fill(0);r.value=1;return r;
 }
 if(!gfxBaseline)return reject("GFX_RECOVERY_BASELINE_REQUIRED");
 if(q.op=="GFX_FACTORY"){
  if(!args(1)||a[0]!=220||gfxModule||gfxFactory)return reject("ONE_D3D8_FACTORY_SDK220");
  {GameCallScope c(guard,q.id);begin();gfxModule=LoadLibraryExW(L"d3d8.dll",nullptr,LOAD_LIBRARY_SEARCH_SYSTEM32);capture();}
  if(!gfxModule){r.value=0;r.extras="object=0 kind=10 module=0";return r;}
  gfxKnownModules[ptr(gfxModule)]=true;FARPROC symbol=GetProcAddress(gfxModule,"Direct3DCreate8");if(!symbol)return reject("D3D8_FACTORY_EXPORT_MISSING");
  using F=void *(WINAPI *)(UINT);
  {GameCallScope c(guard,q.id);begin();r.value=ptr(reinterpret_cast<F>(symbol)(220));capture();}
  if(r.value){gfxFactory=r.value;gfxOwn(r.value,GfxFactory);r.extras=gfxInfo(r.value);}else r.extras="object=0 kind=10";
  wchar_t path[520]{};DWORD n=GetModuleFileNameW(gfxModule,path,520);if(!n||n>=520)fatal(123);
  r.extras+=" module="+number(ptr(gfxModule))+" export="+number(ptr(reinterpret_cast<void *>(symbol)))+" runtime_path_hex="+encodeHex(path,(n+1)*2);return r;
 }
 if(q.op=="GFX_RUNTIME_CLOSE"){
  if(!args(0)||!gfxModule||!gfxResourcesEmpty())return reject("GFX_RUNTIME_REFERENCES_LIVE");
  std::vector<U32> closes;{GameCallScope c(guard,q.id);begin();
   while(!gfxExtraModules.empty()){BOOL closed=FreeLibrary(gfxExtraModules.back());closes.push_back(static_cast<U32>(closed));if(!closed)break;gfxExtraModules.pop_back();}
   r.value=gfxExtraModules.empty()?FreeLibrary(gfxModule):0;capture();}
  if(r.value){gfxModule=nullptr;gfxKnownModules.clear();gfxDebugProcs.clear();gfxMuteStates.clear();gfxMuteCounts.clear();}
  r.extras="extra_close_results_hex="+(closes.empty()?std::string("-"):encodeHex(closes.data(),static_cast<U32>(closes.size()*4)))+" remaining_load_refs="+number(static_cast<U32>(gfxExtraModules.size())+(gfxModule!=nullptr));return r;
 }
 if(q.op=="GFX_MODULE_GET"||q.op=="GFX_MODULE_LOAD"){
  if(!args(1)||!gfxModule)return reject("D3D8_FACTORY_MODULE_REQUIRED");bool normal=windowString(a[0],"d3d8.dll"),debug=windowString(a[0],"d3d8d.dll");
  if(!normal&&!debug)return reject("TWO_ORIGINAL_D3D_MODULE_NAMES_ONLY");bool load=q.op=="GFX_MODULE_LOAD";if(load&&++gfxModuleLoads>4)return reject("BOUNDED_D3D_LOAD_ATTEMPTS");
  HMODULE module=nullptr;{GameCallScope c(guard,q.id);begin();module=load?LoadLibraryExW(normal?L"d3d8.dll":L"d3d8d.dll",nullptr,LOAD_LIBRARY_SEARCH_SYSTEM32):GetModuleHandleA(normal?"d3d8.dll":"d3d8d.dll");r.value=ptr(module);capture();}
  if(module){gfxKnownModules[r.value]=true;if(load)gfxExtraModules.push_back(module);}
  r.extras="module="+number(r.value)+" acquired_reference="+number(load&&module!=nullptr)+" system32_load="+number(load);return r;
 }
 if(q.op=="GFX_PROC"){
  if(!args(2)||!gfxKnownModules.count(a[0])||!windowString(a[1],"DebugSetMute"))return reject("AUTHENTICATED_D3D_DEBUG_EXPORT_ONLY");
  FARPROC f=nullptr;{GameCallScope c(guard,q.id);begin();f=GetProcAddress(static_cast<HMODULE>(handle(a[0])),"DebugSetMute");r.value=ptr(reinterpret_cast<void *>(f));capture();}
  if(f)gfxDebugProcs[a[0]]=r.value;r.extras="module="+number(a[0])+" export="+number(r.value);return r;
 }
 if(q.op=="GFX_INFO") {if(!args(1)||!gfxObjects.count(a[0]))return reject("OWNED_GFX_INTERFACE");r.value=a[0];r.extras=gfxInfo(a[0]);return r;}
 if(q.op=="GFX_ADDREF"||q.op=="GFX_RELEASE"){
  if(!args(1)||!gfxObjects.count(a[0]))return reject("OWNED_GFX_REFERENCE");auto &p=gfxObjects.at(a[0]);bool add=q.op=="GFX_ADDREF";
  if(add&&(p.kind!=GfxDevice||p.refs>=8))return reject("BOUNDED_DEVICE_REFERENCE");
  if(!add&&(p.locked||(p.kind==GfxDevice&&p.refs==1&&(gfxObjects.size()!=2||!gfxBlocks.empty()||gfxRecording||gfxGammaDirty||gfxBoundTexture))||
     (p.kind==GfxFactory&&p.refs==1&&gfxDevice)))return reject("GFX_EXPLICIT_CHILD_GAMMA_CLEANUP_REQUIRED");
  using F=ULONG (STDMETHODCALLTYPE *)(void *);auto fn=reinterpret_cast<F>(gameMethod(a[0],add?1:2));
  {GameCallScope c(guard,q.id);begin();r.value=fn(pointer(a[0]));capture();}
  if(add)++p.refs;else --p.refs;U32 refs=p.refs,kind=p.kind,owner=p.parent;
  if(!add&&!r.value&&refs)fatal(124);
  if(!refs){if((p.kind==GfxDevice||p.kind==GfxFactory)&&r.value)gfxResidual=true;if(a[0]==gfxDevice){gfxDevice=0;gfxGammaSaved=false;}if(a[0]==gfxFactory)gfxFactory=0;gfxObjects.erase(a[0]);}
  r.extras="object="+number(a[0])+" kind="+number(kind)+" group="+number(owner)+" remaining_owned_refs="+number(refs)+" owned_refs="+number(refs)+" released_owned_ref="+number(!add)+" native_return_type=ULONG";return r;
 }
 if(q.op=="GFX_MODE_COUNT"){
  if(!args(2)||!gfxHas(a[0],GfxFactory)||a[1])return reject("ADAPTER0_MODE_COUNT");using F=UINT(STDMETHODCALLTYPE *)(void *,UINT);
  {GameCallScope c(guard,q.id);begin();r.value=reinterpret_cast<F>(gameMethod(a[0],6))(pointer(a[0]),0);capture();}gfxModeCount=r.value;
  if(gfxModeCount>4096)return reject("MODE_ENUMERATION_BUDGET");return r;
 }
 if(q.op=="GFX_ENUM_MODE"||q.op=="GFX_DISPLAY_MODE"){
  bool enumerate=q.op=="GFX_ENUM_MODE";if(!args(enumerate?4:3)||!gfxHas(a[0],GfxFactory)||a[1]||!windowRange(a.back(),16)||
     (enumerate&&(a[2]>=gfxModeCount||gfxModes.size()>=4096)))return reject("OWNED_BOUNDED_ADAPTER_MODE");
  if(enumerate){using F=HRESULT(STDMETHODCALLTYPE *)(void *,UINT,UINT,void *);GameCallScope c(guard,q.id);begin();r.value=static_cast<U32>(reinterpret_cast<F>(gameMethod(a[0],7))(pointer(a[0]),0,a[2],pointer(a[3])));capture();}
  else {using F=HRESULT(STDMETHODCALLTYPE *)(void *,UINT,void *);GameCallScope c(guard,q.id);begin();r.value=static_cast<U32>(reinterpret_cast<F>(gameMethod(a[0],8))(pointer(a[0]),0,pointer(a[2])));capture();}
  if(enumerate&&static_cast<LONG>(r.value)>=0){std::array<U32,4> mode{};memcpy(mode.data(),pointer(a[3]),16);if(std::find(gfxModes.begin(),gfxModes.end(),mode)==gfxModes.end())gfxModes.push_back(mode);}return r;
 }
 if(q.op=="GFX_CREATE_DEVICE"){
  if(!args(7)||!gfxHas(a[0],GfxFactory)||a[1]||a[3]!=ptr(ownedWindow)||!ownedWindow||gfxDevice||gfxAttempts>=4||!windowRange(a[5],52)||!gfxOutput(a[6])||!gfxDisjoint(a[5],52,a[6],4))return reject("OWNED_FULLSCREEN_DEVICE_INPUT");
  static const U32 types[]={1,1,2,2},flags[]={68,36,68,36};if(a[2]!=types[gfxAttempts]||a[4]!=flags[gfxAttempts])return reject("ORIGINAL_DEVICE_FALLBACK_ORDER");
  U32 *pp=static_cast<U32 *>(pointer(a[5]));bool known=false;for(const auto &m:gfxModes)if(m[0]==pp[0]&&m[1]==pp[1]&&m[3]==pp[2])known=true;
  std::array<U32,13> presentation{};memcpy(presentation.data(),pp,52);
  if(!known||!gfxFullscreenPP(presentation,ptr(ownedWindow)))return reject("EXACT_ORIGINAL_FULLSCREEN_PP52");
  ++gfxAttempts;using F=HRESULT(STDMETHODCALLTYPE *)(void *,UINT,U32,HWND,DWORD,void *,void **);
  {GameCallScope c(guard,q.id);begin();r.value=static_cast<U32>(reinterpret_cast<F>(gameMethod(a[0],15))(pointer(a[0]),0,a[2],ownedWindow,a[4],pp,static_cast<void **>(pointer(a[6]))));capture();}
  gfxOutputResult(r,a[6],GfxDevice,gfxFactory);if(static_cast<LONG>(r.value)>=0)gfxDevice=*static_cast<U32 *>(pointer(a[6]));
  r.extras+=" presentation_hex="+encodeHex(pp,52)+" baseline_token_hex="+encodeHex(gfxBaselineToken.data(),32);return r;
 }
 if(q.op=="GFX_CAPS"||q.op=="GFX_CREATION"||q.op=="GFX_DEVICE_MODE"||q.op=="GFX_SURFACE_DESC"||q.op=="GFX_VERTEX_DESC"){
  U32 kind=GfxDevice,slot=7,size=212;if(q.op=="GFX_CREATION"){slot=9;size=16;}if(q.op=="GFX_DEVICE_MODE"){slot=8;size=16;}
  if(q.op=="GFX_SURFACE_DESC"){kind=GfxSurface;slot=8;size=32;}if(q.op=="GFX_VERTEX_DESC"){kind=GfxVertex;slot=13;size=24;}
  if(!args(2)||!gfxHas(a[0],kind)||!windowRange(a[1],size))return reject("OWNED_GFX_STRUCTURE_OUTPUT");using F=HRESULT(STDMETHODCALLTYPE *)(void *,void *);
  {GameCallScope c(guard,q.id);begin();r.value=static_cast<U32>(reinterpret_cast<F>(gameMethod(a[0],slot))(pointer(a[0]),pointer(a[1])));capture();}return r;
 }
 if(q.op=="GFX_GET_FACTORY"||q.op=="GFX_BACKBUFFER"||q.op=="GFX_TEXTURE_SURFACE"){
  U32 slot=6,kind=GfxDevice,outKind=GfxFactory;if(q.op=="GFX_BACKBUFFER")slot=16;else if(q.op=="GFX_TEXTURE_SURFACE"){slot=15;kind=GfxTexture;}
  size_t n=slot==6?2:slot==15?3:4;if(!args(n)||!gfxHas(a[0],kind)||!gfxOutput(a.back())||(n>=3&&a[1])||(n==4&&a[2]))return reject("OWNED_GFX_REFERENCE_OUTPUT");
  if(slot==6){using F=HRESULT(STDMETHODCALLTYPE *)(void *,void **);GameCallScope c(guard,q.id);begin();r.value=static_cast<U32>(reinterpret_cast<F>(gameMethod(a[0],6))(pointer(a[0]),static_cast<void **>(pointer(a[1]))));capture();}
  else if(slot==15){using F=HRESULT(STDMETHODCALLTYPE *)(void *,UINT,void **);GameCallScope c(guard,q.id);begin();r.value=static_cast<U32>(reinterpret_cast<F>(gameMethod(a[0],15))(pointer(a[0]),0,static_cast<void **>(pointer(a[2]))));capture();}
  else {using F=HRESULT(STDMETHODCALLTYPE *)(void *,UINT,U32,void **);GameCallScope c(guard,q.id);begin();r.value=static_cast<U32>(reinterpret_cast<F>(gameMethod(a[0],16))(pointer(a[0]),0,0,static_cast<void **>(pointer(a[3]))));capture();}
  if(slot!=6)outKind=GfxSurface;else if(static_cast<LONG>(r.value)>=0&&*static_cast<U32 *>(pointer(a.back()))!=gfxFactory)fatal(125);
  gfxOutputResult(r,a.back(),outKind,slot==6?0:a[0]);return r;
 }
 if(q.op=="GFX_CHECK_FORMAT"){
  if(!args(7)||!gfxHas(a[0],GfxFactory)||a[1]||(a[2]!=1&&a[2]!=2)||!gfxAllowedFormat(a[3])||!gfxAllowedFormat(a[6])||!((a[4]==1&&a[5]==1)||(a[4]==512&&a[5]==3)))return reject("ORIGINAL_GFX_FORMAT_QUERY");
  using F=HRESULT(STDMETHODCALLTYPE *)(void *,UINT,U32,U32,DWORD,U32,U32);{GameCallScope c(guard,q.id);begin();r.value=static_cast<U32>(reinterpret_cast<F>(gameMethod(a[0],10))(pointer(a[0]),a[1],a[2],a[3],a[4],a[5],a[6]));capture();}return r;
 }
 if(q.op=="GFX_VIEWPORT"){
  const U32 expected[]={0,0,1024,768,0,0x3f800000};if(!args(2)||!gfxHas(a[0],GfxDevice)||!windowRange(a[1],24)||memcmp(pointer(a[1]),expected,24))return reject("ORIGINAL_VIEWPORT24");
  using F=HRESULT(STDMETHODCALLTYPE *)(void *,void *);{GameCallScope c(guard,q.id);begin();r.value=static_cast<U32>(reinterpret_cast<F>(gameMethod(a[0],40))(pointer(a[0]),pointer(a[1])));capture();}return r;
 }
 if(q.op=="GFX_DEBUG_MUTE"||q.op=="GFX_DEBUG_MUTE_RESOLVED"){
  bool resolved=q.op=="GFX_DEBUG_MUTE_RESOLVED";if(!args(resolved?2:1)||!gfxModule||a.back()>1||gfxMuteCalls>=8)return reject("BOUNDED_ORIGINAL_DEBUG_MUTE_PAIR");
  U32 method=0,module=resolved?a[0]:ptr(gfxModule);if(resolved){if(!gfxDebugProcs.count(module))return reject("CURRENT_RESOLVED_DEBUG_EXPORT");method=gfxDebugProcs.at(module);}
  else {FARPROC f=GetProcAddress(gfxModule,"DebugSetMute");method=ptr(reinterpret_cast<void *>(f));}
  if(!method)return reject("ACTUAL_DEBUG_EXPORT_REQUIRED");
  if(!gfxMuteAllowed(gfxMuteStates[module],a.back(),gfxMuteCounts[module],gfxMuteCalls))return reject("PER_MODULE_ORIGINAL_DEBUG_MUTE_PAIR");
  {GameCallScope c(guard,q.id);begin();r.value=gfxVoidMute(method,a.back());capture();}
  gfxMuteStates[module]=a.back();++gfxMuteCounts[module];gfxMute=0;for(const auto &p:gfxMuteStates)gfxMute+=p.second;++gfxMuteCalls;
  r.extras="native_return_type=void eax_is_status=0 method="+number(method)+" module="+number(module)+" module_mute_balance="+number(a.back())+" mute_total_balance="+number(gfxMute);return r;
 }
 if(q.op=="GFX_TEXTURE"){
  if(!args(8)||!gfxHas(a[0],GfxDevice)||!gfxOutput(a[7]))return reject("OWNED_TEXTURE_OUTPUT");
  bool cache=a[1]==64&&a[2]==16&&a[3]==1&&a[4]==512&&a[5]==21&&a[6]==0;
  bool atlas=a[1]==256&&a[2]==256&&a[3]==1&&!a[4]&&a[5]==26&&a[6]==1&&gfxAtlasCreates<2;
  if(!cache&&!atlas)return reject("FIXED_CACHE_OR_TWO_FONT_TEXTURES");if(cache)for(const auto &p:gfxObjects)if(p.second.kind==GfxTexture&&p.second.width==64)return reject("ONE_CACHE_TEXTURE");
  using F=HRESULT(STDMETHODCALLTYPE *)(void *,UINT,UINT,UINT,DWORD,U32,U32,void **);
  {GameCallScope c(guard,q.id);begin();r.value=static_cast<U32>(reinterpret_cast<F>(gameMethod(a[0],20))(pointer(a[0]),a[1],a[2],a[3],a[4],a[5],a[6],static_cast<void **>(pointer(a[7]))));capture();}
  gfxOutputResult(r,a[7],GfxTexture,a[0]);if(static_cast<LONG>(r.value)>=0){auto &p=gfxObjects.at(*static_cast<U32 *>(pointer(a[7])));p.width=a[1];p.height=a[2];p.format=a[5];if(atlas)++gfxAtlasCreates;}return r;
 }
 if(q.op=="GFX_LEVEL_DESC"){
  if(!args(3)||!gfxHas(a[0],GfxTexture)||a[1]||!windowRange(a[2],32))return reject("OWNED_TEXTURE_LEVEL0_DESC");using F=HRESULT(STDMETHODCALLTYPE *)(void *,UINT,void *);
  {GameCallScope c(guard,q.id);begin();r.value=static_cast<U32>(reinterpret_cast<F>(gameMethod(a[0],14))(pointer(a[0]),0,pointer(a[2])));capture();}return r;
 }
 if(q.op=="GFX_LOCK"){
  if(!args(5)||!gfxHas(a[0],GfxTexture)||a[1]||!windowRange(a[2],8)||a[3]||(a[4]!=0&&a[4]!=16))return reject("OWNED_FONT_LEVEL0_LOCK");auto &p=gfxObjects.at(a[0]);
  if(p.locked||p.width!=256||p.height!=256||p.format!=26)return reject("FONT_ATLAS_LOCK_ONLY");using F=HRESULT(STDMETHODCALLTYPE *)(void *,UINT,void *,const RECT *,DWORD);
  {GameCallScope c(guard,q.id);begin();r.value=static_cast<U32>(reinterpret_cast<F>(gameMethod(a[0],16))(pointer(a[0]),0,pointer(a[2]),nullptr,a[4]));capture();}
  if(static_cast<LONG>(r.value)>=0){U32 *v=static_cast<U32 *>(pointer(a[2]));p.locked=true;p.pitch=v[0];p.bits=v[1];if(p.pitch<512||p.pitch>1024||!p.bits||static_cast<uint64_t>(p.bits)+p.pitch*256>0x100000000ull)fatal(126);p.format=a[4]==16?0x8000001a:26;r.extras="pitch="+number(p.pitch)+" bits="+number(p.bits)+" lock_bytes="+number(p.pitch*256);}return r;
 }
 if(q.op=="GFX_LOCK_READ"||q.op=="GFX_LOCK_WRITE"){
  if(!args(4)||!gfxHas(a[0],GfxTexture)||!a[3]||a[3]>kMaxTransfer||!windowRange(a[2],a[3]))return reject("BOUNDED_LOCK_TRANSFER");auto &p=gfxObjects.at(a[0]);
  if(!p.locked||!gfxSpanFits(a[1],a[3],p.pitch*256)||(q.op=="GFX_LOCK_WRITE"&&p.format!=26))return reject("CURRENT_WRITABLE_OWNED_LOCK");
  if(q.op=="GFX_LOCK_READ")memcpy(pointer(a[2]),pointer(p.bits+a[1]),a[3]);else memcpy(pointer(p.bits+a[1]),pointer(a[2]),a[3]);r.value=a[3];r.extras="infrastructure=1";return r;
 }
 if(q.op=="GFX_UNLOCK"){
  if(!args(2)||!gfxHas(a[0],GfxTexture)||a[1]||!gfxObjects.at(a[0]).locked)return reject("CURRENT_TEXTURE_LOCK");using F=HRESULT(STDMETHODCALLTYPE *)(void *,UINT);
  {GameCallScope c(guard,q.id);begin();r.value=static_cast<U32>(reinterpret_cast<F>(gameMethod(a[0],17))(pointer(a[0]),0));capture();}
  if(static_cast<LONG>(r.value)>=0){auto &p=gfxObjects.at(a[0]);p.locked=false;p.bits=0;p.format=26;}return r;
 }
 if(q.op=="GFX_VERTEX_BUFFER"){
  if(!args(6)||!gfxHas(a[0],GfxDevice)||a[1]!=8400||a[2]!=520||a[3]||a[4]||!gfxOutput(a[5])||gfxVBcreates>=2)return reject("TWO_ORIGINAL_FONT_VERTEX_BUFFERS");
  using F=HRESULT(STDMETHODCALLTYPE *)(void *,UINT,DWORD,DWORD,U32,void **);{GameCallScope c(guard,q.id);begin();r.value=static_cast<U32>(reinterpret_cast<F>(gameMethod(a[0],23))(pointer(a[0]),8400,520,0,0,static_cast<void **>(pointer(a[5]))));capture();}
  gfxOutputResult(r,a[5],GfxVertex,a[0]);if(static_cast<LONG>(r.value)>=0)++gfxVBcreates;return r;
 }
 if(q.op=="GFX_BEGIN"||q.op=="GFX_END"||q.op=="GFX_TEXTURE_BIND"||q.op=="GFX_RENDER_STATE"||q.op=="GFX_STAGE_STATE"){
  U32 op=q.op=="GFX_BEGIN"?0:q.op=="GFX_TEXTURE_BIND"?1:q.op=="GFX_RENDER_STATE"?2:q.op=="GFX_STAGE_STATE"?3:4;
  size_t n=op==0?1:op==4?2:op==3?4:3;if(!args(n)||!gfxHas(a[0],GfxDevice))return reject("OWNED_FONT_STATE_DEVICE");
  bool unbind=op==1&&a[1]==0&&a[2]==0&&!gfxRecording;
  const GfxStep &step=gfxFontPlan[gfxFontStep%30];
  if(!unbind&&(gfxFontStep>=120||op!=step.op||gfxVBcreates<gfxFontStep/60+1||(op==1&&(!gfxHas(a[2],GfxTexture)||gfxObjects.at(a[2]).width!=256||a[1]))||
    (op==2&&(a[1]!=step.a||a[2]!=step.b))||(op==3&&(a[1]!=step.a||a[2]!=step.b||a[3]!=step.c))||(op==0&&gfxRecording)||(op==4&&(!gfxRecording||!gfxOutput(a[1])))))return reject("FIXED_FOUR_FONT_STATEBLOCK_PLANS");
  if(op==0){using F=HRESULT(STDMETHODCALLTYPE *)(void *);GameCallScope c(guard,q.id);begin();r.value=static_cast<U32>(reinterpret_cast<F>(gameMethod(a[0],52))(pointer(a[0])));capture();}
  else if(op==4){using F=HRESULT(STDMETHODCALLTYPE *)(void *,DWORD *);GameCallScope c(guard,q.id);begin();r.value=static_cast<U32>(reinterpret_cast<F>(gameMethod(a[0],53))(pointer(a[0]),static_cast<DWORD *>(pointer(a[1]))));capture();}
  else if(op==1){using F=HRESULT(STDMETHODCALLTYPE *)(void *,DWORD,void *);GameCallScope c(guard,q.id);begin();r.value=static_cast<U32>(reinterpret_cast<F>(gameMethod(a[0],61))(pointer(a[0]),0,pointer(a[2])));capture();}
  else if(op==2){using F=HRESULT(STDMETHODCALLTYPE *)(void *,U32,DWORD);GameCallScope c(guard,q.id);begin();r.value=static_cast<U32>(reinterpret_cast<F>(gameMethod(a[0],50))(pointer(a[0]),a[1],a[2]));capture();}
  else {using F=HRESULT(STDMETHODCALLTYPE *)(void *,DWORD,U32,DWORD);GameCallScope c(guard,q.id);begin();r.value=static_cast<U32>(reinterpret_cast<F>(gameMethod(a[0],63))(pointer(a[0]),a[1],a[2],a[3]));capture();}
  if(static_cast<LONG>(r.value)>=0){if(op==0)gfxRecording=true;if(op==1&&!gfxRecording)gfxBoundTexture=a[2];if(op==4){U32 token=*static_cast<U32 *>(pointer(a[1]));if(!token||gfxBlocks.count(token))fatal(127);gfxBlocks[token]=a[0];gfxRecording=false;r.extras="token="+number(token);}if(!unbind)++gfxFontStep;}return r;
 }
 if(q.op=="GFX_DELETE_BLOCK"){
  if(!args(2)||!gfxHas(a[0],GfxDevice)||!gfxBlocks.count(a[1])||gfxBlocks.at(a[1])!=a[0]||gfxRecording)return reject("OWNED_STATEBLOCK_TOKEN");using F=HRESULT(STDMETHODCALLTYPE *)(void *,DWORD);
  {GameCallScope c(guard,q.id);begin();r.value=static_cast<U32>(reinterpret_cast<F>(gameMethod(a[0],56))(pointer(a[0]),a[1]));capture();}if(static_cast<LONG>(r.value)>=0)gfxBlocks.erase(a[1]);return r;
 }
 if(q.op=="GFX_GET_RENDER_STATE"){
  if(!args(3)||!gfxHas(a[0],GfxDevice)||!windowRange(a[2],4)||std::none_of(std::begin(gfxFontPlan),std::end(gfxFontPlan),[&](const GfxStep &s){return s.op==2&&s.a==a[1];}))return reject("ORIGINAL_FONT_RENDER_STATE_QUERY");
  using F=HRESULT(STDMETHODCALLTYPE *)(void *,U32,DWORD *);{GameCallScope c(guard,q.id);begin();r.value=static_cast<U32>(reinterpret_cast<F>(gameMethod(a[0],51))(pointer(a[0]),a[1],static_cast<DWORD *>(pointer(a[2]))));capture();}return r;
 }
 if(q.op=="GFX_GAMMA_READ"){
  if(!args(2)||!gfxHas(a[0],GfxDevice)||!windowRange(a[1],1536))return reject("OWNED_DEVICE_GAMMA_OUTPUT");
  {GameCallScope c(guard,q.id);begin();r.value=gfxReadGamma(a[0],pointer(a[1]));capture();}r.extras="native_return_type=void eax_is_status=0";return r;
 }
 if(q.op=="GFX_GAMMA_SAVE"||q.op=="GFX_GAMMA_SET"||q.op=="GFX_GAMMA_RESTORE"){
  bool set=q.op=="GFX_GAMMA_SET",restore=q.op=="GFX_GAMMA_RESTORE";if(!args(set?3:2)||!gfxHas(a[0],GfxDevice)||!windowRange(a.back(),1536))return reject("OWNED_DEVICE_GAMMA1536");
  if((!set&&!restore&&(gfxGammaSaved||gfxGammaDirty))||((set||restore)&&!gfxGammaSaved)||(set&&(a[1]!=1||gfxGammaDirty||gfxFontStep!=120)))return reject("DEVICE_GAMMA_LIFETIME_ORDER");
  if(set){const auto *v=static_cast<const WORD *>(pointer(a[2]));for(U32 ch=0;ch<3;++ch)for(U32 i=0;i<256;++i)if(v[ch*256+i]!=(i<<8))return reject("ORIGINAL_IDENTITY_GAMMA");}
  std::array<unsigned char,1536> after{};
  {GameCallScope c(guard,q.id);begin();
   if(set||restore){gfxGammaDirty=true;r.value=gfxVoidGamma(gameMethod(a[0],18),a[0],set?1:0,set?pointer(a[2]):gfxOriginalGamma.data());capture();gfxReadGamma(a[0],after.data());}
   else {r.value=gfxReadGamma(a[0],after.data());capture();}
  }
  U32 observedEax=r.value;
  if(!set&&!restore){gfxOriginalGamma=after;gfxGammaSaved=true;memcpy(pointer(a[1]),after.data(),1536);r.value=1;}
  if(restore){memcpy(pointer(a[1]),after.data(),1536);if(after==gfxOriginalGamma)gfxGammaDirty=false;}
  r.extras="native_return_type=void eax_is_status=0 observed_eax="+number(observedEax)+" infrastructure="+number(!set)+" baseline_token_hex="+encodeHex(gfxBaselineToken.data(),32)+" gamma_after_hex="+encodeHex(after.data(),1536)+" gamma_restored="+number(restore&&!gfxGammaDirty)+" gamma_dirty="+number(gfxGammaDirty);return r;
 }
 if(q.op=="GFX_GET_OBJECT"){
  if(!args(3)||a[1]!=60||!windowRange(a[2],60)||(!fonts.count(a[0])&&!gfxFonts.count(a[0])))return reject("OWNED_FONT_LOGFONT60");begin();r.value=static_cast<U32>(GetObjectA(handle(a[0]),60,pointer(a[2])));capture();return r;
 }
 if(q.op=="GFX_DC_CREATE"){
  if(!args(1)||a[0]||gfxDCs.size()>=3)return reject("THREE_OWNED_COMPATIBLE_FONT_DCS");begin();r.value=ptr(CreateCompatibleDC(nullptr));capture();if(r.value&&!gfxDCs.emplace(r.value,GfxDC{}).second)fatal(129);return r;
 }
 if(q.op=="GFX_DIB"){
  if(!args(6)||!gfxDCs.count(a[0])||!windowRange(a[1],40)||a[2]||!gfxOutput(a[3])||a[4]||a[5]||gfxBitmaps.size()>=3||!gfxDisjoint(a[1],40,a[3],4))return reject("OWNED_FONT_DIB_PARAMETERS");
  BITMAPINFOHEADER h{};h.biSize=40;h.biWidth=256;h.biHeight=-256;h.biPlanes=1;h.biBitCount=32;
  if(memcmp(pointer(a[1]),&h,40))return reject("EXACT_TOP_DOWN_FONT_DIB");begin();r.value=ptr(CreateDIBSection(static_cast<HDC>(handle(a[0])),static_cast<BITMAPINFO *>(pointer(a[1])),0,static_cast<void **>(pointer(a[3])),nullptr,0));capture();
  if(r.value){U32 bits=*static_cast<U32 *>(pointer(a[3]));if(!bits||static_cast<uint64_t>(bits)+262144>0x100000000ull)fatal(128);if(!gfxBitmaps.emplace(r.value,GfxBitmap{bits,262144,false}).second)fatal(130);r.extras="bits="+number(bits)+" bytes=262144";}return r;
 }
 if(q.op=="GFX_FONT_INDIRECT"){
  if(!args(1)||!windowRange(a[0],60)||gfxFonts.size()>=3)return reject("OWNED_LOGFONT_INPUT");const auto *lf=static_cast<LOGFONTA *>(pointer(a[0]));
  if(!memchr(lf->lfFaceName,0,32)||lf->lfHeight< -256||lf->lfHeight>256||lf->lfWidth<0||lf->lfWidth>256)return reject("BOUNDED_ORIGINAL_FONT");begin();r.value=ptr(CreateFontIndirectA(lf));capture();if(r.value&&!gfxFonts.emplace(r.value,false).second)fatal(131);return r;
 }
 if(q.op=="GFX_SELECT"){
  if(!args(2)||!gfxDCs.count(a[0]))return reject("OWNED_FONT_DC_SELECTION");auto &dc=gfxDCs.at(a[0]);bool bitmap=gfxBitmaps.count(a[1])||a[1]==dc.oldBitmap;bool font=fonts.count(a[1])||gfxFonts.count(a[1])||a[1]==dc.oldFont;
  if(!a[1]||(!bitmap&&!font))return reject("OWNED_OR_THIS_DC_RESTORATION_OBJECT");begin();r.value=ptr(SelectObject(static_cast<HDC>(handle(a[0])),handle(a[1])));capture();
  if(r.value&&r.value!=UINT32_MAX){if(bitmap){if(!dc.oldBitmap)dc.oldBitmap=r.value;dc.bitmap=a[1];}else{if(!dc.oldFont)dc.oldFont=r.value;dc.font=a[1];}}
  r.extras="selected_bitmap="+number(ptr(GetCurrentObject(static_cast<HDC>(handle(a[0])),OBJ_BITMAP)))+" selected_font="+number(ptr(GetCurrentObject(static_cast<HDC>(handle(a[0])),OBJ_FONT)));return r;
 }
 if(q.op=="GFX_BK_MODE"||q.op=="GFX_BK_COLOR"||q.op=="GFX_TEXT_COLOR"||q.op=="GFX_MAP_MODE"||q.op=="GFX_TEXT_ALIGN"){
  if(!args(2)||!gfxDCs.count(a[0]))return reject("OWNED_FONT_DC_STATE");HDC dc=static_cast<HDC>(handle(a[0]));
  if((q.op=="GFX_BK_MODE"&&(a[1]!=1&&a[1]!=2))||(q.op=="GFX_BK_COLOR"&&a[1])||(q.op=="GFX_TEXT_COLOR"&&a[1]!=0xffffff)||(q.op=="GFX_MAP_MODE"&&a[1]!=1)||(q.op=="GFX_TEXT_ALIGN"&&a[1]))return reject("ORIGINAL_FONT_DC_STATE_VALUES");begin();
  if(q.op=="GFX_BK_MODE")r.value=static_cast<U32>(SetBkMode(dc,static_cast<int>(a[1])));else if(q.op=="GFX_BK_COLOR")r.value=SetBkColor(dc,a[1]);else if(q.op=="GFX_TEXT_COLOR")r.value=SetTextColor(dc,a[1]);else if(q.op=="GFX_MAP_MODE")r.value=static_cast<U32>(SetMapMode(dc,static_cast<int>(a[1])));else r.value=SetTextAlign(dc,a[1]);capture();return r;
 }
 if(q.op=="GFX_MULDIV"){
  if(!args(3)||(a[0]!=8&&a[0]!=12)||a[1]!=96||a[2]!=72)return reject("ORIGINAL_FONT_MULDIV");begin();r.value=static_cast<U32>(MulDiv(static_cast<int>(a[0]),96,72));capture();return r;
 }
 if(q.op=="GFX_TEXT_EXTENT"||q.op=="GFX_TEXT_OUT"){
  bool draw=q.op=="GFX_TEXT_OUT";if(!args(draw?8:4)||!gfxDCs.count(a[0]))return reject("OWNED_FONT_GLYPH_DC");
  U32 text=draw?a[5]:a[1],count=draw?a[6]:a[2];if(count!=1||!windowRange(text,1)||*static_cast<unsigned char *>(pointer(text))<32||*static_cast<unsigned char *>(pointer(text))>126)return reject("ORIGINAL_ASCII_GLYPH");
  HDC dc=static_cast<HDC>(handle(a[0]));if(draw){if(a[1]>=256||a[2]>=256||a[3]!=2||a[4]||a[7]||!gfxBitmaps.count(gfxDCs.at(a[0]).bitmap))return reject("OWNED_FONT_DIB_GLYPH_POSITION");begin();r.value=ExtTextOutA(dc,static_cast<int>(a[1]),static_cast<int>(a[2]),2,nullptr,static_cast<LPCSTR>(pointer(text)),1,nullptr);capture();}
  else {if(!windowRange(a[3],8))return reject("OWNED_SIZE_OUTPUT");begin();r.value=GetTextExtentPoint32A(dc,static_cast<LPCSTR>(pointer(text)),1,static_cast<SIZE *>(pointer(a[3])));capture();}return r;
 }
 if(q.op=="GFX_DIB_READ"||q.op=="GFX_DIB_WRITE"){
  if(!args(4)||!gfxBitmaps.count(a[0])||!a[3]||a[3]>kMaxTransfer||!windowRange(a[2],a[3]))return reject("OWNED_DIB_TRANSFER");const auto &b=gfxBitmaps.at(a[0]);if(b.deleteIssued||!gfxSpanFits(a[1],a[3],b.bytes))return reject("LIVE_BOUNDED_DIB_BYTES");
  begin();BOOL flush=GdiFlush();capture();if(!flush)return reject("GDI_FONT_FLUSH_FAILED",r.error);
  if(q.op=="GFX_DIB_READ")memcpy(pointer(a[2]),pointer(b.bits+a[1]),a[3]);else memcpy(pointer(b.bits+a[1]),pointer(a[2]),a[3]);r.value=a[3];r.extras="flush=1 infrastructure=1";return r;
 }
 if(q.op=="GFX_DELETE_OBJECT"){
  if(!args(1)||(!gfxBitmaps.count(a[0])&&!gfxFonts.count(a[0])&&!fonts.count(a[0])))return reject("OWNED_FONT_OR_DIB_DELETE");
  begin();r.value=DeleteObject(handle(a[0]));capture();if(r.value){if(gfxBitmaps.count(a[0]))gfxBitmaps.at(a[0]).deleteIssued=true;else gfxFonts[a[0]]=true;}
  U32 liveType=GetObjectType(handle(a[0]));unsigned char probe[60]{};int liveBytes=GetObjectA(handle(a[0]),60,probe);std::string swept=gfxSweepGDI();
  bool retired=!gfxBitmaps.count(a[0])&&!gfxFonts.count(a[0])&&!fonts.count(a[0]);r.extras="object_type_after="+number(liveType)+" object_bytes_after="+number(static_cast<U32>(liveBytes))+" retirement_observed="+number(retired)+" deferred_delete="+number(r.value&&!retired)+" "+swept;return r;
 }
 if(q.op=="GFX_DC_DELETE"){
  if(!args(1)||!gfxDCs.count(a[0]))return reject("OWNED_COMPATIBLE_DC_DELETE");begin();r.value=DeleteDC(static_cast<HDC>(handle(a[0])));capture();U32 type=GetObjectType(handle(a[0]));
  if(r.value&&type==0)gfxDCs.erase(a[0]);std::string swept=gfxSweepGDI();r.extras="object_type_after="+number(type)+" retirement_observed="+number(r.value&&type==0)+" "+swept;return r;
 }
 return reject("GFX_OPERATION_NOT_ADMITTED");
}
