
void __thiscall FUN__text__004c8290(undefined4 *param_1,undefined2 param_2)

{
  undefined2 uVar1;
  short sVar2;
  undefined2 uVar3;
  short sVar4;
  undefined2 extraout_var;
  undefined2 extraout_var_00;
  uint uVar5;
  int iVar6;
  undefined2 uVar7;
  undefined2 extraout_var_01;
  undefined2 extraout_var_02;
  undefined2 extraout_var_03;
  undefined2 extraout_var_04;
  undefined2 extraout_var_05;
  undefined2 extraout_var_06;
  undefined2 extraout_var_07;
  undefined4 *puVar8;
  undefined4 local_c0 [16];
  int local_80;
  uint local_7c;
  uint local_78;
  undefined1 local_74 [4];
  uint local_70;
  uint local_68;
  uint local_64;
  undefined4 local_60;
  uint local_5c;
  undefined4 local_58;
  undefined1 local_54;
  uint local_50;
  uint local_4c;
  undefined2 local_48;
  undefined2 local_44;
  undefined2 local_40;
  uint local_3c;
  uint local_38;
  uint local_34;
  uint local_30;
  uint local_2c;
  uint local_28;
  undefined2 local_24;
  undefined2 local_20;
  ushort local_1c;
  uint local_18;
  uint local_14;
  undefined1 local_10;
  uint local_c;
  undefined4 *local_8;
  
  iVar6 = 0x2f;
  puVar8 = local_c0;
  while( true ) {
    if (iVar6 == 0) break;
    iVar6 = iVar6 + -1;
    *puVar8 = 0xcccccccc;
    puVar8 = puVar8 + 1;
  }
  local_10 = *(undefined1 *)param_1[0x683];
  uVar3 = *(undefined2 *)(param_1[0x683] + 2);
  local_14 = CONCAT22(local_14._2_2_,uVar3);
  uVar1 = *(undefined2 *)(param_1[0x683] + 4);
  local_18 = CONCAT22(local_18._2_2_,uVar1);
  local_1c = (ushort)*(byte *)(param_1[0x683] + 0x24);
  local_20 = *(undefined2 *)(param_1[0x683] + 0xe);
  local_24 = *(undefined2 *)(param_1[0x683] + 0x10);
  *(undefined2 *)((int)param_1 + 0x16) = local_24;
  local_28 = CONCAT22(local_28._2_2_,*(undefined2 *)(param_1[0x683] + 0x1c));
  local_2c = CONCAT22(local_2c._2_2_,*(undefined2 *)(param_1[0x683] + 0x1e));
  local_30 = CONCAT22(local_30._2_2_,*(undefined2 *)(param_1[0x683] + 0x20));
  local_34 = CONCAT22(local_34._2_2_,*(undefined2 *)(param_1[0x683] + 0x22));
  local_3c = CONCAT22(local_3c._2_2_,0x37);
  local_40 = 0x38;
  local_44 = 0x39;
  local_48 = 0x3a;
  local_4c = CONCAT31(local_4c._1_3_,1);
  local_50 = CONCAT31(local_50._1_3_,1);
  local_54 = 0;
  local_7c = (int)*(short *)(param_1 + 2) - 1;
  local_8 = param_1;
  if (local_7c < 7) {
    sVar4 = *(short *)(param_1 + 2) >> 0xf;
    uVar7 = (undefined2)(local_7c >> 0x10);
    switch(local_7c) {
    case 0:
      local_4c = (uint)local_4c._1_3_ << 8;
      local_50 = (uint)local_50._1_3_ << 8;
      sVar4 = *(short *)(param_1 + 3);
      *(short *)(param_1 + 3) = *(short *)(param_1 + 3) + -1;
      if (sVar4 == 0) {
        *(undefined2 *)(param_1 + 2) = 2;
      }
      break;
    case 1:
      local_4c = (uint)local_4c._1_3_ << 8;
      local_50 = (uint)local_50._1_3_ << 8;
      uVar3 = FUN__text__004cd850(*(undefined2 *)((int)param_1 + 0xe),
                                  CONCAT22(sVar4,*(undefined2 *)(param_1 + 4)),0xff);
      local_38._0_2_ = uVar3;
      FUN__text__004ca600(CONCAT22(extraout_var_01,(undefined2)local_14),local_18 & 0xffff,
                          CONCAT22(extraout_var_04,local_1c),CONCAT22(extraout_var_01,uVar3),
                          local_44);
      uVar3 = FUN__text__004cd850(*(undefined2 *)((int)local_8 + 0xe),
                                  CONCAT22(extraout_var,*(undefined2 *)(local_8 + 4)),0xcc);
      local_38 = CONCAT22(local_38._2_2_,uVar3);
      FUN__text__00410310((local_14 & 0xffff) + (local_28 & 0xffff),
                          (local_18 & 0xffff) + (local_2c & 0xffff),local_30 & 0xffff,
                          local_34 & 0xffff,CONCAT22(extraout_var_02,local_48),
                          local_38 << 0x18 | 0x10101,1);
      sVar4 = *(short *)((int)local_8 + 0xe);
      *(short *)((int)local_8 + 0xe) = *(short *)((int)local_8 + 0xe) + 1;
      if (*(short *)(local_8 + 4) < sVar4) {
        *(undefined2 *)((int)local_8 + 0xe) = 0;
        *(undefined2 *)(local_8 + 3) = 0x10;
        *(undefined2 *)(local_8 + 2) = 3;
      }
      break;
    case 2:
      local_50 = (uint)local_50._1_3_ << 8;
      local_38._0_2_ = 0xff;
      FUN__text__004ca600(CONCAT22(uVar7,uVar3),CONCAT22(sVar4,uVar1),CONCAT22(uVar7,local_1c),
                          CONCAT22(uVar7,0xff),CONCAT22(sVar4,0x39));
      local_38 = CONCAT22(local_38._2_2_,0xcc);
      FUN__text__00410310((local_14 & 0xffff) + (local_28 & 0xffff),
                          (local_18 & 0xffff) + (local_2c & 0xffff),local_30 & 0xffff,
                          local_34 & 0xffff,CONCAT22(extraout_var_00,local_48),
                          local_38 << 0x18 | 0x10101,1);
      break;
    case 3:
      local_4c = (uint)local_4c._1_3_ << 8;
      local_50 = (uint)local_50._1_3_ << 8;
      local_38._0_2_ = 0xff;
      FUN__text__004ca600(CONCAT22(sVar4,uVar3),CONCAT22(uVar7,uVar1),CONCAT22(uVar7,local_1c),
                          CONCAT22(sVar4,0xff),CONCAT22(uVar7,0x39));
      local_38 = CONCAT22(local_38._2_2_,0xcc);
      FUN__text__00410310((local_14 & 0xffff) + (local_28 & 0xffff),
                          (local_18 & 0xffff) + (local_2c & 0xffff),local_30 & 0xffff,
                          local_34 & 0xffff,CONCAT22(extraout_var_05,local_48),
                          local_38 << 0x18 | 0x10101,1);
      sVar4 = *(short *)(local_8 + 3);
      *(short *)(local_8 + 3) = *(short *)(local_8 + 3) + -1;
      if (sVar4 == 0) {
        *(undefined2 *)(local_8 + 2) = 5;
      }
      break;
    case 4:
      local_4c = (uint)local_4c._1_3_ << 8;
      local_50 = (uint)local_50._1_3_ << 8;
      uVar5 = FUN__text__004cd850(*(undefined2 *)((int)param_1 + 0xe),
                                  CONCAT22(sVar4,*(undefined2 *)(param_1 + 4)),0xff);
      uVar5 = 0xff - (uVar5 & 0xffff);
      local_38._0_2_ = (short)uVar5;
      FUN__text__004ca600(local_14 & 0xffff,CONCAT22(extraout_var_06,(undefined2)local_18),
                          CONCAT22((short)(uVar5 >> 0x10),local_1c),uVar5 & 0xffff,
                          CONCAT22(extraout_var_06,local_44));
      sVar4 = FUN__text__004cd850(*(undefined2 *)((int)local_8 + 0xe),
                                  CONCAT22(extraout_var_07,*(undefined2 *)(local_8 + 4)),0xcc);
      local_38 = CONCAT22(local_38._2_2_,0xcc - sVar4);
      FUN__text__00410310((local_14 & 0xffff) + (local_28 & 0xffff),
                          (local_18 & 0xffff) + (local_2c & 0xffff),local_30 & 0xffff,
                          local_34 & 0xffff,CONCAT22(extraout_var_03,local_48),
                          local_38 << 0x18 | 0x10101,1);
      sVar4 = *(short *)((int)local_8 + 0xe);
      *(short *)((int)local_8 + 0xe) = *(short *)((int)local_8 + 0xe) + 1;
      if (*(short *)((int)local_8 + 0x12) < sVar4) {
        *(undefined2 *)((int)local_8 + 0xe) = 0;
        *(undefined2 *)(local_8 + 2) = 6;
      }
      local_4c = local_4c & 0xffffff00;
      break;
    case 5:
      local_4c = (uint)local_4c._1_3_ << 8;
      break;
    case 6:
    }
  }
  local_60 = (uint)local_60._2_2_ << 0x10;
  local_58 = (uint)local_58._2_2_ << 0x10;
  while ((int)(local_58 & 0xffff) < (int)*(short *)((int)local_8 + 10)) {
    local_80 = *(ushort *)(local_8 + (local_58 & 0xffff) * 0xa6 + 6) - 1;
    uVar3 = (undefined2)((uint)local_80 >> 0x10);
    switch(local_80) {
    case 0:
      local_4c = local_4c & 0xffffff00;
      local_50 = local_50 & 0xffffff00;
      sVar4 = *(short *)((int)local_8 + (local_58 & 0xffff) * 0x298 + 0x22);
      *(short *)((int)local_8 + (local_58 & 0xffff) * 0x298 + 0x22) =
           *(short *)((int)local_8 + (local_58 & 0xffff) * 0x298 + 0x22) + -1;
      if (sVar4 == 0) {
        *(undefined2 *)(local_8 + (local_58 & 0xffff) * 0xa6 + 6) = 2;
      }
      break;
    case 1:
      local_4c = (uint)local_4c._1_3_ << 8;
      local_50 = (uint)local_50._1_3_ << 8;
      local_60 = CONCAT22(local_60._2_2_,1);
      uVar3 = FUN__text__004cd850(CONCAT22(uVar3,*(undefined2 *)
                                                  (local_8 + (local_58 & 0xffff) * 0xa6 + 9)),
                                  CONCAT22(uVar3,*(undefined2 *)
                                                  ((int)local_8 + (local_58 & 0xffff) * 0x298 + 0x26
                                                  )),0xff);
      local_38 = CONCAT22(local_38._2_2_,uVar3);
      sVar4 = *(short *)(local_8 + (local_58 & 0xffff) * 0xa6 + 9);
      sVar2 = *(short *)((int)local_8 + (local_58 & 0xffff) * 0x298 + 0x26);
      *(short *)(local_8 + (local_58 & 0xffff) * 0xa6 + 9) =
           *(short *)(local_8 + (local_58 & 0xffff) * 0xa6 + 9) + 1;
      if (sVar2 < sVar4) {
        *(undefined2 *)(local_8 + (local_58 & 0xffff) * 0xa6 + 9) = 0;
        *(undefined2 *)((int)local_8 + (local_58 & 0xffff) * 0x298 + 0x22) = 0;
        *(undefined2 *)(local_8 + (local_58 & 0xffff) * 0xa6 + 6) = 3;
      }
      break;
    case 2:
      local_50 = (uint)local_50._1_3_ << 8;
      local_60 = CONCAT22(local_60._2_2_,1);
      local_38 = CONCAT22(local_38._2_2_,0xff);
      break;
    case 3:
      local_4c = (uint)local_4c._1_3_ << 8;
      local_50 = (uint)local_50._1_3_ << 8;
      local_60 = CONCAT22(local_60._2_2_,1);
      local_38 = CONCAT22(local_38._2_2_,0xff);
      sVar4 = *(short *)((int)local_8 + (local_58 & 0xffff) * 0x298 + 0x22);
      *(short *)((int)local_8 + (local_58 & 0xffff) * 0x298 + 0x22) =
           *(short *)((int)local_8 + (local_58 & 0xffff) * 0x298 + 0x22) + -1;
      if (sVar4 == 0) {
        *(undefined2 *)(local_8 + (local_58 & 0xffff) * 0xa6 + 6) = 5;
      }
      break;
    case 4:
      local_4c = (uint)local_4c._1_3_ << 8;
      local_50 = (uint)local_50._1_3_ << 8;
      local_60 = CONCAT22(local_60._2_2_,1);
      sVar4 = FUN__text__004cd850(CONCAT22(uVar3,*(undefined2 *)
                                                  (local_8 + (local_58 & 0xffff) * 0xa6 + 9)),
                                  CONCAT22(uVar3,*(undefined2 *)
                                                  (local_8 + (local_58 & 0xffff) * 0xa6 + 10)),0xff)
      ;
      local_38 = CONCAT22(local_38._2_2_,0xff - sVar4);
      sVar4 = *(short *)(local_8 + (local_58 & 0xffff) * 0xa6 + 9);
      sVar2 = *(short *)(local_8 + (local_58 & 0xffff) * 0xa6 + 10);
      *(short *)(local_8 + (local_58 & 0xffff) * 0xa6 + 9) =
           *(short *)(local_8 + (local_58 & 0xffff) * 0xa6 + 9) + 1;
      if (sVar2 < sVar4) {
        *(undefined2 *)(local_8 + (local_58 & 0xffff) * 0xa6 + 9) = 0;
        *(undefined2 *)(local_8 + (local_58 & 0xffff) * 0xa6 + 6) = 6;
      }
      break;
    case 5:
      local_4c = (uint)local_4c._1_3_ << 8;
    }
    if ((local_60 & 0xffff) != 0) {
      local_c = CONCAT22(local_c._2_2_,*(undefined2 *)(local_8 + (local_58 & 0xffff) * 0xa6 + 7));
      local_5c = local_5c & 0xffff0000;
      while ((int)(local_5c & 0xffff) <
             (int)*(short *)((int)local_8 + (local_58 & 0xffff) * 0x298 + 0x2a)) {
        FUN__text__004cbf00(local_8 + (local_58 & 0xffff) * 0xa6 + (local_5c & 0xffff) * 0x20 + 0xc,
                            (int)*(short *)((int)local_8 + (local_58 & 0xffff) * 0x298 + 0x1a),
                            local_c & 0xffff,1,local_38 & 0xffff,0xff,0xff,0xff,local_3c & 0xffff);
        local_c = CONCAT22(local_c._2_2_,
                           (short)local_c +
                           *(short *)((int)local_8 +
                                     (local_5c & 0xffff) * 0x80 + (local_58 & 0xffff) * 0x298 + 0x72
                                     ));
        local_5c = CONCAT22(local_5c._2_2_,(short)local_5c + 1);
      }
    }
    local_58 = CONCAT22(local_58._2_2_,(short)local_58 + 1);
  }
  if ((local_4c & 0xff) != 0) {
    local_64 = local_64 & 0xffff0000;
    while ((int)(local_64 & 0xffff) < (int)*(short *)((int)local_8 + 10)) {
      sVar4 = *(short *)((int)local_8 + 10) >> 0xf;
      FUN__text__004d5ec0(local_74,CONCAT22(sVar4,*(undefined2 *)
                                                   ((int)local_8 +
                                                   (local_64 & 0xffff) * 0x298 + 0x1a)),
                          CONCAT22(sVar4,*(undefined2 *)(local_8 + (local_64 & 0xffff) * 0xa6 + 7)),
                          CONCAT22(sVar4,*(undefined2 *)
                                          ((int)local_8 + (local_64 & 0xffff) * 0x298 + 0x1e)),
                          CONCAT22(sVar4,*(undefined2 *)(local_8 + (local_64 & 0xffff) * 0xa6 + 8)))
      ;
      if ((local_68 & 0xffff) != 0) {
        if ((local_70 & 1) != 0) {
          FUN__text__004c1f40(param_2,*local_8,local_8[1],local_64 & 0xffff);
          if (*(char *)((int)local_8 + 0x1a0a) != '\0') {
            *(undefined2 *)(local_8 + 2) = 4;
          }
          local_78 = local_78 & 0xffff0000;
          while ((int)(local_78 & 0xffff) < (int)*(short *)((int)local_8 + 10)) {
            *(undefined2 *)(local_8 + (local_78 & 0xffff) * 0xa6 + 6) = 4;
            local_78 = CONCAT22(local_78._2_2_,(short)local_78 + 1);
          }
        }
        FUN__text__00410310((int)*(short *)((int)local_8 + (local_64 & 0xffff) * 0x298 + 0x1a),
                            *(short *)(local_8 + (local_64 & 0xffff) * 0xa6 + 7) + 1,
                            (int)*(short *)((int)local_8 + (local_64 & 0xffff) * 0x298 + 0x1e),
                            *(short *)(local_8 + (local_64 & 0xffff) * 0xa6 + 8) + 4,local_40,
                            0xa0a0a020,1);
        break;
      }
      local_64 = CONCAT22(local_64._2_2_,(short)local_64 + 1);
    }
  }
  if ((local_50 & 0xff) == 1) {
    local_54 = 1;
  }
  local_8 = (undefined4 *)0x4c8ec4;
  FUN__text__0056ce80();
  return;
}

