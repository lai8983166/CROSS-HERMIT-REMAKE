
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __fastcall FUN__text__0050d5a0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  int local_10;
  undefined1 local_c;
  undefined3 uStack_b;
  int local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_10 = *(byte *)(param_1 + 0x34) - 2;
  local_8 = param_1;
  switch(local_10) {
  case 0:
    if (*(char *)(param_1 + 0x39) != '\0') {
      _local_c = CONCAT31(uStack_b,0x89);
      FUN__text__00505580((int)_UNK_00758638,(int)_UNK_0075863a,(int)_UNK_0075863c,
                          (int)_UNK_0075863e,(int)_UNK_00758640,(int)_UNK_00758642,
                          (int)_UNK_00758644,(int)_UNK_00758646,*(undefined1 *)(param_1 + 0x69),0x80
                          ,0x80,0x80);
    }
    if (*(char *)(local_8 + 0x3a) != '\0') {
      _local_c = CONCAT31(uStack_b,0xa1);
      FUN__text__00505580((int)_UNK_007587b8,(int)_UNK_007587ba,(int)_UNK_007587bc,
                          (int)_UNK_007587be,(int)_UNK_007587c0,(int)_UNK_007587c2,
                          (int)_UNK_007587c4,(int)_UNK_007587c6,*(undefined1 *)(local_8 + 0x6a),0x80
                          ,0x80,0x80);
    }
    if (*(char *)(local_8 + 0x3b) != '\0') {
      _local_c = CONCAT31(uStack_b,0xa2);
      FUN__text__00505580((int)_UNK_007587c8,(int)_UNK_007587ca,(int)_UNK_007587cc,
                          (int)_UNK_007587ce,(int)_UNK_007587d0,(int)_UNK_007587d2,
                          (int)_UNK_007587d4,(int)_UNK_007587d6,*(undefined1 *)(local_8 + 0x6b),0x80
                          ,0x80,0x80);
    }
    if (*(char *)(local_8 + 0x3c) != '\0') {
      _local_c = CONCAT31(uStack_b,0xa3);
      FUN__text__00505580((int)_UNK_007587d8,(int)_UNK_007587da,(int)_UNK_007587dc,
                          (int)_UNK_007587de,(int)_UNK_007587e0,(int)_UNK_007587e2,
                          (int)_UNK_007587e4,(int)_UNK_007587e6,*(undefined1 *)(local_8 + 0x6c),0x80
                          ,0x80,0x80);
    }
    break;
  case 1:
    if (*(char *)(param_1 + 0x39) != '\0') {
      _local_c = CONCAT31(uStack_b,0x6d);
      if ((*(char *)(param_1 + 0x39) == '\x01') || (*(char *)(param_1 + 0x39) == '\x03')) {
        FUN__text__00505580((int)_UNK_00758478,(int)_UNK_0075847a,(int)*(short *)(param_1 + 0x82),
                            (int)*(short *)(param_1 + 0x9c),(int)_UNK_00758480,(int)_UNK_00758482,
                            (int)_UNK_00758484,(int)_UNK_00758486,*(undefined1 *)(param_1 + 0x69),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00758478,(int)_UNK_0075847a,(int)*(short *)(param_1 + 0x82),
                            (int)*(short *)(param_1 + 0x9c),(int)_UNK_00758480,(int)_UNK_00758482,
                            (int)_UNK_00758484,(int)_UNK_00758486);
      }
    }
    if (*(char *)(local_8 + 0x3a) != '\0') {
      _local_c = CONCAT31(uStack_b,0x77);
      if ((*(char *)(local_8 + 0x3a) == '\x01') || (*(char *)(local_8 + 0x3a) == '\x03')) {
        FUN__text__00505580((int)_UNK_00758518,(int)_UNK_0075851a,(int)*(short *)(local_8 + 0x84),
                            (int)*(short *)(local_8 + 0x9e),(int)_UNK_00758520,(int)_UNK_00758522,
                            (int)_UNK_00758524,(int)_UNK_00758526,*(undefined1 *)(local_8 + 0x6a),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00758518,(int)_UNK_0075851a,(int)*(short *)(local_8 + 0x84),
                            (int)*(short *)(local_8 + 0x9e),(int)_UNK_00758520,(int)_UNK_00758522,
                            (int)_UNK_00758524,(int)_UNK_00758526);
      }
    }
    break;
  case 2:
    if (*(char *)(param_1 + 0x39) != '\0') {
      if ((*(char *)(param_1 + 0x39) == '\x01') || (*(char *)(param_1 + 0x39) == '\x03')) {
        local_c = 0x78;
        FUN__text__00505580((int)_UNK_00758528,(int)_UNK_0075852a,(int)*(short *)(param_1 + 0x82),
                            (int)*(short *)(param_1 + 0x9c),(int)_UNK_00758530,(int)_UNK_00758532,
                            (int)_UNK_00758534,(int)_UNK_00758536,*(undefined1 *)(param_1 + 0x69),
                            0x80,0x80,0x80);
        _local_c = CONCAT31(uStack_b,0x72);
        FUN__text__00505580((int)_UNK_007584c8,(int)_UNK_007584ca,*(short *)(local_8 + 0x82) + 0x400
                            ,*(short *)(local_8 + 0x9c) + 2,(int)_UNK_007584d0,(int)_UNK_007584d2,
                            (int)_UNK_007584d4,(int)_UNK_007584d6,*(undefined1 *)(local_8 + 0x69),
                            0x80,0x80,0x80);
      }
      else {
        local_c = 0x78;
        FUN__text__00505000((int)_UNK_00758528,(int)_UNK_0075852a,(int)*(short *)(param_1 + 0x82),
                            (int)*(short *)(param_1 + 0x9c),(int)_UNK_00758530,(int)_UNK_00758532,
                            (int)_UNK_00758534,(int)_UNK_00758536);
        _local_c = CONCAT31(uStack_b,0x72);
        FUN__text__00505000((int)_UNK_007584c8,(int)_UNK_007584ca,*(short *)(local_8 + 0x82) + 0x400
                            ,*(short *)(local_8 + 0x9c) + 2,(int)_UNK_007584d0,(int)_UNK_007584d2,
                            (int)_UNK_007584d4,(int)_UNK_007584d6);
      }
    }
    if (*(char *)(local_8 + 0x3a) != '\0') {
      _local_c = CONCAT31(uStack_b,0x75);
      if ((*(char *)(local_8 + 0x3a) == '\x01') || (*(char *)(local_8 + 0x3a) == '\x03')) {
        FUN__text__00505580((int)_UNK_007584f8,(int)_UNK_007584fa,(int)*(short *)(local_8 + 0x84),
                            (int)*(short *)(local_8 + 0x9e),(int)_UNK_00758500,(int)_UNK_00758502,
                            (int)_UNK_00758504,(int)_UNK_00758506,*(undefined1 *)(local_8 + 0x6a),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_007584f8,(int)_UNK_007584fa,(int)*(short *)(local_8 + 0x84),
                            (int)*(short *)(local_8 + 0x9e),(int)_UNK_00758500,(int)_UNK_00758502,
                            (int)_UNK_00758504,(int)_UNK_00758506);
      }
    }
    break;
  case 3:
    if (*(char *)(param_1 + 0x39) != '\0') {
      _local_c = CONCAT31(uStack_b,100);
      FUN__text__00505580((int)_UNK_007583e8,(int)_UNK_007583ea,(int)*(short *)(param_1 + 0x82),
                          (int)PTR_DAT_007583ec._2_2_,(int)_UNK_007583f0,(int)_UNK_007583f2,
                          (int)_UNK_007583f4,(int)_UNK_007583f6,*(undefined1 *)(param_1 + 0x69),0x80
                          ,0x80,0x80);
    }
    if (*(char *)(local_8 + 0x3a) != '\0') {
      _local_c = CONCAT31(uStack_b,0x65);
      FUN__text__00505580((int)_UNK_007583f8,(int)_UNK_007583fa,(int)*(short *)(local_8 + 0x84),
                          (int)PTR_DAT_007583fc._2_2_,(int)_UNK_00758400,(int)_UNK_00758402,
                          (int)_UNK_00758404,(int)_UNK_00758406,*(undefined1 *)(local_8 + 0x6a),0x80
                          ,0x80,0x80);
    }
    if (*(char *)(local_8 + 0x3b) != '\0') {
      _local_c = CONCAT31(uStack_b,0x66);
      FUN__text__00505580((int)_UNK_00758408,(int)_UNK_0075840a,(int)*(short *)(local_8 + 0x86),
                          (int)PTR_DAT_0075840c._2_2_,(int)_UNK_00758410,(int)_UNK_00758412,
                          (int)_UNK_00758414,(int)_UNK_00758416,*(undefined1 *)(local_8 + 0x6b),0x80
                          ,0x80,0x80);
    }
    if (*(char *)(local_8 + 0x3c) != '\0') {
      _local_c = CONCAT31(uStack_b,0x67);
      FUN__text__00505580((int)_UNK_00758418,(int)_UNK_0075841a,(int)*(short *)(local_8 + 0x88),
                          (int)PTR_DAT_0075841c._2_2_,(int)_UNK_00758420,(int)_UNK_00758422,
                          (int)_UNK_00758424,(int)_UNK_00758426,*(undefined1 *)(local_8 + 0x6c),0x80
                          ,0x80,0x80);
    }
    if (*(char *)(local_8 + 0x3d) != '\0') {
      _local_c = CONCAT31(uStack_b,0x68);
      FUN__text__00505580((int)_UNK_00758428,(int)_UNK_0075842a,(int)*(short *)(local_8 + 0x8a),
                          (int)PTR_DAT_0075842c._2_2_,(int)_UNK_00758430,(int)_UNK_00758432,
                          (int)_UNK_00758434,(int)_UNK_00758436,*(undefined1 *)(local_8 + 0x6d),0x80
                          ,0x80,0x80);
    }
    if (*(char *)(local_8 + 0x3e) != '\0') {
      _local_c = CONCAT31(uStack_b,0x69);
      FUN__text__00505580((int)_UNK_00758438,(int)_UNK_0075843a,(int)*(short *)(local_8 + 0x8c),
                          (int)PTR_DAT_0075843c._2_2_,(int)_UNK_00758440,(int)_UNK_00758442,
                          (int)_UNK_00758444,(int)_UNK_00758446,*(undefined1 *)(local_8 + 0x6e),0x80
                          ,0x80,0x80);
    }
    if (*(char *)(local_8 + 0x3f) != '\0') {
      _local_c = CONCAT31(uStack_b,0x6a);
      FUN__text__00505580((int)_UNK_00758448,(int)_UNK_0075844a,(int)*(short *)(local_8 + 0x8e),
                          (int)PTR_DAT_0075844c._2_2_,(int)_UNK_00758450,(int)_UNK_00758452,
                          (int)_UNK_00758454,(int)_UNK_00758456,*(undefined1 *)(local_8 + 0x6f),0x80
                          ,0x80,0x80);
    }
    if (*(char *)(local_8 + 0x40) != '\0') {
      _local_c = CONCAT31(uStack_b,0x6b);
      FUN__text__00505580((int)_UNK_00758458,(int)_UNK_0075845a,(int)*(short *)(local_8 + 0x90),
                          (int)PTR_DAT_0075845c._2_2_,(int)_UNK_00758460,(int)_UNK_00758462,
                          (int)_UNK_00758464,(int)_UNK_00758466,*(undefined1 *)(local_8 + 0x70),0x80
                          ,0x80,0x80);
    }
    break;
  case 4:
    if (*(char *)(param_1 + 0x39) != '\0') {
      _local_c = CONCAT31(uStack_b,0x49);
      if ((*(char *)(param_1 + 0x39) == '\x01') || (*(char *)(param_1 + 0x39) == '\x03')) {
        FUN__text__00505580((int)_UNK_00758238,(int)_UNK_0075823a,(int)_UNK_0075823c,
                            (int)*(short *)(param_1 + 0x9c),(int)_UNK_00758240,(int)_UNK_00758242,
                            (int)_UNK_00758244,(int)_UNK_00758246,*(undefined1 *)(param_1 + 0x69),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00758238,(int)_UNK_0075823a,(int)_UNK_0075823c,
                            (int)*(short *)(param_1 + 0x9c),(int)_UNK_00758240,(int)_UNK_00758242,
                            (int)_UNK_00758244,(int)_UNK_00758246);
      }
    }
    break;
  case 5:
    if (*(char *)(param_1 + 0x39) != '\0') {
      _local_c = CONCAT31(uStack_b,0x76);
      if ((*(char *)(param_1 + 0x39) == '\x01') || (*(char *)(param_1 + 0x39) == '\x03')) {
        FUN__text__00505580((int)_UNK_00758508,(int)_UNK_0075850a,(int)*(short *)(param_1 + 0x82),
                            (int)*(short *)(param_1 + 0x9c),(int)_UNK_00758510,(int)_UNK_00758512,
                            (int)_UNK_00758514,(int)_UNK_00758516,*(undefined1 *)(param_1 + 0x69),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00758508,(int)_UNK_0075850a,(int)*(short *)(param_1 + 0x82),
                            (int)*(short *)(param_1 + 0x9c),(int)_UNK_00758510,(int)_UNK_00758512,
                            (int)_UNK_00758514,(int)_UNK_00758516);
      }
    }
    if (*(char *)(local_8 + 0x3a) != '\0') {
      _local_c = CONCAT31(uStack_b,0x73);
      if ((*(char *)(local_8 + 0x3a) == '\x01') || (*(char *)(local_8 + 0x3a) == '\x03')) {
        FUN__text__00505580((int)_UNK_007584d8,(int)_UNK_007584da,(int)*(short *)(local_8 + 0x84),
                            (int)_UNK_007584de,(int)_UNK_007584e0,(int)_UNK_007584e2,
                            (int)_UNK_007584e4,(int)_UNK_007584e6,*(undefined1 *)(local_8 + 0x6a),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_007584d8,(int)_UNK_007584da,(int)*(short *)(local_8 + 0x84),
                            (int)_UNK_007584de,(int)_UNK_007584e0,(int)_UNK_007584e2,
                            (int)_UNK_007584e4,(int)_UNK_007584e6);
      }
    }
    if (*(char *)(local_8 + 0x3d) != '\0') {
      _local_c = CONCAT31(uStack_b,0x74);
      if ((*(char *)(local_8 + 0x3d) == '\x01') || (*(char *)(local_8 + 0x3d) == '\x03')) {
        FUN__text__00505580((int)_UNK_007584e8,(int)_UNK_007584ea,(int)*(short *)(local_8 + 0x8a),
                            (int)*(short *)(local_8 + 0xa4),(int)_UNK_007584f0,(int)_UNK_007584f2,
                            (int)_UNK_007584f4,(int)_UNK_007584f6,*(undefined1 *)(local_8 + 0x6d),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_007584e8,(int)_UNK_007584ea,(int)*(short *)(local_8 + 0x8a),
                            (int)*(short *)(local_8 + 0xa4),(int)_UNK_007584f0,(int)_UNK_007584f2,
                            (int)_UNK_007584f4,(int)_UNK_007584f6);
      }
    }
    if (*(char *)(local_8 + 0x3e) != '\0') {
      _local_c = CONCAT31(uStack_b,0x6c);
      if ((*(char *)(local_8 + 0x3e) == '\x01') || (*(char *)(local_8 + 0x3e) == '\x03')) {
        FUN__text__00505580((int)_UNK_00758468,(int)_UNK_0075846a,(int)*(short *)(local_8 + 0x8c),
                            (int)_UNK_0075846e,(int)_UNK_00758470,(int)_UNK_00758472,
                            (int)_UNK_00758474,(int)_UNK_00758476,*(undefined1 *)(local_8 + 0x6e),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00758468,(int)_UNK_0075846a,(int)*(short *)(local_8 + 0x8c),
                            (int)_UNK_0075846e,(int)_UNK_00758470,(int)_UNK_00758472,
                            (int)_UNK_00758474,(int)_UNK_00758476);
      }
    }
    break;
  case 6:
    if (*(char *)(param_1 + 0x3a) != '\0') {
      _local_c = CONCAT31(uStack_b,0x79);
      if ((*(char *)(param_1 + 0x3a) == '\x01') || (*(char *)(param_1 + 0x3a) == '\x03')) {
        FUN__text__00505580((int)_UNK_00758538,(int)_UNK_0075853a,(int)*(short *)(param_1 + 0x84),
                            (int)*(short *)(param_1 + 0x9e),(int)_UNK_00758540,(int)_UNK_00758542,
                            (int)_UNK_00758544,(int)_UNK_00758546,*(undefined1 *)(param_1 + 0x6a),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00758538,(int)_UNK_0075853a,(int)*(short *)(param_1 + 0x84),
                            (int)*(short *)(param_1 + 0x9e),(int)_UNK_00758540,(int)_UNK_00758542,
                            (int)_UNK_00758544,(int)_UNK_00758546);
      }
    }
    if (*(char *)(local_8 + 0x3b) != '\0') {
      _local_c = CONCAT31(uStack_b,0x7a);
      if ((*(char *)(local_8 + 0x3b) == '\x01') || (*(char *)(local_8 + 0x3b) == '\x03')) {
        FUN__text__00505580((int)_UNK_00758548,(int)_UNK_0075854a,(int)*(short *)(local_8 + 0x86),
                            (int)*(short *)(local_8 + 0xa0),(int)_UNK_00758550,(int)_UNK_00758552,
                            (int)_UNK_00758554,(int)_UNK_00758556,*(undefined1 *)(local_8 + 0x6b),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00758548,(int)_UNK_0075854a,(int)*(short *)(local_8 + 0x86),
                            (int)*(short *)(local_8 + 0xa0),(int)_UNK_00758550,(int)_UNK_00758552,
                            (int)_UNK_00758554,(int)_UNK_00758556);
      }
    }
    break;
  case 8:
    if (*(char *)(param_1 + 0x39) != '\0') {
      _local_c = CONCAT31(uStack_b,0xa4);
      if ((*(char *)(param_1 + 0x39) == '\x01') || (*(char *)(param_1 + 0x39) == '\x03')) {
        FUN__text__00505580((int)_UNK_007587e8,(int)_UNK_007587ea,(int)*(short *)(param_1 + 0x82),
                            (int)*(short *)(param_1 + 0x9c),(int)_UNK_007587f0,(int)_UNK_007587f2,
                            (int)_UNK_007587f4,(int)_UNK_007587f6,*(undefined1 *)(param_1 + 0x69),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_007587e8,(int)_UNK_007587ea,(int)*(short *)(param_1 + 0x82),
                            (int)*(short *)(param_1 + 0x9c),(int)_UNK_007587f0,(int)_UNK_007587f2,
                            (int)_UNK_007587f4,(int)_UNK_007587f6);
      }
    }
    break;
  case 9:
    if (*(char *)(param_1 + 0x39) != '\0') {
      _local_c = CONCAT31(uStack_b,0x6e);
      if (*(char *)(param_1 + 0x39) == '\x01') {
        FUN__text__00505580((int)_UNK_00758488,(int)_UNK_0075848a,(int)*(short *)(param_1 + 0x82),
                            (int)PTR_DAT_0075848c._2_2_,(int)_UNK_00758490,(int)_UNK_00758492,
                            (int)_UNK_00758494,(int)_UNK_00758496,*(undefined1 *)(param_1 + 0x69),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00758488,(int)_UNK_0075848a,(int)*(short *)(param_1 + 0x82),
                            (int)PTR_DAT_0075848c._2_2_,(int)_UNK_00758490,(int)_UNK_00758492,
                            (int)_UNK_00758494,(int)_UNK_00758496);
      }
    }
    if (*(char *)(local_8 + 0x3a) != '\0') {
      _local_c = CONCAT31(uStack_b,0x6f);
      if ((*(char *)(local_8 + 0x3a) == '\x01') || (*(char *)(local_8 + 0x3a) == '\x03')) {
        FUN__text__00505580((int)_UNK_00758498,(int)_UNK_0075849a,(int)*(short *)(local_8 + 0x84),
                            (int)PTR_DAT_0075849c._2_2_,(int)_UNK_007584a0,(int)_UNK_007584a2,
                            (int)_UNK_007584a4,(int)_UNK_007584a6,*(undefined1 *)(local_8 + 0x6a),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00758498,(int)_UNK_0075849a,(int)*(short *)(local_8 + 0x84),
                            (int)PTR_DAT_0075849c._2_2_,(int)_UNK_007584a0,(int)_UNK_007584a2,
                            (int)_UNK_007584a4,(int)_UNK_007584a6);
      }
    }
    if (*(char *)(local_8 + 0x3b) != '\0') {
      _local_c = CONCAT31(uStack_b,0x7b);
      FUN__text__00505580((int)_UNK_00758558,(int)_UNK_0075855a,(int)*(short *)(local_8 + 0x86),
                          (int)*(short *)(local_8 + 0xa0),(int)_UNK_00758560,(int)_UNK_00758562,
                          (int)_UNK_00758564,(int)_UNK_00758566,*(undefined1 *)(local_8 + 0x6b),0x80
                          ,0x80,0x80);
    }
    if (*(char *)(local_8 + 0x3c) != '\0') {
      _local_c = CONCAT31(uStack_b,0x7c);
      FUN__text__00505580((int)_UNK_00758568,(int)_UNK_0075856a,(int)*(short *)(local_8 + 0x88),
                          (int)*(short *)(local_8 + 0xa2),(int)_UNK_00758570,(int)_UNK_00758572,
                          (int)_UNK_00758574,(int)_UNK_00758576,*(undefined1 *)(local_8 + 0x6c),0x80
                          ,0x80,0x80);
    }
    if (*(char *)(local_8 + 0x3d) != '\0') {
      _local_c = CONCAT31(uStack_b,0x7d);
      FUN__text__00505580((int)_UNK_00758578,(int)_UNK_0075857a,(int)*(short *)(local_8 + 0x8a),
                          (int)*(short *)(local_8 + 0xa4),(int)_UNK_00758580,(int)_UNK_00758582,
                          (int)_UNK_00758584,(int)_UNK_00758586,*(undefined1 *)(local_8 + 0x6d),0x80
                          ,0x80,0x80);
    }
    if (*(char *)(local_8 + 0x3e) != '\0') {
      _local_c = CONCAT31(uStack_b,0x7e);
      FUN__text__00505580((int)_UNK_00758588,(int)_UNK_0075858a,(int)*(short *)(local_8 + 0x8c),
                          (int)*(short *)(local_8 + 0xa6),(int)_UNK_00758590,(int)_UNK_00758592,
                          (int)_UNK_00758594,(int)_UNK_00758596,*(undefined1 *)(local_8 + 0x6e),0x80
                          ,0x80,0x80);
    }
    break;
  case 10:
    if (*(char *)(param_1 + 0x39) != '\0') {
      _local_c = CONCAT31(uStack_b,0x8a);
      if ((*(char *)(param_1 + 0x39) == '\x01') || (*(char *)(param_1 + 0x39) == '\x03')) {
        FUN__text__00505580((int)_UNK_00758648,(int)_UNK_0075864a,(int)_UNK_0075864c,
                            (int)_UNK_0075864e,(int)_UNK_00758650,(int)_UNK_00758652,
                            (int)_UNK_00758654,(int)_UNK_00758656,*(undefined1 *)(param_1 + 0x69),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00758648,(int)_UNK_0075864a,(int)_UNK_0075864c,
                            (int)_UNK_0075864e,(int)_UNK_00758650,(int)_UNK_00758652,
                            (int)_UNK_00758654,(int)_UNK_00758656);
      }
    }
    if (*(char *)(local_8 + 0x3a) != '\0') {
      _local_c = CONCAT31(uStack_b,0x8b);
      if ((*(char *)(local_8 + 0x3a) == '\x01') || (*(char *)(local_8 + 0x3a) == '\x03')) {
        FUN__text__00505580((int)_UNK_00758658,(int)_UNK_0075865a,(int)_UNK_0075865c,
                            (int)_UNK_0075865e,(int)_UNK_00758660,(int)_UNK_00758662,
                            (int)_UNK_00758664,(int)_UNK_00758666,*(undefined1 *)(local_8 + 0x6a),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00758658,(int)_UNK_0075865a,(int)_UNK_0075865c,
                            (int)_UNK_0075865e,(int)_UNK_00758660,(int)_UNK_00758662,
                            (int)_UNK_00758664,(int)_UNK_00758666);
      }
    }
    if (*(char *)(local_8 + 0x3b) != '\0') {
      _local_c = CONCAT31(uStack_b,0x8c);
      if ((*(char *)(local_8 + 0x3b) == '\x01') || (*(char *)(local_8 + 0x3b) == '\x03')) {
        FUN__text__00505580((int)_UNK_00758668,(int)_UNK_0075866a,(int)_UNK_0075866c,
                            (int)_UNK_0075866e,(int)_UNK_00758670,(int)_UNK_00758672,
                            (int)_UNK_00758674,(int)_UNK_00758676,*(undefined1 *)(local_8 + 0x6b),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00758668,(int)_UNK_0075866a,(int)_UNK_0075866c,
                            (int)_UNK_0075866e,(int)_UNK_00758670,(int)_UNK_00758672,
                            (int)_UNK_00758674,(int)_UNK_00758676);
      }
    }
    if (*(char *)(local_8 + 0x3c) != '\0') {
      _local_c = CONCAT31(uStack_b,0x8d);
      if ((*(char *)(local_8 + 0x3c) == '\x01') || (*(char *)(local_8 + 0x3c) == '\x03')) {
        FUN__text__00505580((int)_UNK_00758678,(int)_UNK_0075867a,(int)_UNK_0075867c,
                            (int)_UNK_0075867e,(int)_UNK_00758680,(int)_UNK_00758682,
                            (int)_UNK_00758684,(int)_UNK_00758686,*(undefined1 *)(local_8 + 0x6c),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00758678,(int)_UNK_0075867a,(int)_UNK_0075867c,
                            (int)_UNK_0075867e,(int)_UNK_00758680,(int)_UNK_00758682,
                            (int)_UNK_00758684,(int)_UNK_00758686);
      }
    }
    if (*(char *)(local_8 + 0x3d) != '\0') {
      _local_c = CONCAT31(uStack_b,0x8e);
      if ((*(char *)(local_8 + 0x3d) == '\x01') || (*(char *)(local_8 + 0x3d) == '\x03')) {
        FUN__text__00505580((int)_UNK_00758688,(int)_UNK_0075868a,(int)_UNK_0075868c,
                            (int)_UNK_0075868e,(int)_UNK_00758690,(int)_UNK_00758692,
                            (int)_UNK_00758694,(int)_UNK_00758696,*(undefined1 *)(local_8 + 0x6d),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00758688,(int)_UNK_0075868a,(int)_UNK_0075868c,
                            (int)_UNK_0075868e,(int)_UNK_00758690,(int)_UNK_00758692,
                            (int)_UNK_00758694,(int)_UNK_00758696);
      }
    }
    if (*(char *)(local_8 + 0x3e) != '\0') {
      _local_c = CONCAT31(uStack_b,0x8f);
      if ((*(char *)(local_8 + 0x3e) == '\x01') || (*(char *)(local_8 + 0x3e) == '\x03')) {
        FUN__text__00505580((int)_UNK_00758698,(int)_UNK_0075869a,(int)_UNK_0075869c,
                            (int)_UNK_0075869e,(int)_UNK_007586a0,(int)_UNK_007586a2,
                            (int)_UNK_007586a4,(int)_UNK_007586a6,*(undefined1 *)(local_8 + 0x6e),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00758698,(int)_UNK_0075869a,(int)_UNK_0075869c,
                            (int)_UNK_0075869e,(int)_UNK_007586a0,(int)_UNK_007586a2,
                            (int)_UNK_007586a4,(int)_UNK_007586a6);
      }
    }
    if (*(char *)(local_8 + 0x3f) != '\0') {
      _local_c = CONCAT31(uStack_b,0x90);
      if ((*(char *)(local_8 + 0x3f) == '\x01') || (*(char *)(local_8 + 0x3f) == '\x03')) {
        FUN__text__00505580((int)_UNK_007586a8,(int)_UNK_007586aa,(int)_UNK_007586ac,
                            (int)_UNK_007586ae,(int)_UNK_007586b0,(int)_UNK_007586b2,
                            (int)_UNK_007586b4,(int)_UNK_007586b6,*(undefined1 *)(local_8 + 0x6f),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_007586a8,(int)_UNK_007586aa,(int)_UNK_007586ac,
                            (int)_UNK_007586ae,(int)_UNK_007586b0,(int)_UNK_007586b2,
                            (int)_UNK_007586b4,(int)_UNK_007586b6);
      }
    }
    if (*(char *)(local_8 + 0x40) != '\0') {
      _local_c = CONCAT31(uStack_b,0x91);
      if ((*(char *)(local_8 + 0x40) == '\x01') || (*(char *)(local_8 + 0x40) == '\x03')) {
        FUN__text__00505580((int)_UNK_007586b8,(int)_UNK_007586ba,(int)_UNK_007586bc,
                            (int)_UNK_007586be,(int)_UNK_007586c0,(int)_UNK_007586c2,
                            (int)_UNK_007586c4,(int)_UNK_007586c6,*(undefined1 *)(local_8 + 0x70),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_007586b8,(int)_UNK_007586ba,(int)_UNK_007586bc,
                            (int)_UNK_007586be,(int)_UNK_007586c0,(int)_UNK_007586c2,
                            (int)_UNK_007586c4,(int)_UNK_007586c6);
      }
    }
    if (*(char *)(local_8 + 0x41) != '\0') {
      _local_c = CONCAT31(uStack_b,0x92);
      if ((*(char *)(local_8 + 0x41) == '\x01') || (*(char *)(local_8 + 0x41) == '\x03')) {
        FUN__text__00505580((int)_UNK_007586c8,(int)_UNK_007586ca,(int)_UNK_007586cc,
                            (int)_UNK_007586ce,(int)_UNK_007586d0,(int)_UNK_007586d2,
                            (int)_UNK_007586d4,(int)_UNK_007586d6,*(undefined1 *)(local_8 + 0x71),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_007586c8,(int)_UNK_007586ca,(int)_UNK_007586cc,
                            (int)_UNK_007586ce,(int)_UNK_007586d0,(int)_UNK_007586d2,
                            (int)_UNK_007586d4,(int)_UNK_007586d6);
      }
    }
    if (*(char *)(local_8 + 0x42) != '\0') {
      _local_c = CONCAT31(uStack_b,0x93);
      if ((*(char *)(local_8 + 0x42) == '\x01') || (*(char *)(local_8 + 0x42) == '\x03')) {
        FUN__text__00505580((int)_UNK_007586d8,(int)_UNK_007586da,(int)_UNK_007586dc,
                            (int)_UNK_007586de,(int)_UNK_007586e0,(int)_UNK_007586e2,
                            (int)_UNK_007586e4,(int)_UNK_007586e6,*(undefined1 *)(local_8 + 0x72),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_007586d8,(int)_UNK_007586da,(int)_UNK_007586dc,
                            (int)_UNK_007586de,(int)_UNK_007586e0,(int)_UNK_007586e2,
                            (int)_UNK_007586e4,(int)_UNK_007586e6);
      }
    }
    if (*(char *)(local_8 + 0x43) != '\0') {
      _local_c = CONCAT31(uStack_b,0x94);
      if ((*(char *)(local_8 + 0x43) == '\x01') || (*(char *)(local_8 + 0x43) == '\x03')) {
        FUN__text__00505580((int)_UNK_007586e8,(int)_UNK_007586ea,(int)_UNK_007586ec,
                            (int)_UNK_007586ee,(int)_UNK_007586f0,(int)_UNK_007586f2,
                            (int)_UNK_007586f4,(int)_UNK_007586f6,*(undefined1 *)(local_8 + 0x73),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_007586e8,(int)_UNK_007586ea,(int)_UNK_007586ec,
                            (int)_UNK_007586ee,(int)_UNK_007586f0,(int)_UNK_007586f2,
                            (int)_UNK_007586f4,(int)_UNK_007586f6);
      }
    }
    if (*(char *)(local_8 + 0x44) != '\0') {
      _local_c = CONCAT31(uStack_b,0x95);
      if ((*(char *)(local_8 + 0x44) == '\x01') || (*(char *)(local_8 + 0x44) == '\x03')) {
        FUN__text__00505580((int)_UNK_007586f8,(int)_UNK_007586fa,(int)_UNK_007586fc,
                            (int)_UNK_007586fe,(int)_UNK_00758700,(int)_UNK_00758702,
                            (int)_UNK_00758704,(int)_UNK_00758706,*(undefined1 *)(local_8 + 0x74),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_007586f8,(int)_UNK_007586fa,(int)_UNK_007586fc,
                            (int)_UNK_007586fe,(int)_UNK_00758700,(int)_UNK_00758702,
                            (int)_UNK_00758704,(int)_UNK_00758706);
      }
    }
    if (*(char *)(local_8 + 0x45) != '\0') {
      _local_c = CONCAT31(uStack_b,0x96);
      if ((*(char *)(local_8 + 0x45) == '\x01') || (*(char *)(local_8 + 0x45) == '\x03')) {
        FUN__text__00505580((int)_UNK_00758708,(int)_UNK_0075870a,(int)_UNK_0075870c,
                            (int)_UNK_0075870e,(int)_UNK_00758710,(int)_UNK_00758712,
                            (int)_UNK_00758714,(int)_UNK_00758716,*(undefined1 *)(local_8 + 0x75),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00758708,(int)_UNK_0075870a,(int)_UNK_0075870c,
                            (int)_UNK_0075870e,(int)_UNK_00758710,(int)_UNK_00758712,
                            (int)_UNK_00758714,(int)_UNK_00758716);
      }
    }
    if (*(char *)(local_8 + 0x46) != '\0') {
      _local_c = CONCAT31(uStack_b,0x97);
      if ((*(char *)(local_8 + 0x46) == '\x01') || (*(char *)(local_8 + 0x46) == '\x03')) {
        FUN__text__00505580((int)_UNK_00758718,(int)_UNK_0075871a,(int)_UNK_0075871c,
                            (int)_UNK_0075871e,(int)_UNK_00758720,(int)_UNK_00758722,
                            (int)_UNK_00758724,(int)_UNK_00758726,*(undefined1 *)(local_8 + 0x76),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00758718,(int)_UNK_0075871a,(int)_UNK_0075871c,
                            (int)_UNK_0075871e,(int)_UNK_00758720,(int)_UNK_00758722,
                            (int)_UNK_00758724,(int)_UNK_00758726);
      }
    }
    if (*(char *)(local_8 + 0x47) != '\0') {
      _local_c = CONCAT31(uStack_b,0x98);
      if ((*(char *)(local_8 + 0x47) == '\x01') || (*(char *)(local_8 + 0x47) == '\x03')) {
        FUN__text__00505580((int)_UNK_00758728,(int)_UNK_0075872a,(int)_UNK_0075872c,
                            (int)_UNK_0075872e,(int)_UNK_00758730,(int)_UNK_00758732,
                            (int)_UNK_00758734,(int)_UNK_00758736,*(undefined1 *)(local_8 + 0x77),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00758728,(int)_UNK_0075872a,(int)_UNK_0075872c,
                            (int)_UNK_0075872e,(int)_UNK_00758730,(int)_UNK_00758732,
                            (int)_UNK_00758734,(int)_UNK_00758736);
      }
    }
    if (*(char *)(local_8 + 0x48) != '\0') {
      _local_c = CONCAT31(uStack_b,0x99);
      if ((*(char *)(local_8 + 0x48) == '\x01') || (*(char *)(local_8 + 0x48) == '\x03')) {
        FUN__text__00505580((int)_UNK_00758738,(int)_UNK_0075873a,(int)_UNK_0075873c,
                            (int)_UNK_0075873e,(int)_UNK_00758740,(int)_UNK_00758742,
                            (int)_UNK_00758744,(int)_UNK_00758746,*(undefined1 *)(local_8 + 0x78),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00758738,(int)_UNK_0075873a,(int)_UNK_0075873c,
                            (int)_UNK_0075873e,(int)_UNK_00758740,(int)_UNK_00758742,
                            (int)_UNK_00758744,(int)_UNK_00758746);
      }
    }
    if (*(char *)(local_8 + 0x49) != '\0') {
      _local_c = CONCAT31(uStack_b,0x9a);
      if ((*(char *)(local_8 + 0x49) == '\x01') || (*(char *)(local_8 + 0x49) == '\x03')) {
        FUN__text__00505580((int)_UNK_00758748,(int)_UNK_0075874a,(int)_UNK_0075874c,
                            (int)_UNK_0075874e,(int)_UNK_00758750,(int)_UNK_00758752,
                            (int)_UNK_00758754,(int)_UNK_00758756,*(undefined1 *)(local_8 + 0x79),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00758748,(int)_UNK_0075874a,(int)_UNK_0075874c,
                            (int)_UNK_0075874e,(int)_UNK_00758750,(int)_UNK_00758752,
                            (int)_UNK_00758754,(int)_UNK_00758756);
      }
    }
    if (*(char *)(local_8 + 0x4a) != '\0') {
      _local_c = CONCAT31(uStack_b,0x9b);
      if ((*(char *)(local_8 + 0x4a) == '\x01') || (*(char *)(local_8 + 0x4a) == '\x03')) {
        FUN__text__00505580((int)_UNK_00758758,(int)_UNK_0075875a,(int)_UNK_0075875c,
                            (int)_UNK_0075875e,(int)_UNK_00758760,(int)_UNK_00758762,
                            (int)_UNK_00758764,(int)_UNK_00758766,*(undefined1 *)(local_8 + 0x7a),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00758758,(int)_UNK_0075875a,(int)_UNK_0075875c,
                            (int)_UNK_0075875e,(int)_UNK_00758760,(int)_UNK_00758762,
                            (int)_UNK_00758764,(int)_UNK_00758766);
      }
    }
    if (*(char *)(local_8 + 0x4b) != '\0') {
      _local_c = CONCAT31(uStack_b,0x9c);
      if ((*(char *)(local_8 + 0x4b) == '\x01') || (*(char *)(local_8 + 0x4b) == '\x03')) {
        FUN__text__00505580((int)_UNK_00758768,(int)_UNK_0075876a,(int)_UNK_0075876c,
                            (int)_UNK_0075876e,(int)_UNK_00758770,(int)_UNK_00758772,
                            (int)_UNK_00758774,(int)_UNK_00758776,*(undefined1 *)(local_8 + 0x7b),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00758768,(int)_UNK_0075876a,(int)_UNK_0075876c,
                            (int)_UNK_0075876e,(int)_UNK_00758770,(int)_UNK_00758772,
                            (int)_UNK_00758774,(int)_UNK_00758776);
      }
    }
    if (*(char *)(local_8 + 0x4c) != '\0') {
      _local_c = CONCAT31(uStack_b,0x9d);
      if ((*(char *)(local_8 + 0x4c) == '\x01') || (*(char *)(local_8 + 0x4c) == '\x03')) {
        FUN__text__00505580((int)_UNK_00758778,(int)_UNK_0075877a,(int)_UNK_0075877c,
                            (int)_UNK_0075877e,(int)_UNK_00758780,(int)_UNK_00758782,
                            (int)_UNK_00758784,(int)_UNK_00758786,*(undefined1 *)(local_8 + 0x7c),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00758778,(int)_UNK_0075877a,(int)_UNK_0075877c,
                            (int)_UNK_0075877e,(int)_UNK_00758780,(int)_UNK_00758782,
                            (int)_UNK_00758784,(int)_UNK_00758786);
      }
    }
    if (*(char *)(local_8 + 0x4d) != '\0') {
      _local_c = CONCAT31(uStack_b,0x9e);
      if ((*(char *)(local_8 + 0x4d) == '\x01') || (*(char *)(local_8 + 0x4d) == '\x03')) {
        FUN__text__00505580((int)_UNK_00758788,(int)_UNK_0075878a,(int)_UNK_0075878c,
                            (int)_UNK_0075878e,(int)_UNK_00758790,(int)_UNK_00758792,
                            (int)_UNK_00758794,(int)_UNK_00758796,*(undefined1 *)(local_8 + 0x7d),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00758788,(int)_UNK_0075878a,(int)_UNK_0075878c,
                            (int)_UNK_0075878e,(int)_UNK_00758790,(int)_UNK_00758792,
                            (int)_UNK_00758794,(int)_UNK_00758796);
      }
    }
    if (*(char *)(local_8 + 0x4e) != '\0') {
      _local_c = CONCAT31(uStack_b,0x9f);
      if ((*(char *)(local_8 + 0x4e) == '\x01') || (*(char *)(local_8 + 0x4e) == '\x03')) {
        FUN__text__00505580((int)_UNK_00758798,(int)_UNK_0075879a,(int)_UNK_0075879c,
                            (int)_UNK_0075879e,(int)_UNK_007587a0,(int)_UNK_007587a2,
                            (int)_UNK_007587a4,(int)_UNK_007587a6,*(undefined1 *)(local_8 + 0x7e),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00758798,(int)_UNK_0075879a,(int)_UNK_0075879c,
                            (int)_UNK_0075879e,(int)_UNK_007587a0,(int)_UNK_007587a2,
                            (int)_UNK_007587a4,(int)_UNK_007587a6);
      }
    }
    if (*(char *)(local_8 + 0x4f) != '\0') {
      _local_c = CONCAT31(uStack_b,0xa0);
      if ((*(char *)(local_8 + 0x4f) == '\x01') || (*(char *)(local_8 + 0x4f) == '\x03')) {
        FUN__text__00505580((int)_UNK_007587a8,(int)_UNK_007587aa,(int)_UNK_007587ac,
                            (int)_UNK_007587ae,(int)_UNK_007587b0,(int)_UNK_007587b2,
                            (int)_UNK_007587b4,(int)_UNK_007587b6,*(undefined1 *)(local_8 + 0x7f),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_007587a8,(int)_UNK_007587aa,(int)_UNK_007587ac,
                            (int)_UNK_007587ae,(int)_UNK_007587b0,(int)_UNK_007587b2,
                            (int)_UNK_007587b4,(int)_UNK_007587b6);
      }
    }
    break;
  case 0xc:
    if (*(char *)(param_1 + 0x45) != '\0') {
      _local_c = CONCAT31(uStack_b,0x7f);
      FUN__text__00505580((int)_UNK_00758598,(int)_UNK_0075859a,(int)_UNK_0075859c,
                          (int)_UNK_0075859e,(int)_UNK_007585a0,(int)_UNK_007585a2,
                          (int)_UNK_007585a4,(int)_UNK_007585a6,*(undefined1 *)(param_1 + 0x75),0x80
                          ,0x80,0x80);
    }
    if (*(char *)(local_8 + 0x3f) != '\0') {
      _local_c = CONCAT31(uStack_b,0x80);
      FUN__text__00505580((int)_UNK_007585a8,(int)_UNK_007585aa,(int)_UNK_007585ac,
                          (int)_UNK_007585ae,(int)_UNK_007585b0,(int)_UNK_007585b2,
                          (int)_UNK_007585b4,(int)_UNK_007585b6,*(undefined1 *)(local_8 + 0x6f),0x80
                          ,0x80,0x80);
    }
    if (*(char *)(local_8 + 0x3d) != '\0') {
      _local_c = CONCAT31(uStack_b,0x81);
      FUN__text__00505580((int)_UNK_007585b8,(int)_UNK_007585ba,(int)_UNK_007585bc,
                          (int)_UNK_007585be,(int)_UNK_007585c0,(int)_UNK_007585c2,
                          (int)_UNK_007585c4,(int)_UNK_007585c6,*(undefined1 *)(local_8 + 0x6d),0x80
                          ,0x80,0x80);
    }
    if (*(char *)(local_8 + 0x40) != '\0') {
      _local_c = CONCAT31(uStack_b,0x82);
      FUN__text__00505580((int)_UNK_007585c8,(int)_UNK_007585ca,(int)_UNK_007585cc,
                          (int)_UNK_007585ce,(int)_UNK_007585d0,(int)_UNK_007585d2,
                          (int)_UNK_007585d4,(int)_UNK_007585d6,*(undefined1 *)(local_8 + 0x70),0x80
                          ,0x80,0x80);
    }
    if (*(char *)(local_8 + 0x43) != '\0') {
      _local_c = CONCAT31(uStack_b,0x83);
      FUN__text__00505580((int)_UNK_007585d8,(int)_UNK_007585da,(int)_UNK_007585dc,
                          (int)_UNK_007585de,(int)_UNK_007585e0,(int)_UNK_007585e2,
                          (int)_UNK_007585e4,(int)_UNK_007585e6,*(undefined1 *)(local_8 + 0x73),0x80
                          ,0x80,0x80);
    }
    if (*(char *)(local_8 + 0x44) != '\0') {
      _local_c = CONCAT31(uStack_b,0x84);
      FUN__text__00505580((int)_UNK_007585e8,(int)_UNK_007585ea,(int)_UNK_007585ec,
                          (int)_UNK_007585ee,(int)_UNK_007585f0,(int)_UNK_007585f2,
                          (int)_UNK_007585f4,(int)_UNK_007585f6,*(undefined1 *)(local_8 + 0x74),0x80
                          ,0x80,0x80);
    }
  }
  local_8 = 0x512289;
  FUN__text__0056ce80();
  return;
}

