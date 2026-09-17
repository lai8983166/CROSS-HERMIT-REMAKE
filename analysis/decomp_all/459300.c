
void FUN__text__00459300(undefined4 param_1)

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
  FUN__text__00424670();
  *local_8 = &PTR_DAT_0059a7c0;
  local_8[4] = param_1;
  local_8 = (undefined4 *)0x459347;
  FUN__text__0056ce80();
  return;
}

