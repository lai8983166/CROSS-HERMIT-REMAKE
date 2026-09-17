
undefined4 __thiscall FUN__text__00437d10(int param_1,int param_2)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [19];
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if ((((*(int *)(param_1 + 0x60) == 0) || (*(int *)(param_2 + 0x2f8) != 0)) ||
      (*(int *)(param_2 + 0x304) != 0)) ||
     ((*(int *)(param_2 + 0x3e4) != 0 || (*(int *)(param_2 + 0x3f0) != 0)))) {
    uVar1 = 0;
  }
  else {
    uVar1 = 1;
  }
  return uVar1;
}

