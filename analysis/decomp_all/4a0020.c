
void FUN__text__004a0020(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_60 [16];
  undefined1 local_20 [4];
  uint local_1c;
  undefined2 local_10;
  short local_c;
  undefined4 local_8;
  
  puVar2 = local_60;
  for (iVar1 = 0x17; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_10 = 0;
  for (local_c = 0; local_c < 0x10; local_c = local_c + 1) {
    FUN__text__004d2620(0,0,0x400,0x300,0x34,(0xff - (local_c * 0xff) / 0xf) * 0x1000000 | 0x10101,1
                       );
    FUN__text__0049fff0();
    FUN__text__00422360(0);
  }
  while (FUN__text__004d5ec0(local_20,0x261,0x231,0x15e,0x25), (local_1c & 1) == 0) {
    FUN__text__0049fff0();
    FUN__text__00422360(0);
  }
  local_10 = 1;
  for (local_c = 0; local_c < 0x10; local_c = local_c + 1) {
    FUN__text__004d2620(0,0,0x400,0x300,0x34,(local_c * 0xff) / 0xf << 0x18 | 0x10101,1);
    FUN__text__0049fff0();
    FUN__text__00422360(0);
  }
  local_8 = 0x4a0191;
  FUN__text__0056ce80();
  return;
}

