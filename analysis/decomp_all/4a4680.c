
void __fastcall FUN__text__004a4680(int param_1)

{
  short sVar1;
  undefined2 extraout_var;
  undefined2 extraout_var_00;
  undefined2 extraout_var_01;
  uint uVar2;
  int iVar3;
  undefined2 extraout_var_02;
  undefined2 extraout_var_03;
  undefined2 extraout_var_04;
  undefined2 extraout_var_05;
  undefined2 extraout_var_06;
  undefined2 extraout_var_07;
  undefined2 extraout_var_08;
  undefined2 extraout_var_09;
  undefined2 extraout_var_10;
  undefined2 extraout_var_11;
  undefined2 extraout_var_12;
  undefined2 extraout_var_13;
  undefined2 uVar4;
  undefined4 *puVar5;
  undefined4 local_e8 [16];
  char local_a8;
  char local_a4;
  char local_a0;
  char local_9c;
  char local_98;
  char local_94;
  uint local_90;
  undefined2 local_8c;
  uint local_88;
  undefined2 local_84;
  undefined1 local_80 [4];
  undefined2 local_7c;
  undefined1 local_70 [4];
  undefined2 local_6c;
  uint local_60;
  undefined1 local_5c [4];
  undefined2 local_58;
  undefined2 local_4c;
  undefined1 local_48 [4];
  undefined2 local_44;
  uint local_38;
  undefined2 local_34;
  uint local_30;
  uint local_2c;
  uint local_28;
  uint local_24;
  uint local_20;
  undefined2 local_1c;
  uint local_18 [3];
  uint local_c;
  int local_8;
  
  puVar5 = local_e8;
  for (iVar3 = 0x39; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar5 = 0xcccccccc;
    puVar5 = puVar5 + 1;
  }
  local_1c = 0;
  local_28 = CONCAT22(local_28._2_2_,DAT_007d5994);
  local_2c = local_2c & 0xffffff00;
  local_30 = local_30 & 0xffffff00;
  *(undefined1 *)(param_1 + 0x76c2) = 2;
  local_8 = param_1;
  FUN__text__004d5c40(local_18,0);
  if ((local_18[0] & 1) == 0) {
    FUN__text__004db2b0(5);
    local_2c = CONCAT31(local_2c._1_3_,1);
  }
  if (DAT_007d598e == '\0') {
    local_28 = CONCAT22(local_28._2_2_,(short)local_28 + -1);
    local_20 = local_20 & 0xffff0000;
    while ((local_20 & 0xffff) < 5) {
      if (*(short *)(&DAT_007aaa12 + (local_20 & 0xffff) * 0x1c) != -1) {
        local_24 = local_24 & 0xffff0000;
        while ((local_24 & 0xffff) < 4) {
          FUN__text__004d5ec0(local_18,(local_24 & 0xffff) * 0x4e + 0xe0,
                              (local_20 & 0xffff) * 0x61 + 0x53,0x44,0x40);
          if ((local_c & 0xffff) != 0) {
            FUN__text__004d2700(&DAT_0061b418,1,0x71,(local_24 & 0xffff) * 0x4e + 0xd8,
                                (local_20 & 0xffff) * 0x61 + 0x4c);
            FUN__text__004a8b50(CONCAT22(extraout_var,(short)local_20));
            if ((local_2c & 0xff) != 0) {
              FUN__text__004db2b0(5);
              local_30 = CONCAT31(local_30._1_3_,1);
              if (*(short *)(&DAT_007aaa22 + (local_24 & 0xffff) * 2 + (local_20 & 0xffff) * 0x1c)
                  == -1) {
                local_98 = DAT_007d598f;
                if (DAT_007d598f == '\0') {
                  *(short *)(&DAT_007aaa22 + (local_24 & 0xffff) * 2 + (local_20 & 0xffff) * 0x1c) =
                       (short)(char)DAT_007d5994;
                  (&DAT_007aaa20)[(local_20 & 0xffff) * 0x1c] =
                       (&DAT_007aaa20)[(local_20 & 0xffff) * 0x1c] + '\x01';
                  DAT_007d57de = DAT_007d57de + -1;
                  local_60 = CONCAT22(local_60._2_2_,DAT_007d5992);
                  while ((int)(local_60 & 0xffff) < (int)DAT_007d57de) {
                    *(undefined2 *)(&DAT_007d57e2 + (local_60 & 0xffff) * 2) =
                         *(undefined2 *)(&DAT_007d57e4 + (local_60 & 0xffff) * 2);
                    local_60 = CONCAT22(local_60._2_2_,(short)local_60 + 1);
                  }
                  FUN__text__004a95f0(local_70,local_20 & 0xffff);
                  FUN__text__004d48a0(CONCAT22(extraout_var_07,DAT_007d5994),1,5,
                                      CONCAT22(extraout_var_03,local_6c));
                }
                else if (DAT_007d598f == '\x01') {
                  *(undefined2 *)
                   (&DAT_007aaa22 + (local_24 & 0xffff) * 2 + (local_20 & 0xffff) * 0x1c) =
                       DAT_007d5994;
                  *(undefined2 *)(&DAT_007aaa22 + DAT_007d5992 * 2 + DAT_007d5990 * 0x1c) = 0xffff;
                  FUN__text__004a95f0(local_80,local_20 & 0xffff);
                  FUN__text__004d48a0(CONCAT22(extraout_var_01,DAT_007d5994),1,5,
                                      CONCAT22(extraout_var_08,local_7c));
                }
              }
              else {
                local_94 = DAT_007d598f;
                if (DAT_007d598f == '\0') {
                  local_34 = *(undefined2 *)
                              (&DAT_007aaa22 + (local_24 & 0xffff) * 2 + (local_20 & 0xffff) * 0x1c)
                  ;
                  *(undefined2 *)
                   (&DAT_007aaa22 + (local_24 & 0xffff) * 2 + (local_20 & 0xffff) * 0x1c) =
                       DAT_007d5994;
                  DAT_007d57de = DAT_007d57de + -1;
                  local_38 = CONCAT22(local_38._2_2_,DAT_007d5992);
                  while (sVar1 = DAT_007d57de, (int)(local_38 & 0xffff) < (int)DAT_007d57de) {
                    *(undefined2 *)(&DAT_007d57e2 + (local_38 & 0xffff) * 2) =
                         *(undefined2 *)(&DAT_007d57e4 + (local_38 & 0xffff) * 2);
                    local_38 = CONCAT22(local_38._2_2_,(short)local_38 + 1);
                  }
                  *(undefined2 *)(&DAT_007d57e2 + DAT_007d57de * 2) = local_34;
                  DAT_007d57de = DAT_007d57de + 1;
                  FUN__text__004a95f0(local_48,CONCAT22(sVar1 >> 0xf,(short)local_20));
                  FUN__text__004d48a0(CONCAT22(extraout_var_00,DAT_007d5994),1,5,
                                      CONCAT22(extraout_var_05,local_44));
                }
                else if (DAT_007d598f == '\x01') {
                  local_4c = *(undefined2 *)
                              (&DAT_007aaa22 + (local_24 & 0xffff) * 2 + (local_20 & 0xffff) * 0x1c)
                  ;
                  *(undefined2 *)
                   (&DAT_007aaa22 + (local_24 & 0xffff) * 2 + (local_20 & 0xffff) * 0x1c) =
                       DAT_007d5994;
                  iVar3 = (int)DAT_007d5990;
                  *(undefined2 *)(&DAT_007aaa22 + DAT_007d5992 * 2 + iVar3 * 0x1c) = local_4c;
                  FUN__text__004a95f0(local_5c,CONCAT22((short)((uint)(iVar3 * 0x1c) >> 0x10),
                                                        (short)local_20));
                  FUN__text__004d48a0(CONCAT22(extraout_var_06,DAT_007d5994),1,5,
                                      CONCAT22(extraout_var_02,local_58));
                }
              }
              FUN__text__004a8bf0(DAT_007d57da,0);
            }
          }
          local_24 = CONCAT22(local_24._2_2_,(short)local_24 + 1);
        }
      }
      local_20 = CONCAT22(local_20._2_2_,(short)local_20 + 1);
    }
  }
  uVar2 = (uint)DAT_007d598e;
  if (uVar2 == 1) {
    local_28 = CONCAT22(local_28._2_2_,(short)local_28 + -0x65);
    local_20 = local_20 & 0xffff0000;
    while (uVar2 = local_20 & 0xffff, uVar2 < 5) {
      FUN__text__004d5ec0(local_18,0x10,(local_20 & 0xffff) * 0x61 + 0x53,0x44,0x40);
      if (((local_c & 0xffff) != 0) &&
         (FUN__text__004d2700(&DAT_0061b418,1,0x71,8,(local_20 & 0xffff) * 0x61 + 0x4c),
         (local_2c & 0xff) != 0)) {
        FUN__text__004db2b0(5);
        local_30 = CONCAT31(local_30._1_3_,1);
        uVar4 = extraout_var_09;
        if (*(short *)(&DAT_007aaa12 + (local_20 & 0xffff) * 0x1c) == -1) {
          local_a0 = DAT_007d598f;
          if (DAT_007d598f == '\0') {
            *(short *)(&DAT_007aaa12 + (local_20 & 0xffff) * 0x1c) = (short)(char)DAT_007d5994;
            DAT_007d58b0 = DAT_007d58b0 + -1;
            local_90 = CONCAT22(local_90._2_2_,DAT_007d5992);
            while (iVar3 = (int)DAT_007d58b0, (int)(local_90 & 0xffff) < iVar3) {
              *(undefined2 *)(&DAT_007d58b4 + (local_90 & 0xffff) * 2) =
                   *(undefined2 *)(&DAT_007d58b6 + (local_90 & 0xffff) * 2);
              local_90 = CONCAT22(local_90._2_2_,(short)local_90 + 1);
            }
            if (DAT_007a55fa != 0) {
              iVar3 = (local_20 & 0xffff) * 0x1c;
              (&DAT_007aaa15)[iVar3] = 0;
            }
            *(undefined2 *)(&DAT_007aaa18 + (local_20 & 0xffff) * 0x1c) = 0xffff;
            *(undefined2 *)(&DAT_007aaa1a + (local_20 & 0xffff) * 0x1c) = 0xffff;
            FUN__text__004a8b50(CONCAT22((short)((uint)iVar3 >> 0x10),(short)local_20));
            uVar4 = extraout_var_12;
          }
          else if (DAT_007d598f == '\x01') {
            *(undefined2 *)(&DAT_007aaa12 + (local_20 & 0xffff) * 0x1c) = DAT_007d5994;
            *(undefined2 *)(&DAT_007aaa12 + DAT_007d5990 * 0x1c) = 0xffff;
            local_24 = local_24 & 0xffff0000;
            while ((local_24 & 0xffff) < 4) {
              if (*(short *)(&DAT_007aaa22 + (local_24 & 0xffff) * 2 + DAT_007d5990 * 0x1c) != -1) {
                *(undefined2 *)(&DAT_007d57e2 + DAT_007d57de * 2) =
                     *(undefined2 *)(&DAT_007aaa22 + (local_24 & 0xffff) * 2 + DAT_007d5990 * 0x1c);
                DAT_007d57de = DAT_007d57de + 1;
                *(undefined2 *)(&DAT_007aaa22 + (local_24 & 0xffff) * 2 + DAT_007d5990 * 0x1c) =
                     0xffff;
              }
              local_24 = CONCAT22(local_24._2_2_,(short)local_24 + 1);
            }
            (&DAT_007aaa15)[DAT_007d5990 * 0x1c] = 1;
            *(undefined2 *)(&DAT_007aaa18 + DAT_007d5990 * 0x1c) = 0xffff;
            *(undefined2 *)(&DAT_007aaa1a + DAT_007d5990 * 0x1c) = 0xffff;
            iVar3 = 0;
            if (DAT_007a55fa == 0) {
              iVar3 = (local_20 & 0xffff) * 0x1c;
              (&DAT_007aaa15)[iVar3] = 1;
            }
            else {
              (&DAT_007aaa15)[(local_20 & 0xffff) * 0x1c] = 0;
            }
            *(undefined2 *)(&DAT_007aaa18 + (local_20 & 0xffff) * 0x1c) = 0xffff;
            *(undefined2 *)(&DAT_007aaa1a + (local_20 & 0xffff) * 0x1c) = 0xffff;
            FUN__text__004a8b50(CONCAT22((short)((uint)iVar3 >> 0x10),(short)local_20));
            uVar4 = extraout_var_13;
          }
        }
        else {
          local_9c = DAT_007d598f;
          if (DAT_007d598f == '\0') {
            local_84 = *(undefined2 *)(&DAT_007aaa12 + (local_20 & 0xffff) * 0x1c);
            *(undefined2 *)(&DAT_007aaa12 + (local_20 & 0xffff) * 0x1c) = DAT_007d5994;
            DAT_007d58b0 = DAT_007d58b0 + -1;
            local_88 = CONCAT22(local_88._2_2_,DAT_007d5992);
            while ((int)(local_88 & 0xffff) < (int)DAT_007d58b0) {
              *(undefined2 *)(&DAT_007d58b4 + (local_88 & 0xffff) * 2) =
                   *(undefined2 *)(&DAT_007d58b6 + (local_88 & 0xffff) * 2);
              local_88 = CONCAT22(local_88._2_2_,(short)local_88 + 1);
            }
            *(undefined2 *)(&DAT_007d58b4 + DAT_007d58b0 * 2) = local_84;
            DAT_007d58b0 = DAT_007d58b0 + 1;
            *(undefined2 *)(&DAT_007aaa18 + (local_20 & 0xffff) * 0x1c) = 0xffff;
            *(undefined2 *)(&DAT_007aaa1a + (local_20 & 0xffff) * 0x1c) = 0xffff;
            FUN__text__004a8b50(local_20 & 0xffff);
            uVar4 = extraout_var_10;
          }
          else if (DAT_007d598f == '\x01') {
            local_8c = *(undefined2 *)(&DAT_007aaa12 + (local_20 & 0xffff) * 0x1c);
            *(undefined2 *)(&DAT_007aaa12 + (local_20 & 0xffff) * 0x1c) = DAT_007d5994;
            *(undefined2 *)(&DAT_007aaa12 + DAT_007d5990 * 0x1c) = local_8c;
            *(undefined2 *)(&DAT_007aaa18 + (local_20 & 0xffff) * 0x1c) = 0xffff;
            iVar3 = (local_20 & 0xffff) * 0x1c;
            *(undefined2 *)(&DAT_007aaa1a + iVar3) = 0xffff;
            *(undefined2 *)(&DAT_007aaa18 + DAT_007d5990 * 0x1c) = 0xffff;
            *(undefined2 *)(&DAT_007aaa1a + DAT_007d5990 * 0x1c) = 0xffff;
            FUN__text__004a8b50(CONCAT22((short)((uint)iVar3 >> 0x10),(short)local_20));
            uVar4 = extraout_var_11;
          }
        }
        FUN__text__004a8bf0(CONCAT22(uVar4,(ushort)DAT_007d58aa),1);
      }
      local_20 = CONCAT22(local_20._2_2_,(short)local_20 + 1);
    }
  }
  FUN__text__004aadb0(*(short *)(DAT_007a49fc + 0x196c) + -0x26,
                      *(short *)(DAT_007a49fc + 0x1970) + -0x24,DAT_007d598e,
                      CONCAT22((short)(uVar2 >> 0x10),(ushort)(byte)local_28),0xff,0xff,0x6a);
  local_a4 = DAT_007d598e;
  if (DAT_007d598e == '\0') {
    FUN__text__004aacf0(*(short *)(DAT_007a49fc + 0x196c) + -0x26,
                        *(short *)(DAT_007a49fc + 0x1970) + -0x24,
                        (byte)(&DAT_006b2d8a)
                              [*(short *)(&DAT_007e17ee + ((local_28 & 0xffff) + 1) * 0x4a0) * 0x40]
                        - 1,0xff,0x69);
  }
  if ((local_2c & 0xff) != 0) {
    if (((local_30 & 0xff) == 0) && (iVar3 = (int)DAT_007d598f, iVar3 != 0)) {
      if (DAT_007d598f == '\x01') {
        local_a8 = DAT_007d598e;
        if (DAT_007d598e == '\0') {
          FUN__text__004d48a0(DAT_007d5994,2,5,DAT_007d5996);
          *(undefined2 *)(&DAT_007d57e2 + DAT_007d57de * 2) = DAT_007d5994;
          DAT_007d57de = DAT_007d57de + 1;
          iVar3 = CONCAT22(extraout_var_04,DAT_007d57de);
          *(undefined2 *)(&DAT_007aaa22 + DAT_007d5992 * 2 + DAT_007d5990 * 0x1c) = 0xffff;
        }
        else if (DAT_007d598e == '\x01') {
          FUN__text__004db2b0(5);
          *(undefined2 *)(&DAT_007d58b4 + DAT_007d58b0 * 2) = DAT_007d5994;
          DAT_007d58b0 = DAT_007d58b0 + 1;
          *(undefined2 *)(&DAT_007aaa12 + DAT_007d5990 * 0x1c) = 0xffff;
          local_20 = local_20 & 0xffff0000;
          while ((local_20 & 0xffff) < 4) {
            if (*(short *)(&DAT_007aaa22 + (local_20 & 0xffff) * 2 + DAT_007d5990 * 0x1c) != -1) {
              *(undefined2 *)(&DAT_007d57e2 + DAT_007d57de * 2) =
                   *(undefined2 *)(&DAT_007aaa22 + (local_20 & 0xffff) * 2 + DAT_007d5990 * 0x1c);
              DAT_007d57de = DAT_007d57de + 1;
              *(undefined2 *)(&DAT_007aaa22 + (local_20 & 0xffff) * 2 + DAT_007d5990 * 0x1c) =
                   0xffff;
            }
            local_20 = CONCAT22(local_20._2_2_,(short)local_20 + 1);
          }
          (&DAT_007aaa15)[DAT_007d5990 * 0x1c] = 1;
          *(undefined2 *)(&DAT_007aaa18 + DAT_007d5990 * 0x1c) = 0xffff;
          iVar3 = DAT_007d5990 * 0x1c;
          *(undefined2 *)(&DAT_007aaa1a + iVar3) = 0xffff;
        }
      }
      FUN__text__004a8bf0(CONCAT22((short)((uint)iVar3 >> 0x10),(ushort)DAT_007d57da),0);
      FUN__text__004a8bf0(DAT_007d58aa,1);
    }
    DAT_007d598f = -1;
    DAT_007d598e = -1;
    DAT_007d5990 = -1;
    DAT_007d5992 = -1;
    DAT_007d5994 = 0xffff;
    *(undefined2 *)(local_8 + 0x76c6) = 0;
  }
  local_8 = 0x4a5439;
  FUN__text__0056ce80();
  return;
}

