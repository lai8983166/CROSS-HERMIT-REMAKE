
void FUN__text1__0084288d(int param_1,int *param_2)

{
  int iVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  int iVar5;
  uint uVar6;
  int iVar7;
  uint local_34;
  int local_28;
  int local_24;
  uint local_20;
  uint local_1c;
  int local_10;
  
  iVar1 = *param_2;
  iVar2 = param_2[1];
  iVar3 = *(int *)param_2[2];
  iVar4 = *(int *)(param_2[2] + 4);
  iVar5 = *(int *)(param_2[2] + 8);
  uVar6 = *(uint *)(param_2[2] + 0x10);
  local_10 = 0;
  for (local_1c = 0; (int)local_1c < 0x10; local_1c = local_1c + 1) {
    *(undefined2 *)(param_1 + 0xb34 + local_1c * 2) = 0;
  }
  *(undefined2 *)(iVar1 + 2 + *(int *)(param_1 + 0xb54 + *(int *)(param_1 + 0x144c) * 4) * 4) = 0;
  local_24 = *(int *)(param_1 + 0x144c);
  while (local_24 = local_24 + 1, local_24 < 0x23d) {
    iVar7 = *(int *)(param_1 + 0xb54 + local_24 * 4);
    local_1c = *(ushort *)(iVar1 + 2 + (uint)*(ushort *)(iVar1 + 2 + iVar7 * 4) * 4) + 1;
    if ((int)uVar6 < (int)local_1c) {
      local_10 = local_10 + 1;
      local_1c = uVar6;
    }
    *(undefined2 *)(iVar1 + 2 + iVar7 * 4) = (undefined2)local_1c;
    if (iVar7 <= iVar2) {
      *(short *)(param_1 + 0xb34 + local_1c * 2) = *(short *)(param_1 + 0xb34 + local_1c * 2) + 1;
      local_28 = 0;
      if (iVar5 <= iVar7) {
        local_28 = *(int *)(iVar4 + (iVar7 - iVar5) * 4);
      }
      local_20 = (uint)*(ushort *)(iVar1 + iVar7 * 4);
      *(uint *)(param_1 + 0x16a0) = *(int *)(param_1 + 0x16a0) + local_20 * (local_1c + local_28);
      if (iVar3 != 0) {
        *(uint *)(param_1 + 0x16a4) =
             *(int *)(param_1 + 0x16a4) +
             local_20 * ((uint)*(ushort *)(iVar3 + 2 + iVar7 * 4) + local_28);
      }
    }
  }
  local_1c = uVar6;
  if (local_10 != 0) {
    do {
      do {
        local_1c = local_1c - 1;
      } while (*(short *)(param_1 + 0xb34 + local_1c * 2) == 0);
      *(short *)(param_1 + 0xb34 + local_1c * 2) = *(short *)(param_1 + 0xb34 + local_1c * 2) + -1;
      *(short *)(param_1 + 0xb36 + local_1c * 2) = *(short *)(param_1 + 0xb36 + local_1c * 2) + 2;
      *(short *)(param_1 + 0xb34 + uVar6 * 2) = *(short *)(param_1 + 0xb34 + uVar6 * 2) + -1;
      local_10 = local_10 + -2;
      local_1c = uVar6;
    } while (0 < local_10);
    for (; local_1c != 0; local_1c = local_1c - 1) {
      local_34 = (uint)*(ushort *)(param_1 + 0xb34 + local_1c * 2);
      while (local_34 != 0) {
        local_24 = local_24 + -1;
        iVar3 = *(int *)(param_1 + 0xb54 + local_24 * 4);
        if (iVar3 <= iVar2) {
          if (*(ushort *)(iVar1 + 2 + iVar3 * 4) != local_1c) {
            *(uint *)(param_1 + 0x16a0) =
                 *(int *)(param_1 + 0x16a0) +
                 (local_1c - *(ushort *)(iVar1 + 2 + iVar3 * 4)) *
                 (uint)*(ushort *)(iVar1 + iVar3 * 4);
            *(undefined2 *)(iVar1 + 2 + iVar3 * 4) = (undefined2)local_1c;
          }
          local_34 = local_34 - 1;
        }
      }
    }
  }
  return;
}

