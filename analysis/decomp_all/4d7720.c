
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN__text__004d7720(undefined4 param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 *puVar3;
  undefined4 local_5c [16];
  undefined4 local_1c;
  undefined4 *local_18;
  int local_14;
  int local_10;
  short local_c;
  int local_8;
  
  puVar2 = local_5c;
  for (iVar1 = 0x16; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  DAT_007a50e8._0_2_ = 7;
  DAT_007a50ec = FUN__text__004e2c30();
  local_10 = local_8 + 0x2c72a;
  local_14 = local_8 + 0x2c72a;
  local_18 = (undefined4 *)(local_8 + 0x2c72a);
  for (local_c = 0; local_c < 0x41; local_c = local_c + 1) {
    puVar2 = (undefined4 *)(&DAT_007e17e8 + local_c * 0x4a0);
    puVar3 = (undefined4 *)(&DAT_007bc6ac + local_c * 0x4a0);
    for (iVar1 = 0x128; iVar1 != 0; iVar1 = iVar1 + -1) {
      *puVar3 = *puVar2;
      puVar2 = puVar2 + 1;
      puVar3 = puVar3 + 1;
    }
  }
  puVar2 = &DAT_007f7c18;
  puVar3 = &DAT_007aaf7c;
  for (iVar1 = 0x45cc; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar3 = *puVar2;
    puVar2 = puVar2 + 1;
    puVar3 = puVar3 + 1;
  }
  _DAT_007a5114 = 0;
  local_1c = FUN__text__004d76b0(&DAT_007a50e8,0x306d4);
  puVar2 = &DAT_007a50e8;
  puVar3 = local_18;
  _DAT_007a5114 = local_1c;
  for (iVar1 = 0xc1b5; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar3 = *puVar2;
    puVar2 = puVar2 + 1;
    puVar3 = puVar3 + 1;
  }
  FUN__text__0042af00(param_1,local_18,0x306d4);
  local_8 = 0x4d7823;
  FUN__text__0056ce80();
  return;
}

