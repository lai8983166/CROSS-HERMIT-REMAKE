
void __thiscall FUN__text1__0080ecdb(int param_1,int param_2,uint param_3,uint param_4)

{
  undefined4 *puVar1;
  undefined4 *puVar2;
  uint *puVar3;
  undefined4 uVar4;
  int iVar5;
  uint uVar6;
  int iVar7;
  uint local_14;
  uint *local_10;
  uint *local_c;
  
  if (param_2 + 2U == param_3) {
    if (*(uint *)(*(int *)(param_1 + 0x18) + 4 + param_2 * 4) <
        *(uint *)(*(int *)(param_1 + 0x18) + param_2 * 4)) {
      puVar1 = (undefined4 *)(*(int *)(param_1 + 0xc) + param_2 * 4);
      puVar2 = (undefined4 *)(*(int *)(param_1 + 0xc) + (param_2 + 1) * 4);
      uVar4 = *puVar1;
      *puVar1 = *puVar2;
      *puVar2 = uVar4;
      puVar1 = (undefined4 *)(*(int *)(param_1 + 0x18) + param_2 * 4);
      puVar2 = (undefined4 *)(*(int *)(param_1 + 0x18) + (param_2 + 1) * 4);
      uVar4 = *puVar1;
      *puVar1 = *puVar2;
      *puVar2 = uVar4;
    }
  }
  else {
    if (param_2 + 3U == param_3) {
      if (*(uint *)(*(int *)(param_1 + 0x18) + 8 + param_2 * 4) <
          *(uint *)(*(int *)(param_1 + 0x18) + param_2 * 4)) {
        puVar1 = (undefined4 *)(*(int *)(param_1 + 0xc) + param_2 * 4);
        puVar2 = (undefined4 *)(*(int *)(param_1 + 0xc) + (param_2 + 2) * 4);
        uVar4 = *puVar1;
        *puVar1 = *puVar2;
        *puVar2 = uVar4;
        puVar1 = (undefined4 *)(*(int *)(param_1 + 0x18) + param_2 * 4);
        puVar2 = (undefined4 *)(*(int *)(param_1 + 0x18) + (param_2 + 2) * 4);
        uVar4 = *puVar1;
        *puVar1 = *puVar2;
        *puVar2 = uVar4;
      }
      if (*(uint *)(*(int *)(param_1 + 0x18) + 4 + param_2 * 4) <
          *(uint *)(*(int *)(param_1 + 0x18) + param_2 * 4)) {
        puVar1 = (undefined4 *)(*(int *)(param_1 + 0xc) + param_2 * 4);
        puVar2 = (undefined4 *)(*(int *)(param_1 + 0xc) + (param_2 + 1) * 4);
        uVar4 = *puVar1;
        *puVar1 = *puVar2;
        *puVar2 = uVar4;
        puVar1 = (undefined4 *)(*(int *)(param_1 + 0x18) + param_2 * 4);
        puVar2 = (undefined4 *)(*(int *)(param_1 + 0x18) + (param_2 + 1) * 4);
        uVar4 = *puVar1;
        *puVar1 = *puVar2;
        *puVar2 = uVar4;
      }
      else if (*(uint *)(*(int *)(param_1 + 0x18) + 8 + param_2 * 4) <
               *(uint *)(*(int *)(param_1 + 0x18) + 4 + param_2 * 4)) {
        puVar1 = (undefined4 *)(*(int *)(param_1 + 0xc) + (param_2 + 1) * 4);
        puVar2 = (undefined4 *)(*(int *)(param_1 + 0xc) + (param_2 + 2) * 4);
        uVar4 = *puVar1;
        *puVar1 = *puVar2;
        *puVar2 = uVar4;
        puVar1 = (undefined4 *)(*(int *)(param_1 + 0x18) + (param_2 + 1) * 4);
        puVar2 = (undefined4 *)(*(int *)(param_1 + 0x18) + (param_2 + 2) * 4);
        uVar4 = *puVar1;
        *puVar1 = *puVar2;
        *puVar2 = uVar4;
      }
    }
    local_c = (uint *)(*(int *)(param_1 + 0x18) + param_2 * 4);
    puVar3 = (uint *)(*(int *)(param_1 + 0x18) + param_3 * 4);
    local_14 = *local_c;
    while ((local_c = local_c + 1, local_c < puVar3 && (local_14 <= *local_c))) {
      local_14 = *local_c;
    }
    if (local_c != puVar3) {
      local_c = (uint *)(*(int *)(param_1 + 0x18) + param_2 * 4);
      local_10 = (uint *)(*(int *)(param_1 + 0x18) + -4 + param_3 * 4);
      while( true ) {
        for (; (local_c < local_10 && ((*local_c & param_4) == 0)); local_c = local_c + 1) {
        }
        for (; (local_c < local_10 && ((*local_10 & param_4) != 0)); local_10 = local_10 + -1) {
        }
        if (local_10 <= local_c) break;
        iVar7 = (int)local_10 - *(int *)(param_1 + 0x18) >> 2;
        iVar5 = (int)local_c - *(int *)(param_1 + 0x18) >> 2;
        local_c = local_c + 1;
        local_10 = local_10 + -1;
        puVar1 = (undefined4 *)(*(int *)(param_1 + 0xc) + iVar5 * 4);
        puVar2 = (undefined4 *)(*(int *)(param_1 + 0xc) + iVar7 * 4);
        uVar4 = *puVar1;
        *puVar1 = *puVar2;
        *puVar2 = uVar4;
        puVar1 = (undefined4 *)(*(int *)(param_1 + 0x18) + iVar5 * 4);
        puVar2 = (undefined4 *)(*(int *)(param_1 + 0x18) + iVar7 * 4);
        uVar4 = *puVar1;
        *puVar1 = *puVar2;
        *puVar2 = uVar4;
      }
      for (; (local_c < (uint *)(*(int *)(param_1 + 0x18) + param_3 * 4) &&
             ((*local_c & param_4) == 0)); local_c = local_c + 1) {
      }
      uVar6 = (int)local_c - *(int *)(param_1 + 0x18) >> 2;
      param_4 = param_4 >> 1;
      if (param_4 != 0) {
        if (param_2 + 1U < uVar6) {
          FUN__text1__0080ecdb(param_2,uVar6,param_4);
        }
        if (uVar6 + 1 < param_3) {
          FUN__text1__0080ecdb(uVar6,param_3,param_4);
        }
      }
    }
  }
  return;
}

