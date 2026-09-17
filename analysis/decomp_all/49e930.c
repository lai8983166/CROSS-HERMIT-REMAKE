
void FUN__text__0049e930(void)

{
  undefined1 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 *puVar4;
  undefined4 local_54 [16];
  short local_14;
  short local_10;
  short local_c;
  undefined4 local_8;
  
  puVar3 = local_54;
  for (iVar2 = 0x14; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  _memset(&DAT_007a50e8,0,0x306d4);
  DAT_007a528c = 1;
  DAT_007a528e = 4;
  DAT_007a5290 = 0;
  DAT_007a5292 = 1;
  DAT_007a55f8 = 1;
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
  FUN__text__004d3d00();
  DAT_007a511c = 0;
  for (local_8._0_2_ = 0; (short)local_8 < 0x168; local_8._0_2_ = (short)local_8 + 1) {
    *(ushort *)(&DAT_007aacac + (short)local_8 * 2) =
         *(ushort *)(&DAT_007aacac + (short)local_8 * 2) & 0xfffe;
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
  for (local_8._0_2_ = 0; (short)local_8 < 5; local_8._0_2_ = (short)local_8 + 1) {
    *(undefined2 *)(&DAT_007aaa1a + (short)local_8 * 0x1c) = 0xffff;
    *(undefined2 *)(&DAT_007aaa1c + (short)local_8 * 0x1c) = 0xffff;
    *(undefined2 *)(&DAT_007aaa1e + (short)local_8 * 0x1c) = 0xffff;
  }
  for (local_8._0_2_ = 0; (short)local_8 < 0x43; local_8._0_2_ = (short)local_8 + 1) {
    puVar3 = (undefined4 *)(&DAT_0074e4b0 + (short)local_8 * 0x44);
    puVar4 = (undefined4 *)(&DAT_007d3d70 + (short)local_8 * 0x44);
    for (iVar2 = 0x11; iVar2 != 0; iVar2 = iVar2 + -1) {
      *puVar4 = *puVar3;
      puVar3 = puVar3 + 1;
      puVar4 = puVar4 + 1;
    }
  }
  for (local_8._0_2_ = 0; (short)local_8 < 0xf0; local_8._0_2_ = (short)local_8 + 1) {
    (&DAT_007a5120)[(short)local_8] = 0;
  }
  DAT_007aab0a = 0;
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
  for (local_8._0_2_ = 0; (short)local_8 < 0x2d; local_8._0_2_ = (short)local_8 + 1) {
    for (local_14 = 0; local_14 < 0x20; local_14 = local_14 + 1) {
      local_10 = *(short *)(&DAT_00751242 + local_14 * 2 + (short)local_8 * 0x42);
      if (local_10 == 100) {
        (&DAT_007cf445)[(int)local_14 + (short)local_8 * 0x124] = 1;
      }
      else {
        (&DAT_007cf445)[(int)local_14 + (short)local_8 * 0x124] = 0;
      }
      uVar1 = FUN__text__004d1ba0((int)local_10,0,100);
      (&DAT_007cf424)[(int)local_14 + (short)local_8 * 0x124] = uVar1;
    }
  }
  FUN__text__004d3e90(0x65,0,0xffffffff);
  FUN__text__004d3e90(3,0,0);
  FUN__text__004d3e90(4,0,1);
  FUN__text__004d3e90(9,0,2);
  for (local_8._0_2_ = 0; (short)local_8 < 0x80; local_8._0_2_ = (short)local_8 + 1) {
    (&DAT_007d4f3c)[(short)local_8] = 0;
  }
  FUN__text__004e1ca0();
  DAT_007d6a34 = 0;
  local_8 = 0x49ee25;
  FUN__text__0056ce80();
  return;
}

