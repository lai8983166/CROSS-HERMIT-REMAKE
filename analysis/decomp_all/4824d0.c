
void FUN__text__004824d0(ushort *param_1,int param_2)

{
  ushort uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_58 [16];
  uint local_18;
  int local_14;
  int local_10;
  int local_c;
  undefined4 local_8;
  
  puVar3 = local_58;
  for (iVar2 = 0x15; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_14 = 100;
  local_c = (uint)param_1[2] - (int)((uint)*(byte *)(param_2 + 8) * *(int *)(param_2 + 0x10)) / 100;
  local_10 = FUN__text__00467e00("E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                 DAT_00618ef4 + 10);
  local_10 = local_10 % 100;
  local_c = local_c - local_10;
  if (*(char *)(param_2 + 8) == '\0') {
    if (0x95 < local_c) goto LAB__text__0048259c;
  }
  else {
    if (4 < local_10) {
      if ((0x5e < local_10) || (local_c < 0)) goto LAB__text__004826d9;
      if (local_c < 0x96) goto LAB__text__004825b4;
    }
LAB__text__0048259c:
    local_14 = local_c;
    if (local_c < 0x96) {
      local_14 = 0x96;
    }
  }
LAB__text__004825b4:
  if (param_1[1] == 0) {
    local_18 = (uint)*param_1;
  }
  else {
    uVar1 = *param_1;
    iVar2 = FUN__text__00467e00("E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                DAT_00618ef4 + 0x3a);
    local_18 = (uint)uVar1 + iVar2 % (int)(uint)param_1[1];
  }
  local_18 = (int)(local_18 * local_14) / 100 -
             (int)((uint)*(byte *)(param_2 + 9) * *(int *)(param_2 + 0x14)) / 100;
  if (local_14 == 100) {
    if ((int)local_18 < 1) {
      param_1[0x14] = 0;
      param_1[0x15] = 0;
    }
    else if ((int)((uint)*(ushort *)(param_2 + 0x24) * 3) < (int)local_18) {
      *(uint *)(param_1 + 0x14) = local_18;
    }
    else if ((int)(uint)*(ushort *)(param_2 + 0x24) < (int)local_18) {
      *(uint *)(param_1 + 0x14) = local_18;
    }
    else {
      *(uint *)(param_1 + 0x14) = local_18;
    }
  }
  else {
    if ((int)local_18 < 0) {
      local_18 = 1;
    }
    *(uint *)(param_1 + 0x14) = local_18;
  }
LAB__text__004826d9:
  local_8 = 0x4826e6;
  FUN__text__0056ce80();
  return;
}

