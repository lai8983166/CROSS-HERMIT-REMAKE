
void __fastcall FUN__text__004b8f70(undefined4 *param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  undefined4 *local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  *param_1 = &PTR_DAT_005a0c38;
  local_8 = param_1;
  FUN__text__00439f80();
  local_8 = (undefined4 *)0x4b8fab;
  FUN__text__0056ce80();
  return;
}

