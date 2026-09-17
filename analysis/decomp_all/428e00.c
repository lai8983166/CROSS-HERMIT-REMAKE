
void __fastcall FUN_00428e00(int *param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  int local_c;
  int *local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*param_1 != 0) {
    local_8 = param_1;
    (*API_ADVAPI32_DLL_RegCloseKey)(*param_1);
    local_c = __chkesp();
    if (local_c == 0) {
      *local_8 = 0;
    }
    else {
      FUN_004292e0(local_c);
    }
  }
  local_8 = (int *)0x428e6e;
  __chkesp();
  return;
}

