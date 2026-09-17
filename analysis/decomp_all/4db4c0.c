
void FUN__text__004db4c0(undefined4 param_1,void *param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  undefined *local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = &DAT_006c2e10;
  _memset(param_2,0,0x24);
  local_8 = (undefined *)0x4db4fc;
  FUN__text__0056ce80();
  return;
}

