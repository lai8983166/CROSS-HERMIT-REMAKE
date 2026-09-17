
undefined4 __thiscall FUN__text__0052b910(int *param_1,undefined4 param_2,int param_3)

{
  code *pcVar1;
  undefined4 uVar2;
  int iVar3;
  undefined1 uVar4;
  int iVar5;
  uint uVar6;
  uint uVar7;
  undefined1 *puVar8;
  int *piVar9;
  undefined1 local_498 [1024];
  int local_98 [3];
  undefined2 local_8c;
  ushort local_8a;
  undefined4 local_88;
  undefined4 local_80;
  undefined4 local_7c;
  undefined2 local_2c;
  int local_2a;
  undefined2 uStack_26;
  undefined2 uStack_24;
  int local_22;
  uint local_1c;
  undefined1 local_18 [4];
  uint local_14;
  undefined1 local_10;
  undefined1 local_f;
  undefined1 local_e;
  undefined1 local_d;
  int local_c;
  undefined4 local_8;
  
  local_10 = 0;
  local_f = 0;
  local_e = 0;
  local_d = 0;
  local_8 = 0xff000000;
  local_18[0] = 0;
  local_14 = 0xff000000;
  piVar9 = local_98;
  for (iVar5 = 0x1b; uVar2 = local_8, iVar5 != 0; iVar5 = iVar5 + -1) {
    *piVar9 = 0;
    piVar9 = piVar9 + 1;
  }
  iVar5 = *param_1;
  local_8._3_1_ = SUB41(uVar2,3);
  local_8._0_3_ = CONCAT12(0xaa,CONCAT11(0x55,(undefined1)local_8));
  local_18[1] = 0x24;
  local_18[2] = 0x49;
  local_18[3] = 0x6d;
  local_14 = CONCAT13(local_14._3_1_,0xdbb692);
  local_c = 0;
  if (iVar5 == 0x14) {
    local_98[0] = 0x28;
    local_8a = 0x18;
  }
  else if (iVar5 == 0x1b) {
    local_98[0] = 0x28;
    local_8a = 8;
    local_c = 0x400;
    uVar6 = 0;
    do {
      uVar4 = local_18[uVar6 >> 5];
      iVar5 = uVar6 * 4;
      local_498[iVar5 + 3] = 0;
      local_498[iVar5 + 2] = uVar4;
      local_498[iVar5 + 1] = local_18[uVar6 >> 2 & 7];
      uVar7 = uVar6 & 3;
      uVar6 = uVar6 + 1;
      local_498[iVar5] = *(undefined1 *)((int)&local_8 + uVar7);
    } while (uVar6 < 0x100);
  }
  else if (iVar5 == 0x29) {
    iVar5 = param_1[2];
    puVar8 = (undefined1 *)(iVar5 + 2);
    uVar6 = 0;
    local_98[0] = 0x28;
    local_8a = 8;
    local_c = 0x400;
    do {
      iVar3 = uVar6 * 4;
      local_498[iVar3 + 2] = *(undefined1 *)(iVar5 + iVar3);
      local_498[iVar3 + 1] = puVar8[-1];
      uVar4 = *puVar8;
      local_498[iVar3 + 3] = 0;
      uVar6 = uVar6 + 1;
      puVar8 = puVar8 + 4;
      local_498[iVar3] = uVar4;
    } while (uVar6 < 0x100);
  }
  else {
    if (iVar5 != 0x32) {
      return 0x80004005;
    }
    local_98[0] = 0x28;
    local_8a = 8;
    local_c = 0x400;
    uVar6 = 0;
    do {
      iVar5 = uVar6 * 4;
      local_498[iVar5 + 3] = 0;
      uVar4 = (undefined1)uVar6;
      local_498[iVar5 + 2] = uVar4;
      local_498[iVar5 + 1] = uVar4;
      local_498[iVar5] = uVar4;
      uVar6 = uVar6 + 1;
    } while (uVar6 < 0x100);
  }
  local_88 = 0;
  local_98[1] = param_1[3];
  local_98[2] = param_1[4];
  local_80 = 0xb12;
  local_7c = 0xb12;
  local_1c = (uint)(local_8a >> 3);
  local_8 = local_98[1] * local_1c;
  local_14 = local_8 + 3 & 0xfffffffc;
  local_2a = local_98[2] * local_14 + 0x36 + local_c;
  uStack_26 = 0;
  uStack_24 = 0;
  iVar5 = (local_2a + 3U & 0xfffffffc) - local_2a;
  local_2a = iVar5 + local_2a;
  local_22 = local_c + 0x36;
  local_8c = 1;
  local_2c = 0x4d42;
  if (param_3 != 0) {
    (*DAT_005922bc)(param_2,&local_2c,0xe,&param_3,0);
  }
  pcVar1 = DAT_005922bc;
  (*DAT_005922bc)(param_2,local_98,0x28,&param_3,0);
  if (local_c != 0) {
    (*pcVar1)(param_2,local_498,local_c,&param_3,0);
  }
  local_1c = param_1[7] * param_1[0xc] + param_1[6] * local_1c + param_1[1];
  uVar6 = (param_1[4] + -1) * param_1[0xc] + local_1c;
  if (local_1c <= uVar6) {
    do {
      (*DAT_005922bc)(param_2,uVar6,local_8,&param_3,0);
      if (local_8 < local_14) {
        (*DAT_005922bc)(param_2,&local_10,local_14 - local_8,&param_3,0);
      }
      uVar6 = uVar6 - param_1[0xc];
    } while (local_1c <= uVar6);
  }
  if (iVar5 != 0) {
    (*DAT_005922bc)(param_2,&local_10,iVar5,&param_3,0);
  }
  return 0;
}

