
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __fastcall FUN__text__004e8f10(int param_1)

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
      FUN__text__00505580((int)_UNK_00752fb4,(int)_UNK_00752fb6,(int)_UNK_00752fb8,
                          (int)_UNK_00752fba,(int)_UNK_00752fbc,(int)_UNK_00752fbe,
                          (int)_UNK_00752fc0,(int)_UNK_00752fc2,*(undefined1 *)(param_1 + 0x69),0x80
                          ,0x80,0x80);
    }
    if (*(char *)(local_8 + 0x3a) != '\0') {
      _local_c = CONCAT31(uStack_b,0xa1);
      FUN__text__00505580((int)_UNK_00753134,(int)_UNK_00753136,(int)_UNK_00753138,
                          (int)_UNK_0075313a,(int)_UNK_0075313c,(int)_UNK_0075313e,
                          (int)_UNK_00753140,(int)_UNK_00753142,*(undefined1 *)(local_8 + 0x6a),0x80
                          ,0x80,0x80);
    }
    if (*(char *)(local_8 + 0x3b) != '\0') {
      _local_c = CONCAT31(uStack_b,0xa2);
      FUN__text__00505580((int)_UNK_00753144,(int)_UNK_00753146,(int)_UNK_00753148,
                          (int)_UNK_0075314a,(int)_UNK_0075314c,(int)_UNK_0075314e,
                          (int)_UNK_00753150,(int)_UNK_00753152,*(undefined1 *)(local_8 + 0x6b),0x80
                          ,0x80,0x80);
    }
    if (*(char *)(local_8 + 0x3c) != '\0') {
      _local_c = CONCAT31(uStack_b,0xa3);
      FUN__text__00505580((int)_UNK_00753154,(int)_UNK_00753156,(int)_UNK_00753158,
                          (int)_UNK_0075315a,(int)_UNK_0075315c,(int)_UNK_0075315e,
                          (int)_UNK_00753160,(int)_UNK_00753162,*(undefined1 *)(local_8 + 0x6c),0x80
                          ,0x80,0x80);
    }
    break;
  case 1:
    if (*(char *)(param_1 + 0x39) != '\0') {
      _local_c = CONCAT31(uStack_b,0x6d);
      if ((*(char *)(param_1 + 0x39) == '\x01') || (*(char *)(param_1 + 0x39) == '\x03')) {
        FUN__text__00505580((int)_UNK_00752df4,(int)_UNK_00752df6,(int)*(short *)(param_1 + 0x82),
                            (int)*(short *)(param_1 + 0x9c),(int)_UNK_00752dfc,(int)_UNK_00752dfe,
                            (int)_UNK_00752e00,(int)_UNK_00752e02,*(undefined1 *)(param_1 + 0x69),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00752df4,(int)_UNK_00752df6,(int)*(short *)(param_1 + 0x82),
                            (int)*(short *)(param_1 + 0x9c),(int)_UNK_00752dfc,(int)_UNK_00752dfe,
                            (int)_UNK_00752e00,(int)_UNK_00752e02);
      }
    }
    if (*(char *)(local_8 + 0x3a) != '\0') {
      _local_c = CONCAT31(uStack_b,0x77);
      if ((*(char *)(local_8 + 0x3a) == '\x01') || (*(char *)(local_8 + 0x3a) == '\x03')) {
        FUN__text__00505580((int)_UNK_00752e94,(int)_UNK_00752e96,(int)*(short *)(local_8 + 0x84),
                            (int)*(short *)(local_8 + 0x9e),(int)_UNK_00752e9c,(int)_UNK_00752e9e,
                            (int)_UNK_00752ea0,(int)_UNK_00752ea2,*(undefined1 *)(local_8 + 0x6a),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00752e94,(int)_UNK_00752e96,(int)*(short *)(local_8 + 0x84),
                            (int)*(short *)(local_8 + 0x9e),(int)_UNK_00752e9c,(int)_UNK_00752e9e,
                            (int)_UNK_00752ea0,(int)_UNK_00752ea2);
      }
    }
    break;
  case 2:
    if (*(char *)(param_1 + 0x39) != '\0') {
      if ((*(char *)(param_1 + 0x39) == '\x01') || (*(char *)(param_1 + 0x39) == '\x03')) {
        local_c = 0x78;
        FUN__text__00505580((int)_UNK_00752ea4,(int)_UNK_00752ea6,(int)*(short *)(param_1 + 0x82),
                            (int)*(short *)(param_1 + 0x9c),(int)_UNK_00752eac,(int)_UNK_00752eae,
                            (int)_UNK_00752eb0,(int)_UNK_00752eb2,*(undefined1 *)(param_1 + 0x69),
                            0x80,0x80,0x80);
        _local_c = CONCAT31(uStack_b,0x72);
        FUN__text__00505580((int)_UNK_00752e44,(int)_UNK_00752e46,*(short *)(local_8 + 0x82) + 0x400
                            ,*(short *)(local_8 + 0x9c) + 2,(int)_UNK_00752e4c,(int)_UNK_00752e4e,
                            (int)_UNK_00752e50,(int)_UNK_00752e52,*(undefined1 *)(local_8 + 0x69),
                            0x80,0x80,0x80);
      }
      else {
        local_c = 0x78;
        FUN__text__00505000((int)_UNK_00752ea4,(int)_UNK_00752ea6,(int)*(short *)(param_1 + 0x82),
                            (int)*(short *)(param_1 + 0x9c),(int)_UNK_00752eac,(int)_UNK_00752eae,
                            (int)_UNK_00752eb0,(int)_UNK_00752eb2);
        _local_c = CONCAT31(uStack_b,0x72);
        FUN__text__00505000((int)_UNK_00752e44,(int)_UNK_00752e46,*(short *)(local_8 + 0x82) + 0x400
                            ,*(short *)(local_8 + 0x9c) + 2,(int)_UNK_00752e4c,(int)_UNK_00752e4e,
                            (int)_UNK_00752e50,(int)_UNK_00752e52);
      }
    }
    if (*(char *)(local_8 + 0x3a) != '\0') {
      _local_c = CONCAT31(uStack_b,0x75);
      if ((*(char *)(local_8 + 0x3a) == '\x01') || (*(char *)(local_8 + 0x3a) == '\x03')) {
        FUN__text__00505580((int)_UNK_00752e74,(int)_UNK_00752e76,(int)*(short *)(local_8 + 0x84),
                            (int)*(short *)(local_8 + 0x9e),(int)_UNK_00752e7c,(int)_UNK_00752e7e,
                            (int)_UNK_00752e80,(int)_UNK_00752e82,*(undefined1 *)(local_8 + 0x6a),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00752e74,(int)_UNK_00752e76,(int)*(short *)(local_8 + 0x84),
                            (int)*(short *)(local_8 + 0x9e),(int)_UNK_00752e7c,(int)_UNK_00752e7e,
                            (int)_UNK_00752e80,(int)_UNK_00752e82);
      }
    }
    break;
  case 3:
    if (*(char *)(param_1 + 0x39) != '\0') {
      _local_c = CONCAT31(uStack_b,100);
      FUN__text__00505580((int)_UNK_00752d64,(int)_UNK_00752d66,(int)*(short *)(param_1 + 0x82),
                          (int)PTR_DAT_00752d68._2_2_,(int)_UNK_00752d6c,(int)_UNK_00752d6e,
                          (int)_UNK_00752d70,(int)_UNK_00752d72,*(undefined1 *)(param_1 + 0x69),0x80
                          ,0x80,0x80);
    }
    if (*(char *)(local_8 + 0x3a) != '\0') {
      _local_c = CONCAT31(uStack_b,0x65);
      FUN__text__00505580((int)_UNK_00752d74,(int)_UNK_00752d76,(int)*(short *)(local_8 + 0x84),
                          (int)PTR_DAT_00752d78._2_2_,(int)_UNK_00752d7c,(int)_UNK_00752d7e,
                          (int)_UNK_00752d80,(int)_UNK_00752d82,*(undefined1 *)(local_8 + 0x6a),0x80
                          ,0x80,0x80);
    }
    if (*(char *)(local_8 + 0x3b) != '\0') {
      _local_c = CONCAT31(uStack_b,0x66);
      FUN__text__00505580((int)_UNK_00752d84,(int)_UNK_00752d86,(int)*(short *)(local_8 + 0x86),
                          (int)PTR_DAT_00752d88._2_2_,(int)_UNK_00752d8c,(int)_UNK_00752d8e,
                          (int)_UNK_00752d90,(int)_UNK_00752d92,*(undefined1 *)(local_8 + 0x6b),0x80
                          ,0x80,0x80);
    }
    if (*(char *)(local_8 + 0x3c) != '\0') {
      _local_c = CONCAT31(uStack_b,0x67);
      FUN__text__00505580((int)_UNK_00752d94,(int)_UNK_00752d96,(int)*(short *)(local_8 + 0x88),
                          (int)PTR_DAT_00752d98._2_2_,(int)_UNK_00752d9c,(int)_UNK_00752d9e,
                          (int)_UNK_00752da0,(int)_UNK_00752da2,*(undefined1 *)(local_8 + 0x6c),0x80
                          ,0x80,0x80);
    }
    if (*(char *)(local_8 + 0x3d) != '\0') {
      _local_c = CONCAT31(uStack_b,0x68);
      FUN__text__00505580((int)_UNK_00752da4,(int)_UNK_00752da6,(int)*(short *)(local_8 + 0x8a),
                          (int)PTR_DAT_00752da8._2_2_,(int)_UNK_00752dac,(int)_UNK_00752dae,
                          (int)_UNK_00752db0,(int)_UNK_00752db2,*(undefined1 *)(local_8 + 0x6d),0x80
                          ,0x80,0x80);
    }
    if (*(char *)(local_8 + 0x3e) != '\0') {
      _local_c = CONCAT31(uStack_b,0x69);
      FUN__text__00505580((int)_UNK_00752db4,(int)_UNK_00752db6,(int)*(short *)(local_8 + 0x8c),
                          (int)PTR_DAT_00752db8._2_2_,(int)_UNK_00752dbc,(int)_UNK_00752dbe,
                          (int)_UNK_00752dc0,(int)_UNK_00752dc2,*(undefined1 *)(local_8 + 0x6e),0x80
                          ,0x80,0x80);
    }
    if (*(char *)(local_8 + 0x3f) != '\0') {
      _local_c = CONCAT31(uStack_b,0x6a);
      FUN__text__00505580((int)_UNK_00752dc4,(int)_UNK_00752dc6,(int)*(short *)(local_8 + 0x8e),
                          (int)PTR_DAT_00752dc8._2_2_,(int)_UNK_00752dcc,(int)_UNK_00752dce,
                          (int)_UNK_00752dd0,(int)_UNK_00752dd2,*(undefined1 *)(local_8 + 0x6f),0x80
                          ,0x80,0x80);
    }
    if (*(char *)(local_8 + 0x40) != '\0') {
      _local_c = CONCAT31(uStack_b,0x6b);
      FUN__text__00505580((int)_UNK_00752dd4,(int)_UNK_00752dd6,(int)*(short *)(local_8 + 0x90),
                          (int)PTR_DAT_00752dd8._2_2_,(int)_UNK_00752ddc,(int)_UNK_00752dde,
                          (int)_UNK_00752de0,(int)_UNK_00752de2,*(undefined1 *)(local_8 + 0x70),0x80
                          ,0x80,0x80);
    }
    break;
  case 4:
    if (*(char *)(param_1 + 0x39) != '\0') {
      _local_c = CONCAT31(uStack_b,0x49);
      if ((*(char *)(param_1 + 0x39) == '\x01') || (*(char *)(param_1 + 0x39) == '\x03')) {
        FUN__text__00505580((int)_UNK_00752bb4,(int)_UNK_00752bb6,(int)_UNK_00752bb8,
                            (int)*(short *)(param_1 + 0x9c),(int)_UNK_00752bbc,(int)_UNK_00752bbe,
                            (int)_UNK_00752bc0,(int)_UNK_00752bc2,*(undefined1 *)(param_1 + 0x69),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00752bb4,(int)_UNK_00752bb6,(int)_UNK_00752bb8,
                            (int)*(short *)(param_1 + 0x9c),(int)_UNK_00752bbc,(int)_UNK_00752bbe,
                            (int)_UNK_00752bc0,(int)_UNK_00752bc2);
      }
    }
    break;
  case 5:
    if (*(char *)(param_1 + 0x39) != '\0') {
      _local_c = CONCAT31(uStack_b,0x76);
      if ((*(char *)(param_1 + 0x39) == '\x01') || (*(char *)(param_1 + 0x39) == '\x03')) {
        FUN__text__00505580((int)_UNK_00752e84,(int)_UNK_00752e86,(int)*(short *)(param_1 + 0x82),
                            (int)*(short *)(param_1 + 0x9c),(int)_UNK_00752e8c,(int)_UNK_00752e8e,
                            (int)_UNK_00752e90,(int)_UNK_00752e92,*(undefined1 *)(param_1 + 0x69),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00752e84,(int)_UNK_00752e86,(int)*(short *)(param_1 + 0x82),
                            (int)*(short *)(param_1 + 0x9c),(int)_UNK_00752e8c,(int)_UNK_00752e8e,
                            (int)_UNK_00752e90,(int)_UNK_00752e92);
      }
    }
    if (*(char *)(local_8 + 0x3a) != '\0') {
      _local_c = CONCAT31(uStack_b,0x73);
      if ((*(char *)(local_8 + 0x3a) == '\x01') || (*(char *)(local_8 + 0x3a) == '\x03')) {
        FUN__text__00505580((int)_UNK_00752e54,(int)_UNK_00752e56,(int)*(short *)(local_8 + 0x84),
                            (int)_UNK_00752e5a,(int)_UNK_00752e5c,(int)_UNK_00752e5e,
                            (int)_UNK_00752e60,(int)_UNK_00752e62,*(undefined1 *)(local_8 + 0x6a),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00752e54,(int)_UNK_00752e56,(int)*(short *)(local_8 + 0x84),
                            (int)_UNK_00752e5a,(int)_UNK_00752e5c,(int)_UNK_00752e5e,
                            (int)_UNK_00752e60,(int)_UNK_00752e62);
      }
    }
    if (*(char *)(local_8 + 0x3d) != '\0') {
      _local_c = CONCAT31(uStack_b,0x74);
      if ((*(char *)(local_8 + 0x3d) == '\x01') || (*(char *)(local_8 + 0x3d) == '\x03')) {
        FUN__text__00505580((int)_UNK_00752e64,(int)_UNK_00752e66,(int)*(short *)(local_8 + 0x8a),
                            (int)*(short *)(local_8 + 0xa4),(int)_UNK_00752e6c,(int)_UNK_00752e6e,
                            (int)_UNK_00752e70,(int)_UNK_00752e72,*(undefined1 *)(local_8 + 0x6d),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00752e64,(int)_UNK_00752e66,(int)*(short *)(local_8 + 0x8a),
                            (int)*(short *)(local_8 + 0xa4),(int)_UNK_00752e6c,(int)_UNK_00752e6e,
                            (int)_UNK_00752e70,(int)_UNK_00752e72);
      }
    }
    if (*(char *)(local_8 + 0x3e) != '\0') {
      _local_c = CONCAT31(uStack_b,0x6c);
      if ((*(char *)(local_8 + 0x3e) == '\x01') || (*(char *)(local_8 + 0x3e) == '\x03')) {
        FUN__text__00505580((int)_UNK_00752de4,(int)_UNK_00752de6,(int)*(short *)(local_8 + 0x8c),
                            (int)_UNK_00752dea,(int)_UNK_00752dec,(int)_UNK_00752dee,
                            (int)_UNK_00752df0,(int)_UNK_00752df2,*(undefined1 *)(local_8 + 0x6e),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00752de4,(int)_UNK_00752de6,(int)*(short *)(local_8 + 0x8c),
                            (int)_UNK_00752dea,(int)_UNK_00752dec,(int)_UNK_00752dee,
                            (int)_UNK_00752df0,(int)_UNK_00752df2);
      }
    }
    break;
  case 6:
    if (*(char *)(param_1 + 0x3a) != '\0') {
      _local_c = CONCAT31(uStack_b,0x79);
      if ((*(char *)(param_1 + 0x3a) == '\x01') || (*(char *)(param_1 + 0x3a) == '\x03')) {
        FUN__text__00505580((int)_UNK_00752eb4,(int)_UNK_00752eb6,(int)*(short *)(param_1 + 0x84),
                            (int)*(short *)(param_1 + 0x9e),(int)_UNK_00752ebc,(int)_UNK_00752ebe,
                            (int)_UNK_00752ec0,(int)_UNK_00752ec2,*(undefined1 *)(param_1 + 0x6a),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00752eb4,(int)_UNK_00752eb6,(int)*(short *)(param_1 + 0x84),
                            (int)*(short *)(param_1 + 0x9e),(int)_UNK_00752ebc,(int)_UNK_00752ebe,
                            (int)_UNK_00752ec0,(int)_UNK_00752ec2);
      }
    }
    if (*(char *)(local_8 + 0x3b) != '\0') {
      _local_c = CONCAT31(uStack_b,0x7a);
      if ((*(char *)(local_8 + 0x3b) == '\x01') || (*(char *)(local_8 + 0x3b) == '\x03')) {
        FUN__text__00505580((int)_UNK_00752ec4,(int)_UNK_00752ec6,(int)*(short *)(local_8 + 0x86),
                            (int)*(short *)(local_8 + 0xa0),(int)_UNK_00752ecc,(int)_UNK_00752ece,
                            (int)_UNK_00752ed0,(int)_UNK_00752ed2,*(undefined1 *)(local_8 + 0x6b),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00752ec4,(int)_UNK_00752ec6,(int)*(short *)(local_8 + 0x86),
                            (int)*(short *)(local_8 + 0xa0),(int)_UNK_00752ecc,(int)_UNK_00752ece,
                            (int)_UNK_00752ed0,(int)_UNK_00752ed2);
      }
    }
    break;
  case 7:
    if (*(char *)(param_1 + 0x3a) != '\0') {
      _local_c = CONCAT31(uStack_b,0x48);
      if ((*(char *)(param_1 + 0x3a) == '\x01') || (*(char *)(param_1 + 0x3a) == '\x03')) {
        FUN__text__00505580((int)_UNK_00752ba4,(int)_UNK_00752ba6,(int)*(short *)(param_1 + 0x84),
                            (int)*(short *)(param_1 + 0x9e),(int)_UNK_00752bac,(int)_UNK_00752bae,
                            (int)_UNK_00752bb0,(int)_UNK_00752bb2,*(undefined1 *)(param_1 + 0x6a),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00752ba4,(int)_UNK_00752ba6,(int)*(short *)(param_1 + 0x84),
                            (int)*(short *)(param_1 + 0x9e),(int)_UNK_00752bac,(int)_UNK_00752bae,
                            (int)_UNK_00752bb0,(int)_UNK_00752bb2);
      }
    }
    break;
  case 8:
    if (*(char *)(param_1 + 0x39) != '\0') {
      _local_c = CONCAT31(uStack_b,0x31);
      if (*(char *)(param_1 + 0x39) == '\x01') {
        FUN__text__00505580((int)_UNK_00752614,(int)_UNK_00752616,(int)_UNK_00752618,
                            (int)_UNK_0075261a,(int)_UNK_0075261c,(int)_UNK_0075261e,
                            (int)_UNK_00752620,(int)_UNK_00752622,*(undefined1 *)(param_1 + 0x69),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00752614,(int)_UNK_00752616,(int)_UNK_00752618,
                            (int)_UNK_0075261a,(int)_UNK_0075261c,(int)_UNK_0075261e,
                            (int)_UNK_00752620,(int)_UNK_00752622);
      }
    }
    if (*(char *)(local_8 + 0x3a) != '\0') {
      _local_c = CONCAT31(uStack_b,0x32);
      if (*(char *)(local_8 + 0x3a) == '\x01') {
        FUN__text__00505580((int)_UNK_00752624,(int)_UNK_00752626,(int)_UNK_00752628,
                            (int)_UNK_0075262a,(int)_UNK_0075262c,(int)_UNK_0075262e,
                            (int)_UNK_00752630,(int)_UNK_00752632,*(undefined1 *)(local_8 + 0x6a),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00752624,(int)_UNK_00752626,(int)_UNK_00752628,
                            (int)_UNK_0075262a,(int)_UNK_0075262c,(int)_UNK_0075262e,
                            (int)_UNK_00752630,(int)_UNK_00752632);
      }
    }
    if (*(char *)(local_8 + 0x3b) != '\0') {
      _local_c = CONCAT31(uStack_b,0x33);
      if (*(char *)(local_8 + 0x3b) == '\x01') {
        FUN__text__00505580((int)_UNK_00752634,(int)_UNK_00752636,(int)_UNK_00752638,
                            (int)_UNK_0075263a,(int)_UNK_0075263c,(int)_UNK_0075263e,
                            (int)_UNK_00752640,(int)_UNK_00752642,*(undefined1 *)(local_8 + 0x6b),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00752634,(int)_UNK_00752636,(int)_UNK_00752638,
                            (int)_UNK_0075263a,(int)_UNK_0075263c,(int)_UNK_0075263e,
                            (int)_UNK_00752640,(int)_UNK_00752642);
      }
    }
    if (*(char *)(local_8 + 0x3c) != '\0') {
      _local_c = CONCAT31(uStack_b,0x34);
      if (*(char *)(local_8 + 0x3c) == '\x01') {
        FUN__text__00505580((int)_UNK_00752644,(int)_UNK_00752646,(int)_UNK_00752648,
                            (int)_UNK_0075264a,(int)_UNK_0075264c,(int)_UNK_0075264e,
                            (int)_UNK_00752650,(int)_UNK_00752652,*(undefined1 *)(local_8 + 0x6c),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00752644,(int)_UNK_00752646,(int)_UNK_00752648,
                            (int)_UNK_0075264a,(int)_UNK_0075264c,(int)_UNK_0075264e,
                            (int)_UNK_00752650,(int)_UNK_00752652);
      }
    }
    if (*(char *)(local_8 + 0x3d) != '\0') {
      _local_c = CONCAT31(uStack_b,0x35);
      if (*(char *)(local_8 + 0x3d) == '\x01') {
        FUN__text__00505580((int)_UNK_00752654,(int)_UNK_00752656,(int)_UNK_00752658,
                            (int)_UNK_0075265a,(int)_UNK_0075265c,(int)_UNK_0075265e,
                            (int)_UNK_00752660,(int)_UNK_00752662,*(undefined1 *)(local_8 + 0x6d),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00752654,(int)_UNK_00752656,(int)_UNK_00752658,
                            (int)_UNK_0075265a,(int)_UNK_0075265c,(int)_UNK_0075265e,
                            (int)_UNK_00752660,(int)_UNK_00752662);
      }
    }
    if (*(char *)(local_8 + 0x3e) != '\0') {
      _local_c = CONCAT31(uStack_b,0x36);
      if (*(char *)(local_8 + 0x3e) == '\x01') {
        FUN__text__00505580((int)_UNK_00752664,(int)_UNK_00752666,(int)_UNK_00752668,
                            (int)_UNK_0075266a,(int)_UNK_0075266c,(int)_UNK_0075266e,
                            (int)_UNK_00752670,(int)_UNK_00752672,*(undefined1 *)(local_8 + 0x6e),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00752664,(int)_UNK_00752666,(int)_UNK_00752668,
                            (int)_UNK_0075266a,(int)_UNK_0075266c,(int)_UNK_0075266e,
                            (int)_UNK_00752670,(int)_UNK_00752672);
      }
    }
    if (*(char *)(local_8 + 0x3f) != '\0') {
      _local_c = CONCAT31(uStack_b,0x37);
      if (*(char *)(local_8 + 0x3f) == '\x01') {
        FUN__text__00505580((int)_UNK_00752674,(int)_UNK_00752676,(int)_UNK_00752678,
                            (int)_UNK_0075267a,(int)_UNK_0075267c,(int)_UNK_0075267e,
                            (int)_UNK_00752680,(int)_UNK_00752682,*(undefined1 *)(local_8 + 0x6f),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00752674,(int)_UNK_00752676,(int)_UNK_00752678,
                            (int)_UNK_0075267a,(int)_UNK_0075267c,(int)_UNK_0075267e,
                            (int)_UNK_00752680,(int)_UNK_00752682);
      }
    }
    if (*(char *)(local_8 + 0x40) != '\0') {
      _local_c = CONCAT31(uStack_b,0x38);
      if (*(char *)(local_8 + 0x40) == '\x01') {
        FUN__text__00505580((int)_UNK_00752684,(int)_UNK_00752686,(int)_UNK_00752688,
                            (int)_UNK_0075268a,(int)_UNK_0075268c,(int)_UNK_0075268e,
                            (int)_UNK_00752690,(int)_UNK_00752692,*(undefined1 *)(local_8 + 0x70),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00752684,(int)_UNK_00752686,(int)_UNK_00752688,
                            (int)_UNK_0075268a,(int)_UNK_0075268c,(int)_UNK_0075268e,
                            (int)_UNK_00752690,(int)_UNK_00752692);
      }
    }
    if (*(char *)(local_8 + 0x41) != '\0') {
      _local_c = CONCAT31(uStack_b,0x39);
      if (*(char *)(local_8 + 0x41) == '\x01') {
        FUN__text__00505580((int)_UNK_00752694,(int)_UNK_00752696,(int)_UNK_00752698,
                            (int)_UNK_0075269a,(int)_UNK_0075269c,(int)_UNK_0075269e,
                            (int)_UNK_007526a0,(int)_UNK_007526a2,*(undefined1 *)(local_8 + 0x71),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00752694,(int)_UNK_00752696,(int)_UNK_00752698,
                            (int)_UNK_0075269a,(int)_UNK_0075269c,(int)_UNK_0075269e,
                            (int)_UNK_007526a0,(int)_UNK_007526a2);
      }
    }
    if (*(char *)(local_8 + 0x42) != '\0') {
      _local_c = CONCAT31(uStack_b,0x3a);
      if (*(char *)(local_8 + 0x42) == '\x01') {
        FUN__text__00505580((int)_UNK_007526a4,(int)_UNK_007526a6,(int)_UNK_007526a8,
                            (int)_UNK_007526aa,(int)_UNK_007526ac,(int)_UNK_007526ae,
                            (int)_UNK_007526b0,(int)_UNK_007526b2,*(undefined1 *)(local_8 + 0x72),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_007526a4,(int)_UNK_007526a6,(int)_UNK_007526a8,
                            (int)_UNK_007526aa,(int)_UNK_007526ac,(int)_UNK_007526ae,
                            (int)_UNK_007526b0,(int)_UNK_007526b2);
      }
    }
    if (*(char *)(local_8 + 0x43) != '\0') {
      _local_c = CONCAT31(uStack_b,0x3b);
      if (*(char *)(local_8 + 0x43) == '\x01') {
        FUN__text__00505580((int)_UNK_007526b4,(int)_UNK_007526b6,(int)_UNK_007526b8,
                            (int)_UNK_007526ba,(int)_UNK_007526bc,(int)_UNK_007526be,
                            (int)_UNK_007526c0,(int)_UNK_007526c2,*(undefined1 *)(local_8 + 0x73),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_007526b4,(int)_UNK_007526b6,(int)_UNK_007526b8,
                            (int)_UNK_007526ba,(int)_UNK_007526bc,(int)_UNK_007526be,
                            (int)_UNK_007526c0,(int)_UNK_007526c2);
      }
    }
    if (*(char *)(local_8 + 0x44) != '\0') {
      _local_c = CONCAT31(uStack_b,0x3c);
      if (*(char *)(local_8 + 0x44) == '\x01') {
        FUN__text__00505580((int)_UNK_007526c4,(int)_UNK_007526c6,(int)_UNK_007526c8,
                            (int)_UNK_007526ca,(int)_UNK_007526cc,(int)_UNK_007526ce,
                            (int)_UNK_007526d0,(int)_UNK_007526d2,*(undefined1 *)(local_8 + 0x74),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_007526c4,(int)_UNK_007526c6,(int)_UNK_007526c8,
                            (int)_UNK_007526ca,(int)_UNK_007526cc,(int)_UNK_007526ce,
                            (int)_UNK_007526d0,(int)_UNK_007526d2);
      }
    }
    if (*(char *)(local_8 + 0x45) != '\0') {
      _local_c = CONCAT31(uStack_b,0x3d);
      if (*(char *)(local_8 + 0x45) == '\x01') {
        FUN__text__00505580((int)_UNK_007526d4,(int)_UNK_007526d6,(int)_UNK_007526d8,
                            (int)_UNK_007526da,(int)_UNK_007526dc,(int)_UNK_007526de,
                            (int)_UNK_007526e0,(int)_UNK_007526e2,*(undefined1 *)(local_8 + 0x75),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_007526d4,(int)_UNK_007526d6,(int)_UNK_007526d8,
                            (int)_UNK_007526da,(int)_UNK_007526dc,(int)_UNK_007526de,
                            (int)_UNK_007526e0,(int)_UNK_007526e2);
      }
    }
    if (*(char *)(local_8 + 0x46) != '\0') {
      _local_c = CONCAT31(uStack_b,0x3e);
      if (*(char *)(local_8 + 0x46) == '\x01') {
        FUN__text__00505580((int)_UNK_007526e4,(int)_UNK_007526e6,(int)_UNK_007526e8,
                            (int)_UNK_007526ea,(int)_UNK_007526ec,(int)_UNK_007526ee,
                            (int)_UNK_007526f0,(int)_UNK_007526f2,*(undefined1 *)(local_8 + 0x76),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_007526e4,(int)_UNK_007526e6,(int)_UNK_007526e8,
                            (int)_UNK_007526ea,(int)_UNK_007526ec,(int)_UNK_007526ee,
                            (int)_UNK_007526f0,(int)_UNK_007526f2);
      }
    }
    if (*(char *)(local_8 + 0x47) != '\0') {
      _local_c = CONCAT31(uStack_b,0x3f);
      if (*(char *)(local_8 + 0x47) == '\x01') {
        FUN__text__00505580((int)_UNK_007526f4,(int)_UNK_007526f6,(int)_UNK_007526f8,
                            (int)_UNK_007526fa,(int)_UNK_007526fc,(int)_UNK_007526fe,
                            (int)_UNK_00752700,(int)_UNK_00752702,*(undefined1 *)(local_8 + 0x77),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_007526f4,(int)_UNK_007526f6,(int)_UNK_007526f8,
                            (int)_UNK_007526fa,(int)_UNK_007526fc,(int)_UNK_007526fe,
                            (int)_UNK_00752700,(int)_UNK_00752702);
      }
    }
    if (*(char *)(local_8 + 0x48) != '\0') {
      _local_c = CONCAT31(uStack_b,0x40);
      if ((*(char *)(local_8 + 0x48) == '\x01') || (*(char *)(local_8 + 0x48) == '\x03')) {
        FUN__text__00505580((int)_UNK_00752704,(int)_UNK_00752706,(int)_UNK_00752708,
                            (int)_UNK_0075270a,(int)_UNK_0075270c,(int)_UNK_0075270e,
                            (int)_UNK_00752710,(int)_UNK_00752712,*(undefined1 *)(local_8 + 0x78),
                            0x80,0x80,0x80);
      }
      else {
        FUN__text__00505000((int)_UNK_00752704,(int)_UNK_00752706,(int)_UNK_00752708,
                            (int)_UNK_0075270a,(int)_UNK_0075270c,(int)_UNK_0075270e,
                            (int)_UNK_00752710,(int)_UNK_00752712);
      }
    }
  }
  local_8 = 0x4ec50f;
  FUN__text__0056ce80();
  return;
}

