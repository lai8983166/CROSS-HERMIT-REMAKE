
void FUN__text__004d5ec0(undefined4 *param_1,undefined2 param_2,undefined2 param_3,
                        undefined2 param_4,undefined2 param_5)

{
  char cVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  uint local_c;
  undefined4 local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = local_c & 0xffffff00;
  *param_1 = 0;
  param_1[1] = 0;
  param_1[2] = 0;
  *(undefined2 *)(param_1 + 3) = 0;
  cVar1 = FUN__text__004d5b70(CONCAT22((short)((uint)DAT_007a49fc >> 0x10),
                                       *(undefined2 *)(DAT_007a49fc + 0x196c)),
                              *(undefined2 *)(DAT_007a49fc + 0x1970),param_2,param_3,param_4,param_5
                             );
  local_c = CONCAT31(local_c._1_3_,cVar1);
  if (cVar1 != '\0') {
    *param_1 = *(undefined4 *)(DAT_007a49fc + 0x198c);
    param_1[1] = *(undefined4 *)(DAT_007a49fc + 0x1990);
    param_1[2] = *(undefined4 *)(DAT_007a49fc + 0x19a0);
    *(undefined2 *)(param_1 + 3) = 1;
  }
  local_8 = 0x4d5fa1;
  FUN__text__0056ce80();
  return;
}

