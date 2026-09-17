
void __fastcall FUN__text__004abb60(int param_1)

{
  uint uVar1;
  ushort uVar2;
  short sVar3;
  int *piVar4;
  undefined2 extraout_var;
  int iVar5;
  undefined2 extraout_var_00;
  undefined2 extraout_var_01;
  undefined2 extraout_var_02;
  undefined2 extraout_var_03;
  undefined4 *puVar6;
  int *piVar7;
  undefined4 *puVar8;
  undefined4 local_750 [16];
  char local_710;
  uint local_70c;
  int local_708;
  undefined1 local_704 [32];
  undefined1 local_6e4 [32];
  short local_6c4;
  undefined4 local_6c0;
  char local_6bc;
  undefined4 local_6b8;
  undefined1 local_6b4 [8];
  undefined4 local_6ac;
  undefined1 local_5bc [16];
  undefined1 local_5ac;
  int local_4c4;
  int local_4c0;
  uint local_4bc;
  uint local_4b8;
  uint local_4b4;
  char local_4b0;
  undefined3 uStack_4af;
  int local_4ac;
  undefined1 local_4a8 [8];
  int local_4a0;
  int local_3b0;
  int local_3ac;
  int local_3a8 [8];
  short local_388;
  uint local_384;
  uint local_380;
  undefined4 local_37c;
  undefined4 local_378;
  short local_374;
  uint local_370;
  uint local_36c;
  byte local_368 [424];
  int local_1c0 [8];
  undefined2 local_1a0;
  int local_19c [8];
  undefined2 local_17c;
  undefined1 local_178 [12];
  int local_16c;
  int local_80 [8];
  int local_60;
  short local_5c;
  int local_58;
  int local_54;
  char local_50;
  short local_4c;
  short local_48;
  uint local_44;
  byte local_40;
  uint local_3c;
  uint local_38;
  uint local_34;
  uint local_30;
  undefined *local_2c;
  ushort local_28;
  undefined2 uStack_26;
  undefined4 local_24;
  uint local_20;
  undefined4 local_1c;
  undefined1 local_18 [4];
  uint local_14;
  uint local_c;
  int local_8;
  
  puVar6 = local_750;
  for (iVar5 = 0x1d3; iVar5 != 0; iVar5 = iVar5 + -1) {
    *puVar6 = 0xcccccccc;
    puVar6 = puVar6 + 1;
  }
  local_30 = local_30 & 0xffff0000;
  local_34 = local_34 & 0xffff0000;
  local_38 = local_38 & 0xffff0000;
  local_3c = CONCAT22(local_3c._2_2_,1);
  local_40 = 0;
  local_708 = (int)DAT_007a528c;
  if ((local_708 < 0) || (1 < local_708)) {
    local_44 = CONCAT22(local_44._2_2_,0x87);
  }
  else {
    local_44 = CONCAT22(local_44._2_2_,100);
  }
  *(undefined1 *)(param_1 + 0xc88) = 1;
  local_1c = local_1c & 0xffff0000;
  while ((local_1c & 0xffff) < 7) {
    if (*(short *)(&DAT_007d71fa + (local_1c & 0xffff) * 2) != 0) {
      local_34 = CONCAT22(local_34._2_2_,1);
    }
    local_1c = CONCAT22(local_1c._2_2_,(short)local_1c + 1);
  }
  local_8 = param_1;
  if ((local_34 & 0xffff) == 0) {
    FUN__text__004d2620(0x392,0x2d6,0x5b,0x1e,0x37,0x70010101,1);
  }
  else {
    FUN__text__004d5ec0(local_18,0x393,0x2d7,0x59,0x1c);
    if ((local_14 & 1) != 0) {
      FUN__text__004db2b0(1);
      local_1c = local_1c & 0xffff0000;
      while ((local_1c & 0xffff) < 10) {
        *(undefined2 *)(&DAT_007d71fa + (local_1c & 0xffff) * 2) = 0;
        *(undefined4 *)(&DAT_007d7230 + (local_1c & 0xffff) * 4) = 0;
        *(undefined2 *)(&DAT_007d7254 + (local_1c & 0xffff) * 2) = 0;
        local_1c = CONCAT22(local_1c._2_2_,(short)local_1c + 1);
      }
      FUN__text__004b6690(*(undefined2 *)(local_8 + 0x596 + DAT_007d6a34 * 2),0xffffffff,1,2);
      FUN__text__004b6690(CONCAT22(extraout_var_00,
                                   *(undefined2 *)(local_8 + 0x596 + DAT_007d6a34 * 2)),0xffffffff,0
                          ,0);
      puVar6 = (undefined4 *)
               (&DAT_007e17e8 + *(short *)(local_8 + 0x596 + DAT_007d6a34 * 2) * 0x4a0);
      puVar8 = &DAT_007d7264;
      for (iVar5 = 0x128; iVar5 != 0; iVar5 = iVar5 + -1) {
        *puVar8 = *puVar6;
        puVar6 = puVar6 + 1;
        puVar8 = puVar8 + 1;
      }
      DAT_007d6f66 = 1;
    }
  }
  if (DAT_007d72b4 != '2') {
    local_38 = CONCAT22(local_38._2_2_,1);
  }
  local_70c = (uint)DAT_007d6f66;
  if (local_70c < 2) {
    puVar6 = (undefined4 *)(&DAT_007e17e8 + *(short *)(local_8 + 0x596 + DAT_007d6a34 * 2) * 0x4a0);
    puVar8 = &DAT_007d7264;
    for (iVar5 = 0x128; iVar5 != 0; iVar5 = iVar5 + -1) {
      *puVar8 = *puVar6;
      puVar6 = puVar6 + 1;
      puVar8 = puVar8 + 1;
    }
    DAT_007d6f64 = -1;
    local_1c = local_1c & 0xffff0000;
    while ((local_1c & 0xffff) < 8) {
      *(undefined2 *)(&DAT_007d71fa + (local_1c & 0xffff) * 2) = 0;
      *(undefined4 *)(&DAT_007d7230 + (local_1c & 0xffff) * 4) = 0;
      *(undefined2 *)(&DAT_007d7254 + (local_1c & 0xffff) * 2) = 0;
      local_1c = CONCAT22(local_1c._2_2_,(short)local_1c + 1);
    }
    DAT_007d7250 = 0;
    local_48 = 0;
    DAT_007d6f68 = 0;
    local_1c = (uint)local_1c._2_2_ << 0x10;
    while ((local_1c & 0xffff) < 0x1e) {
      if (*(short *)(local_8 + 0x596 + (local_1c & 0xffff) * 2) != -1) {
        local_48 = 0;
        sVar3 = *(short *)(local_8 + 0x596 + (local_1c & 0xffff) * 2);
        local_24 = (uint)local_24._2_2_ << 0x10;
        while ((local_24 & 0xffff) < 7) {
          uVar2 = (ushort)(byte)(&DAT_007e17f4)[(local_24 & 0xffff) * 8 + sVar3 * 0x4a0];
          _local_28 = CONCAT22(uStack_26,uVar2);
          *(ushort *)(&DAT_007d6f6a + (local_24 & 0xffff) * 2 + (uint)DAT_007d6f68 * 0x10) = uVar2;
          local_48 = local_48 + uVar2;
          local_24 = CONCAT22(local_24._2_2_,(short)local_24 + 1);
        }
        *(short *)(&DAT_007d6f6a + (local_24 & 0xffff) * 2 + (uint)DAT_007d6f68 * 0x10) = local_48;
        DAT_007d6f68 = DAT_007d6f68 + 1;
      }
      local_1c = CONCAT22(local_1c._2_2_,(short)local_1c + 1);
    }
    local_24 = (uint)local_24._2_2_ << 0x10;
    while ((local_24 & 0xffff) < 8) {
      local_4c = 1;
      local_1c = local_1c & 0xffff0000;
      while ((local_1c & 0xffff) < (uint)DAT_007d6f68) {
        if (((int)DAT_007d6a34 != (local_1c & 0xffff)) &&
           (*(ushort *)(&DAT_007d6f6a + (local_24 & 0xffff) * 2 + DAT_007d6a34 * 0x10) <
            *(ushort *)(&DAT_007d6f6a + (local_24 & 0xffff) * 2 + (local_1c & 0xffff) * 0x10))) {
          local_4c = local_4c + 1;
        }
        local_1c = CONCAT22(local_1c._2_2_,(short)local_1c + 1);
      }
      *(short *)(&DAT_007d720a + (local_24 & 0xffff) * 2) = local_4c;
      local_24 = CONCAT22(local_24._2_2_,(short)local_24 + 1);
    }
    DAT_007d6f66 = 2;
  }
  else if (local_70c != 2) goto LAB__text__004ac5f4;
  local_2c = &DAT_007e17e8 + *(short *)(local_8 + 0x596 + DAT_007d6a34 * 2) * 0x4a0;
  local_1c = local_1c & 0xffff0000;
  while ((local_1c & 0xffff) < 7) {
    *(ushort *)(&DAT_007d71ea + (local_1c & 0xffff) * 2) =
         (ushort)(byte)local_2c[(local_1c & 0xffff) * 8 + 0xc];
    _local_28 = CONCAT22(uStack_26,(ushort)(byte)local_2c[(local_1c & 0xffff) * 8 + 0xc]);
    local_50 = '\x02';
    local_40 = 0;
    if ((uint)(ushort)(byte)local_2c[(local_1c & 0xffff) * 8 + 0xc] +
        (uint)*(ushort *)(&DAT_007d71fa + (local_1c & 0xffff) * 2) == (local_44 & 0xffff)) {
      local_50 = '\x01';
    }
    else {
      local_60 = 0;
      local_20 = local_20 & 0xffff0000;
      while ((local_20 & 0xffff) < 7) {
        local_5c = (ushort)(byte)local_2c[(local_20 & 0xffff) * 8 + 0xc] +
                   *(short *)(&DAT_007d71fa + (local_20 & 0xffff) * 2);
        if ((local_1c & 0xffff) == (local_20 & 0xffff)) {
          piVar4 = (int *)FUN__text__004d56a0(local_6e4,local_5c,0);
          piVar7 = local_80;
          for (iVar5 = 8; iVar5 != 0; iVar5 = iVar5 + -1) {
            *piVar7 = *piVar4;
            piVar4 = piVar4 + 1;
            piVar7 = piVar7 + 1;
          }
          local_54 = *(int *)(local_2c + (local_20 & 0xffff) * 8 + 0x10);
          local_60 = local_60 + (local_80[1] - local_54);
        }
        else {
          piVar4 = (int *)FUN__text__004d56a0(local_704,local_5c,0);
          piVar7 = local_80;
          for (iVar5 = 8; iVar5 != 0; iVar5 = iVar5 + -1) {
            *piVar7 = *piVar4;
            piVar4 = piVar4 + 1;
            piVar7 = piVar7 + 1;
          }
          local_54 = *(int *)(local_2c + (local_20 & 0xffff) * 8 + 0x10);
          local_58 = local_80[0] - local_54;
          if (0 < local_58) {
            local_60 = local_60 + local_58;
          }
        }
        local_20 = CONCAT22(local_20._2_2_,(short)local_20 + 1);
      }
      if (DAT_007a511c < local_60) {
        local_50 = '\0';
        local_40 = 2;
      }
      else {
        FUN__text__004d58e0(local_178,*(undefined2 *)(local_8 + 0x596 + DAT_007d6a34 * 2));
        if (local_16c < local_60) {
          local_50 = '\0';
          local_40 = 2;
        }
      }
    }
    if ((((local_38 & 0xffff) != 0) &&
        (FUN__text__004d5ec0(local_18,0x1b1,(local_1c & 0xffff) * 0x22 + 0x1e9,0x15,0x12),
        (local_14 & 1) != 0)) && (local_710 = local_50, local_50 == '\x02')) {
      FUN__text__004d68b0(&DAT_0061c010,0x4c,0x1a7,(local_1c & 0xffff) * 0x22 + 0x1e1,8);
      FUN__text__004db2b0(5);
      local_3c = local_3c & 0xffff0000;
      *(short *)(&DAT_007d71fa + (local_1c & 0xffff) * 2) =
           *(short *)(&DAT_007d71fa + (local_1c & 0xffff) * 2) + 1;
      local_17c = (undefined2)
                  ((uint)(byte)local_2c[(local_1c & 0xffff) * 8 + 0xc] +
                  (uint)*(ushort *)(&DAT_007d71fa + (local_1c & 0xffff) * 2));
      FUN__text__004d56a0(local_19c,
                          (uint)(byte)local_2c[(local_1c & 0xffff) * 8 + 0xc] +
                          (uint)*(ushort *)(&DAT_007d71fa + (local_1c & 0xffff) * 2),0);
      *(int *)(&DAT_007d7230 + (local_1c & 0xffff) * 4) =
           local_19c[0] - *(int *)(local_2c + (local_1c & 0xffff) * 8 + 0x10);
    }
    FUN__text__004d5ec0(local_18,0x1d5,(local_1c & 0xffff) * 0x22 + 0x1e9,0x15,0x12);
    if (((local_14 & 1) != 0) && (*(short *)(&DAT_007d71fa + (local_1c & 0xffff) * 2) != 0)) {
      *(short *)(&DAT_007d71fa + (local_1c & 0xffff) * 2) =
           *(short *)(&DAT_007d71fa + (local_1c & 0xffff) * 2) + -1;
      FUN__text__004d68b0(&DAT_0061c020,0x4c,0x1cc,(local_1c & 0xffff) * 0x22 + 0x1e1,8);
      FUN__text__004db2b0(5);
      if (*(short *)(&DAT_007d71fa + (local_1c & 0xffff) * 2) == 0) {
        *(undefined4 *)(&DAT_007d7230 + (local_1c & 0xffff) * 4) = 0;
      }
      else {
        local_1a0 = (undefined2)
                    ((uint)(byte)local_2c[(local_1c & 0xffff) * 8 + 0xc] +
                    (uint)*(ushort *)(&DAT_007d71fa + (local_1c & 0xffff) * 2));
        FUN__text__004d56a0(local_1c0,
                            (uint)(byte)local_2c[(local_1c & 0xffff) * 8 + 0xc] +
                            (uint)*(ushort *)(&DAT_007d71fa + (local_1c & 0xffff) * 2),0);
        *(int *)(&DAT_007d7230 + (local_1c & 0xffff) * 4) =
             local_1c0[0] - *(int *)(local_2c + (local_1c & 0xffff) * 8 + 0x10);
      }
      local_40 = 0;
      local_3c = local_3c & 0xffff0000;
    }
    if (*(short *)(&DAT_007d71fa + (local_1c & 0xffff) * 2) == 0) {
      FUN__text__004d2620(0x1ce,(local_1c & 0xffff) * 0x22 + 0x1e5,0x1f,0x19,0x37,0x70010101,1);
    }
    *(ushort *)(&DAT_007d7254 + (local_1c & 0xffff) * 2) = (ushort)local_40;
    local_1c = CONCAT22(local_1c._2_2_,(short)local_1c + 1);
  }
  if ((local_3c & 0xffff) == 0) {
    local_1c = local_1c & 0xffff0000;
    while ((local_1c & 0xffff) < 8) {
      (&DAT_007d7270)[(local_1c & 0xffff) * 8] =
           (char)*(undefined2 *)(&DAT_007d71ea + (local_1c & 0xffff) * 2) +
           (char)*(undefined2 *)(&DAT_007d71fa + (local_1c & 0xffff) * 2);
      local_1c = CONCAT22(local_1c._2_2_,(short)local_1c + 1);
    }
    FUN__text__004b66f0(&DAT_007d7264,0xffffffff,0,0);
  }
LAB__text__004ac5f4:
  FUN__text__004d2700(&DAT_0061bb30,0,0x4e,0xd7,0x1a7);
  local_368[0] = 1;
  local_368[1] = 9;
  local_368[2] = 0xb;
  local_368[3] = 5;
  local_368[4] = 6;
  local_368[5] = 1;
  local_368[6] = 9;
  local_368[7] = 0xb;
  local_368[8] = 5;
  local_368[9] = 6;
  local_368[10] = 1;
  local_368[0xb] = 9;
  local_368[0xc] = 0xb;
  local_368[0xd] = 0;
  local_368[0xe] = 0;
  local_368[0xf] = 1;
  local_368[0x10] = 9;
  local_368[0x11] = 0xb;
  local_368[0x12] = 0;
  local_368[0x13] = 0;
  local_368[0x14] = 1;
  local_368[0x15] = 9;
  local_368[0x16] = 0xb;
  local_368[0x17] = 6;
  local_368[0x18] = 0xf;
  local_368[0x19] = 1;
  local_368[0x1a] = 9;
  local_368[0x1b] = 0xb;
  local_368[0x1c] = 0;
  local_368[0x1d] = 0;
  local_368[0x1e] = 1;
  local_368[0x1f] = 9;
  local_368[0x20] = 0xb;
  local_368[0x21] = 0;
  local_368[0x22] = 0;
  local_368[0x23] = 1;
  local_368[0x24] = 9;
  local_368[0x25] = 0xb;
  local_368[0x26] = 0;
  local_368[0x27] = 0;
  local_368[0x28] = 1;
  local_368[0x29] = 9;
  local_368[0x2a] = 0xb;
  local_368[0x2b] = 0;
  local_368[0x2c] = 0;
  local_368[0x2d] = 1;
  local_368[0x2e] = 9;
  local_368[0x2f] = 0xb;
  local_368[0x30] = 0;
  local_368[0x31] = 0;
  local_368[0x32] = 1;
  local_368[0x33] = 1;
  local_368[0x34] = 1;
  local_368[0x35] = 8;
  local_368[0x36] = 0xe;
  local_368[0x37] = 1;
  local_368[0x38] = 0;
  local_368[0x39] = 0;
  local_368[0x3a] = 8;
  local_368[0x3b] = 0xe;
  local_368[0x3c] = 1;
  local_368[0x3d] = 0;
  local_368[0x3e] = 0;
  local_368[0x3f] = 8;
  local_368[0x40] = 0xe;
  local_368[0x41] = 1;
  local_368[0x42] = 5;
  local_368[0x43] = 6;
  local_368[0x44] = 8;
  local_368[0x45] = 0xe;
  local_368[0x46] = 1;
  local_368[0x47] = 5;
  local_368[0x48] = 6;
  local_368[0x49] = 8;
  local_368[0x4a] = 0xe;
  local_368[0x4b] = 1;
  local_368[0x4c] = 0;
  local_368[0x4d] = 0;
  local_368[0x4e] = 8;
  local_368[0x4f] = 0xe;
  local_368[0x50] = 1;
  local_368[0x51] = 0;
  local_368[0x52] = 0;
  local_368[0x53] = 8;
  local_368[0x54] = 0xe;
  local_368[0x55] = 1;
  local_368[0x56] = 0;
  local_368[0x57] = 0;
  local_368[0x58] = 8;
  local_368[0x59] = 0xe;
  local_368[0x5a] = 1;
  local_368[0x5b] = 0;
  local_368[0x5c] = 0;
  local_368[0x5d] = 8;
  local_368[0x5e] = 0xe;
  local_368[0x5f] = 1;
  local_368[0x60] = 0;
  local_368[0x61] = 0;
  local_368[0x62] = 8;
  local_368[99] = 0xe;
  local_368[100] = 1;
  local_368[0x65] = 0;
  local_368[0x66] = 0;
  local_368[0x67] = 2;
  local_368[0x68] = 2;
  local_368[0x69] = 2;
  local_368[0x6a] = 0xd;
  local_368[0x6b] = 0x12;
  local_368[0x6c] = 0;
  local_368[0x6d] = 0;
  local_368[0x6e] = 0;
  local_368[0x6f] = 0xd;
  local_368[0x70] = 0x12;
  local_368[0x71] = 0;
  local_368[0x72] = 0;
  local_368[0x73] = 0;
  local_368[0x74] = 0xd;
  local_368[0x75] = 0x12;
  local_368[0x76] = 0;
  local_368[0x77] = 0;
  local_368[0x78] = 0;
  local_368[0x79] = 0xd;
  local_368[0x7a] = 0x12;
  local_368[0x7b] = 0;
  local_368[0x7c] = 0;
  local_368[0x7d] = 0;
  local_368[0x7e] = 0xd;
  local_368[0x7f] = 0x12;
  local_368[0x80] = 5;
  local_368[0x81] = 6;
  local_368[0x82] = 0xf;
  local_368[0x83] = 0xd;
  local_368[0x84] = 0x12;
  local_368[0x85] = 5;
  local_368[0x86] = 6;
  local_368[0x87] = 0xf;
  local_368[0x88] = 0xd;
  local_368[0x89] = 0x12;
  local_368[0x8a] = 0;
  local_368[0x8b] = 0;
  local_368[0x8c] = 0;
  local_368[0x8d] = 0xd;
  local_368[0x8e] = 0x12;
  local_368[0x8f] = 0;
  local_368[0x90] = 0;
  local_368[0x91] = 0;
  local_368[0x92] = 0xd;
  local_368[0x93] = 0x12;
  local_368[0x94] = 0;
  local_368[0x95] = 0;
  local_368[0x96] = 0;
  local_368[0x97] = 0xd;
  local_368[0x98] = 0x12;
  local_368[0x99] = 0;
  local_368[0x9a] = 0;
  local_368[0x9b] = 0;
  local_368[0x9c] = 3;
  local_368[0x9d] = 3;
  local_368[0x9e] = 3;
  local_368[0x9f] = 0x13;
  local_368[0xa0] = 2;
  local_368[0xa1] = 0xc;
  local_368[0xa2] = 0;
  local_368[0xa3] = 0;
  local_368[0xa4] = 0x13;
  local_368[0xa5] = 2;
  local_368[0xa6] = 0xc;
  local_368[0xa7] = 0;
  local_368[0xa8] = 0;
  local_368[0xa9] = 0x13;
  local_368[0xaa] = 2;
  local_368[0xab] = 0xc;
  local_368[0xac] = 0;
  local_368[0xad] = 0;
  local_368[0xae] = 0x13;
  local_368[0xaf] = 2;
  local_368[0xb0] = 0xc;
  local_368[0xb1] = 0;
  local_368[0xb2] = 0;
  local_368[0xb3] = 0x13;
  local_368[0xb4] = 2;
  local_368[0xb5] = 0xc;
  local_368[0xb6] = 0;
  local_368[0xb7] = 0;
  local_368[0xb8] = 0x13;
  local_368[0xb9] = 2;
  local_368[0xba] = 0xc;
  local_368[0xbb] = 0;
  local_368[0xbc] = 0;
  local_368[0xbd] = 0x13;
  local_368[0xbe] = 2;
  local_368[0xbf] = 0xc;
  local_368[0xc0] = 6;
  local_368[0xc1] = 0xf;
  local_368[0xc2] = 0x13;
  local_368[0xc3] = 2;
  local_368[0xc4] = 0xc;
  local_368[0xc5] = 6;
  local_368[0xc6] = 0xf;
  local_368[199] = 0x13;
  local_368[200] = 2;
  local_368[0xc9] = 0xc;
  local_368[0xca] = 0;
  local_368[0xcb] = 0;
  local_368[0xcc] = 0x13;
  local_368[0xcd] = 2;
  local_368[0xce] = 0xc;
  local_368[0xcf] = 0;
  local_368[0xd0] = 0;
  local_368[0xd1] = 4;
  local_368[0xd2] = 4;
  local_368[0xd3] = 4;
  local_368[0xd4] = 10;
  local_368[0xd5] = 2;
  local_368[0xd6] = 0;
  local_368[0xd7] = 0;
  local_368[0xd8] = 0;
  local_368[0xd9] = 10;
  local_368[0xda] = 2;
  local_368[0xdb] = 0;
  local_368[0xdc] = 0;
  local_368[0xdd] = 0;
  local_368[0xde] = 10;
  local_368[0xdf] = 2;
  local_368[0xe0] = 0;
  local_368[0xe1] = 0;
  local_368[0xe2] = 0;
  local_368[0xe3] = 10;
  local_368[0xe4] = 2;
  local_368[0xe5] = 0;
  local_368[0xe6] = 0;
  local_368[0xe7] = 0;
  local_368[0xe8] = 10;
  local_368[0xe9] = 2;
  local_368[0xea] = 0;
  local_368[0xeb] = 0;
  local_368[0xec] = 0;
  local_368[0xed] = 10;
  local_368[0xee] = 2;
  local_368[0xef] = 0;
  local_368[0xf0] = 0;
  local_368[0xf1] = 0;
  local_368[0xf2] = 10;
  local_368[0xf3] = 2;
  local_368[0xf4] = 0;
  local_368[0xf5] = 0;
  local_368[0xf6] = 0;
  local_368[0xf7] = 10;
  local_368[0xf8] = 2;
  local_368[0xf9] = 0;
  local_368[0xfa] = 0;
  local_368[0xfb] = 0;
  local_368[0xfc] = 10;
  local_368[0xfd] = 2;
  local_368[0xfe] = 6;
  local_368[0xff] = 0xf;
  local_368[0x100] = 0;
  local_368[0x101] = 10;
  local_368[0x102] = 2;
  local_368[0x103] = 6;
  local_368[0x104] = 0xf;
  local_368[0x105] = 0;
  local_368[0x106] = 5;
  local_368[0x107] = 5;
  local_368[0x108] = 5;
  local_368[0x109] = 1;
  local_368[0x10a] = 0xb;
  local_368[0x10b] = 0x12;
  local_368[0x10c] = 0;
  local_368[0x10d] = 0;
  local_368[0x10e] = 1;
  local_368[0x10f] = 0xb;
  local_368[0x110] = 0x12;
  local_368[0x111] = 0;
  local_368[0x112] = 0;
  local_368[0x113] = 1;
  local_368[0x114] = 0xb;
  local_368[0x115] = 0x12;
  local_368[0x116] = 0;
  local_368[0x117] = 0;
  local_368[0x118] = 1;
  local_368[0x119] = 0xb;
  local_368[0x11a] = 0x12;
  local_368[0x11b] = 0;
  local_368[0x11c] = 0;
  local_368[0x11d] = 1;
  local_368[0x11e] = 0xb;
  local_368[0x11f] = 0x12;
  local_368[0x120] = 0;
  local_368[0x121] = 0;
  local_368[0x122] = 1;
  local_368[0x123] = 0xb;
  local_368[0x124] = 0x12;
  local_368[0x125] = 0;
  local_368[0x126] = 0;
  local_368[0x127] = 1;
  local_368[0x128] = 0xb;
  local_368[0x129] = 0x12;
  local_368[0x12a] = 0;
  local_368[299] = 0;
  local_368[300] = 1;
  local_368[0x12d] = 0xb;
  local_368[0x12e] = 0x12;
  local_368[0x12f] = 0;
  local_368[0x130] = 0;
  local_368[0x131] = 1;
  local_368[0x132] = 0xb;
  local_368[0x133] = 0x12;
  local_368[0x134] = 0;
  local_368[0x135] = 0;
  local_368[0x136] = 1;
  local_368[0x137] = 0xb;
  local_368[0x138] = 0x12;
  local_368[0x139] = 0;
  local_368[0x13a] = 0;
  local_368[0x13b] = 6;
  local_368[0x13c] = 6;
  local_368[0x13d] = 6;
  local_368[0x13e] = 2;
  local_368[0x13f] = 0xc;
  local_368[0x140] = 0x13;
  local_368[0x141] = 0;
  local_368[0x142] = 0;
  local_368[0x143] = 2;
  local_368[0x144] = 0xc;
  local_368[0x145] = 0x13;
  local_368[0x146] = 0;
  local_368[0x147] = 0;
  local_368[0x148] = 2;
  local_368[0x149] = 0xc;
  local_368[0x14a] = 0x13;
  local_368[0x14b] = 0;
  local_368[0x14c] = 0;
  local_368[0x14d] = 2;
  local_368[0x14e] = 0xc;
  local_368[0x14f] = 0x13;
  local_368[0x150] = 0;
  local_368[0x151] = 0;
  local_368[0x152] = 2;
  local_368[0x153] = 0xc;
  local_368[0x154] = 0x13;
  local_368[0x155] = 0;
  local_368[0x156] = 0;
  local_368[0x157] = 2;
  local_368[0x158] = 0xc;
  local_368[0x159] = 0x13;
  local_368[0x15a] = 0;
  local_368[0x15b] = 0;
  local_368[0x15c] = 2;
  local_368[0x15d] = 0xc;
  local_368[0x15e] = 0x13;
  local_368[0x15f] = 0;
  local_368[0x160] = 0;
  local_368[0x161] = 2;
  local_368[0x162] = 0xc;
  local_368[0x163] = 0x13;
  local_368[0x164] = 0;
  local_368[0x165] = 0;
  local_368[0x166] = 2;
  local_368[0x167] = 0xc;
  local_368[0x168] = 0x13;
  local_368[0x169] = 0;
  local_368[0x16a] = 0;
  local_368[0x16b] = 2;
  local_368[0x16c] = 0xc;
  local_368[0x16d] = 0x13;
  local_368[0x16e] = 0;
  local_368[0x16f] = 0;
  local_368[0x170] = 7;
  local_368[0x171] = 7;
  local_368[0x172] = 7;
  local_368[0x173] = 0;
  local_368[0x174] = 0;
  local_368[0x175] = 0;
  local_368[0x176] = 0;
  local_368[0x177] = 0;
  local_368[0x178] = 0;
  local_368[0x179] = 0;
  local_368[0x17a] = 0;
  local_368[0x17b] = 0;
  local_368[0x17c] = 0;
  local_368[0x17d] = 0;
  local_368[0x17e] = 0;
  local_368[0x17f] = 0;
  local_368[0x180] = 0;
  local_368[0x181] = 0;
  local_368[0x182] = 0;
  local_368[0x183] = 0;
  local_368[0x184] = 0;
  local_368[0x185] = 0;
  local_368[0x186] = 0;
  local_368[0x187] = 0;
  local_368[0x188] = 0;
  local_368[0x189] = 0;
  local_368[0x18a] = 0;
  local_368[0x18b] = 0;
  local_368[0x18c] = 0;
  local_368[0x18d] = 0;
  local_368[0x18e] = 0;
  local_368[399] = 0;
  local_368[400] = 0;
  local_368[0x191] = 0;
  local_368[0x192] = 0;
  local_368[0x193] = 0;
  local_368[0x194] = 0;
  local_368[0x195] = 0;
  local_368[0x196] = 0;
  local_368[0x197] = 0;
  local_368[0x198] = 0;
  local_368[0x199] = 0;
  local_368[0x19a] = 0;
  local_368[0x19b] = 0;
  local_368[0x19c] = 0;
  local_368[0x19d] = 0;
  local_368[0x19e] = 0;
  local_368[0x19f] = 0;
  local_368[0x1a0] = 0;
  local_368[0x1a1] = 0;
  local_368[0x1a2] = 0;
  local_368[0x1a3] = 0;
  local_368[0x1a4] = 0;
  local_368[0x1a5] = 8;
  local_368[0x1a6] = 8;
  local_368[0x1a7] = 8;
  local_370 = CONCAT22(local_370._2_2_,
                       (ushort)(byte)(&DAT_006b2d8a)[*(short *)(local_2c + 6) * 0x40]);
  *(short *)(local_8 + 0x391da) = DAT_007d6f64;
  local_1c = local_1c & 0xffff0000;
  while( true ) {
    if (6 < (local_1c & 0xffff)) break;
    FUN__text__004d5ec0(local_18,0xe2,(local_1c & 0xffff) * 0x22 + 0x1e5,0x1a9,0x17);
    if ((local_14 & 1) != 0) {
      DAT_007d6f64 = (short)local_1c;
    }
    local_20 = local_20 & 0xffff0000;
    while ((local_20 & 0xffff) < 5) {
      local_374 = (byte)local_2c[0x72] - 1;
      uVar2 = (ushort)local_368[(local_1c & 0xffff) * 0x35 + ((local_370 & 0xffff) - 1) * 10 +
                                local_374 * 5 + (local_20 & 0xffff)];
      local_36c = CONCAT22(local_36c._2_2_,uVar2);
      if (uVar2 != 0) {
        FUN__text__004d2790(&DAT_0061bfe0,1,0x4a,(local_20 & 0xffff) * 0x19 + 0x29a,
                            (local_1c & 0xffff) * 0x23 + 0x1e6,(uVar2 - 1) * 0x16,0);
        FUN__text__004d5ec0(local_18,(local_20 & 0xffff) * 0x18 + 0x29c,
                            (local_1c & 0xffff) * 0x23 + 0x1e8,0x12,0x12);
        if ((local_c & 0xffff) != 0) {
          FUN__text__004b8930(0x2c8,0x1cc,(local_36c & 0xffff) - 1,0x4a);
        }
      }
      local_20 = CONCAT22(local_20._2_2_,(short)local_20 + 1);
    }
    local_1c = CONCAT22(local_1c._2_2_,(short)local_1c + 1);
  }
  FUN__text__004d5ec0(local_18,0x3e1,0x209,0x14,0x2a);
  if ((local_14 & 1) != 0) {
    FUN__text__004d68b0(&DAT_0061c030,0x4c,0x3df,0x207,8);
    FUN__text__004d6230(0);
    FUN__text__004db2b0(5);
  }
  FUN__text__004d5ec0(local_18,0x3e1,0x238,0x14,0x2a);
  if ((local_14 & 1) != 0) {
    FUN__text__004d68b0(&DAT_0061c040,0x4c,0x3df,0x236,8);
    FUN__text__004d6230(1);
    FUN__text__004db2b0(5);
  }
  if (-1 < DAT_007d6f64) {
    if (*(short *)(local_8 + 0x391da) != DAT_007d6f64) {
      FUN__text__004d64d0(DAT_007d6f64,6);
    }
    FUN__text__004d2950(&DAT_0061bc40,3,0x36,0xdf,DAT_007d6f64 * 0x22 + 0x1e1,0x90);
    FUN__text__004d2790(&DAT_0061c050,1,0x4b,0x32c,0x1c7,0,DAT_007d6f64 * 0x14);
    FUN__text__004d2790(&DAT_0061c060,1,0x4b,0x3b0,0x1ca,0,(int)DAT_007d6f64 << 4);
    FUN__text__004d2790(&DAT_0061c070,1,0x4b,0x3a4,0x1eb,0,(int)DAT_007d6f64 << 4);
    FUN__text__004d62f0(0x325,0x20d,0x3d);
  }
  local_378 = (uint)local_378._2_2_ << 0x10;
  DAT_007d722c = 0;
  DAT_007d7250 = 0;
  local_37c = (uint)local_37c._2_2_ << 0x10;
  local_1c = local_1c & 0xffff0000;
  while( true ) {
    if (6 < (local_1c & 0xffff)) break;
    uVar1 = local_37c >> 0x10;
    local_37c = local_37c & 0xffff0000;
    *(short *)(&DAT_007d721a + (local_1c & 0xffff) * 2) =
         *(short *)(&DAT_007d71ea + (local_1c & 0xffff) * 2) +
         *(short *)(&DAT_007d71fa + (local_1c & 0xffff) * 2);
    local_378 = CONCAT22(local_378._2_2_,
                         (short)local_378 + *(short *)(&DAT_007d721a + (local_1c & 0xffff) * 2));
    if (*(short *)(&DAT_007d71fa + (local_1c & 0xffff) * 2) != 0) {
      local_37c = CONCAT22((short)uVar1,1);
      local_30 = CONCAT22(local_30._2_2_,1);
    }
    FUN__text__004b7590(0x16c,(local_1c & 0xffff) * 0x22 + 0x1ea,0,(local_37c & 0xffff) * 0x98,3,
                        0x4a,0x3e,*(undefined2 *)(&DAT_007d721a + (local_1c & 0xffff) * 2),10,1,4,7,
                        0);
    FUN__text__004b7590(0x22b,(local_1c & 0xffff) * 0x22 + 0x1eb,0,(local_37c & 0xffff) * 0x98,3,
                        0x4a,0x3f,*(undefined2 *)(&DAT_007d71fa + (local_1c & 0xffff) * 2),8,1,4,7,
                        local_37c & 0xff);
    local_380 = CONCAT22(local_380._2_2_,1);
    local_20 = local_20 & 0xffff0000;
    while ((local_20 & 0xffff) < (uint)DAT_007d6f68) {
      if (((int)DAT_007d6a34 != (local_20 & 0xffff)) &&
         (*(ushort *)(&DAT_007d721a + (local_1c & 0xffff) * 2) <
          *(ushort *)(&DAT_007d6f6a + (local_1c & 0xffff) * 2 + (local_20 & 0xffff) * 0x10))) {
        local_380 = CONCAT22(local_380._2_2_,(short)local_380 + 1);
      }
      local_20 = CONCAT22(local_20._2_2_,(short)local_20 + 1);
    }
    sVar3 = FUN__text__004b28b0(*(undefined2 *)(&DAT_007d720a + (local_1c & 0xffff) * 2),
                                local_380 & 0xffff);
    local_384 = CONCAT22(local_384._2_2_,sVar3);
    if (sVar3 == 0x98) {
      local_384 = CONCAT22(local_384._2_2_,0x130);
    }
    else if (sVar3 == 0x130) {
      local_384 = CONCAT22(local_384._2_2_,0x98);
    }
    FUN__text__004b7590(0x19b,(local_1c & 0xffff) * 0x22 + 0x1eb,0,local_384 & 0xffff,2,0x4a,0x3f,
                        local_380 & 0xffff,8,1,4,7,0);
    if ((uint)(byte)local_2c[(local_1c & 0xffff) * 8 + 0xc] +
        (uint)*(ushort *)(&DAT_007d71fa + (local_1c & 0xffff) * 2) == (local_44 & 0xffff)) {
      FUN__text__004d2620(0x1a9,(local_1c & 0xffff) * 0x22 + 0x1e5,0x1f,0x19,0x37,0x70010101,1);
      FUN__text__004d2620(0x237,(local_1c & 0xffff) * 0x22 + 0x1e5,0x53,0x19,0x37,0x70010101,1);
    }
    else {
      if (*(short *)(&DAT_007d7254 + (local_1c & 0xffff) * 2) == 2) {
        FUN__text__004d2620(0x1a9,(local_1c & 0xffff) * 0x22 + 0x1e5,0x1f,0x19,0x37,0x70010101,1);
      }
      local_388 = (byte)local_2c[(local_1c & 0xffff) * 8 + 0xc] + 1 +
                  *(short *)(&DAT_007d71fa + (local_1c & 0xffff) * 2);
      FUN__text__004d56a0(local_3a8,local_388,0);
      local_3ac = *(int *)(&DAT_007d7230 + (local_1c & 0xffff) * 4) +
                  *(int *)(local_2c + (local_1c & 0xffff) * 8 + 0x10);
      local_3b0 = local_3a8[0] - local_3ac;
      FUN__text__004b7590(0x285,(local_1c & 0xffff) * 0x22 + 0x1eb,0,
                          (uint)*(ushort *)(&DAT_007d7254 + (local_1c & 0xffff) * 2) * 0x98,7,0x4a,
                          0x3f,local_3b0,8,1,4,7,0);
    }
    DAT_007d722c = DAT_007d722c + (uint)*(ushort *)(&DAT_007d71fa + (local_1c & 0xffff) * 2);
    DAT_007d7250 = DAT_007d7250 + *(int *)(&DAT_007d7230 + (local_1c & 0xffff) * 4);
    local_1c = CONCAT22(local_1c._2_2_,(short)local_1c + 1);
  }
  if ((local_3c & 0xffff) == 0) {
    FUN__text__004d58e0(local_4a8,*(undefined2 *)(local_8 + 0x596 + DAT_007d6a34 * 2));
    local_4ac = local_4a0 + DAT_007d7250;
    DAT_007d72b4 = FUN__text__004d5590(local_4ac);
    _local_4b0 = CONCAT31(uStack_4af,DAT_007d72b4);
    *(char *)(local_8 + 0xae2) = DAT_007d72b4;
    FUN__text__0042b2d0(&DAT_005a0a7c,DAT_007d72b4,DAT_007d72b4,local_4ac,local_4a0,DAT_007d7250);
    (&DAT_007d7270)[(local_1c & 0xffff) * 8] =
         (char)*(undefined2 *)(&DAT_007d71ea + (local_1c & 0xffff) * 2) +
         (char)*(undefined2 *)(&DAT_007d71fa + (local_1c & 0xffff) * 2);
    FUN__text__004b66f0(&DAT_007d7264,0xffffffff,0,0);
    local_3c = CONCAT22(local_3c._2_2_,1);
  }
  local_4b4 = CONCAT22(local_4b4._2_2_,0x2dc);
  local_4b8 = CONCAT22(local_4b8._2_2_,1);
  local_20 = local_20 & 0xffff0000;
  while ((local_20 & 0xffff) < (uint)DAT_007d6f68) {
    if (((int)DAT_007d6a34 != (local_20 & 0xffff)) &&
       ((local_378 & 0xffff) < (uint)*(ushort *)(&DAT_007d6f78 + (local_20 & 0xffff) * 0x10))) {
      local_4b8 = CONCAT22(local_4b8._2_2_,(short)local_4b8 + 1);
    }
    local_20 = CONCAT22(local_20._2_2_,(short)local_20 + 1);
  }
  FUN__text__004b7590(0x16c,0x2dc,0,(local_30 & 0xffff) * 0x98,3,0x4a,0x3e,local_378 & 0xffff,10,1,4
                      ,7,0);
  sVar3 = FUN__text__004b28b0(DAT_007d7218,local_4b8 & 0xffff);
  local_4bc = CONCAT22(local_4bc._2_2_,sVar3);
  if (sVar3 == 0x98) {
    local_4bc = CONCAT22(local_4bc._2_2_,0x130);
  }
  else if (sVar3 == 0x130) {
    local_4bc = CONCAT22(local_4bc._2_2_,0x98);
  }
  FUN__text__004b7590(0x19b,(local_4b4 & 0xffff) + 3,0,local_4bc & 0xffff,2,0x4a,0x3f,
                      local_4b8 & 0xffff,8,1,4,7,0);
  if (DAT_007d722c == 0) {
    FUN__text__004b7590(0x22b,(local_4b4 & 0xffff) + 3,0,0,3,0x4a,0x3f,0,8,1,4,7,0);
  }
  else {
    FUN__text__004b7590(0x22b,(local_4b4 & 0xffff) + 3,0,0x98,3,0x4a,0x3f,DAT_007d722c,8,1,4,7,1);
  }
  local_4c0 = DAT_007a511c - DAT_007d7250;
  FUN__text__004b7590(0x3f4,0x273,0,0,9,0x4a,0x3f,DAT_007a511c,8,1,4,7,0);
  FUN__text__004b7590(0x3f4,0x295,0,0,9,0x4a,0x3f,DAT_007d7250,8,1,4,7,0);
  FUN__text__004b7590(0x3f4,0x2b7,0,0,9,0x4a,0x3f,local_4c0,8,1,4,7,0);
  local_4c4 = 0;
  if ((local_34 & 0xffff) == 0) {
    FUN__text__004d2620(0x32b,0x2d6,0x5d,0x1e,0x37,0x70010101,1);
  }
  else {
    FUN__text__004d5ec0(local_18,0x32c,0x2d7,0x5a,0x1c);
    if ((local_14 & 1) != 0) {
      FUN__text__004db2b0(5);
      FUN__text__004d48a0(CONCAT22(extraout_var,*(undefined2 *)(local_8 + 0x596 + DAT_007d6a34 * 2))
                          ,7,0xffffffff,0);
      if (*(byte *)(local_8 + 0xb92) < *(byte *)(local_8 + 0xae2)) {
        FUN__text__00409ff0(local_8 + 0x3a24c,0,1,0);
        FUN__text__004db2b0(0xb);
      }
      FUN__text__004d68b0(&DAT_0061bff0,0x4c,800,0x2d4,8);
      iVar5 = *(short *)(local_8 + 0x596 + DAT_007d6a34 * 2) * 0x4a0;
      local_2c = &DAT_007e17e8 + iVar5;
      local_1c = local_1c & 0xffff0000;
      while ((local_1c & 0xffff) < 7) {
        (&DAT_007e17f4)[(local_1c & 0xffff) * 8 + iVar5] =
             (&DAT_007e17f4)[(local_1c & 0xffff) * 8 + iVar5] +
             (&DAT_007d71fa)[(local_1c & 0xffff) * 2];
        *(int *)(&DAT_007e17f8 + (local_1c & 0xffff) * 8 + iVar5) =
             *(int *)(&DAT_007e17f8 + (local_1c & 0xffff) * 8 + iVar5) +
             *(int *)(&DAT_007d7230 + (local_1c & 0xffff) * 4);
        local_4c4 = local_4c4 + *(int *)(&DAT_007e17f8 + (local_1c & 0xffff) * 8 + iVar5);
        local_1c = CONCAT22(local_1c._2_2_,(short)local_1c + 1);
      }
      FUN__text__004d58e0(local_5bc,*(undefined2 *)(local_8 + 0x596 + DAT_007d6a34 * 2));
      local_2c[0x50] = local_5ac;
      DAT_007d6f64 = -1;
      local_1c = local_1c & 0xffff0000;
      while ((local_1c & 0xffff) < 8) {
        *(undefined2 *)(&DAT_007d71fa + (local_1c & 0xffff) * 2) = 0;
        *(undefined4 *)(&DAT_007d7230 + (local_1c & 0xffff) * 4) = 0;
        *(undefined2 *)(&DAT_007d7254 + (local_1c & 0xffff) * 2) = 0;
        local_1c = CONCAT22(local_1c._2_2_,(short)local_1c + 1);
      }
      DAT_007a511c = DAT_007a511c - DAT_007d7250;
      *(int *)(&DAT_007cf468 + *(short *)(local_8 + 0x596 + DAT_007d6a34 * 2) * 0x124) =
           *(int *)(&DAT_007cf468 + *(short *)(local_8 + 0x596 + DAT_007d6a34 * 2) * 0x124) +
           DAT_007d7250;
      FUN__text__004b66f0(local_2c,0xffffffff,1,2);
      FUN__text__004b66f0(&DAT_007d7264,0xffffffff,0,0);
      FUN__text__004d58e0(local_6b4,
                          CONCAT22(extraout_var_02,
                                   *(undefined2 *)(local_8 + 0x596 + DAT_007d6a34 * 2)));
      local_6b8 = local_6ac;
      DAT_007d72b4 = FUN__text__004d5590(local_6ac);
      DAT_007d6f66 = 1;
      local_6bc = DAT_007d72b4;
    }
  }
  local_6c0 = (uint)local_6c0._2_2_ << 0x10;
  local_6c4 = 0;
  iVar5 = FUN__text__004128f0(0xcb,1);
  if (iVar5 != 0) {
    local_6c4 = FUN__text__004b6fb0(0,DAT_007d6a34);
    local_6c0 = CONCAT22(local_6c0._2_2_,1);
    FUN__text__004db2b0(5);
  }
  iVar5 = FUN__text__004128f0(0xcd,1);
  if (iVar5 != 0) {
    local_6c4 = FUN__text__004b6fb0(1,CONCAT22(extraout_var_01,DAT_007d6a34));
    local_6c0 = CONCAT22(local_6c0._2_2_,1);
    FUN__text__004db2b0(5);
  }
  if ((local_6c0 & 0xffff) != 0) {
    DAT_007d6f64 = -1;
    local_1c = local_1c & 0xffff0000;
    while ((local_1c & 0xffff) < 10) {
      *(undefined2 *)(&DAT_007d71fa + (local_1c & 0xffff) * 2) = 0;
      *(undefined4 *)(&DAT_007d7230 + (local_1c & 0xffff) * 4) = 0;
      *(undefined2 *)(&DAT_007d7254 + (local_1c & 0xffff) * 2) = 0;
      local_1c = CONCAT22(local_1c._2_2_,(short)local_1c + 1);
    }
    DAT_007d6a34 = local_6c4;
    FUN__text__004b6690(*(undefined2 *)(local_8 + 0x596 + local_6c4 * 2),0xffffffff,1,2);
    FUN__text__004b6690(CONCAT22(extraout_var_03,*(undefined2 *)(local_8 + 0x596 + DAT_007d6a34 * 2)
                                ),0xffffffff,0,0);
    puVar6 = (undefined4 *)(&DAT_007e17e8 + *(short *)(local_8 + 0x596 + DAT_007d6a34 * 2) * 0x4a0);
    puVar8 = &DAT_007d7264;
    for (iVar5 = 0x128; iVar5 != 0; iVar5 = iVar5 + -1) {
      *puVar8 = *puVar6;
      puVar6 = puVar6 + 1;
      puVar8 = puVar8 + 1;
    }
    DAT_007d6f66 = 1;
  }
  FUN__text__004ae340(*(undefined2 *)(local_8 + 0x596 + DAT_007d6a34 * 2));
  local_8 = 0x4ae2eb;
  FUN__text__0056ce80();
  return;
}

