
void FUN__text__005772b0(int param_1,int param_2)

{
  if (param_1 < 0x14) {
    FUN__text__00577040(param_1 + 0x1c);
  }
  else {
    (*API_NTDLL_DLL_RtlEnterCriticalSection)(param_2 + 0x20);
  }
  return;
}

