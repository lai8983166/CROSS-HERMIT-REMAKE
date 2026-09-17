
void __fastcall FUN__text__004c99e0(int param_1)

{
  short sVar1;
  undefined1 uVar2;
  ushort uVar3;
  uint uVar4;
  undefined2 extraout_var;
  undefined4 uVar5;
  undefined2 extraout_var_00;
  undefined2 extraout_var_01;
  int iVar6;
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
  undefined2 extraout_var_14;
  undefined2 extraout_var_15;
  undefined4 *puVar7;
  undefined4 local_a0 [16];
  int local_60;
  uint local_5c;
  undefined1 local_58;
  uint local_54;
  short local_50;
  uint local_4c;
  uint local_48;
  uint local_44;
  undefined2 local_40;
  undefined1 local_3c;
  uint local_38;
  undefined1 local_34;
  uint local_30;
  undefined2 local_2c;
  undefined1 local_28;
  uint local_24;
  uint local_20;
  undefined4 local_1c;
  undefined4 local_18;
  undefined4 local_14;
  undefined4 local_10;
  undefined4 local_c;
  int local_8;
  
  puVar7 = local_a0;
  for (iVar6 = 0x27; iVar6 != 0; iVar6 = iVar6 + -1) {
    *puVar7 = 0xcccccccc;
    puVar7 = puVar7 + 1;
  }
  local_c = 0;
  local_10 = 0;
  local_14 = 0;
  local_18 = 0;
  local_1c = 0;
  local_20 = 0;
  local_5c = (uint)*(ushort *)(param_1 + 0x30);
  if (-2 < (int)local_5c) {
    if (local_5c == 0) {
      local_c = 0x3b;
      local_10 = 0x3c;
      local_14 = 0x3d;
      local_18 = 0x3e;
      local_1c = 0x3f;
      local_20 = 0x40;
    }
    else if (local_5c == 1) {
      local_c = 0x44;
      local_10 = 0x45;
      local_14 = 0x46;
      local_18 = 0x47;
      local_1c = 0x48;
      local_20 = 0x49;
    }
  }
  local_60 = *(ushort *)(param_1 + 0x22) - 2;
  local_8 = param_1;
  switch(local_60) {
  case 1:
    uVar2 = FUN__text__004ca9b0();
    local_38 = CONCAT31(local_38._1_3_,uVar2);
    local_3c = FUN__text__004ca9e0();
    uVar5 = FUN__text__004cd850(*(undefined2 *)(local_8 + 0x24),
                                CONCAT22(extraout_var_05,*(undefined2 *)(local_8 + 0x26)),0xff);
    local_40 = (undefined2)uVar5;
    FUN__text__004c9690(*(undefined2 *)(local_8 + 0x2c),*(undefined2 *)(local_8 + 0x2e),uVar5,
                        local_38 & 0xff,CONCAT22(extraout_var_06,(undefined2)local_20));
    FUN__text__004c97a0(*(undefined2 *)(local_8 + 0x2c),*(undefined2 *)(local_8 + 0x2e),local_40,
                        *(undefined2 *)(local_8 + 0x38 + (local_38 & 0xff) * 2),local_38 & 0xff,
                        CONCAT22(extraout_var_11,(undefined2)local_1c));
    uVar3 = *(ushort *)(local_8 + 0x24);
    *(short *)(local_8 + 0x24) = *(short *)(local_8 + 0x24) + 1;
    if (*(ushort *)(local_8 + 0x26) < uVar3) {
      *(undefined2 *)(local_8 + 0x24) = 0;
      *(undefined2 *)(local_8 + 0x22) = 2;
    }
    break;
  case 2:
    uVar2 = FUN__text__004ca9b0();
    local_24 = CONCAT31(local_24._1_3_,uVar2);
    local_28 = FUN__text__004ca9e0();
    uVar4 = FUN__text__004cd850(*(undefined2 *)(local_8 + 0x24),
                                CONCAT22(extraout_var_10,*(undefined2 *)(local_8 + 0x26)),0xff);
    iVar6 = 0xff - (uVar4 & 0xffff);
    local_2c = (undefined2)iVar6;
    FUN__text__004c9690(*(undefined2 *)(local_8 + 0x2c),*(undefined2 *)(local_8 + 0x2e),iVar6,
                        local_24 & 0xff,local_20 & 0xffff);
    FUN__text__004c97a0(*(undefined2 *)(local_8 + 0x2c),*(undefined2 *)(local_8 + 0x2e),local_2c,
                        *(undefined2 *)(local_8 + 0x38 + (local_24 & 0xff) * 2),local_24 & 0xff,
                        CONCAT22(extraout_var_02,(undefined2)local_1c));
    uVar3 = *(ushort *)(local_8 + 0x24);
    *(short *)(local_8 + 0x24) = *(short *)(local_8 + 0x24) + 1;
    if (*(ushort *)(local_8 + 0x26) < uVar3) {
      *(undefined2 *)(local_8 + 0x24) = 0;
      *(undefined2 *)(local_8 + 0x22) = 1;
    }
    break;
  case 3:
    uVar2 = FUN__text__004ca9b0();
    local_48 = CONCAT31(local_48._1_3_,uVar2);
    uVar2 = FUN__text__004ca9e0();
    local_4c = CONCAT31(local_4c._1_3_,uVar2);
    uVar3 = FUN__text__004cd850(*(undefined2 *)(local_8 + 0x24),
                                CONCAT22(extraout_var_12,*(undefined2 *)(local_8 + 0x26)),0xff);
    local_44 = CONCAT22(local_44._2_2_,uVar3);
    FUN__text__004c9690(*(undefined2 *)(local_8 + 0x2c),*(undefined2 *)(local_8 + 0x2e),
                        0xff - (uint)uVar3,local_4c & 0xff,
                        CONCAT22(extraout_var_13,(undefined2)local_14));
    FUN__text__004c97a0(*(undefined2 *)(local_8 + 0x2c),*(undefined2 *)(local_8 + 0x2e),
                        0xff - (local_44 & 0xffff),
                        *(undefined2 *)(local_8 + 0x38 + (local_4c & 0xff) * 2),local_4c & 0xff,
                        CONCAT22(extraout_var_07,(undefined2)local_10));
    FUN__text__004c9690(*(undefined2 *)(local_8 + 0x2c),*(undefined2 *)(local_8 + 0x2e),
                        CONCAT22(extraout_var_14,(undefined2)local_44),local_48 & 0xff,
                        CONCAT22(extraout_var,(undefined2)local_20));
    FUN__text__004c97a0(*(undefined2 *)(local_8 + 0x2c),*(undefined2 *)(local_8 + 0x2e),
                        local_44 & 0xffff,*(undefined2 *)(local_8 + 0x38 + (local_48 & 0xff) * 2),
                        local_48 & 0xff,CONCAT22(extraout_var_08,(undefined2)local_1c));
    uVar3 = *(ushort *)(local_8 + 0x24);
    *(short *)(local_8 + 0x24) = *(short *)(local_8 + 0x24) + 1;
    if (*(ushort *)(local_8 + 0x26) < uVar3) {
      *(undefined2 *)(local_8 + 0x24) = 0;
      *(undefined2 *)(local_8 + 0x22) = 2;
    }
    break;
  case 4:
    uVar2 = FUN__text__004ca9b0();
    local_54 = CONCAT31(local_54._1_3_,uVar2);
    local_58 = FUN__text__004ca9e0();
    uVar5 = FUN__text__004cd850(*(undefined2 *)(local_8 + 0x24),
                                CONCAT22(extraout_var_09,*(undefined2 *)(local_8 + 0x26)),0xff);
    local_50 = 0xff - (short)uVar5;
    FUN__text__004c97a0(*(undefined2 *)(local_8 + 0x2c),*(undefined2 *)(local_8 + 0x2e),local_50,
                        *(undefined2 *)(local_8 + 0x3c + (local_54 & 0xff) * 2),
                        CONCAT31((int3)((uint)uVar5 >> 8),(undefined1)local_54) & 0xffff,
                        CONCAT22(extraout_var_15,(undefined2)local_18));
    FUN__text__004c97a0(*(undefined2 *)(local_8 + 0x2c),*(undefined2 *)(local_8 + 0x2e),0xff,
                        *(undefined2 *)(local_8 + 0x38 + (local_54 & 0xff) * 2),local_54 & 0xff,
                        CONCAT22(extraout_var_00,(undefined2)local_1c));
    FUN__text__004c9690(*(undefined2 *)(local_8 + 0x2c),
                        CONCAT22(extraout_var_01,*(undefined2 *)(local_8 + 0x2e)),0xff,
                        local_54 & 0xff,CONCAT22(extraout_var_01,(undefined2)local_20));
    *(short *)(local_8 + 0x24) = *(short *)(local_8 + 0x24) + 1;
    if (*(ushort *)(local_8 + 0x26) < *(ushort *)(local_8 + 0x24)) {
      *(undefined2 *)(local_8 + 0x24) = 0;
      *(undefined2 *)(local_8 + 0x22) = 2;
    }
    break;
  case 5:
    sVar1 = *(short *)(param_1 + 0x28);
    *(short *)(param_1 + 0x28) = *(short *)(param_1 + 0x28) + 1;
    if (*(short *)(param_1 + 0x2a) < sVar1) {
      *(undefined2 *)(param_1 + 0x28) = 0;
      *(undefined2 *)(param_1 + 0x22) = 3;
    }
    break;
  case 6:
    sVar1 = *(short *)(param_1 + 0x28);
    *(short *)(param_1 + 0x28) = *(short *)(param_1 + 0x28) + 1;
    if (*(short *)(param_1 + 0x2a) < sVar1) {
      *(undefined2 *)(param_1 + 0x28) = 0;
      *(undefined2 *)(param_1 + 0x22) = 4;
    }
  case 0:
    uVar2 = FUN__text__004ca9b0();
    local_30 = CONCAT31(local_30._1_3_,uVar2);
    local_34 = FUN__text__004ca9e0();
    FUN__text__004c9690(*(undefined2 *)(local_8 + 0x2c),
                        CONCAT22(extraout_var_03,*(undefined2 *)(local_8 + 0x2e)),0xff,
                        local_30 & 0xff,CONCAT22(extraout_var_03,(undefined2)local_20));
    FUN__text__004c97a0(*(undefined2 *)(local_8 + 0x2c),*(undefined2 *)(local_8 + 0x2e),0xff,
                        *(undefined2 *)(local_8 + 0x38 + (local_30 & 0xff) * 2),local_30 & 0xff,
                        CONCAT22(extraout_var_04,(undefined2)local_1c));
  }
  local_8 = 0x4ca03b;
  FUN__text__0056ce80();
  return;
}

