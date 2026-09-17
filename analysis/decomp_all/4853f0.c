
/* WARNING: Removing unreachable block (ram,0x00485534) */

void __thiscall FUN__text__004853f0(int param_1,int param_2,int param_3,undefined4 *param_4)

{
  code *pcVar1;
  short sVar2;
  undefined2 uVar3;
  int iVar4;
  int iVar5;
  undefined4 *puVar6;
  undefined4 uVar7;
  undefined3 *puVar8;
  undefined4 local_dc [16];
  char local_9c;
  int local_98;
  int local_94;
  int local_90;
  int local_8c;
  int local_88;
  uint local_84;
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
  
  puVar6 = local_dc;
  for (iVar4 = 0x36; iVar4 != 0; iVar4 = iVar4 + -1) {
    *puVar6 = 0xcccccccc;
    puVar6 = puVar6 + 1;
  }
  local_78 = &DAT_006c3c68;
  local_9c = *(char *)((int)param_4 + 7);
  local_8 = param_1;
  if (local_9c == '\0') {
    *(char *)((int)param_4 + 7) = *(char *)((int)param_4 + 7) + '\x01';
    *(char *)(param_4 + 2) =
         (char)((int)((*(int *)(param_3 + 0x2ec) >> 0x10) +
                     (*(int *)(param_3 + 0x2ec) >> 0x1f & 0x1fU)) >> 5);
    *(char *)((int)param_4 + 9) =
         (char)((int)((*(int *)(param_3 + 0x2f0) >> 0x10) +
                     (*(int *)(param_3 + 0x2f0) >> 0x1f & 0x1fU)) >> 5);
    FUN__text__0046beb0(param_3,0xbf5,0,0,0,param_4);
  }
  else if (local_9c == '\x01') {
    *(char *)((int)param_4 + 7) = *(char *)((int)param_4 + 7) + '\x01';
    local_84 = (uint)DAT_006c3c7e +
               ((uint)*(byte *)(*(int *)(param_2 + 600) + 10) * (uint)DAT_006c3c7f) / 100;
    if (0x20 < local_84) {
      local_84 = 0x20;
    }
    iVar4 = *(int *)(param_1 + 0x80dd8 + (uint)*(byte *)((int)param_4 + 3) * 0x520);
    local_90 = (int)((iVar4 >> 0x10) + (iVar4 >> 0x1f & 0x1fU)) >> 5;
    iVar4 = *(int *)(param_1 + 0x80ddc + (uint)*(byte *)((int)param_4 + 3) * 0x520);
    local_94 = (int)((iVar4 >> 0x10) + (iVar4 >> 0x1f & 0xfU)) >> 4;
    FUN__text__004deaa0(param_2,&local_44);
    FUN__text__0046b3e0(param_2,&local_44);
    local_44 = (undefined2)
               ((((int)(((uint)*(byte *)(*(int *)(param_2 + 600) + 8) +
                         (uint)*(byte *)(*(int *)(param_2 + 600) + 9) +
                        (int)*(short *)(local_78 + 0x20)) *
                       (uint)*(byte *)(*(int *)(param_2 + 600) + 8)) / 100) *
                (int)*(short *)(local_78 + 0x22)) / 100);
    local_42 = (undefined2)
               ((((int)(((uint)*(byte *)(*(int *)(param_2 + 600) + 8) +
                         (uint)*(byte *)(*(int *)(param_2 + 600) + 9) +
                        (int)*(short *)(local_78 + 0x24)) *
                       (uint)*(byte *)(*(int *)(param_2 + 600) + 8)) / 100) *
                (int)*(short *)(local_78 + 0x26)) / 100);
    local_c = (int *)(local_8 + 0xdc8ec);
    local_80 = 0;
    for (local_7c = 0; local_7c != *local_c; local_7c = local_7c + 1) {
      local_98 = local_c[local_7c + 1];
      iVar4 = FUN__text__0046ae20(param_2,local_98);
      if (iVar4 != 0) {
        local_88 = (int)((*(int *)(local_98 + 0x2ec) >> 0x10) +
                        (*(int *)(local_98 + 0x2ec) >> 0x1f & 0x1fU)) >> 5;
        local_8c = (int)((*(int *)(local_98 + 0x2f0) >> 0x10) +
                        (*(int *)(local_98 + 0x2f0) >> 0x1f & 0xfU)) >> 4;
        if (((ushort)*(byte *)((int)param_4 + 3) != *(ushort *)(local_98 + 2)) &&
           (iVar4 = FUN__text__0043c1d0(local_90,local_94,local_88,local_8c,local_84), iVar4 != 0))
        {
          FUN__text__004deaa0(local_98,local_70);
          FUN__text__0046b3e0(local_98,local_70);
          local_74 = FUN__text__004826f0(&local_44,local_70);
          if ((local_74 != 0) && (iVar4 = FUN__text__004692e0(local_98), iVar4 != 0)) {
            local_74 = 1;
          }
          _local_14 = CONCAT13(2,CONCAT12((undefined1)local_74,(short)param_4[1]));
          _local_10 = CONCAT22(-local_1c,(short)param_4[2]);
          _local_18 = CONCAT13(*(undefined1 *)(local_98 + 2),(int3)*param_4);
          sVar2 = FUN__text__00467e00("E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                      DAT_00618f30 + 0x42);
          sVar2 = sVar2 % 0x32 + 10;
          local_18._0_2_ = sVar2;
          uVar3 = FUN__text__00415070((int)sVar2);
          _local_18 = CONCAT22(stack0xffffffea,uVar3);
          puVar8 = &local_18;
          uVar7 = 0;
          iVar4 = FUN__text__00467e00("E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                      DAT_00618f30 + 0x45);
          iVar5 = iVar4 % 0x14 + -10;
          iVar4 = FUN__text__00467e00("E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                      DAT_00618f30 + 0x45);
          FUN__text__0046beb0(local_98,0xbf6,iVar4 % 0x14 + -10,iVar5,uVar7,puVar8);
          local_80 = local_80 + 1;
        }
      }
    }
  }
  else if ((local_9c == '\x02') &&
          (iVar4 = FUN__text__00424f80(&DAT_0059dd40,
                                       "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                       DAT_00618f30 + 0x4f,0), iVar4 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_8 = 0x4858c3;
  FUN__text__0056ce80();
  return;
}

