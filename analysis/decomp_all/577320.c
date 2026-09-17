
void FUN__text__00577320(int param_1,int param_2)

{
  if (param_1 < 0x14) {
    FUN__text__005770e0(param_1 + 0x1c);
  }
  else {
    (*API_NTDLL_DLL_RtlLeaveCriticalSection)(param_2 + 0x20);
  }
  return;
}

