
undefined4 FUN__text__0057b9d0(int param_1)

{
  undefined4 uVar1;
  int iVar2;
  
  DAT_0080ab28 = (*API_KERNEL32_DLL_HeapCreate)(param_1 == 0,0x1000,0);
  if (DAT_0080ab28 == 0) {
    uVar1 = 0;
  }
  else {
    DAT_0080ab2c = FUN__text__0057b7a0();
    if (DAT_0080ab2c == 3) {
      iVar2 = ___sbh_heap_init(0x3f8);
      if (iVar2 == 0) {
        (*API_KERNEL32_DLL_HeapDestroy)(DAT_0080ab28);
        return 0;
      }
    }
    else if ((DAT_0080ab2c == 2) && (iVar2 = FUN__text__0057a860(), iVar2 == 0)) {
      (*API_KERNEL32_DLL_HeapDestroy)(DAT_0080ab28);
      return 0;
    }
    uVar1 = 1;
  }
  return uVar1;
}

