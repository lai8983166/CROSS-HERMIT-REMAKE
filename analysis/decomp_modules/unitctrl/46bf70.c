
void FUN__text__0046bf70(int param_1,int param_2,undefined4 *param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  undefined4 *local_10;
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (param_2 == 0) {
    if (param_3 != (undefined4 *)0x0) {
      *(undefined4 *)(param_1 + 0xe8) = *param_3;
      *(undefined4 *)(param_1 + 0xec) = param_3[1];
      *(undefined4 *)(param_1 + 0xf0) = param_3[2];
    }
  }
  else {
    FUN__text__0040ad20(param_1 + 0xa0 + param_2 * 0x58);
  }
  local_c = FUN__text__0040bd10();
  local_10 = *(undefined4 **)(local_c + 8);
  *local_10 = *param_3;
  local_10[1] = param_3[1];
  local_10[2] = param_3[2];
  FUN__text__0040bdd0(param_1 + 0x48,local_c);
  local_8 = 0x46c034;
  FUN__text__0056ce80();
  return;
}

