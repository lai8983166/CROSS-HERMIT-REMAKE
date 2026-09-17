
void FUN__text__004026d0(undefined4 *param_1,undefined4 *param_2,undefined4 param_3,
                        undefined4 param_4,undefined4 param_5)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_60 [16];
  undefined4 local_20 [4];
  undefined4 local_10;
  undefined4 local_c;
  undefined4 local_8;
  
  puVar2 = local_60;
  for (iVar1 = 0x17; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  FUN__text__00402740();
  local_20[0] = *param_2;
  local_20[1] = param_2[1];
  local_20[2] = param_2[2];
  local_20[3] = param_2[3];
  local_10 = param_3;
  local_c = param_4;
  local_8 = param_5;
  puVar2 = local_20;
  for (iVar1 = 7; iVar1 != 0; iVar1 = iVar1 + -1) {
    *param_1 = *puVar2;
    puVar2 = puVar2 + 1;
    param_1 = param_1 + 1;
  }
  local_8 = 0x402739;
  FUN__text__0056ce80();
  return;
}

