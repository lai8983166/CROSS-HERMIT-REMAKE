
void FUN__text__004e2c60(undefined4 *param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_44 [15];
  undefined4 uStack_8;
  
  puVar2 = local_44;
  for (iVar1 = 0x10; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  _memset(param_1,0,0x28);
  *param_1 = 0;
  param_1[1] = 0;
  param_1[2] = 0;
  param_1[3] = 1;
  param_1[4] = 1;
  param_1[5] = 1;
  param_1[6] = 1;
  param_1[7] = 6;
  param_1[8] = 4;
  param_1[9] = 9;
  uStack_8 = 0x4e2cf8;
  FUN__text__0056ce80();
  return;
}

