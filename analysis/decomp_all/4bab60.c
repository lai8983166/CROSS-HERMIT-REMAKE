
void __fastcall FUN__text__004bab60(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_68 [16];
  int local_28;
  short local_24;
  undefined1 local_20 [4];
  uint local_1c;
  short local_10;
  undefined2 local_c;
  int local_8;
  
  puVar2 = local_68;
  for (iVar1 = 0x19; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = 0;
  *(undefined2 *)(param_1 + 0x30) = 0;
  local_8 = param_1;
  do {
    local_28 = (int)*(short *)(local_8 + 0x30);
    switch(local_28) {
    case 0:
      FUN__text__00415420();
      *(undefined2 *)(local_8 + 0x30) = 1;
      break;
    case 1:
      local_24 = DAT_007f450c + -1;
      if (local_24 < 3) {
        FUN__text__004db060(0x17,0);
      }
      else {
        FUN__text__004db060(0x1c,0);
      }
      for (local_10 = 0; local_10 < 0x10; local_10 = local_10 + 1) {
        FUN__text__00422360(0);
        FUN__text__004d2620(0,0,0x400,0x300,0x34,
                            (0xff - (local_10 * 0xff) / 0xf) * 0x1000000 | 0x10101,1);
        FUN__text__004bae30();
      }
      *(undefined2 *)(local_8 + 0x30) = 2;
      break;
    case 2:
      FUN__text__004bae30();
      FUN__text__004d5ec0(local_20,0x175,0x2c8,299,0x1c);
      if ((local_1c & 1) != 0) {
        FUN__text__004db2b0(5);
        *(undefined2 *)(local_8 + 0x30) = 3;
      }
      break;
    case 3:
      for (local_10 = 0; local_10 < 8; local_10 = local_10 + 1) {
        FUN__text__004d2700(&DAT_0061c3a0,1,0x54,0x169,0x2c4);
        FUN__text__004bae30();
        FUN__text__00422360(0);
      }
      for (local_10 = 0; local_10 < 0x10; local_10 = local_10 + 1) {
        FUN__text__004d2620(0,0,0x400,0x300,0x34,(local_10 * 0xff) / 0xf << 0x18 | 0x10101,1);
        FUN__text__004bae30();
        FUN__text__00422360(0);
      }
      FUN__text__004db230(0x5a);
      while (iVar1 = FUN__text__004db270(), iVar1 == 0) {
        FUN__text__00422360(0);
      }
      FUN__text__004db120();
      *(undefined2 *)(local_8 + 0x30) = 4;
    }
    FUN__text__00422360(0);
  } while (*(short *)(local_8 + 0x30) != 4);
  local_8 = 0x4bae18;
  FUN__text__0056ce80();
  return;
}

