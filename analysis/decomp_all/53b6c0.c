
undefined4 __thiscall FUN__text__0053b6c0(int *param_1,undefined4 *param_2,int param_3)

{
  code *pcVar1;
  int iVar2;
  undefined4 uStack_c8;
  undefined1 *puStack_c4;
  undefined1 *puStack_c0;
  undefined4 uStack_bc;
  undefined4 uStack_b8;
  undefined4 uStack_b4;
  undefined4 uStack_b0;
  undefined4 *puStack_ac;
  undefined4 local_9c [4];
  int local_8c;
  undefined4 local_8;
  
  if (param_2 == (undefined4 *)0x0) {
    return 0x8876086c;
  }
  if (param_3 != 0) {
    puStack_ac = local_9c;
    local_9c[0] = 0x94;
    uStack_b0 = 0x53b6f7;
    (*API_KERNEL32_DLL_GetVersionExA)();
    pcVar1 = API_KERNEL32_DLL_WideCharToMultiByte;
    if (local_8c != 2) {
      puStack_ac = (undefined4 *)0x0;
      uStack_b0 = 0;
      uStack_b4 = 0;
      uStack_b8 = 0;
      uStack_bc = 0xffffffff;
      puStack_c0 = (undefined1 *)param_2;
      puStack_c4 = (undefined1 *)0x0;
      uStack_c8 = 0;
      local_8 = (*API_KERNEL32_DLL_WideCharToMultiByte)();
      FUN__text__0056e230();
      (*pcVar1)(0,0,param_2,0xffffffff,&uStack_c8,local_8,0,0);
      param_3 = 0;
      param_2 = &uStack_c8;
    }
    if (param_3 != 0) {
      puStack_ac = (undefined4 *)0x0;
      uStack_b0 = 0x10000000;
      uStack_b4 = 3;
      uStack_b8 = 0;
      uStack_bc = 1;
      puStack_c0 = (undefined1 *)0x80000000;
      puStack_c4 = (undefined1 *)param_2;
      uStack_c8 = 0x53b759;
      iVar2 = (*DAT_005922b0)();
      goto LAB__text__0053b774;
    }
  }
  puStack_ac = (undefined4 *)0x0;
  uStack_b0 = 0x10000000;
  uStack_b4 = 3;
  uStack_b8 = 0;
  uStack_bc = 1;
  puStack_c0 = (undefined1 *)0x80000000;
  puStack_c4 = (undefined1 *)param_2;
  uStack_c8 = 0x53b774;
  iVar2 = (*DAT_005921ec)();
LAB__text__0053b774:
  *param_1 = iVar2;
  if (iVar2 != -1) {
    uStack_c8 = 0;
    iVar2 = (*DAT_005922b4)(iVar2,0,2,0,0);
    param_1[1] = iVar2;
    if (iVar2 != -1) {
      uStack_c8 = 0;
      iVar2 = (*DAT_005922b8)(iVar2,4,0,0);
      param_1[2] = iVar2;
      if (iVar2 != 0) {
        uStack_c8 = 0;
        iVar2 = (*DAT_005921f0)(*param_1);
        param_1[3] = iVar2;
        if (iVar2 != -1) {
          return 0;
        }
      }
    }
  }
  uStack_c8 = 0x53b7ba;
  (*API_KERNEL32_DLL_GetLastError)();
  return 0x88760b59;
}

