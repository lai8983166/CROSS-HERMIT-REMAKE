
undefined4
FUN__text__0058d3a0(undefined4 param_1,undefined4 param_2,undefined4 param_3,int param_4,int param_5
                   )

{
  int iVar1;
  undefined4 uVar2;
  undefined4 uStack_48;
  undefined4 uStack_44;
  undefined4 uStack_40;
  int iStack_3c;
  void *local_14;
  undefined1 *puStack_10;
  undefined *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &DAT_005fb080;
  puStack_10 = &LAB__text__00576b9c;
  local_14 = ExceptionList;
  ExceptionList = &local_14;
  if (DAT_0080a794 == 0) {
    iStack_3c = 0;
    uStack_40 = 0;
    uStack_44 = 1;
    uStack_48 = 0;
    ExceptionList = &local_14;
    iVar1 = (*API_KERNEL32_DLL_GetLocaleInfoW)();
    if (iVar1 == 0) {
      iStack_3c = 0;
      uStack_40 = 0;
      uStack_44 = 1;
      uStack_48 = 0;
      iVar1 = (*API_KERNEL32_DLL_GetLocaleInfoA)();
      if (iVar1 == 0) {
        ExceptionList = local_14;
        return 0;
      }
      DAT_0080a794 = 2;
    }
    else {
      DAT_0080a794 = 1;
    }
  }
  if (DAT_0080a794 == 2) {
    iStack_3c = param_4;
    uStack_40 = param_3;
    uStack_44 = param_2;
    uStack_48 = param_1;
    uVar2 = (*API_KERNEL32_DLL_GetLocaleInfoA)();
  }
  else if (DAT_0080a794 == 1) {
    if (param_5 == 0) {
      param_5 = DAT_0080a63c;
    }
    iStack_3c = 0;
    uStack_40 = 0;
    uStack_44 = param_2;
    uStack_48 = param_1;
    iVar1 = (*API_KERNEL32_DLL_GetLocaleInfoW)();
    if (iVar1 == 0) {
      uVar2 = 0;
    }
    else {
      local_8 = 0;
      FUN__text__0056e230();
      local_8 = 0xffffffff;
      if (&stack0x00000000 == (undefined1 *)0x48) {
        uVar2 = 0;
      }
      else {
        iVar1 = (*API_KERNEL32_DLL_GetLocaleInfoW)(param_1,param_2,&uStack_48,iVar1);
        if (iVar1 == 0) {
          uVar2 = 0;
        }
        else if (param_4 == 0) {
          uVar2 = (*API_KERNEL32_DLL_WideCharToMultiByte)
                            (param_5,0x220,&uStack_48,0xffffffff,0,0,0,0);
        }
        else {
          uVar2 = (*API_KERNEL32_DLL_WideCharToMultiByte)
                            (param_5,0x220,&uStack_48,0xffffffff,param_3,param_4,0,0);
        }
      }
    }
  }
  else {
    uVar2 = 0;
  }
  ExceptionList = local_14;
  return uVar2;
}

