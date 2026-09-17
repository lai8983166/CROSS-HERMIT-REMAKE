
/* WARNING: Removing unreachable block (ram,0x0048499c) */

void __thiscall FUN__text__00484810(int param_1,int param_2,int param_3,undefined4 *param_4)

{
  code *pcVar1;
  short sVar2;
  undefined2 uVar3;
  int iVar4;
  int iVar5;
  undefined4 *puVar6;
  undefined4 uVar7;
  undefined3 *puVar8;
  undefined4 local_e4 [16];
  char local_a4;
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
  short local_42;
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
  
  puVar6 = local_e4;
  for (iVar4 = 0x38; iVar4 != 0; iVar4 = iVar4 + -1) {
    *puVar6 = 0xcccccccc;
    puVar6 = puVar6 + 1;
  }
  local_78 = &DAT_006c36c8;
  local_a4 = *(char *)((int)param_4 + 7);
  local_8 = param_1;
  if (local_a4 == '\0') {
    *(char *)((int)param_4 + 7) = *(char *)((int)param_4 + 7) + '\x01';
    *(char *)(param_4 + 2) =
         (char)((int)((*(int *)(param_3 + 0x2ec) >> 0x10) +
                     (*(int *)(param_3 + 0x2ec) >> 0x1f & 0x1fU)) >> 5);
    *(char *)((int)param_4 + 9) =
         (char)((int)((*(int *)(param_3 + 0x2f0) >> 0x10) +
                     (*(int *)(param_3 + 0x2f0) >> 0x1f & 0xfU)) >> 4);
    FUN__text__0046beb0(param_3,0xbde,0,0,0,param_4);
  }
  else if (local_a4 == '\x01') {
    *(char *)((int)param_4 + 7) = *(char *)((int)param_4 + 7) + '\x01';
    local_9c = (int)*(short *)(&DAT_006b2da0 +
                              (uint)*(ushort *)(*(int *)(param_2 + 600) + 0xc) * 0x40);
    local_7c = &DAT_006c2dc8 + local_9c * 0x48;
    local_88 = (uint)(byte)(&DAT_006c2dde)[local_9c * 0x48] + (uint)DAT_006c36de +
               ((uint)*(byte *)(*(int *)(param_2 + 600) + 10) * (uint)DAT_006c36df) / 100;
    if (0x20 < local_88) {
      local_88 = 0x20;
    }
    iVar4 = *(int *)(param_1 + 0x80dd8 + (uint)*(byte *)((int)param_4 + 3) * 0x520);
    local_94 = (int)((iVar4 >> 0x10) + (iVar4 >> 0x1f & 0x1fU)) >> 5;
    iVar4 = *(int *)(param_1 + 0x80ddc + (uint)*(byte *)((int)param_4 + 3) * 0x520);
    local_98 = (int)((iVar4 >> 0x10) + (iVar4 >> 0x1f & 0xfU)) >> 4;
    FUN__text__004deaa0(param_2,&local_44);
    FUN__text__0046b3e0(param_2,&local_44);
    local_44 = *(short *)(local_78 + 0x20) +
               (short)((int)((uint)*(byte *)(*(int *)(param_2 + 600) + 7) *
                            (int)*(short *)(local_78 + 0x22)) / 100);
    local_42 = *(short *)(local_78 + 0x24) +
               (short)((int)((uint)*(byte *)(*(int *)(param_2 + 600) + 7) *
                            (int)*(short *)(local_78 + 0x26)) / 100);
    local_c = (int *)(local_8 + 0xdc8ec);
    local_84 = 0;
    for (local_80 = 0; local_80 != *local_c; local_80 = local_80 + 1) {
      local_a0 = local_c[local_80 + 1];
      iVar4 = FUN__text__0046ae20(param_2,local_a0);
      if (iVar4 != 0) {
        local_8c = (int)((*(int *)(local_a0 + 0x2ec) >> 0x10) +
                        (*(int *)(local_a0 + 0x2ec) >> 0x1f & 0x1fU)) >> 5;
        local_90 = (int)((*(int *)(local_a0 + 0x2f0) >> 0x10) +
                        (*(int *)(local_a0 + 0x2f0) >> 0x1f & 0xfU)) >> 4;
        if (((ushort)*(byte *)((int)param_4 + 3) != *(ushort *)(local_a0 + 2)) &&
           (iVar4 = FUN__text__0043c1d0(local_94,local_98,local_8c,local_90,local_88), iVar4 != 0))
        {
          FUN__text__004deaa0(local_a0,local_70);
          FUN__text__0046b3e0(local_a0,local_70);
          local_74 = FUN__text__004826f0(&local_44,local_70);
          if ((local_74 != 0) && (iVar4 = FUN__text__004692e0(local_a0), iVar4 != 0)) {
            local_74 = 1;
          }
          _local_14 = CONCAT13(2,CONCAT12((undefined1)local_74,(short)param_4[1]));
          _local_10 = CONCAT22(-local_1c,(short)param_4[2]);
          _local_18 = CONCAT13(*(undefined1 *)(local_a0 + 2),(int3)*param_4);
          sVar2 = FUN__text__00467e00("E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                      DAT_00618f24 + 0x48);
          sVar2 = sVar2 % 0x32 + 10;
          local_18._0_2_ = sVar2;
          uVar3 = FUN__text__00415070((int)sVar2);
          _local_18 = CONCAT22(stack0xffffffea,uVar3);
          puVar8 = &local_18;
          uVar7 = 0;
          iVar4 = FUN__text__00467e00("E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                      DAT_00618f24 + 0x4b);
          iVar5 = iVar4 % 0x14 + -10;
          iVar4 = FUN__text__00467e00("E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                      DAT_00618f24 + 0x4b);
          FUN__text__0046beb0(local_a0,0xbdf,iVar4 % 0x14 + -10,iVar5,uVar7,puVar8);
          local_84 = local_84 + 1;
        }
      }
    }
  }
  else if ((local_a4 == '\x02') &&
          (iVar4 = FUN__text__00424f80(&DAT_0059dbd4,
                                       "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                       DAT_00618f24 + 0x53,0), iVar4 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_8 = 0x484ce0;
  FUN__text__0056ce80();
  return;
}

