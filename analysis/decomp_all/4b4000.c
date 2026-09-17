
void FUN__text__004b4000(void)

{
  undefined2 extraout_var;
  undefined2 extraout_var_00;
  undefined2 extraout_var_01;
  ushort uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_8c [16];
  uint local_4c;
  byte local_48;
  char local_44;
  ushort local_40;
  undefined2 uStack_3e;
  undefined2 local_3c;
  uint local_38;
  uint local_34;
  uint local_30;
  uint local_2c;
  uint local_28;
  undefined4 local_24;
  uint local_20;
  undefined *local_1c;
  undefined1 local_18 [4];
  uint local_14;
  uint local_c;
  int local_8;
  
  puVar3 = local_8c;
  for (iVar2 = 0x22; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_34 = CONCAT22(local_34._2_2_,0x79);
  local_38 = CONCAT22(local_38._2_2_,0x53);
  FUN__text__004d2700(&DAT_0061bb50,0,0x4e,0x74,0x52);
  local_24 = (uint)local_24._2_2_ << 0x10;
  while ((local_24 & 0xffff) < 3) {
    local_20 = local_20 & 0xffff0000;
    while ((local_20 & 0xffff) < 10) {
      uVar1 = (short)local_24 * 10 + (short)local_20;
      local_28 = CONCAT22(local_28._2_2_,uVar1);
      if (*(short *)(local_8 + 0x596 + (uint)uVar1 * 2) != -1) {
        FUN__text__004d5ec0(local_18,(local_34 & 0xffff) + (local_20 & 0xffff) * 0x4e,
                            (local_38 & 0xffff) + (local_24 & 0xffff) * 0x61,0x44,0x54);
        if ((local_c & 0xffff) != 0) {
          local_2c = CONCAT22(local_2c._2_2_,(short)local_20);
          local_30 = CONCAT22(local_30._2_2_,(short)local_24);
          if ((local_14 & 1) != 0) {
            DAT_007d6a31 = 0;
            DAT_007d6a34 = (short)local_28;
            FUN__text__004db2b0(5);
            FUN__text__004b6690(CONCAT22(extraout_var,
                                         *(undefined2 *)(local_8 + 0x596 + DAT_007d6a34 * 2)),
                                0xffffffff,1,2);
            FUN__text__004b6690(CONCAT22(extraout_var_00,
                                         *(undefined2 *)(local_8 + 0x596 + DAT_007d6a34 * 2)),
                                0xffffffff,0,0);
          }
        }
        local_3c = 0x80;
        local_44 = DAT_007d6a32;
        if (DAT_007d6a32 == '\0') {
          if ((-1 < DAT_007d6a3c) &&
             ((local_48 = (&DAT_007e18a0)
                          [(DAT_007d6a3c + -1) * 0xc +
                           *(short *)(local_8 + 0x596 + (local_28 & 0xffff) * 2) * 0x4a0],
              local_48 == 3 || ((4 < local_48 && (local_48 < 7)))))) {
            local_3c = 0xff;
          }
        }
        else if (((DAT_007d6a32 == '\x01') && (-1 < DAT_007d6a52)) && (-1 < DAT_007d6a54)) {
          _local_40 = CONCAT22(uStack_3e,DAT_007d7c26);
          if ((((*(ushort *)(&DAT_007aacac + (uint)DAT_007d7c26 * 2) & 1) != 0) &&
              (local_4c = (uint)(*(ushort *)(&DAT_007aacac + (uint)DAT_007d7c26 * 2) >> 8 & 0xf),
              2 < local_4c)) &&
             ((local_4c < 5 &&
              ((int)*(short *)(local_8 + 0x596 + (local_28 & 0xffff) * 2) ==
               (uint)(*(ushort *)(&DAT_007aacac + (uint)DAT_007d7c26 * 2) >> 1 & 0x7f))))) {
            local_3c = 0xff;
          }
        }
        FUN__text__004b8140((local_34 & 0xffff) + (local_20 & 0xffff) * 0x4e,
                            (local_38 & 0xffff) + (local_24 & 0xffff) * 0x61,0,
                            *(short *)(local_8 + 0x596 + (local_28 & 0xffff) * 2) + -1,0xffffffff,
                            (undefined1)local_3c,0x46);
        FUN__text__004b82f0((local_34 & 0xffff) + 4 + (local_20 & 0xffff) * 0x4e,
                            (local_38 & 0xffff) + 0x4b + (local_24 & 0xffff) * 0x61,0,
                            *(short *)(local_8 + 0x596 + (local_28 & 0xffff) * 2) + -1,
                            (undefined1)local_3c,0x46);
        FUN__text__004b7fc0((local_34 & 0xffff) + (local_20 & 0xffff) * 0x4e,
                            (local_38 & 0xffff) + (local_24 & 0xffff) * 0x61,
                            (byte)(&DAT_006b2d8a)
                                  [*(short *)(&DAT_007e17ee +
                                             *(short *)(local_8 + 0x596 + (local_28 & 0xffff) * 2) *
                                             0x4a0) * 0x40] - 1,CONCAT22(extraout_var_01,local_3c),
                            0x44);
        if (*(char *)(local_8 + 0x5fa + (local_28 & 0xffff)) != -1) {
          FUN__text__004b8080((local_34 & 0xffff) + 0x3e + (local_20 & 0xffff) * 0x4e,
                              (local_38 & 0xffff) + (local_24 & 0xffff) * 0x61,
                              *(undefined1 *)(local_8 + 0x5fa + (local_28 & 0xffff)),local_3c,0x44);
        }
      }
      local_20 = CONCAT22(local_20._2_2_,(short)local_20 + 1);
    }
    local_24 = CONCAT22(local_24._2_2_,(short)local_24 + 1);
  }
  local_1c = &DAT_0061bc30;
  FUN__text__004d2ca0(0xd,6,DAT_0061bc32,(local_34 & 0xffff) + (local_2c & 0xffff) * 0x4e,
                      (local_38 & 0xffff) + (local_30 & 0xffff) * 0x61,DAT_0061bc34,DAT_0061bc36,
                      DAT_0061bc38,DAT_0061bc3a);
  local_8 = 0x4b450b;
  FUN__text__0056ce80();
  return;
}

