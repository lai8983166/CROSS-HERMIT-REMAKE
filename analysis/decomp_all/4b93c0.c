
void FUN__text__004b93c0(undefined2 *param_1,undefined2 *param_2,short *param_3)

{
  undefined1 uVar1;
  byte bVar2;
  undefined2 uVar3;
  ushort uVar4;
  undefined4 uVar5;
  ushort uVar6;
  int iVar7;
  undefined4 *puVar8;
  undefined4 local_1a8 [16];
  int local_168;
  uint local_164;
  int local_160;
  int local_15c;
  uint local_158;
  uint local_154;
  uint local_150;
  uint local_14c;
  int local_148;
  uint local_144;
  uint local_140;
  uint local_13c;
  int local_138;
  uint local_134;
  uint local_130;
  uint local_12c;
  uint local_128;
  int local_124;
  uint local_120;
  uint local_11c;
  uint local_118;
  int local_114;
  uint local_110;
  uint local_10c;
  uint local_108;
  uint local_104;
  uint local_100;
  uint local_fc;
  uint local_f8;
  uint local_f4;
  uint local_f0;
  uint local_ec;
  uint local_e8;
  uint local_e4;
  uint local_e0;
  uint local_dc;
  uint local_d8;
  uint local_d4;
  char local_d0;
  int local_cc;
  uint local_c8;
  uint local_c4;
  uint local_c0;
  int local_bc;
  uint local_b8;
  uint local_b4;
  uint local_b0;
  int local_ac;
  uint local_a8;
  uint local_a4;
  uint local_a0;
  int local_9c;
  uint local_98;
  uint local_94;
  int local_90;
  int local_8c;
  uint local_88;
  uint local_84;
  int local_80;
  int local_7c;
  undefined2 *local_78;
  ushort local_74;
  undefined2 uStack_72;
  ushort local_70;
  undefined2 uStack_6e;
  short local_6c;
  undefined2 uStack_6a;
  uint local_68;
  short local_64;
  ushort local_60;
  ushort local_5c;
  ushort local_58;
  undefined2 uStack_56;
  ushort local_54;
  undefined2 uStack_52;
  undefined4 local_50;
  undefined2 local_4c;
  undefined *local_48;
  undefined4 local_44;
  undefined2 local_40;
  undefined4 local_3c;
  undefined4 local_38;
  int local_34;
  ushort local_30;
  ushort local_2c;
  undefined2 uStack_2a;
  uint local_28;
  uint local_24;
  uint local_20;
  uint local_1c;
  uint local_18;
  uint local_14;
  uint local_10;
  uint local_c;
  uint local_8;
  
  iVar7 = 0x69;
  puVar8 = local_1a8;
  while( true ) {
    if (iVar7 == 0) break;
    iVar7 = iVar7 + -1;
    *puVar8 = 0xcccccccc;
    puVar8 = puVar8 + 1;
  }
  FUN__text__004db340(param_1,param_3);
  local_38 = (uint)local_38._2_2_ << 0x10;
  local_3c = (uint)local_3c._2_2_ << 0x10;
  local_40 = 0;
  local_44 = (uint)local_44._2_2_ << 0x10;
  while ((local_44 & 0xffff) < 8) {
    local_7c = (int)(short)param_1[(local_44 & 0xffff) + 0x29];
    if (local_7c == 1) {
      local_38 = CONCAT22(local_38._2_2_,1);
    }
    else if (local_7c == 5) {
      local_3c = CONCAT22(local_3c._2_2_,1);
    }
    local_44 = CONCAT22(local_44._2_2_,(short)local_44 + 1);
  }
  uVar3 = FUN__text__004d1ba0(*param_1,0,0x3ff);
  *param_2 = uVar3;
  uVar3 = FUN__text__004d1ba0(*param_1,0,0x3ff);
  param_2[1] = uVar3;
  uVar1 = FUN__text__004d1ba0(*(undefined1 *)(param_1 + 6),1,0x87);
  local_8 = CONCAT31(local_8._1_3_,uVar1);
  uVar1 = FUN__text__004d1ba0(*(undefined1 *)(param_1 + 10),1,0x87);
  local_c = CONCAT31(local_c._1_3_,uVar1);
  uVar1 = FUN__text__004d1ba0(*(undefined1 *)(param_1 + 0xe),1,0x87);
  local_10 = CONCAT31(local_10._1_3_,uVar1);
  uVar1 = FUN__text__004d1ba0(*(undefined1 *)(param_1 + 0x12),1,0x87);
  local_14 = CONCAT31(local_14._1_3_,uVar1);
  uVar1 = FUN__text__004d1ba0(*(undefined1 *)(param_1 + 0x16),1,0x87);
  local_18 = CONCAT31(local_18._1_3_,uVar1);
  uVar1 = FUN__text__004d1ba0(*(undefined1 *)(param_1 + 0x1a),1,0x87);
  local_1c = CONCAT31(local_1c._1_3_,uVar1);
  uVar1 = FUN__text__004d1ba0(*(undefined1 *)(param_1 + 0x1e),1,0x87);
  local_20 = CONCAT31(local_20._1_3_,uVar1);
  *(byte *)(param_2 + 2) = (byte)local_8;
  *(undefined1 *)((int)param_2 + 5) = (undefined1)local_c;
  *(undefined1 *)(param_2 + 3) = (undefined1)local_10;
  *(undefined1 *)((int)param_2 + 7) = (undefined1)local_14;
  *(undefined1 *)(param_2 + 4) = (undefined1)local_18;
  *(undefined1 *)((int)param_2 + 9) = (undefined1)local_1c;
  *(undefined1 *)(param_2 + 5) = uVar1;
  uVar3 = FUN__text__004d1ba0((int)(short)param_1[3],0,0x3ff);
  local_28 = CONCAT22(local_28._2_2_,uVar3);
  param_2[6] = uVar3;
  uVar1 = FUN__text__004d1ba0(*(undefined1 *)(param_1 + 0x28),0,99);
  local_24 = CONCAT31(local_24._1_3_,uVar1);
  *(undefined1 *)(param_2 + 7) = uVar1;
  *(undefined1 *)((int)param_2 + 0xf) = 0;
  param_2[8] = (ushort)(byte)(&DAT_006b2da8)[(local_28 & 0xffff) * 0x40];
  param_2[9] = 0;
  local_30 = (ushort)((int)(((local_1c & 0xff) * 3 + (local_8 & 0xff) + (local_c & 0xff) +
                             (uint)(ushort)param_3[0x15] + (int)param_3[8]) *
                           (uint)*(ushort *)(&DAT_006b2d8e + (local_28 & 0xffff) * 0x40)) / 100);
  uVar3 = FUN__text__004d1ba0((int)(short)local_30,1,999);
  param_2[10] = uVar3;
  local_80 = (uint)*(ushort *)(&DAT_006b2d90 + (local_28 & 0xffff) * 0x40) - (local_1c & 0xff);
  local_84 = local_8 & 0xff;
  local_88 = (uint)(ushort)param_3[0x16];
  local_8c = (int)param_3[9];
  local_30 = __ftol();
  uVar3 = FUN__text__004d1ba0((int)(short)local_30,0x1e,999);
  param_2[0xc] = uVar3;
  local_30 = (ushort)((int)(((local_20 & 0xff) * 3 + (local_18 & 0xff) + (local_14 & 0xff) +
                             (uint)(ushort)param_3[0x17] + (int)param_3[0xf]) *
                           (uint)*(ushort *)(&DAT_006b2d92 + (local_28 & 0xffff) * 0x40)) / 100);
  uVar3 = FUN__text__004d1ba0((int)(short)local_30,1,999);
  param_2[0xd] = uVar3;
  local_90 = (uint)*(ushort *)(&DAT_006b2d94 + (local_28 & 0xffff) * 0x40) - (local_20 & 0xff);
  local_94 = local_14 & 0xff;
  local_98 = (uint)(ushort)param_3[0x18];
  local_9c = (int)param_3[10];
  local_30 = __ftol();
  uVar3 = FUN__text__004d1ba0((int)(short)local_30,0x1e,999);
  param_2[0xf] = uVar3;
  local_34 = (uint)(ushort)param_3[0x1e] * 0xe10;
  iVar7 = FUN__text__004d1ba0(local_24 & 0xff,0,0x32);
  local_34 = local_34 + *(int *)(&DAT_006e4528 + iVar7 * 4) * 0x3c + *(int *)(param_3 + 0x10);
  uVar5 = FUN__text__004d1ba0(local_34,1,0x57030);
  *(undefined4 *)(param_2 + 0x10) = uVar5;
  *(undefined4 *)(param_2 + 0x14) = 0;
  local_a0 = (uint)(byte)(&DAT_006b2d9a)[(local_28 & 0xffff) * 0x40];
  local_a4 = local_10 & 0xff;
  local_a8 = (uint)*(byte *)(param_3 + 0x19);
  local_30 = __ftol();
  uVar1 = FUN__text__004d1ba0((int)(short)local_30,0,0x20);
  *(undefined1 *)(param_2 + 0x16) = uVar1;
  local_30 = *(short *)(&DAT_006b2d9c + (local_28 & 0xffff) * 0x40) +
             (short)((((int)(uint)*(ushort *)(&DAT_006b2d9c + (local_28 & 0xffff) * 0x40) >> 1) *
                     (local_c & 0xff)) / 100) + param_3[0x1a] + param_3[0xe];
  uVar3 = FUN__text__004d1ba0((int)(short)local_30,0,999);
  param_2[0x17] = uVar3;
  uVar1 = FUN__text__004d1ba0((&DAT_006b2d9e)[(local_28 & 0xffff) * 0x40],0,7);
  *(undefined1 *)(param_2 + 0x18) = uVar1;
  _local_2c = CONCAT22(uStack_2a,*(ushort *)(&DAT_006b2da0 + (local_28 & 0xffff) * 0x40));
  iVar7 = (uint)*(ushort *)(&DAT_006b2da0 + (local_28 & 0xffff) * 0x40) * 0x48;
  local_48 = &DAT_006c2dc8 + iVar7;
  uVar3 = FUN__text__004d1ba0(*(undefined2 *)(&DAT_006c2dd2 + iVar7),0,0xffff);
  param_2[0x19] = uVar3;
  uVar3 = FUN__text__004d1ba0(*(undefined2 *)(local_48 + 0xe),0,0xffff);
  param_2[0x1a] = uVar3;
  uVar1 = FUN__text__004d1ba0(local_48[0x10],0,0x7f);
  *(undefined1 *)(param_2 + 0x1b) = uVar1;
  local_ac = (byte)(&DAT_006b2d8a)[(local_28 & 0xffff) * 0x40] - 1;
  switch(local_ac) {
  case 0:
    local_30 = (ushort)(byte)local_48[0x12] + (ushort)*(byte *)(param_3 + 0x1b);
    uVar1 = FUN__text__004d1ba0(local_30,0,0x7f);
    *(undefined1 *)((int)param_2 + 0x37) = uVar1;
    local_b0 = (uint)(byte)local_48[0x14];
    local_b4 = local_8 & 0xff;
    local_b8 = (uint)(ushort)param_3[0x12];
    local_bc = (int)*param_3;
    local_30 = __ftol();
    uVar3 = FUN__text__004d1ba0((int)(short)local_30,0,999);
    param_2[0x1c] = uVar3;
    local_30 = (short)((int)((int)*(short *)(local_48 + 0x24) * (local_8 & 0xff)) / 100) +
               param_3[0x14] + param_3[2];
    uVar3 = FUN__text__004d1ba0((int)(short)local_30,0,999);
    param_2[0x1e] = uVar3;
    local_30 = (short)((int)((int)*(short *)(local_48 + 0x20) * (local_8 & 0xff)) / 100) +
               param_3[0x13] + param_3[1] + (short)((int)(uint)(ushort)param_2[0x1e] >> 1);
    uVar3 = FUN__text__004d1ba0((int)(short)local_30,0,999);
    param_2[0x1d] = uVar3;
    break;
  case 1:
    local_30 = (ushort)(byte)local_48[0x12] + (ushort)*(byte *)(param_3 + 0x1b);
    uVar1 = FUN__text__004d1ba0(local_30,0,0x7f);
    *(undefined1 *)((int)param_2 + 0x37) = uVar1;
    local_30 = (ushort)(byte)local_48[0x14] + ((ushort)local_c & 0xff) + param_3[0x12] + *param_3;
    uVar3 = FUN__text__004d1ba0((int)(short)local_30,0,999);
    param_2[0x1c] = uVar3;
    local_30 = (short)((int)((int)*(short *)(local_48 + 0x24) * (local_c & 0xff)) / 100) +
               param_3[0x14] + param_3[2];
    uVar3 = FUN__text__004d1ba0((int)(short)local_30,0,999);
    param_2[0x1e] = uVar3;
    local_30 = (short)((int)((int)*(short *)(local_48 + 0x20) * (local_c & 0xff)) / 100) +
               param_3[0x13] + param_3[1] + (short)((int)(uint)(ushort)param_2[0x1e] >> 1);
    uVar3 = FUN__text__004d1ba0((int)(short)local_30,0,999);
    param_2[0x1d] = uVar3;
    break;
  case 2:
    local_c0 = (uint)(byte)local_48[0x14];
    local_c4 = local_10 & 0xff;
    local_c8 = (uint)(ushort)param_3[0x12];
    local_cc = (int)*param_3;
    local_30 = __ftol();
    uVar3 = FUN__text__004d1ba0((int)(short)local_30,0,999);
    param_2[0x1c] = uVar3;
    local_d0 = *(char *)(param_1 + 0x39);
    if (local_d0 == '\x01') {
      local_d4 = (uint)(byte)local_48[0x12];
      local_d8 = local_10 & 0xff;
      local_dc = local_8 & 0xff;
      local_e0 = (uint)*(byte *)(param_3 + 0x1b);
      local_30 = __ftol();
      uVar1 = FUN__text__004d1ba0((int)(short)local_30,0,0x7f);
      *(undefined1 *)((int)param_2 + 0x37) = uVar1;
      local_30 = (short)((int)((int)*(short *)(local_48 + 0x24) *
                              ((local_10 & 0xff) + (local_8 & 0xff) / 10)) / 100) + param_3[0x14] +
                 param_3[2];
      uVar3 = FUN__text__004d1ba0((int)(short)local_30,0,999);
      param_2[0x1e] = uVar3;
      local_30 = (short)((int)((int)*(short *)(local_48 + 0x20) *
                              ((local_10 & 0xff) + (local_8 & 0xff) / 10)) / 100) + param_3[0x13] +
                 param_3[1] + (short)((int)(uint)(ushort)param_2[0x1e] >> 1);
      uVar3 = FUN__text__004d1ba0((int)(short)local_30,0,999);
      param_2[0x1d] = uVar3;
    }
    else if (local_d0 == '\x02') {
      local_e4 = (uint)(byte)local_48[0x12];
      local_e8 = local_10 & 0xff;
      local_ec = (uint)*(byte *)(param_3 + 0x1b);
      local_30 = __ftol();
      uVar1 = FUN__text__004d1ba0((int)(short)local_30,0,0x7f);
      *(undefined1 *)((int)param_2 + 0x37) = uVar1;
      local_30 = (short)((int)((int)*(short *)(local_48 + 0x24) * (local_10 & 0xff)) / 100) +
                 param_3[0x14] + param_3[2];
      uVar3 = FUN__text__004d1ba0((int)(short)local_30,0,999);
      param_2[0x1e] = uVar3;
      local_30 = (short)((int)((int)*(short *)(local_48 + 0x20) * (local_10 & 0xff)) / 100) +
                 param_3[0x13] + param_3[1] + (short)((int)(uint)(ushort)param_2[0x1e] >> 1);
      uVar3 = FUN__text__004d1ba0((int)(short)local_30,0,999);
      param_2[0x1d] = uVar3;
    }
    break;
  case 3:
    local_f0 = (uint)(byte)local_48[0x12];
    local_f4 = local_14 & 0xff;
    local_f8 = (uint)*(byte *)(param_3 + 0x1b);
    local_30 = __ftol();
    uVar1 = FUN__text__004d1ba0((int)(short)local_30,0,0x7f);
    *(undefined1 *)((int)param_2 + 0x37) = uVar1;
    param_2[0x1d] = 999;
    local_30 = (short)((int)((int)*(short *)(local_48 + 0x24) * (local_14 & 0xff)) / 100) +
               param_3[0x14] + param_3[2];
    uVar3 = FUN__text__004d1ba0((int)(short)local_30,0,999);
    param_2[0x1e] = uVar3;
    local_30 = (short)((int)((int)*(short *)(local_48 + 0x20) * (local_14 & 0xff)) / 100) +
               param_3[0x13] + param_3[1] + (short)((int)(uint)(ushort)param_2[0x1e] >> 1);
    uVar3 = FUN__text__004d1ba0((int)(short)local_30,0,999);
    param_2[0x1d] = uVar3;
    param_2[0x1c] = 999;
    break;
  case 4:
    local_fc = (uint)(byte)local_48[0x12];
    local_100 = local_18 & 0xff;
    local_104 = (uint)*(byte *)(param_3 + 0x1b);
    local_30 = __ftol();
    uVar1 = FUN__text__004d1ba0((int)(short)local_30,0,0x7f);
    *(undefined1 *)((int)param_2 + 0x37) = uVar1;
    param_2[0x1d] = 999;
    local_30 = (short)((int)((int)*(short *)(local_48 + 0x24) * (local_18 & 0xff)) / 100) +
               param_3[0x14] + param_3[2];
    uVar3 = FUN__text__004d1ba0((int)(short)local_30,0,999);
    param_2[0x1e] = uVar3;
    local_30 = (short)((int)((int)*(short *)(local_48 + 0x20) * (local_18 & 0xff)) / 100) +
               param_3[0x13] + param_3[1] + (short)((int)(uint)(ushort)param_2[0x1e] >> 1);
    uVar3 = FUN__text__004d1ba0((int)(short)local_30,0,999);
    param_2[0x1d] = uVar3;
    param_2[0x1c] = 999;
  }
  bVar2 = FUN__text__004d1ba0(*(undefined2 *)(local_48 + 2),0,999);
  param_2[0x1f] = (ushort)bVar2;
  uVar1 = FUN__text__004d1ba0(local_48[5],0,7);
  *(undefined1 *)(param_2 + 0x20) = uVar1;
  uVar1 = FUN__text__004d1ba0((char)param_3[0x20],0,100);
  *(undefined1 *)((int)param_2 + 0x41) = uVar1;
  uVar3 = FUN__text__004d1ba0(param_3[0x21],0,999);
  param_2[0x21] = uVar3;
  uVar1 = FUN__text__004d1ba0(local_48[0x16],0,0x7f);
  *(undefined1 *)(param_2 + 0x22) = uVar1;
  uVar1 = FUN__text__004d1ba0(local_48[0x1a],0,0x7f);
  *(undefined1 *)((int)param_2 + 0x45) = uVar1;
  uVar5 = FUN__text__004d1ba0(*(undefined4 *)(param_3 + 0x24),0,0x7fffffff);
  *(undefined4 *)(param_2 + 0x24) = uVar5;
  local_108 = ((uint)(byte)(&DAT_006b2da2)[(local_28 & 0xffff) * 0x40] * (local_c & 0xff)) / 100;
  local_10c = local_c & 0xff;
  local_110 = (uint)*(byte *)((int)param_3 + 0x37);
  local_114 = (int)param_3[3];
  local_30 = __ftol();
  uVar1 = FUN__text__004d1ba0((int)(short)local_30,0,0xff);
  *(undefined1 *)(param_2 + 0x26) = uVar1;
  local_118 = ((uint)(byte)(&DAT_006b2da3)[(local_28 & 0xffff) * 0x40] * (local_8 & 0xff)) / 100;
  local_11c = local_8 & 0xff;
  local_120 = (uint)*(byte *)((int)param_3 + 0x39);
  local_124 = (int)param_3[5];
  local_30 = __ftol();
  uVar1 = FUN__text__004d1ba0((int)(short)local_30,0,0xff);
  *(undefined1 *)((int)param_2 + 0x4d) = uVar1;
  local_128 = (uint)(byte)(&DAT_006b2da4)[(local_28 & 0xffff) * 0x40];
  local_12c = local_1c & 0xff;
  local_130 = local_10 & 0xff;
  local_134 = (uint)*(byte *)(param_3 + 0x1c);
  local_138 = (int)param_3[4];
  local_30 = __ftol();
  uVar1 = FUN__text__004d1ba0((int)(short)local_30,0,99);
  *(undefined1 *)(param_2 + 0x27) = uVar1;
  local_13c = (uint)(byte)(&DAT_006b2da5)[(local_28 & 0xffff) * 0x40];
  local_140 = local_18 & 0xff;
  local_144 = (uint)*(byte *)(param_3 + 0x1d);
  local_148 = (int)param_3[6];
  local_30 = __ftol();
  uVar1 = FUN__text__004d1ba0((int)(short)local_30,0,0xff);
  *(undefined1 *)((int)param_2 + 0x4f) = uVar1;
  local_14c = (uint)(byte)(&DAT_006b2da6)[(local_28 & 0xffff) * 0x40];
  local_150 = local_20 & 0xff;
  local_154 = local_14 & 0xff;
  local_158 = (uint)*(byte *)((int)param_3 + 0x3b);
  local_15c = (int)param_3[7];
  local_30 = __ftol();
  uVar1 = FUN__text__004d1ba0((int)(short)local_30,0,99);
  *(undefined1 *)(param_2 + 0x28) = uVar1;
  if ((local_38 & 0xffff) == 0) {
    local_168 = (int)(short)param_2[10];
    local_30 = __ftol();
  }
  else {
    local_160 = (int)((int)(short)param_2[10] *
                     (uint)(byte)(&DAT_006b2da9)[(local_28 & 0xffff) * 0x40]) / 100;
    local_164 = local_8 & 0xff;
    local_30 = __ftol();
  }
  uVar3 = FUN__text__004d1ba0((int)(short)local_30,0,999);
  param_2[0x29] = uVar3;
  if ((local_3c & 0xffff) == 0) {
    local_30 = 0;
  }
  else {
    local_30 = (ushort)(byte)local_8;
  }
  uVar3 = FUN__text__004d1ba0(local_30,0,999);
  param_2[0x2a] = uVar3;
  param_2[0xb] = param_2[10];
  param_2[0xe] = param_2[0xd];
  *(undefined4 *)(param_2 + 0x12) = *(undefined4 *)(param_2 + 0x10);
  local_4c = 0;
  uVar4 = (ushort)(byte)(&DAT_006b2d8b)[(short)param_1[3] * 0x40];
  _local_54 = CONCAT22(uStack_52,uVar4);
  bVar2 = (&DAT_006b2d8c)[(short)param_1[3] * 0x40];
  _local_58 = CONCAT22(uStack_56,(ushort)bVar2);
  local_50 = (uint)local_50._2_2_ << 0x10;
  while ((local_50 & 0xffff) < (uint)uVar4) {
    param_2[(local_50 & 0xffff) + 0x42] = param_1[(local_50 & 0xffff) + 0x29];
    local_50 = CONCAT22(local_50._2_2_,(short)local_50 + 1);
  }
  local_50 = (uint)local_50._2_2_ << 0x10;
  while ((local_50 & 0xffff) < (uint)(ushort)bVar2) {
    if (param_1[(local_50 & 0xffff) + 0x31] == 0) {
      param_2[(uint)uVar4 + (local_50 & 0xffff) + 0x42] = 0;
    }
    else {
      param_2[(uint)uVar4 + (local_50 & 0xffff) + 0x42] =
           param_1[(local_50 & 0xffff) + 0x31] | 0x8000;
    }
    local_50 = CONCAT22(local_50._2_2_,(short)local_50 + 1);
  }
  local_5c = 0;
  local_60 = 0;
  local_78 = param_1;
  for (local_64 = 0; local_64 < 8; local_64 = local_64 + 1) {
    uVar4 = param_1[local_64 + 0x31];
    _local_74 = CONCAT22(uStack_72,uVar4);
    if (uVar4 != 0) {
      local_68 = local_68 & 0xffff0000;
      while ((local_68 & 0xffff) < 3) {
        _local_6c = CONCAT22(uStack_6a,
                             (short)(char)(&DAT_006d514d)[(local_68 & 0xffff) + (uint)uVar4 * 0x38])
        ;
        if ((char)(&DAT_006d514d)[(local_68 & 0xffff) + (uint)uVar4 * 0x38] == 0x19) {
          uVar6 = (ushort)(byte)(&DAT_006d5140)[(uint)uVar4 * 0x38];
          _local_70 = CONCAT22(uStack_6e,uVar6);
          if (local_60 < (byte)(&DAT_006f408b)[(uint)uVar6 * 0x10]) {
            local_60 = (ushort)(byte)(&DAT_006f408b)[(uint)uVar6 * 0x10];
            local_5c = uVar6;
          }
        }
        local_68 = CONCAT22(local_68._2_2_,(short)local_68 + 1);
      }
    }
  }
  *(undefined1 *)((int)param_2 + 0x45) = (undefined1)local_5c;
  local_8 = 0x4baa71;
  FUN__text__0056ce80();
  return;
}

