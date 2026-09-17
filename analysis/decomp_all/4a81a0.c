
void __fastcall FUN__text__004a81a0(int param_1)

{
  undefined4 *puVar1;
  undefined2 extraout_var;
  undefined2 extraout_var_00;
  undefined2 extraout_var_01;
  undefined2 extraout_var_02;
  undefined2 extraout_var_03;
  undefined2 extraout_var_04;
  undefined2 extraout_var_05;
  undefined2 uVar2;
  int iVar3;
  uint uVar4;
  undefined2 extraout_var_06;
  undefined2 extraout_var_07;
  undefined2 extraout_var_08;
  undefined2 extraout_var_09;
  undefined2 extraout_var_10;
  undefined2 extraout_var_11;
  undefined2 extraout_var_12;
  undefined2 uVar5;
  ushort uVar6;
  undefined2 extraout_var_13;
  undefined4 local_e4 [16];
  char local_a4;
  char local_a0;
  uint local_9c;
  char local_98;
  char local_94;
  int local_90;
  undefined1 local_8c [16];
  short local_7c;
  uint local_78;
  uint local_74;
  short local_70;
  short local_6c;
  ushort local_68;
  undefined2 uStack_66;
  short asStack_64 [2];
  undefined4 auStack_60 [2];
  undefined2 auStack_58 [30];
  undefined1 local_1c [4];
  uint local_18;
  uint local_c;
  int local_8;
  
  puVar1 = local_e4;
  for (iVar3 = 0x38; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar1 = 0xcccccccc;
    puVar1 = puVar1 + 1;
  }
  local_c = local_c & 0xffff0000;
  local_8 = param_1;
  while ((local_c & 0xffff) < 5) {
    puVar1 = (undefined4 *)FUN__text__004a95f0(local_8c,local_c & 0xffff);
    uVar4 = local_c & 0xffff;
    *(undefined4 *)(asStack_64 + uVar4 * 7) = *puVar1;
    *(undefined4 *)((int)auStack_60 + uVar4 * 0xe) = puVar1[1];
    *(undefined4 *)((int)auStack_60 + uVar4 * 0xe + 4) = puVar1[2];
    auStack_58[uVar4 * 7] = *(undefined2 *)(puVar1 + 3);
    local_90 = (int)asStack_64[(local_c & 0xffff) * 7];
    if ((1 < local_90) && (local_90 < 6)) {
      uVar6 = 8 - *(short *)((int)auStack_60 + (local_c & 0xffff) * 0xe);
      _local_68 = CONCAT22(uStack_66,uVar6);
      if ((uint)uVar6 != (int)*(short *)(local_8 + 0x2c0 + (local_c & 0xffff) * 2)) {
        FUN__text__00409ff0(local_8 + 0x88 + (local_c & 0xffff) * 0x58,0,uVar6,0);
      }
      *(ushort *)(local_8 + 0x2c0 + (local_c & 0xffff) * 2) = local_68;
      FUN__text__0040a100(local_8 + 0x88 + (local_c & 0xffff) * 0x58);
      FUN__text__0040a330(local_8 + 0x88 + (local_c & 0xffff) * 0x58,local_8 + 0x240,0xac,
                          (local_c & 0xffff) * 0x61 + 0x8e,0x6e);
    }
    local_c = CONCAT22(local_c._2_2_,(short)local_c + 1);
  }
  FUN__text__004d2700(&DAT_0061b208,1,0x80,0,0);
  FUN__text__004d1cf0(&DAT_0061b4b8,0x36,0x244,2,0x7a,(int)DAT_007d57de,0);
  FUN__text__004d1cf0(&DAT_0061b4b8,0x54,0x244,2,0x7a,(int)DAT_007d57e0,0);
  FUN__text__004d1cf0(&DAT_0061b4b8,0x36,0x2a5,2,0x7a,(int)DAT_007d58b0,0);
  FUN__text__004d1cf0(&DAT_0061b4b8,0x54,0x2a5,2,0x7a,(int)DAT_007d58b2,0);
  FUN__text__004d1cf0(&DAT_0061b4c8,0x3e2,0x1dd,2,0x7a,DAT_007d6a14,0);
  FUN__text__004d1cf0(&DAT_0061b4c8,0x3e2,0x1fc,2,0x7a,DAT_007d6a16,0);
  FUN__text__004d1cf0(&DAT_0061b4c8,0x3e2,0x21b,2,0x7a,DAT_007d6a18,0);
  FUN__text__004d1cf0(&DAT_0061b4c8,0x3e2,0x70,2,0x7a,DAT_007d62fe,0);
  FUN__text__004d1cf0(&DAT_0061b4c8,0x3e2,0x8f,2,0x7a,DAT_007d62fc,0);
  if (DAT_007a55fa != 0) {
    FUN__text__004d2700(&DAT_0061b428,1,0x78,0x3a1,0x47);
  }
  FUN__text__004a6460();
  FUN__text__004a5440();
  FUN__text__004a1ff0();
  FUN__text__004a2da0();
  if (DAT_007a55fa == 0) {
    local_94 = DAT_007d598a;
    if (DAT_007d598a == '\0') {
      FUN__text__004ab0d0(0x2c,0,0,0x7f);
    }
    else if (DAT_007d598a == '\x01') {
      FUN__text__004ab0d0(0x2d,0,0,0x7f);
    }
    else if (DAT_007d598a == '\x02') {
      FUN__text__004ab0d0(0x2e,0,0,0x7f);
    }
    local_98 = DAT_007d5984;
    if (DAT_007d5984 == '\0') {
      FUN__text__004ab0d0(0x1e,0,0,0x7f);
    }
    else if (DAT_007d5984 == '\x01') {
      FUN__text__004ab0d0(0x1f,0,0,0x7f);
    }
  }
  else {
    FUN__text__004d2620(0x3a2,0x68,0x5a,0x3c,0x70,0x90010101,1);
  }
  local_6c = 1;
  local_c = local_c & 0xffff0000;
  while ((local_c & 0xffff) < 5) {
    if (*(short *)(&DAT_007aaa12 + (local_c & 0xffff) * 0x1c) == -1) {
      FUN__text__004d2620(6,(local_c & 0xffff) * 0x61 + 0x4d,0x212,0x5f,0x70,0x90010101,1);
    }
    else {
      FUN__text__004d5ec0(local_1c,10,(local_c & 0xffff) * 0x61 + 0x51,0x20a,0x57);
      if ((local_18 & 1) != 0) {
        FUN__text__004a8b50(CONCAT22(extraout_var_13,(short)local_c));
        FUN__text__004db2b0(5);
      }
    }
    if ((&DAT_007aaa15)[(local_c & 0xffff) * 0x1c] == '\0') {
      local_6c = 0;
      FUN__text__004ab0d0((local_c & 0xffff) + 1,0,0,0x7f);
      FUN__text__004ab0d0((local_c & 0xffff) + 0x19,0,(local_c & 0xffff) * 0x1a,0x7f);
      FUN__text__004d2620(0x60,(local_c & 0xffff) * 0x61 + 0x96,0x74,0x16,0x70,0x90010101,1);
    }
    else {
      FUN__text__004ab0d0((local_c & 0xffff) + 6,0,0,0x7f);
    }
    local_c = CONCAT22(local_c._2_2_,(short)local_c + 1);
  }
  if (local_6c != 0) {
    FUN__text__004d2620(0x61,0x30,0x74,0x16,0x70,0x90010101,1);
  }
  local_70 = FUN__text__004a8bc0();
  if (local_70 != -1) {
    if (*(short *)(&DAT_007aaa12 + local_70 * 0x1c) == -1) {
      FUN__text__004a8b50(0xffffffff);
    }
    else {
      FUN__text__004d2700(&DAT_0061b408,1,0x71,3,local_70 * 0x61 + 0x4a);
      FUN__text__004aadb0(0x23d,0x1d3,1,*(short *)(&DAT_007aaa12 + local_70 * 0x1c) + -0x65,0xff,
                          0xff,0x77);
      FUN__text__004aaf60(0x241,0x21e,1,*(short *)(&DAT_007aaa12 + local_70 * 0x1c) + -0x65,0xff,
                          0x77);
    }
  }
  uVar4 = (uint)DAT_007d6a26;
  if (uVar4 == 0) {
    uVar4 = FUN__text__004d2620(0xd6,0x28,0x142,0x23,0x70,0x90010101,1);
  }
  uVar2 = (undefined2)(uVar4 >> 0x10);
  uVar5 = 0;
  local_9c = (uint)DAT_007d5982;
  switch(local_9c) {
  case 0:
    FUN__text__004ab0d0(0x20,0,0,0x7f);
    uVar2 = extraout_var;
    uVar5 = extraout_var_06;
    break;
  case 1:
    FUN__text__004ab0d0(0x21,0,0,0x7f);
    uVar2 = extraout_var_00;
    uVar5 = extraout_var_07;
    break;
  case 2:
    FUN__text__004ab0d0(0x22,0,0,0x7f);
    uVar2 = extraout_var_01;
    uVar5 = extraout_var_08;
    break;
  case 3:
    FUN__text__004ab0d0(0x23,0,0,0x7f);
    uVar2 = extraout_var_02;
    uVar5 = extraout_var_09;
  }
  local_a0 = DAT_007d57da;
  if (DAT_007d57da == '\0') {
    FUN__text__004ab0d0(0xb,0,0,0x7f);
    uVar2 = extraout_var_03;
    uVar5 = extraout_var_10;
  }
  else if (DAT_007d57da == '\x01') {
    FUN__text__004ab0d0(0xc,0,0,0x7f);
    uVar2 = extraout_var_04;
    uVar5 = extraout_var_11;
  }
  else if (DAT_007d57da == '\x02') {
    FUN__text__004ab0d0(0xd,0,0,0x7f);
    uVar2 = extraout_var_05;
    uVar5 = extraout_var_12;
  }
  local_a4 = *(char *)(local_8 + 0x76c2);
  if (local_a4 == '\0') {
    FUN__text__004d29e0(0xc,0,1,0x65,*(undefined2 *)(DAT_007a49fc + 0x196c),
                        *(undefined2 *)(DAT_007a49fc + 0x1970),0x326,0x300,0x28,0x30,100,100,0xff,
                        0x80,0x80,0x80);
  }
  else if (local_a4 == '\x01') {
    FUN__text__004d29e0(0xc,0,1,0x65,*(undefined2 *)(DAT_007a49fc + 0x196c),
                        CONCAT22(uVar2,*(undefined2 *)(DAT_007a49fc + 0x1970)),0x34e,0x300,0x28,0x30
                        ,100,100,0xff,0x80,0x80,0x80);
  }
  else if (local_a4 == '\x02') {
    FUN__text__004d29e0(0xc,0,1,0x65,*(undefined2 *)(DAT_007a49fc + 0x196c),
                        CONCAT22(uVar5,*(undefined2 *)(DAT_007a49fc + 0x1970)),0x376,0x300,0x28,0x30
                        ,100,100,0xff,0x80,0x80,0x80);
  }
  local_74 = CONCAT31(local_74._1_3_,1);
  local_78 = CONCAT31(local_78._1_3_,1);
  local_7c = FUN__text__004a8bc0();
  if ((local_7c != -1) && (*(short *)(&DAT_007aaa12 + local_7c * 0x1c) != -1)) {
    if ((&DAT_007aaa15)[local_7c * 0x1c] == '\0') {
      local_74 = local_74 & 0xffffff00;
    }
    else {
      local_78 = local_78 & 0xffffff00;
    }
  }
  if ((local_74 & 0xff) != 0) {
    FUN__text__004d2620(0x232,0x27,0x1cd,0x184,0x70,0x90010101,1);
  }
  if ((local_78 & 0xff) != 0) {
    FUN__text__004d2620(0x232,0x1b6,0x1cd,0x145,0x70,0x90010101,1);
  }
  FUN__text__004d69e0();
  local_8 = 0x4a8b33;
  FUN__text__0056ce80();
  return;
}

