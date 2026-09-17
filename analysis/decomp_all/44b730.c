
void FUN__text__0044b730(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_64 [16];
  short local_24;
  undefined2 local_20;
  short local_1c;
  short local_18;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_64;
  for (iVar1 = 0x18; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = FUN__text__0041ae70();
  local_10 = local_8 + 0x1a54;
  local_20 = 0x239;
  local_24 = 0x24a;
  local_18 = 0x256;
  local_1c = 0x24d;
  for (local_14 = 0; local_14 != 4; local_14 = local_14 + 1) {
    if (*(char *)(local_c + local_14 * 0x88) != '\0') {
      if (*(char *)(local_c + 1 + local_14 * 0x88) != '\0') {
        FUN__text__0044cb40(local_8 + 0x38,
                            CONCAT22((short)((uint)(&DAT_006065b8 + local_14 * 8) >> 0x10),local_20)
                            ,(int)local_24 + local_14 * 0x19,0x55,5,&DAT_006065b8 + local_14 * 8);
      }
      *(undefined2 *)(local_8 + 0xc2e + local_14 * 0x80) = 0x55;
      FUN__text__00408f10((int)local_18,(int)local_1c + local_14 * 0x19,0xffffffff);
      FUN__text__0044cc80(0x36e,local_1c + 2 + local_14 * 0x19,0x55,
                          (int)*(char *)(local_10 + local_14 + 0x41),2);
      FUN__text__0044cc80(0x3b8,local_1c + 2 + local_14 * 0x19,0x55,
                          (int)*(short *)(local_10 + 0x46 + local_14 * 2),4);
    }
  }
  local_8 = 0x44b8a2;
  FUN__text__0056ce80();
  return;
}

