
/* WARNING: Removing unreachable block (ram,0x0048415d) */

void __thiscall FUN__text__00484080(int param_1,int param_2,undefined4 param_3,undefined4 *param_4)

{
  code *pcVar1;
  undefined2 uVar2;
  int iVar3;
  int iVar4;
  undefined4 *puVar5;
  undefined4 uVar6;
  undefined3 *puVar7;
  undefined4 local_88 [16];
  char local_48;
  int local_44;
  uint local_40;
  uint local_3c;
  int local_38;
  int local_34;
  uint local_30;
  int local_2c;
  int local_28;
  undefined *local_24;
  undefined4 local_20;
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
  
  puVar5 = local_88;
  for (iVar3 = 0x21; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar5 = 0xcccccccc;
    puVar5 = puVar5 + 1;
  }
  iVar3 = *(short *)(param_4 + 1) * 0x48;
  local_24 = &DAT_006c2dc8 + iVar3;
  local_48 = *(char *)((int)param_4 + 7);
  local_8 = param_1;
  if (local_48 == '\0') {
    *(char *)((int)param_4 + 7) = *(char *)((int)param_4 + 7) + '\x01';
    *(undefined1 *)(param_4 + 2) = *(undefined1 *)(param_2 + 0x4f0);
    *(undefined1 *)((int)param_4 + 9) = *(undefined1 *)(param_2 + 0x4f1);
  }
  else if (local_48 != '\x01') {
    if ((local_48 == '\x02') &&
       (iVar3 = FUN__text__00424f80(&DAT_0059daec,
                                    "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                    DAT_00618f1c + 0x47,0), iVar3 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    goto LAB__text__00484387;
  }
  *(char *)((int)param_4 + 7) = *(char *)((int)param_4 + 7) + '\x01';
  local_30 = (uint)(byte)(&DAT_006c2dde)[iVar3] +
             ((uint)*(byte *)(*(int *)(param_2 + 600) + 10) * (uint)(byte)(&DAT_006c2ddf)[iVar3]) /
             100;
  if (0x20 < local_30) {
    local_30 = 0x20;
  }
  local_3c = (uint)*(byte *)(param_4 + 2);
  local_40 = (uint)*(byte *)((int)param_4 + 9);
  local_1c = (int)*(short *)(&DAT_006c2de8 + iVar3) +
             (int)((uint)*(byte *)(*(int *)(param_2 + 600) + 7) *
                  (int)*(short *)(&DAT_006c2dea + iVar3)) / 100;
  local_20 = 1;
  local_c = (int *)(param_1 + 0xdc8ec);
  local_2c = 0;
  for (local_28 = 0; local_28 != *local_c; local_28 = local_28 + 1) {
    local_44 = local_c[local_28 + 1];
    iVar3 = FUN__text__0048c950((int)*(short *)(param_4 + 1),param_2,local_44);
    if (iVar3 != 0) {
      local_34 = (int)((*(int *)(local_44 + 0x2ec) >> 0x10) +
                      (*(int *)(local_44 + 0x2ec) >> 0x1f & 0x1fU)) >> 5;
      local_38 = (int)((*(int *)(local_44 + 0x2f0) >> 0x10) +
                      (*(int *)(local_44 + 0x2f0) >> 0x1f & 0xfU)) >> 4;
      iVar3 = FUN__text__0043c1d0(local_3c,local_40,local_34,local_38,local_30);
      if (iVar3 != 0) {
        _local_14 = CONCAT13(2,CONCAT12((undefined1)local_20,(short)param_4[1]));
        _local_10 = CONCAT22((undefined2)local_1c,(short)param_4[2]);
        _local_18 = CONCAT13(*(undefined1 *)(local_44 + 2),(int3)*param_4);
        iVar3 = FUN__text__00467e00("E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                    DAT_00618f1c + 0x3b);
        local_18._0_2_ = (short)(iVar3 % 0x32) + 10;
        if ((ushort)*(byte *)((int)param_4 + 3) == *(ushort *)(local_44 + 2)) {
          local_18._0_2_ = 0;
        }
        uVar2 = FUN__text__00415070((int)(short)local_18);
        _local_18 = CONCAT22(stack0xffffffea,uVar2);
        puVar7 = &local_18;
        uVar6 = 0;
        iVar3 = FUN__text__00467e00("E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                    DAT_00618f1c + 0x3f);
        iVar4 = iVar3 % 0x14 + -10;
        iVar3 = FUN__text__00467e00("E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                    DAT_00618f1c + 0x3f);
        FUN__text__0046beb0(local_44,0xbd8,iVar3 % 0x14 + -10,iVar4,uVar6,puVar7);
        local_2c = local_2c + 1;
      }
    }
  }
LAB__text__00484387:
  local_8 = 0x484397;
  FUN__text__0056ce80();
  return;
}

