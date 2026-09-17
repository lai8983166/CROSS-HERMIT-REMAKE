
int * FUN_005792a0(int param_1)

{
  int *piVar1;
  int *piVar2;
  char cVar3;
  int *piVar4;
  int iVar5;
  undefined4 uVar6;
  byte bVar7;
  uint *puVar8;
  int *piVar9;
  uint uVar10;
  uint local_38;
  int local_34;
  uint local_28;
  int local_24;
  uint local_20;
  uint *local_1c;
  int local_18;
  
  puVar8 = DAT_0080ab48 + DAT_0080ab44 * 5;
  uVar10 = param_1 + 0x17U & 0xfffffff0;
  iVar5 = ((int)(param_1 + 0x17U) >> 4) + -1;
  bVar7 = (byte)iVar5;
  if (iVar5 < 0x20) {
    local_28 = 0xffffffff >> (bVar7 & 0x1f);
    local_38 = 0xffffffff;
  }
  else {
    local_28 = 0;
    local_38 = 0xffffffff >> (bVar7 - 0x20 & 0x1f);
  }
  for (local_1c = DAT_0080ab38;
      (local_1c < puVar8 && ((local_28 & *local_1c) == 0 && (local_38 & local_1c[1]) == 0));
      local_1c = local_1c + 5) {
  }
  if (local_1c == puVar8) {
    for (local_1c = DAT_0080ab48;
        (local_1c < DAT_0080ab38 && ((local_28 & *local_1c) == 0 && (local_38 & local_1c[1]) == 0));
        local_1c = local_1c + 5) {
    }
    if (local_1c == DAT_0080ab38) {
      for (; (local_1c < puVar8 && (local_1c[2] == 0)); local_1c = local_1c + 5) {
      }
      if (local_1c == puVar8) {
        for (local_1c = DAT_0080ab48; (local_1c < DAT_0080ab38 && (local_1c[2] == 0));
            local_1c = local_1c + 5) {
        }
        if ((local_1c == DAT_0080ab38) &&
           (local_1c = (uint *)FUN_005797e0(), local_1c == (uint *)0x0)) {
          return (int *)0x0;
        }
      }
      uVar6 = FUN_005798f0(local_1c);
      *(undefined4 *)local_1c[4] = uVar6;
      if (*(int *)local_1c[4] == -1) {
        return (int *)0x0;
      }
    }
  }
  DAT_0080ab38 = local_1c;
  piVar4 = (int *)local_1c[4];
  local_34 = *piVar4;
  if ((local_34 == -1) ||
     ((local_28 & piVar4[local_34 + 0x11]) == 0 && (local_38 & piVar4[local_34 + 0x31]) == 0)) {
    local_34 = 0;
    while ((local_28 & piVar4[local_34 + 0x11]) == 0 && (local_38 & piVar4[local_34 + 0x31]) == 0) {
      local_34 = local_34 + 1;
    }
  }
  piVar2 = piVar4 + local_34 * 0x81 + 0x51;
  local_24 = 0;
  local_20 = local_28 & piVar4[local_34 + 0x11];
  if (local_20 == 0) {
    local_24 = 0x20;
    local_20 = local_38 & piVar4[local_34 + 0x31];
  }
  for (; -1 < (int)local_20; local_20 = local_20 << 1) {
    local_24 = local_24 + 1;
  }
  piVar9 = (int *)piVar2[local_24 * 2 + 1];
  iVar5 = *piVar9 - uVar10;
  local_18 = (iVar5 >> 4) + -1;
  if (0x3f < local_18) {
    local_18 = 0x3f;
  }
  if (local_18 != local_24) {
    if (piVar9[1] == piVar9[2]) {
      bVar7 = (byte)local_24;
      if (local_24 < 0x20) {
        piVar4[local_34 + 0x11] = piVar4[local_34 + 0x11] & ~(0x80000000U >> (bVar7 & 0x1f));
        *(char *)((int)piVar4 + local_24 + 4) = *(char *)((int)piVar4 + local_24 + 4) + -1;
        if (*(char *)((int)piVar4 + local_24 + 4) == '\0') {
          *local_1c = *local_1c & ~(0x80000000U >> (bVar7 & 0x1f));
        }
      }
      else {
        piVar4[local_34 + 0x31] = piVar4[local_34 + 0x31] & ~(0x80000000U >> (bVar7 - 0x20 & 0x1f));
        *(char *)((int)piVar4 + local_24 + 4) = *(char *)((int)piVar4 + local_24 + 4) + -1;
        if (*(char *)((int)piVar4 + local_24 + 4) == '\0') {
          local_1c[1] = local_1c[1] & ~(0x80000000U >> (bVar7 - 0x20 & 0x1f));
        }
      }
    }
    *(int *)(piVar9[2] + 4) = piVar9[1];
    *(int *)(piVar9[1] + 8) = piVar9[2];
    if (iVar5 != 0) {
      piVar1 = piVar2 + local_18 * 2;
      piVar9[1] = piVar1[1];
      piVar9[2] = (int)piVar1;
      piVar1[1] = (int)piVar9;
      *(int **)(piVar9[1] + 8) = piVar9;
      if (piVar9[1] == piVar9[2]) {
        bVar7 = (byte)local_18;
        if (local_18 < 0x20) {
          cVar3 = *(char *)((int)piVar4 + local_18 + 4);
          *(char *)((int)piVar4 + local_18 + 4) = *(char *)((int)piVar4 + local_18 + 4) + '\x01';
          if (cVar3 == '\0') {
            *local_1c = *local_1c | 0x80000000U >> (bVar7 & 0x1f);
          }
          piVar4[local_34 + 0x11] = piVar4[local_34 + 0x11] | 0x80000000U >> (bVar7 & 0x1f);
        }
        else {
          cVar3 = *(char *)((int)piVar4 + local_18 + 4);
          *(char *)((int)piVar4 + local_18 + 4) = *(char *)((int)piVar4 + local_18 + 4) + '\x01';
          if (cVar3 == '\0') {
            local_1c[1] = local_1c[1] | 0x80000000U >> (bVar7 - 0x20 & 0x1f);
          }
          piVar4[local_34 + 0x31] = piVar4[local_34 + 0x31] | 0x80000000U >> (bVar7 - 0x20 & 0x1f);
        }
      }
    }
  }
  if (iVar5 != 0) {
    *piVar9 = iVar5;
    *(int *)((int)piVar9 + iVar5 + -4) = iVar5;
  }
  piVar9 = (int *)((int)piVar9 + iVar5);
  *piVar9 = uVar10 + 1;
  *(uint *)((int)piVar9 + (uVar10 - 4)) = uVar10 + 1;
  iVar5 = *piVar2;
  *piVar2 = *piVar2 + 1;
  if (((iVar5 == 0) && (local_1c == DAT_0080ab40)) && (local_34 == DAT_0080ab34)) {
    DAT_0080ab40 = (uint *)0x0;
  }
  *piVar4 = local_34;
  return piVar9 + 1;
}

