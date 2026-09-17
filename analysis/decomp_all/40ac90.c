
void FUN_0040ac90(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  int local_10;
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*(char *)(param_1 + 8) == '\0') {
    local_10 = *(int *)(param_1 + 0x20);
    while (local_10 != 0) {
      local_c = *(int *)(local_10 + 0x20);
      FUN_0040ab80(local_10);
      local_10 = local_c;
    }
    local_c = 0;
  }
  local_8 = 0x40ad0c;
  __chkesp();
  return;
}

