
/* WARNING: Removing unreachable block (ram,0x00485c89) */

void __thiscall FUN__text__00485bd0(int param_1,int param_2,undefined4 param_3,undefined4 *param_4)

{
  code *pcVar1;
  undefined2 uVar2;
  int iVar3;
  int iVar4;
  undefined4 *puVar5;
  undefined4 uVar6;
  undefined3 *puVar7;
  undefined4 local_80 [16];
  char local_40;
  int local_3c;
  int local_38;
  int local_34;
  int local_30;
  int local_2c;
  uint local_28;
  int local_24;
  int local_20;
  undefined *local_1c;
  undefined3 local_18;
  undefined1 uStack_15;
  undefined2 local_14;
  undefined1 uStack_12;
  undefined1 uStack_11;
  uint local_10;
  int *local_c;
  int local_8;
  
  puVar5 = local_80;
  for (iVar3 = 0x1f; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar5 = 0xcccccccc;
    puVar5 = puVar5 + 1;
  }
  iVar3 = *(short *)(param_4 + 1) * 0x48;
  local_1c = &DAT_006c2dc8 + iVar3;
  local_40 = *(char *)((int)param_4 + 7);
  local_8 = param_1;
  if (local_40 == '\0') {
    *(char *)((int)param_4 + 7) = *(char *)((int)param_4 + 7) + '\x01';
  }
  else if (local_40 != '\x01') {
    if ((local_40 == '\x02') &&
       (iVar3 = FUN__text__00424f80(&DAT_0059de38,
                                    "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                    DAT_00618f38 + 0x3a,0), iVar3 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    goto LAB__text__00485eb2;
  }
  *(char *)((int)param_4 + 7) = *(char *)((int)param_4 + 7) + '\x01';
  local_28 = (uint)(byte)(&DAT_006c2dde)[iVar3] +
             ((uint)*(byte *)(*(int *)(param_2 + 600) + 10) * (uint)(byte)(&DAT_006c2ddf)[iVar3]) /
             100;
  if (0x20 < local_28) {
    local_28 = 0x20;
  }
  iVar3 = *(int *)(param_1 + 0x80dd8 + (uint)*(byte *)((int)param_4 + 3) * 0x520);
  local_34 = (int)((iVar3 >> 0x10) + (iVar3 >> 0x1f & 0x1fU)) >> 5;
  iVar3 = *(int *)(param_1 + 0x80ddc + (uint)*(byte *)((int)param_4 + 3) * 0x520);
  local_38 = (int)((iVar3 >> 0x10) + (iVar3 >> 0x1f & 0xfU)) >> 4;
  local_c = (int *)(param_1 + 0xdc8ec);
  local_24 = 0;
  for (local_20 = 0; local_20 != *local_c; local_20 = local_20 + 1) {
    local_3c = local_c[local_20 + 1];
    iVar3 = FUN__text__0048c950((int)*(short *)(param_4 + 1),param_2,local_3c);
    if (iVar3 != 0) {
      local_2c = (int)((*(int *)(local_3c + 0x2ec) >> 0x10) +
                      (*(int *)(local_3c + 0x2ec) >> 0x1f & 0x1fU)) >> 5;
      local_30 = (int)((*(int *)(local_3c + 0x2f0) >> 0x10) +
                      (*(int *)(local_3c + 0x2f0) >> 0x1f & 0xfU)) >> 4;
      iVar3 = FUN__text__0043c1d0(local_34,local_38,local_2c,local_30,local_28);
      if (iVar3 != 0) {
        _local_14 = CONCAT13(2,CONCAT12(1,(short)param_4[1]));
        local_10 = param_4[2] & 0xffff;
        _local_18 = CONCAT13(*(undefined1 *)(local_3c + 2),(int3)*param_4);
        iVar3 = FUN__text__00467e00("E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                    DAT_00618f38 + 0x2b);
        local_18._0_2_ = (short)(iVar3 % 0x32) + 10;
        if ((ushort)*(byte *)((int)param_4 + 3) == *(ushort *)(local_3c + 2)) {
          local_18._0_2_ = 0;
        }
        uVar2 = FUN__text__00415070((int)(short)local_18);
        _local_18 = CONCAT22(stack0xffffffea,uVar2);
        puVar7 = &local_18;
        uVar6 = 0;
        iVar3 = FUN__text__00467e00("E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                    DAT_00618f38 + 0x2f);
        iVar4 = iVar3 % 0x14 + -10;
        iVar3 = FUN__text__00467e00("E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                    DAT_00618f38 + 0x2f);
        FUN__text__0046beb0(local_3c,0xbfa,iVar3 % 0x14 + -10,iVar4,uVar6,puVar7);
        local_24 = local_24 + 1;
      }
    }
  }
LAB__text__00485eb2:
  local_8 = 0x485ebf;
  FUN__text__0056ce80();
  return;
}

