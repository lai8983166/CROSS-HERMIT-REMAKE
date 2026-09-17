
/* WARNING: Removing unreachable block (ram,0x0048ae1c) */

void FUN__text__0048adc0(int param_1,undefined4 param_2,undefined4 *param_3)

{
  short sVar1;
  undefined2 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_d4 [16];
  int local_94;
  int local_90;
  int local_8c;
  int local_88;
  int local_84;
  uint local_80;
  int local_7c;
  undefined *local_78;
  int local_74;
  undefined1 local_70 [44];
  undefined1 local_44 [40];
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
  
  puVar4 = local_d4;
  for (iVar3 = 0x34; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_78 = &DAT_006c2dc8 + *(short *)(param_3 + 1) * 0x48;
  local_80 = (uint)*(byte *)(*(int *)(param_1 + 600) + 0x37);
  if (0x20 < local_80) {
    local_80 = 0x20;
  }
  local_8c = (int)((*(int *)(param_1 + 0x2ec) >> 0x10) + (*(int *)(param_1 + 0x2ec) >> 0x1f & 0x1fU)
                  ) >> 5;
  local_90 = (int)((*(int *)(param_1 + 0x2f0) >> 0x10) + (*(int *)(param_1 + 0x2f0) >> 0x1f & 0xfU))
             >> 4;
  FUN__text__004deaa0(param_1,local_44);
  FUN__text__0046b3e0(param_1,local_44);
  local_c = (int *)(local_8 + 0xdc8ec);
  for (local_7c = 0; local_7c != *local_c; local_7c = local_7c + 1) {
    local_94 = local_c[local_7c + 1];
    iVar3 = FUN__text__0046ae20(param_1,local_94);
    if (iVar3 != 0) {
      local_84 = (int)((*(int *)(local_94 + 0x2ec) >> 0x10) +
                      (*(int *)(local_94 + 0x2ec) >> 0x1f & 0x1fU)) >> 5;
      local_88 = (int)((*(int *)(local_94 + 0x2f0) >> 0x10) +
                      (*(int *)(local_94 + 0x2f0) >> 0x1f & 0xfU)) >> 4;
      iVar3 = FUN__text__0043c1d0(local_8c,local_90,local_84,local_88,local_80);
      if (iVar3 != 0) {
        FUN__text__004deaa0(local_94,local_70);
        FUN__text__0046b3e0(local_94,local_70);
        local_74 = FUN__text__004824d0(local_44,local_70);
        if ((local_74 != 0) && (iVar3 = FUN__text__004692e0(local_94), iVar3 != 0)) {
          local_74 = 1;
        }
        _local_14 = CONCAT13(2,CONCAT12((undefined1)local_74,(short)param_3[1]));
        _local_10 = CONCAT22(-local_1c,(short)param_3[2]);
        _local_18 = CONCAT13(*(undefined1 *)(local_94 + 2),(int3)*param_3);
        sVar1 = FUN__text__00467e00("E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                    DAT_00618f74 + 0x2d);
        sVar1 = sVar1 % 0x32 + 10;
        local_18._0_2_ = sVar1;
        uVar2 = FUN__text__00415070((int)sVar1);
        _local_18 = CONCAT22(stack0xffffffea,uVar2);
        FUN__text__00482d60((int)*(short *)(param_3 + 1),local_74,param_1,local_94,&local_18);
        FUN__text__0048b2e0(*(undefined1 *)(*(int *)(param_1 + 600) + 0x45),
                            (int)*(short *)(param_3 + 1),param_1,local_94,local_44,local_70);
      }
    }
  }
  local_8 = 0x48b072;
  FUN__text__0056ce80();
  return;
}

