
void FUN__text__00423ad0(undefined4 param_1,undefined4 param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [14];
  undefined4 uStack_1c;
  int local_14;
  undefined4 local_10;
  undefined4 local_c;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  (*API_USER32_DLL_GetWindowLongA)(param_1,0xfffffff0);
  local_c = FUN__text__0056ce80();
  (*API_USER32_DLL_SetWindowLongA)(param_1,0xfffffff0,param_2);
  local_14 = FUN__text__0056ce80();
  if (local_14 == 0) {
    local_14 = 0;
  }
  else {
    (*API_USER32_DLL_GetWindowLongA)(param_1,0xfffffff0);
    local_10 = FUN__text__0056ce80();
    (*API_USER32_DLL_SetWindowPos)(param_1,0,0,0,0,0,0x67);
    local_14 = FUN__text__0056ce80();
    if (local_14 != 0) {
      (*API_USER32_DLL_ShowWindow)(param_1,1);
      FUN__text__0056ce80();
    }
  }
  uStack_1c = 0x423b99;
  FUN__text__0056ce80();
  return;
}

