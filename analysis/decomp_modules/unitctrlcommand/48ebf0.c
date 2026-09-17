
void FUN__text__0048ebf0(int param_1,int param_2)

{
  code *pcVar1;
  uint uVar2;
  ushort uVar3;
  int iVar4;
  ushort uVar5;
  undefined4 *puVar6;
  undefined4 local_5c [16];
  int local_1c;
  uint local_18;
  ushort local_14;
  undefined2 uStack_12;
  ushort local_10;
  undefined2 uStack_e;
  ushort local_c;
  undefined2 uStack_a;
  undefined4 local_8;
  
  puVar6 = local_5c;
  for (iVar4 = 0x16; iVar4 != 0; iVar4 = iVar4 + -1) {
    *puVar6 = 0xcccccccc;
    puVar6 = puVar6 + 1;
  }
  iVar4 = FUN__text__004693b0(param_1);
  if (iVar4 == 0) {
    if (((int)*(char *)(param_1 + 0x260) != (uint)*(byte *)(param_2 + 2)) &&
       (iVar4 = FUN__text__00424f80("wk->appear.cnt == comw->appear_cnt",
                                    "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlCommand.cpp",
                                    DAT_00618fb0 + 6,0), iVar4 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    for (local_18 = 0; (local_18 != 0x14 && (*(short *)(param_1 + 0x262 + local_18 * 2) != -1));
        local_18 = local_18 + 1) {
    }
    if ((local_18 == 0x14) &&
       (iVar4 = FUN__text__00424f80("(i!=20)",
                                    "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlCommand.cpp",
                                    DAT_00618fb0 + 0xb,0), iVar4 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    uVar2 = local_18;
    local_1c = local_18;
    for (local_18 = 0; local_18 != *(byte *)(param_2 + 3); local_18 = local_18 + 1) {
      uVar5 = ((ushort)*(byte *)(param_2 + 4) & (ushort)(1 << (7U - (char)local_18 & 0x1f))) <<
              ((char)local_18 + 1U & 0x1f);
      _local_c = CONCAT22(uStack_a,uVar5);
      uVar3 = (ushort)*(byte *)(param_2 + local_18 + 5);
      _local_10 = CONCAT22(uStack_e,uVar3);
      uVar5 = uVar5 | uVar3;
      _local_14 = CONCAT22(uStack_12,uVar5);
      if (uVar5 == 0) {
        *(undefined2 *)(param_1 + 0x262 + (uVar2 + local_18) * 2) = 0xffff;
      }
      else {
        *(ushort *)(param_1 + 0x262 + (uVar2 + local_18) * 2) = uVar5 - 1;
      }
    }
  }
  local_8 = 0x48ed90;
  FUN__text__0056ce80();
  return;
}

