
void __fastcall FUN__text__004bdac0(int param_1)

{
  undefined1 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_74 [16];
  int local_34;
  uint local_30;
  short local_2c;
  short local_28;
  short local_24;
  undefined1 local_20 [4];
  uint local_1c;
  undefined2 local_10;
  short local_c;
  int local_8;
  
  puVar3 = local_74;
  for (iVar2 = 0x1c; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_10 = 0;
  local_24 = 0;
  *(undefined2 *)(param_1 + 0x32) = 0;
  local_8 = param_1;
  do {
    local_34 = (int)*(short *)(local_8 + 0x32);
    switch(local_34) {
    case 0:
      FUN__text__00415420();
      *(undefined2 *)(local_8 + 0x32) = 1;
      break;
    case 1:
      for (local_c = 0; local_c < 0x10; local_c = local_c + 1) {
        FUN__text__004d2620(0,0,0x400,0x300,0x51,
                            (0xff - (local_c * 0xff) / 0xf) * 0x1000000 | 0x10101,1);
        FUN__text__004be0b0();
        FUN__text__00422360(0);
      }
      if (*(short *)(local_8 + 0x142e) == 0) {
        FUN__text__004db060(0x1d,0);
      }
      else {
        FUN__text__004db060(0x1e,0);
      }
      for (local_c = 0; local_c < 0x1e; local_c = local_c + 1) {
        FUN__text__004be0b0();
        FUN__text__00422360(0);
      }
      *(undefined2 *)(local_8 + 0x32) = 2;
      break;
    case 2:
      FUN__text__0040d390(1,3,1,1);
      local_28 = 0;
      local_2c = 0;
      for (local_c = 0; local_c < 0xf0; local_c = local_c + 1) {
        DAT_007e1190 = (DAT_007e1188 * local_c) / 0xef;
        DAT_007e1196 = (short)(((int)DAT_007e118e * (int)local_c) / 0xef);
        if (local_28 != DAT_007e1196) {
          FUN__text__0040d390(1,2,0xffffffff,0);
        }
        local_28 = DAT_007e1196;
        DAT_007e1194 = (short)(((int)DAT_007e118c * (int)local_c) / 0xef);
        if (local_2c != DAT_007e1194) {
          FUN__text__0040d390(1,0,0xffffffff,0);
        }
        local_2c = DAT_007e1194;
        DAT_007e119c = (DAT_007a511c / 0xef) * (int)local_c;
        FUN__text__004be0b0();
        FUN__text__00422360(0);
      }
      FUN__text__0040d390(1,4,1,0);
      DAT_007e1190 = DAT_007e1188;
      DAT_007e1196 = DAT_007e118e;
      DAT_007e1194 = DAT_007e118c;
      DAT_007e119c = DAT_007a511c;
      for (local_c = 0; local_c < 0x1e; local_c = local_c + 1) {
        FUN__text__004be0b0();
        FUN__text__00422360(0);
      }
      if (*(short *)(local_8 + 0x142c) != 0) {
        DAT_007e1198 = 1;
        FUN__text__0040d390(1,1,0xffffffff,0);
      }
      *(undefined2 *)(local_8 + 0x32) = 5;
      break;
    case 3:
      FUN__text__004d5ec0(local_20,0x2e1,0x2db,0x10f,0x1e);
      if ((local_1c & 1) != 0) {
        FUN__text__004db2b0(5);
        for (local_c = 0; local_c < 8; local_c = local_c + 1) {
          FUN__text__004d2700(&DAT_0061c630,1,0x57,0x2d6,0x2d8);
          FUN__text__004be0b0();
          FUN__text__00422360(0);
        }
        *(undefined2 *)(local_8 + 0x32) = 4;
      }
      FUN__text__004d5ec0(local_20,0x1ba,0x2db,0x10e,0x1e);
      if ((local_1c & 1) != 0) {
        FUN__text__004db2b0(5);
        for (local_c = 0; local_c < 8; local_c = local_c + 1) {
          FUN__text__004d2700(&DAT_0061c620,1,0x57,0x1ae,0x2d8);
          FUN__text__004be0b0();
          FUN__text__00422360(0);
        }
        *(undefined2 *)(local_8 + 0x32) = 5;
      }
      FUN__text__004be0b0();
      FUN__text__00422360(0);
      break;
    case 4:
      for (local_c = 0xf; -1 < local_c; local_c = local_c + -1) {
        FUN__text__004d2620(0,0,0x400,0x300,0x51,
                            (0xff - (local_c * 0xff) / 0xf) * 0x1000000 | 0x10101,1);
        FUN__text__004be0b0();
        FUN__text__00422360(0);
      }
      FUN__text__004db230(0x5a);
      while (iVar2 = FUN__text__004db270(), iVar2 == 0) {
        FUN__text__00422360(0);
      }
      FUN__text__004db120();
      *(undefined2 *)(local_8 + 0x32) = 6;
      break;
    case 5:
      FUN__text__004ce210("Data\\AllResult\\dat\\mvp.ybc",0xffffffff);
      do {
        uVar1 = FUN__text__004ce8f0();
        local_30 = CONCAT31(local_30._1_3_,uVar1);
        FUN__text__004be0b0();
        FUN__text__00422360(0);
      } while ((local_30 & 0xff) != 0);
      *(undefined2 *)(local_8 + 0x32) = 3;
      break;
    case 6:
      local_24 = 1;
    }
  } while (local_24 == 0);
  local_8 = 0x4be08f;
  FUN__text__0056ce80();
  return;
}

