
/* WARNING: Removing unreachable block (ram,0x00484481) */

void __thiscall FUN__text__004843a0(int param_1,int param_2,undefined4 param_3,undefined4 *param_4)

{
  code *pcVar1;
  undefined2 uVar2;
  int iVar3;
  int iVar4;
  undefined4 *puVar5;
  undefined4 uVar6;
  undefined3 *puVar7;
  undefined4 local_90 [16];
  uint local_50;
  char local_4c;
  int local_48;
  uint local_44;
  uint local_40;
  int local_3c;
  int local_38;
  uint local_34;
  int local_30;
  int local_2c;
  undefined *local_28;
  undefined4 local_24;
  int local_20;
  int local_1c;
  undefined3 local_18;
  undefined1 uStack_15;
  undefined2 local_14;
  undefined1 uStack_12;
  undefined1 uStack_11;
  undefined2 local_10;
  undefined2 uStack_e;
  int *local_c;
  int local_8;
  
  puVar5 = local_90;
  for (iVar3 = 0x23; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar5 = 0xcccccccc;
    puVar5 = puVar5 + 1;
  }
  local_28 = &DAT_006c3680;
  local_4c = *(char *)((int)param_4 + 7);
  local_8 = param_1;
  if (local_4c == '\0') {
    *(char *)((int)param_4 + 7) = *(char *)((int)param_4 + 7) + '\x01';
  }
  else if (local_4c != '\x01') {
    if ((local_4c == '\x02') &&
       (iVar3 = FUN__text__00424f80(&DAT_0059db60,
                                    "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                    DAT_00618f20 + 0x55,0), iVar3 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    goto LAB__text__004847dc;
  }
  *(char *)((int)param_4 + 7) = *(char *)((int)param_4 + 7) + '\x01';
  local_34 = (uint)DAT_006c3696 +
             ((uint)*(byte *)(*(int *)(param_2 + 600) + 10) * (uint)DAT_006c3697) / 100;
  if (0x20 < local_34) {
    local_34 = 0x20;
  }
  local_1c = (int)DAT_006c36a0 +
             (int)((uint)*(byte *)(*(int *)(param_2 + 600) + 7) * (int)DAT_006c36a2) / 100;
  local_20 = (int)DAT_006c36a4 +
             (int)((uint)*(byte *)(*(int *)(param_2 + 600) + 7) * (int)DAT_006c36a6) / 100;
  if (local_20 != 0) {
    iVar3 = FUN__text__00467e00("E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                DAT_00618f20 + 0x1d);
    local_1c = local_1c + iVar3 % local_20;
  }
  local_24 = 1;
  local_50 = (uint)(byte)local_28[0x18];
  switch(local_50) {
  case 0:
  case 5:
    iVar3 = FUN__text__00424f80(&DAT_005924d4,
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                DAT_00618f20 + 0x25,0);
    if (iVar3 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    break;
  case 1:
  case 2:
  case 3:
  case 6:
    iVar3 = *(int *)(local_8 + 0x80dd8 + (uint)*(byte *)((int)param_4 + 3) * 0x520);
    local_40 = (int)((iVar3 >> 0x10) + (iVar3 >> 0x1f & 0x1fU)) >> 5;
    iVar3 = *(int *)(local_8 + 0x80ddc + (uint)*(byte *)((int)param_4 + 3) * 0x520);
    local_44 = (int)((iVar3 >> 0x10) + (iVar3 >> 0x1f & 0xfU)) >> 4;
    break;
  case 4:
    local_40 = (uint)*(byte *)(param_2 + 0x4f0);
    local_44 = (uint)*(byte *)(param_2 + 0x4f1);
  }
  local_c = (int *)(local_8 + 0xdc8ec);
  local_30 = 0;
  for (local_2c = 0; local_2c != *local_c; local_2c = local_2c + 1) {
    local_48 = local_c[local_2c + 1];
    iVar3 = FUN__text__0046abc0(param_2,local_48);
    if ((iVar3 != 0) || (iVar3 = FUN__text__0046ad60(param_2,local_48), iVar3 != 0)) {
      local_38 = (int)((*(int *)(local_48 + 0x2ec) >> 0x10) +
                      (*(int *)(local_48 + 0x2ec) >> 0x1f & 0x1fU)) >> 5;
      local_3c = (int)((*(int *)(local_48 + 0x2f0) >> 0x10) +
                      (*(int *)(local_48 + 0x2f0) >> 0x1f & 0xfU)) >> 4;
      iVar3 = FUN__text__0043c1d0(local_40,local_44,local_38,local_3c,local_34);
      if (iVar3 != 0) {
        iVar3 = FUN__text__00467e00("E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                    DAT_00618f20 + 0x41);
        local_20 = local_1c + iVar3 % 6;
        _local_14 = CONCAT13(2,CONCAT12((undefined1)local_24,(short)param_4[1]));
        _local_10 = CONCAT22((undefined2)local_20,(short)param_4[2]);
        _local_18 = CONCAT13(*(undefined1 *)(local_48 + 2),(int3)*param_4);
        iVar3 = FUN__text__00467e00("E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                    DAT_00618f20 + 0x48);
        local_18._0_2_ = (short)(iVar3 % 0x28) + 0x14;
        if ((ushort)*(byte *)((int)param_4 + 3) == *(ushort *)(local_48 + 2)) {
          local_18._0_2_ = 0;
        }
        uVar2 = FUN__text__00415070((int)(short)local_18);
        _local_18 = CONCAT22(stack0xffffffea,uVar2);
        puVar7 = &local_18;
        uVar6 = 0;
        iVar3 = FUN__text__00467e00("E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                    DAT_00618f20 + 0x4d);
        iVar4 = iVar3 % 0x14 + -10;
        iVar3 = FUN__text__00467e00("E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                    DAT_00618f20 + 0x4d);
        FUN__text__0046beb0(local_48,0x7f2,iVar3 % 0x14 + -10,iVar4,uVar6,puVar7);
        local_30 = local_30 + 1;
      }
    }
  }
LAB__text__004847dc:
  local_8 = 0x4847ec;
  FUN__text__0056ce80();
  return;
}

