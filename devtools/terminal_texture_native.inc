// A separate readonly lock after the original successful writable UnlockRect.
// No old lock pointer is read, and no implicit unlock success is manufactured.
std::string textureStatus() {
 U32 pending=0;for(const auto &x:gfxObjects)pending+=x.second.verifyPending;
 return "texture_verify_pending="+number(pending)+" texture_verify_failed="+number(textureFailed);
}
struct TexturePreserve {
 U32 slot,value,error;std::array<unsigned char,116> bytes{};
 TexturePreserve(U32 s,U32 v,U32 e):slot(s),value(v),error(e){memcpy(bytes.data(),pointer(value),116);}
 bool restore() {
  SetLastError(0);U32 current=ptr(TlsGetValue(slot));U32 observedError=GetLastError();
  if(current!=value||observedError||!windowRange(value,116))return false;
  memcpy(pointer(value),bytes.data(),116);SetLastError(error);
  return memcmp(pointer(value),bytes.data(),116)==0&&GetLastError()==error;
 }
 ~TexturePreserve(){if(!restore())fatal(133);}
};
Result textureVerify(const Request &q,std::unique_lock<std::mutex> &guard,U32 savedError) {
 Result r;r.error=savedError;std::vector<U32>a;
 if(!numeric(q,3,a)||q.lane||GetCurrentThreadId()!=lanes[0].tid||__readfsdword(0x18)!=lanes[0].teb||!windowCallbacks.empty()||textureFailed||!gfxGate||!gfxBaseline||!gfxHas(a[0],GfxTexture))return reject("CURRENT_MAIN_TEXTURE_VERIFICATION");
 auto &p=gfxObjects.at(a[0]);
 if(p.locked||!p.verifyPending||!a[1]||p.unlockedGeneration!=a[1]||p.generation!=a[1]||p.verifiedGeneration==a[1]||p.width!=256||p.height!=256||p.format!=26||!windowRange(a[2],131072)||tlsSlots.size()!=1)return reject("EXACT_UNLOCKED_TEXTURE_GENERATION");
 U32 slot=tlsSlots.begin()->first,ptd=tlsSlots.begin()->second.values[0];
 SetLastError(0);U32 actual=ptr(TlsGetValue(slot)),tlsError=GetLastError();SetLastError(savedError);
 if(!ptd||actual!=ptd||tlsError||!windowRange(ptd,116)||!gfxDisjoint(a[2],131072,ptd,116))return reject("CURRENT_MAIN_TEXTURE_PTD");
 TexturePreserve preserve(slot,ptd,savedError);
 U32 lockHR=UINT32_MAX,unlockHR=UINT32_MAX,lockError=0,unlockError=0,verifyGeneration=0;
 U32 rectangle[2]={0,0};bool locked=false,shape=false,copied=false,unlocked=false;
 U32 readRows=0,readBytes=0,readError=0,readFailedRow=UINT32_MAX;BOOL readOK=FALSE;
 using Lock=HRESULT(STDMETHODCALLTYPE *)(void *,UINT,void *,const RECT *,DWORD);
 using Unlock=HRESULT(STDMETHODCALLTYPE *)(void *,UINT);
 {
  GameCallScope call(guard,q.id);SetLastError(savedError);
  lockHR=static_cast<U32>(reinterpret_cast<Lock>(gameMethod(a[0],16))(pointer(a[0]),0,rectangle,nullptr,16));lockError=GetLastError();
 }
 if(static_cast<LONG>(lockHR)>=0){
  locked=true;p.locked=true;p.format=0x8000001a;p.pitch=rectangle[0];p.bits=rectangle[1];verifyGeneration=++textureGeneration;
  if(!verifyGeneration)fatal(134);
  shape=p.pitch>=512&&p.pitch<=1024&&p.bits&&static_cast<uint64_t>(p.bits)+p.pitch*256<=0x100000000ull;
  if(shape){
   for(U32 y=0;y<256;++y){
    SIZE_T actualBytes=0;SetLastError(0);
    readOK=ReadProcessMemory(GetCurrentProcess(),static_cast<unsigned char *>(pointer(p.bits))+y*p.pitch,static_cast<unsigned char *>(pointer(a[2]))+y*512,512,&actualBytes);readError=GetLastError();
    if(actualBytes>512)fatal(135);readBytes+=static_cast<U32>(actualBytes);
    if(!readOK||actualBytes!=512){readFailedRow=y;break;}++readRows;
   }
   copied=readRows==256&&readBytes==131072&&readOK;
  }
  // An invalid returned pitch still owes its actual readonly UnlockRect.
  {GameCallScope call(guard,q.id);SetLastError(lockError);unlockHR=static_cast<U32>(reinterpret_cast<Unlock>(gameMethod(a[0],17))(pointer(a[0]),0));unlockError=GetLastError();}
  unlocked=static_cast<LONG>(unlockHR)>=0;
  if(unlocked){p.locked=false;p.bits=0;p.format=26;}
 }
 const std::string observedPTD=encodeHex(pointer(ptd),116);
 bool restored=preserve.restore();U32 restoredError=GetLastError();
 r.value=locked&&shape&&copied&&unlocked&&restored;
 if(r.value){p.verifiedGeneration=a[1];p.verifyPending=false;}else textureFailed=true;
 r.extras="source_generation="+number(a[1])+" verify_generation="+number(verifyGeneration)+" readonly_flags=16 level=0 logical_row_bytes=512 rows=256 logical_bytes=131072"+
  " pitch="+number(rectangle[0])+" bits="+number(rectangle[1])+" padding_bytes_per_row="+number(shape?rectangle[0]-512:0)+
  " lock_hresult="+number(lockHR)+" unlock_hresult="+number(unlockHR)+" lock_last_error="+number(lockError)+" unlock_last_error="+number(unlockError)+
  " readonly_lock_acquired="+number(locked)+" readonly_unlock_attempted="+number(locked)+" readonly_unlock_succeeded="+number(unlocked)+" geometry_valid="+number(shape)+" copied="+number(copied)+
  " read_process_memory_result="+number(static_cast<U32>(readOK))+" read_rows="+number(readRows)+" read_bytes="+number(readBytes)+" read_error="+number(readError)+" read_failed_row="+number(readFailedRow)+
  " pending="+number(p.verifyPending)+" original_last_error="+number(savedError)+" restored_last_error="+number(restoredError)+
  " tls_slot="+number(slot)+" tls_value="+number(ptd)+" ptd_before_hex="+encodeHex(preserve.bytes.data(),116)+" ptd_observed_hex="+observedPTD+" ptd_restored_hex="+encodeHex(pointer(ptd),116)+" state_restored="+number(restored);
 return r;
}
