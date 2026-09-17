
int FUN__text__004385a0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  int local_10;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_10 = param_1;
  if (*(int *)(param_1 + 0x14) != 0) {
    iVar1 = local_10;
    do {
      local_10 = iVar1;
      iVar1 = *(int *)(local_10 + 0x14);
    } while (*(int *)(*(int *)(local_10 + 0x14) + 0x14) != 0);
  }
  return local_10;
}

