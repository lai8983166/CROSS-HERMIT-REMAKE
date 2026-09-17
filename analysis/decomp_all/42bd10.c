
void __thiscall FUN__text__0042bd10(undefined4 *param_1,undefined4 param_2,undefined4 param_3)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_48 [12];
  undefined4 uStack_18;
  undefined4 *local_8;
  
  puVar3 = local_48;
  for (iVar2 = 0x11; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  param_1[2] = param_2;
  param_1[3] = param_3;
  local_8 = param_1;
  (*API_USER32_DLL_SetWindowsHookExA)(7,param_1[4],*param_1,0);
  uVar1 = FUN__text__0056ce80();
  local_8[1] = uVar1;
  uStack_18 = 0x42bd84;
  FUN__text__0056ce80();
  return;
}

