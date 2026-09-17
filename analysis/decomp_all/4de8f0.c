
undefined * FUN__text__004de8f0(int param_1)

{
  undefined *puVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_44 [16];
  
  puVar3 = local_44;
  for (iVar2 = 0x10; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (param_1 < 0x65) {
    puVar1 = &DAT_006d4e58 + param_1 * 7;
  }
  else {
    puVar1 = &DAT_00738af0;
  }
  return puVar1;
}

