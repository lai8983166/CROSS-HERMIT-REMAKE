
int __thiscall FUN__text__00584900(undefined4 param_1,int param_2)

{
  bool bVar1;
  uint uVar2;
  
  if (DAT_0080a62c == 0) {
    if ((0x40 < param_2) && (param_2 < 0x5b)) {
      param_2 = param_2 + 0x20;
    }
  }
  else {
    (*API_KERNEL32_DLL_InterlockedIncrement)(&DAT_0080bb6c,param_1);
    bVar1 = DAT_0080bb68 != 0;
    if (bVar1) {
      (*API_KERNEL32_DLL_InterlockedDecrement)(&DAT_0080bb6c);
      FUN__text__00577040(0x13);
    }
    uVar2 = (uint)bVar1;
    param_2 = FUN__text__005849a0(param_2);
    if (uVar2 == 0) {
      (*API_KERNEL32_DLL_InterlockedDecrement)(&DAT_0080bb6c);
    }
    else {
      FUN__text__005770e0(0x13);
    }
  }
  return param_2;
}

