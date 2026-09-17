
void __thiscall FUN__text1__0080f24c(int param_1,int param_2,int param_3,int param_4)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 *puVar3;
  int *piVar4;
  int *piVar5;
  byte *pbVar6;
  int iVar7;
  undefined4 uVar8;
  uint local_9c;
  uint local_1c;
  uint local_18;
  int local_14;
  int local_10;
  uint *local_8;
  
  if (param_2 + 2 == param_3) {
    iVar7 = FUN__text1__0080eb87
                      (*(undefined4 *)(*(int *)(param_1 + 0xc) + param_2 * 4),
                       *(undefined4 *)(*(int *)(param_1 + 0xc) + 4 + param_2 * 4));
    if (0 < iVar7) {
      puVar2 = (undefined4 *)(*(int *)(param_1 + 0xc) + param_2 * 4);
      puVar3 = (undefined4 *)(*(int *)(param_1 + 0xc) + (param_2 + 1) * 4);
      uVar8 = *puVar2;
      *puVar2 = *puVar3;
      *puVar3 = uVar8;
      puVar2 = (undefined4 *)(*(int *)(param_1 + 0x18) + param_2 * 4);
      puVar3 = (undefined4 *)(*(int *)(param_1 + 0x18) + (param_2 + 1) * 4);
      uVar8 = *puVar2;
      *puVar2 = *puVar3;
      *puVar3 = uVar8;
    }
  }
  else if (param_2 + 3 == param_3) {
    iVar7 = FUN__text1__0080eb87
                      (*(undefined4 *)(*(int *)(param_1 + 0xc) + param_2 * 4),
                       *(undefined4 *)(*(int *)(param_1 + 0xc) + 8 + param_2 * 4));
    if (0 < iVar7) {
      puVar2 = (undefined4 *)(*(int *)(param_1 + 0xc) + param_2 * 4);
      puVar3 = (undefined4 *)(*(int *)(param_1 + 0xc) + (param_2 + 2) * 4);
      uVar8 = *puVar2;
      *puVar2 = *puVar3;
      *puVar3 = uVar8;
      puVar2 = (undefined4 *)(*(int *)(param_1 + 0x18) + param_2 * 4);
      puVar3 = (undefined4 *)(*(int *)(param_1 + 0x18) + (param_2 + 2) * 4);
      uVar8 = *puVar2;
      *puVar2 = *puVar3;
      *puVar3 = uVar8;
    }
    iVar7 = FUN__text1__0080eb87
                      (*(undefined4 *)(*(int *)(param_1 + 0xc) + param_2 * 4),
                       *(undefined4 *)(*(int *)(param_1 + 0xc) + 4 + param_2 * 4));
    if (iVar7 < 1) {
      iVar7 = FUN__text1__0080eb87
                        (*(undefined4 *)(*(int *)(param_1 + 0xc) + 4 + param_2 * 4),
                         *(undefined4 *)(*(int *)(param_1 + 0xc) + 8 + param_2 * 4));
      if (0 < iVar7) {
        puVar2 = (undefined4 *)(*(int *)(param_1 + 0xc) + (param_2 + 1) * 4);
        puVar3 = (undefined4 *)(*(int *)(param_1 + 0xc) + (param_2 + 2) * 4);
        uVar8 = *puVar2;
        *puVar2 = *puVar3;
        *puVar3 = uVar8;
        puVar2 = (undefined4 *)(*(int *)(param_1 + 0x18) + (param_2 + 1) * 4);
        puVar3 = (undefined4 *)(*(int *)(param_1 + 0x18) + (param_2 + 2) * 4);
        uVar8 = *puVar2;
        *puVar2 = *puVar3;
        *puVar3 = uVar8;
      }
    }
    else {
      puVar2 = (undefined4 *)(*(int *)(param_1 + 0xc) + param_2 * 4);
      puVar3 = (undefined4 *)(*(int *)(param_1 + 0xc) + (param_2 + 1) * 4);
      uVar8 = *puVar2;
      *puVar2 = *puVar3;
      *puVar3 = uVar8;
      puVar2 = (undefined4 *)(*(int *)(param_1 + 0x18) + param_2 * 4);
      puVar3 = (undefined4 *)(*(int *)(param_1 + 0x18) + (param_2 + 1) * 4);
      uVar8 = *puVar2;
      *puVar2 = *puVar3;
      *puVar3 = uVar8;
    }
  }
  else {
    if (param_4 == 0) {
      iVar7 = *(int *)(param_1 + 0x18);
      local_18 = param_2;
      for (local_8 = (uint *)(*(int *)(param_1 + 0x18) + param_2 * 4);
          local_8 < (uint *)(iVar7 + param_3 * 4); local_8 = local_8 + 1) {
        pbVar6 = *(byte **)(*(int *)(param_1 + 0xc) + local_18 * 4);
        local_18 = local_18 + 1;
        if (pbVar6 < *(byte **)(param_1 + 8)) {
          local_9c = (uint)*pbVar6 << 0x18 | (uint)pbVar6[1] << 0x10 | (uint)pbVar6[2] << 8 |
                     (uint)pbVar6[3];
        }
        else {
          local_9c = FUN__text1__0080ea40(pbVar6,0);
        }
        *local_8 = local_9c;
      }
      FUN__text1__0080ecdb(param_2,param_3,0x80000000);
    }
    else {
      while( true ) {
        iVar7 = *(int *)(param_1 + 0x18);
        local_18 = param_2;
        for (local_8 = (uint *)(*(int *)(param_1 + 0x18) + param_2 * 4);
            local_8 < (undefined4 *)(iVar7 + param_3 * 4); local_8 = local_8 + 1) {
          iVar1 = local_18 * 4;
          local_18 = local_18 + 1;
          uVar8 = FUN__text1__0080ea40(*(undefined4 *)(*(int *)(param_1 + 0xc) + iVar1),param_4);
          *local_8 = uVar8;
        }
        FUN__text1__0080ecdb(param_2,param_3,0x80000000);
        if (*(int *)(*(int *)(param_1 + 0x18) + param_2 * 4) !=
            *(int *)(*(int *)(param_1 + 0x18) + -4 + param_3 * 4)) break;
        param_4 = param_4 + 4;
      }
    }
    piVar4 = (int *)(*(int *)(param_1 + 0x18) + param_2 * 4);
    piVar5 = (int *)(*(int *)(param_1 + 0x18) + param_3 * 4);
    local_18 = param_2 + 1;
    local_14 = *piVar4;
    local_8 = (uint *)(piVar4 + 1);
    local_10 = 0;
    while (local_8 < piVar5) {
      local_1c = (int)piVar5 - (int)local_8 >> 2;
      if (local_1c < 0x101) {
        local_1c = local_1c + local_18;
      }
      else {
        local_1c = local_18 + 0x100;
      }
      for (; local_18 < local_1c; local_18 = local_18 + 1) {
        if (*local_8 == local_14) {
          local_10 = local_10 + 1;
        }
        else {
          if (local_10 != 0) {
            FUN__text1__0080f24c(local_18 - (local_10 + 1),local_18,param_4 + 4);
            local_10 = 0;
          }
          local_14 = *local_8;
        }
        local_8 = local_8 + 1;
      }
    }
    if (local_10 != 0) {
      FUN__text1__0080f24c(param_3 - (local_10 + 1),param_3,param_4 + 4);
    }
  }
  return;
}

