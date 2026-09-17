
undefined4 FUN__text__004b28b0(uint param_1,uint param_2)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_44 [16];
  
  puVar3 = local_44;
  for (iVar2 = 0x10; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (param_1 == param_2) {
    uVar1 = 0;
  }
  else if (param_1 < param_2) {
    uVar1 = 0x98;
  }
  else {
    uVar1 = 0x130;
  }
  return uVar1;
}

