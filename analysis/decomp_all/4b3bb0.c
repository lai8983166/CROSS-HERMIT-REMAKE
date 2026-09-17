
void FUN__text__004b3bb0(void)

{
  char cVar1;
  undefined2 extraout_var;
  undefined2 uVar2;
  undefined2 extraout_var_00;
  int iVar3;
  ushort uVar4;
  undefined2 extraout_var_01;
  undefined4 *puVar5;
  undefined4 local_70 [16];
  short local_30;
  uint local_2c;
  uint local_28;
  undefined4 local_24;
  uint local_20;
  undefined *local_1c;
  undefined1 local_18 [4];
  uint local_14;
  uint local_c;
  int local_8;
  
  puVar5 = local_70;
  for (iVar3 = 0x1b; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar5 = 0xcccccccc;
    puVar5 = puVar5 + 1;
  }
  local_2c = local_2c & 0xffff0000;
  local_30 = 0;
  FUN__text__004d2700(&DAT_0061bb40,0,0x4e,0xd7,0x1a7);
  *(undefined1 *)(local_8 + 0xc88) = 1;
  local_24 = (uint)local_24._2_2_ << 0x10;
  while ((local_24 & 0xffff) < 3) {
    local_20 = local_20 & 0xffff0000;
    while ((local_20 & 0xffff) < 10) {
      uVar4 = (short)local_24 * 10 + (short)local_20;
      local_28 = CONCAT22(local_28._2_2_,uVar4);
      if (*(short *)(local_8 + 0x596 + (uint)uVar4 * 2) != -1) {
        FUN__text__004d5ec0(local_18,(local_20 & 0xffff) * 0x4e + 0xea,
                            (local_24 & 0xffff) * 0x61 + 0x1d4,0x44,0x54);
        if (((local_c & 0xffff) != 0) && ((local_14 & 1) != 0)) {
          local_2c = CONCAT22(local_2c._2_2_,1);
          local_30 = (short)local_28;
          FUN__text__004db2b0(5);
        }
        FUN__text__004b8140((local_20 & 0xffff) * 0x4e + 0xe5,(local_24 & 0xffff) * 0x61 + 0x1cd,0,
                            *(short *)(local_8 + 0x596 + (local_28 & 0xffff) * 2) + -1,0xffffffff,
                            0xff,0x46);
        FUN__text__004b82f0((local_20 & 0xffff) * 0x4e + 0xe9,(local_24 & 0xffff) * 0x61 + 0x218,0,
                            *(short *)(local_8 + 0x596 + (local_28 & 0xffff) * 2) + -1,0xff,0x46);
        FUN__text__004b7fc0((local_20 & 0xffff) * 0x4e + 0xe5,(local_24 & 0xffff) * 0x61 + 0x1cd,
                            (byte)(&DAT_006b2d8a)
                                  [*(short *)(&DAT_007e17ee +
                                             *(short *)(local_8 + 0x596 + (local_28 & 0xffff) * 2) *
                                             0x4a0) * 0x40] - 1,0xff,0x44);
        cVar1 = *(char *)(local_8 + 0x5fa + (local_28 & 0xffff));
        if (cVar1 != -1) {
          FUN__text__004b8080((local_20 & 0xffff) * 0x4e + 0x123,(local_24 & 0xffff) * 0x61 + 0x1cd,
                              CONCAT31(cVar1 >> 7,
                                       *(undefined1 *)(local_8 + 0x5fa + (local_28 & 0xffff))),0xff,
                              0x44);
        }
      }
      local_20 = CONCAT22(local_20._2_2_,(short)local_20 + 1);
    }
    local_24 = CONCAT22(local_24._2_2_,(short)local_24 + 1);
  }
  iVar3 = FUN__text__004128f0(0xcb,1);
  if (iVar3 != 0) {
    local_30 = FUN__text__004b6fb0(0,CONCAT22(extraout_var_01,DAT_007d6a34));
    local_2c = CONCAT22(local_2c._2_2_,1);
    FUN__text__004db2b0(5);
  }
  iVar3 = FUN__text__004128f0(0xcd,1);
  uVar2 = 0;
  if (iVar3 != 0) {
    local_30 = FUN__text__004b6fb0(1,DAT_007d6a34);
    local_2c = CONCAT22(local_2c._2_2_,1);
    FUN__text__004db2b0(5);
    uVar2 = extraout_var;
  }
  if ((local_2c & 0xffff) != 0) {
    DAT_007d6a34 = local_30;
    FUN__text__004b6690(CONCAT22(uVar2,*(undefined2 *)(local_8 + 0x596 + local_30 * 2)),0xffffffff,1
                        ,2);
    FUN__text__004b6690(CONCAT22(extraout_var_00,*(undefined2 *)(local_8 + 0x596 + DAT_007d6a34 * 2)
                                ),0xffffffff,0,0);
  }
  DAT_007d7708 = DAT_007d6a34 % 10;
  DAT_007d770a = DAT_007d6a34 / 10;
  local_1c = &DAT_0061bc30;
  FUN__text__004d2ca0(0xd,6,DAT_0061bc32,(uint)DAT_007d7708 * 0x4e + 0xe4,
                      (uint)DAT_007d770a * 0x61 + 0x1cb,DAT_0061bc34,DAT_0061bc36,DAT_0061bc38,
                      DAT_0061bc3a);
  local_8 = 0x4b3ff1;
  FUN__text__0056ce80();
  return;
}

