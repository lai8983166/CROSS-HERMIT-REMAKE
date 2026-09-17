
undefined4
FUN__text__004ccb30(undefined4 param_1,undefined4 param_2,undefined4 *param_3,undefined4 *param_4)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [18];
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  *param_3 = *(undefined4 *)(DAT_007a49fc + 0x198c);
  *param_4 = *(undefined4 *)(DAT_007a49fc + 0x1990);
  return 1;
}

