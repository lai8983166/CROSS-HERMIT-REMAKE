
undefined4 __thiscall FUN__text__0053b7d0(int *param_1,undefined1 *param_2,int param_3)

{
  code *pcVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 *puVar4;
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
  int *local_8;
  
  if (param_2 == (undefined1 *)0x0) {
    return 0x8876086c;
  }
  puVar4 = (undefined4 *)param_2;
  local_8 = param_1;
  if (param_3 != 0) {
    puStack_ac = local_9c;
    local_9c[0] = 0x94;
    uStack_b0 = 0x53b80c;
    (*API_KERNEL32_DLL_GetVersionExA)();
    pcVar1 = API_KERNEL32_DLL_WideCharToMultiByte;
    if (local_8c != 2) {
      puStack_ac = (undefined4 *)0x0;
      uStack_b0 = 0;
      uStack_b4 = 0;
      uStack_b8 = 0;
      uStack_bc = 0xffffffff;
      puStack_c0 = param_2;
      puStack_c4 = (undefined1 *)0x0;
      uStack_c8 = 0;
      puVar4 = &uStack_c8;
      uVar2 = (*API_KERNEL32_DLL_WideCharToMultiByte)();
      FUN__text__0056e230();
      (*pcVar1)(0,0,param_2,0xffffffff,&uStack_c8,uVar2,0,0);
      param_3 = 0;
      param_1 = local_8;
    }
    if (param_3 != 0) {
      puStack_ac = (undefined4 *)0x0;
      uStack_b0 = 0;
      uStack_b4 = 2;
      uStack_b8 = 0;
      uStack_bc = 0;
      puStack_c0 = (undefined1 *)0x40000000;
      uStack_c8 = 0x53b863;
      puStack_c4 = (undefined1 *)puVar4;
      iVar3 = (*DAT_005922b0)();
      goto LAB__text__0053b877;
    }
  }
  puStack_ac = (undefined4 *)0x0;
  uStack_b0 = 0;
  uStack_b4 = 2;
  uStack_b8 = 0;
  uStack_bc = 0;
  puStack_c0 = (undefined1 *)0x40000000;
  uStack_c8 = 0x53b877;
  puStack_c4 = (undefined1 *)puVar4;
  iVar3 = (*DAT_005921ec)();
LAB__text__0053b877:
  *param_1 = iVar3;
  if (iVar3 == -1) {
    uStack_c8 = 0x53b884;
    (*API_KERNEL32_DLL_GetLastError)();
    uVar2 = 0x88760b59;
  }
  else {
    uVar2 = 0;
  }
  return uVar2;
}

