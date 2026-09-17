
void FUN__text__00403480(undefined4 *param_1,undefined4 *param_2,undefined4 *param_3,
                        undefined4 param_4,undefined4 param_5)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_64 [16];
  undefined4 local_24 [4];
  undefined4 local_14;
  undefined4 local_10;
  undefined4 local_c;
  undefined4 local_8;
  
  puVar2 = local_64;
  for (iVar1 = 0x18; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  FUN__text__00403500();
  local_24[0] = *param_2;
  local_24[1] = param_2[1];
  local_24[2] = param_2[2];
  local_24[3] = *param_3;
  local_14 = param_3[1];
  local_10 = param_3[2];
  local_c = param_4;
  local_8 = param_5;
  puVar2 = local_24;
  for (iVar1 = 8; iVar1 != 0; iVar1 = iVar1 + -1) {
    *param_1 = *puVar2;
    puVar2 = puVar2 + 1;
    param_1 = param_1 + 1;
  }
  local_8 = 0x4034f1;
  FUN__text__0056ce80();
  return;
}

