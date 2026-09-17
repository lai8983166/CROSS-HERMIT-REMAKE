
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN__text__004b8d50(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_64 [16];
  uint local_24;
  uint local_20;
  int local_1c;
  undefined4 local_18;
  undefined2 local_14;
  int local_10;
  undefined4 local_c;
  int local_8;
  
  puVar2 = local_64;
  for (iVar1 = 0x18; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = 0;
  local_10 = FUN__text__0042ae20("data\\menu\\KojinData.bin");
  if (local_10 != 0) {
    FUN__text__00416790(local_10,0xd);
  }
  local_1c = local_10;
  FUN__text__00428ad0(local_10);
  local_14 = 0;
  DAT_007d6a32 = 0;
  local_18 = (uint)local_18._2_2_ << 0x10;
  do {
    local_20 = (uint)DAT_007a4e60;
    if (local_20 == 0) {
      DAT_007a4ae0 = '\x01';
      *(undefined2 *)(local_8 + 0x391da) = 0xffff;
    }
    else if (local_20 == 1) {
      if (DAT_007a4ae0 != '\0') {
        DAT_007a4ae0 = '\0';
        FUN__text__004b5600();
        FUN__text__004b5a00();
      }
      _DAT_007e117a = 0;
      FUN__text__004b5fc0();
      local_18 = local_18 & 0xffff0000;
    }
    else if (local_20 == 2) {
      _DAT_007e117a = 0;
      FUN__text__004b5fc0();
      local_24 = ((local_18 & 0xffff) * 0xff) / 0x1e << 0x18 | 0x10101;
      local_18 = CONCAT22(local_18._2_2_,(short)local_18 + 1);
      FUN__text__004d2620(0,0,0x400,0x300,0,local_24,1);
      if ((local_18 & 0xffff) == 0x1e) {
        DAT_007d6a32 = 0;
        DAT_007a4e60 = 0;
      }
    }
    FUN__text__00422360(0);
  } while (DAT_007a4e60 < 3);
  FUN__text__0041f4e0(0xd);
  local_8 = 0x4b8f17;
  FUN__text__0056ce80();
  return;
}

