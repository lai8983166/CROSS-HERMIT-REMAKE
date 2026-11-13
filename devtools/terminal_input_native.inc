// Fixed original DirectInput/cursor leaves. Build only; no standalone launcher.
struct InputObject { U32 kind=0,refs=1,parent=0; bool format=false,cooperative=false,acquired=false,unacquired=false; };
struct InputObjectFormat { const GUID *guid; DWORD offset,type,flags; };
struct InputDataFormat { DWORD size,objectSize,flags,dataSize,count; const InputObjectFormat *objects; };
struct InputCursorSnapshot { DWORD flags,cursor; LONG x,y,left,top,right,bottom; DWORD lastInput; };
static_assert(sizeof(InputObjectFormat)==16 && sizeof(InputDataFormat)==24 && sizeof(InputCursorSnapshot)==36,"original x86 input ABI");
@@INPUT_CONSTANTS@@
std::map<U32,InputObject> inputObjects;
HMODULE inputModule=nullptr;
bool inputGate=false,inputBaseline=false,inputInstance=false,inputPositionChanged=false;
bool inputCursorRestored=false;
bool inputConvertedPointValid=false;
POINT inputConvertedPoint{};
LONG inputShowDelta=0,inputInitialCount=0,inputLastCount=0;
bool inputCountKnown=false;
U32 inputCalls=0,inputShowCalls=0,inputUnacquires=0,inputReleases=0;
U32 inputUnexpectedOutputs=0;
InputCursorSnapshot inputOriginal{},inputLast{};
bool inputEmpty(){return inputObjects.empty()&&!inputModule&&!inputBaseline&&!inputShowDelta&&!inputPositionChanged&&!inputUnexpectedOutputs;}
std::string inputStatus(){return "input_gate="+number(inputGate)+" input_baseline="+number(inputBaseline)+" input_instance="+number(inputInstance)+
 " input_interfaces="+number(static_cast<U32>(inputObjects.size()))+" input_modules="+number(inputModule!=nullptr)+
 " input_show_delta_bits="+number(static_cast<U32>(inputShowDelta))+" input_position_dirty="+number(inputPositionChanged)+
 " input_cursor_restored="+number(inputCursorRestored)+
 " input_unexpected_outputs="+number(inputUnexpectedOutputs)+
 " input_unacquires="+number(inputUnacquires)+" input_releases="+number(inputReleases);}
bool inputReadCursor(InputCursorSnapshot &s){
 CURSORINFO c{};c.cbSize=sizeof(c);POINT p{};RECT r{};LASTINPUTINFO l{};l.cbSize=sizeof(l);
 if(!GetCursorInfo(&c)||!GetCursorPos(&p)||!GetClipCursor(&r)||!GetLastInputInfo(&l))return false;
 s={c.flags,ptr(c.hCursor),p.x,p.y,r.left,r.top,r.right,r.bottom,l.dwTime};return true;
}
bool inputSafe(){LASTINPUTINFO l{};l.cbSize=sizeof(l);return inputBaseline&&ownedWindow&&IsWindow(ownedWindow)&&
 GetLastInputInfo(&l)&&l.dwTime==inputOriginal.lastInput&&GetForegroundWindow()==ownedWindow;}
