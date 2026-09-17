
void __fastcall FUN__text__004a6f90(int param_1)

{
  undefined1 uVar1;
  short sVar2;
  undefined2 extraout_var;
  undefined2 extraout_var_00;
  int iVar3;
  undefined2 extraout_var_01;
  undefined2 extraout_var_02;
  undefined2 uVar4;
  undefined2 extraout_var_03;
  undefined2 extraout_var_04;
  undefined2 extraout_var_05;
  undefined2 uVar5;
  undefined2 extraout_var_06;
  undefined2 extraout_var_07;
  undefined4 *puVar6;
  undefined4 local_b0 [16];
  int local_70;
  int local_6c;
  short local_68;
  short local_64;
  uint local_60;
  short local_5c;
  short local_58;
  undefined2 local_54;
  short local_50;
  short local_4c;
  short asStack_48 [20];
  undefined *local_20;
  undefined1 local_1c [4];
  uint local_18;
  uint local_10;
  uint local_c;
  int local_8;
  
  puVar6 = local_b0;
  for (iVar3 = 0x2b; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar6 = 0xcccccccc;
    puVar6 = puVar6 + 1;
  }
  local_6c = (int)*(short *)(param_1 + 0x76c6);
  local_8 = param_1;
  switch(local_6c) {
  case 0:
    sVar2 = FUN__text__004aa320();
    local_70 = sVar2 + -1;
    switch(local_70) {
    case 0:
      *(undefined2 *)(local_8 + 0x76c6) = 0xb;
      break;
    case 1:
      *(undefined2 *)(local_8 + 0x76c6) = 0xc;
      break;
    case 2:
      *(undefined2 *)(local_8 + 0x76c6) = 7;
      break;
    case 3:
      *(undefined2 *)(local_8 + 0x76c6) = 8;
      break;
    default:
      break;
    case 6:
      *(undefined2 *)(local_8 + 0x76c6) = 0xd;
      *(undefined2 *)(local_8 + 0x1294) = 0;
    }
    FUN__text__004a3ca0();
    break;
  case 2:
    FUN__text__004d2620(0,0,0x400,0x300,0,
                        (0xff - (*(short *)(param_1 + 0x76c8) * 0xff) / 0x1e) * 0x1000000 | 0x10101,
                        1);
    sVar2 = *(short *)(local_8 + 0x76c8);
    *(short *)(local_8 + 0x76c8) = *(short *)(local_8 + 0x76c8) + 1;
    if (sVar2 == 0x1e) {
      *(undefined2 *)(local_8 + 0x76c8) = 0;
      *(undefined2 *)(local_8 + 0x76c6) = 0;
    }
    break;
  case 3:
    FUN__text__004d2620(0,0,0x400,0x300,0,
                        (*(short *)(param_1 + 0x76c8) * 0xff) / 0x1e << 0x18 | 0x10101,1);
    sVar2 = *(short *)(local_8 + 0x76c8);
    *(short *)(local_8 + 0x76c8) = *(short *)(local_8 + 0x76c8) + 1;
    if (sVar2 == 0x1e) {
      *(undefined2 *)(local_8 + 0x76c8) = 0;
      *(undefined2 *)(local_8 + 0x76c4) = 0;
      *(undefined2 *)(local_8 + 0x7950) = 8;
    }
    break;
  case 6:
    FUN__text__004a4680();
    break;
  case 7:
    FUN__text__004d2620(0,0,0x400,0x300,0,
                        (*(short *)(param_1 + 0x76c8) * 0xff) / 0x1e << 0x18 | 0x10101,1);
    sVar2 = *(short *)(local_8 + 0x76c8);
    *(short *)(local_8 + 0x76c8) = *(short *)(local_8 + 0x76c8) + 1;
    if (sVar2 == 0x1e) {
      *(undefined2 *)(local_8 + 0x76c8) = 0;
      *(undefined2 *)(local_8 + 0x76c4) = 0;
      *(undefined2 *)(local_8 + 0x7950) = 3;
    }
    DAT_007e11a0 = 1;
    break;
  case 8:
    FUN__text__004d2620(0,0,0x400,0x300,0,
                        (*(short *)(param_1 + 0x76c8) * 0xff) / 0x1e << 0x18 | 0x10101,1);
    sVar2 = *(short *)(local_8 + 0x76c8);
    *(short *)(local_8 + 0x76c8) = *(short *)(local_8 + 0x76c8) + 1;
    if (sVar2 == 0x1e) {
      *(undefined2 *)(local_8 + 0x76c8) = 0;
      *(undefined2 *)(local_8 + 0x76c6) = 9;
      DAT_007a4e60 = 1;
    }
    FUN__text__004d6710();
    break;
  case 9:
    local_c = local_c & 0xffff0000;
    while ((local_c & 0xffff) < 0x1e) {
      FUN__text__004d2620(0,0,0x400,0x300,0,
                          (0xff - ((local_c & 0xffff) * 0xff) / 0x1e) * 0x1000000 | 0x10101,1);
      FUN__text__00422360(0);
      local_c = CONCAT22(local_c._2_2_,(short)local_c + 1);
    }
    while (DAT_007a4e60 != 0) {
      FUN__text__00422360(0);
    }
    FUN__text__004d2620(0,0,0x400,0x300,0,0xff010101,1);
    *(undefined2 *)(local_8 + 0x76c6) = 2;
    FUN__text__004a9ab0();
    break;
  case 10:
    FUN__text__004d2620(0,0,0x400,0x300,0,
                        (*(short *)(param_1 + 0x76c8) * 0xff) / 0x1e << 0x18 | 0x10101,1);
    sVar2 = *(short *)(local_8 + 0x76c8);
    *(short *)(local_8 + 0x76c8) = *(short *)(local_8 + 0x76c8) + 1;
    if (sVar2 == 0x1e) {
      FUN__text__004ce210("Data\\ADV\\DAT\\mm001.ybc",0xffffffff);
      do {
        uVar1 = FUN__text__004ce8f0();
        local_60 = CONCAT31(local_60._1_3_,uVar1);
        FUN__text__00422360(0);
      } while ((local_60 & 0xff) != 0);
      FUN__text__004d2620(0,0,0x400,0x300,0,0xff010101,1);
      *(undefined2 *)(local_8 + 0x76c8) = 0;
      *(undefined2 *)(local_8 + 0x76c6) = 2;
      DAT_007e11a0 = 0;
      FUN__text__004db010((int)DAT_007a55f6);
    }
    break;
  case 0xb:
    FUN__text__004d2620(0,0,0x400,0x300,0,
                        (*(short *)(param_1 + 0x76c8) * 0xff) / 0x1e << 0x18 | 0x10101,1);
    sVar2 = *(short *)(local_8 + 0x76c8);
    *(short *)(local_8 + 0x76c8) = *(short *)(local_8 + 0x76c8) + 1;
    if (sVar2 == 0x1e) {
      *(undefined2 *)(local_8 + 0x76c8) = 0;
      DAT_007e11a8 = 1;
      *(undefined2 *)(local_8 + 0x76c4) = 0;
      *(undefined2 *)(local_8 + 0x7950) = 1;
    }
    break;
  case 0xc:
    FUN__text__004d2620(0,0,0x400,0x300,0,
                        (*(short *)(param_1 + 0x76c8) * 0xff) / 0x1e << 0x18 | 0x10101,1);
    sVar2 = *(short *)(local_8 + 0x76c8);
    *(short *)(local_8 + 0x76c8) = *(short *)(local_8 + 0x76c8) + 1;
    if (sVar2 == 0x1e) {
      *(undefined2 *)(local_8 + 0x76c8) = 0;
      DAT_007e11a8 = 2;
      *(undefined2 *)(local_8 + 0x76c4) = 0;
      *(undefined2 *)(local_8 + 0x7950) = 2;
    }
    break;
  case 0xd:
    if (*(short *)(param_1 + 0x1294) == 0) {
      FUN__text__004d60e0(5);
      FUN__text__004d6150(&DAT_005a09c8);
      FUN__text__004d6150(&DAT_005a09fc);
      *(undefined2 *)(local_8 + 0x1294) = 1;
    }
    local_64 = 0x179;
    local_68 = 0x152;
    FUN__text__004d62f0(0x183,0x15c,0x66);
    FUN__text__004d5ec0(local_1c,local_64 + 0x1c,local_68 + 0x34,0x66,0x1d);
    if (((local_10 & 0xffff) != 0) && ((local_18 & 1) != 0)) {
      local_20 = &DAT_0061b5f8;
      FUN__text__004d68b0(&DAT_0061b5f8,0x67,(int)local_64 + (uint)DAT_0061b604,
                          (int)local_68 + (uint)DAT_0061b606,2);
      *(undefined2 *)(local_8 + 0x76c6) = 0xf;
      FUN__text__004db2b0(6);
    }
    FUN__text__004d5ec0(local_1c,local_64 + 0x8c,local_68 + 0x34,0x66,0x1d);
    uVar5 = extraout_var;
    uVar4 = extraout_var_06;
    if (((local_10 & 0xffff) != 0) && (uVar4 = 0, (local_18 & 1) != 0)) {
      local_20 = &DAT_0061b608;
      FUN__text__004d68b0(&DAT_0061b608,0x67,(int)local_64 + (uint)DAT_0061b614,
                          (int)local_68 + (uint)DAT_0061b616,2);
      FUN__text__004db2b0(1);
      *(undefined2 *)(local_8 + 0x76c6) = 0;
      uVar5 = extraout_var_00;
      uVar4 = extraout_var_07;
    }
    FUN__text__004d2700(&DAT_0061b5e8,1,0x68,CONCAT22(uVar5,local_64),CONCAT22(uVar4,local_68));
    FUN__text__004d2620(0x16a,0x143,300,0x78,0x69,0xd8080808,1);
    break;
  case 0xe:
    if (*(short *)(param_1 + 0x1294) == 0) {
      local_4c = 0;
      local_c = CONCAT22(local_c._2_2_,1);
      while ((local_c & 0xffff) < 0xc) {
        sVar2 = FUN__text__004d46e0(local_c & 0xffff);
        if (sVar2 != 0) {
          asStack_48[local_4c] = (short)local_c;
          local_4c = local_4c + 1;
        }
        local_c = CONCAT22(local_c._2_2_,(short)local_c + 1);
      }
      sVar2 = FUN__text__004d46e0(0x23);
      if (sVar2 != 0) {
        asStack_48[local_4c] = (short)local_c;
        local_4c = local_4c + 1;
      }
      local_50 = FUN__text__004d1cb0();
      local_50 = local_50 % local_4c;
      local_54 = FUN__text__004d1ba0((int)asStack_48[local_50],0,0x23);
      FUN__text__004d48a0(CONCAT22(extraout_var_03,asStack_48[local_50]),10,0xffffffff,0);
      FUN__text__004d60e0(5);
      FUN__text__004d6150(&DAT_005a0a24);
      FUN__text__004d6150(&DAT_005a09fc);
      *(undefined2 *)(local_8 + 0x1294) = 1;
    }
    local_58 = 0x179;
    local_5c = 0x152;
    FUN__text__004d62f0(0x183,0x15c,0x66);
    FUN__text__004d5ec0(local_1c,local_58 + 0x1c,local_5c + 0x34,0x66,0x1d);
    if (((local_10 & 0xffff) != 0) && ((local_18 & 1) != 0)) {
      local_20 = &DAT_0061b5f8;
      FUN__text__004d68b0(&DAT_0061b5f8,0x67,(int)local_58 + (uint)DAT_0061b604,
                          (int)local_5c + (uint)DAT_0061b606,2);
      *(undefined2 *)(local_8 + 0x76c6) = 3;
      *(undefined2 *)(local_8 + 0x30) = 1;
      FUN__text__004db2b0(5);
    }
    FUN__text__004d5ec0(local_1c,local_58 + 0x8c,local_5c + 0x34,0x66,0x1d);
    uVar5 = extraout_var_04;
    uVar4 = extraout_var_01;
    if (((local_10 & 0xffff) != 0) && (uVar4 = 0, (local_18 & 1) != 0)) {
      local_20 = &DAT_0061b608;
      FUN__text__004d68b0(&DAT_0061b608,0x67,(int)local_58 + (uint)DAT_0061b614,
                          (int)local_5c + (uint)DAT_0061b616,2);
      FUN__text__004db2b0(1);
      *(undefined2 *)(local_8 + 0x76c6) = 0;
      uVar5 = extraout_var_05;
      uVar4 = extraout_var_02;
    }
    FUN__text__004d2700(&DAT_0061b5e8,1,0x68,CONCAT22(uVar5,local_58),CONCAT22(uVar4,local_5c));
    FUN__text__004d2620(0x16a,0x143,300,0x78,0x69,0xd8080808,1);
    break;
  case 0xf:
    FUN__text__004d2620(0,0,0x400,0x300,0,
                        (*(short *)(param_1 + 0x76c8) * 0xff) / 0x1e << 0x18 | 0x10101,1);
    sVar2 = *(short *)(local_8 + 0x76c8);
    *(short *)(local_8 + 0x76c8) = *(short *)(local_8 + 0x76c8) + 1;
    if (sVar2 == 0x1e) {
      *(undefined2 *)(local_8 + 0x76c8) = 0;
      *(undefined2 *)(local_8 + 0x76c4) = 0;
      *(undefined2 *)(local_8 + 0x7950) = 7;
    }
  }
  local_8 = 0x4a7bd2;
  FUN__text__0056ce80();
  return;
}

