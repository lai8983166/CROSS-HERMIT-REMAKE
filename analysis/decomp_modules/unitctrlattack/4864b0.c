
/* WARNING: Removing unreachable block (ram,0x00486622) */

void FUN__text__004864b0(int param_1,undefined4 param_2,undefined4 *param_3)

{
  code *pcVar1;
  short sVar2;
  undefined2 uVar3;
  int iVar4;
  int iVar5;
  undefined4 *puVar6;
  undefined4 uVar7;
  undefined3 *puVar8;
  undefined4 local_ec [16];
  char local_ac;
  int local_a8;
  uint local_a4;
  uint local_a0;
  int local_9c;
  int local_98;
  uint local_94;
  int local_90;
  int local_8c;
  int local_88;
  int local_84;
  int local_80;
  int local_7c;
  undefined *local_78;
  int local_74;
  undefined1 local_70 [44];
  undefined2 local_44;
  undefined2 local_42;
  short local_1c;
  undefined3 local_18;
  undefined1 uStack_15;
  undefined2 local_14;
  undefined1 uStack_12;
  undefined1 uStack_11;
  undefined2 local_10;
  short sStack_e;
  int *local_c;
  int local_8;
  
  puVar6 = local_ec;
  for (iVar4 = 0x3a; iVar4 != 0; iVar4 = iVar4 + -1) {
    *puVar6 = 0xcccccccc;
    puVar6 = puVar6 + 1;
  }
  local_78 = &DAT_006c3e60;
  local_ac = *(char *)((int)param_3 + 7);
  if (local_ac == '\0') {
    *(char *)((int)param_3 + 7) = *(char *)((int)param_3 + 7) + '\x01';
    *(undefined1 *)(param_3 + 2) = *(undefined1 *)(param_1 + 0x4f0);
    *(undefined1 *)((int)param_3 + 9) = *(undefined1 *)(param_1 + 0x4f1);
    local_84 = (int)((*(int *)(param_1 + 0x2ec) >> 0x10) +
                    (*(int *)(param_1 + 0x2ec) >> 0x1f & 0x1fU)) >> 5;
    local_88 = (int)((*(int *)(param_1 + 0x2f0) >> 0x10) +
                    (*(int *)(param_1 + 0x2f0) >> 0x1f & 0xfU)) >> 4;
    local_7c = ((uint)*(byte *)(param_1 + 0x4f0) - local_84) * 0x20 + 0x10;
    local_80 = ((uint)*(byte *)(param_1 + 0x4f1) - local_88) * 0x10 + 8;
    FUN__text__0046beb0(param_1,0xc00,local_7c,local_80,0,param_3);
  }
  else if (local_ac == '\x01') {
    *(char *)((int)param_3 + 7) = *(char *)((int)param_3 + 7) + '\x01';
    local_94 = (uint)DAT_006c3e76 +
               ((uint)*(byte *)(*(int *)(param_1 + 600) + 10) * (uint)DAT_006c3e77) / 100;
    if (0x20 < local_94) {
      local_94 = 0x20;
    }
    local_a0 = (uint)*(byte *)(param_3 + 2);
    local_a4 = (uint)*(byte *)((int)param_3 + 9);
    FUN__text__004deaa0(param_1,&local_44);
    FUN__text__0046b3e0(param_1,&local_44);
    local_44 = (undefined2)
               ((((int)(((uint)*(byte *)(*(int *)(param_1 + 600) + 8) +
                         (uint)*(byte *)(*(int *)(param_1 + 600) + 5) +
                        (int)*(short *)(local_78 + 0x20)) *
                       (uint)*(byte *)(*(int *)(param_1 + 600) + 8)) / 100) *
                (int)*(short *)(local_78 + 0x22)) / 100);
    local_42 = (undefined2)
               ((((int)(((uint)*(byte *)(*(int *)(param_1 + 600) + 8) +
                         (uint)*(byte *)(*(int *)(param_1 + 600) + 5) +
                        (int)*(short *)(local_78 + 0x24)) *
                       (uint)*(byte *)(*(int *)(param_1 + 600) + 8)) / 100) *
                (int)*(short *)(local_78 + 0x26)) / 100);
    local_c = (int *)(local_8 + 0xdc8ec);
    local_90 = 0;
    for (local_8c = 0; local_8c != *local_c; local_8c = local_8c + 1) {
      local_a8 = local_c[local_8c + 1];
      iVar4 = FUN__text__0046ae20(param_1,local_a8);
      if (iVar4 != 0) {
        local_98 = (int)((*(int *)(local_a8 + 0x2ec) >> 0x10) +
                        (*(int *)(local_a8 + 0x2ec) >> 0x1f & 0x1fU)) >> 5;
        local_9c = (int)((*(int *)(local_a8 + 0x2f0) >> 0x10) +
                        (*(int *)(local_a8 + 0x2f0) >> 0x1f & 0xfU)) >> 4;
        iVar4 = FUN__text__0043c1d0(local_a0,local_a4,local_98,local_9c,local_94);
        if (iVar4 != 0) {
          FUN__text__004deaa0(local_a8,local_70);
          FUN__text__0046b3e0(local_a8,local_70);
          local_74 = FUN__text__004826f0(&local_44,local_70);
          if ((local_74 != 0) && (iVar4 = FUN__text__004692e0(local_a8), iVar4 != 0)) {
            local_74 = 1;
          }
          _local_14 = CONCAT13(2,CONCAT12((undefined1)local_74,(short)param_3[1]));
          _local_10 = CONCAT22(-local_1c,(short)param_3[2]);
          _local_18 = CONCAT13(*(undefined1 *)(local_a8 + 2),(int3)*param_3);
          sVar2 = FUN__text__00467e00("E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                      DAT_00618f44 + 0x43);
          sVar2 = sVar2 % 0x32 + 10;
          local_18._0_2_ = sVar2;
          uVar3 = FUN__text__00415070((int)sVar2);
          _local_18 = CONCAT22(stack0xffffffea,uVar3);
          puVar8 = &local_18;
          uVar7 = 0;
          iVar4 = FUN__text__00467e00("E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                      DAT_00618f44 + 0x46);
          iVar5 = iVar4 % 0x14 + -10;
          iVar4 = FUN__text__00467e00("E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                      DAT_00618f44 + 0x46);
          FUN__text__0046beb0(local_a8,0xc01,iVar4 % 0x14 + -10,iVar5,uVar7,puVar8);
          local_90 = local_90 + 1;
        }
      }
    }
  }
  else if ((local_ac == '\x02') &&
          (iVar4 = FUN__text__00424f80(&DAT_0059df74,
                                       "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                       DAT_00618f44 + 0x4e,0), iVar4 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_8 = 0x48697e;
  FUN__text__0056ce80();
  return;
}

