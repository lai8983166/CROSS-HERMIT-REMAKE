
void __fastcall FUN__text__004a01a0(int param_1)

{
  int iVar1;
  undefined2 extraout_var;
  undefined4 *puVar2;
  undefined4 local_74 [16];
  int local_34;
  int local_30;
  int local_2c;
  int local_28;
  undefined *local_24;
  short local_20;
  undefined1 local_1c [4];
  uint local_18;
  uint local_10;
  undefined *local_c;
  int local_8;
  
  puVar2 = local_74;
  for (iVar1 = 0x1c; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  *(undefined2 *)(param_1 + 0x48) = *(undefined2 *)(param_1 + 0xc9c8);
  local_8 = param_1;
  for (local_20 = 0;
      (local_20 < 0x29 &&
      ((int)local_20 + (int)*(short *)(local_8 + 0x48) <= *(short *)(local_8 + 0x1457c) + -1));
      local_20 = local_20 + 1) {
    FUN__text__004d5ec0(local_1c,0x3c,local_20 * 0xe + 0x4f,0xb7,0xd);
    if (((local_10 & 0xffff) != 0) &&
       (FUN__text__004d2620(0x3c,local_20 * 0xe + 0x4f,0xb7,0xd,0x38,0x8020a000,2),
       (local_18 & 1) != 0)) {
      FUN__text__004db2b0(5);
      *(undefined2 *)(local_8 + 0x3a) = 1;
      *(undefined2 *)(local_8 + 0x3c) = 0xffff;
      *(short *)(local_8 + 0x46) = local_20 + *(short *)(local_8 + 0x48);
      FUN__text__004d64d0(*(undefined2 *)(local_8 + 0x13dae + *(short *)(local_8 + 0x46) * 4),9);
    }
    if ((int)*(short *)(local_8 + 0x46) == (int)local_20 + (int)*(short *)(local_8 + 0x48)) {
      FUN__text__004d2620(0x3c,local_20 * 0xe + 0x4f,0xb7,0xd,0x38,0xa0c0a000,2);
    }
  }
  for (local_20 = 0; local_20 < 4; local_20 = local_20 + 1) {
    FUN__text__004d5ec0(local_1c,0xf8,local_20 * 0x91 + 0x4e,0x14,0x8d);
    if ((local_18 & 1) != 0) {
      FUN__text__004db2b0(5);
      local_28 = (int)local_20;
      switch(local_28) {
      case 0:
        FUN__text__004d6230(2);
        local_c = &DAT_0061b160;
        break;
      case 1:
        FUN__text__004d6230(0);
        local_c = &DAT_0061b170;
        break;
      case 2:
        FUN__text__004d6230(1);
        local_c = &DAT_0061b180;
        break;
      case 3:
        FUN__text__004d6230(3);
        local_c = &DAT_0061b190;
      }
      FUN__text__004d68b0(local_c,0x3c,0xf6,local_20 * 0x91 + 0x4c,8);
    }
  }
  FUN__text__004d62f0(0x3c,0x4f,0x3c);
  *(undefined2 *)(local_8 + 0x48) = *(undefined2 *)(local_8 + 0xc9c8);
  local_2c = (int)*(short *)(local_8 + 0x3a);
  if (local_2c == 0) {
    for (local_20 = 0; local_20 < 4; local_20 = local_20 + 1) {
      FUN__text__004d5ec0(local_1c,0x3ab,local_20 * 0x22 + 0x232,0x14,0x1e);
      if ((local_18 & 1) != 0) {
        FUN__text__004db2b0(5);
        local_30 = (int)local_20;
        switch(local_30) {
        case 0:
          FUN__text__004d6230(2);
          local_c = &DAT_0061b1a0;
          break;
        case 1:
          FUN__text__004d6230(0);
          local_c = &DAT_0061b1b0;
          break;
        case 2:
          FUN__text__004d6230(1);
          local_c = &DAT_0061b1c0;
          break;
        case 3:
          FUN__text__004d6230(3);
          local_c = &DAT_0061b1d0;
        }
        FUN__text__004d68b0(local_c,0x3c,0x3a9,local_20 * 0x22 + 0x230,8);
      }
    }
    FUN__text__004d62f0(0x120,0x236,0x3c);
  }
  else if (local_2c == 1) {
    for (local_20 = 0; local_20 < 4; local_20 = local_20 + 1) {
      FUN__text__004d5ec0(local_1c,0x3ab,local_20 * 0x22 + 0x232,0x14,0x1e);
      if ((local_18 & 1) != 0) {
        FUN__text__004db2b0(5);
        local_34 = (int)local_20;
        switch(local_34) {
        case 0:
          FUN__text__004d6230(2);
          local_c = &DAT_0061b1a0;
          break;
        case 1:
          FUN__text__004d6230(0);
          local_c = &DAT_0061b1b0;
          break;
        case 2:
          FUN__text__004d6230(1);
          local_c = &DAT_0061b1c0;
          break;
        case 3:
          FUN__text__004d6230(3);
          local_c = &DAT_0061b1d0;
        }
        FUN__text__004d68b0(local_c,0x3c,0x3a9,local_20 * 0x22 + 0x230,8);
      }
    }
    FUN__text__004d62f0(0x120,0x236,0x3c);
  }
  local_24 = &DAT_0061b060;
  FUN__text__004d2700(&DAT_0061b060,1,0x3d,0,0);
  FUN__text__004d2700(&DAT_0061b050,1,0x33,*(undefined2 *)(DAT_007a49fc + 0x196c),
                      CONCAT22(extraout_var,*(undefined2 *)(DAT_007a49fc + 0x1970)));
  FUN__text__004d69e0();
  local_8 = 0x4a0726;
  FUN__text__0056ce80();
  return;
}

