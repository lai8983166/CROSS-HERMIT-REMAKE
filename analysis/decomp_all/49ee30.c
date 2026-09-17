
void FUN__text__0049ee30(void)

{
  undefined2 extraout_var;
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_170 [16];
  byte local_130;
  undefined1 local_12c [16];
  undefined1 local_11c;
  undefined4 local_34 [8];
  short local_14;
  uint local_10;
  short local_c;
  undefined4 local_8;
  
  puVar2 = local_170;
  for (iVar1 = 0x5b; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  DAT_007a528c = FUN__text__004d1ba0(DAT_007a528c + 1,1,99);
  DAT_007a528e = 4;
  DAT_007a5290 = 0;
  DAT_007a5292 = 1;
  DAT_007a55f8 = 1;
  FUN__text__004d3d00();
  for (local_8._0_2_ = 0; (short)local_8 < 5; local_8._0_2_ = (short)local_8 + 1) {
    *(undefined2 *)(&DAT_007aaa12 + (short)local_8 * 0x1c) = 0xffff;
    (&DAT_007aaa20)[(short)local_8 * 0x1c] = 0;
    *(undefined2 *)(&DAT_007aaa22 + (short)local_8 * 0x1c) = 0xffff;
    *(undefined2 *)(&DAT_007aaa24 + (short)local_8 * 0x1c) = 0xffff;
    *(undefined2 *)(&DAT_007aaa26 + (short)local_8 * 0x1c) = 0xffff;
    *(undefined2 *)(&DAT_007aaa28 + (short)local_8 * 0x1c) = 0xffff;
    (&DAT_007aaa15)[(short)local_8 * 0x1c] = 1;
    (&DAT_007aaa16)[(short)local_8 * 0x1c] = 0xff;
    *(undefined2 *)(&DAT_007aaa18 + (short)local_8 * 0x1c) = 0xffff;
    *(undefined2 *)(&DAT_007aaa1a + (short)local_8 * 0x1c) = 0xffff;
  }
  for (local_8._0_2_ = 0; (short)local_8 < 0x65; local_8._0_2_ = (short)local_8 + 1) {
    (&DAT_007a55fc)[(short)local_8] = 0;
  }
  DAT_007a5b62 = 0;
  for (local_8._0_2_ = 0; (short)local_8 < 0x65; local_8._0_2_ = (short)local_8 + 1) {
    (&DAT_007a5b64)[(short)local_8] = 0;
  }
  for (local_8._0_2_ = 0; (short)local_8 < 0x14; local_8._0_2_ = (short)local_8 + 1) {
    *(undefined2 *)(&DAT_007aa9ea + (short)local_8 * 2) = 0;
    for (local_c = 0; local_c < 100; local_c = local_c + 1) {
      (&DAT_007a5bca)[local_c * 10 + (short)local_8 * 1000] = 0;
    }
  }
  for (local_8._0_2_ = 0; (short)local_8 < 0x50; local_8._0_2_ = (short)local_8 + 1) {
  }
  for (local_8._0_2_ = 0; (short)local_8 < 5; local_8._0_2_ = (short)local_8 + 1) {
    *(undefined2 *)(&DAT_007aaa1a + (short)local_8 * 0x1c) = 0xffff;
    *(undefined2 *)(&DAT_007aaa1c + (short)local_8 * 0x1c) = 0xffff;
    *(undefined2 *)(&DAT_007aaa1e + (short)local_8 * 0x1c) = 0xffff;
  }
  DAT_007aab0a = 0;
  for (local_8._0_2_ = 0; (short)local_8 < 0xf0; local_8._0_2_ = (short)local_8 + 1) {
    (&DAT_007a5120)[(short)local_8] = 0;
  }
  DAT_007a5294 = 0;
  DAT_007a5296 = 0;
  DAT_007a5298 = 0;
  for (local_8._0_2_ = 0; (short)local_8 < 5; local_8._0_2_ = (short)local_8 + 1) {
    *(undefined2 *)(&DAT_007a52f8 + (short)local_8 * 0x70) = 0;
    *(undefined2 *)(&DAT_007a5304 + (short)local_8 * 0x70) = 0;
  }
  for (local_8._0_2_ = 0; (short)local_8 < 0x50; local_8._0_2_ = (short)local_8 + 1) {
    (&DAT_007a5664)[(short)local_8 * 0x10] = 0;
  }
  for (local_8._0_2_ = 0; (short)local_8 < 300; local_8._0_2_ = (short)local_8 + 1) {
    (&DAT_007a54ca)[(short)local_8] = 5;
  }
  FUN__text__004d3e90(0x65,0,0xffffffff);
  FUN__text__004d3e90(3,0,0);
  FUN__text__004d3e90(4,0,1);
  FUN__text__004d3e90(9,0,2);
  for (local_8._0_2_ = 0; iVar1 = (int)(short)local_8, iVar1 < 0x2d;
      local_8._0_2_ = (short)local_8 + 1) {
    local_10 = local_10 & 0xffff0000;
    while ((local_10 & 0xffff) < 0x54) {
      local_130 = (&DAT_007e18a0)[(local_10 & 0xffff) * 0xc + (short)local_8 * 0x4a0];
      if ((local_130 == 0) || (6 < local_130)) {
        (&DAT_007e18a0)[(local_10 & 0xffff) * 0xc + (short)local_8 * 0x4a0] = 0;
      }
      else {
        (&DAT_007e18a0)[(local_10 & 0xffff) * 0xc + (short)local_8 * 0x4a0] = 4;
      }
      local_10 = CONCAT22(local_10._2_2_,(short)local_10 + 1);
    }
  }
  for (local_8._0_2_ = 0; (short)local_8 < 0x168; local_8._0_2_ = (short)local_8 + 1) {
    iVar1 = (int)(short)local_8;
    *(ushort *)(&DAT_007aacac + (short)local_8 * 2) =
         *(ushort *)(&DAT_007aacac + iVar1 * 2) & 0xf0ff | 0x100;
  }
  local_8._0_2_ = 1;
  while ((short)local_8 < 0x2d) {
    *(undefined4 *)(&DAT_007cf468 + (short)local_8 * 0x124) = 0;
    local_14 = 0;
    while (local_14 < 7) {
      (&DAT_007e17f4)[local_14 * 8 + (short)local_8 * 0x4a0] =
           (char)((int)(uint)(byte)(&DAT_007e17f4)[local_14 * 8 + (short)local_8 * 0x4a0] >> 1);
      FUN__text__004d56a0(local_34,CONCAT22(local_14 >> 0xf,
                                            (ushort)(byte)(&DAT_007e17f4)
                                                          [local_14 * 8 + (short)local_8 * 0x4a0]),0
                         );
      *(undefined4 *)(&DAT_007e17f8 + local_14 * 8 + (int)((longlong)(int)(short)local_8 * 0x4a0)) =
           local_34[0];
      local_14 = local_14 + 1;
      iVar1 = CONCAT22((short)((ulonglong)((longlong)(int)(short)local_8 * 0x4a0) >> 0x10),local_14)
      ;
    }
    FUN__text__004d58e0(local_12c,CONCAT22((short)((uint)iVar1 >> 0x10),(short)local_8));
    (&DAT_007e1838)[(short)local_8 * 0x4a0] = local_11c;
    local_8._0_2_ = (short)local_8 + 1;
    iVar1 = CONCAT22(extraout_var,(short)local_8);
  }
  for (local_8._0_2_ = 0; (short)local_8 < 0x80; local_8._0_2_ = (short)local_8 + 1) {
    (&DAT_007d4f3c)[(short)local_8] = 0;
  }
  FUN__text__004e1ca0();
  DAT_007d6a34 = 0;
  local_8 = 0x49f406;
  FUN__text__0056ce80();
  return;
}

