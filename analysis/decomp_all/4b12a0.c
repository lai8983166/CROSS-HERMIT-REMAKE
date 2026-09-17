
void __fastcall FUN__text__004b12a0(int param_1)

{
  uint uVar1;
  short sVar2;
  undefined2 extraout_var;
  undefined2 extraout_var_00;
  ushort uVar3;
  int iVar4;
  undefined2 extraout_var_01;
  undefined2 extraout_var_02;
  undefined2 uVar5;
  undefined2 extraout_var_03;
  short sVar6;
  undefined2 extraout_var_04;
  undefined2 extraout_var_05;
  undefined4 *puVar7;
  undefined4 local_110 [16];
  uint local_d0;
  char local_cc;
  short local_c8;
  uint local_c4;
  undefined4 local_c0;
  uint local_bc;
  uint local_b8;
  uint local_b4;
  undefined4 local_b0;
  undefined4 local_ac;
  short local_a8 [36];
  short local_60;
  ushort local_5c [16];
  uint local_3c;
  uint local_38;
  undefined1 local_34;
  short local_30;
  undefined2 uStack_2e;
  short local_2c;
  undefined2 uStack_2a;
  uint local_28;
  uint local_24;
  undefined *local_20;
  uint local_1c;
  uint local_18;
  uint local_10;
  undefined2 local_c;
  int local_8;
  
  puVar7 = local_110;
  for (iVar4 = 0x43; iVar4 != 0; iVar4 = iVar4 + -1) {
    *puVar7 = 0xcccccccc;
    puVar7 = puVar7 + 1;
  }
  local_8 = param_1;
  local_c = 0;
  local_34 = 0;
  *(undefined1 *)(param_1 + 0xc88) = 1;
  local_38 = local_38 & 0xffff0000;
  local_3c = local_3c & 0xffff0000;
  local_5c[0] = 0xb;
  local_5c[1] = 0xd;
  local_5c[2] = 0xf;
  local_5c[3] = 0x11;
  local_5c[4] = 0x13;
  local_5c[5] = 1;
  local_5c[6] = 3;
  local_5c[7] = 5;
  local_5c[8] = 7;
  local_5c[9] = 9;
  local_5c[10] = 0x15;
  local_5c[0xb] = 0x17;
  local_5c[0xc] = 0x19;
  local_5c[0xd] = 0x1b;
  local_5c[0xe] = 0x1d;
  local_28 = local_28 & 0xffff0000;
  while ((local_28 & 0xffff) < 3) {
    local_24 = local_24 & 0xffff0000;
    while ((local_24 & 0xffff) < 5) {
      sVar6 = (short)local_24 * 0x5a + 0xe2;
      _local_2c = CONCAT22(uStack_2a,sVar6);
      sVar2 = (short)local_28 * 0x5a + 0x1ef;
      _local_30 = CONCAT22(uStack_2e,sVar2);
      uVar3 = (short)local_28 * 5 + (short)local_24;
      local_38 = CONCAT22(local_38._2_2_,uVar3);
      uVar1 = (local_5c[uVar3] - 1) + (uint)*(byte *)(local_8 + 0x69);
      local_3c = CONCAT22(local_3c._2_2_,(short)uVar1);
      local_60 = *(short *)(local_8 + 0x596 + DAT_007d6a34 * 2);
      local_a8[0x22] = (short)(char)(&DAT_007cf444)[(uVar1 & 0xffff) + local_60 * 0x124];
      if (local_a8[0x22] == 0) {
        local_20 = &DAT_0061bd50;
        FUN__text__004d2ca0(0xd,0x42,DAT_0061bd52,sVar6,sVar2,DAT_0061bd54,DAT_0061bd56,DAT_0061bd58
                            ,DAT_0061bd5a);
      }
      else {
        FUN__text__004d5ec0(&local_1c,CONCAT22((short)(uVar1 >> 0x10),sVar6),sVar2,0x50,0x50);
        if (((local_10 & 0xffff) != 0) && ((local_18 & 1) != 0)) {
          FUN__text__004db2b0(5);
          *(short *)(local_8 + 0x62e) = (short)local_24;
          *(short *)(local_8 + 0x630) = (short)local_28;
          *(undefined2 *)(local_8 + 0x632) = (undefined2)local_3c;
          FUN__text__004b6690(*(undefined2 *)(local_8 + 0x596 + DAT_007d6a34 * 2),
                              *(undefined2 *)(local_8 + 0x632),0,2);
        }
        local_20 = &DAT_0061bf10;
        FUN__text__004d2ca0(0xd,0x42,DAT_0061bf12,(local_24 & 0xffff) * 0x5a + 0xdd,
                            (local_28 & 0xffff) * 0x5a + 0x22b,DAT_0061bf14 + 1,
                            (uint)DAT_0061bf16 + ((local_3c & 0xffff) - 1) * 0x18,DAT_0061bf18 - 1,
                            DAT_0061bf1a);
        FUN__text__004b8460((local_24 & 0xffff) * 0x5a + 0xf4,(local_28 & 0xffff) * 0x5a + 0x1e8,
                            CONCAT22(extraout_var_04,(undefined2)local_3c),0x43);
        FUN__text__004b71b0(0x22,(int)*(char *)(local_8 + 0x41 + (local_3c & 0xffff)),0,
                            (local_24 & 0xffff) * 0x5a + 0xe1,(local_28 & 0xffff) * 0x5a + 0x1ef,
                            0x3b);
        if ((int)*(short *)(local_8 + 0x30) == (local_3c & 0xffff)) {
          if (*(char *)(local_8 + 0x62c) == '\0') {
            *(undefined1 *)(local_8 + 0x62c) = 1;
            *(short *)(local_8 + 0x62e) = (short)local_24;
            *(short *)(local_8 + 0x630) = (short)local_28;
            *(undefined2 *)(local_8 + 0x632) = (undefined2)local_3c;
            FUN__text__004b6690(*(undefined2 *)(local_8 + 0x596 + DAT_007d6a34 * 2),
                                *(undefined2 *)(local_8 + 0x632),1,2);
          }
          FUN__text__004d2620((local_24 & 0xffff) * 0x5a + 0xe2,(local_28 & 0xffff) * 0x5a + 0x1ef,
                              0x50,0x50,0x41,0x70010101,1);
        }
      }
      local_24 = CONCAT22(local_24._2_2_,(short)local_24 + 1);
    }
    local_28 = CONCAT22(local_28._2_2_,(short)local_28 + 1);
  }
  local_20 = &DAT_0061bc20;
  FUN__text__004d2ca0(0xd,0x3e,DAT_0061bc22,(uint)*(ushort *)(local_8 + 0x62e) * 0x5a + 0xdd,
                      (uint)*(ushort *)(local_8 + 0x630) * 0x5a + 0x1ea,DAT_0061bc24,DAT_0061bc26,
                      DAT_0061bc28,DAT_0061bc2a);
  FUN__text__004b8700(0x2aa,0x1c2,CONCAT22(extraout_var,*(undefined2 *)(local_8 + 0xc84)),0x42);
  local_a8[0] = 0x31a;
  local_a8[1] = 0x1e6;
  local_a8[2] = 0x31a;
  local_a8[3] = 0x1f9;
  local_a8[4] = 0x31a;
  local_a8[5] = 0x235;
  local_a8[6] = 0x31a;
  local_a8[7] = 0x248;
  local_a8[8] = 0x31a;
  local_a8[9] = 0x271;
  local_a8[10] = 0x31a;
  local_a8[0xb] = 0x284;
  local_a8[0xc] = 0x31a;
  local_a8[0xd] = 0x297;
  local_a8[0xe] = 0x3c6;
  local_a8[0xf] = 0x1e6;
  local_a8[0x10] = 0x3c6;
  local_a8[0x11] = 0x1f9;
  local_a8[0x12] = 0x3c6;
  local_a8[0x13] = 0x20c;
  local_a8[0x14] = 0x3c6;
  local_a8[0x15] = 0x21f;
  local_a8[0x16] = 0x3c6;
  local_a8[0x17] = 0x235;
  local_a8[0x18] = 0x3c6;
  local_a8[0x19] = 0x248;
  local_a8[0x1a] = 0x3c6;
  local_a8[0x1b] = 0x25b;
  local_a8[0x1c] = 0x3c6;
  local_a8[0x1d] = 0x284;
  local_a8[0x1e] = 0x3c6;
  local_a8[0x1f] = 0x297;
  local_a8[0x20] = 0xffff;
  local_a8[0x21] = 0xffff;
  local_ac = (uint)local_ac._2_2_ << 0x10;
  while( true ) {
    if (local_a8[(local_ac & 0xffff) * 2] == -1) break;
    local_cc = (&DAT_00738cef)[(local_ac & 0xffff) + (uint)*(ushort *)(local_8 + 0xc84) * 0x32];
    if (local_cc == '\x01') {
      local_20 = &DAT_0061bf60;
      local_b0 = CONCAT22(local_b0._2_2_,1);
    }
    else if (local_cc == '\x02') {
      local_20 = &DAT_0061bf70;
      local_b0 = CONCAT22(local_b0._2_2_,1);
    }
    else if (local_cc == '\x03') {
      local_20 = &DAT_0061bf80;
      local_b0 = CONCAT22(local_b0._2_2_,1);
    }
    else {
      local_b0 = (uint)local_b0._2_2_ << 0x10;
    }
    if ((local_b0 & 0xffff) != 0) {
      FUN__text__004d2ca0(0xd,0x49,*(undefined2 *)(local_20 + 2),
                          (int)local_a8[(local_ac & 0xffff) * 2],
                          (int)local_a8[(local_ac & 0xffff) * 2 + 1],*(undefined2 *)(local_20 + 4),
                          *(undefined2 *)(local_20 + 6),*(undefined2 *)(local_20 + 8),
                          *(undefined2 *)(local_20 + 10));
    }
    local_ac = CONCAT22(local_ac._2_2_,(short)local_ac + 1);
  }
  if ((uint)*(ushort *)(local_8 + 0x632) == (int)*(short *)(local_8 + 0x30)) {
    FUN__text__004d2620(0x35a,0x1bf,0x9e,0x23,0x47,0x70010101,1);
  }
  else {
    local_b4 = CONCAT22(local_b4._2_2_,1);
    local_20 = &DAT_0061bd10;
    FUN__text__004d5ec0(&local_1c,0x360,0x1c3,0x8a,0x1c);
    uVar5 = extraout_var_01;
    if (((local_10 & 0xffff) != 0) && (uVar5 = 0, (local_1c & 1) != 0)) {
      FUN__text__004db2b0(0xb);
      FUN__text__004d48a0(CONCAT22(extraout_var_02,
                                   *(undefined2 *)(local_8 + 0x596 + DAT_007d6a34 * 2)),5,5,0);
      FUN__text__00409ff0(local_8 + 0x3a1f4,0,3,0);
      local_b4 = local_b4 & 0xffff0000;
      *(undefined2 *)(&DAT_007e17ee + *(short *)(local_8 + 0x596 + DAT_007d6a34 * 2) * 0x4a0) =
           *(undefined2 *)(local_8 + 0x632);
      FUN__text__004b6690(*(undefined2 *)(local_8 + 0x596 + DAT_007d6a34 * 2),
                          *(undefined2 *)(local_8 + 0x632),1,1);
      FUN__text__004b6690(CONCAT22(extraout_var_05,
                                   *(undefined2 *)(local_8 + 0x596 + DAT_007d6a34 * 2)),
                          CONCAT22(extraout_var_05,*(undefined2 *)(local_8 + 0x632)),1,2);
      *(undefined *)(local_8 + 0x570) = (&DAT_006b2d8c)[(uint)*(ushort *)(local_8 + 0x632) * 0x40];
      uVar5 = (undefined2)((uint)local_8 >> 0x10);
      *(undefined *)(local_8 + 0x582) = (&DAT_006b2d8b)[(uint)*(ushort *)(local_8 + 0x632) * 0x40];
    }
    if ((local_b4 & 0xffff) == 0) {
      FUN__text__004d67f0(0xd,0x48,*(undefined2 *)(local_20 + 2),*(undefined2 *)(local_20 + 0xc),
                          *(undefined2 *)(local_20 + 0xe),*(undefined2 *)(local_20 + 4),
                          *(undefined2 *)(local_20 + 6),*(undefined2 *)(local_20 + 8),
                          CONCAT22(uVar5,*(undefined2 *)(local_20 + 10)),8);
    }
  }
  FUN__text__004d2700(&DAT_0061bb20,0,0x4e,0xd7,0x1a7);
  local_b8 = CONCAT22(local_b8._2_2_,
                      (ushort)(byte)(&DAT_006b2d8b)[(uint)*(ushort *)(local_8 + 0x632) * 0x40]);
  local_bc = CONCAT22(local_bc._2_2_,
                      (ushort)(byte)(&DAT_006b2d8c)[(uint)*(ushort *)(local_8 + 0x632) * 0x40]);
  FUN__text__004b70a0(0x20,(ushort)(byte)(&DAT_006b2d8b)[(uint)*(ushort *)(local_8 + 0x632) * 0x40],
                      1);
  FUN__text__004b70a0(0x21,local_bc & 0xffff,1);
  FUN__text__004d2620(0x33d,0x2c,0xad,0x168,0x37,0x70010101,1);
  FUN__text__004d2620(0x16f,0x1bf,0x120,0x24,0x37,0x70010101,1);
  if ((int)*(short *)(local_8 + 0x391d8) != (uint)*(ushort *)(local_8 + 0x632)) {
    FUN__text__004d64d0(*(undefined2 *)(local_8 + 0x632),4);
  }
  FUN__text__004d62f0(0x2b2,0x2b6,0x3d);
  *(undefined2 *)(local_8 + 0x391d8) = *(undefined2 *)(local_8 + 0x632);
  local_c0 = (uint)local_c0._2_2_ << 0x10;
  while ((local_c0 & 0xffff) < 8) {
    if ((local_c0 & 0xffff) < (local_b8 & 0xffff)) {
      FUN__text__004d2620((local_c0 & 0xffff) * 0x24 + 0x16f,0x1bf,0x22,0x22,0x36,0x700000a0,1);
    }
    else {
      FUN__text__004d2620((local_c0 & 0xffff) * 0x24 + 0x16f,0x1bf,0x22,0x22,0x36,0x7000a000,1);
    }
    local_c0 = CONCAT22(local_c0._2_2_,(short)local_c0 + 1);
  }
  local_d0 = FUN__text__004b6c60();
  local_d0 = local_d0 & 0xffff;
  if (local_d0 == 1) {
    FUN__text__004d6230(0);
  }
  else if (local_d0 == 2) {
    FUN__text__004d6230(1);
  }
  local_c4 = local_c4 & 0xffffff00;
  iVar4 = FUN__text__004128f0(0xcb,1);
  if (iVar4 != 0) {
    local_c8 = FUN__text__004b6fb0(0,DAT_007d6a34);
    local_c4 = CONCAT31(local_c4._1_3_,1);
    FUN__text__004db2b0(5);
  }
  iVar4 = FUN__text__004128f0(0xcd,1);
  uVar5 = 0;
  if (iVar4 != 0) {
    local_c8 = FUN__text__004b6fb0(1,CONCAT22(extraout_var_03,DAT_007d6a34));
    local_c4 = CONCAT31(local_c4._1_3_,1);
    FUN__text__004db2b0(5);
    uVar5 = extraout_var_00;
  }
  if ((local_c4 & 0xff) != 0) {
    DAT_007d6a34 = local_c8;
    FUN__text__004b6690(CONCAT22(uVar5,*(undefined2 *)(local_8 + 0x596 + local_c8 * 2)),0xffffffff,1
                        ,2);
    *(undefined1 *)(local_8 + 0x62c) = 0;
  }
  local_8 = 0x4b1f25;
  FUN__text__0056ce80();
  return;
}

