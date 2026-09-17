
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __fastcall FUN__text__0051e2b0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  int local_10;
  uint local_c;
  int local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_10 = *(byte *)(param_1 + 0x35) - 1;
  local_8 = param_1;
  switch(local_10) {
  case 0:
    if (*(char *)(param_1 + 0xea) != '\0') {
      if (*(char *)(param_1 + 0xea) == '\x01') {
        local_c = local_c & 0xffffff00;
        FUN__text__00505580((int)_DAT_007579c8,(int)_DAT_007579ca,(int)_DAT_007579cc,
                            (int)*(short *)(param_1 + 0x11a),(int)_DAT_007579d0,(int)_DAT_007579d2,
                            (int)_DAT_007579d4,(int)_DAT_007579d6,*(undefined1 *)(param_1 + 0x102),
                            0x80,0x80,0x80);
      }
      else {
        local_c = (uint)local_c._1_3_ << 8;
        FUN__text__00505000((int)_DAT_007579c8,(int)_DAT_007579ca,(int)_DAT_007579cc,
                            (int)*(short *)(param_1 + 0x11a),(int)_DAT_007579d0,(int)_DAT_007579d2,
                            (int)_DAT_007579d4,(int)_DAT_007579d6);
      }
    }
    if ((*(char *)(local_8 + 0xeb) != '\0') && (*(char *)(local_8 + 0xeb) == '\x01')) {
      local_c = CONCAT31(local_c._1_3_,1);
      while ((local_c & 0xff) < 9) {
        FUN__text__00505000((int)*(short *)(&DAT_007579c8 + (local_c & 0xff) * 0x10),
                            (int)*(short *)(&DAT_007579ca + (local_c & 0xff) * 0x10),
                            (int)*(short *)(&DAT_007579cc + (local_c & 0xff) * 0x10),
                            (int)*(short *)(local_8 + 0x11c) +
                            (uint)*(ushort *)(&DAT_00758870 + (local_c & 0xff) * 2),
                            (int)*(short *)(&DAT_007579d0 + (local_c & 0xff) * 0x10),
                            (int)*(short *)(&DAT_007579d2 + (local_c & 0xff) * 0x10),
                            (int)*(short *)(&DAT_007579d4 + (local_c & 0xff) * 0x10),
                            (int)*(short *)(&DAT_007579d6 + (local_c & 0xff) * 0x10));
        local_c = CONCAT31(local_c._1_3_,(char)local_c + '\x01');
      }
    }
    if ((*(char *)(local_8 + 0xec) != '\0') && (*(char *)(local_8 + 0xec) == '\x01')) {
      local_c = CONCAT31(local_c._1_3_,9);
      while ((local_c & 0xff) < 0xe) {
        FUN__text__00505000((int)*(short *)(&DAT_007579c8 + (local_c & 0xff) * 0x10),
                            (int)*(short *)(&DAT_007579ca + (local_c & 0xff) * 0x10),
                            (int)*(short *)(&DAT_007579cc + (local_c & 0xff) * 0x10),
                            (int)*(short *)(local_8 + 0x11e) +
                            (uint)*(ushort *)(&DAT_00758870 + (local_c & 0xff) * 2),
                            (int)*(short *)(&DAT_007579d0 + (local_c & 0xff) * 0x10),
                            (int)*(short *)(&DAT_007579d2 + (local_c & 0xff) * 0x10),
                            (int)*(short *)(&DAT_007579d4 + (local_c & 0xff) * 0x10),
                            (int)*(short *)(&DAT_007579d6 + (local_c & 0xff) * 0x10));
        local_c = CONCAT31(local_c._1_3_,(char)local_c + '\x01');
      }
    }
    if ((*(char *)(local_8 + 0xed) != '\0') && (*(char *)(local_8 + 0xed) == '\x01')) {
      local_c = CONCAT31(local_c._1_3_,0xe);
      FUN__text__00505580((int)_UNK_00757aa8,(int)_UNK_00757aaa,(int)_UNK_00757aac,
                          (int)*(short *)(local_8 + 0x120),(int)_UNK_00757ab0,(int)_UNK_00757ab2,
                          (int)_UNK_00757ab4,(int)_UNK_00757ab6,*(undefined1 *)(local_8 + 0x105),
                          0x80,0x80,0x80);
    }
    if (*(char *)(local_8 + 0xee) != '\0') {
      if (*(char *)(local_8 + 0xee) == '\x01') {
        local_c = CONCAT31(local_c._1_3_,0xf);
        FUN__text__00505580((int)_UNK_00757ab8,(int)_UNK_00757aba,(int)_UNK_00757abc,
                            (int)*(short *)(local_8 + 0x122),(int)_UNK_00757ac0,(int)_UNK_00757ac2,
                            (int)_UNK_00757ac4,(int)_UNK_00757ac6,*(undefined1 *)(local_8 + 0x106),
                            0x80,0x80,0x80);
      }
      else {
        local_c = CONCAT31(local_c._1_3_,0xf);
        FUN__text__00505000((int)_UNK_00757ab8,(int)_UNK_00757aba,(int)_UNK_00757abc,
                            (int)*(short *)(local_8 + 0x122),(int)_UNK_00757ac0,(int)_UNK_00757ac2,
                            (int)_UNK_00757ac4,(int)_UNK_00757ac6);
      }
    }
    if (*(char *)(local_8 + 0xef) != '\0') {
      if (*(char *)(local_8 + 0xef) == '\x01') {
        local_c = CONCAT31(local_c._1_3_,0x10);
        FUN__text__00505580((int)_UNK_00757ac8,(int)_UNK_00757aca,(int)_UNK_00757acc,
                            (int)*(short *)(local_8 + 0x124),(int)_UNK_00757ad0,(int)_UNK_00757ad2,
                            (int)_UNK_00757ad4,(int)_UNK_00757ad6,*(undefined1 *)(local_8 + 0x107),
                            0x80,0x80,0x80);
      }
      else {
        local_c = CONCAT31(local_c._1_3_,0x10);
        FUN__text__00505000((int)_UNK_00757ac8,(int)_UNK_00757aca,(int)_UNK_00757acc,
                            (int)*(short *)(local_8 + 0x124),(int)_UNK_00757ad0,(int)_UNK_00757ad2,
                            (int)_UNK_00757ad4,(int)_UNK_00757ad6);
      }
    }
    break;
  case 1:
    if (*(char *)(param_1 + 0xea) != '\0') {
      local_c = CONCAT31(local_c._1_3_,0x20);
      FUN__text__00505580((int)_UNK_00757bc8,(int)_UNK_00757bca,(int)_UNK_00757bcc,
                          (int)_UNK_00757bce,(int)_UNK_00757bd0,(int)_UNK_00757bd2,
                          (int)_UNK_00757bd4,(int)_UNK_00757bd6,*(undefined1 *)(param_1 + 0x102),
                          0x80,0x80,0x80);
    }
    if (*(char *)(local_8 + 0xeb) != '\0') {
      local_c = CONCAT31(local_c._1_3_,0x21);
      FUN__text__00505580((int)_UNK_00757bd8,(int)_UNK_00757bda,(int)_UNK_00757bdc,
                          (int)_UNK_00757bde,(int)_UNK_00757be0,(int)_UNK_00757be2,
                          (int)_UNK_00757be4,(int)_UNK_00757be6,*(undefined1 *)(local_8 + 0x103),
                          0x80,0x80,0x80);
    }
    if (*(char *)(local_8 + 0xec) != '\0') {
      local_c = CONCAT31(local_c._1_3_,0x24);
      FUN__text__00505580((int)_UNK_00757c08,(int)_UNK_00757c0a,(int)_UNK_00757c0c,
                          (int)_UNK_00757c0e,(int)_UNK_00757c10,(int)_UNK_00757c12,
                          (int)_UNK_00757c14,(int)_UNK_00757c16,*(undefined1 *)(local_8 + 0x104),
                          0x80,0x80,0x80);
    }
    if (*(char *)(local_8 + 0xed) != '\0') {
      local_c = CONCAT31(local_c._1_3_,0x22);
      FUN__text__00505580((int)_UNK_00757be8,(int)_UNK_00757bea,(int)_UNK_00757bec,
                          (int)_UNK_00757bee,(int)_UNK_00757bf0,(int)_UNK_00757bf2,
                          (int)_UNK_00757bf4,(int)_UNK_00757bf6,*(undefined1 *)(local_8 + 0x105),
                          0x80,0x80,0x80);
    }
    if (*(char *)(local_8 + 0xee) != '\0') {
      local_c = CONCAT31(local_c._1_3_,0x25);
      FUN__text__00505580((int)_UNK_00757c18,(int)_UNK_00757c1a,(int)_UNK_00757c1c,
                          (int)_UNK_00757c1e,(int)_UNK_00757c20,(int)_UNK_00757c22,
                          (int)_UNK_00757c24,(int)_UNK_00757c26,*(undefined1 *)(local_8 + 0x106),
                          0x80,0x80,0x80);
    }
    if (*(char *)(local_8 + 0xef) != '\0') {
      local_c = CONCAT31(local_c._1_3_,0x23);
      FUN__text__00505580((int)_UNK_00757bf8,(int)_UNK_00757bfa,(int)_UNK_00757bfc,
                          (int)_UNK_00757bfe,(int)_UNK_00757c00,(int)_UNK_00757c02,
                          (int)_UNK_00757c04,(int)_UNK_00757c06,*(undefined1 *)(local_8 + 0x107),
                          0x80,0x80,0x80);
    }
    if (*(char *)(local_8 + 0xf0) != '\0') {
      local_c = CONCAT31(local_c._1_3_,0x26);
      FUN__text__00505580((int)_UNK_00757c28,(int)_UNK_00757c2a,(int)_UNK_00757c2c,
                          (int)_UNK_00757c2e,(int)_UNK_00757c30,(int)_UNK_00757c32,
                          (int)_UNK_00757c34,(int)_UNK_00757c36,*(undefined1 *)(local_8 + 0x108),
                          0x80,0x80,0x80);
    }
    if (*(char *)(local_8 + 0xf1) != '\0') {
      local_c = CONCAT31(local_c._1_3_,0x27);
      if (*(char *)(local_8 + 0xf1) == '\x01') {
        FUN__text__00505580((int)_UNK_00757c38,(int)_UNK_00757c3a,(int)_UNK_00757c3c,
                            (int)_UNK_00757c3e,(int)_UNK_00757c40,(int)_UNK_00757c42,
                            (int)_UNK_00757c44,(int)_UNK_00757c46,*(undefined1 *)(local_8 + 0x109),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00757c38,(int)_UNK_00757c3a,(int)_UNK_00757c3c,
                            (int)_UNK_00757c3e,(int)_UNK_00757c40,(int)_UNK_00757c42,
                            (int)_UNK_00757c44,(int)_UNK_00757c46);
      }
    }
    break;
  case 2:
    if (*(char *)(param_1 + 0xf1) != '\0') {
      local_c = CONCAT31(local_c._1_3_,0x27);
      FUN__text__00505000((int)_UNK_00757c38,(int)_UNK_00757c3a,(int)_UNK_00757c3c,
                          (int)_UNK_00757c3e,(int)_UNK_00757c40,(int)_UNK_00757c42,
                          (int)_UNK_00757c44,(int)_UNK_00757c46);
    }
    if (*(char *)(local_8 + 0xea) != '\0') {
      local_c = CONCAT31(local_c._1_3_,0x28);
      if ((*(char *)(local_8 + 0xea) == '\x01') || (*(char *)(local_8 + 0xea) == '\x03')) {
        FUN__text__00505580((int)_UNK_00757c48,(int)_UNK_00757c4a,(int)*(short *)(local_8 + 0x10a),
                            (int)PTR_DAT_00757c4c._2_2_,(int)_UNK_00757c50,(int)_UNK_00757c52,
                            (int)_UNK_00757c54,(int)_UNK_00757c56,*(undefined1 *)(local_8 + 0x102),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00757c48,(int)_UNK_00757c4a,(int)*(short *)(local_8 + 0x10a),
                            (int)PTR_DAT_00757c4c._2_2_,(int)_UNK_00757c50,(int)_UNK_00757c52,
                            (int)_UNK_00757c54,(int)_UNK_00757c56);
      }
    }
    if (*(char *)(local_8 + 0xeb) != '\0') {
      local_c = CONCAT31(local_c._1_3_,0x29);
      if ((*(char *)(local_8 + 0xeb) == '\x01') || (*(char *)(local_8 + 0xeb) == '\x03')) {
        FUN__text__00505580((int)_UNK_00757c58,(int)_UNK_00757c5a,(int)*(short *)(local_8 + 0x10c),
                            (int)PTR_DAT_00757c5c._2_2_,(int)_UNK_00757c60,(int)_UNK_00757c62,
                            (int)_UNK_00757c64,(int)_UNK_00757c66,*(undefined1 *)(local_8 + 0x103),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00757c58,(int)_UNK_00757c5a,(int)*(short *)(local_8 + 0x10c),
                            (int)PTR_DAT_00757c5c._2_2_,(int)_UNK_00757c60,(int)_UNK_00757c62,
                            (int)_UNK_00757c64,(int)_UNK_00757c66);
      }
    }
    break;
  case 3:
    if (*(char *)(param_1 + 0xeb) != '\0') {
      local_c = CONCAT31(local_c._1_3_,0x29);
      if ((*(char *)(param_1 + 0xeb) == '\x01') || (*(char *)(param_1 + 0xeb) == '\x03')) {
        FUN__text__00505580((int)_UNK_00757c58,(int)_UNK_00757c5a,(int)*(short *)(param_1 + 0x10c),
                            (int)PTR_DAT_00757c5c._2_2_,(int)_UNK_00757c60,(int)_UNK_00757c62,
                            (int)_UNK_00757c64,(int)_UNK_00757c66,*(undefined1 *)(param_1 + 0x103),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00757c58,(int)_UNK_00757c5a,(int)*(short *)(param_1 + 0x10c),
                            (int)PTR_DAT_00757c5c._2_2_,(int)_UNK_00757c60,(int)_UNK_00757c62,
                            (int)_UNK_00757c64,(int)_UNK_00757c66);
      }
    }
    if (*(char *)(local_8 + 0xea) != '\0') {
      local_c = CONCAT31(local_c._1_3_,0x2a);
      FUN__text__00505000((int)_UNK_00757c68,(int)_UNK_00757c6a,(int)*(short *)(local_8 + 0x10a),
                          (int)PTR_DAT_00757c6c._2_2_,(int)_UNK_00757c70,(int)_UNK_00757c72,
                          (int)_UNK_00757c74,(int)_UNK_00757c76);
    }
    break;
  case 4:
    if (*(char *)(param_1 + 0xea) != '\0') {
      local_c = CONCAT31(local_c._1_3_,0x2c);
      if ((*(char *)(param_1 + 0xea) == '\x01') || (*(char *)(param_1 + 0xea) == '\x03')) {
        FUN__text__00505580((int)_UNK_00757c88,(int)_UNK_00757c8a,(int)_UNK_00757c8c,
                            (int)*(short *)(param_1 + 0x11a),(int)_UNK_00757c90,(int)_UNK_00757c92,
                            (int)_UNK_00757c94,(int)_UNK_00757c96,*(undefined1 *)(param_1 + 0x102),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00757c88,(int)_UNK_00757c8a,(int)_UNK_00757c8c,
                            (int)*(short *)(param_1 + 0x11a),(int)_UNK_00757c90,(int)_UNK_00757c92,
                            (int)_UNK_00757c94,(int)_UNK_00757c96);
      }
    }
    if (*(char *)(local_8 + 0xeb) != '\0') {
      local_c = CONCAT31(local_c._1_3_,0x2d);
      if ((*(char *)(local_8 + 0xeb) == '\x01') || (*(char *)(local_8 + 0xeb) == '\x03')) {
        FUN__text__00505580((int)_UNK_00757c98,(int)_UNK_00757c9a,(int)_UNK_00757c9c,
                            (int)*(short *)(local_8 + 0x11c),(int)_UNK_00757ca0,(int)_UNK_00757ca2,
                            (int)_UNK_00757ca4,(int)_UNK_00757ca6,*(undefined1 *)(local_8 + 0x103),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00757c98,(int)_UNK_00757c9a,(int)_UNK_00757c9c,
                            (int)*(short *)(local_8 + 0x11c),(int)_UNK_00757ca0,(int)_UNK_00757ca2,
                            (int)_UNK_00757ca4,(int)_UNK_00757ca6);
      }
    }
    if (*(char *)(local_8 + 0xec) != '\0') {
      local_c = CONCAT31(local_c._1_3_,0x2e);
      if ((*(char *)(local_8 + 0xec) == '\x01') || (*(char *)(local_8 + 0xec) == '\x03')) {
        FUN__text__00505580((int)_UNK_00757ca8,(int)_UNK_00757caa,(int)_UNK_00757cac,
                            (int)*(short *)(local_8 + 0x11e),(int)_UNK_00757cb0,(int)_UNK_00757cb2,
                            (int)_UNK_00757cb4,(int)_UNK_00757cb6,*(undefined1 *)(local_8 + 0x104),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00757ca8,(int)_UNK_00757caa,(int)_UNK_00757cac,
                            (int)*(short *)(local_8 + 0x11e),(int)_UNK_00757cb0,(int)_UNK_00757cb2,
                            (int)_UNK_00757cb4,(int)_UNK_00757cb6);
      }
    }
    if (*(char *)(local_8 + 0xed) != '\0') {
      local_c = CONCAT31(local_c._1_3_,0x2f);
      if (*(char *)(local_8 + 0xed) == '\x03') {
        FUN__text__00505580((int)_UNK_00757cb8,(int)_UNK_00757cba,(int)_UNK_00757cbc,
                            (int)*(short *)(local_8 + 0x120),(int)_UNK_00757cc0,(int)_UNK_00757cc2,
                            (int)_UNK_00757cc4,(int)_UNK_00757cc6,*(undefined1 *)(local_8 + 0x105),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00757cb8,(int)_UNK_00757cba,(int)_UNK_00757cbc,
                            (int)*(short *)(local_8 + 0x120),(int)_UNK_00757cc0,(int)_UNK_00757cc2,
                            (int)_UNK_00757cc4,(int)_UNK_00757cc6);
      }
    }
    break;
  case 5:
    if (*(char *)(param_1 + 0xed) != '\0') {
      local_c = CONCAT31(local_c._1_3_,0x2f);
      if (*(char *)(param_1 + 0xed) == '\x03') {
        FUN__text__00505580((int)_UNK_00757cb8,(int)_UNK_00757cba,(int)_UNK_00757cbc,
                            (int)*(short *)(param_1 + 0x120),(int)_UNK_00757cc0,(int)_UNK_00757cc2,
                            (int)_UNK_00757cc4,(int)_UNK_00757cc6,*(undefined1 *)(param_1 + 0x105),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00757cb8,(int)_UNK_00757cba,(int)_UNK_00757cbc,
                            (int)*(short *)(param_1 + 0x120),(int)_UNK_00757cc0,(int)_UNK_00757cc2,
                            (int)_UNK_00757cc4,(int)_UNK_00757cc6);
      }
    }
    if (*(char *)(local_8 + 0xea) != '\0') {
      local_c = CONCAT31(local_c._1_3_,0x2b);
      FUN__text__00505580((int)_UNK_00757c78,(int)_UNK_00757c7a,(int)_UNK_00757c7c,
                          (int)_UNK_00757c7e,(int)_UNK_00757c80,(int)_UNK_00757c82,
                          (int)_UNK_00757c84,(int)_UNK_00757c86,*(undefined1 *)(local_8 + 0x102),
                          0x80,0x80,0x80);
    }
    if (*(char *)(local_8 + 0xeb) != '\0') {
      local_c = CONCAT31(local_c._1_3_,0x25);
      if ((*(char *)(local_8 + 0xeb) == '\x01') || (*(char *)(local_8 + 0xeb) == '\x03')) {
        FUN__text__00505580((int)_UNK_00757c18,(int)_UNK_00757c1a,(int)_UNK_00757c1c,
                            (int)_UNK_00757c1e,(int)_UNK_00757c20,(int)_UNK_00757c22,
                            (int)_UNK_00757c24,(int)_UNK_00757c26,*(undefined1 *)(local_8 + 0x103),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00757c18,(int)_UNK_00757c1a,(int)_UNK_00757c1c,
                            (int)_UNK_00757c1e,(int)_UNK_00757c20,(int)_UNK_00757c22,
                            (int)_UNK_00757c24,(int)_UNK_00757c26);
      }
    }
    if (*(char *)(local_8 + 0xec) != '\0') {
      local_c = CONCAT31(local_c._1_3_,0x30);
      if ((*(char *)(local_8 + 0xec) == '\x01') || (*(char *)(local_8 + 0xec) == '\x03')) {
        FUN__text__00505580((int)_UNK_00757cc8,(int)_UNK_00757cca,(int)_UNK_00757ccc,
                            (int)*(short *)(local_8 + 0x11e),(int)_UNK_00757cd0,(int)_UNK_00757cd2,
                            (int)_UNK_00757cd4,(int)_UNK_00757cd6,*(undefined1 *)(local_8 + 0x104),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00757cc8,(int)_UNK_00757cca,(int)_UNK_00757ccc,
                            (int)*(short *)(local_8 + 0x11e),(int)_UNK_00757cd0,(int)_UNK_00757cd2,
                            (int)_UNK_00757cd4,(int)_UNK_00757cd6);
      }
    }
    break;
  case 6:
    if (*(char *)(param_1 + 0xec) != '\0') {
      local_c = CONCAT31(local_c._1_3_,0x30);
      if ((*(char *)(param_1 + 0xec) == '\x01') || (*(char *)(param_1 + 0xec) == '\x03')) {
        FUN__text__00505580((int)_UNK_00757cc8,(int)_UNK_00757cca,(int)_UNK_00757ccc,
                            (int)*(short *)(param_1 + 0x11e),(int)_UNK_00757cd0,(int)_UNK_00757cd2,
                            (int)_UNK_00757cd4,(int)_UNK_00757cd6,*(undefined1 *)(param_1 + 0x104),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00757cc8,(int)_UNK_00757cca,(int)_UNK_00757ccc,
                            (int)*(short *)(param_1 + 0x11e),(int)_UNK_00757cd0,(int)_UNK_00757cd2,
                            (int)_UNK_00757cd4,(int)_UNK_00757cd6);
      }
    }
    break;
  case 7:
    if (*(char *)(param_1 + 0xea) != '\0') {
      if ((*(char *)(param_1 + 0xea) == '\x01') || (*(char *)(param_1 + 0xea) == '\x03')) {
        local_c._0_1_ = 0x31;
        FUN__text__00505580((int)_UNK_00757cd8,(int)_UNK_00757cda,(int)*(short *)(param_1 + 0x10a),
                            (int)PTR_DAT_00757cdc._2_2_,(int)_UNK_00757ce0,(int)_UNK_00757ce2,
                            (int)_UNK_00757ce4,(int)_UNK_00757ce6,*(undefined1 *)(param_1 + 0x102),
                            0x80,0x80,0x80);
        local_c = CONCAT31(local_c._1_3_,0x32);
        FUN__text__00505580((int)_UNK_00757ce8,(int)_UNK_00757cea,
                            *(short *)(local_8 + 0x10a) + 0x400,(int)_UNK_00757cee,
                            (int)_UNK_00757cf0,(int)_UNK_00757cf2,(int)_UNK_00757cf4,
                            (int)_UNK_00757cf6,*(undefined1 *)(local_8 + 0x102),0x80,0x80,0x80);
      }
      else {
        local_c._0_1_ = 0x31;
        FUN__text__00505000((int)_UNK_00757cd8,(int)_UNK_00757cda,(int)*(short *)(param_1 + 0x10a),
                            (int)PTR_DAT_00757cdc._2_2_,(int)_UNK_00757ce0,(int)_UNK_00757ce2,
                            (int)_UNK_00757ce4,(int)_UNK_00757ce6);
        local_c = CONCAT31(local_c._1_3_,0x32);
        FUN__text__00505000((int)_UNK_00757ce8,(int)_UNK_00757cea,
                            *(short *)(local_8 + 0x10a) + 0x400,(int)_UNK_00757cee,
                            (int)_UNK_00757cf0,(int)_UNK_00757cf2,(int)_UNK_00757cf4,
                            (int)_UNK_00757cf6);
      }
    }
    break;
  case 8:
    if (*(char *)(param_1 + 0xea) != '\0') {
      if (*(char *)(param_1 + 0xea) == '\x01') {
        local_c._0_1_ = 0x35;
        FUN__text__00505580((int)_UNK_00757d18,(int)_UNK_00757d1a,(int)*(short *)(param_1 + 0x10a),
                            (int)PTR_DAT_00757d1c._2_2_,(int)_UNK_00757d20,(int)_UNK_00757d22,
                            (int)_UNK_00757d24,(int)_UNK_00757d26,*(undefined1 *)(param_1 + 0x102),
                            0x80,0x80,0x80);
        local_c = CONCAT31(local_c._1_3_,0x36);
        FUN__text__00505580((int)_UNK_00757d28,(int)_UNK_00757d2a,
                            *(short *)(local_8 + 0x10a) + 0x400,(int)_UNK_00757d2e,
                            (int)_UNK_00757d30,(int)_UNK_00757d32,(int)_UNK_00757d34,
                            (int)_UNK_00757d36,*(undefined1 *)(local_8 + 0x102),0x80,0x80,0x80);
      }
      else {
        local_c._0_1_ = 0x35;
        FUN__text__00505000((int)_UNK_00757d18,(int)_UNK_00757d1a,(int)*(short *)(param_1 + 0x10a),
                            (int)PTR_DAT_00757d1c._2_2_,(int)_UNK_00757d20,(int)_UNK_00757d22,
                            (int)_UNK_00757d24,(int)_UNK_00757d26);
        local_c = CONCAT31(local_c._1_3_,0x36);
        FUN__text__00505000((int)_UNK_00757d28,(int)_UNK_00757d2a,
                            *(short *)(local_8 + 0x10a) + 0x400,(int)_UNK_00757d2e,
                            (int)_UNK_00757d30,(int)_UNK_00757d32,(int)_UNK_00757d34,
                            (int)_UNK_00757d36);
      }
    }
    if (*(char *)(local_8 + 0xeb) != '\0') {
      if (*(char *)(local_8 + 0xeb) == '\x01') {
        local_c = CONCAT31(local_c._1_3_,0x33);
        FUN__text__00505580((int)_UNK_00757cf8,(int)_UNK_00757cfa,(int)_UNK_00757cfc,
                            (int)*(short *)(local_8 + 0x11c),(int)_UNK_00757d00,(int)_UNK_00757d02,
                            (int)_UNK_00757d04,(int)_UNK_00757d06,*(undefined1 *)(local_8 + 0x103),
                            0x80,0x80,0x80);
      }
      else {
        local_c = CONCAT31(local_c._1_3_,0x33);
        FUN__text__00505000((int)_UNK_00757cf8,(int)_UNK_00757cfa,(int)_UNK_00757cfc,
                            (int)*(short *)(local_8 + 0x11c),(int)_UNK_00757d00,(int)_UNK_00757d02,
                            (int)_UNK_00757d04,(int)_UNK_00757d06);
      }
    }
    if (*(char *)(local_8 + 0xec) != '\0') {
      if ((*(char *)(local_8 + 0xec) == '\x01') || (*(char *)(local_8 + 0xec) == '\x03')) {
        local_c = CONCAT31(local_c._1_3_,0x34);
        FUN__text__00505580((int)_UNK_00757d08,(int)_UNK_00757d0a,(int)_UNK_00757d0c,
                            (int)*(short *)(local_8 + 0x11e),(int)_UNK_00757d10,(int)_UNK_00757d12,
                            (int)_UNK_00757d14,(int)_UNK_00757d16,*(undefined1 *)(local_8 + 0x104),
                            0x80,0x80,0x80);
      }
      else {
        local_c = CONCAT31(local_c._1_3_,0x34);
        FUN__text__00505000((int)_UNK_00757d08,(int)_UNK_00757d0a,(int)_UNK_00757d0c,
                            (int)*(short *)(local_8 + 0x11e),(int)_UNK_00757d10,(int)_UNK_00757d12,
                            (int)_UNK_00757d14,(int)_UNK_00757d16);
      }
    }
    if (*(char *)(local_8 + 0xed) != '\0') {
      if ((*(char *)(local_8 + 0xed) == '\x01') || (*(char *)(local_8 + 0xed) == '\x03')) {
        local_c._0_1_ = 0x37;
        FUN__text__00505580((int)_UNK_00757d38,(int)_UNK_00757d3a,(int)*(short *)(local_8 + 0x110),
                            (int)PTR_DAT_00757d3c._2_2_,(int)_UNK_00757d40,(int)_UNK_00757d42,
                            (int)_UNK_00757d44,(int)_UNK_00757d46,*(undefined1 *)(local_8 + 0x105),
                            0x80,0x80,0x80);
        local_c = CONCAT31(local_c._1_3_,0x38);
        FUN__text__00505580((int)_UNK_00757d48,(int)_UNK_00757d4a,
                            *(short *)(local_8 + 0x110) + 0x400,(int)_UNK_00757d4e,
                            (int)_UNK_00757d50,(int)_UNK_00757d52,(int)_UNK_00757d54,
                            (int)_UNK_00757d56,*(undefined1 *)(local_8 + 0x105),0x80,0x80,0x80);
      }
      else {
        local_c._0_1_ = 0x37;
        FUN__text__00505000((int)_UNK_00757d38,(int)_UNK_00757d3a,(int)*(short *)(local_8 + 0x110),
                            (int)PTR_DAT_00757d3c._2_2_,(int)_UNK_00757d40,(int)_UNK_00757d42,
                            (int)_UNK_00757d44,(int)_UNK_00757d46);
        local_c = CONCAT31(local_c._1_3_,0x38);
        FUN__text__00505000((int)_UNK_00757d48,(int)_UNK_00757d4a,
                            *(short *)(local_8 + 0x110) + 0x400,(int)_UNK_00757d4e,
                            (int)_UNK_00757d50,(int)_UNK_00757d52,(int)_UNK_00757d54,
                            (int)_UNK_00757d56);
      }
    }
    break;
  case 9:
    if (*(char *)(param_1 + 0xea) != '\0') {
      local_c = CONCAT31(local_c._1_3_,0x39);
      FUN__text__00505000((int)_UNK_00757d58,(int)_UNK_00757d5a,(int)_UNK_00757d5c,
                          (int)_UNK_00757d5e,(int)_UNK_00757d60,(int)_UNK_00757d62,
                          (int)_UNK_00757d64,(int)_UNK_00757d66);
    }
    break;
  case 10:
    if (*(char *)(param_1 + 0xea) != '\0') {
      local_c = CONCAT31(local_c._1_3_,0x3a);
      FUN__text__00505000((int)_UNK_00757d68,(int)_UNK_00757d6a,(int)_UNK_00757d6c,
                          (int)*(short *)(param_1 + 0x11a),(int)_UNK_00757d70,(int)_UNK_00757d72,
                          (int)_UNK_00757d74,(int)_UNK_00757d76);
    }
    if (*(char *)(local_8 + 0xeb) != '\0') {
      if (*(char *)(local_8 + 0xeb) == '\x03') {
        local_c = CONCAT31(local_c._1_3_,0x3b);
        FUN__text__00505b90((int)_UNK_00757d78,(int)_UNK_00757d7a,(int)_UNK_00757d7c,
                            (int)*(short *)(local_8 + 0x11c),(int)_UNK_00757d80,(int)_UNK_00757d82,
                            0x333,0x2c6,*(undefined1 *)(local_8 + 0x103),0x80,0x80,0x80,
                            (int)_UNK_00757d84,(int)_UNK_00757d86);
      }
      else {
        local_c = CONCAT31(local_c._1_3_,0x3b);
        FUN__text__00505a60((int)_UNK_00757d78,(int)_UNK_00757d7a,(int)_UNK_00757d7c,
                            (int)*(short *)(local_8 + 0x11c),(int)_UNK_00757d80,(int)_UNK_00757d82,
                            0x333,0x2c6,(int)_UNK_00757d84,(int)_UNK_00757d86);
      }
    }
    if (*(char *)(local_8 + 0xec) != '\0') {
      if ((*(char *)(local_8 + 0xec) == '\x01') || (*(char *)(local_8 + 0xec) == '\x03')) {
        local_c = CONCAT31(local_c._1_3_,0x3c);
        FUN__text__00505b90((int)_UNK_00757d88,(int)_UNK_00757d8a,(int)_UNK_00757d8c,
                            (int)*(short *)(local_8 + 0x11e),(int)_UNK_00757d90,(int)_UNK_00757d92,
                            0x333,0x2c6,*(undefined1 *)(local_8 + 0x104),0x80,0x80,0x80,
                            (int)_UNK_00757d94,(int)_UNK_00757d96);
      }
      else {
        local_c = CONCAT31(local_c._1_3_,0x3c);
        FUN__text__00505a60((int)_UNK_00757d88,(int)_UNK_00757d8a,(int)_UNK_00757d8c,
                            (int)*(short *)(local_8 + 0x11e),(int)_UNK_00757d90,(int)_UNK_00757d92,
                            0x333,0x2c6,(int)_UNK_00757d94,(int)_UNK_00757d96);
      }
    }
    break;
  case 0xb:
    if (*(char *)(param_1 + 0xea) != '\0') {
      local_c = CONCAT31(local_c._1_3_,0x3d);
      FUN__text__00505000((int)_UNK_00757d98,(int)_UNK_00757d9a,(int)_UNK_00757d9c,
                          (int)*(short *)(param_1 + 0x11a),(int)_UNK_00757da0,(int)_UNK_00757da2,
                          (int)_UNK_00757da4,(int)_UNK_00757da6);
    }
  }
  local_8 = 0x521741;
  FUN__text__0056ce80();
  return;
}

