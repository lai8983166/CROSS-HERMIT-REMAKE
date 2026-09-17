
undefined4 FUN__text__00589020(undefined4 param_1,undefined4 param_2,undefined4 param_3)

{
  undefined4 uVar1;
  bool bVar2;
  
  (*API_KERNEL32_DLL_InterlockedIncrement)(&DAT_0080bb6c);
  bVar2 = DAT_0080bb68 == 0;
  if (!bVar2) {
    (*API_KERNEL32_DLL_InterlockedDecrement)(&DAT_0080bb6c);
    FUN__text__00577040(0x13);
  }
  uVar1 = FUN__text__005890a0(param_1,param_2,param_3);
  if (bVar2) {
    (*API_KERNEL32_DLL_InterlockedDecrement)(&DAT_0080bb6c);
  }
  else {
    FUN__text__005770e0(0x13);
  }
  return uVar1;
}

