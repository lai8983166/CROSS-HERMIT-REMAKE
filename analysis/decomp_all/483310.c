
/* WARNING: Removing unreachable block (ram,0x0048341a) */

void __thiscall FUN__text__00483310(int param_1,int param_2,undefined4 param_3,undefined4 *param_4)

{
  code *pcVar1;
  undefined2 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_e4 [16];
  char local_a4;
  int local_a0;
  int local_9c;
  undefined *local_98;
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
  
  puVar4 = local_e4;
  for (iVar3 = 0x38; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  iVar3 = *(short *)(param_4 + 1) * 0x48;
  local_78 = &DAT_006c2dc8 + iVar3;
  local_a4 = *(char *)((int)param_4 + 7);
  local_8 = param_1;
  if (local_a4 == '\0') {
    *(char *)((int)param_4 + 7) = *(char *)((int)param_4 + 7) + '\x01';
  }
  else if (local_a4 != '\x01') {
    if ((local_a4 == '\x02') &&
       (iVar3 = FUN__text__00424f80(&DAT_0059da04,
                                    "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                    DAT_00618f10 + 0x4d,0), iVar3 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    goto LAB__text__00483778;
  }
  *(char *)((int)param_4 + 7) = *(char *)((int)param_4 + 7) + '\x01';
  local_9c = (int)*(short *)(&DAT_006b2da0 + (uint)*(ushort *)(*(int *)(param_2 + 600) + 0xc) * 0x40
                            );
  local_98 = &DAT_006c2dc8 + local_9c * 0x48;
  local_84 = (uint)(byte)(&DAT_006c2dde)[local_9c * 0x48] + (uint)(byte)(&DAT_006c2dde)[iVar3] +
             ((uint)*(byte *)(*(int *)(param_2 + 600) + 4) * (uint)(byte)(&DAT_006c2ddf)[iVar3]) /
             100;
  if (0x20 < local_84) {
    local_84 = 0x20;
  }
  iVar3 = *(int *)(param_1 + 0x80dd8 + (uint)*(byte *)((int)param_4 + 3) * 0x520);
  local_90 = (int)((iVar3 >> 0x10) + (iVar3 >> 0x1f & 0x1fU)) >> 5;
  iVar3 = *(int *)(param_1 + 0x80ddc + (uint)*(byte *)((int)param_4 + 3) * 0x520);
  local_94 = (int)((iVar3 >> 0x10) + (iVar3 >> 0x1f & 0xfU)) >> 4;
  FUN__text__004deaa0(param_2,&local_44);
  FUN__text__0046b3e0(param_2,&local_44);
  local_44 = local_44 + *(short *)(local_78 + 0x20) +
             (short)((int)((uint)*(byte *)(*(int *)(param_2 + 600) + 4) *
                          (int)*(short *)(local_78 + 0x22)) / 100);
  sStack_42 = sStack_42 + *(short *)(local_78 + 0x24) +
              (short)((int)((uint)*(byte *)(*(int *)(param_2 + 600) + 4) *
                           (int)*(short *)(local_78 + 0x26)) / 100);
  local_40 = local_40 + (ushort)(byte)local_78[0x14] +
             (short)(((uint)*(byte *)(*(int *)(param_2 + 600) + 4) * (uint)(byte)local_78[0x15]) /
                    100);
  local_c = (int *)(local_8 + 0xdc8ec);
  local_80 = 0;
  for (local_7c = 0; local_7c != *local_c; local_7c = local_7c + 1) {
    local_a0 = local_c[local_7c + 1];
    if ((*(short *)(param_2 + 2) != *(short *)(local_a0 + 2)) &&
       (iVar3 = FUN__text__0048c950((int)*(short *)(param_4 + 1),param_2,local_a0), iVar3 != 0)) {
      local_88 = (int)((*(int *)(local_a0 + 0x2ec) >> 0x10) +
                      (*(int *)(local_a0 + 0x2ec) >> 0x1f & 0x1fU)) >> 5;
      local_8c = (int)((*(int *)(local_a0 + 0x2f0) >> 0x10) +
                      (*(int *)(local_a0 + 0x2f0) >> 0x1f & 0xfU)) >> 4;
      iVar3 = FUN__text__0043c1d0(local_90,local_94,local_88,local_8c,local_84);
      if (iVar3 != 0) {
        FUN__text__004deaa0(local_a0,local_70);
        FUN__text__0046b3e0(local_a0,local_70);
        local_74 = FUN__text__004824d0(&local_44,local_70);
        if ((local_74 != 0) && (iVar3 = FUN__text__004692e0(local_a0), iVar3 != 0)) {
          local_74 = 1;
        }
        _local_14 = CONCAT13(2,CONCAT12((undefined1)local_74,(short)param_4[1]));
        _local_10 = CONCAT22(-local_1c,(short)param_4[2]);
        _local_18 = CONCAT13(*(undefined1 *)(local_a0 + 2),(int3)*param_4);
        iVar3 = FUN__text__00467e00("E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                    DAT_00618f10 + 0x41);
        local_18._0_2_ = (short)(iVar3 % 0x1e) + 10;
        if ((ushort)*(byte *)((int)param_4 + 3) == *(ushort *)(local_a0 + 2)) {
          local_18._0_2_ = 0;
        }
        uVar2 = FUN__text__00415070((int)(short)local_18);
        _local_18 = CONCAT22(stack0xffffffea,uVar2);
        FUN__text__00482d60((int)*(short *)(param_4 + 1),local_74,param_2,local_a0,&local_18);
        local_80 = local_80 + 1;
      }
    }
  }
LAB__text__00483778:
  local_8 = 0x483788;
  FUN__text__0056ce80();
  return;
}