bool inputHas(U32 object,U32 kind=0){auto i=inputObjects.find(object);return i!=inputObjects.end()&&i->second.refs&&(kind==0||i->second.kind==kind);}
std::string inputInfo(U32 object){const auto &p=inputObjects.at(object);std::string s="object="+number(object)+" kind="+number(p.kind)+
 " owned_refs="+number(p.refs)+" group="+number(p.parent)+" vtable="+number(*static_cast<U32 *>(pointer(object)))+" method2="+number(gameMethod(object,2));
 std::vector<U32> slots=p.kind==20?std::vector<U32>{3}:std::vector<U32>{6,7,8,11,13,15};
 for(U32 slot:slots)s+=" method"+number(slot)+"="+number(gameMethod(object,slot));return s;
}
bool inputOp(const std::string &op){return op.size()>6&&op.compare(0,6,"INPUT_")==0;}
Result inputDispatchImpl(const Request &q,std::unique_lock<std::mutex> &guard,U32 savedError){
 Result r;r.error=savedError;std::vector<U32>a;const auto args=[&](size_t n){return numeric(q,n,a);};
 const auto begin=[&](){SetLastError(savedError);};const auto capture=[&](){r.error=GetLastError();};
 if(q.lane||GetCurrentThreadId()!=lanes[0].tid||__readfsdword(0x18)!=lanes[0].teb||!windowCallbacks.empty())return reject("INPUT_CURRENT_MAIN_OUTSIDE_CALLBACK");
 if(++inputCalls>512)return reject("BOUNDED_INPUT_INITIALIZATION_ONLY");
 if(q.op=="INPUT_GATE"){
  if(!args(1)||a[0]>1||!inputEmpty()||(a[0]&&(!gfxGate||!gfxBaseline||!ownedWindow)))return reject("INPUT_GATE_CURRENT_GRAPHICS_BASELINE");
  inputGate=a[0]!=0;r.value=1;r.extras=inputStatus();return r;
 }
 if(!inputGate)return reject("INPUT_GATE_CLOSED",ERROR_ACCESS_DENIED);
 if(q.op=="INPUT_BASELINE"){
  if(!args(2)||inputBaseline||!gfxBaseline||!windowRange(a[0],32)||!windowRange(a[1],36)||
     memcmp(pointer(a[0]),gfxBaselineToken.data(),32))return reject("INPUT_PARENT_BASELINE_TOKEN_AND_CURSOR36");
  InputCursorSnapshot actual{};begin();BOOL ok=inputReadCursor(actual);capture();
  if(!ok||memcmp(&actual,pointer(a[1]),36))return reject("INPUT_ACTUAL_CURSOR_BASELINE_MISMATCH",r.error);
  inputOriginal=inputLast=actual;inputBaseline=true;inputCursorRestored=false;r.value=1;
  r.extras="cursor_hex="+encodeHex(&actual,36)+" observed=1";return r;
 }
 if(!inputBaseline)return reject("INPUT_ACTUAL_PARENT_BASELINE_REQUIRED");
 if(q.op=="INPUT_INSTANCE_INFO"){
  if(!args(1)||!windowModule||a[0]!=ptr(windowModule)||!ownedWindow)return reject("ORIGINAL_WINMAIN_INSTANCE_ONLY");
  HMODULE actual=nullptr;MEMORY_BASIC_INFORMATION mi{};begin();
  BOOL found=GetModuleHandleExW(GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS|GET_MODULE_HANDLE_EX_FLAG_UNCHANGED_REFCOUNT,
   reinterpret_cast<LPCWSTR>(windowModule),&actual);SIZE_T n=VirtualQuery(windowModule,&mi,sizeof(mi));capture();
  auto dos=reinterpret_cast<const IMAGE_DOS_HEADER *>(windowModule);
  bool valid=found&&actual==windowModule&&n==sizeof(mi)&&mi.AllocationBase==windowModule&&mi.Type==MEM_IMAGE&&
   !(a[0]&3)&&dos->e_magic==IMAGE_DOS_SIGNATURE&&dos->e_lfanew>0&&dos->e_lfanew<1024;
  const IMAGE_NT_HEADERS32 *nt=valid?reinterpret_cast<const IMAGE_NT_HEADERS32 *>(reinterpret_cast<const unsigned char *>(windowModule)+dos->e_lfanew):nullptr;
  valid=valid&&nt->Signature==IMAGE_NT_SIGNATURE&&nt->FileHeader.Machine==IMAGE_FILE_MACHINE_I386&&
   (nt->FileHeader.Characteristics&IMAGE_FILE_DLL)&&GetWindowLongPtrW(ownedWindow,GWLP_HINSTANCE)==reinterpret_cast<LONG_PTR>(windowModule);
  inputInstance=valid;r.value=valid;r.extras="original_instance="+number(a[0])+" loaded_instance="+number(ptr(actual))+
   " image_mapping="+number(n==sizeof(mi)&&mi.Type==MEM_IMAGE)+" entry_rva="+number(valid?nt->OptionalHeader.AddressOfEntryPoint:0)+
   " unchanged_module_refcount=1 helper_instance_substituted=0 creator_proxy_declared=1";return r;
 }
 if(q.op=="INPUT_CREATE"){
  if(!args(5)||!inputInstance||a[0]!=ptr(windowModule)||a[1]!=0x800||a[2]!=0x5cc1bc||!gameOutput(a[3])||a[4]||inputModule||!inputObjects.empty())return reject("ORIGINAL_DIRECTINPUT8_CREATE5");
  FARPROC fn=nullptr;{GameCallScope c(guard,q.id);begin();inputModule=LoadLibraryExW(L"dinput8.dll",nullptr,LOAD_LIBRARY_SEARCH_SYSTEM32);capture();}
  if(!inputModule)return reject("DIRECTINPUT_RUNTIME_LOAD_FAILED",r.error);
  fn=GetProcAddress(inputModule,"DirectInput8Create");if(!fn)return reject("DIRECTINPUT8_EXPORT_REQUIRED");
  using F=HRESULT(WINAPI *)(HINSTANCE,DWORD,REFIID,void **,void *);
  {GameCallScope c(guard,q.id);begin();r.value=static_cast<U32>(reinterpret_cast<F>(fn)(windowModule,0x800,*inputGuid(0x5cc1bc),static_cast<void **>(pointer(a[3])),nullptr));capture();}
  U32 object=*static_cast<U32 *>(pointer(a[3]));
  if(static_cast<LONG>(r.value)>=0){if(!object)fatal(140);inputObjects.emplace(object,InputObject{20});r.extras=inputInfo(object);}
  else {if(object)++inputUnexpectedOutputs;r.extras="object="+number(object)+" kind=20";}
  wchar_t path[520]{};DWORD count=GetModuleFileNameW(inputModule,path,520);if(!count||count>=520)fatal(142);
  r.extras+=" original_instance="+number(a[0])+" runtime_module="+number(ptr(inputModule))+" export="+number(ptr(reinterpret_cast<void *>(fn)))+
   " runtime_path_hex="+encodeHex(path,(count+1)*2);return r;
 }
 if(q.op=="INPUT_DEVICE"){
  if(!args(4)||!inputHas(a[0],20)||(a[1]!=0x5cc04c&&a[1]!=0x5cc05c)||!gameOutput(a[2])||a[3]||inputObjects.size()>=3)return reject("TWO_ORIGINAL_SYSTEM_INPUT_DEVICES");
  U32 kind=a[1]==0x5cc04c?21:22;for(const auto &p:inputObjects)if(p.second.kind==kind)return reject("ONE_DEVICE_PER_ORIGINAL_KIND");
  using F=HRESULT(STDMETHODCALLTYPE *)(void *,REFGUID,void **,void *);
  {GameCallScope c(guard,q.id);begin();r.value=static_cast<U32>(reinterpret_cast<F>(gameMethod(a[0],3))(pointer(a[0]),*inputGuid(a[1]),static_cast<void **>(pointer(a[2])),nullptr));capture();}
  U32 object=*static_cast<U32 *>(pointer(a[2]));if(static_cast<LONG>(r.value)>=0){if(!object||inputObjects.count(object))fatal(141);InputObject owned{kind};owned.parent=a[0];inputObjects.emplace(object,owned);r.extras=inputInfo(object);}else {if(object)++inputUnexpectedOutputs;r.extras="object="+number(object)+" kind="+number(kind);}return r;
 }
 if(q.op=="INPUT_FORMAT"){
  if(!args(2)||!inputHas(a[0])||inputObjects.at(a[0]).kind==20)return reject("OWNED_INPUT_DATAFORMAT");auto &p=inputObjects.at(a[0]);
  const InputDataFormat *format=p.kind==21?&inputKeyboardFormat:&inputMouseFormat;
  if(a[1]!=(p.kind==21?0x5cac3cu:0x5cae44u)||p.acquired)return reject("EXACT_ORIGINAL_DATAFORMAT_TABLE");
  using F=HRESULT(STDMETHODCALLTYPE *)(void *,const InputDataFormat *);
  {GameCallScope c(guard,q.id);begin();r.value=static_cast<U32>(reinterpret_cast<F>(gameMethod(a[0],11))(pointer(a[0]),format));capture();}
  if(static_cast<LONG>(r.value)>=0)p.format=true;r.extras="format_guest="+number(a[1])+" object_count="+number(format->count)+" data_bytes="+number(format->dataSize)+" exact_original_guid_relocation=1";return r;
 }
 if(q.op=="INPUT_COOPERATIVE"){
  if(!args(3)||!inputHas(a[0])||inputObjects.at(a[0]).kind==20||a[1]!=ptr(ownedWindow)||a[2]!=6||!IsWindow(ownedWindow))return reject("ORIGINAL_FOREGROUND_NONEXCLUSIVE6");
  using F=HRESULT(STDMETHODCALLTYPE *)(void *,HWND,DWORD);
  {GameCallScope c(guard,q.id);begin();r.value=static_cast<U32>(reinterpret_cast<F>(gameMethod(a[0],13))(pointer(a[0]),ownedWindow,6));capture();}
  if(static_cast<LONG>(r.value)>=0)inputObjects.at(a[0]).cooperative=true;r.extras="hwnd="+number(a[1])+" flags=6 window_alive=1";return r;
 }
 if(q.op=="INPUT_PROPERTY"||q.op=="INPUT_DEVICE_INFO"){
  bool property=q.op=="INPUT_PROPERTY";if(!args(property?3:2)||!inputHas(a[0],22)||!windowRange(a.back(),property?20:580))return reject("ORIGINAL_MOUSE_PROPERTY_OR_INSTANCE");
  if(property){const U32 expected[]={20,16,0,0,1};if(a[1]!=2||memcmp(pointer(a[2]),expected,20))return reject("ORIGINAL_AXISMODE_RELATIVE_PROPERTY");
   using F=HRESULT(STDMETHODCALLTYPE *)(void *,const GUID *,void *);GameCallScope c(guard,q.id);begin();r.value=static_cast<U32>(reinterpret_cast<F>(gameMethod(a[0],6))(pointer(a[0]),reinterpret_cast<const GUID *>(2),pointer(a[2])));capture();}
  else {if(*static_cast<U32 *>(pointer(a[1]))!=580)return reject("ORIGINAL_DEVICEINSTANCEA580");using F=HRESULT(STDMETHODCALLTYPE *)(void *,void *);GameCallScope c(guard,q.id);begin();r.value=static_cast<U32>(reinterpret_cast<F>(gameMethod(a[0],15))(pointer(a[0]),pointer(a[1])));capture();}return r;
 }
 if(q.op=="INPUT_ACQUIRE"||q.op=="INPUT_UNACQUIRE"){
  bool acquire=q.op=="INPUT_ACQUIRE";if(!args(1)||!inputHas(a[0])||inputObjects.at(a[0]).kind==20||!ownedWindow||!IsWindow(ownedWindow))return reject("INPUT_DEVICE_CURRENT_LIVE_WINDOW");auto &p=inputObjects.at(a[0]);
  if(acquire&&(!p.format||!p.cooperative||!inputSafe()))return reject("INPUT_ORIGINAL_FOREGROUND_ACQUIRE_PRECONDITIONS");
  using F=HRESULT(STDMETHODCALLTYPE *)(void *);{GameCallScope c(guard,q.id);begin();r.value=static_cast<U32>(reinterpret_cast<F>(gameMethod(a[0],acquire?7:8))(pointer(a[0])));capture();}
  if(static_cast<LONG>(r.value)>=0){p.acquired=acquire;p.unacquired=!acquire;}if(!acquire)++inputUnacquires;
  r.extras="object="+number(a[0])+" acquired="+number(p.acquired)+" unacquired="+number(p.unacquired)+" hwnd="+number(ptr(ownedWindow))+" window_alive=1";return r;
 }
 if(q.op=="INPUT_RELEASE"){
  if(!args(1)||!inputHas(a[0])||!ownedWindow||!IsWindow(ownedWindow))return reject("INPUT_RELEASE_BEFORE_WINDOW");auto &p=inputObjects.at(a[0]);
  if((p.kind!=20&&(!p.unacquired||p.acquired))||(p.kind==20&&inputObjects.size()!=1))return reject("UNACQUIRE_DEVICES_THEN_RELEASE_FACTORY");
  using F=ULONG(STDMETHODCALLTYPE *)(void *);{GameCallScope c(guard,q.id);begin();r.value=reinterpret_cast<F>(gameMethod(a[0],2))(pointer(a[0]));capture();}
  p.refs=0;++inputReleases;if(r.value==0)inputObjects.erase(a[0]);
  r.extras="object="+number(a[0])+" remaining_owned_refs=0 native_remaining_refs="+number(r.value)+" window_alive=1 hwnd="+number(ptr(ownedWindow));return r;
 }
 if(q.op=="INPUT_CLIENT_TO_SCREEN"){
  if(!args(2)||a[0]!=ptr(ownedWindow)||!windowRange(a[1],8))return reject("OWNED_WINDOW_POINT8");
  POINT *point=static_cast<POINT *>(pointer(a[1]));if(point->x!=512||point->y!=384||inputPositionChanged)return reject("ORIGINAL_FULLSCREEN_INPUT_CENTER");
  begin();r.value=ClientToScreen(ownedWindow,point);capture();if(r.value){inputConvertedPoint=*point;inputConvertedPointValid=true;}return r;
 }
 if(q.op=="INPUT_CURSOR_POS"||q.op=="INPUT_SHOW_CURSOR"){
  bool show=q.op=="INPUT_SHOW_CURSOR";if(!args(show?1:2)||!inputSafe()||(show&&(a[0]>1||inputShowCalls>=8)))return reject("BOUNDED_ORIGINAL_CURSOR_WITHOUT_NEW_USER_INPUT");
  if(!show&&(!inputConvertedPointValid||a[0]!=static_cast<U32>(inputConvertedPoint.x)||a[1]!=static_cast<U32>(inputConvertedPoint.y)))return reject("EXACT_ORIGINAL_CLIENT_TO_SCREEN_OUTPUT");
  InputCursorSnapshot before{};if(!inputReadCursor(before))return reject("CURSOR_PRECALL_READ_FAILED");begin();
  inputCursorRestored=false;
  if(show){LONG count=ShowCursor(a[0]!=0);r.value=static_cast<U32>(count);LONG delta=a[0]?1:-1;if(!inputCountKnown){inputInitialCount=count-delta;inputCountKnown=true;}inputLastCount=count;inputShowDelta+=delta;++inputShowCalls;}
  else {r.value=SetCursorPos(static_cast<int>(a[0]),static_cast<int>(a[1]));if(r.value)inputPositionChanged=true;inputConvertedPointValid=false;}capture();
  if(!inputReadCursor(inputLast))return reject("CURSOR_POSTCALL_READ_FAILED",r.error);
  r.extras="before_hex="+encodeHex(&before,36)+" after_hex="+encodeHex(&inputLast,36)+" show_delta_bits="+number(static_cast<U32>(inputShowDelta))+" show_count_bits="+number(static_cast<U32>(inputLastCount));return r;
 }
 if(q.op=="INPUT_METRIC"||q.op=="INPUT_DOUBLE_CLICK"){
  bool metric=q.op=="INPUT_METRIC";if(!args(metric?1:0)||(metric&&a[0]!=36&&a[0]!=37&&a[0]!=68&&a[0]!=69))return reject("ORIGINAL_MOUSE_SETTINGS_ONLY");
  begin();r.value=metric?static_cast<U32>(GetSystemMetrics(static_cast<int>(a[0]))):GetDoubleClickTime();capture();return r;
 }
 if(q.op=="INPUT_CURSOR_RESTORE"){
  if(!args(0)||!inputObjects.empty()||!inputSafe())return reject("CURSOR_RESTORE_AFTER_INPUT_RELEASE_SAME_USER");
  InputCursorSnapshot now{};if(!inputReadCursor(now)||now.lastInput!=inputOriginal.lastInput||
    now.left!=inputOriginal.left||now.top!=inputOriginal.top||now.right!=inputOriginal.right||now.bottom!=inputOriginal.bottom||
    now.x!=(inputPositionChanged?inputLast.x:inputOriginal.x)||now.y!=(inputPositionChanged?inputLast.y:inputOriginal.y)||
    now.cursor!=inputLast.cursor||now.flags!=inputLast.flags)return reject("UNOWNED_CURSOR_OR_CLIP_CHANGE");
  while(inputShowDelta){if(inputShowCalls>=16||!inputSafe())return reject("CURSOR_BALANCE_BUDGET_OR_NEW_INPUT");bool show=inputShowDelta<0;begin();inputLastCount=ShowCursor(show);capture();inputShowDelta+=show?1:-1;++inputShowCalls;}
  if(inputPositionChanged){if(!inputSafe())return reject("NEW_INPUT_BEFORE_POSITION_RESTORE");begin();r.value=SetCursorPos(inputOriginal.x,inputOriginal.y);capture();if(!r.value)return r;}
  if(!inputReadCursor(now))return reject("FINAL_CURSOR_READ_FAILED");
  bool equal=memcmp(&now,&inputOriginal,36)==0&&(!inputCountKnown||inputLastCount==inputInitialCount);
  inputCursorRestored=equal;if(equal)inputPositionChanged=false;r.value=equal;r.extras="cursor_hex="+encodeHex(&now,36)+" show_delta_bits="+number(static_cast<U32>(inputShowDelta))+" show_count_bits="+number(static_cast<U32>(inputLastCount))+" initial_show_count_bits="+number(static_cast<U32>(inputInitialCount))+" actual_readback=1";return r;
 }
 if(q.op=="INPUT_CLOSE"){
  if(!args(0)||!inputObjects.empty()||inputShowDelta||inputPositionChanged||!inputCursorRestored||inputUnexpectedOutputs)return reject("INPUT_RESTORE_BEFORE_CLOSE");
  if(inputModule){GameCallScope c(guard,q.id);begin();r.value=FreeLibrary(inputModule);capture();if(!r.value)return r;inputModule=nullptr;}
  inputBaseline=false;inputInstance=false;r.value=1;r.extras=inputStatus();return r;
 }
 return reject("INPUT_OPERATION_NOT_ADMITTED");
}
Result inputDispatch(const Request &q,std::unique_lock<std::mutex> &guard,U32 savedError){
 bool bound=inputBaseline;const auto token=gfxBaselineToken;Result r=inputDispatchImpl(q,guard,savedError);
 if(bound||inputBaseline)r.extras+=" baseline_token_hex="+encodeHex(token.data(),32)+" owner_hwnd="+number(ptr(ownedWindow));
 return r;
}
