
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __fastcall FUN__text__004ae370(int param_1)

{
  ushort uVar1;
  uint uVar2;
  undefined2 extraout_var;
  undefined2 extraout_var_00;
  undefined2 extraout_var_01;
  undefined2 extraout_var_02;
  undefined2 extraout_var_03;
  undefined2 extraout_var_04;
  int iVar3;
  undefined2 extraout_var_05;
  undefined2 extraout_var_06;
  undefined2 extraout_var_07;
  undefined2 uVar4;
  undefined2 extraout_var_08;
  undefined2 uVar5;
  undefined2 extraout_var_09;
  undefined2 extraout_var_10;
  undefined2 extraout_var_11;
  undefined2 extraout_var_12;
  undefined4 *puVar6;
  undefined4 local_450 [16];
  char local_410;
  uint local_40c;
  uint local_408;
  uint local_404;
  int local_400;
  uint local_3fc;
  uint local_3f8;
  int local_3f4;
  uint local_3f0;
  int local_3ec;
  undefined1 local_3e8 [16];
  uint local_3d8;
  ushort local_2f0;
  int local_2ec;
  int local_2e8;
  undefined1 local_2e4 [12];
  int local_2d8;
  undefined2 local_1ec;
  undefined2 local_1e8;
  uint local_1e4;
  undefined4 local_1e0;
  uint local_1dc;
  undefined2 local_1d8;
  undefined1 local_1d4 [100];
  short local_170;
  undefined2 local_16c;
  undefined1 local_168 [12];
  int local_15c;
  undefined2 local_70;
  undefined2 local_6c;
  ushort local_68;
  uint local_64;
  undefined4 local_60;
  undefined2 local_5c;
  ushort local_58;
  uint local_54;
  short local_50;
  uint local_4c;
  undefined *local_48;
  undefined *local_44;
  undefined *local_40;
  uint local_3c;
  short local_38;
  undefined4 local_34;
  undefined4 local_30;
  uint local_2c;
  undefined4 local_28;
  uint local_24;
  undefined1 *local_20;
  uint local_1c;
  uint local_18;
  uint local_10;
  undefined4 local_c;
  int local_8;
  
  puVar6 = local_450;
  for (iVar3 = 0x113; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar6 = 0xcccccccc;
    puVar6 = puVar6 + 1;
  }
  local_3c = CONCAT22(local_3c._2_2_,*(undefined2 *)(param_1 + 0x596 + DAT_007d6a34 * 2));
  local_40 = &DAT_006b2d88 + (uint)*(ushort *)(param_1 + 0x632) * 0x40;
  local_44 = &DAT_007e17e8 + *(short *)(param_1 + 0x596 + DAT_007d6a34 * 2) * 0x4a0;
  local_48 = &DAT_007cf34c + *(short *)(param_1 + 0x596 + DAT_007d6a34 * 2) * 0x124;
  local_8 = param_1;
  FUN__text__004ae340(CONCAT22((short)((uint)local_48 >> 0x10),
                               *(undefined2 *)(param_1 + 0x596 + DAT_007d6a34 * 2)));
  DAT_007d6a30 = 0;
  local_3f0 = (uint)DAT_007d6a36;
  switch(local_3f0) {
  case 0:
    *(undefined2 *)(local_8 + 0x391d6) = 0xffff;
    DAT_007d6a36 = 1;
    break;
  case 1:
    *(undefined1 *)(local_8 + 0xc88) = 1;
    local_4c = local_4c & 0xffff0000;
    local_50 = 0;
    iVar3 = FUN__text__004128f0(0xcb,1);
    if (iVar3 != 0) {
      local_50 = FUN__text__004b6fb0(0,CONCAT22(extraout_var_05,DAT_007d6a34));
      local_4c = CONCAT22(local_4c._2_2_,1);
      FUN__text__004db2b0(5);
    }
    iVar3 = FUN__text__004128f0(0xcd,1);
    uVar4 = extraout_var_06;
    if (iVar3 != 0) {
      local_50 = FUN__text__004b6fb0(1,CONCAT22(extraout_var_09,DAT_007d6a34));
      local_4c = CONCAT22(local_4c._2_2_,1);
      FUN__text__004db2b0(5);
      uVar4 = extraout_var_07;
    }
    if ((local_4c & 0xffff) != 0) {
      DAT_007d6a34 = local_50;
      FUN__text__004b6690(CONCAT22(uVar4,*(undefined2 *)(local_8 + 0x596 + local_50 * 2)),0xffffffff
                          ,1,2);
      FUN__text__004b6690(CONCAT22(extraout_var_08,
                                   *(undefined2 *)(local_8 + 0x596 + DAT_007d6a34 * 2)),0xffffffff,0
                          ,0);
      DAT_007d6a38 = -1;
      DAT_007d6a3a = -1;
      DAT_007d6a3c = -1;
      _DAT_007d6a3e = 0;
    }
    uVar2 = FUN__text__004b6d90();
    local_3f4 = (uVar2 & 0xffff) - 1;
    switch(local_3f4) {
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
    break;
  case 2:
    local_54 = local_54 & 0xffff0000;
    DAT_007d6a30 = 2;
    FUN__text__004d5c40(&local_1c,0);
    if ((local_1c & 1) == 0) {
      FUN__text__004db2b0(5);
      DAT_007d6a36 = 1;
      local_54 = CONCAT22(local_54._2_2_,1);
    }
    else {
      DAT_007d6a30 = 2;
    }
    local_58 = (ushort)(byte)local_40[3];
    local_5c = 0;
    local_60 = (uint)local_60._2_2_ << 0x10;
    local_c = (uint)local_c._2_2_ << 0x10;
    while ((local_c & 0xffff) < (uint)(byte)local_40[3]) {
      FUN__text__004b10b0(&local_1c,local_c & 0xffff);
      if ((local_10 & 0xffff) != 0) {
        local_20 = &DAT_0061bc10;
        FUN__text__004d2ca0(0xd,0x35,DAT_0061bc12,(local_c & 0xffff) * 0x24 + 0x16e,0x1be,
                            DAT_0061bc14,DAT_0061bc16,DAT_0061bc18,DAT_0061bc1a);
        if ((local_54 & 0xffff) == 1) {
          if (*(short *)(local_44 + (local_c & 0xffff) * 2 + 0x52) == 0) {
            *(short *)(local_44 + (local_c & 0xffff) * 2 + 0x52) = DAT_007d6a3c;
            local_54 = CONCAT22(local_54._2_2_,3);
          }
          else {
            uVar1 = *(ushort *)(local_44 + (local_c & 0xffff) * 2 + 0x52);
            local_60 = CONCAT22(local_60._2_2_,uVar1);
            *(short *)(local_44 + (local_c & 0xffff) * 2 + 0x52) = DAT_007d6a3c;
            (&DAT_007e18a0)[(uVar1 - 1) * 0xc + (local_3c & 0xffff) * 0x4a0] = 3;
            local_54 = CONCAT22(local_54._2_2_,2);
          }
        }
      }
      local_c = CONCAT22(local_c._2_2_,(short)local_c + 1);
    }
    FUN__text__004b4d70(*(short *)(DAT_007a49fc + 0x196c) + -0x10,
                        *(short *)(DAT_007a49fc + 0x1970) + -0x10,DAT_007d6a38,DAT_007d6a3a,7,0x34);
    local_3f8 = local_54 & 0xffff;
    if (local_3f8 == 1) {
      (&DAT_007e18a0)[(DAT_007d6a3c + -1) * 0xc + (local_3c & 0xffff) * 0x4a0] = 3;
    }
    else if ((local_3f8 < 2) || (3 < local_3f8)) break;
    FUN__text__004b6690(local_3c & 0xffff,0xffffffff,0,0);
    break;
  case 3:
    local_64 = local_64 & 0xffff0000;
    DAT_007d6a30 = 2;
    FUN__text__004d5c40(&local_1c,0);
    if ((local_1c & 1) == 0) {
      FUN__text__004db2b0(5);
      local_64 = CONCAT22(local_64._2_2_,1);
      DAT_007d6a36 = 1;
    }
    else {
      DAT_007d6a30 = 2;
    }
    local_68 = (ushort)(byte)local_40[3];
    local_6c = 0;
    local_70 = 0;
    local_c = (uint)local_c._2_2_ << 0x10;
    while ((local_c & 0xffff) < (uint)(byte)local_40[3]) {
      FUN__text__004b10b0(&local_1c,local_c & 0xffff);
      if ((local_10 & 0xffff) != 0) {
        local_20 = &DAT_0061bc10;
        FUN__text__004d2ca0(0xd,0x35,DAT_0061bc12,(local_c & 0xffff) * 0x24 + 0x16e,0x1be,
                            DAT_0061bc14,DAT_0061bc16,DAT_0061bc18,DAT_0061bc1a);
        if ((local_64 & 0xffff) == 1) {
          if (*(short *)(local_44 + (local_c & 0xffff) * 2 + 0x52) == 0) {
            *(short *)(local_44 + (local_c & 0xffff) * 2 + 0x52) = DAT_007d6a3c;
            local_64 = CONCAT22(local_64._2_2_,3);
          }
          else {
            local_70 = *(undefined2 *)(local_44 + (local_c & 0xffff) * 2 + 0x52);
            *(short *)(local_44 + (local_c & 0xffff) * 2 + 0x52) = DAT_007d6a3c;
            *(undefined2 *)(local_44 + (short)DAT_007d6a44 * 2 + 0x52) = local_70;
            local_64 = CONCAT22(local_64._2_2_,2);
          }
        }
      }
      local_c = CONCAT22(local_c._2_2_,(short)local_c + 1);
    }
    FUN__text__004b4d70(*(short *)(DAT_007a49fc + 0x196c) + -0x10,
                        *(short *)(DAT_007a49fc + 0x1970) + -0x10,DAT_007d6a46,DAT_007d6a48,7,0x34);
    local_3fc = local_64 & 0xffff;
    if (local_3fc == 1) {
      (&DAT_007e18a0)[(DAT_007d6a3c + -1) * 0xc + (local_3c & 0xffff) * 0x4a0] = 3;
LAB__text__004aeab9:
      FUN__text__004b6690(local_3c & 0xffff,0xffffffff,0,0);
    }
    else if ((1 < local_3fc) && (local_3fc < 4)) goto LAB__text__004aeab9;
    local_c = CONCAT22(local_c._2_2_,DAT_007d6a44);
    local_20 = &DAT_0061bc10;
    FUN__text__004d2ca0(0xd,0x35,DAT_0061bc12,(uint)DAT_007d6a44 * 0x24 + 0x16e,0x1be,DAT_0061bc14,
                        DAT_0061bc16,DAT_0061bc18,DAT_0061bc1a);
    FUN__text__004b4d70((local_c & 0xffff) * 0x24 + 0x16f,0x1bf,CONCAT22(extraout_var,DAT_007d6a46),
                        CONCAT22(extraout_var_10,DAT_007d6a48),6,0x40);
  }
  local_28 = (uint)local_28._2_2_ << 0x10;
  while( true ) {
    if (6 < (local_28 & 0xffff)) break;
    local_24 = local_24 & 0xffff0000;
    while ((local_24 & 0xffff) < 0xc) {
      local_38 = FUN__text__004ae2f0(local_24 & 0xffff,local_28 & 0xffff);
      puVar6 = (undefined4 *)(&DAT_007e1898 + (local_38 + -1) * 0xc + (local_3c & 0xffff) * 0x4a0);
      local_34 = *puVar6;
      local_30 = puVar6[1];
      local_2c = puVar6[2];
      uVar5 = (undefined2)(local_2c >> 0x10);
      uVar4 = (undefined2)((uint)local_30 >> 0x10);
      if (DAT_007d6a36 == 1) {
        FUN__text__004d5ec0(&local_1c,(local_24 & 0xffff) * 0x24 + 0xf0,
                            (local_28 & 0xffff) * 0x24 + 0x1e9,0x23,0x23);
        uVar5 = extraout_var_00;
        if ((local_10 & 0xffff) != 0) {
          if ((local_2c & 0xff) != 0) {
            FUN__text__004d2690((local_24 & 0xffff) * 0x24 + 0xf0,(local_28 & 0xffff) * 0x24 + 0x1e9
                                ,0x24,0x24,0x3e,0xffffffff,1);
          }
          if ((local_2c & 0xff) == 3) {
            DAT_007d6a30 = 1;
          }
          if (DAT_007d6a31 != '\0') {
            DAT_007d6a30 = 0;
          }
          if ((local_18 & 1) != 0) {
            local_400 = (local_2c & 0xff) - 2;
            switch(local_400) {
            case 0:
            case 2:
            case 3:
            case 4:
              DAT_007d6a38 = (short)local_24;
              DAT_007d6a3a = (short)local_28;
              DAT_007d6a3c = local_38;
              _DAT_007d6a3e = (short)local_28 * 0xc + (short)local_24;
              FUN__text__004db2b0(5);
              break;
            case 1:
              FUN__text__004db2b0(5);
              DAT_007d6a38 = (short)local_24;
              DAT_007d6a3a = (short)local_28;
              DAT_007d6a3c = local_38;
              _DAT_007d6a3e = (short)local_28 * 0xc + (short)local_24;
              if (DAT_007d6a31 == '\0') {
                DAT_007d6a36 = 2;
                (&DAT_007e18a0)[(local_38 + -1) * 0xc + (local_3c & 0xffff) * 0x4a0] = 6;
              }
              else {
                DAT_007d6a30 = 0;
              }
            }
          }
          uVar5 = 0;
        }
        uVar4 = 0;
      }
      FUN__text__004b4d70((local_24 & 0xffff) * 0x24 + 0xf1,(local_28 & 0xffff) * 0x24 + 0x1e9,
                          local_24 & 0xffff,CONCAT22(uVar5,(short)local_28),
                          CONCAT22(uVar4,(ushort)(byte)local_2c),0x48);
      local_24 = CONCAT22(local_24._2_2_,(short)local_24 + 1);
    }
    local_28 = CONCAT22(local_28._2_2_,(short)local_28 + 1);
  }
  if (DAT_007d6a38 < 0) {
    DAT_007d6a40 = '\0';
  }
  else if (DAT_007d6a3a < 0) {
    DAT_007d6a40 = '\0';
  }
  else {
    FUN__text__004d2700(&DAT_0061bc10,1,0x3e,DAT_007d6a38 * 0x24 + 0xf1,DAT_007d6a3a * 0x24 + 0x1ea)
    ;
  }
  DAT_007d6a4c = 0;
  if (DAT_007d6a3c < 0) {
    FUN__text__004b4d70(0x2a9,0x1e9,0,0,8,0x40);
    DAT_007d6a40 = '\0';
  }
  else {
    FUN__text__004d58e0(local_168,local_3c & 0xffff);
    if (local_15c < 0) {
      DAT_007d6a40 = '\0';
    }
    else {
      local_404 = (uint)(byte)(&DAT_007e18a0)
                              [(DAT_007d6a3c + -1) * 0xc + (local_3c & 0xffff) * 0x4a0];
      switch(local_404) {
      case 0:
        DAT_007d6a40 = '\0';
        break;
      case 1:
        DAT_007d6a40 = '\x01';
        break;
      case 2:
        DAT_007d6a40 = '\x01';
        break;
      case 4:
        DAT_007d6a40 = '\x01';
        break;
      case 5:
        DAT_007d6a40 = '\x02';
        break;
      case 6:
        DAT_007d6a40 = '\x02';
        break;
      case 7:
        DAT_007d6a40 = '\0';
        break;
      case 8:
        DAT_007d6a40 = '\0';
      }
      local_16c = (undefined2)((byte)(&DAT_006c2dcc)[DAT_007d6a3c * 0x48] - 1);
      local_170 = (byte)(&DAT_006c2dcf)[DAT_007d6a3c * 0x48] - 1;
      FUN__text__004b4d70(0x2a9,0x1e9,
                          CONCAT22((short)((uint)(DAT_007d6a3c * 0x48) >> 0x10),local_16c),
                          CONCAT22((short)((byte)(&DAT_006c2dcc)[DAT_007d6a3c * 0x48] - 1 >> 0x10),
                                   local_170),3,0x40);
      FUN__text__004b4f40(0x2cd,0x1ed,CONCAT22(extraout_var_01,local_16c),
                          CONCAT22(extraout_var_11,local_170),0x40);
      FUN__text__004b7230(0x313,0x1ff,0,0,3,0x4a,0x3f,
                          (int)*(short *)(&DAT_006c2dd0 + DAT_007d6a3c * 0x48),1);
      DAT_007d6a4c = *(int *)(&DAT_006c2e08 + DAT_007d6a3c * 0x48);
      if (*(short *)(local_8 + 0x391d6) != DAT_007d6a3c) {
        FUN__text__004d64d0(DAT_007d6a3c,10);
        FUN__text__004d60e0(1);
        FUN__text__004d60e0(1);
        FUN__text__004d60e0(1);
        FUN__text__004d60e0(1);
        FUN__text__0056d810(local_1d4,&PTR_DAT_005a0b28,
                            *(undefined2 *)(&DAT_006c2dd2 + DAT_007d6a3c * 0x48));
        FUN__text__004d6150(local_1d4);
        FUN__text__0056d810(local_1d4,&PTR_DAT_005a0b28,
                            *(undefined2 *)(&DAT_006c2dd6 + DAT_007d6a3c * 0x48));
        FUN__text__004d6150(local_1d4);
        local_1d8 = 2;
        local_408 = (uint)(byte)(&DAT_006c2de0)[DAT_007d6a3c * 0x48];
        switch(local_408) {
        case 0:
          FUN__text__004d6150(&DAT_005a0b20);
          break;
        case 1:
          FUN__text__004d6150(&DAT_005a0b18);
          break;
        case 2:
          FUN__text__004d6150(&DAT_005a0b0c);
          break;
        case 3:
          FUN__text__004d6150(&DAT_005a0b04);
          break;
        case 4:
          FUN__text__004d6150(&DAT_005a0afc);
          break;
        case 5:
          FUN__text__004d6150(&DAT_005a0af4);
          break;
        case 6:
          FUN__text__004d6150(&DAT_005a0ae8);
          break;
        default:
          FUN__text__004d6150("!!!!ERROR!!!!");
        }
        local_1d8 = 3;
        local_40c = (uint)(byte)(&DAT_006c2de1)[DAT_007d6a3c * 0x48];
        switch(local_40c) {
        case 0:
          FUN__text__004d6150(&DAT_005a0ad0);
          break;
        case 1:
          FUN__text__004d6150(&DAT_005a0b18);
          break;
        case 2:
          FUN__text__004d6150(&DAT_005a0b0c);
          break;
        case 3:
          FUN__text__004d6150(&DAT_005a0b04);
          break;
        case 4:
          FUN__text__004d6150(&DAT_005a0ac4);
          break;
        case 5:
          FUN__text__004d6150(&DAT_005a0ab8);
          break;
        default:
          FUN__text__004d6150("!!!!ERROR!!!!");
        }
      }
      FUN__text__004d62f0(0x304,0x22d,0x3d);
      FUN__text__004d62f0(0x304,0x240,0x3d);
      FUN__text__004d62f0(0x3a2,0x22d,0x3d);
      FUN__text__004d62f0(0x3a2,0x240,0x3d);
      FUN__text__004d62f0(0x2b2,0x25e,0x3d);
      *(short *)(local_8 + 0x391d6) = DAT_007d6a3c;
    }
  }
  FUN__text__004d2700(&DAT_0061bb00,0,0x4e,0xd7,0x1a7);
  FUN__text__004b70a0(0x20,*(undefined1 *)(local_8 + 0xc87),1);
  FUN__text__004b70a0(0x21,(int)*(char *)(local_8 + 0x582),1);
  local_1dc = CONCAT22(local_1dc._2_2_,
                       (ushort)(byte)(&DAT_006b2d8b)[(uint)*(ushort *)(local_8 + 0x632) * 0x40]);
  local_1e0 = (uint)local_1e0._2_2_ << 0x10;
  while ((local_1e0 & 0xffff) < 8) {
    if ((local_1dc & 0xffff) <= (local_1e0 & 0xffff)) {
      FUN__text__004d2620((local_1e0 & 0xffff) * 0x24 + 0x16f,0x1bf,0x22,0x22,0x36,0x7000a000,1);
    }
    local_1e0 = CONCAT22(local_1e0._2_2_,(short)local_1e0 + 1);
  }
  local_1e4 = CONCAT22(local_1e4._2_2_,1);
  local_1e8 = 0x48;
  local_1ec = 1;
  FUN__text__004d58e0(local_2e4,local_3c & 0xffff);
  if (local_2d8 == 0) {
    DAT_007d6a40 = '\0';
  }
  local_410 = DAT_007d6a40;
  if (DAT_007d6a40 == '\0') {
    FUN__text__004d2620(0x354,0x1bf,0xa3,0x25,0x37,0x70010101,1);
    uVar4 = extraout_var_03;
  }
  else if (DAT_007d6a40 == '\x01') {
    local_20 = &DAT_0061bc80;
    FUN__text__004d5ec0(&local_1c,0x360,0x1c3,0x8a,0x1c);
    local_2e8 = DAT_007a511c - DAT_007d6a4c;
    if (local_2e8 < 0) {
      FUN__text__004d2620(0x354,0x1bf,0xa3,0x25,0x37,0x70010101,1);
    }
    if ((((local_10 & 0xffff) != 0) && ((local_18 & 1) != 0)) &&
       (local_2ec = DAT_007a511c - DAT_007d6a4c, -1 < local_2ec)) {
      local_1e4 = local_1e4 & 0xffff0000;
      local_1e8 = 0x47;
      local_1ec = 8;
      FUN__text__004db2b0(0xb);
      FUN__text__004d48a0(CONCAT22(extraout_var_12,(undefined2)local_3c),6,0xffffffff,0);
      FUN__text__00409ff0(local_8 + 0x3a2a4,0,1,0);
      (&DAT_007e18a0)[(DAT_007d6a3c + -1) * 0xc + (local_3c & 0xffff) * 0x4a0] = 3;
      iVar3 = (local_3c & 0xffff) * 0x124;
      *(int *)(&DAT_007cf468 + iVar3) =
           *(int *)(&DAT_007cf468 + (local_3c & 0xffff) * 0x124) + DAT_007d6a4c;
      local_2f0 = (ushort)*(byte *)(local_8 + 0xb92);
      FUN__text__004d58e0(local_3e8,CONCAT22((short)((uint)iVar3 >> 0x10),(undefined2)local_3c));
      (&DAT_007e1838)[(local_3c & 0xffff) * 0x4a0] = (undefined1)local_3d8;
      *(undefined1 *)(local_8 + 0xb92) = (undefined1)local_3d8;
      *(undefined1 *)(local_8 + 0xae2) = (undefined1)local_3d8;
      if ((int)(short)local_2f0 < (int)(local_3d8 & 0xff)) {
        FUN__text__00409ff0(local_8 + 0x3a24c,0,1,0);
        FUN__text__004db2b0(0xb);
      }
      FUN__text__004b6690(local_3c & 0xffff,0xffffffff,1,2);
      FUN__text__004b6690(CONCAT22(extraout_var_04,(undefined2)local_3c),0xffffffff,0,0);
      DAT_007a511c = local_2ec;
      DAT_007d6a40 = '\x02';
    }
    uVar4 = 0;
  }
  else {
    uVar4 = extraout_var_02;
    if (DAT_007d6a40 == '\x02') {
      local_20 = &DAT_0061bc90;
      DAT_007d6a4c = 0;
      local_1e4 = local_1e4 & 0xffff0000;
      local_1e8 = 0x48;
    }
  }
  if ((local_1e4 & 0xffff) == 0) {
    uVar5 = (undefined2)((uint)local_20 >> 0x10);
    FUN__text__004d67f0(CONCAT31((int3)(CONCAT22(uVar5,*(undefined2 *)(local_20 + 2)) >> 8),
                                 *local_20),CONCAT22(uVar5,local_1e8),
                        CONCAT22(uVar5,*(undefined2 *)(local_20 + 2)),
                        CONCAT22(uVar5,*(undefined2 *)(local_20 + 0xc)),
                        CONCAT22(uVar5,*(undefined2 *)(local_20 + 0xe)),
                        CONCAT22(uVar5,*(undefined2 *)(local_20 + 4)),
                        CONCAT22(uVar5,*(undefined2 *)(local_20 + 6)),
                        CONCAT22(uVar5,*(undefined2 *)(local_20 + 8)),*(undefined2 *)(local_20 + 10)
                        ,CONCAT22(uVar4,local_1ec));
  }
  local_3ec = DAT_007a511c - DAT_007d6a4c;
  FUN__text__004b7590(0x3ec,0x1ed,0,0,9,0x4a,0x3f,DAT_007a511c,8,1,4,7,0);
  FUN__text__004b7590(0x3ec,0x200,0,0,9,0x4a,0x3f,DAT_007d6a4c,8,1,4,7,0);
  if (local_3ec < 0) {
    FUN__text__004b7590(0x3ec,0x213,0,0x130,9,0x4a,0x3f,-local_3ec,8,1,4,7,0);
  }
  else {
    FUN__text__004b7590(0x3ec,0x213,0,0x98,9,0x4a,0x3f,local_3ec,8,1,4,7,0);
  }
  FUN__text__004d5ec0(&local_1c,0x2b6,0x1c3,0x8a,0x1c);
  if (((local_10 & 0xffff) != 0) && ((local_18 & 1) != 0)) {
    FUN__text__004db2b0(5);
    if (DAT_007d6a31 == '\0') {
      DAT_007d6a31 = '\x01';
    }
    else {
      DAT_007d6a31 = '\0';
    }
  }
  if (DAT_007d6a31 != '\0') {
    local_20 = &DAT_0061bc70;
    FUN__text__004d2ca0(0xd,0x47,DAT_0061bc72,DAT_0061bc7c,DAT_0061bc7e,DAT_0061bc74,DAT_0061bc76,
                        DAT_0061bc78,DAT_0061bc7a);
  }
  local_8 = 0x4afad6;
  FUN__text__0056ce80();
  return;
}

