
void FUN__text__004e1be0(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 *puVar3;
  undefined4 local_48 [16];
  int local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  _memset(&DAT_007e17e8,0,0x12ca0);
  for (local_8 = 0; local_8 != 0x41; local_8 = local_8 + 1) {
    puVar2 = (undefined4 *)(&DAT_006f5088 + local_8 * 0x4a0);
    puVar3 = (undefined4 *)(&DAT_007e17e8 + local_8 * 0x4a0);
    for (iVar1 = 0x128; iVar1 != 0; iVar1 = iVar1 + -1) {
      *puVar3 = *puVar2;
      puVar2 = puVar2 + 1;
      puVar3 = puVar3 + 1;
    }
  }
  FUN__text__0049e930();
  local_8 = 0x4e1c5f;
  FUN__text__0056ce80();
  return;
}

