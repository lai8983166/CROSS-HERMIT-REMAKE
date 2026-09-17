
void FUN__text__004239f0(undefined4 param_1,undefined4 param_2,undefined4 param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [10];
  undefined4 uStack_24;
  undefined4 local_c;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  (*API_USER32_DLL_SetWindowPos)(param_1,0,param_2,param_3,0,0,5);
  local_c = FUN__text__0056ce80();
  uStack_24 = 0x423a4f;
  FUN__text__0056ce80();
  return;
}

