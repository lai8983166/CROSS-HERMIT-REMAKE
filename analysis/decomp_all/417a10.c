
undefined4 __thiscall FUN__text__00417a10(int param_1,int param_2,int param_3)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [18];
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (param_2 < 100) {
    if (param_3 < *(int *)(param_1 + 4 + param_2 * 8)) {
      uVar1 = *(undefined4 *)(*(int *)(param_1 + param_2 * 8) + param_3 * 0x10);
    }
    else {
      uVar1 = 0;
    }
  }
  else {
    uVar1 = 0;
  }
  return uVar1;
}

