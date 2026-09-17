
void __thiscall FUN__text__00424e70(undefined4 *param_1,undefined4 param_2,undefined4 param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [14];
  undefined4 uStack_14;
  undefined4 local_c;
  undefined4 *local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  *param_1 = param_2;
  local_8 = param_1;
  (*API_USER32_DLL_SetPropA)(*param_1,"sys_win_prop",param_3);
  local_c = FUN__text__0056ce80();
  uStack_14 = 0x424ec6;
  FUN__text__0056ce80();
  return;
}

