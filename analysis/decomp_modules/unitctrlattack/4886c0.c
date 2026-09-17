
/* WARNING: Removing unreachable block (ram,0x004887f0) */

void FUN__text__004886c0(int param_1,undefined4 param_2,undefined4 *param_3)

{
  code *pcVar1;
  short sVar2;
  undefined2 uVar3;
  int iVar4;
  undefined4 *puVar5;
  undefined4 local_e0 [16];
  char local_a0;
  int local_9c;
  uint local_98;
  uint local_94;
  int local_90;
  int local_8c;
  uint local_88;
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
  
  puVar5 = local_e0;
  for (iVar4 = 0x37; iVar4 != 0; iVar4 = iVar4 + -1) {
    *puVar5 = 0xcccccccc;
    puVar5 = puVar5 + 1;
  }
  local_78 = &DAT_006c4370;
  local_a0 = *(char *)((int)param_3 + 7);
  if (local_a0 == '\0') {
    *(char *)((int)param_3 + 7) = *(char *)((int)param_3 + 7) + '\x01';
    local_7c = (int)((*(int *)(param_1 + 0x2ec) >> 0x10) +
                    (*(int *)(param_1 + 0x2ec) >> 0x1f & 0x1fU)) >> 5;
    local_80 = (int)((*(int *)(param_1 + 0x2f0) >> 0x10) +
                    (*(int *)(param_1 + 0x2f0) >> 0x1f & 0xfU)) >> 4;
    *(undefined1 *)(param_3 + 2) = (undefined1)local_7c;
    *(undefined1 *)((int)param_3 + 9) = (undefined1)local_80;
    FUN__text__0046beb0(param_1,0xc21,0,0,0,param_3);
  }
  else if (local_a0 == '\x01') {
    *(char *)((int)param_3 + 7) = *(char *)((int)param_3 + 7) + '\x01';
    local_88 = (uint)DAT_006c4386 +
               ((uint)*(byte *)(*(int *)(param_1 + 600) + 10) * (uint)DAT_006c4387) / 100;
    if (0x20 < local_88) {
      local_88 = 0x20;
    }
    local_94 = (uint)*(byte *)(param_3 + 2);
    local_98 = (uint)*(byte *)((int)param_3 + 9);
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
    for (local_84 = 0; local_84 != *local_c; local_84 = local_84 + 1) {
      local_9c = local_c[local_84 + 1];
      iVar4 = FUN__text__0046ae20(param_1,local_9c);
      if (iVar4 != 0) {
        local_8c = (int)((*(int *)(local_9c + 0x2ec) >> 0x10) +
                        (*(int *)(local_9c + 0x2ec) >> 0x1f & 0x1fU)) >> 5;
        local_90 = (int)((*(int *)(local_9c + 0x2f0) >> 0x10) +
                        (*(int *)(local_9c + 0x2f0) >> 0x1f & 0xfU)) >> 4;
        iVar4 = FUN__text__0043c1d0(local_94,local_98,local_8c,local_90,local_88);
        if (iVar4 != 0) {
          FUN__text__004deaa0(local_9c,local_70);
          FUN__text__0046b3e0(local_9c,local_70);
          local_74 = FUN__text__004826f0(&local_44,local_70);
          if ((local_74 != 0) && (iVar4 = FUN__text__004692e0(local_9c), iVar4 != 0)) {
            local_74 = 1;
          }
          _local_14 = CONCAT13(2,CONCAT12((undefined1)local_74,(short)param_3[1]));
          _local_10 = CONCAT22(-local_1c,(short)param_3[2]);
          _local_18 = CONCAT13(*(undefined1 *)(local_9c + 2),(int3)*param_3);
          sVar2 = FUN__text__00467e00("E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                      DAT_00618f60 + 0x3f);
          sVar2 = sVar2 % 0x32 + 10;
          local_18._0_2_ = sVar2;
          uVar3 = FUN__text__00415070((int)sVar2);
          _local_18 = CONCAT22(stack0xffffffea,uVar3);
          FUN__text__0046beb0(local_9c,0xc22,0,0,0,&local_18);
        }
      }
    }
  }
  else if ((local_a0 == '\x02') &&
          (iVar4 = FUN__text__00424f80(&DAT_0059e06c,
                                       "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                       DAT_00618f60 + 0x49,0), iVar4 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_8 = 0x488ae0;
  FUN__text__0056ce80();
  return;
}

