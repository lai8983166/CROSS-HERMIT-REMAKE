
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN__text__00412290(undefined4 *param_1)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_58 [16];
  uint local_18;
  undefined4 uStack_14;
  double local_10;
  
  puVar3 = local_58;
  for (iVar2 = 0x15; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  _memset(param_1,0,0x14);
  (*API_USER32_DLL_GetSystemMetrics)(0x24);
  uVar1 = FUN__text__0056ce80();
  *param_1 = uVar1;
  (*API_USER32_DLL_GetSystemMetrics)(0x25);
  uVar1 = FUN__text__0056ce80();
  param_1[1] = uVar1;
  (*API_USER32_DLL_GetDoubleClickTime)();
  local_18 = FUN__text__0056ce80();
  uStack_14 = 0;
  local_10 = (double)local_18 / _DAT_00592c50;
  if (local_10 < _DAT_00592c48) {
    local_10 = 10.0;
  }
  uVar1 = __ftol();
  param_1[2] = uVar1;
  (*API_USER32_DLL_GetSystemMetrics)(0x44);
  uVar1 = FUN__text__0056ce80();
  param_1[3] = uVar1;
  (*API_USER32_DLL_GetSystemMetrics)(0x45);
  uVar1 = FUN__text__0056ce80();
  param_1[4] = uVar1;
  local_18 = 0x41237b;
  FUN__text__0056ce80();
  return;
}

