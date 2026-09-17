
void __fastcall FUN__text__004a0760(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_74 [16];
  short local_34;
  short local_30;
  short local_2c;
  short local_28;
  undefined *local_24;
  undefined1 local_20 [4];
  uint local_1c;
  undefined2 local_10;
  short local_c;
  int local_8;
  
  puVar2 = local_74;
  for (iVar1 = 0x1c; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_10 = 0;
  local_8 = param_1;
  FUN__text__00409ff0(param_1 + 0xa4,0,4,0);
  *(undefined2 *)(local_8 + 0x3a) = 0;
  *(undefined2 *)(local_8 + 0x46) = 0xffff;
  *(undefined2 *)(local_8 + 0x3c) = 0xffff;
  FUN__text__004d6710();
  FUN__text__004d64d0(0,9);
  for (local_c = 0; local_c < 0x10; local_c = local_c + 1) {
    FUN__text__004d2620(0,0,0x400,0x300,0x34,(0xff - (local_c * 0xff) / 0xf) * 0x1000000 | 0x10101,1
                       );
    FUN__text__004a01a0();
    FUN__text__00422360(0);
  }
  while( true ) {
    FUN__text__004a0ad0();
    if (*(short *)(local_8 + 0x34) != -1) {
      local_24 = &DAT_0061b1e0;
      local_28 = *(short *)(local_8 + 0x34) / 0x14;
      local_2c = *(short *)(local_8 + 0x34) % 0x14;
      FUN__text__004d2790(&DAT_0061b1e0,1,0x3c,*(undefined2 *)(local_8 + 0x36),
                          CONCAT22((short)((uint)(local_2c * 0x32) >> 0x10),
                                   *(undefined2 *)(local_8 + 0x38)),local_28 * 200,local_2c * 0x32);
    }
    if (*(short *)(local_8 + 0x3c) != -1) {
      local_24 = &DAT_0061b1e0;
      local_30 = *(short *)(local_8 + 0x3c) / 0x14;
      local_34 = *(short *)(local_8 + 0x3c) % 0x14;
      FUN__text__004d2790(&DAT_0061b1e0,1,0x3c,*(undefined2 *)(local_8 + 0x3e),
                          CONCAT22((short)((uint)(local_34 * 0x32) >> 0x10),
                                   *(undefined2 *)(local_8 + 0x40)),local_30 * 200,local_34 * 0x32);
      FUN__text__0040a100(local_8 + 0xa4);
      FUN__text__0040a330(local_8 + 0xa4,local_8 + 0xfc,(int)*(short *)(local_8 + 0x42),
                          (int)*(short *)(local_8 + 0x44),0x3b);
    }
    FUN__text__004d5ec0(local_20,0x42,0x299,0xc2,0x1c);
    if ((local_1c & 1) != 0) break;
    FUN__text__004a01a0();
    FUN__text__00422360(0);
  }
  FUN__text__004db2b0(5);
  local_10 = 1;
  local_24 = &DAT_0061b150;
  FUN__text__004d68b0(&DAT_0061b150,0x3c,0x36,0x295,8);
  for (local_c = 0; local_c < 4; local_c = local_c + 1) {
    FUN__text__004a01a0();
    FUN__text__00422360(0);
  }
  for (local_c = 0; local_c < 0x10; local_c = local_c + 1) {
    FUN__text__004d2620(0,0,0x400,0x300,0x34,(local_c * 0xff) / 0xf << 0x18 | 0x10101,1);
    FUN__text__004a01a0();
    FUN__text__00422360(0);
  }
  local_8 = 0x4a0ac1;
  FUN__text__0056ce80();
  return;
}

