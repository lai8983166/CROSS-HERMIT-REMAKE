
void __fastcall FUN__text__004d8620(int param_1)

{
  undefined2 uVar1;
  undefined4 uVar2;
  undefined2 extraout_var;
  undefined2 extraout_var_00;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_49c [16];
  int local_45c;
  int local_458;
  uint local_454;
  undefined4 local_450;
  undefined1 local_44c [200];
  short local_384;
  short local_380;
  short local_37c;
  short local_378;
  undefined4 local_374;
  undefined1 local_370 [200];
  short local_2a8;
  undefined2 local_2a4;
  short local_2a0;
  short local_29c;
  undefined *local_298;
  undefined1 local_294 [200];
  undefined4 local_1cc;
  ushort local_1c8;
  ushort uStack_1c6;
  ushort local_1c2;
  ushort uStack_1c0;
  ushort local_1be;
  ushort uStack_1bc;
  undefined1 local_1b8 [16];
  char local_1a8;
  char local_1a7;
  char local_1a6;
  char local_1a5;
  char local_1a4;
  char local_1a3;
  char local_1a2;
  char local_1a1;
  char local_1a0;
  char local_19f;
  char local_19e;
  char local_19d;
  char local_19c;
  char local_19b;
  undefined1 local_f0 [200];
  short local_28;
  short local_24;
  undefined2 local_20;
  int local_1c;
  undefined1 local_18 [4];
  uint local_14;
  uint local_c;
  int local_8;
  
  puVar4 = local_49c;
  for (iVar3 = 0x126; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_20 = 0;
  local_24 = 0;
  local_28 = 1;
  *(undefined2 *)(param_1 + 0x19aac) = 0;
  *(undefined2 *)(param_1 + 0x2c726) = 0xffff;
  local_8 = param_1;
  do {
    local_454 = (int)local_28 - 1;
    if (local_454 < 0xc) {
      uVar1 = (undefined2)(local_454 >> 0x10);
      switch(local_454) {
      case 0:
        (*API_KERNEL32_DLL_GetLocalTime)(&local_1c8);
        FUN__text__0056ce80();
        FUN__text__0056cd90(local_1b8,&DAT_005c8368);
        local_1a8 = (char)(((ulonglong)local_1c8 / 1000) % 10) + '0';
        local_1a7 = (char)(((ulonglong)local_1c8 / 100) % 10) + '0';
        local_1a6 = (char)(((ulonglong)local_1c8 / 10) % 10) + '0';
        local_1a5 = (char)((ulonglong)local_1c8 % 10) + '0';
        local_1a4 = (char)(((ulonglong)uStack_1c6 / 10) % 10) + '0';
        local_1a3 = (char)((ulonglong)uStack_1c6 % 10) + '0';
        local_1a2 = (char)(((ulonglong)local_1c2 / 10) % 10) + '0';
        local_1a1 = (char)((ulonglong)local_1c2 % 10) + '0';
        local_1a0 = (char)(((ulonglong)uStack_1c0 / 10) % 10) + '0';
        local_19f = (char)((ulonglong)uStack_1c0 % 10) + '0';
        local_19e = (char)(((ulonglong)local_1be / 10) % 10) + '0';
        local_19d = (char)((ulonglong)local_1be % 10) + '0';
        local_19c = (char)(((ulonglong)uStack_1bc / 10) % 10) + '0';
        local_19b = (char)((ulonglong)uStack_1bc % 10) + '0';
        FUN__text__004d60e0(1);
        FUN__text__004d6150(local_1b8);
        local_28 = 2;
        break;
      case 1:
        for (local_1c = 0; local_1c < 0x1e; local_1c = local_1c + 1) {
          FUN__text__004d2620(0,0,0x400,0x300,0x51,
                              (0xff - (local_1c * 0xff) / 0x1d) * 0x1000000 | 0x10101,1);
          FUN__text__004d9990();
          FUN__text__00422360(0);
        }
        local_28 = 3;
        break;
      case 2:
        for (local_1c = 0; local_1c < 0x20; local_1c = local_1c + 1) {
          FUN__text__004d7a80(1);
          FUN__text__004d9990();
          FUN__text__00422360(0);
        }
        local_1cc = FUN__text__00450230("*.sav");
        FUN__text__004d60e0(0x16);
        FUN__text__004d6cb0(local_1cc);
        local_28 = 5;
        *(undefined2 *)(local_8 + 0x2c726) = 0xffff;
        *(undefined2 *)(local_8 + 0x2c728) = 0;
        break;
      case 3:
        for (local_1c = 0; local_1c < 0x1e; local_1c = local_1c + 1) {
          FUN__text__004d2620(0,0,0x400,0x300,0x51,
                              (0xff - ((0x1d - local_1c) * 0xff) / 0x1d) * 0x1000000 | 0x10101,1);
          FUN__text__004d9990();
          FUN__text__00422360(0);
        }
        local_24 = 1;
        break;
      case 4:
        for (local_1c = 0;
            (local_1c < 0x16 &&
            (local_1c + *(short *)(local_8 + 0x2c728) <= *(short *)(local_8 + 0x19aac) + -1));
            local_1c = local_1c + 1) {
          FUN__text__004d5ec0(local_18,0xb0,local_1c * 0xe + 0x132,0x294,0xd);
          if (((local_c & 0xffff) != 0) &&
             (FUN__text__004d2620(0xad,local_1c * 0xe + 0x132,0x298,0xd,0x58,0x8020a000,2),
             (local_14 & 1) != 0)) {
            *(short *)(local_8 + 0x2c726) = (short)local_1c + *(short *)(local_8 + 0x2c728);
            FUN__text__004db2b0(5);
            FUN__text__0056cd90(local_1b8,local_8 + 0x14c + *(short *)(local_8 + 0x2c726) * 0x20c);
            FUN__text__004d60e0(1);
            FUN__text__004d6150(local_1b8);
          }
          if ((int)*(short *)(local_8 + 0x2c726) == local_1c + *(short *)(local_8 + 0x2c728)) {
            FUN__text__004d2620(0xad,local_1c * 0xe + 0x132,0x298,0xd,0x57,0xa0c0a000,2);
          }
        }
        FUN__text__004d5ec0(local_18,0xaa,0xb7,0x2b5,0x12);
        if (((local_c & 0xffff) != 0) && ((local_14 & 1) != 0)) {
          FUN__text__004db2b0(5);
          FUN__text__004d60e0(1);
          local_28 = 0xb;
          *(undefined2 *)(local_8 + 0x2c726) = 0xffff;
          FUN__text__00425a10();
          FUN__text__004262a0(0x40);
          FUN__text__00426310(local_1b8);
          FUN__text__00425ed0(1);
        }
        FUN__text__004d5ec0(local_18,0xe3,0xf3,0x8d,0x1f);
        if (((local_c & 0xffff) != 0) && ((local_14 & 1) != 0)) {
          FUN__text__004db2b0(5);
          FUN__text__004d68b0(&DAT_00625708,0x5a,0xd9,0xf1,8);
          local_28 = 6;
        }
        FUN__text__004d5ec0(local_18,0x1bc,0xf3,0x8d,0x1f);
        if ((((local_c & 0xffff) != 0) && ((local_14 & 1) != 0)) &&
           (*(short *)(local_8 + 0x2c726) != -1)) {
          FUN__text__004d68b0(&DAT_00625718,0x5a,0x1b2,0xf1,8);
          local_28 = 8;
          FUN__text__004db2b0(5);
        }
        FUN__text__004d5ec0(local_18,0x295,0xf3,0x8d,0x1f);
        if (((local_c & 0xffff) == 0) || ((local_14 & 1) == 0)) {
          for (local_1c = 0; local_1c < 4; local_1c = local_1c + 1) {
            FUN__text__004d5ec0(local_18,0x34b,local_1c * 0x4f + 0x12e,0x14,0x4b);
            if (((local_c & 0xffff) != 0) && ((local_14 & 1) != 0)) {
              FUN__text__004db2b0(5);
              local_458 = local_1c;
              switch(local_1c) {
              case 0:
                uVar1 = FUN__text__004d6230(2);
                *(undefined2 *)(local_8 + 0x2c728) = uVar1;
                local_298 = &DAT_006256c8;
                break;
              case 1:
                uVar1 = FUN__text__004d6230(0);
                *(undefined2 *)(local_8 + 0x2c728) = uVar1;
                local_298 = &DAT_006256d8;
                break;
              case 2:
                uVar1 = FUN__text__004d6230(1);
                *(undefined2 *)(local_8 + 0x2c728) = uVar1;
                local_298 = &DAT_006256e8;
                break;
              case 3:
                uVar1 = FUN__text__004d6230(3);
                *(undefined2 *)(local_8 + 0x2c728) = uVar1;
                local_298 = &DAT_006256f8;
              }
              FUN__text__004d68b0(local_298,0x5a,0x349,local_1c * 0x4f + 300,8);
            }
          }
          FUN__text__004d9990();
          FUN__text__00422360(0);
        }
        else {
          FUN__text__004db2b0(1);
          FUN__text__004d68b0(&DAT_00625728,0x5a,0x28b,0xf1,8);
          local_28 = 4;
          DAT_007e11aa = 0;
        }
        break;
      case 5:
        FUN__text__0056cd90(local_370,local_1b8);
        FUN__text__0056cda0(local_370,&DAT_005c8320);
        local_374 = FUN__text__00450230(local_370);
        FUN__text__0056cd90(local_f0,local_374);
        local_45c = FUN__text__0042a8e0(local_374);
        if (local_45c == 0) {
          local_28 = 9;
        }
        else if (local_45c == 1) {
          local_28 = 7;
        }
        FUN__text__004d9990();
        FUN__text__00422360(0);
        break;
      case 6:
        local_378 = 0x179;
        local_37c = 0x192;
        FUN__text__004d2700(&DAT_00625758,1,0x54,CONCAT22(local_28 >> 0xf,0x179),
                            CONCAT22(uVar1,0x192));
        FUN__text__004d5ec0(local_18,local_378 + 0x1c,local_37c + 0x34,0x66,0x1d);
        if (((local_c & 0xffff) != 0) && ((local_14 & 1) != 0)) {
          FUN__text__004db2b0(5);
          local_28 = 9;
        }
        FUN__text__004d5ec0(local_18,local_378 + 0x8c,local_37c + 0x34,0x66,0x1d);
        if (((local_c & 0xffff) != 0) && ((local_14 & 1) != 0)) {
          FUN__text__004db2b0(1);
          local_28 = 5;
        }
        FUN__text__004d2620(0xe3,0xf3,0x8d,0x1f,0x52,0xa0010101,1);
        if (*(short *)(local_8 + 0x2c726) != -1) {
          FUN__text__004d2620(0x1bc,0xf3,0x8d,0x1f,0x52,0xa0010101,1);
        }
        FUN__text__004d2620(0x295,0xf3,0x8d,0x1f,0x52,0xa0010101,1);
        FUN__text__004d2620(0xaa,300,0x2b7,0x13d,0x55,0xc0101010,1);
        FUN__text__004d9990();
        FUN__text__00422360(0);
        break;
      case 7:
        local_380 = 0x179;
        local_384 = 0x192;
        FUN__text__004d2700(&DAT_00625788,1,0x54,CONCAT22(local_28 >> 0xf,0x179),
                            CONCAT22(uVar1,0x192));
        FUN__text__004d5ec0(local_18,local_380 + 0x1c,local_384 + 0x34,0x66,0x1d);
        if (((local_c & 0xffff) != 0) && ((local_14 & 1) != 0)) {
          FUN__text__004db2b0(5);
          local_28 = 10;
        }
        FUN__text__004d5ec0(local_18,local_380 + 0x8c,local_384 + 0x34,0x66,0x1d);
        if (((local_c & 0xffff) != 0) && ((local_14 & 1) != 0)) {
          FUN__text__004db2b0(1);
          local_28 = 5;
        }
        FUN__text__004d2620(0xe3,0xf3,0x8d,0x1f,0x52,0xa0010101,1);
        if (*(short *)(local_8 + 0x2c726) != -1) {
          FUN__text__004d2620(0x1bc,0xf3,0x8d,0x1f,0x52,0xa0010101,1);
        }
        FUN__text__004d2620(0x295,0xf3,0x8d,0x1f,0x52,0xa0010101,1);
        FUN__text__004d2620(0xaa,300,0x2b7,0x13d,0x55,0xc0101010,1);
        FUN__text__004d9990();
        FUN__text__00422360(0);
        break;
      case 8:
        FUN__text__004d7720(local_f0);
        FUN__text__004d9990();
        FUN__text__00422360(0);
        local_28 = 3;
        break;
      case 9:
        FUN__text__0056cd90(local_44c,local_1b8);
        FUN__text__0056cda0(local_44c,&DAT_005c8320);
        local_450 = FUN__text__00450230(local_44c);
        FUN__text__0056cd90(local_f0,local_450);
        FUN__text__0042afc0(local_f0);
        FUN__text__004d9990();
        FUN__text__00422360(0);
        local_28 = 3;
        break;
      case 10:
        FUN__text__004d2620(0xaa,0xb7,0x2b5,0x12,0x5b,0x3820a000,2);
        iVar3 = FUN__text__004263b0(DAT_007a49fc);
        if (iVar3 != 0) {
          uVar2 = FUN__text__004264d0();
          FUN__text__0056cd90(local_294,uVar2);
          iVar3 = FUN__text__00429b40(local_294);
          if (iVar3 == 0) {
            FUN__text__004d60e0(1);
            FUN__text__004d6150(local_1b8);
            FUN__text__004d60e0(5);
            FUN__text__004d6150("       \\ / : * ? \" < > |     ");
            FUN__text__004d6150(&DAT_005c8330);
            FUN__text__004db2b0(1);
            local_28 = 0xc;
          }
          else {
            FUN__text__0056cd90(local_1b8,local_294);
            FUN__text__004d60e0(1);
            FUN__text__004d6150(local_1b8);
            FUN__text__00425ed0(0);
            local_28 = 5;
            FUN__text__004db2b0(5);
          }
        }
        FUN__text__004d5ec0(local_18,0x295,0xf3,0x8d,0x1f);
        if (((local_c & 0xffff) == 0) || ((local_14 & 1) == 0)) {
          iVar3 = FUN__text__00425c70();
          if (iVar3 == 0) {
            FUN__text__004d7a80(3);
          }
          else {
            FUN__text__004d7a80(2);
          }
          FUN__text__00426820(DAT_007a49fc,0xb0,0xba,0xc,0,local_8 + 0x30,local_8 + 0xbc,0);
          FUN__text__004d2620(0xe3,0xf3,0x8d,0x1f,0x52,0xa0010101,1);
          FUN__text__004d9990();
          FUN__text__00422360(0);
        }
        else {
          FUN__text__004db2b0(1);
          FUN__text__004d68b0(&DAT_00625728,0x5a,0x28b,0xf1,8);
          local_28 = 4;
          DAT_007e11aa = 0;
        }
        break;
      case 0xb:
        *(undefined2 *)(local_8 + 0x2c724) = 0xffff;
        local_29c = 0x179;
        local_2a0 = 0x192;
        FUN__text__004d2700(&DAT_006257c8,1,0x54,CONCAT22(uVar1,0x179),CONCAT22(uVar1,0x192));
        FUN__text__004d5ec0(local_18,local_29c + 0x1c,local_2a0 + 0x34,0xd7,0x1d);
        uVar1 = extraout_var;
        if (((local_c & 0xffff) != 0) && (uVar1 = 0, (local_14 & 1) != 0)) {
          FUN__text__004db2b0(5);
          local_28 = 5;
          uVar1 = extraout_var_00;
        }
        local_2a4 = (undefined2)(local_29c + 5);
        local_2a8 = local_2a0 + 10;
        FUN__text__004d62f0(local_29c + 5,CONCAT22(uVar1,local_2a8),0x53);
        FUN__text__004d2620(0xaa,300,0x2b7,0x13d,0x55,0xc0101010,1);
        FUN__text__004d2620(0xe3,0xf3,0x8d,0x1f,0x52,0xa0010101,1);
        if (*(short *)(local_8 + 0x2c726) != -1) {
          FUN__text__004d2620(0x1bc,0xf3,0x8d,0x1f,0x52,0xa0010101,1);
        }
        FUN__text__004d2620(0x295,0xf3,0x8d,0x1f,0x52,0xa0010101,1);
        FUN__text__004d9990();
        FUN__text__00422360(0);
      }
    }
  } while (local_24 == 0);
  local_8 = 0x4d9834;
  FUN__text__0056ce80();
  return;
}

