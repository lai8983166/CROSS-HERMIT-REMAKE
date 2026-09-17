
void FUN__text__0042a1a0(int *param_1,undefined4 param_2,undefined4 param_3)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_64 [16];
  int local_24;
  int local_20;
  int local_1c;
  int local_18;
  int local_14;
  int local_10;
  
  puVar3 = local_64;
  for (iVar2 = 0x18; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  (*API_USER32_DLL_GetWindowRect)(param_2,&local_14);
  FUN__text__0056ce80();
  (*API_USER32_DLL_GetDlgItem)(param_2,param_3,&local_24);
  uVar1 = FUN__text__0056ce80();
  (*API_USER32_DLL_GetWindowRect)(uVar1);
  FUN__text__0056ce80();
  *param_1 = local_24 - local_14;
  param_1[2] = local_1c - local_14;
  param_1[1] = local_20 - local_10;
  param_1[3] = local_18 - local_10;
  local_20 = 0x42a236;
  FUN__text__0056ce80();
  return;
}

