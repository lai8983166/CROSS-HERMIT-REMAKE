
undefined4 __thiscall FUN__text__0044e5d0(int param_1,int param_2)

{
  int iVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_58 [17];
  int local_14;
  
  puVar3 = local_58;
  for (iVar2 = 0x15; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  iVar2 = *(int *)(param_1 + 0xb4 + param_2 * 4);
  iVar1 = *(int *)(iVar2 + 0x14);
  for (local_14 = 0; local_14 != iVar1; local_14 = local_14 + 1) {
    *(int *)(iVar2 + 0x18 + local_14 * 4) = *(int *)(iVar2 + 0x18 + local_14 * 4) + iVar2;
  }
  return 0;
}

