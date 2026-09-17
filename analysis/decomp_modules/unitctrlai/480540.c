
int __thiscall FUN__text__00480540(int param_1,int param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  int local_14;
  int local_10;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_14 = 0;
  for (local_10 = 0; local_10 != *(int *)(param_1 + 0xdc8ec); local_10 = local_10 + 1) {
    if ((((*(short *)(param_2 + 2) != *(short *)(*(int *)(param_1 + 0xdc8f0 + local_10 * 4) + 2)) &&
         (*(char *)(*(int *)(*(int *)(param_1 + 0xdc8f0 + local_10 * 4) + 600) + 0xa4) ==
          *(char *)(*(int *)(param_2 + 600) + 0xa4))) &&
        (*(char *)(*(int *)(*(int *)(param_1 + 0xdc8f0 + local_10 * 4) + 600) + 0x98) ==
         *(char *)(*(int *)(param_2 + 600) + 0x98))) &&
       (*(char *)(*(int *)(*(int *)(param_1 + 0xdc8f0 + local_10 * 4) + 600) + 0x96) == '\x03')) {
      local_14 = local_14 + 1;
    }
  }
  return local_14;
}

