
void __fastcall FUN__text__004c1350(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_78 [16];
  int local_38;
  undefined *local_34;
  undefined *local_30;
  short local_2c;
  char local_28;
  short local_24;
  short local_20;
  short local_1c;
  undefined4 local_18;
  uint local_14;
  uint local_10;
  undefined4 local_c;
  int local_8;
  
  puVar2 = local_78;
  for (iVar1 = 0x1d; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  *(undefined2 *)(param_1 + 0x11ce) = 0;
  *(undefined2 *)(param_1 + 0x12a2) = 0;
  *(undefined2 *)(param_1 + 0x136c) = 0;
  local_18 = local_18 & 0xffff0000;
  while ((local_18 & 0xffff) < 5) {
    *(undefined2 *)(param_1 + 0x1160 + (local_18 & 0xffff) * 2) = 0;
    local_14 = local_14 & 0xffff0000;
    while ((local_14 & 0xffff) < 4) {
      *(undefined2 *)(param_1 + 0x1138 + (local_18 & 0xffff) * 8 + (local_14 & 0xffff) * 2) = 0xffff
      ;
      local_1c = *(short *)(&DAT_007aaa22 + (local_14 & 0xffff) * 2 + (local_18 & 0xffff) * 0x1c);
      if (-1 < local_1c) {
        *(short *)(param_1 + 0x1138 + (local_18 & 0xffff) * 8 +
                  *(short *)(param_1 + 0x1160 + (local_18 & 0xffff) * 2) * 2) = local_1c;
        *(short *)(param_1 + 0x1160 + (local_18 & 0xffff) * 2) =
             *(short *)(param_1 + 0x1160 + (local_18 & 0xffff) * 2) + 1;
        *(short *)(param_1 + 0x116a + *(short *)(param_1 + 0x11ce) * 2) = local_1c;
        *(short *)(param_1 + 0x11ce) = *(short *)(param_1 + 0x11ce) + 1;
      }
      local_14 = CONCAT22(local_14._2_2_,(short)local_14 + 1);
    }
    local_18 = CONCAT22(local_18._2_2_,(short)local_18 + 1);
  }
  *(undefined2 *)(param_1 + 0x12a2) = 0;
  local_c = local_c & 0xffff0000;
  while ((int)(local_c & 0xffff) < (int)DAT_007a5260) {
    local_20 = 1;
    local_1c = *(short *)(&DAT_007a5210 + (local_c & 0xffff) * 2);
    *(short *)(param_1 + 0x12a4 + *(short *)(param_1 + 0x136c) * 2) = local_1c;
    *(short *)(param_1 + 0x136c) = *(short *)(param_1 + 0x136c) + 1;
    local_10 = local_10 & 0xffff0000;
    while ((int)(local_10 & 0xffff) < (int)*(short *)(param_1 + 0x11ce)) {
      if (local_1c == *(short *)(param_1 + 0x116a + (local_10 & 0xffff) * 2)) {
        local_20 = 0;
      }
      local_10 = CONCAT22(local_10._2_2_,(short)local_10 + 1);
    }
    if (local_20 != 0) {
      *(short *)(param_1 + 0x11da + *(short *)(param_1 + 0x12a2) * 2) = local_1c;
      *(short *)(param_1 + 0x12a2) = *(short *)(param_1 + 0x12a2) + 1;
    }
    local_c = CONCAT22(local_c._2_2_,(short)local_c + 1);
  }
  local_18 = (uint)local_18._2_2_ << 0x10;
  while ((local_18 & 0xffff) < 5) {
    local_1c = *(short *)(&DAT_007aaa12 + (local_18 & 0xffff) * 0x1c);
    if (-1 < local_1c) {
      *(short *)(param_1 + 0x11d0 + (local_18 & 0xffff) * 2) = local_1c;
    }
    local_18 = CONCAT22(local_18._2_2_,(short)local_18 + 1);
  }
  local_c = (uint)local_c._2_2_ << 0x10;
  local_8 = param_1;
  while ((int)(local_c & 0xffff) < (int)*(short *)(local_8 + 0x136c)) {
    local_1c = *(short *)(local_8 + 0x12a4 + (local_c & 0xffff) * 2);
    local_24 = *(short *)(&DAT_007e17ee + local_1c * 0x4a0);
    local_28 = (&DAT_007cf423)[(int)local_24 + local_1c * 0x124];
    if (local_28 != 'd') {
      local_28 = local_28 + '\x01';
      local_28 = FUN__text__004d1ba0((int)local_28,0,99);
    }
    (&DAT_007cf423)[(int)local_24 + local_1c * 0x124] = local_28;
    local_c = CONCAT22(local_c._2_2_,(short)local_c + 1);
  }
  local_2c = (DAT_007a528e + -4) * 5 + DAT_007a5290 + -1;
  local_18 = local_18 & 0xffff0000;
  while ((local_18 & 0xffff) < 5) {
    local_14 = local_14 & 0xffff0000;
    while ((int)(local_14 & 0xffff) < (int)*(short *)(local_8 + 0x1160 + (local_18 & 0xffff) * 2)) {
      local_1c = *(short *)(local_8 + 0x1138 + (local_18 & 0xffff) * 8 + (local_14 & 0xffff) * 2);
      iVar1 = local_1c * 0x124;
      local_30 = &DAT_007cf34c + iVar1;
      local_38 = (int)*(short *)(&DAT_007a529a + (local_18 & 0xffff) * 0x70);
      if (local_38 == 2) {
        (&UNK_007cf370)[local_2c * 3 + iVar1] = 2;
        (&UNK_007cf371)[local_2c * 3 + iVar1] = (&DAT_007a52a0)[(local_18 & 0xffff) * 0x70];
        (&UNK_007cf372)[local_2c * 3 + iVar1] = (&DAT_007a52a2)[(local_18 & 0xffff) * 0x70];
      }
      else if (local_38 == 4) {
        (&UNK_007cf370)[local_2c * 3 + iVar1] = 1;
        (&UNK_007cf371)[local_2c * 3 + iVar1] = (&DAT_007a52a0)[(local_18 & 0xffff) * 0x70];
        (&UNK_007cf372)[local_2c * 3 + iVar1] = (&DAT_007a52a2)[(local_18 & 0xffff) * 0x70];
      }
      local_14 = CONCAT22(local_14._2_2_,(short)local_14 + 1);
    }
    local_18 = CONCAT22(local_18._2_2_,(short)local_18 + 1);
  }
  local_c = local_c & 0xffff0000;
  while ((int)(local_c & 0xffff) < (int)*(short *)(local_8 + 0x12a2)) {
    local_1c = *(short *)(local_8 + 0x11da + (local_c & 0xffff) * 2);
    local_34 = &DAT_007cf34c + local_1c * 0x124;
    (&UNK_007cf370)[local_2c * 3 + local_1c * 0x124] = 3;
    local_c = CONCAT22(local_c._2_2_,(short)local_c + 1);
  }
  FUN__text__004bf9e0();
  local_8 = 0x4c1900;
  FUN__text__0056ce80();
  return;
}

