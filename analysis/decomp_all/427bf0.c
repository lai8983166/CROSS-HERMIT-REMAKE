
undefined4 __fastcall FUN__text__00427bf0(int param_1)

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
  if (*(int *)(param_1 + 0x24) == 0) {
    uVar1 = 0;
  }
  else {
    uVar1 = *(undefined4 *)(param_1 + 0x24);
    *(undefined4 *)(param_1 + 0x24) = *(undefined4 *)(*(int *)(param_1 + 0x24) + 4);
  }
  return uVar1;
}

