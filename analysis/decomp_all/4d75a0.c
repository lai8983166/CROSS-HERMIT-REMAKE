
void __thiscall
FUN__text__004d75a0(int param_1,undefined4 param_2,undefined4 *param_3,short param_4,short param_5)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 *puVar3;
  undefined4 local_5c [16];
  undefined4 *local_1c;
  undefined4 *local_18;
  undefined4 *local_14;
  undefined4 *local_10;
  short local_c;
  int local_8;
  
  puVar2 = local_5c;
  for (iVar1 = 0x16; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_10 = param_3;
  local_1c = (undefined4 *)(param_1 + 0x2c72a);
  local_18 = local_1c;
  local_14 = local_1c;
  local_8 = param_1;
  FUN__text__0042add0(param_2,local_1c);
  puVar2 = local_1c;
  puVar3 = local_10;
  for (iVar1 = 0xc1b5; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar3 = *puVar2;
    puVar2 = puVar2 + 1;
    puVar3 = puVar3 + 1;
  }
  if (param_5 == 1) {
    if (DAT_007e11a8 == 6) {
      FUN__text__004e1c70(local_10 + 0x17a5,0);
    }
    else {
      FUN__text__004e1c70(local_10 + 0x17a5,1);
    }
  }
  if (param_4 != 0) {
    for (local_c = 0; local_c < 0x41; local_c = local_c + 1) {
      puVar2 = local_10 + local_c * 0x128 + 0x5d71;
      puVar3 = (undefined4 *)(&DAT_007e17e8 + local_c * 0x4a0);
      for (iVar1 = 0x128; iVar1 != 0; iVar1 = iVar1 + -1) {
        *puVar3 = *puVar2;
        puVar2 = puVar2 + 1;
        puVar3 = puVar3 + 1;
      }
    }
  }
  local_8 = 0x4d769f;
  FUN__text__0056ce80();
  return;
}

