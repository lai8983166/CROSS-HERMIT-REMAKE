
void wndproc_2(undefined4 param_1,int param_2,undefined4 param_3,undefined4 *param_4)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 auStack_50 [12];
  undefined *puStack_20;
  undefined4 uStack_10;
  undefined4 *puStack_c;
  undefined4 *puStack_8;
  
  puVar2 = auStack_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  (*API_USER32_DLL_GetPropA)(param_1,"CPP_CLASS");
  puStack_8 = (undefined4 *)__chkesp();
  if (puStack_8 == (undefined4 *)0x0) {
    if ((param_2 == 1) || (param_2 == 0x81)) {
      puStack_c = param_4;
      puStack_8 = (undefined4 *)*param_4;
    }
    else if (param_2 == 0x110) {
      puStack_8 = param_4;
    }
    if (puStack_8 != (undefined4 *)0x0) {
      func_0x00424730(param_1,0);
    }
  }
  if (puStack_8 == (undefined4 *)0x0) {
    (*API_USER32_DLL_GetWindowLongA)(param_1,4);
    iVar1 = __chkesp();
    if (iVar1 == 0) {
      (*API_NTDLL_DLL_NtdllDefWindowProc_A)(param_1,param_2,param_3,param_4);
      __chkesp();
    }
  }
  else {
    (**(code **)*puStack_8)(param_1,param_2,param_3,param_4);
    uStack_10 = __chkesp();
    if (param_2 == 2) {
      func_0x004248e0();
    }
  }
  puStack_20 = &UNK_00424a83;
  __chkesp();
  return;
}

