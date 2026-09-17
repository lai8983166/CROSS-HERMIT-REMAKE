
int FUN__text__004280c0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  int local_10;
  int local_c;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*(int *)(param_1 + 4) == 0) {
    local_10 = 0;
  }
  else {
    local_10 = 0;
    local_c = *(int *)(param_1 + 4);
    do {
      local_10 = local_10 + 1;
      local_c = *(int *)(local_c + 4);
    } while (local_c != 0);
  }
  return local_10;
}

