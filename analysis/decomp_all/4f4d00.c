
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __fastcall FUN__text__004f4d00(int param_1)

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
        FUN__text__00505580((int)_DAT_00752304,(int)_DAT_00752306,(int)_DAT_00752308,
                            (int)*(short *)(param_1 + 0x11a),(int)_DAT_0075230c,(int)_DAT_0075230e,
                            (int)_DAT_00752310,(int)_DAT_00752312,*(undefined1 *)(param_1 + 0x102),
                            0x80,0x80,0x80);
      }
      else {
        local_c = (uint)local_c._1_3_ << 8;
        FUN__text__00505000((int)_DAT_00752304,(int)_DAT_00752306,(int)_DAT_00752308,
                            (int)*(short *)(param_1 + 0x11a),(int)_DAT_0075230c,(int)_DAT_0075230e,
                            (int)_DAT_00752310,(int)_DAT_00752312);
      }
    }
    if ((*(char *)(local_8 + 0xeb) != '\0') && (*(char *)(local_8 + 0xeb) == '\x01')) {
      local_c = CONCAT31(local_c._1_3_,1);
      while ((local_c & 0xff) < 9) {
        FUN__text__00505000((int)*(short *)(&DAT_00752304 + (local_c & 0xff) * 0x10),
                            (int)*(short *)(&DAT_00752306 + (local_c & 0xff) * 0x10),
                            (int)*(short *)(&DAT_00752308 + (local_c & 0xff) * 0x10),
                            (int)*(short *)(local_8 + 0x11c) +
                            (uint)*(ushort *)(&DAT_0075327c + (local_c & 0xff) * 2),
                            (int)*(short *)(&DAT_0075230c + (local_c & 0xff) * 0x10),
                            (int)*(short *)(&DAT_0075230e + (local_c & 0xff) * 0x10),
                            (int)*(short *)(&DAT_00752310 + (local_c & 0xff) * 0x10),
                            (int)*(short *)(&DAT_00752312 + (local_c & 0xff) * 0x10));
        local_c = CONCAT31(local_c._1_3_,(char)local_c + '\x01');
      }
    }
    if ((*(char *)(local_8 + 0xec) != '\0') && (*(char *)(local_8 + 0xec) == '\x01')) {
      local_c = CONCAT31(local_c._1_3_,9);
      while ((local_c & 0xff) < 0xe) {
        FUN__text__00505000((int)*(short *)(&DAT_00752304 + (local_c & 0xff) * 0x10),
                            (int)*(short *)(&DAT_00752306 + (local_c & 0xff) * 0x10),
                            (int)*(short *)(&DAT_00752308 + (local_c & 0xff) * 0x10),
                            (int)*(short *)(local_8 + 0x11e) +
                            (uint)*(ushort *)(&DAT_0075327c + (local_c & 0xff) * 2),
                            (int)*(short *)(&DAT_0075230c + (local_c & 0xff) * 0x10),
                            (int)*(short *)(&DAT_0075230e + (local_c & 0xff) * 0x10),
                            (int)*(short *)(&DAT_00752310 + (local_c & 0xff) * 0x10),
                            (int)*(short *)(&DAT_00752312 + (local_c & 0xff) * 0x10));
        local_c = CONCAT31(local_c._1_3_,(char)local_c + '\x01');
      }
    }
    if ((*(char *)(local_8 + 0xed) != '\0') && (*(char *)(local_8 + 0xed) == '\x01')) {
      local_c = CONCAT31(local_c._1_3_,0xe);
      FUN__text__00505580((int)_UNK_007523e4,(int)_UNK_007523e6,(int)_UNK_007523e8,
                          (int)*(short *)(local_8 + 0x120),(int)_UNK_007523ec,(int)_UNK_007523ee,
                          (int)_UNK_007523f0,(int)_UNK_007523f2,*(undefined1 *)(local_8 + 0x105),
                          0x80,0x80,0x80);
    }
    if (*(char *)(local_8 + 0xee) != '\0') {
      if (*(char *)(local_8 + 0xee) == '\x01') {
        local_c = CONCAT31(local_c._1_3_,0xf);
        FUN__text__00505580((int)_UNK_007523f4,(int)_UNK_007523f6,(int)_UNK_007523f8,
                            (int)*(short *)(local_8 + 0x122),(int)_UNK_007523fc,(int)_UNK_007523fe,
                            (int)_UNK_00752400,(int)_UNK_00752402,*(undefined1 *)(local_8 + 0x106),
                            0x80,0x80,0x80);
      }
      else {
        local_c = CONCAT31(local_c._1_3_,0xf);
        FUN__text__00505000((int)_UNK_007523f4,(int)_UNK_007523f6,(int)_UNK_007523f8,
                            (int)*(short *)(local_8 + 0x122),(int)_UNK_007523fc,(int)_UNK_007523fe,
                            (int)_UNK_00752400,(int)_UNK_00752402);
      }
    }
    if (*(char *)(local_8 + 0xef) != '\0') {
      if (*(char *)(local_8 + 0xef) == '\x01') {
        local_c = CONCAT31(local_c._1_3_,0x10);
        FUN__text__00505580((int)_UNK_00752404,(int)_UNK_00752406,(int)_UNK_00752408,
                            (int)*(short *)(local_8 + 0x124),(int)_UNK_0075240c,(int)_UNK_0075240e,
                            (int)_UNK_00752410,(int)_UNK_00752412,*(undefined1 *)(local_8 + 0x107),
                            0x80,0x80,0x80);
      }
      else {
        local_c = CONCAT31(local_c._1_3_,0x10);
        FUN__text__00505000((int)_UNK_00752404,(int)_UNK_00752406,(int)_UNK_00752408,
                            (int)*(short *)(local_8 + 0x124),(int)_UNK_0075240c,(int)_UNK_0075240e,
                            (int)_UNK_00752410,(int)_UNK_00752412);
      }
    }
    break;
  case 1:
    if (*(char *)(param_1 + 0xea) != '\0') {
      local_c = CONCAT31(local_c._1_3_,0x20);
      FUN__text__00505580((int)_UNK_00752504,(int)_UNK_00752506,(int)_UNK_00752508,
                          (int)_UNK_0075250a,(int)_UNK_0075250c,(int)_UNK_0075250e,
                          (int)_UNK_00752510,(int)_UNK_00752512,*(undefined1 *)(param_1 + 0x102),
                          0x80,0x80,0x80);
    }
    if (*(char *)(local_8 + 0xeb) != '\0') {
      local_c = CONCAT31(local_c._1_3_,0x21);
      FUN__text__00505580((int)_UNK_00752514,(int)_UNK_00752516,(int)_UNK_00752518,
                          (int)_UNK_0075251a,(int)_UNK_0075251c,(int)_UNK_0075251e,
                          (int)_UNK_00752520,(int)_UNK_00752522,*(undefined1 *)(local_8 + 0x103),
                          0x80,0x80,0x80);
    }
    if (*(char *)(local_8 + 0xec) != '\0') {
      local_c = CONCAT31(local_c._1_3_,0x24);
      FUN__text__00505580((int)_UNK_00752544,(int)_UNK_00752546,(int)_UNK_00752548,
                          (int)_UNK_0075254a,(int)_UNK_0075254c,(int)_UNK_0075254e,
                          (int)_UNK_00752550,(int)_UNK_00752552,*(undefined1 *)(local_8 + 0x104),
                          0x80,0x80,0x80);
    }
    if (*(char *)(local_8 + 0xed) != '\0') {
      local_c = CONCAT31(local_c._1_3_,0x22);
      FUN__text__00505580((int)_UNK_00752524,(int)_UNK_00752526,(int)_UNK_00752528,
                          (int)_UNK_0075252a,(int)_UNK_0075252c,(int)_UNK_0075252e,
                          (int)_UNK_00752530,(int)_UNK_00752532,*(undefined1 *)(local_8 + 0x105),
                          0x80,0x80,0x80);
    }
    if (*(char *)(local_8 + 0xee) != '\0') {
      local_c = CONCAT31(local_c._1_3_,0x25);
      FUN__text__00505580((int)_UNK_00752554,(int)_UNK_00752556,(int)_UNK_00752558,
                          (int)_UNK_0075255a,(int)_UNK_0075255c,(int)_UNK_0075255e,
                          (int)_UNK_00752560,(int)_UNK_00752562,*(undefined1 *)(local_8 + 0x106),
                          0x80,0x80,0x80);
    }
    if (*(char *)(local_8 + 0xef) != '\0') {
      local_c = CONCAT31(local_c._1_3_,0x23);
      FUN__text__00505580((int)_UNK_00752534,(int)_UNK_00752536,(int)_UNK_00752538,
                          (int)_UNK_0075253a,(int)_UNK_0075253c,(int)_UNK_0075253e,
                          (int)_UNK_00752540,(int)_UNK_00752542,*(undefined1 *)(local_8 + 0x107),
                          0x80,0x80,0x80);
    }
    if (*(char *)(local_8 + 0xf0) != '\0') {
      local_c = CONCAT31(local_c._1_3_,0x26);
      FUN__text__00505580((int)_UNK_00752564,(int)_UNK_00752566,(int)_UNK_00752568,
                          (int)_UNK_0075256a,(int)_UNK_0075256c,(int)_UNK_0075256e,
                          (int)_UNK_00752570,(int)_UNK_00752572,*(undefined1 *)(local_8 + 0x108),
                          0x80,0x80,0x80);
    }
    if (*(char *)(local_8 + 0xf1) != '\0') {
      local_c = CONCAT31(local_c._1_3_,0x27);
      if (*(char *)(local_8 + 0xf1) == '\x01') {
        FUN__text__00505580((int)_UNK_00752574,(int)_UNK_00752576,(int)_UNK_00752578,
                            (int)_UNK_0075257a,(int)_UNK_0075257c,(int)_UNK_0075257e,
                            (int)_UNK_00752580,(int)_UNK_00752582,*(undefined1 *)(local_8 + 0x109),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00752574,(int)_UNK_00752576,(int)_UNK_00752578,
                            (int)_UNK_0075257a,(int)_UNK_0075257c,(int)_UNK_0075257e,
                            (int)_UNK_00752580,(int)_UNK_00752582);
      }
    }
    break;
  case 2:
    if (*(char *)(param_1 + 0xf1) != '\0') {
      local_c = CONCAT31(local_c._1_3_,0x27);
      FUN__text__00505000((int)_UNK_00752574,(int)_UNK_00752576,(int)_UNK_00752578,
                          (int)_UNK_0075257a,(int)_UNK_0075257c,(int)_UNK_0075257e,
                          (int)_UNK_00752580,(int)_UNK_00752582);
    }
    if (*(char *)(local_8 + 0xea) != '\0') {
      local_c = CONCAT31(local_c._1_3_,0x28);
      if ((*(char *)(local_8 + 0xea) == '\x01') || (*(char *)(local_8 + 0xea) == '\x03')) {
        FUN__text__00505580((int)_UNK_00752584,(int)_UNK_00752586,(int)*(short *)(local_8 + 0x10a),
                            (int)PTR_DAT_00752588._2_2_,(int)_UNK_0075258c,(int)_UNK_0075258e,
                            (int)_UNK_00752590,(int)_UNK_00752592,*(undefined1 *)(local_8 + 0x102),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00752584,(int)_UNK_00752586,(int)*(short *)(local_8 + 0x10a),
                            (int)PTR_DAT_00752588._2_2_,(int)_UNK_0075258c,(int)_UNK_0075258e,
                            (int)_UNK_00752590,(int)_UNK_00752592);
      }
    }
    if (*(char *)(local_8 + 0xeb) != '\0') {
      local_c = CONCAT31(local_c._1_3_,0x29);
      if ((*(char *)(local_8 + 0xeb) == '\x01') || (*(char *)(local_8 + 0xeb) == '\x03')) {
        FUN__text__00505580((int)_UNK_00752594,(int)_UNK_00752596,(int)*(short *)(local_8 + 0x10c),
                            (int)PTR_DAT_00752598._2_2_,(int)_UNK_0075259c,(int)_UNK_0075259e,
                            (int)_UNK_007525a0,(int)_UNK_007525a2,*(undefined1 *)(local_8 + 0x103),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00752594,(int)_UNK_00752596,(int)*(short *)(local_8 + 0x10c),
                            (int)PTR_DAT_00752598._2_2_,(int)_UNK_0075259c,(int)_UNK_0075259e,
                            (int)_UNK_007525a0,(int)_UNK_007525a2);
      }
    }
    break;
  case 3:
    if (*(char *)(param_1 + 0xeb) != '\0') {
      local_c = CONCAT31(local_c._1_3_,0x29);
      if ((*(char *)(param_1 + 0xeb) == '\x01') || (*(char *)(param_1 + 0xeb) == '\x03')) {
        FUN__text__00505580((int)_UNK_00752594,(int)_UNK_00752596,(int)*(short *)(param_1 + 0x10c),
                            (int)PTR_DAT_00752598._2_2_,(int)_UNK_0075259c,(int)_UNK_0075259e,
                            (int)_UNK_007525a0,(int)_UNK_007525a2,*(undefined1 *)(param_1 + 0x103),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00752594,(int)_UNK_00752596,(int)*(short *)(param_1 + 0x10c),
                            (int)PTR_DAT_00752598._2_2_,(int)_UNK_0075259c,(int)_UNK_0075259e,
                            (int)_UNK_007525a0,(int)_UNK_007525a2);
      }
    }
    if (*(char *)(local_8 + 0xea) != '\0') {
      local_c = CONCAT31(local_c._1_3_,0x2a);
      FUN__text__00505000((int)_UNK_007525a4,(int)_UNK_007525a6,(int)*(short *)(local_8 + 0x10a),
                          (int)PTR_DAT_007525a8._2_2_,(int)_UNK_007525ac,(int)_UNK_007525ae,
                          (int)_UNK_007525b0,(int)_UNK_007525b2);
    }
    break;
  case 4:
    if (*(char *)(param_1 + 0xea) != '\0') {
      local_c = CONCAT31(local_c._1_3_,0x2c);
      if ((*(char *)(param_1 + 0xea) == '\x01') || (*(char *)(param_1 + 0xea) == '\x03')) {
        FUN__text__00505580((int)_UNK_007525c4,(int)_UNK_007525c6,(int)_UNK_007525c8,
                            (int)*(short *)(param_1 + 0x11a),(int)_UNK_007525cc,(int)_UNK_007525ce,
                            (int)_UNK_007525d0,(int)_UNK_007525d2,*(undefined1 *)(param_1 + 0x102),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_007525c4,(int)_UNK_007525c6,(int)_UNK_007525c8,
                            (int)*(short *)(param_1 + 0x11a),(int)_UNK_007525cc,(int)_UNK_007525ce,
                            (int)_UNK_007525d0,(int)_UNK_007525d2);
      }
    }
    if (*(char *)(local_8 + 0xeb) != '\0') {
      local_c = CONCAT31(local_c._1_3_,0x2d);
      if ((*(char *)(local_8 + 0xeb) == '\x01') || (*(char *)(local_8 + 0xeb) == '\x03')) {
        FUN__text__00505580((int)_UNK_007525d4,(int)_UNK_007525d6,(int)_UNK_007525d8,
                            (int)*(short *)(local_8 + 0x11c),(int)_UNK_007525dc,(int)_UNK_007525de,
                            (int)_UNK_007525e0,(int)_UNK_007525e2,*(undefined1 *)(local_8 + 0x103),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_007525d4,(int)_UNK_007525d6,(int)_UNK_007525d8,
                            (int)*(short *)(local_8 + 0x11c),(int)_UNK_007525dc,(int)_UNK_007525de,
                            (int)_UNK_007525e0,(int)_UNK_007525e2);
      }
    }
    if (*(char *)(local_8 + 0xec) != '\0') {
      local_c = CONCAT31(local_c._1_3_,0x2e);
      if ((*(char *)(local_8 + 0xec) == '\x01') || (*(char *)(local_8 + 0xec) == '\x03')) {
        FUN__text__00505580((int)_UNK_007525e4,(int)_UNK_007525e6,(int)_UNK_007525e8,
                            (int)*(short *)(local_8 + 0x11e),(int)_UNK_007525ec,(int)_UNK_007525ee,
                            (int)_UNK_007525f0,(int)_UNK_007525f2,*(undefined1 *)(local_8 + 0x104),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_007525e4,(int)_UNK_007525e6,(int)_UNK_007525e8,
                            (int)*(short *)(local_8 + 0x11e),(int)_UNK_007525ec,(int)_UNK_007525ee,
                            (int)_UNK_007525f0,(int)_UNK_007525f2);
      }
    }
    if (*(char *)(local_8 + 0xed) != '\0') {
      local_c = CONCAT31(local_c._1_3_,0x2f);
      if (*(char *)(local_8 + 0xed) == '\x03') {
        FUN__text__00505580((int)_UNK_007525f4,(int)_UNK_007525f6,(int)_UNK_007525f8,
                            (int)*(short *)(local_8 + 0x120),(int)_UNK_007525fc,(int)_UNK_007525fe,
                            (int)_UNK_00752600,(int)_UNK_00752602,*(undefined1 *)(local_8 + 0x105),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_007525f4,(int)_UNK_007525f6,(int)_UNK_007525f8,
                            (int)*(short *)(local_8 + 0x120),(int)_UNK_007525fc,(int)_UNK_007525fe,
                            (int)_UNK_00752600,(int)_UNK_00752602);
      }
    }
    break;
  case 5:
    if (*(char *)(param_1 + 0xed) != '\0') {
      local_c = CONCAT31(local_c._1_3_,0x2f);
      if (*(char *)(param_1 + 0xed) == '\x03') {
        FUN__text__00505580((int)_UNK_007525f4,(int)_UNK_007525f6,(int)_UNK_007525f8,
                            (int)*(short *)(param_1 + 0x120),(int)_UNK_007525fc,(int)_UNK_007525fe,
                            (int)_UNK_00752600,(int)_UNK_00752602,*(undefined1 *)(param_1 + 0x105),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_007525f4,(int)_UNK_007525f6,(int)_UNK_007525f8,
                            (int)*(short *)(param_1 + 0x120),(int)_UNK_007525fc,(int)_UNK_007525fe,
                            (int)_UNK_00752600,(int)_UNK_00752602);
      }
    }
    if (*(char *)(local_8 + 0xea) != '\0') {
      local_c = CONCAT31(local_c._1_3_,0x2b);
      FUN__text__00505580((int)_UNK_007525b4,(int)_UNK_007525b6,(int)_UNK_007525b8,
                          (int)_UNK_007525ba,(int)_UNK_007525bc,(int)_UNK_007525be,
                          (int)_UNK_007525c0,(int)_UNK_007525c2,*(undefined1 *)(local_8 + 0x102),
                          0x80,0x80,0x80);
    }
    if (*(char *)(local_8 + 0xeb) != '\0') {
      local_c = CONCAT31(local_c._1_3_,0x25);
      if ((*(char *)(local_8 + 0xeb) == '\x01') || (*(char *)(local_8 + 0xeb) == '\x03')) {
        FUN__text__00505580((int)_UNK_00752554,(int)_UNK_00752556,(int)_UNK_00752558,
                            (int)_UNK_0075255a,(int)_UNK_0075255c,(int)_UNK_0075255e,
                            (int)_UNK_00752560,(int)_UNK_00752562,*(undefined1 *)(local_8 + 0x103),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00752554,(int)_UNK_00752556,(int)_UNK_00752558,
                            (int)_UNK_0075255a,(int)_UNK_0075255c,(int)_UNK_0075255e,
                            (int)_UNK_00752560,(int)_UNK_00752562);
      }
    }
    if (*(char *)(local_8 + 0xec) != '\0') {
      local_c = CONCAT31(local_c._1_3_,0x30);
      if ((*(char *)(local_8 + 0xec) == '\x01') || (*(char *)(local_8 + 0xec) == '\x03')) {
        FUN__text__00505580((int)_UNK_00752604,(int)_UNK_00752606,(int)_UNK_00752608,
                            (int)*(short *)(local_8 + 0x11e),(int)_UNK_0075260c,(int)_UNK_0075260e,
                            (int)_UNK_00752610,(int)_UNK_00752612,*(undefined1 *)(local_8 + 0x104),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00752604,(int)_UNK_00752606,(int)_UNK_00752608,
                            (int)*(short *)(local_8 + 0x11e),(int)_UNK_0075260c,(int)_UNK_0075260e,
                            (int)_UNK_00752610,(int)_UNK_00752612);
      }
    }
    break;
  case 6:
    if (*(char *)(param_1 + 0xec) != '\0') {
      local_c = CONCAT31(local_c._1_3_,0x30);
      if ((*(char *)(param_1 + 0xec) == '\x01') || (*(char *)(param_1 + 0xec) == '\x03')) {
        FUN__text__00505580((int)_UNK_00752604,(int)_UNK_00752606,(int)_UNK_00752608,
                            (int)*(short *)(param_1 + 0x11e),(int)_UNK_0075260c,(int)_UNK_0075260e,
                            (int)_UNK_00752610,(int)_UNK_00752612,*(undefined1 *)(param_1 + 0x104),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00752604,(int)_UNK_00752606,(int)_UNK_00752608,
                            (int)*(short *)(param_1 + 0x11e),(int)_UNK_0075260c,(int)_UNK_0075260e,
                            (int)_UNK_00752610,(int)_UNK_00752612);
      }
    }
    break;
  case 7:
    if (*(char *)(param_1 + 0xea) != '\0') {
      local_c = CONCAT31(local_c._1_3_,0x41);
      if ((*(char *)(param_1 + 0xea) == '\x01') || (*(char *)(param_1 + 0xea) == '\x03')) {
        FUN__text__00505580((int)_UNK_00752714,(int)_UNK_00752716,(int)_UNK_00752718,
                            (int)*(short *)(param_1 + 0x11a),(int)_UNK_0075271c,(int)_UNK_0075271e,
                            (int)_UNK_00752720,(int)_UNK_00752722,*(undefined1 *)(param_1 + 0x102),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00752714,(int)_UNK_00752716,(int)_UNK_00752718,
                            (int)*(short *)(param_1 + 0x11a),(int)_UNK_0075271c,(int)_UNK_0075271e,
                            (int)_UNK_00752720,(int)_UNK_00752722);
      }
    }
  }
  local_8 = 0x4f7195;
  FUN__text__0056ce80();
  return;
}

