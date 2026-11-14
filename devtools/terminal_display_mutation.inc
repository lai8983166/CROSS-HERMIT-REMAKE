// Reached the validated leaf boundary, before its actual call. This is neither
// an HRESULT nor a promise that a pending native call completed.
std::map<U32,std::string> displayMutationReceipts;
U32 displayMutationSequence=0;
void displayMutationBegin(const Request &q,U32 savedError,const char *kind,const void *data,U32 size){
 if(q.lane||GetCurrentThreadId()!=lanes[0].tid||__readfsdword(0x18)!=lanes[0].teb||!ownedWindow||!gfxBaseline||tlsSlots.size()!=1||size>1536||(++displayMutationSequence)>32||displayMutationReceipts.count(q.id))fatal(151);
 U32 slot=tlsSlots.begin()->first,ptd=tlsSlots.begin()->second.values[0];SetLastError(0);U32 actual=ptr(TlsGetValue(slot)),error=GetLastError();SetLastError(savedError);
 if(!ptd||actual!=ptd||error||!windowRange(ptd,116))fatal(152);
 TexturePreserve preserve(slot,ptd,savedError);
 std::string message="E NATIVE_MUTATION_BEGIN request_id="+number(q.id)+" op="+q.op+" lane=0 tid="+number(lanes[0].tid)+" teb="+number(lanes[0].teb)+" pid="+number(GetCurrentProcessId())+
  " baseline_token_hex="+encodeHex(gfxBaselineToken.data(),32)+" window_generation="+number(displayWindowGeneration)+" owned_hwnd="+number(ptr(ownedWindow))+" mutation_sequence="+number(displayMutationSequence)+
  " data_kind="+kind+" data_bytes="+number(size)+" data_hex="+(size?encodeHex(data,size):std::string("-"))+" argc="+number(static_cast<U32>(q.args.size()))+
  " original_last_error="+number(savedError)+" tls_slot="+number(slot)+" tls_value="+number(ptd)+" ptd_before_hex="+encodeHex(preserve.bytes.data(),116);
 for(size_t i=0;i<q.args.size();++i)message+=" arg"+number(static_cast<U32>(i))+"="+q.args[i];
 if(!preserve.restore())fatal(153);emit(message);
 const std::string observed=encodeHex(pointer(ptd),116);if(!preserve.restore())fatal(154);const U32 restoredError=GetLastError();
 displayMutationReceipts.emplace(q.id," mutation_emission_restored=1 mutation_original_last_error="+number(savedError)+" mutation_restored_last_error="+number(restoredError)+" mutation_ptd_before_hex="+encodeHex(preserve.bytes.data(),116)+" mutation_ptd_observed_hex="+observed+" mutation_ptd_restored_hex="+encodeHex(pointer(ptd),116));
 // Allocation/encoding above is also infrastructure, so restore once more.
 if(!preserve.restore())fatal(155);
}
std::string displayMutationReceipt(U32 id){
 auto found=displayMutationReceipts.find(id);if(found==displayMutationReceipts.end())return std::string();
 std::string value=found->second;displayMutationReceipts.erase(found);return value;
}
