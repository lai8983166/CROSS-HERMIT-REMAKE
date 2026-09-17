
void __fastcall FUN__text__004bbd40(int param_1)

{
  short sVar1;
  undefined2 uVar2;
  undefined4 *puVar3;
  undefined4 uVar4;
  int iVar5;
  undefined4 *puVar6;
  undefined4 local_224 [16];
  int local_1e4;
  int local_1e0;
  int local_1dc;
  undefined1 local_1d8 [32];
  short local_1b8;
  short local_1b4;
  ushort local_1b0;
  undefined2 uStack_1ae;
  uint local_1ac;
  uint local_1a8;
  int local_1a4;
  int local_1a0;
  int local_19c;
  undefined4 local_198 [6];
  int local_180;
  undefined1 local_178 [12];
  int local_16c;
  short local_80;
  undefined *local_7c;
  undefined *local_78;
  uint local_74;
  int local_70;
  short local_6c;
  short local_68;
  short local_64;
  short local_60;
  short local_5c;
  int local_58;
  int local_54;
  ushort local_50;
  short local_4c;
  int local_48;
  int local_44;
  short local_40;
  short local_3c;
  short local_38;
  short local_34;
  short local_30;
  short local_2c;
  short local_28;
  short local_24;
  short local_20;
  int local_1c;
  int local_18;
  int local_14;
  short local_10;
  short local_c;
  int local_8;
  
  sVar1 = DAT_007a5294;
  puVar3 = local_224;
  for (iVar5 = 0x88; iVar5 != 0; iVar5 = iVar5 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_14 = 0;
  local_18 = 0;
  local_1c = 0;
  local_20 = DAT_007a5294;
  local_28 = DAT_007f450e;
  local_2c = DAT_007f4510;
  local_30 = DAT_007a5296 + -1;
  local_24 = DAT_007f450c + -1;
  if (local_24 < 0) {
    local_24 = 0;
  }
  *(short *)(&DAT_007a5306 + local_30 * 0x70) = local_24;
  local_1dc = (int)DAT_007f450e;
  if (local_1dc == 0) {
    *(undefined2 *)(param_1 + 0x36) = 3;
  }
  else if (((0 < local_1dc) && (local_1dc < 4)) &&
          (*(short *)(param_1 + 0x36) = DAT_007f450e + -1, 2 < local_24)) {
    *(undefined2 *)(param_1 + 0x36) = 3;
  }
  if (((*(short *)(&DAT_0073bf0a + sVar1 * 0x100) == 0) &&
      (*(short *)(&DAT_0073bf0c + sVar1 * 0x100) == 0)) &&
     (*(short *)(&DAT_0073bf0e + sVar1 * 0x100) == 0)) {
    *(undefined2 *)(param_1 + 0x36) = 4;
  }
  local_1e0 = (int)DAT_007f4510;
  if (local_1e0 == 0) {
    *(undefined2 *)(param_1 + 0x38) = 2;
  }
  else if (local_1e0 == 1) {
    *(undefined2 *)(param_1 + 0x38) = 1;
  }
  else if (local_1e0 == 2) {
    *(undefined2 *)(param_1 + 0x38) = 0;
  }
  if (*(short *)(&DAT_0073bf08 + sVar1 * 0x100) == 0) {
    local_2c = 0;
    *(undefined2 *)(param_1 + 0x38) = 2;
  }
  local_8 = param_1;
  local_34 = FUN__text__004d1ba0(*(short *)(&DAT_007a52f8 + local_30 * 0x70) + -1,1,0x14);
  local_38 = (short)((int)((int)local_34 + ((int)local_34 >> 0x1f & 3U)) >> 2);
  FUN__text__0042b2d0(&DAT_005a0de4,(int)local_38);
  *(short *)(local_8 + 0x34) = local_24;
  *(undefined2 *)(local_8 + 0x48) = *(undefined2 *)(&DAT_007a52f8 + local_30 * 0x70);
  *(undefined4 *)(local_8 + 0x44) = DAT_007a511c;
  *(undefined2 *)(local_8 + 0x4c) = 0;
  for (local_c = 0; local_c < *(short *)(&DAT_007a52f8 + local_30 * 0x70); local_c = local_c + 1) {
    *(short *)(local_8 + 0x4c) =
         *(short *)(local_8 + 0x4c) + *(short *)(&DAT_007f45c4 + local_c * 0xb0);
  }
  uVar2 = FUN__text__004d1ba0((int)*(short *)(local_8 + 0x4c),0,999999999);
  *(undefined2 *)(local_8 + 0x4c) = uVar2;
  local_3c = 0;
  local_40 = 0;
  local_4c = 0;
  local_44 = *(int *)(&DAT_0073bef4 + local_24 * 4 + local_20 * 0x100);
  local_48 = local_44 / 2;
  if (local_2c == 2) {
    local_4c = *(short *)(&DAT_0073bf08 + local_20 * 0x100);
  }
  local_50 = (ushort)(local_2c == 2);
  local_1e4 = (int)*(short *)(local_8 + 0x36);
  if ((-1 < local_1e4) && (local_1e4 < 3)) {
    local_4c = local_4c +
               *(short *)(&DAT_0073bf0a + *(short *)(local_8 + 0x36) * 2 + local_20 * 0x100);
    local_50 = local_50 + 1;
  }
  local_50 = local_50 + 1;
  local_4c = local_4c + *(short *)(&DAT_0073bf10 + local_38 * 2 + local_20 * 0x100) +
             local_50 * -100;
  local_54 = local_44 + (local_44 * local_4c) / 100;
  local_58 = 0;
  for (local_c = 0; local_c < *(short *)(&DAT_007a52f8 + local_30 * 0x70); local_c = local_c + 1) {
    local_78 = &DAT_007f4518 + local_c * 0xb0;
    local_60 = *(short *)(&DAT_007a52d0 + local_c * 2 + local_30 * 0x70);
    local_64 = *(short *)(&DAT_007a52a8 + local_c * 2 + local_30 * 0x70);
    if (*(short *)(local_8 + 0x4c) == 0) {
      local_68 = 0;
    }
    else {
      local_68 = (short)((*(short *)(&DAT_007f45c4 + local_c * 0xb0) * 100) /
                        (int)*(short *)(local_8 + 0x4c));
    }
    FUN__text__0042b2d0(&DAT_005a0db4,(int)local_60,(int)local_68,
                        (int)*(short *)(&DAT_007f45c4 + local_c * 0xb0),
                        (int)*(short *)(local_8 + 0x4c));
    local_10 = 0;
    while ((local_10 < 10 && (*(short *)(&DAT_0061c50a + local_10 * 2) + -1 < (int)local_68))) {
      local_10 = local_10 + 1;
    }
    local_6c = local_10;
    FUN__text__0042b2d0("[ Cno %3d ] Reat Offset %2d \n",(int)local_60,(int)local_10);
    local_7c = &DAT_007e17e8 + local_60 * 0x4a0;
    local_74 = CONCAT22(local_74._2_2_,
                        (ushort)(byte)(&DAT_006b2d8a)
                                      [*(short *)(&DAT_007e17ee + local_60 * 0x4a0) * 0x40]);
    FUN__text__0042b2d0(&DAT_005a0d78,(int)local_60,
                        (ushort)(byte)(&DAT_006b2d8a)
                                      [*(short *)(&DAT_007e17ee + local_60 * 0x4a0) * 0x40]);
    local_68 = *(short *)(&DAT_0061c508 + ((local_74 & 0xffff) * 0xb + (int)local_6c) * 2);
    if (DAT_007f4491 == '\0') {
      local_80 = *(short *)(&DAT_007a529c + local_64 * 0x70);
    }
    else {
      local_80 = 0;
    }
    local_5c = local_80 / 10 + 100;
    local_70 = local_54;
    FUN__text__0042b2d0(&DAT_005a0d58,(int)local_60,local_54);
    local_70 = local_70 + ((local_68 + -100) * local_70) / 100 +
               (local_70 * (local_5c + -100)) / 100;
    FUN__text__0042b2d0(&DAT_005a0d3c,(int)local_60,(int)local_68);
    FUN__text__0042b2d0(&DAT_005a0d1c,(int)local_60,(int)local_5c);
    if (local_70 < local_48) {
      local_70 = local_48;
    }
    if (DAT_007f4491 != '\0') {
      local_70 = local_70 / 10;
      FUN__text__0042b2d0(&DAT_005a0cf0,(int)local_60,local_70);
    }
    FUN__text__004d58e0(local_178,local_60);
    for (local_10 = 0; local_10 < 8; local_10 = local_10 + 1) {
      *(undefined4 *)(&DAT_007cf34c + local_10 * 4 + local_60 * 0x124) = 0;
    }
    local_19c = 0;
    local_1a0 = 0;
    for (local_10 = 0; local_10 < 7; local_10 = local_10 + 1) {
      if (*(short *)(&DAT_0061c58c + ((local_74 & 0xffff) * 7 + (int)local_10) * 2) != 0) {
        local_19c = (local_70 *
                    *(short *)(&DAT_0061c58c + ((local_74 & 0xffff) * 7 + (int)local_10) * 2)) / 100
        ;
        puVar3 = (undefined4 *)
                 FUN__text__004d56a0(local_1d8,
                                     CONCAT22((short)((uint)*(undefined4 *)
                                                             (&DAT_007e17f8 +
                                                             local_10 * 8 + local_60 * 0x4a0) >>
                                                     0x10),
                                              (ushort)(byte)(&DAT_007e17f4)
                                                            [local_10 * 8 + local_60 * 0x4a0]),
                                     *(undefined4 *)
                                      (&DAT_007e17f8 + local_10 * 8 + local_60 * 0x4a0));
        puVar6 = local_198;
        for (iVar5 = 8; iVar5 != 0; iVar5 = iVar5 + -1) {
          *puVar6 = *puVar3;
          puVar3 = puVar3 + 1;
          puVar6 = puVar6 + 1;
        }
        if (local_180 < local_19c) {
          local_1c = local_1c + (local_19c - local_180) / 2;
          local_19c = local_180;
        }
        if (local_16c < local_1a0 + local_19c) {
          local_1a4 = (local_1a0 + local_19c) - local_16c;
          if (local_1a4 < local_19c) {
            local_1c = local_1c + local_1a4 / 2;
            local_19c = local_19c - local_1a4;
          }
          else {
            local_1c = local_1c + local_19c / 2;
            local_19c = 0;
          }
        }
        *(int *)(&DAT_007cf34c + local_10 * 4 + local_60 * 0x124) = local_19c;
        local_1a0 = local_1a0 + local_19c;
      }
    }
    *(int *)(&DAT_007cf36c + local_60 * 0x124) = local_1a0;
    if (local_58 < local_1a0) {
      local_58 = local_1a0;
    }
    local_14 = local_14 + local_1a0;
    local_18 = local_18 + 1;
    local_1b4 = 0;
    local_1ac = local_1ac & 0xffff0000;
    while ((local_1ac & 0xffff) < 5) {
      local_1a8 = local_1a8 & 0xffff0000;
      while ((local_1a8 & 0xffff) < 4) {
        if (DAT_007f4491 == '\0') {
          _local_1b0 = CONCAT22(uStack_1ae,
                                *(ushort *)
                                 (&DAT_007aaae0 +
                                 (local_1ac & 0xffff) * 8 + (local_1a8 & 0xffff) * 2));
          if (*(short *)(&DAT_007a5210 +
                        (uint)*(ushort *)
                               (&DAT_007aaae0 + (local_1ac & 0xffff) * 8 + (local_1a8 & 0xffff) * 2)
                        * 2) == local_60) {
            *(short *)(local_8 + 0x50 + (local_1ac & 0xffff) * 8 + (local_1a8 & 0xffff) * 2) =
                 local_60;
            *(undefined2 *)(local_8 + 0x78 + (local_1ac & 0xffff) * 8 + (local_1a8 & 0xffff) * 2) =
                 *(undefined2 *)(&DAT_007f45c2 + local_c * 0xb0);
            *(undefined2 *)(local_8 + 0xa0 + (local_1ac & 0xffff) * 8 + (local_1a8 & 0xffff) * 2) =
                 *(undefined2 *)(&DAT_007f45c4 + local_c * 0xb0);
            *(short *)(local_8 + 200 + (local_1ac & 0xffff) * 8 + (local_1a8 & 0xffff) * 2) =
                 (short)(char)(&DAT_007f45c6)[local_c * 0xb0];
            *(int *)(local_8 + 0xf0 + (local_1ac & 0xffff) * 0x10 + (local_1a8 & 0xffff) * 4) =
                 local_1a0;
            local_3c = local_3c + (char)(&DAT_007f45c6)[local_c * 0xb0];
            local_40 = local_40 + *(short *)(&DAT_007f45c2 + local_c * 0xb0);
          }
        }
        else {
          local_1b4 = (short)local_1a8 + (short)local_1ac * 4;
          _local_1b0 = CONCAT22(uStack_1ae,*(ushort *)(&DAT_007f451a + local_1b4 * 0xb0));
          if ((uint)*(ushort *)(&DAT_007f451a + local_1b4 * 0xb0) == (int)local_60) {
            *(short *)(local_8 + 0x50 + (local_1ac & 0xffff) * 8 + (local_1a8 & 0xffff) * 2) =
                 local_60;
            *(undefined2 *)(local_8 + 0x78 + (local_1ac & 0xffff) * 8 + (local_1a8 & 0xffff) * 2) =
                 *(undefined2 *)(&DAT_007f45c2 + local_c * 0xb0);
            *(undefined2 *)(local_8 + 0xa0 + (local_1ac & 0xffff) * 8 + (local_1a8 & 0xffff) * 2) =
                 *(undefined2 *)(&DAT_007f45c4 + local_c * 0xb0);
            *(short *)(local_8 + 200 + (local_1ac & 0xffff) * 8 + (local_1a8 & 0xffff) * 2) =
                 (short)(char)(&DAT_007f45c6)[local_c * 0xb0];
            *(int *)(local_8 + 0xf0 + (local_1ac & 0xffff) * 0x10 + (local_1a8 & 0xffff) * 4) =
                 local_1a0;
            local_3c = local_3c + (char)(&DAT_007f45c6)[local_c * 0xb0];
            local_40 = local_40 + *(short *)(&DAT_007f45c2 + local_c * 0xb0);
          }
        }
        local_1a8 = CONCAT22(local_1a8._2_2_,(short)local_1a8 + 1);
      }
      local_1ac = CONCAT22(local_1ac._2_2_,(short)local_1ac + 1);
    }
  }
  *(short *)(local_8 + 0x4e) = local_3c;
  local_1b8 = 100;
  if ((*(short *)(local_8 + 0x4e) != 0) &&
     (*(short *)(local_8 + 0x4e) <= *(short *)(local_8 + 0x48))) {
    local_1b8 = 0x5a;
  }
  local_70 = ((local_14 * local_1b8) / local_18) / 100 + local_1c;
  *(int *)(local_8 + 0x40) = local_70;
  *(int *)(local_8 + 0x3c) = *(int *)(local_8 + 0x40) + *(int *)(local_8 + 0x44);
  *(short *)(local_8 + 0x4a) = local_40;
  uVar4 = FUN__text__004d1ba0(*(undefined4 *)(local_8 + 0x3c),0,999999999);
  *(undefined4 *)(local_8 + 0x3c) = uVar4;
  DAT_007a511c = *(undefined4 *)(local_8 + 0x3c);
  local_8 = 0x4bca31;
  FUN__text__0056ce80();
  return;
}

