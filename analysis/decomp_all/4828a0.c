
void FUN__text__004828a0(undefined4 param_1,int param_2,int param_3,int param_4)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_54 [16];
  int local_14;
  int local_10;
  undefined *local_c;
  undefined4 local_8;
  
  puVar3 = local_54;
  for (iVar2 = 0x14; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if ((0x3b < param_3) &&
     (iVar2 = FUN__text__00424f80("no<60","E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                  DAT_00618f00 + 10,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_c = &DAT_006f4088 + param_3 * 0x10;
  if ((&DAT_006f408c)[param_3 * 0x10] == '\x01') {
    local_10 = (100 - (uint)*(byte *)(param_2 + 0xc)) + *(int *)(param_2 + 0x20);
  }
  else {
    local_10 = (100 - (uint)*(byte *)(param_2 + 10)) + *(int *)(param_2 + 0x20);
  }
  if (100 < local_10) {
    local_10 = 100;
  }
  local_14 = FUN__text__00467e00("E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAttack.cpp",
                                 DAT_00618f00 + 0x17);
  local_14 = local_14 % 100;
  if (((local_c[5] != '\x02') || (local_10 < local_14)) && (local_10 != 0)) {
    if (local_10 < 0) {
      local_10 = 100 - local_10;
    }
    *(int *)(param_4 + 8) = (*(int *)(param_4 + 8) * local_10) / 100;
    *(short *)(param_4 + 0xe) = (short)((*(short *)(param_4 + 0xe) * local_10) / 100);
    *(short *)(param_4 + 0xe) = -*(short *)(param_4 + 0xe);
    if (0xb7 < *(int *)(param_4 + 8)) goto LAB__text__00482a14;
  }
  *(undefined4 *)(param_4 + 8) = 0;
  *(undefined2 *)(param_4 + 0xe) = 0;
LAB__text__00482a14:
  local_8 = 0x482a21;
  FUN__text__0056ce80();
  return;
}

