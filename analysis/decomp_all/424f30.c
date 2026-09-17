
void FUN__text__00424f30(undefined4 param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_44 [13];
  undefined4 uStack_10;
  
  puVar2 = local_44;
  for (iVar1 = 0x10; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  (*API_USER32_DLL_GetPropA)(param_1,"sys_win_prop");
  FUN__text__0056ce80();
  uStack_10 = 0x424f6d;
  FUN__text__0056ce80();
  return;
}

