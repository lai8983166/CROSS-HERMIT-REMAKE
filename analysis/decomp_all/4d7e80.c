
void __fastcall FUN__text__004d7e80(int param_1)

{
  undefined2 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_210 [16];
  uint local_1d0;
  int local_1cc;
  int local_1c8;
  undefined4 local_1c4;
  undefined1 local_1c0 [200];
  undefined1 local_f8 [200];
  undefined *local_30;
  undefined4 local_2c;
  short local_28;
  short local_24;
  undefined2 local_20;
  int local_1c;
  undefined1 local_18 [4];
  uint local_14;
  uint local_c;
  int local_8;
  
  puVar3 = local_210;
  for (iVar2 = 0x83; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_20 = 0;
  local_24 = 0;
  local_28 = 1;
  *(undefined2 *)(param_1 + 0x19aac) = 0;
  *(undefined2 *)(param_1 + 0x2c726) = 0xffff;
  local_8 = param_1;
  do {
    local_1c8 = local_28 + -1;
    switch(local_1c8) {
    case 0:
      local_28 = 2;
      break;
    case 1:
      for (local_1c = 0; local_1c < 0x1e; local_1c = local_1c + 1) {
        FUN__text__004d2620(0,0,0x400,0x300,0x51,
                            (0xff - (local_1c * 0xff) / 0x1d) * 0x1000000 | 0x10101,1);
        FUN__text__004d98b0();
        FUN__text__00422360(0);
      }
      local_28 = 3;
      break;
    case 2:
      for (local_1c = 0; local_1c < 0x20; local_1c = local_1c + 1) {
        FUN__text__004d7a80(0);
        FUN__text__004d98b0();
        FUN__text__00422360(0);
      }
      local_2c = FUN__text__00450230("*.sav");
      FUN__text__004d60e0(0x1e);
      FUN__text__004d6cb0(local_2c);
      local_28 = 5;
      *(undefined2 *)(local_8 + 0x2c726) = 0xffff;
      *(undefined2 *)(local_8 + 0x2c728) = 0;
      break;
    case 3:
      for (local_1c = 0; local_1c < 0x1e; local_1c = local_1c + 1) {
        FUN__text__004d2620(0,0,0x400,0x300,0x51,
                            (0xff - ((0x1d - local_1c) * 0xff) / 0x1d) * 0x1000000 | 0x10101,1);
        FUN__text__004d98b0();
        FUN__text__00422360(0);
      }
      local_24 = 1;
      break;
    case 4:
      for (local_1c = 0;
          (local_1c < 0x1e &&
          (local_1c + *(short *)(local_8 + 0x2c728) <= *(short *)(local_8 + 0x19aac) + -1));
          local_1c = local_1c + 1) {
        FUN__text__004d5ec0(local_18,0xb0,local_1c * 0xe + 0xbe,0x294,0xd);
        if (((local_c & 0xffff) != 0) &&
           (FUN__text__004d2620(0xad,local_1c * 0xe + 0xbe,0x298,0xd,0x58,0x8020a000,2),
           (local_14 & 1) != 0)) {
          FUN__text__004db2b0(5);
          *(short *)(local_8 + 0x2c726) = (short)local_1c + *(short *)(local_8 + 0x2c728);
        }
        if ((int)*(short *)(local_8 + 0x2c726) == local_1c + *(short *)(local_8 + 0x2c728)) {
          FUN__text__004d2620(0xad,local_1c * 0xe + 0xbe,0x298,0xd,0x57,0xa0c0a000,2);
        }
      }
      FUN__text__004d5ec0(local_18,0x237,0x272,0x8d,0x1f);
      if (((local_c & 0xffff) == 0) || ((local_14 & 1) == 0)) {
        FUN__text__004d5ec0(local_18,0x140,0x272,0x8d,0x1f);
        if (((local_c & 0xffff) != 0) &&
           (((local_14 & 1) != 0 && (FUN__text__004db2b0(5), -1 < *(short *)(local_8 + 0x2c726)))))
        {
          FUN__text__004d68b0(&DAT_00625698,0x5a,0x136,0x270,8);
          DAT_007e11a0 = 0;
          local_28 = 6;
        }
        for (local_1c = 0; local_1c < 4; local_1c = local_1c + 1) {
          FUN__text__004d5ec0(local_18,0x34b,local_1c * 0x6d + 0xb7,0x14,0x69);
          if (((local_c & 0xffff) != 0) && ((local_14 & 1) != 0)) {
            FUN__text__004db2b0(5);
            local_1cc = local_1c;
            switch(local_1c) {
            case 0:
              uVar1 = FUN__text__004d6230(2);
              *(undefined2 *)(local_8 + 0x2c728) = uVar1;
              local_30 = &DAT_00625658;
              break;
            case 1:
              uVar1 = FUN__text__004d6230(0);
              *(undefined2 *)(local_8 + 0x2c728) = uVar1;
              local_30 = &DAT_00625668;
              break;
            case 2:
              uVar1 = FUN__text__004d6230(1);
              *(undefined2 *)(local_8 + 0x2c728) = uVar1;
              local_30 = &DAT_00625678;
              break;
            case 3:
              uVar1 = FUN__text__004d6230(3);
              *(undefined2 *)(local_8 + 0x2c728) = uVar1;
              local_30 = &DAT_00625688;
            }
            FUN__text__004d68b0(local_30,0x5a,0x349,local_1c * 0x6d + 0xb5,8);
          }
        }
        FUN__text__004d98b0();
        FUN__text__00422360(0);
      }
      else {
        FUN__text__004db2b0(1);
        FUN__text__004d68b0(&DAT_006256a8,0x5a,0x22d,0x270,8);
        local_28 = 4;
        DAT_007e11aa = 0;
      }
      break;
    case 5:
      FUN__text__0056cd90(local_1c0,local_8 + 0x14c + *(short *)(local_8 + 0x2c726) * 0x20c);
      FUN__text__0056cda0(local_1c0,&DAT_005c8320);
      local_1c4 = FUN__text__00450230(local_1c0);
      FUN__text__0056cd90(local_f8,local_1c4);
      FUN__text__004d75a0(local_f8,&DAT_007a50e8,1,1);
      FUN__text__004e1d70();
      FUN__text__0049e8f0();
      local_28 = 7;
      local_1d0 = (uint)DAT_007e11a8;
      switch(local_1d0) {
      case 0:
      case 1:
      case 5:
        DAT_007e11aa = 1;
        break;
      case 6:
        DAT_007e11aa = 3;
      }
      FUN__text__004d98b0();
      FUN__text__00422360(0);
      break;
    case 6:
      for (local_1c = 0; local_1c < 0x1e; local_1c = local_1c + 1) {
        FUN__text__004d2620(0,0,0x400,0x300,0x51,
                            (0xff - ((0x1d - local_1c) * 0xff) / 0x1d) * 0x1000000 | 0x10101,1);
        FUN__text__004d98b0();
        FUN__text__00422360(0);
      }
      local_24 = 1;
    }
  } while (local_24 == 0);
  local_8 = 0x4d85ce;
  FUN__text__0056ce80();
  return;
}

