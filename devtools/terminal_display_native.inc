// Supplemental read-only adapter binding, on the current original MAIN lane.
static_assert(sizeof(MONITORINFOEXW)==104 && sizeof(DISPLAY_DEVICEW)==840 && sizeof(DEVMODEW)==220,"fixed Win32 display ABI");
struct DisplayBlob {
 U32 header[16]{}; MONITORINFOEXW monitor{}; DISPLAY_DEVICEW adapter{};
 DISPLAY_DEVICEW monitors[16]{}; DEVMODEW mode{}; unsigned char gamma[1536]{};
};
static_assert(sizeof(DisplayBlob)==16204 && offsetof(DisplayBlob,mode)==14448 && offsetof(DisplayBlob,gamma)==14668,"bounded display blob layout");
bool displayBound=false,displayFailed=false;
U32 displayPhase=0,displaySequence=0,displayFactory=0,displayHWND=0,displayGeneration=0;
HDC displayDC=nullptr;
std::array<unsigned char,32> displayToken{};
std::array<wchar_t,32> displayDevice{};
std::string displayStatus(){return "display_bound="+number(displayBound)+" display_failed="+number(displayFailed)+" display_dc="+number(displayDC!=nullptr);}
std::string displayMetadata(){return "display_window_generation="+number(displayWindowGeneration)+" display_owner_hwnd="+number(displayHWND)+" display_pid="+number(GetCurrentProcessId())+" display_baseline_token_hex="+encodeHex(displayToken.data(),32);}
bool displayCurrent(){return displayBound&&!displayFailed&&!displayDC&&gfxBaseline&&displayToken==gfxBaselineToken&&displayFactory==gfxFactory&&displayHWND==ptr(ownedWindow)&&displayGeneration==displayWindowGeneration;}
Result displaySnapshot(const Request &q,std::unique_lock<std::mutex> &guard,U32 savedError){
 Result r;r.error=savedError;std::vector<U32>a;bool binding=q.op=="DISPLAY_BIND";
 if(!numeric(q,binding?3:2,a)||q.lane||GetCurrentThreadId()!=lanes[0].tid||__readfsdword(0x18)!=lanes[0].teb||!windowCallbacks.empty()||!gfxGate||!gfxBaseline||!ownedWindow||displayFailed||displayDC||tlsSlots.size()!=1)return reject("DISPLAY_CURRENT_MAIN_BASELINE");
 U32 phase=binding?0:a[0],out=a.back();
 if(!windowRange(out,sizeof(DisplayBlob))||!gfxHas(gfxFactory,GfxFactory)||
  (binding?(a[0]!=gfxFactory||a[1]||displayBound||gfxDevice||displaySequence):(phase<1||phase>2||!displayCurrent()||phase!=displayPhase+1||((phase==1)!=static_cast<bool>(gfxDevice))||(phase==2&&(!inputEmpty()||gfxGammaDirty)))))return reject("DISPLAY_EXACT_FACTORY_PHASE_OUTPUT");
 U32 slot=tlsSlots.begin()->first,ptd=tlsSlots.begin()->second.values[0];
 SetLastError(0);U32 actual=ptr(TlsGetValue(slot)),tlsError=GetLastError();SetLastError(savedError);
 if(!ptd||actual!=ptd||tlsError||!windowRange(ptd,116)||!gfxDisjoint(out,sizeof(DisplayBlob),ptd,116))return reject("DISPLAY_CURRENT_PTD");
 TexturePreserve preserve(slot,ptd,savedError);DisplayBlob b;U32 method=gameMethod(gfxFactory,14),count=0;
 U32 monitorError=0,adapterError=0,childError=0,modeError=0,dcError=0,gammaError=0,deleteError=0,methodError=0;
 bool adapterFound=false,adapterUnique=true,bounded=true,childBounded=true;HDC leftover=nullptr;HMONITOR monitor=nullptr;U32 createdDC=0;std::vector<U32> adapterResults,monitorResults;
 b.monitor.cbSize=sizeof(b.monitor);b.mode.dmSize=sizeof(b.mode);
 {
  GameCallScope call(guard,q.id);using F=HMONITOR(STDMETHODCALLTYPE *)(void *,UINT);
  SetLastError(savedError);monitor=reinterpret_cast<F>(method)(pointer(gfxFactory),0);methodError=GetLastError();
  if(monitor){SetLastError(0);b.header[10]=GetMonitorInfoW(monitor,reinterpret_cast<MONITORINFO *>(&b.monitor));monitorError=GetLastError();}
  if(b.header[10]&&b.monitor.szDevice[0]&&b.monitor.szDevice[31]==0){
   for(U32 i=0;i<=16;++i){DISPLAY_DEVICEW d{};d.cb=sizeof(d);SetLastError(0);BOOL ok=EnumDisplayDevicesW(nullptr,i,&d,1);adapterError=GetLastError();adapterResults.push_back(static_cast<U32>(ok));if(!ok)break;if(i==16){bounded=false;break;}
    if(!memcmp(d.DeviceName,b.monitor.szDevice,sizeof(d.DeviceName))){if(adapterFound)adapterUnique=false;b.adapter=d;adapterFound=true;}
   }
   for(U32 i=0;i<=16;++i){DISPLAY_DEVICEW d{};d.cb=sizeof(d);SetLastError(0);BOOL ok=EnumDisplayDevicesW(b.monitor.szDevice,i,&d,1);childError=GetLastError();monitorResults.push_back(static_cast<U32>(ok));if(!ok)break;if(i==16){childBounded=false;break;}b.monitors[count++]=d;}
   SetLastError(0);b.header[7]=EnumDisplaySettingsW(b.monitor.szDevice,ENUM_CURRENT_SETTINGS,&b.mode);modeError=GetLastError();
   SetLastError(0);HDC dc=CreateDCW(L"DISPLAY",b.monitor.szDevice,nullptr,nullptr);dcError=GetLastError();createdDC=ptr(dc);
   if(dc){SetLastError(0);b.header[8]=GetDeviceGammaRamp(dc,b.gamma);gammaError=GetLastError();SetLastError(0);b.header[9]=DeleteDC(dc);deleteError=GetLastError();if(!b.header[9])leftover=dc;}
  }
 }
 displayDC=leftover;b.header[11]=adapterFound&&adapterUnique&&bounded&&childBounded&&count&&(b.adapter.StateFlags&DISPLAY_DEVICE_ATTACHED_TO_DESKTOP)&&!(b.adapter.StateFlags&DISPLAY_DEVICE_MIRRORING_DRIVER);
 bool sameDevice=binding||!memcmp(displayDevice.data(),b.monitor.szDevice,sizeof(b.monitor.szDevice));
 bool valid=monitor&&b.header[10]&&b.header[11]&&b.header[7]&&b.header[8]&&b.header[9]&&b.mode.dmSize==220&&!b.mode.dmDriverExtra&&sameDevice;
 b.header[0]=0x31505344;b.header[1]=1;b.header[2]=phase;b.header[3]=gfxFactory;b.header[4]=0;b.header[5]=ptr(monitor);b.header[6]=count;b.header[12]=gfxDevice;b.header[13]=++displaySequence;b.header[14]=ptr(ownedWindow);b.header[15]=displayWindowGeneration;
 memcpy(pointer(out),&b,sizeof(b));const std::string observedPTD=encodeHex(pointer(ptd),116);bool restored=preserve.restore();const U32 restoredError=GetLastError();
 r.value=valid&&restored;if(r.value){displayPhase=phase;if(binding){displayBound=true;displayFactory=gfxFactory;displayHWND=ptr(ownedWindow);displayGeneration=displayWindowGeneration;displayToken=gfxBaselineToken;memcpy(displayDevice.data(),b.monitor.szDevice,sizeof(b.monitor.szDevice));}}else displayFailed=true;
 r.extras="phase="+number(phase)+" snapshot_sequence="+number(displaySequence)+" blob_bytes=16204 factory="+number(gfxFactory)+" adapter=0 adapter_monitor_method="+number(method)+" hmonitor="+number(ptr(monitor))+" monitor_count="+number(count)+" same_device="+number(sameDevice)+
  " get_adapter_monitor_error="+number(methodError)+" monitor_info_error="+number(monitorError)+" adapter_enum_error="+number(adapterError)+" monitor_enum_error="+number(childError)+" adapter_enum_results_hex="+(adapterResults.empty()?std::string("-"):encodeHex(adapterResults.data(),static_cast<U32>(adapterResults.size()*4)))+" monitor_enum_results_hex="+(monitorResults.empty()?std::string("-"):encodeHex(monitorResults.data(),static_cast<U32>(monitorResults.size()*4)))+" mode_error="+number(modeError)+" create_dc="+number(createdDC)+" create_dc_error="+number(dcError)+" gamma_error="+number(gammaError)+" delete_dc_error="+number(deleteError)+
  " original_last_error="+number(savedError)+" restored_last_error="+number(restoredError)+" tls_slot="+number(slot)+" tls_value="+number(ptd)+" ptd_before_hex="+encodeHex(preserve.bytes.data(),116)+" ptd_observed_hex="+observedPTD+" ptd_restored_hex="+encodeHex(pointer(ptd),116)+" state_restored="+number(restored)+" baseline_token_hex="+encodeHex(gfxBaselineToken.data(),32)+" "+displayMetadata()+" "+displayStatus();return r;
}
Result displayGraphics(const Request &q,std::unique_lock<std::mutex> &guard,U32 savedError){
 if(q.op=="GFX_CREATE_DEVICE"&&(!displayCurrent()||displayPhase!=0))return reject("D3D_DEVICE_REQUIRES_CURRENT_DISPLAY_BINDING");
 if(q.op=="GFX_BASELINE_CLEAR"&&(!displayBound||displayFailed||displayDC||displayPhase!=2||!gfxBaseline||displayToken!=gfxBaselineToken||displayHWND!=ptr(ownedWindow)||displayGeneration!=displayWindowGeneration))return reject("DISPLAY_POST_RELEASE_OBSERVATION_REQUIRED");
 Result r=gfxDispatch(q,guard,savedError);
 if(q.op=="GFX_BASELINE_CLEAR"&&r.ok&&r.value){displayBound=false;displayFactory=0;}
 if(displaySequence){if(r.extras.find("baseline_token_hex=")==std::string::npos)r.extras+=" baseline_token_hex="+encodeHex(displayToken.data(),32);r.extras+=" "+displayMetadata();}return r;
}
