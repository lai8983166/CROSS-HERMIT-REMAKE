
void FUN__text__004dab50(void)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_7c [16];
  int local_3c;
  int local_38;
  int local_34;
  int local_30;
  int local_2c;
  int local_28;
  int local_24;
  int local_20;
  int local_1c;
  int local_18;
  int local_14;
  undefined *local_10;
  undefined *local_c;
  undefined *local_8;
  
  puVar3 = local_7c;
  for (iVar2 = 0x1e; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = &DAT_008093fa;
  local_c = &DAT_0080967a;
  local_10 = &DAT_007f4518;
  for (local_14 = 0; local_14 != DAT_007f448c._1_1_; local_14 = local_14 + 1) {
    local_24 = (int)*(short *)(&DAT_008093fa + local_14 * 8) +
               (int)*(short *)(&DAT_007f45c0 + local_14 * 0xb0);
    if (0x7fff < local_24) {
      local_24 = 0x7fff;
    }
    local_18._0_2_ = (undefined2)local_24;
    *(undefined2 *)(&DAT_008093fa + local_14 * 8) = (undefined2)local_18;
    local_28 = (int)*(short *)(&DAT_008093fc + local_14 * 8) +
               (int)*(short *)(&DAT_007f45c2 + local_14 * 0xb0);
    if (0x7fff < local_28) {
      local_28 = 0x7fff;
    }
    local_18._0_2_ = (undefined2)local_28;
    *(undefined2 *)(&DAT_008093fc + local_14 * 8) = (undefined2)local_18;
    local_2c = (int)*(short *)(&DAT_008093fe + local_14 * 8) +
               (int)*(short *)(&DAT_007f45c4 + local_14 * 0xb0);
    if (0x7fff < local_2c) {
      local_2c = 0x7fff;
    }
    local_18._0_2_ = (undefined2)local_2c;
    *(undefined2 *)(&DAT_008093fe + local_14 * 8) = (undefined2)local_18;
    local_30 = (int)(char)(&DAT_00809400)[local_14 * 8] +
               (int)(char)(&DAT_007f45c6)[local_14 * 0xb0];
    if (0x7f < local_30) {
      local_30 = 0x7f;
    }
    local_18._0_1_ = (undefined1)local_30;
    (&DAT_00809400)[local_14 * 8] = (undefined1)local_18;
    local_18 = local_30;
  }
  local_34 = (int)DAT_007f450c;
  switch(local_34) {
  case 0:
    local_1c = 0;
    break;
  case 1:
    local_1c = 10;
    break;
  case 2:
    local_1c = 7;
    break;
  case 3:
    local_1c = 5;
    break;
  case 4:
    local_1c = 1;
    break;
  case 5:
    local_1c = 0;
    break;
  default:
    iVar2 = FUN__text__00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\SRC\\COMMON\\ComScenario.cpp",
                                DAT_006b2cf0 + 0x29,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_38 = *(short *)(local_c + 0x10) + local_1c;
  if (0x7fff < local_38) {
    local_38 = 0x7fff;
  }
  local_20._0_2_ = (undefined2)local_38;
  *(undefined2 *)(local_c + 0x10) = (undefined2)local_20;
  if (*(short *)(local_c + 0x14) < DAT_007f4510) {
    *(short *)(local_c + 0x14) = DAT_007f4510;
  }
  local_3c = (int)*(short *)(local_c + 0x16) + (int)DAT_007f4512;
  if (0x7fff < local_3c) {
    local_3c = 0x7fff;
  }
  local_20 = local_3c;
  iVar2 = local_20;
  local_20._0_2_ = (undefined2)local_3c;
  *(undefined2 *)(local_c + 0x16) = (undefined2)local_20;
  for (local_14 = 0; local_14 != 0x10; local_14 = local_14 + 1) {
    if ((&DAT_007f44be)[local_14] != '\0') {
      local_c[local_14] = local_c[local_14] | (&DAT_007f44be)[local_14];
    }
  }
  DAT_008093f8 = DAT_008093f8 + 1;
  local_8 = (undefined *)0x4dae50;
  local_20 = iVar2;
  FUN__text__0056ce80();
  return;
}

