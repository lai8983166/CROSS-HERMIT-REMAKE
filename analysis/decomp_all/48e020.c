
undefined4 FUN__text__0048e020(int param_1,uint param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [17];
  int local_c;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*(int *)(param_1 + 0x518) != 0) {
    local_c = *(int *)(param_1 + 0x518);
    do {
      if (**(byte **)(local_c + 8) == param_2) {
        return 1;
      }
      local_c = *(int *)(local_c + 4);
    } while (local_c != 0);
  }
  return 0;
}

