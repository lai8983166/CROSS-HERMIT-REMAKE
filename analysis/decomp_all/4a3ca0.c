
void FUN__text__004a3ca0(void)

{
  char cVar1;
  undefined2 extraout_var;
  undefined2 extraout_var_00;
  undefined2 extraout_var_01;
  undefined2 extraout_var_02;
  undefined2 extraout_var_03;
  undefined2 extraout_var_04;
  undefined2 extraout_var_05;
  int iVar2;
  undefined2 extraout_var_06;
  undefined2 extraout_var_07;
  ushort uVar3;
  undefined2 extraout_var_08;
  undefined4 *puVar4;
  undefined4 local_b0 [16];
  uint local_70;
  int local_6c;
  uint local_68;
  int local_64;
  int local_60;
  int local_5c;
  int local_58;
  int local_54;
  ushort local_50;
  undefined2 uStack_4e;
  short local_4c;
  ushort local_48;
  undefined2 uStack_46;
  short local_44;
  short local_40;
  short local_3c;
  char local_38;
  uint local_34;
  char local_30;
  undefined2 local_2c;
  short local_28;
  char local_24;
  short local_20;
  short local_1c;
  short local_18;
  short local_14;
  short local_10;
  short local_c;
  int local_8;
  
  puVar4 = local_b0;
  for (iVar2 = 0x2b; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_c = FUN__text__004a8bc0();
  local_10 = FUN__text__004aa4b0();
  local_54 = (int)local_10;
  cVar1 = (char)local_10;
  switch(local_54) {
  case 0:
    if (DAT_007d6a26 == '\x01') {
      FUN__text__004aa590((int)local_10);
      FUN__text__004db2b0(5);
      *(undefined2 *)(local_8 + 0x1294) = 0;
      *(undefined2 *)(local_8 + 0x76c6) = 0xe;
    }
    else {
      FUN__text__004db2b0(5);
    }
    break;
  case 1:
  case 2:
  case 3:
  case 4:
  case 5:
    local_14 = local_10 + -1;
    local_18 = local_10;
    if (*(short *)(&DAT_007aaa12 + local_14 * 0x1c) != -1) {
      FUN__text__004aa590(local_10);
      FUN__text__004db2b0(5);
      (&DAT_007aaa15)[local_14 * 0x1c] = 0;
    }
    break;
  case 6:
  case 7:
  case 8:
  case 9:
  case 10:
    local_1c = local_10 + -6;
    local_20 = local_10;
    if (*(short *)(&DAT_007aaa12 + local_1c * 0x1c) != -1) {
      (&DAT_007aaa15)[local_1c * 0x1c] = 1;
      FUN__text__004aa590(CONCAT22((short)((uint)(local_1c * 0x1c) >> 0x10),local_10));
      FUN__text__004db2b0(5);
      if (DAT_007a55fa != 0) {
        (&DAT_007aaa15)[local_1c * 0x1c] = 0;
      }
    }
    break;
  case 0xb:
  case 0xc:
  case 0xd:
    local_24 = cVar1 + -0xb;
    local_28 = local_10;
    FUN__text__004aa590((int)local_10);
    FUN__text__004db2b0(5);
    local_2c = 0;
    local_58 = (int)local_10;
    if (local_58 == 0xb) {
      local_2c = 0;
    }
    else if (local_58 == 0xc) {
      local_2c = 1;
    }
    else if (local_58 == 0xd) {
      local_2c = 2;
    }
    FUN__text__004a8bf0(CONCAT22(extraout_var_08,local_2c),0);
    DAT_007d57da = local_24;
    break;
  case 0xe:
  case 0xf:
  case 0x10:
  case 0x11:
    local_30 = cVar1 + -0xb;
    FUN__text__004aa590((int)local_10);
    FUN__text__004db2b0(5);
    local_5c = local_10 + -0xe;
    switch(local_5c) {
    case 0:
      DAT_007d57db = '\0';
      break;
    case 1:
      if (DAT_007d57db != '\0') {
        DAT_007d57db = DAT_007d57db + -1;
      }
      break;
    case 2:
      if (DAT_007d57db != DAT_007d57dc) {
        DAT_007d57db = DAT_007d57db + '\x01';
      }
      break;
    case 3:
      DAT_007d57db = DAT_007d57dc;
    }
    break;
  case 0x12:
  case 0x13:
  case 0x14:
    break;
  case 0x15:
  case 0x16:
  case 0x17:
  case 0x18:
    local_60 = local_10 + -0x15;
    switch(local_60) {
    case 0:
      DAT_007d58ac = 0;
      break;
    case 1:
      if (DAT_007d58ac != 0) {
        DAT_007d58ac = DAT_007d58ac + -1;
      }
      break;
    case 2:
      if (DAT_007d58ac != DAT_007d58ae) {
        DAT_007d58ac = DAT_007d58ac + 1;
      }
      break;
    case 3:
      DAT_007d58ac = DAT_007d58ae;
    }
    FUN__text__004db2b0(5);
    FUN__text__004aa590(CONCAT22(extraout_var,local_10));
    break;
  case 0x19:
  case 0x1a:
  case 0x1b:
  case 0x1c:
  case 0x1d:
    uVar3 = local_10 - 0x19;
    local_34 = CONCAT22(local_34._2_2_,uVar3);
    if (*(short *)(&DAT_007aaa12 + (uint)uVar3 * 0x1c) == -1) {
      (&DAT_007aaa15)[(uint)uVar3 * 0x1c] = 1;
    }
    else {
      FUN__text__004db2b0(5);
      FUN__text__004aa590(CONCAT22(extraout_var_00,local_10));
      if (DAT_007a55fa == 0) {
        if ((&DAT_007aaa15)[(local_34 & 0xffff) * 0x1c] == '\0') {
          (&DAT_007aaa15)[(local_34 & 0xffff) * 0x1c] = 1;
          if (DAT_007a55fa != 0) {
            (&DAT_007aaa15)[(local_34 & 0xffff) * 0x1c] = 0;
          }
        }
        else {
          (&DAT_007aaa15)[(local_34 & 0xffff) * 0x1c] = 0;
        }
      }
      else {
        (&DAT_007aaa15)[(local_34 & 0xffff) * 0x1c] = 0;
      }
    }
    break;
  case 0x1e:
  case 0x1f:
    local_38 = cVar1 + -0x1e;
    if (((local_c != -1) && ((&DAT_007aaa15)[local_c * 0x1c] != '\x01')) && (DAT_007a55fa == 0)) {
      FUN__text__004db2b0(5);
      FUN__text__004aa590(CONCAT22(extraout_var_01,local_10));
      DAT_007d5984 = local_38;
    }
    break;
  case 0x20:
  case 0x21:
  case 0x22:
  case 0x23:
    if ((local_c != -1) && ((&DAT_007aaa15)[local_c * 0x1c] == '\0')) {
      FUN__text__004db2b0(5);
      FUN__text__004aa590(CONCAT22(extraout_var_02,local_10));
      DAT_007d5982 = local_10 + -0x20;
      local_3c = DAT_007d5982;
    }
    break;
  case 0x24:
  case 0x25:
  case 0x26:
  case 0x27:
    if ((local_c != -1) && ((&DAT_007aaa15)[local_c * 0x1c] == '\0')) {
      local_40 = local_10 + -0x24;
      local_44 = DAT_007aab08;
      local_64 = local_10 + -0x24;
      switch(local_64) {
      case 0:
        *(undefined2 *)(&DAT_007d6300 + DAT_007aab08 * 2) = 0;
        break;
      case 1:
        if (*(short *)(&DAT_007d6300 + DAT_007aab08 * 2) != 0) {
          *(short *)(&DAT_007d6300 + DAT_007aab08 * 2) =
               *(short *)(&DAT_007d6300 + DAT_007aab08 * 2) + -1;
        }
        break;
      case 2:
        if (*(short *)(&DAT_007d6300 + DAT_007aab08 * 2) !=
            *(short *)(&DAT_007d6306 + DAT_007aab08 * 2)) {
          *(short *)(&DAT_007d6300 + DAT_007aab08 * 2) =
               *(short *)(&DAT_007d6300 + DAT_007aab08 * 2) + 1;
        }
        break;
      case 3:
        *(undefined2 *)(&DAT_007d6300 + DAT_007aab08 * 2) =
             *(undefined2 *)(&DAT_007d6306 + DAT_007aab08 * 2);
      }
      FUN__text__004db2b0(5);
      FUN__text__004aa590(CONCAT22(extraout_var_06,local_10));
    }
    break;
  case 0x28:
  case 0x29:
  case 0x2a:
  case 0x2b:
    if ((local_c != -1) && ((&DAT_007aaa15)[local_c * 0x1c] == '\0')) {
      _local_48 = CONCAT22(uStack_46,local_10 - 0x28U);
      local_68 = (uint)(ushort)(local_10 - 0x28U);
      switch(local_68) {
      case 0:
        FUN__text__004d6230(2);
        break;
      case 1:
        FUN__text__004d6230(0);
        break;
      case 2:
        FUN__text__004d6230(1);
        break;
      case 3:
        FUN__text__004d6230(3);
      }
      FUN__text__004db2b0(5);
      FUN__text__004aa590(CONCAT22(extraout_var_03,local_10));
    }
    break;
  case 0x2c:
  case 0x2d:
  case 0x2e:
    if (((local_c != -1) && ((&DAT_007aaa15)[local_c * 0x1c] != '\0')) && (DAT_007a55fa == 0)) {
      FUN__text__004db2b0(5);
      FUN__text__004aa590(CONCAT22(extraout_var_04,local_10));
      DAT_007d598a = (char)local_10 + -0x2c;
    }
    break;
  case 0x2f:
  case 0x30:
  case 0x31:
  case 0x32:
    if (((local_c != -1) && ((&DAT_007aaa15)[local_c * 0x1c] != '\0')) && (DAT_007a55fa == 0)) {
      FUN__text__004db2b0(5);
      FUN__text__004aa590(CONCAT22(extraout_var_07,local_10));
      local_4c = (short)DAT_007d598a;
      local_6c = local_10 + -0x2f;
      switch(local_6c) {
      case 0:
        *(undefined2 *)(&DAT_007d6a1a + local_4c * 2) = 0;
        break;
      case 1:
        if (*(short *)(&DAT_007d6a1a + local_4c * 2) != 0) {
          *(short *)(&DAT_007d6a1a + local_4c * 2) = *(short *)(&DAT_007d6a1a + local_4c * 2) + -1;
        }
        break;
      case 2:
        if (*(short *)(&DAT_007d6a1a + local_4c * 2) != *(short *)(&DAT_007d6a20 + local_4c * 2)) {
          *(short *)(&DAT_007d6a1a + local_4c * 2) = *(short *)(&DAT_007d6a1a + local_4c * 2) + 1;
        }
        break;
      case 3:
        *(undefined2 *)(&DAT_007d6a1a + local_4c * 2) =
             *(undefined2 *)(&DAT_007d6a20 + local_4c * 2);
      }
    }
    break;
  case 0x33:
  case 0x34:
  case 0x35:
  case 0x36:
    if (((local_c != -1) && ((&DAT_007aaa15)[local_c * 0x1c] != '\0')) && (DAT_007a55fa == 0)) {
      FUN__text__004db2b0(5);
      FUN__text__004aa590(CONCAT22(extraout_var_05,local_10));
      _local_50 = CONCAT22(uStack_4e,local_10 - 0x33U);
      local_70 = (uint)(ushort)(local_10 - 0x33U);
      switch(local_70) {
      case 0:
        FUN__text__004d6230(2);
        break;
      case 1:
        FUN__text__004d6230(0);
        break;
      case 2:
        FUN__text__004d6230(1);
        break;
      case 3:
        FUN__text__004d6230(3);
      }
    }
  }
  local_8 = 0x4a45a7;
  FUN__text__0056ce80();
  return;
}

