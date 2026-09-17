
undefined4 FUN__text__00578130(undefined4 param_1,uint param_2)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 uStack_30;
  int iStack_2c;
  undefined4 uStack_28;
  int local_24;
  undefined4 local_20;
  void *pvStack_14;
  undefined1 *puStack_10;
  undefined *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &DAT_005fa268;
  puStack_10 = &LAB__text__00576b9c;
  pvStack_14 = ExceptionList;
  if (param_2 < 0xffffffe1) {
    if (DAT_0080ab2c == 3) {
      ExceptionList = &pvStack_14;
      FUN__text__00577040(9);
      local_8 = 0;
      local_24 = FUN__text__00578c00(param_1);
      if ((local_24 != 0) && (local_20 = 0, param_2 <= DAT_0080ab4c)) {
        iVar2 = FUN__text__00579ae0(local_24,param_1,param_2);
        if (iVar2 != 0) {
          local_20 = param_1;
        }
      }
      local_8 = 0xffffffff;
      FUN__text__005781d1();
      uVar1 = FUN__text__005781dc();
      return uVar1;
    }
    if (DAT_0080ab2c == 2) {
      if (param_2 == 0) {
        param_2 = 1;
      }
      ExceptionList = &pvStack_14;
      FUN__text__00577040(9);
      local_8 = 1;
      iStack_2c = FUN__text__0057ac20(param_1,&uStack_30,&uStack_28);
      if (iStack_2c == 0) {
        local_8 = 0xffffffff;
        FUN__text__005782ca();
        uVar1 = FUN__text__005782d5();
        return uVar1;
      }
      local_20 = 0;
      if ((param_2 + 0xf & 0xfffffff0) <= DAT_0076415c) {
        iVar2 = FUN__text__0057b390(uStack_30,uStack_28,iStack_2c,param_2 + 0xf >> 4);
        if (iVar2 != 0) {
          local_20 = param_1;
        }
      }
      uVar1 = local_20;
      __local_unwind2(&pvStack_14,0xffffffff);
    }
    else {
      if (param_2 == 0) {
        param_2 = 1;
      }
      ExceptionList = &pvStack_14;
      uVar1 = (*API_NTDLL_DLL_RtlReAllocateHeap)
                        (DAT_0080ab28,0x10,param_1,param_2 + 0xf & 0xfffffff0);
    }
  }
  else {
    uVar1 = 0;
  }
  ExceptionList = pvStack_14;
  return uVar1;
}

