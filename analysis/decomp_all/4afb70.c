
void __fastcall FUN__text__004afb70(int param_1)

{
  undefined2 extraout_var;
  undefined2 extraout_var_00;
  uint uVar1;
  undefined2 extraout_var_01;
  undefined4 uVar2;
  int iVar3;
  undefined2 extraout_var_02;
  undefined2 extraout_var_03;
  short sVar4;
  ushort uVar5;
  undefined2 extraout_var_04;
  undefined2 extraout_var_05;
  undefined2 extraout_var_06;
  undefined2 uVar6;
  undefined2 extraout_var_07;
  undefined2 extraout_var_08;
  undefined2 extraout_var_09;
  undefined4 *puVar7;
  undefined4 uVar8;
  undefined *puVar9;
  undefined4 uVar10;
  undefined4 local_f4 [16];
  uint local_b4;
  int local_b0;
  uint local_ac;
  uint local_a8;
  int local_a4;
  uint local_a0;
  undefined4 local_9c;
  uint local_98;
  uint local_94;
  undefined2 local_90;
  short local_8c;
  undefined2 uStack_8a;
  uint local_88;
  short local_84;
  ushort local_80;
  ushort local_7c;
  undefined2 uStack_7a;
  uint local_78;
  ushort local_74;
  ushort local_70;
  undefined2 uStack_6e;
  ushort local_6c;
  undefined2 uStack_6a;
  uint local_68;
  uint local_64;
  ushort local_60;
  ushort local_5c;
  undefined2 uStack_5a;
  undefined2 local_58;
  uint local_54;
  ushort local_50;
  ushort local_4c;
  undefined2 uStack_4a;
  short local_48;
  uint local_44;
  uint local_40;
  undefined *local_3c;
  undefined *local_38;
  uint local_34;
  uint local_30;
  uint local_2c;
  undefined4 local_28;
  uint local_24;
  undefined4 local_20;
  undefined1 *local_1c;
  uint local_18;
  uint local_14;
  uint local_c;
  int local_8;
  
  iVar3 = 0x3c;
  puVar7 = local_f4;
  while( true ) {
    if (iVar3 == 0) break;
    iVar3 = iVar3 + -1;
    *puVar7 = 0xcccccccc;
    puVar7 = puVar7 + 1;
  }
  local_2c = local_2c & 0xffff0000;
  uVar5 = *(ushort *)(param_1 + 0x596 + DAT_007d6a34 * 2);
  local_34 = CONCAT22(local_34._2_2_,uVar5);
  local_38 = &DAT_006b2d88 + (uint)*(ushort *)(param_1 + 0x632) * 0x40;
  local_3c = &DAT_007e17e8 + (uint)uVar5 * 0x4a0;
  local_8 = param_1;
  FUN__text__004d2700(&DAT_0061bb10,0,0x4e,0xd7,0x1a7);
  FUN__text__004b70a0(0x20,*(undefined1 *)(local_8 + 0xc86),1);
  FUN__text__004b70a0(0x21,(int)*(char *)(local_8 + 0x570),1);
  local_40._0_2_ = (ushort)(byte)local_38[3];
  if (DAT_007d6a31 != '\0') {
    local_40._0_2_ = 8;
  }
  local_20 = (uint)local_20._2_2_ << 0x10;
  while ((local_20 & 0xffff) < (local_40 & 0xffff)) {
    FUN__text__004d2620((local_20 & 0xffff) * 0x24 + 0x16f,0x1bf,0x22,0x22,0x37,0x70010101,1);
    local_20 = CONCAT22(local_20._2_2_,(short)local_20 + 1);
  }
  DAT_007d6a30 = 0;
  local_a0 = (uint)DAT_007d6a50;
  switch(local_a0) {
  case 0:
    *(undefined2 *)(local_8 + 0x391d4) = 0xffff;
    DAT_007d6a50 = 1;
    break;
  case 1:
    *(undefined1 *)(local_8 + 0xc88) = 1;
    local_44 = local_44 & 0xffff0000;
    local_48 = 0;
    iVar3 = FUN__text__004128f0(0xcb,1);
    if (iVar3 != 0) {
      local_48 = FUN__text__004b6fb0(0,CONCAT22(extraout_var_04,DAT_007d6a34));
      local_44 = CONCAT22(local_44._2_2_,1);
      FUN__text__004db2b0(5);
    }
    iVar3 = FUN__text__004128f0(0xcd,1);
    uVar6 = extraout_var_05;
    if (iVar3 != 0) {
      local_48 = FUN__text__004b6fb0(1,DAT_007d6a34);
      local_44 = CONCAT22(local_44._2_2_,1);
      FUN__text__004db2b0(5);
      uVar6 = extraout_var_06;
    }
    if ((local_44 & 0xffff) != 0) {
      DAT_007d6a34 = local_48;
      FUN__text__004b6690(CONCAT22(uVar6,*(undefined2 *)(local_8 + 0x596 + local_48 * 2)),0xffffffff
                          ,1,2);
      FUN__text__004b6690(CONCAT22(extraout_var_07,
                                   *(undefined2 *)(local_8 + 0x596 + DAT_007d6a34 * 2)),0xffffffff,0
                          ,0);
      DAT_007d6a52 = 0xffff;
      DAT_007d6a56 = -1;
    }
    FUN__text__004b6c60();
    uVar1 = FUN__text__004b0f80();
    local_a4 = (uVar1 & 0xffff) - 1;
    switch(local_a4) {
    case 0:
      DAT_007d6a5a = 0;
      break;
    case 1:
      if (DAT_007d6a5a != 0) {
        DAT_007d6a5a = DAT_007d6a5a + -1;
      }
      break;
    case 2:
      if (DAT_007d6a5a != 9) {
        DAT_007d6a5a = DAT_007d6a5a + 1;
      }
      break;
    case 3:
      DAT_007d6a5a = 9;
    }
    break;
  case 2:
    DAT_007d6a30 = 2;
    FUN__text__004d5c40(&local_18,0);
    if ((local_18 & 1) == 0) {
      FUN__text__004db2b0(5);
      DAT_007d6a50 = 1;
      _local_5c = CONCAT22(uStack_5a,(ushort)(byte)local_38[3]);
      local_60 = (ushort)(byte)local_38[4];
      local_64 = local_64 & 0xffff0000;
      local_68 = local_68 & 0xffff0000;
      local_20 = local_20 & 0xffff0000;
      while ((local_20 & 0xffff) < (uint)(byte)local_38[4]) {
        sVar4 = (short)_local_5c + (short)local_20;
        local_64 = CONCAT22(local_64._2_2_,sVar4);
        FUN__text__004b10b0(&local_18,sVar4);
        if ((local_c & 0xffff) != 0) {
          local_1c = &DAT_0061bc10;
          FUN__text__004d2ca0(0xd,0x35,DAT_0061bc12,(local_64 & 0xffff) * 0x24 + 0x16e,0x1be,
                              DAT_0061bc14,DAT_0061bc16,DAT_0061bc18,DAT_0061bc1a);
          local_ac = FUN__text__004b1110(local_3c,CONCAT22(extraout_var,(short)local_20),
                                         CONCAT22(extraout_var_09,DAT_007d6a56));
          local_ac = local_ac & 0xffff;
          if (local_ac == 0) {
            FUN__text__004d48a0(CONCAT22(extraout_var_03,
                                         *(undefined2 *)(local_8 + 0x596 + DAT_007d6a34 * 2)),8,
                                0xffffffff,0);
          }
          else if (local_ac == 1) {
            FUN__text__004d48a0(CONCAT22(extraout_var_03,
                                         *(undefined2 *)(local_8 + 0x596 + DAT_007d6a34 * 2)),0xb,
                                0xffffffff,0);
            uVar5 = *(ushort *)(local_3c + (local_20 & 0xffff) * 2 + 0x62);
            _local_6c = CONCAT22(uStack_6a,uVar5);
            if (uVar5 == 0) {
              *(short *)(local_3c + (local_20 & 0xffff) * 2 + 0x62) = DAT_007d6a56;
            }
            else {
              *(ushort *)(&DAT_007aacaa + (uint)uVar5 * 2) =
                   *(ushort *)(&DAT_007aacaa + (uint)uVar5 * 2) & 0xf0ff | 0x100;
              *(short *)(local_3c + (local_20 & 0xffff) * 2 + 0x62) = DAT_007d6a56;
            }
            local_68 = CONCAT22(local_68._2_2_,1);
          }
        }
        local_20 = CONCAT22(local_20._2_2_,(short)local_20 + 1);
      }
      if ((local_68 & 0xffff) == 0) {
        *(ushort *)(&DAT_007aacaa + DAT_007d6a56 * 2) =
             *(ushort *)(&DAT_007aacaa + DAT_007d6a56 * 2) & 0xf0ff | (DAT_007d6a5c & 0xf) << 8;
      }
      FUN__text__004b6690(local_34 & 0xffff,0xffffffff,0,0);
    }
    else {
      _local_4c = CONCAT22(uStack_4a,(ushort)(byte)local_38[3]);
      local_50 = (ushort)(byte)local_38[4];
      local_54 = local_54 & 0xffff0000;
      local_58 = 1;
      local_20 = local_20 & 0xffff0000;
      while ((local_20 & 0xffff) < (uint)(byte)local_38[4]) {
        sVar4 = (short)_local_4c + (short)local_20;
        local_54 = CONCAT22(local_54._2_2_,sVar4);
        FUN__text__004b10b0(&local_18,sVar4);
        if ((local_c & 0xffff) != 0) {
          local_1c = &DAT_0061bc10;
          FUN__text__004d2ca0(0xd,0x35,DAT_0061bc12,(local_54 & 0xffff) * 0x24 + 0x16e,0x1be,
                              DAT_0061bc14,DAT_0061bc16,DAT_0061bc18,DAT_0061bc1a);
          local_58 = 2;
          local_a8 = FUN__text__004b1110(local_3c,CONCAT22(extraout_var_08,(short)local_20),
                                         CONCAT22(extraout_var_02,DAT_007d6a56));
          local_a8 = local_a8 & 0xffff;
          if (local_a8 == 0) {
            local_58 = 2;
          }
          else if (local_a8 == 1) {
            local_58 = 1;
          }
        }
        local_20 = CONCAT22(local_20._2_2_,(short)local_20 + 1);
      }
      FUN__text__004b4b00(*(short *)(DAT_007a49fc + 0x196c) + -0x10,
                          *(short *)(DAT_007a49fc + 0x1970) + -0x10,DAT_007d6a56 + -1,local_58,0x34)
      ;
    }
    break;
  case 3:
    DAT_007d6a30 = 2;
    local_1c = &DAT_0061bc10;
    FUN__text__004d2ca0(0xd,0x35,DAT_0061bc12,DAT_007d6a60 * 0x24 + 0x16e,0x1be,DAT_0061bc14,
                        DAT_0061bc16,DAT_0061bc18,DAT_0061bc1a);
    FUN__text__004b4b00(DAT_007d6a60 * 0x24 + 0x16f,0x1bf,DAT_007d6a56 + -1,5,0x3f);
    FUN__text__004d5c40(&local_18,0);
    if ((local_18 & 1) == 0) {
      DAT_007d6a50 = 1;
      FUN__text__004db2b0(5);
      _local_7c = CONCAT22(uStack_7a,(ushort)(byte)local_38[3]);
      local_80 = (ushort)(byte)local_38[4];
      local_84 = 0;
      local_88 = local_88 & 0xffff0000;
      local_20 = local_20 & 0xffff0000;
      while ((local_20 & 0xffff) < (uint)(byte)local_38[4]) {
        local_84 = (short)_local_7c + (short)local_20;
        FUN__text__004b10b0(&local_18,local_84);
        if ((local_c & 0xffff) != 0) {
          _local_8c = CONCAT22(uStack_8a,*(short *)(local_3c + (local_20 & 0xffff) * 2 + 0x62));
          if (*(short *)(local_3c + (local_20 & 0xffff) * 2 + 0x62) != 0) {
            *(undefined2 *)(local_3c + DAT_007d6a5e * 2 + 0x62) =
                 *(undefined2 *)(local_3c + (local_20 & 0xffff) * 2 + 0x62);
          }
          *(short *)(local_3c + (local_20 & 0xffff) * 2 + 0x62) = DAT_007d6a56;
          FUN__text__004db2b0(5);
          local_88 = CONCAT22(local_88._2_2_,1);
        }
        local_20 = CONCAT22(local_20._2_2_,(short)local_20 + 1);
      }
      if ((local_88 & 0xffff) == 0) {
        *(ushort *)(&DAT_007aacaa + DAT_007d6a56 * 2) =
             *(ushort *)(&DAT_007aacaa + DAT_007d6a56 * 2) & 0xf0ff | 0x100;
      }
      FUN__text__004b6690(local_34 & 0xffff,0xffffffff,0,0);
    }
    else {
      FUN__text__004b4b00(*(short *)(DAT_007a49fc + 0x196c) + -0x10,
                          *(short *)(DAT_007a49fc + 0x1970) + -0x10,DAT_007d6a56 + -1,1,0x34);
      _local_70 = CONCAT22(uStack_6e,(ushort)(byte)local_38[3]);
      local_74 = (ushort)(byte)local_38[4];
      local_78 = local_78 & 0xffff0000;
      local_20 = local_20 & 0xffff0000;
      while ((local_20 & 0xffff) < (uint)(byte)local_38[4]) {
        sVar4 = (short)_local_70 + (short)local_20;
        local_78 = CONCAT22(local_78._2_2_,sVar4);
        FUN__text__004b10b0(&local_18,sVar4);
        if ((local_c & 0xffff) != 0) {
          FUN__text__004d2ca0(0xd,0x35,*(undefined2 *)(local_1c + 2),
                              (local_78 & 0xffff) * 0x24 + 0x16e,0x1be,*(undefined2 *)(local_1c + 4)
                              ,*(undefined2 *)(local_1c + 6),*(undefined2 *)(local_1c + 8),
                              *(undefined2 *)(local_1c + 10));
        }
        local_20 = CONCAT22(local_20._2_2_,(short)local_20 + 1);
      }
    }
  }
  local_28 = (uint)local_28._2_2_ << 0x10;
  while( true ) {
    if (6 < (local_28 & 0xffff)) break;
    local_24 = local_24 & 0xffff0000;
    while ((local_24 & 0xffff) < 0xc) {
      uVar5 = (short)local_28 * 0xc + (short)local_24 + DAT_007d6a5a * 0xc;
      local_2c = CONCAT22(local_2c._2_2_,uVar5);
      local_30 = CONCAT22(local_30._2_2_,uVar5 + 1);
      uVar1 = (uint)uVar5;
      if ((*(ushort *)(&DAT_007aacac + uVar1 * 2) & 1) != 0) {
        if (DAT_007d6a50 == 1) {
          FUN__text__004d5ec0(&local_18,(local_24 & 0xffff) * 0x24 + 0xf0,
                              (local_28 & 0xffff) * 0x24 + 0x1e9,0x23,0x23);
          uVar1 = 0;
          if ((local_c & 0xffff) != 0) {
            FUN__text__004d2690((local_24 & 0xffff) * 0x24 + 0xf0,(local_28 & 0xffff) * 0x24 + 0x1e9
                                ,0x24,0x24,0x3e,0xffffffff,1);
            if ((*(ushort *)(&DAT_007aacac + (local_2c & 0xffff) * 2) >> 8 & 0xf) == 1) {
              DAT_007d6a30 = 1;
            }
            if (DAT_007d6a31 != '\0') {
              DAT_007d6a30 = 0;
            }
            uVar1 = 0;
            if ((local_14 & 1) != 0) {
              DAT_007d7c26 = (undefined2)local_2c;
              FUN__text__004db2b0(5);
              DAT_007d6a52 = (short)local_24;
              uVar1 = CONCAT22(extraout_var_00,(short)local_28);
              DAT_007d6a54 = (short)local_28;
              DAT_007d6a56 = (short)local_30;
              if (DAT_007d6a31 == '\0') {
                uVar1 = local_2c & 0xffff;
                if ((*(ushort *)(&DAT_007aacac + uVar1 * 2) >> 8 & 0xf) == 1) {
                  DAT_007d6a30 = 2;
                  DAT_007d6a50 = 2;
                  DAT_007d6a5c = (byte)((ushort)*(undefined2 *)
                                                 (&DAT_007aacac + (local_2c & 0xffff) * 2) >> 8) &
                                 0xf;
                  *(ushort *)(&DAT_007aacac + (local_2c & 0xffff) * 2) =
                       *(ushort *)(&DAT_007aacac + (local_2c & 0xffff) * 2) & 0xf0ff | 0x300;
                  uVar1 = local_2c & 0xffff;
                  *(ushort *)(&DAT_007aacac + uVar1 * 2) =
                       *(ushort *)(&DAT_007aacac + (local_2c & 0xffff) * 2) & 0xff01 |
                       (*(ushort *)(local_8 + 0x596 + DAT_007d6a34 * 2) & 0x7f) << 1;
                }
                else {
                  DAT_007d6a30 = 0;
                }
              }
              else {
                DAT_007d6a30 = 0;
              }
            }
          }
        }
        FUN__text__004b4b00((local_24 & 0xffff) * 0x24 + 0xf1,(local_28 & 0xffff) * 0x24 + 0x1e9,
                            (local_30 & 0xffff) - 1,
                            CONCAT22((short)(uVar1 >> 0x10),
                                     *(ushort *)(&DAT_007aacac + (local_2c & 0xffff) * 2) >> 8) &
                            0xffff000f,0x3f);
        if ((int)DAT_007d6a56 == (local_30 & 0xffff)) {
          local_1c = &DAT_0061bc10;
          FUN__text__004d2ca0(0xd,0x35,DAT_0061bc12,(local_24 & 0xffff) * 0x24 + 0xf1,
                              (local_28 & 0xffff) * 0x24 + 0x1ea,DAT_0061bc14,DAT_0061bc16,
                              DAT_0061bc18,DAT_0061bc1a);
        }
      }
      local_24 = CONCAT22(local_24._2_2_,(short)local_24 + 1);
    }
    local_28 = CONCAT22(local_28._2_2_,(short)local_28 + 1);
  }
  if (DAT_007d6a56 < 1) {
    FUN__text__004b4b00(0x2a9,0x1e9,DAT_007d6a56 + -1,6,0x3f);
  }
  else {
    FUN__text__004b4b00(0x2a9,0x1e9,DAT_007d6a56 + -1,1,0x3f);
    FUN__text__004b4520(CONCAT22(extraout_var_01,DAT_007d6a56));
  }
  if (0 < DAT_007d6a56) {
    if (*(short *)(local_8 + 0x391d4) != DAT_007d6a56) {
      FUN__text__004d64d0(DAT_007d6a56,4);
      if (DAT_007d6a56 < 1) goto LAB__text__004b0c64;
      local_90 = 4;
      FUN__text__004d60e0(1);
      local_b0 = *(ushort *)(&DAT_006d5120 + DAT_007d6a56 * 0x38) - 1;
      switch(local_b0) {
      case 0:
        FUN__text__004d6150(" VULGAR");
        break;
      case 1:
        FUN__text__004d6150(" Common");
        break;
      case 2:
        FUN__text__004d6150("Superior");
        break;
      case 3:
        FUN__text__004d6150("  Rare");
        break;
      case 4:
        FUN__text__004d6150(" Mystic");
        break;
      case 5:
        FUN__text__004d6150(" Hory");
        break;
      case 6:
        FUN__text__004d6150(" Divine");
        break;
      case 7:
        FUN__text__004d6150(" Special");
        break;
      default:
        FUN__text__004d6150("!!!!ERROR!!!!");
      }
    }
    FUN__text__004d62f0(0x3a9,0x212,0x3d);
    FUN__text__004d62f0(0x2b2,0x2b6,0x3d);
    *(short *)(local_8 + 0x391d4) = DAT_007d6a56;
  }
LAB__text__004b0c64:
  if (0 < DAT_007d6a56) {
    local_94 = CONCAT22(local_94._2_2_,9);
    if (DAT_007d6a58 != DAT_007d6a56) {
      FUN__text__004077c0(DAT_007a49fc);
      uVar10 = 2;
      puVar9 = (&PTR_DAT_006e3150)[DAT_007d6a56];
      uVar8 = *(undefined4 *)(local_8 + 0xc8c);
      uVar2 = FUN__text__004142b0(uVar8,puVar9,2);
      FUN__text__00408e30(uVar2,uVar8,puVar9,uVar10);
    }
    *(undefined2 *)(&DAT_007d6ada + (local_94 & 0xffff) * 0x80) = 0x3d;
    FUN__text__00408f90((0x78 - *(short *)(&DAT_007d6aa4 + (local_94 & 0xffff) * 0x80)) / 2 + 0x2d0,
                        0x1ed);
  }
  local_b4 = FUN__text__004b6c60();
  local_b4 = local_b4 & 0xffff;
  if (local_b4 == 1) {
    FUN__text__004d6230(0);
  }
  else if (local_b4 == 2) {
    FUN__text__004d6230(1);
  }
  FUN__text__004d5ec0(&local_18,0x2b6,0x1c3,0x8a,0x1c);
  if (((local_c & 0xffff) != 0) && ((local_14 & 1) != 0)) {
    FUN__text__004db2b0(5);
    if (DAT_007d6a31 == '\0') {
      DAT_007d6a31 = '\x01';
    }
    else {
      DAT_007d6a31 = '\0';
    }
  }
  if (DAT_007d6a31 != '\0') {
    local_1c = &DAT_0061bc70;
    FUN__text__004d2ca0(0xd,0x48,DAT_0061bc72,DAT_0061bc7c,DAT_0061bc7e,DAT_0061bc74,DAT_0061bc76,
                        DAT_0061bc78,DAT_0061bc7a);
  }
  local_98 = CONCAT22(local_98._2_2_,
                      (ushort)(byte)(&DAT_006b2d8b)[(uint)*(ushort *)(local_8 + 0x632) * 0x40]);
  local_9c = (uint)local_9c._2_2_ << 0x10;
  while ((local_9c & 0xffff) < 8) {
    if ((local_9c & 0xffff) < (local_98 & 0xffff)) {
      FUN__text__004d2620((local_9c & 0xffff) * 0x24 + 0x16f,0x1bf,0x22,0x22,0x36,0x700000a0,1);
    }
    local_9c = CONCAT22(local_9c._2_2_,(short)local_9c + 1);
  }
  local_8 = 0x4b0f2f;
  FUN__text__0056ce80();
  return;
}

