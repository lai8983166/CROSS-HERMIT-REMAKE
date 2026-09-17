
void __fastcall FUN__text__004ca1b0(int param_1)

{
  undefined2 uVar1;
  short sVar2;
  undefined4 uVar3;
  int iVar4;
  undefined2 extraout_var;
  undefined2 extraout_var_00;
  undefined2 extraout_var_01;
  undefined2 extraout_var_02;
  undefined2 extraout_var_03;
  undefined2 extraout_var_04;
  undefined4 *puVar5;
  undefined4 local_64 [16];
  int local_24;
  undefined2 local_20;
  int local_1c;
  int local_18;
  int local_14;
  undefined2 local_10;
  undefined2 local_c;
  int local_8;
  
  puVar5 = local_64;
  for (iVar4 = 0x18; iVar4 != 0; iVar4 = iVar4 + -1) {
    *puVar5 = 0xcccccccc;
    puVar5 = puVar5 + 1;
  }
  local_c = 0x42;
  local_10 = 0x43;
  local_24 = *(ushort *)(param_1 + 2) - 2;
  uVar1 = (undefined2)((uint)local_24 >> 0x10);
  iVar4 = local_24;
  local_8 = param_1;
  switch(local_24) {
  case 1:
    uVar3 = FUN__text__004cd850(*(undefined2 *)(param_1 + 6),
                                CONCAT22(uVar1,*(undefined2 *)(param_1 + 0x10)),0xff);
    local_18._0_2_ = (short)uVar3;
    FUN__text__004ca600(*(undefined2 *)(local_8 + 0xc),*(undefined2 *)(local_8 + 0xe),
                        CONCAT22(extraout_var_01,*(undefined2 *)(local_8 + 8)),uVar3,
                        CONCAT22(extraout_var_01,local_c));
    uVar1 = FUN__text__004cd850(*(undefined2 *)(local_8 + 6),
                                CONCAT22(extraout_var_02,*(undefined2 *)(local_8 + 0x10)),0xcc);
    local_18 = CONCAT22(local_18._2_2_,uVar1);
    FUN__text__00410310((int)*(short *)(local_8 + 0xc) + (int)*(short *)(local_8 + 0x16),
                        (int)*(short *)(local_8 + 0xe) + (int)*(short *)(local_8 + 0x18),
                        (int)*(short *)(local_8 + 0x1a),(int)*(short *)(local_8 + 0x1c),local_10,
                        local_18 << 0x18 | 0x223438,1);
    *(short *)(local_8 + 6) = *(short *)(local_8 + 6) + 1;
    if (*(ushort *)(local_8 + 0x10) < *(ushort *)(local_8 + 6)) {
      *(undefined2 *)(local_8 + 6) = 0;
      *(undefined2 *)(local_8 + 2) = 2;
    }
    break;
  case 2:
    sVar2 = FUN__text__004cd850(*(undefined2 *)(param_1 + 6),
                                CONCAT22(uVar1,*(undefined2 *)(param_1 + 0x10)),0xff);
    local_1c._0_2_ = 0xff - sVar2;
    FUN__text__004ca600(*(undefined2 *)(local_8 + 0xc),*(undefined2 *)(local_8 + 0xe),
                        CONCAT22(extraout_var_03,*(undefined2 *)(local_8 + 8)),0xff - sVar2,
                        CONCAT22(extraout_var_03,local_c));
    sVar2 = FUN__text__004cd850(*(undefined2 *)(local_8 + 6),
                                CONCAT22(extraout_var_04,*(undefined2 *)(local_8 + 0x10)),0xcc);
    local_1c = CONCAT22(local_1c._2_2_,0xcc - sVar2);
    FUN__text__00410310((int)*(short *)(local_8 + 0xc) + (int)*(short *)(local_8 + 0x16),
                        (int)*(short *)(local_8 + 0xe) + (int)*(short *)(local_8 + 0x18),
                        (int)*(short *)(local_8 + 0x1a),(int)*(short *)(local_8 + 0x1c),
                        CONCAT22(extraout_var,local_10),local_1c << 0x18 | 0x223438,1);
    *(short *)(local_8 + 6) = *(short *)(local_8 + 6) + 1;
    if (*(ushort *)(local_8 + 0x10) < *(ushort *)(local_8 + 6)) {
      *(undefined2 *)(local_8 + 6) = 0;
      *(undefined2 *)(local_8 + 2) = 1;
    }
    break;
  case 3:
    local_20 = *(undefined2 *)(param_1 + 6);
    *(short *)(param_1 + 6) = *(short *)(param_1 + 6) + 1;
    if (*(ushort *)(param_1 + 0x10) < *(ushort *)(param_1 + 6)) {
      *(undefined2 *)(param_1 + 6) = 0;
      *(undefined2 *)(param_1 + 2) = 2;
    }
    break;
  case 4:
    *(short *)(param_1 + 0x12) = *(short *)(param_1 + 0x12) + 1;
    if (*(short *)(param_1 + 0x14) < *(short *)(param_1 + 0x12)) {
      *(undefined2 *)(param_1 + 0x12) = 0;
      *(undefined2 *)(param_1 + 2) = 3;
    }
    break;
  case 5:
    *(short *)(param_1 + 0x12) = *(short *)(param_1 + 0x12) + 1;
    if (*(short *)(param_1 + 0x14) < *(short *)(param_1 + 0x12)) {
      *(undefined2 *)(param_1 + 0x12) = 0;
      *(undefined2 *)(param_1 + 2) = 4;
    }
    iVar4 = 0;
  case 0:
    local_14 = CONCAT22(local_14._2_2_,0xcc);
    FUN__text__004ca600(*(undefined2 *)(param_1 + 0xc),*(undefined2 *)(param_1 + 0xe),
                        CONCAT22((short)((uint)iVar4 >> 0x10),*(undefined2 *)(param_1 + 8)),0xff,
                        0x42);
    FUN__text__00410310((int)*(short *)(local_8 + 0xc) + (int)*(short *)(local_8 + 0x16),
                        (int)*(short *)(local_8 + 0xe) + (int)*(short *)(local_8 + 0x18),
                        (int)*(short *)(local_8 + 0x1a),(int)*(short *)(local_8 + 0x1c),
                        CONCAT22(extraout_var_00,local_10),local_14 << 0x18 | 0x223438,1);
    FUN__text__004ca860();
  }
  local_8 = 0x4ca5df;
  FUN__text__0056ce80();
  return;
}

