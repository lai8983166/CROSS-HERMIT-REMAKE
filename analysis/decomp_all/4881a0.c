
/* WARNING: Removing unreachable block (ram,0x004882fc) */

void __thiscall FUN__text__004881a0(int param_1,int param_2,int param_3,undefined4 *param_4)

{
  code *pcVar1;
  short sVar2;
  undefined2 uVar3;
  int iVar4;
  int iVar5;
  undefined4 *puVar6;
  undefined4 uVar7;
  undefined3 *puVar8;
  undefined4 local_e8 [16];
  char local_a8;
  int local_a4;
  int local_a0;
  int local_9c;
  int local_98;
  int local_94;
  int local_90;
  uint local_8c;
  int local_88;
  int local_84;
  undefined *local_80;
  undefined *local_7c;
  int local_78;
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
  
  puVar6 = local_e8;
  for (iVar4 = 0x39; iVar4 != 0; iVar4 = iVar4 + -1) {
    *puVar6 = 0xcccccccc;
    puVar6 = puVar6 + 1;
  }
  iVar4 = *(short *)(param_4 + 1) * 0x48;
  local_7c = &DAT_006c2dc8 + iVar4;
  local_a8 = *(char *)((int)param_4 + 7);
  local_8 = param_1;
  if (local_a8 == '\0') {
    *(char *)((int)param_4 + 7) = *(char *)((int)param_4 + 7) + '\x01';
    *(char *)(param_4 + 2) =
         (char)((int)((*(int *)(param_3 + 0x2ec) >> 0x10) +
                     (*(int *)(param_3 + 0x2ec) >> 0x1f & 0x1fU)) >> 5);
    *(char *)((int)param_4 + 9) =
         (char)((int)((*(int *)(param_3 + 0x2f0) >> 0x10) +
                     (*(int *)(param_3 + 0x2f0) >> 0x1f & 0xfU)) >> 4);
    FUN__text__0046beb0(param_3,0xc1f,0,0,0,param_4);
  }
  else if (local_a8 == '\x01') {
    *(char *)((int)param_4 + 7) = *(char *)((int)param_4 + 7) + '\x01';
    local_a0 = (int)*(short *)(&DAT_006b2da0 +
                              (uint)*(ushort *)(*(int *)(param_2 + 600) + 0xc) * 0x40);
    local_80 = &DAT_006c2dc8 + local_a0 * 0x48;
    local_8c = (uint)(byte)(&DAT_006c2dde)[iVar4] +
               ((uint)*(byte *)(*(int *)(param_2 + 600) + 10) * (uint)(byte)(&DAT_006c2ddf)[iVar4])
               / 100;
    if (0x20 < local_8c) {
      local_8c = 0x20;
    }
    iVar4 = *(int *)(param_1 + 0x80dd8 + (uint)*(byte *)((int)param_4 + 3) * 0x520);
    local_98 = (int)((iVar4 >> 0x10) + (iVar4 >> 0x1f & 0x1fU)) >> 5;
    iVar4 = *(int *)(param_1 + 0x80ddc + (uint)*(byte *)((int)param_4 + 3) * 0x520);
    local_9c = (int)((iVar4 >> 0x10) + (iVar4 >> 0x1f & 0xfU)) >> 4;
    FUN__text__004deaa0(param_2,&local_44);
    FUN__text__0046b3e0(param_2,&local_44);
    local_44 = (undefined2)
               (((int)*(short *)(local_7c + 0x22) *
                ((int)(((uint)*(byte *)(*(int *)(param_2 + 600) + 8) +
                        (uint)*(byte *)(*(int *)(param_2 + 600) + 4) +
                       (int)*(short *)(local_7c + 0x20)) *
                      (uint)*(byte *)(*(int *)(param_2 + 600) + 8)) / 100)) / 100);
    local_78 = (int)(((uint)*(byte *)(*(int *)(param_2 + 600) + 8) +
                      (uint)*(byte *)(*(int *)(param_2 + 600) + 4) +
                     (int)*(short *)(local_7c + 0x24)) *
                    (uint)*(byte *)(*(int *)(param_2 + 600) + 8)) / 100;
    local_42 = (undefined2)((*(short *)(local_7c + 0x26) * local_78) / 100);
    local_c = (int *)(local_8 + 0xdc8ec);
    local_88 = 0;
    for (local_84 = 0; local_84 != *local_c; local_84 = local_84 + 1) {
      local_a4 = local_c[local_84 + 1];
      if ((*(short *)(param_2 + 2) != *(short *)(local_a4 + 2)) &&
         (iVar4 = FUN__text__0048c950((int)*(short *)(param_4 + 1),param_2,local_a4), iVar4 != 0)) {
        local_90 = (int)((*(int *)(local_a4 + 0x2ec) >> 0x10) +
                        (*(int *)(local_a4 + 0x2ec) >> 0x1f & 0x1fU)) >> 5;
        local_94 = (int)((*(int *)(local_a4 + 0x2f0) >> 0x10) +
                        (*(int *)(local_a4 + 0x2f0) >> 0x1f & 0xfU)) >> 4;
        iVar4 = FUN__text__0043c1d0(local_98,local_9c,local_90,local_94,local_8c);
        if (iVar4 != 0) {
          FUN__text__004deaa0(local_a4,local_70);
          FUN__text__0046b3e0(local_a4,local_70);
          local_74 = FUN__text__004826f0(&local_44,local_70);
          if ((local_74 != 0) && (iVar4 = FUN__text__004692e0(local_a4), iVar4 != 0)) {
            local_74 = 1;
          }
          _local_14 = CONCAT13(2,CONCAT12((undefined1)local_74,(short)param_4[1]));
          _local_10 = CONCAT22(-local_1c,(short)param_4[2]);
          _local_18 = CONCAT13(*(undefined1 *)(local_a4 + 2),(int3)*param_4);
          sVar2 = FUN__text__00467e00("E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                      DAT_00618f5c + 0x4a);
          sVar2 = sVar2 % 0x28 + 0x14;
          local_18._0_2_ = sVar2;
          uVar3 = FUN__text__00415070((int)sVar2);
          _local_18 = CONCAT22(stack0xffffffea,uVar3);
          puVar8 = &local_18;
          uVar7 = 0;
          iVar4 = FUN__text__00467e00("E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                      DAT_00618f5c + 0x4d);
          iVar5 = iVar4 % 0x14 + -10;
          iVar4 = FUN__text__00467e00("E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                      DAT_00618f5c + 0x4d);
          FUN__text__0046beb0(local_a4,0xc20,iVar4 % 0x14 + -10,iVar5,uVar7,puVar8);
          local_88 = local_88 + 1;
        }
      }
    }
  }
  else if ((local_a8 == '\x02') &&
          (iVar4 = FUN__text__00424f80(&DAT_0059e0e8,
                                       "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                       DAT_00618f5c + 0x55,0), iVar4 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_8 = 0x4886b4;
  FUN__text__0056ce80();
  return;
}

