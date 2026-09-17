
void __fastcall FUN__text__004b28f0(int param_1)

{
  short sVar1;
  byte bVar2;
  undefined4 uVar3;
  undefined2 extraout_var;
  int iVar4;
  undefined2 extraout_var_00;
  undefined2 extraout_var_01;
  undefined2 extraout_var_02;
  undefined2 extraout_var_03;
  undefined2 extraout_var_04;
  undefined2 extraout_var_05;
  undefined2 extraout_var_06;
  undefined2 extraout_var_07;
  uint uVar5;
  undefined2 extraout_var_08;
  undefined4 *puVar6;
  undefined4 uVar7;
  undefined4 uVar8;
  undefined4 local_238 [16];
  uint local_1f8;
  uint local_1f4;
  undefined2 local_1f0;
  short local_1ec;
  short local_1e8;
  undefined1 local_1e4 [4];
  uint local_1e0;
  uint local_1d8;
  short local_1d4;
  short local_1d0;
  short local_1cc;
  short local_1c8;
  uint local_1c4;
  undefined1 local_1c0 [12];
  uint local_1b4;
  short local_1b0 [38];
  ushort local_164 [24];
  undefined4 local_134;
  undefined4 local_130;
  undefined4 local_12c;
  short local_128;
  short local_124;
  byte local_120 [8];
  uint local_118;
  short local_114;
  undefined2 local_110;
  undefined1 local_10c [52];
  short asStack_d8 [98];
  uint local_14;
  short local_10;
  undefined2 uStack_e;
  uint local_c;
  int local_8;
  
  puVar6 = local_238;
  for (iVar4 = 0x8d; iVar4 != 0; iVar4 = iVar4 + -1) {
    *puVar6 = 0xcccccccc;
    puVar6 = puVar6 + 1;
  }
  local_c = local_c & 0xffff0000;
  sVar1 = *(short *)(param_1 + 0x596 + DAT_007d6a34 * 2);
  _local_10 = CONCAT22(uStack_e,sVar1);
  local_14 = CONCAT22(local_14._2_2_,sVar1 + 0xb);
  local_8 = param_1;
  FUN__text__004d2700(&DAT_0061baf0,0,0x4e,0x118,0x1f);
  FUN__text__004d2ba0(0xd,0x4e,local_14 & 0xffff,0,0x1f);
  uVar8 = 0;
  uVar7 = 0;
  uVar3 = FUN__text__004b28b0((int)*(short *)(local_8 + 0xb98),(int)*(short *)(local_8 + 0xae8),0,0)
  ;
  FUN__text__004b7e20(0,0,999,(int)*(short *)(local_8 + 0xae8),0x3b,0,uVar3,uVar7,uVar8);
  uVar8 = 0;
  uVar7 = 0;
  uVar3 = FUN__text__004b28b0((int)*(short *)(local_8 + 0xb9e),(int)*(short *)(local_8 + 0xaee),0,0)
  ;
  FUN__text__004b7e20(1,1,999,(int)*(short *)(local_8 + 0xaee),0x3b,0,uVar3,uVar7,uVar8);
  uVar8 = 0;
  uVar7 = 0;
  uVar3 = FUN__text__004b28b0(*(int *)(local_8 + 0xba4) / 0xe10,*(int *)(local_8 + 0xaf4) / 0xe10,0,
                              0);
  FUN__text__004b7e20(2,2,99,*(int *)(local_8 + 0xaf4) / 0xe10,0x3b,0,uVar3,uVar7,uVar8);
  uVar8 = 0;
  uVar7 = 0;
  uVar3 = FUN__text__004b28b0(*(undefined1 *)(local_8 + 0xbb0),*(undefined1 *)(local_8 + 0xb00),0,0)
  ;
  FUN__text__004b7e20(4,0xffffffff,0x20,*(undefined1 *)(local_8 + 0xb00),0x3b,0,uVar3,uVar7,uVar8);
  uVar8 = 0;
  uVar7 = 0;
  uVar3 = FUN__text__004b28b0(*(undefined1 *)(local_8 + 0xbbb),*(undefined1 *)(local_8 + 0xb0b),0,0)
  ;
  FUN__text__004b7e20(7,0xffffffff,0x7f,*(undefined1 *)(local_8 + 0xb0b),0x3b,0,uVar3,uVar7,uVar8);
  uVar8 = 0;
  uVar7 = 0;
  uVar3 = FUN__text__004b28b0(*(undefined1 *)(local_8 + 0xbc8),*(undefined1 *)(local_8 + 0xb18),0,0)
  ;
  FUN__text__004b7e20(8,0xffffffff,99,*(undefined1 *)(local_8 + 0xb18),0x3b,0,uVar3,uVar7,uVar8);
  uVar8 = 0;
  uVar7 = 0;
  uVar3 = FUN__text__004b28b0(*(undefined2 *)(local_8 + 0xb08),*(undefined2 *)(local_8 + 3000),0,0);
  FUN__text__004b7e20(9,0xffffffff,999,*(undefined2 *)(local_8 + 0xb08),0x3b,0,uVar3,uVar7,uVar8);
  uVar8 = 0;
  uVar7 = 0;
  uVar3 = FUN__text__004b28b0(*(undefined1 *)(local_8 + 0xbd0),*(undefined1 *)(local_8 + 0xb20),0,0)
  ;
  FUN__text__004b7e20(10,6,0xff,*(undefined1 *)(local_8 + 0xb20),0x3b,0,uVar3,uVar7,uVar8);
  uVar8 = 0;
  uVar7 = 0;
  uVar3 = FUN__text__004b28b0(*(undefined1 *)(local_8 + 0xbd1),*(undefined1 *)(local_8 + 0xb21),0,0)
  ;
  FUN__text__004b7e20(0xb,7,0xff,*(undefined1 *)(local_8 + 0xb21),0x3b,0,uVar3,uVar7,uVar8);
  uVar8 = 0;
  uVar7 = 0;
  uVar3 = FUN__text__004b28b0(*(undefined1 *)(local_8 + 0xbd3),*(undefined1 *)(local_8 + 0xb23),0,0)
  ;
  FUN__text__004b7e20(0xc,8,0xff,*(undefined1 *)(local_8 + 0xb23),0x3b,0,uVar3,uVar7,uVar8);
  uVar8 = 0;
  uVar7 = 0;
  uVar3 = FUN__text__004b28b0(*(undefined1 *)(local_8 + 0xbd2),*(undefined1 *)(local_8 + 0xb22),0,0)
  ;
  FUN__text__004b7e20(0xd,0xffffffff,99,*(undefined1 *)(local_8 + 0xb22),0x3b,0,uVar3,uVar7,uVar8);
  uVar8 = 0;
  uVar7 = 0;
  uVar3 = FUN__text__004b28b0(*(undefined1 *)(local_8 + 0xbd4),*(undefined1 *)(local_8 + 0xb24),0,0)
  ;
  FUN__text__004b7e20(0xe,0xffffffff,99,*(undefined1 *)(local_8 + 0xb24),0x3b,0,uVar3,uVar7,uVar8);
  uVar8 = 0;
  uVar7 = 0;
  uVar3 = FUN__text__004b28b0(*(undefined1 *)(local_8 + 0xb92),*(undefined1 *)(local_8 + 0xae2),0,0)
  ;
  FUN__text__004b7e20(0xf,0xffffffff,99,*(undefined1 *)(local_8 + 0xae2),0x3b,0,uVar3,uVar7,uVar8);
  FUN__text__004d58e0(local_10c,CONCAT22(extraout_var_04,local_10));
  local_c = local_c & 0xffff0000;
  while( true ) {
    if (6 < (local_c & 0xffff)) break;
    FUN__text__004d2620(0x2c7,(local_c & 0xffff) * 0x12 + 0x10e,0x47,3,0x3a,0x10101,0);
    FUN__text__004d2620(0x2c8,(local_c & 0xffff) * 0x12 + 0x10f,0x45,1,0x39,0x3831,0);
    local_1f4 = local_c & 0xffff;
    switch(local_1f4) {
    case 0:
      local_114 = FUN__text__004b28b0(*(undefined1 *)(local_8 + 0xb88),
                                      *(undefined1 *)(local_8 + 0xad8));
      FUN__text__004b7e20(0x10,9,0x87,*(undefined1 *)(local_8 + 0xad8),0x3b,0,
                          CONCAT22(extraout_var_05,local_114),0,0);
      break;
    case 1:
      uVar3 = FUN__text__004b28b0(*(undefined1 *)(local_8 + 0xb89),*(undefined1 *)(local_8 + 0xad9))
      ;
      local_114 = (short)uVar3;
      FUN__text__004b7e20(0x11,10,0x87,*(undefined1 *)(local_8 + 0xad9),0x3b,0,uVar3,0,0);
      break;
    case 2:
      local_114 = FUN__text__004b28b0(*(undefined1 *)(local_8 + 0xb8a),
                                      *(undefined1 *)(local_8 + 0xada));
      FUN__text__004b7e20(0x12,0xb,0x87,*(undefined1 *)(local_8 + 0xada),0x3b,0,
                          CONCAT22(extraout_var_00,local_114),0,0);
      break;
    case 3:
      local_114 = FUN__text__004b28b0(*(undefined1 *)(local_8 + 0xb8b),
                                      *(undefined1 *)(local_8 + 0xadb));
      FUN__text__004b7e20(0x13,0xc,0x87,*(undefined1 *)(local_8 + 0xadb),0x3b,0,
                          CONCAT22(extraout_var_06,local_114),0,0);
      break;
    case 4:
      uVar3 = FUN__text__004b28b0(*(undefined1 *)(local_8 + 0xb8c),*(undefined1 *)(local_8 + 0xadc))
      ;
      local_114 = (short)uVar3;
      FUN__text__004b7e20(0x14,0xd,0x87,*(undefined1 *)(local_8 + 0xadc),0x3b,0,uVar3,0,0);
      break;
    case 5:
      local_114 = FUN__text__004b28b0(*(undefined1 *)(local_8 + 0xb8d),
                                      *(undefined1 *)(local_8 + 0xadd));
      FUN__text__004b7e20(0x15,0xe,0x87,*(undefined1 *)(local_8 + 0xadd),0x3b,0,
                          CONCAT22(extraout_var_01,local_114),0,0);
      break;
    case 6:
      local_114 = FUN__text__004b28b0(*(undefined1 *)(local_8 + 0xb8e),
                                      *(undefined1 *)(local_8 + 0xade));
      FUN__text__004b7e20(0x16,0xf,0x87,*(undefined1 *)(local_8 + 0xade),0x3b,0,
                          CONCAT22(extraout_var_07,local_114),0,0);
    }
    if (local_114 != 0x98) {
      local_110 = (undefined2)((asStack_d8[(local_c & 0xffff) * 0x10] * 0x45) / 100);
      FUN__text__004d2620(0x2c8,(local_c & 0xffff) * 0x12 + 0x10f,
                          CONCAT22((short)((uint)((asStack_d8[(local_c & 0xffff) * 0x10] * 0x45) %
                                                 100) >> 0x10),local_110),1,0x38,0xa68c,0);
    }
    local_c = CONCAT22(local_c._2_2_,(short)local_c + 1);
  }
  uVar8 = 0;
  uVar7 = 0;
  uVar3 = FUN__text__004b28b0(*(undefined2 *)(local_8 + 0xc80),*(undefined2 *)(local_8 + 0xc82),0,0)
  ;
  FUN__text__004b7e20(0x17,0x10,999,*(undefined2 *)(local_8 + 0xc82),0x3b,0,uVar3,uVar7,uVar8);
  bVar2 = FUN__text__004d1ba0((&DAT_006b2d8a)[(uint)*(ushort *)(local_8 + 0xc84) * 0x40],0,5);
  local_118 = CONCAT22(local_118._2_2_,(ushort)bVar2);
  local_120[0] = 0;
  local_120[1] = 0;
  local_120[2] = 1;
  local_120[3] = 2;
  local_120[4] = 3;
  local_120[5] = 4;
  local_124 = *(short *)(local_8 + 0xb0e) + (short)((int)(uint)*(ushort *)(local_8 + 0xb10) >> 1);
  iVar4 = (uint)*(ushort *)(local_8 + 0xbbe) + ((int)(uint)*(ushort *)(local_8 + 0xbc0) >> 1);
  local_128 = (short)iVar4;
  uVar7 = CONCAT22((short)((uint)iVar4 >> 0x10),(ushort)local_120[(ushort)bVar2]);
  uVar8 = 0;
  uVar3 = FUN__text__004b28b0((int)local_128,(int)local_124,0,uVar7);
  FUN__text__004b7e20(6,5,0xff,(int)local_124,0x3b,0,uVar3,uVar8,uVar7);
  if (*(short *)(local_8 + 0xb0c) == 999) {
    uVar8 = 0;
    uVar5 = (uint)local_120[local_118 & 0xffff];
    uVar7 = 0;
    uVar3 = FUN__text__004b28b0(*(undefined2 *)(local_8 + 0xbbc),*(undefined2 *)(local_8 + 0xb0c),0,
                                uVar5,0);
    FUN__text__004b7e90(5,4,999,*(undefined2 *)(local_8 + 0xb0c),0x3b,0,uVar3,uVar7,uVar5,uVar8);
    FUN__text__004d2700(&DAT_0061c090,1,0x3b,0x1f2,0xd0);
  }
  else {
    uVar5 = (uint)local_120[local_118 & 0xffff];
    uVar7 = 0;
    uVar3 = FUN__text__004b28b0(*(undefined2 *)(local_8 + 0xbbc),*(undefined2 *)(local_8 + 0xb0c),0,
                                uVar5);
    FUN__text__004b7e20(5,4,999,*(undefined2 *)(local_8 + 0xb0c),0x3b,0,uVar3,uVar7,uVar5);
  }
  uVar5 = 0;
  local_164[0x10] = 0x1e;
  local_164[0x11] = 0x3c;
  local_164[0x12] = 0x78;
  local_164[0x13] = 0xb4;
  local_164[0x14] = 0xf0;
  local_164[0x15] = 300;
  local_164[0x16] = 600;
  local_164[0x17] = 999;
  local_130 = (uint)local_130._2_2_ << 0x10;
  while (((local_130 & 0xffff) < 7 &&
         (uVar5 = (uint)local_164[(local_130 & 0xffff) + 0x10],
         (int)uVar5 < (int)*(short *)(local_8 + 0xb9c)))) {
    local_130 = CONCAT22(local_130._2_2_,(short)local_130 + 1);
  }
  local_12c = (uint)local_12c._2_2_ << 0x10;
  while (((local_12c & 0xffff) < 7 &&
         (uVar5 = (uint)local_164[(local_12c & 0xffff) + 0x10],
         (int)uVar5 < (int)*(short *)(local_8 + 0xaec)))) {
    local_12c = CONCAT22(local_12c._2_2_,(short)local_12c + 1);
  }
  if ((local_130 & 0xffff) == (local_12c & 0xffff)) {
    local_134 = (uint)local_134._2_2_ << 0x10;
  }
  else {
    uVar5 = local_130 & 0xffff;
    if (uVar5 < (local_12c & 0xffff)) {
      local_134 = CONCAT22(local_134._2_2_,2);
    }
    else {
      local_134 = CONCAT22(local_134._2_2_,1);
    }
  }
  FUN__text__004b8830(0x24b,0x48,CONCAT31((int3)(uVar5 >> 8),(undefined1)local_12c),0x3b,
                      (local_134 & 0xffff) * 0x98);
  local_164[8] = 0x1e;
  local_164[9] = 0x3c;
  local_164[10] = 0x78;
  local_164[0xb] = 0xb4;
  local_164[0xc] = 0xf0;
  local_164[0xd] = 300;
  local_164[0xe] = 600;
  local_164[0xf] = 999;
  local_130 = local_130 & 0xffff0000;
  while (((local_130 & 0xffff) < 7 &&
         ((int)(uint)local_164[(local_130 & 0xffff) + 8] < (int)*(short *)(local_8 + 0xba2)))) {
    local_130 = CONCAT22(local_130._2_2_,(short)local_130 + 1);
  }
  local_12c = local_12c & 0xffff0000;
  while (((local_12c & 0xffff) < 7 &&
         ((int)(uint)local_164[(local_12c & 0xffff) + 8] < (int)*(short *)(local_8 + 0xaf2)))) {
    local_12c = CONCAT22(local_12c._2_2_,(short)local_12c + 1);
  }
  if ((local_130 & 0xffff) == (local_12c & 0xffff)) {
    local_134 = local_134 & 0xffff0000;
  }
  else if ((local_130 & 0xffff) < (local_12c & 0xffff)) {
    local_134 = CONCAT22(local_134._2_2_,2);
  }
  else {
    local_134 = CONCAT22(local_134._2_2_,1);
  }
  FUN__text__004b8830(0x24b,0x5d,local_12c & 0xff,0x3b,(local_134 & 0xffff) * 0x98);
  local_164[0] = 999;
  local_164[1] = 0x96;
  local_164[2] = 0x7d;
  local_164[3] = 100;
  local_164[4] = 0x50;
  local_164[5] = 0x3c;
  local_164[6] = 0x28;
  local_164[7] = 0x14;
  local_130 = local_130 & 0xffff0000;
  while (((local_130 & 0xffff) < 7 && (*(ushort *)(local_8 + 0xbb2) < local_164[local_130 & 0xffff])
         )) {
    local_130 = CONCAT22(local_130._2_2_,(short)local_130 + 1);
  }
  local_12c = local_12c & 0xffff0000;
  while (((local_12c & 0xffff) < 7 && (*(ushort *)(local_8 + 0xb02) < local_164[local_12c & 0xffff])
         )) {
    local_12c = CONCAT22(local_12c._2_2_,(short)local_12c + 1);
  }
  if ((local_130 & 0xffff) == (local_12c & 0xffff)) {
    local_134 = local_134 & 0xffff0000;
  }
  else if ((local_130 & 0xffff) < (local_12c & 0xffff)) {
    local_134 = CONCAT22(local_134._2_2_,2);
  }
  else {
    local_134 = CONCAT22(local_134._2_2_,1);
  }
  FUN__text__004b8830(0x24b,0x94,local_12c & 0xff,0x3b,(local_134 & 0xffff) * 0x98);
  FUN__text__004b8460(0x2c7,0x80,CONCAT22(extraout_var_08,*(undefined2 *)(local_8 + 0xc84)),0x43);
  FUN__text__004b8700(0x28b,0x49,CONCAT22(extraout_var_02,*(undefined2 *)(local_8 + 0xc84)),0x42);
  FUN__text__004b1f30();
  FUN__text__004b2100();
  local_1b0[0] = 1;
  local_1b0[1] = 0x21a;
  local_1b0[2] = 0x30;
  local_1b0[3] = 10;
  local_1b0[4] = 2;
  local_1b0[5] = 0x21a;
  local_1b0[6] = 0x30;
  local_1b0[7] = 0xb;
  local_1b0[8] = 3;
  local_1b0[9] = 0x21a;
  local_1b0[10] = 0x30;
  local_1b0[0xb] = 0xc;
  local_1b0[0xc] = 4;
  local_1b0[0xd] = 0x21a;
  local_1b0[0xe] = 0x30;
  local_1b0[0xf] = 0xd;
  local_1b0[0x10] = 5;
  local_1b0[0x11] = 0x21a;
  local_1b0[0x12] = 0xba;
  local_1b0[0x13] = 0xe;
  local_1b0[0x14] = 6;
  local_1b0[0x15] = 0x21a;
  local_1b0[0x16] = 0xba;
  local_1b0[0x17] = 0xf;
  local_1b0[0x18] = 7;
  local_1b0[0x19] = 0x21a;
  local_1b0[0x1a] = 0xba;
  local_1b0[0x1b] = 0x10;
  local_1b0[0x1c] = 8;
  local_1b0[0x1d] = 0x21a;
  local_1b0[0x1e] = 0x12e;
  local_1b0[0x1f] = 0x11;
  local_1b0[0x20] = 9;
  local_1b0[0x21] = 0x21a;
  local_1b0[0x22] = 0x12e;
  local_1b0[0x23] = 0x12;
  local_1b0[0x24] = 0xffff;
  local_1c4 = local_1c4 & 0xffff0000;
  while (local_1c8 = local_1b0[(local_1c4 & 0xffff) * 4], local_1c8 != -1) {
    local_1cc = local_1b0[(local_1c4 & 0xffff) * 4 + 1];
    local_1d0 = local_1b0[(local_1c4 & 0xffff) * 4 + 2];
    local_1d4 = local_1b0[(local_1c4 & 0xffff) * 4 + 3];
    FUN__text__004d5c40(local_1c0,CONCAT22((short)(((local_1c4 & 0xffff) << 2) >> 0x10),local_1c8));
    if ((local_1b4 & 0xffff) != 0) {
      FUN__text__004b8930(local_1cc,CONCAT22(extraout_var_03,local_1d0),(undefined1)local_1d4,0);
    }
    local_1c4 = CONCAT22(local_1c4._2_2_,(short)local_1c4 + 1);
  }
  FUN__text__004d5ec0(local_1e4,0x21,0x38,0xe8,0x147);
  if (((local_1d8 & 0xffff) != 0) && ((local_1e0 & 1) != 0)) {
    FUN__text__004d48a0(CONCAT22(extraout_var,local_10),0,0xffffffff,0);
  }
  local_c = local_c & 0xffff0000;
  while ((local_c & 0xffff) < 10) {
    local_1f0 = 0;
    FUN__text__0040a100(local_8 + 0x3a1f4 + (local_c & 0xffff) * 0x58);
    local_1f8 = local_c & 0xffff;
    if (local_1f8 == 0) {
      local_1e8 = 0x2db;
      local_1ec = 0xb0;
    }
    else if (local_1f8 == 1) {
      local_1e8 = 0x2f4;
      local_1ec = 0x38;
    }
    else if (local_1f8 == 2) {
      local_1e8 = DAT_007d6a38 * 0x24 + 0x103;
      local_1ec = DAT_007d6a3a * 0x24 + 0x1fc;
    }
    else {
      local_1e8 = *(short *)(DAT_007a49fc + 0x196c);
      local_1ec = *(short *)(DAT_007a49fc + 0x1970);
    }
    FUN__text__0040a330(local_8 + 0x3a1f4 + (local_c & 0xffff) * 0x58,local_8 + 0x3a564,
                        (int)local_1e8,(int)local_1ec,local_1f0);
    local_c = CONCAT22(local_c._2_2_,(short)local_c + 1);
  }
  local_8 = 0x4b3b8c;
  FUN__text__0056ce80();
  return;
}

