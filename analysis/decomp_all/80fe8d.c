
void FUN__text1__0080fe8d(int param_1)

{
  undefined4 *puVar1;
  undefined4 *puVar2;
  uint uVar3;
  int iVar4;
  int iVar5;
  int local_14;
  int local_10;
  int local_c;
  
  local_10 = *(int *)(param_1 + 0x408) + -1;
  for (local_c = local_10; -1 < local_c; local_c = local_c + -1) {
    if (*(int *)(param_1 + 0x414 + local_c * 0x10) != 0) {
      puVar1 = (undefined4 *)(param_1 + 0x40c + local_c * 0x10);
      puVar2 = (undefined4 *)(param_1 + 0x40c + local_10 * 0x10);
      *puVar2 = *puVar1;
      puVar2[1] = puVar1[1];
      puVar2[2] = puVar1[2];
      puVar2[3] = puVar1[3];
      *(uint *)(param_1 + 0x40c + local_10 * 0x10) =
           *(int *)(param_1 + 0x40c + local_10 * 0x10) + 1U >> 1;
      local_10 = local_10 + -1;
    }
  }
  iVar4 = *(int *)(param_1 + 0x408);
  for (; local_c = iVar4 + -2, -1 < local_10; local_10 = local_10 + -1) {
    *(int *)(param_1 + 0x40c + local_10 * 0x10) =
         *(int *)(param_1 + 0x40c + local_c * 0x10) +
         *(int *)(param_1 + 0x40c + (iVar4 + -1) * 0x10);
    uVar3 = *(uint *)(param_1 + 0x40c + local_10 * 0x10);
    *(undefined4 *)(param_1 + 0x414 + local_10 * 0x10) = 0;
    iVar4 = local_10;
    do {
      iVar5 = iVar4;
      local_14 = iVar5 + 1;
      iVar4 = local_14;
    } while (uVar3 < *(uint *)(param_1 + 0x40c + local_14 * 0x10));
    FUN__text1__008487d0
              (param_1 + 0x40c + local_10 * 0x10,param_1 + 0x40c + (local_10 + 1) * 0x10,
               (iVar5 - local_10) * 0x10);
    *(uint *)(param_1 + 0x40c + iVar5 * 0x10) = uVar3;
    *(int *)(param_1 + 0x418 + iVar5 * 0x10) = local_c;
    *(undefined4 *)(param_1 + 0x414 + iVar5 * 0x10) = 0;
    iVar4 = local_c;
  }
  local_c = *(int *)(param_1 + 0x408);
  while (local_c = local_c + -1, -1 < local_c) {
    if (*(int *)(param_1 + 0x414 + local_c * 0x10) == 0) {
      iVar4 = *(int *)(param_1 + 0x418 + local_c * 0x10);
      *(int *)(param_1 + 0x410 + (iVar4 + 1) * 0x10) = local_c;
      *(int *)(param_1 + 0x410 + iVar4 * 0x10) = local_c;
    }
    else {
      *(int *)(param_1 + *(int *)(param_1 + 0x418 + local_c * 0x10) * 4) = local_c;
    }
  }
  return;
}

