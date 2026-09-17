
/* WARNING: Removing unreachable block (ram,0x00482ff1) */

void FUN__text__00482ef0(int param_1,int param_2,undefined4 *param_3)

{
  short sVar1;
  undefined2 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_e0 [16];
  int local_a0;
  int local_9c;
  int local_98;
  int local_94;
  int local_90;
  int local_8c;
  uint local_88;
  int local_84;
  int local_80;
  undefined *local_7c;
  undefined *local_78;
  int local_74;
  undefined1 local_70 [44];
  short local_44;
  short sStack_42;
  short local_40;
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
  
  puVar4 = local_e0;
  for (iVar3 = 0x37; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_78 = &DAT_006c2e58;
  local_9c = (int)*(short *)(&DAT_006b2da0 + (uint)*(ushort *)(*(int *)(param_1 + 600) + 0xc) * 0x40
                            );
  local_7c = &DAT_006c2dc8 + local_9c * 0x48;
  local_88 = (uint)*(byte *)(*(int *)(param_1 + 600) + 0x44) + (uint)DAT_006c2e6e +
             ((uint)*(byte *)(*(int *)(param_1 + 600) + 4) * (uint)DAT_006c2e6f) / 100;
  if (0x20 < local_88) {
    local_88 = 0x20;
  }
  local_94 = (int)((*(int *)(param_2 + 0x2ec) >> 0x10) + (*(int *)(param_2 + 0x2ec) >> 0x1f & 0x1fU)
                  ) >> 5;
  local_98 = (int)((*(int *)(param_2 + 0x2f0) >> 0x10) + (*(int *)(param_2 + 0x2f0) >> 0x1f & 0xfU))
             >> 4;
  FUN__text__004deaa0(param_1,&local_44);
  FUN__text__0046b3e0(param_1,&local_44);
  local_44 = local_44 + *(short *)(local_78 + 0x20) +
             (short)((int)((uint)*(byte *)(*(int *)(param_1 + 600) + 4) *
                          (int)*(short *)(local_78 + 0x22)) / 100);
  sStack_42 = sStack_42 + *(short *)(local_78 + 0x24) +
              (short)((int)((uint)*(byte *)(*(int *)(param_1 + 600) + 4) *
                           (int)*(short *)(local_78 + 0x26)) / 100);
  local_40 = local_40 + (ushort)(byte)local_78[0x14] +
             (short)(((uint)*(byte *)(*(int *)(param_1 + 600) + 4) * (uint)(byte)local_78[0x15]) /
                    100);
  local_c = (int *)(local_8 + 0xdc8ec);
  local_84 = 0;
  for (local_80 = 0; local_80 != *local_c; local_80 = local_80 + 1) {
    local_a0 = local_c[local_80 + 1];
    iVar3 = FUN__text__0046ae20(param_1,local_a0);
    if (iVar3 != 0) {
      local_8c = (int)((*(int *)(local_a0 + 0x2ec) >> 0x10) +
                      (*(int *)(local_a0 + 0x2ec) >> 0x1f & 0x1fU)) >> 5;
      local_90 = (int)((*(int *)(local_a0 + 0x2f0) >> 0x10) +
                      (*(int *)(local_a0 + 0x2f0) >> 0x1f & 0xfU)) >> 4;
      iVar3 = FUN__text__0043c1d0(local_94,local_98,local_8c,local_90,local_88);
      if (iVar3 != 0) {
        FUN__text__004deaa0(local_a0,local_70);
        FUN__text__0046b3e0(local_a0,local_70);
        local_74 = FUN__text__004824d0(&local_44,local_70);
        if ((local_74 != 0) && (iVar3 = FUN__text__004692e0(local_a0), iVar3 != 0)) {
          local_74 = 1;
        }
        _local_14 = CONCAT13(2,CONCAT12((undefined1)local_74,(short)param_3[1]));
        _local_10 = CONCAT22(-local_1c,(short)param_3[2]);
        _local_18 = CONCAT13(*(undefined1 *)(local_a0 + 2),(int3)*param_3);
        sVar1 = FUN__text__00467e00("E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                    DAT_00618f0c + 0x3e);
        local_18._0_2_ = sVar1 % 0x32 + 10;
        if ((ushort)*(byte *)((int)param_3 + 3) == *(ushort *)(local_a0 + 2)) {
          local_18._0_2_ = 0;
        }
        uVar2 = FUN__text__00415070((int)(short)local_18);
        _local_18 = CONCAT22(stack0xffffffea,uVar2);
        FUN__text__00482d60((int)*(short *)(param_3 + 1),local_74,param_1,local_a0,&local_18);
        local_84 = local_84 + 1;
      }
    }
  }
  local_8 = 0x4832fc;
  FUN__text__0056ce80();
  return;
}

