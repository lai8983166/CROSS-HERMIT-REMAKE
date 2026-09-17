
void __fastcall FUN__text__004a5440(int param_1)

{
  undefined4 *puVar1;
  undefined2 extraout_var;
  undefined2 extraout_var_00;
  int iVar2;
  undefined4 local_8c [16];
  undefined1 local_4c [16];
  undefined4 local_3c;
  undefined4 local_38;
  undefined4 local_34;
  undefined2 local_30;
  undefined1 local_2c;
  undefined1 local_28;
  short local_24;
  short local_20;
  short local_1c;
  undefined1 local_18 [4];
  uint local_14;
  uint local_c;
  int local_8;
  
  puVar1 = local_8c;
  for (iVar2 = 0x22; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar1 = 0xcccccccc;
    puVar1 = puVar1 + 1;
  }
  local_24 = 0;
  local_2c = 0;
  local_8 = param_1;
  for (local_1c = 0; local_1c < 5; local_1c = local_1c + 1) {
    if (*(short *)(&DAT_007aaa12 + local_1c * 0x1c) != -1) {
      if ((*(short *)(&DAT_007aaa18 + local_1c * 0x1c) != -1) &&
         (*(short *)(&DAT_007aaa1a + local_1c * 0x1c) != -1)) {
        FUN__text__004aa6c0(0x60,local_1c * 0x61 + 0x96,
                            CONCAT22((short)((uint)(local_1c * 0x1c) >> 0x10),
                                     *(undefined2 *)(&DAT_007aaa18 + local_1c * 0x1c)),
                            CONCAT22((short)((uint)(local_1c * 0x1c) >> 0x10),
                                     *(undefined2 *)(&DAT_007aaa1a + local_1c * 0x1c)),0xff,0x73);
      }
      for (local_20 = 0; local_20 < 4; local_20 = local_20 + 1) {
        if (*(short *)(&DAT_007aaa22 + local_20 * 2 + local_1c * 0x1c) != -1) {
          local_28 = 0xff;
          FUN__text__004d5ec0(local_18,local_20 * 0x4e + 0xe0,local_1c * 0x61 + 0x53,0x44,0x40);
          if ((*(short *)(local_8 + 0x76c6) == 0) && ((local_c & 0xffff) != 0)) {
            *(undefined1 *)(local_8 + 0x76c2) = 1;
            local_28 = 0x80;
            if ((local_14 & 2) != 0) {
              FUN__text__004db2b0(5);
              if (DAT_007d57c6 == 0) {
                DAT_007d57ca = local_1c;
              }
              DAT_007d57c6 = (ushort)(DAT_007d57c6 == 0);
              DAT_007d57c4 = 0;
              DAT_007d57c8 = *(undefined2 *)(&DAT_007aaa22 + local_20 * 2 + local_1c * 0x1c);
              DAT_007d57cc = local_20 * 0x4e + 0x131;
              DAT_007d57ce = local_1c * 0x61 + 0x4c;
              DAT_007d57d0 = local_20 * 0x4e + 0xe0;
              DAT_007d57d2 = local_1c * 0x61 + 0x53;
              DAT_007d57d4 = 0x44;
              DAT_007d57d6 = 0x40;
            }
            if ((local_14 & 1) != 0) {
              DAT_007d598f = 1;
              DAT_007d598e = '\0';
              DAT_007d5990 = local_1c;
              DAT_007d5992 = local_20;
              DAT_007d57c2 = *(short *)(&DAT_007aaa22 + local_20 * 2 + local_1c * 0x1c);
              DAT_007d5994 = DAT_007d57c2;
              puVar1 = (undefined4 *)
                       FUN__text__004a95f0(local_4c,CONCAT22(local_20 >> 0xf,local_1c));
              local_3c = *puVar1;
              local_38 = puVar1[1];
              local_34 = puVar1[2];
              local_30 = *(undefined2 *)(puVar1 + 3);
              DAT_007d5996 = (undefined2)local_38;
              FUN__text__004d48a0(CONCAT22((short)((uint)local_34 >> 0x10),DAT_007d5994),9,5,0);
              *(undefined2 *)(local_8 + 0x76c6) = 6;
            }
          }
          if ((((*(short *)(local_8 + 0x76c6) == 6) && (DAT_007d598e == '\0')) &&
              (DAT_007d5990 == local_1c)) && (DAT_007d5992 == local_20)) {
            local_28 = 0x80;
          }
          if (DAT_007d57c2 == *(short *)(&DAT_007aaa22 + local_20 * 2 + local_1c * 0x1c)) {
            FUN__text__004d2700(&DAT_0061b418,1,0x71,local_20 * 0x4e + 0xd8,local_1c * 0x61 + 0x4c);
          }
          local_24 = *(short *)(&DAT_007aaa22 + local_20 * 2 + local_1c * 0x1c) + -1;
          FUN__text__004aadb0(local_20 * 0x4e + 0xdc,local_1c * 0x61 + 0x4f,0,
                              CONCAT22(local_20 >> 0xf,local_24),0xff,
                              CONCAT31((int3)((uint)(local_1c * 0x1c) >> 8),local_28),0x77);
          FUN__text__004aaf60(local_20 * 0x4e + 0xe0,local_1c * 0x61 + 0x9a,0,
                              CONCAT22(extraout_var,local_24),local_28,0x77);
          FUN__text__004aacf0(local_20 * 0x4e + 0xdc,local_1c * 0x61 + 0x4f,
                              (byte)(&DAT_006b2d8a)
                                    [*(short *)(&DAT_007e17ee + (local_24 + 1) * 0x4a0) * 0x40] - 1,
                              local_28,0x76);
        }
      }
    }
  }
  for (local_1c = 0; local_1c < 5; local_1c = local_1c + 1) {
    if (*(short *)(&DAT_007aaa12 + local_1c * 0x1c) != -1) {
      local_28 = 0xff;
      FUN__text__004d5ec0(local_18,0x10,local_1c * 0x61 + 0x53,0x44,0x40);
      if ((*(short *)(local_8 + 0x76c6) == 0) && ((local_c & 0xffff) != 0)) {
        *(undefined1 *)(local_8 + 0x76c2) = 1;
        local_28 = 0x80;
        if ((local_14 & 1) != 0) {
          FUN__text__004db2b0(5);
          DAT_007d598f = 1;
          DAT_007d598e = '\x01';
          DAT_007d5990 = local_1c;
          DAT_007d5992 = -1;
          DAT_007d5994 = *(short *)(&DAT_007aaa12 + local_1c * 0x1c);
          *(undefined2 *)(local_8 + 0x76c6) = 6;
        }
      }
      if (((*(short *)(local_8 + 0x76c6) == 6) && (DAT_007d598e == '\x01')) &&
         (DAT_007d5990 == local_1c)) {
        local_28 = 0x80;
      }
      if (*(short *)(&DAT_007aaa12 + local_1c * 0x1c) != -1) {
        local_24 = *(short *)(&DAT_007aaa12 + local_1c * 0x1c) + -0x65;
        FUN__text__004aadb0(0xc,local_1c * 0x61 + 0x4f,1,
                            CONCAT22((short)((uint)(local_1c * 0x1c) >> 0x10),local_24) & 0xffff00ff
                            ,0xff,CONCAT31((int3)(char)((ushort)*(short *)(&DAT_007aaa12 +
                                                                          local_1c * 0x1c) >> 8),
                                           local_28),0x77);
        FUN__text__004aaf60(0x10,local_1c * 0x61 + 0x9a,1,
                            CONCAT22(extraout_var_00,local_24) & 0xffff00ff,local_28,0x77);
      }
    }
  }
  local_8 = 0x4a5a53;
  FUN__text__0056ce80();
  return;
}

