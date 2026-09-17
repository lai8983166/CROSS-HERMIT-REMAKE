
void FUN__text__0049fd50(void)

{
  undefined2 extraout_var;
  int iVar1;
  undefined2 extraout_var_00;
  undefined4 *puVar2;
  undefined4 local_74 [16];
  undefined1 *local_34;
  int local_30;
  undefined1 *local_2c;
  int local_28;
  short local_24;
  short local_20;
  undefined2 local_1c;
  undefined1 local_18 [4];
  uint local_14;
  int local_8;
  
  puVar2 = local_74;
  for (iVar1 = 0x1c; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_1c = 1;
  local_24 = 0x1f;
  for (local_20 = 0; local_20 < local_24; local_20 = local_20 + 1) {
    FUN__text__004d2620(0,0,0x400,0x300,0x34,
                        (0xff - (local_20 * 0xff) / (local_24 + -1)) * 0x1000000 | 0x10101,1);
    FUN__text__0049faa0();
    FUN__text__00422360(0);
  }
  do {
    FUN__text__004d5ec0(local_18,0x28e,0x2d6,0x8d,0x1e);
    if ((local_14 & 1) != 0) {
      local_1c = 2;
      FUN__text__004db2b0(5);
      local_28 = local_8 + 0x12de8;
      local_2c = &DAT_0061b130;
      FUN__text__004d67f0(CONCAT31(0x61b1,DAT_0061b130),0x38,CONCAT22(0x61,DAT_0061b132),
                          CONCAT22(0x61,DAT_0061b13c),CONCAT22(0x61,DAT_0061b13e),
                          CONCAT22(0x61,DAT_0061b134),CONCAT22(0x61,DAT_0061b136),
                          CONCAT22(0x61,DAT_0061b138),CONCAT22(extraout_var_00,DAT_0061b13a),8);
LAB__text__0049ff5c:
      for (local_20 = 0; local_20 < local_24; local_20 = local_20 + 1) {
        FUN__text__004d2620(0,0,0x400,0x300,0x34,(local_20 * 0xff) / (int)local_24 << 0x18 | 0x10101
                            ,1);
        FUN__text__0049faa0();
        FUN__text__00422360(0);
      }
      local_8 = 0x49ffeb;
      FUN__text__0056ce80();
      return;
    }
    FUN__text__004d5ec0(local_18,0x34f,0x2d6,0x8d,0x1e);
    if ((local_14 & 1) != 0) {
      FUN__text__004db2b0(5);
      local_30 = local_8 + 0x12de8;
      local_34 = &DAT_0061b140;
      FUN__text__004d67f0(CONCAT31(0x61b1,DAT_0061b140),0x38,CONCAT22(0x61,DAT_0061b142),
                          CONCAT22(0x61,DAT_0061b14c),CONCAT22(0x61,DAT_0061b14e),
                          CONCAT22(0x61,DAT_0061b144),CONCAT22(0x61,DAT_0061b146),
                          CONCAT22(0x61,DAT_0061b148),CONCAT22(extraout_var,DAT_0061b14a),8);
      local_1c = 4;
      goto LAB__text__0049ff5c;
    }
    FUN__text__0049faa0();
    FUN__text__00422360(0);
  } while( true );
}

