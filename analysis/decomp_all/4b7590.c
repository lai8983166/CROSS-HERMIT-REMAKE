
void FUN__text__004b7590(short param_1,short param_2,short param_3,ushort param_4,uint param_5,
                        undefined2 param_6,uint param_7,uint param_8,short param_9,short param_10,
                        short param_11,uint param_12,char param_13)

{
  int iVar1;
  ushort uVar2;
  short sVar3;
  undefined4 *puVar4;
  undefined4 local_154 [16];
  char local_114;
  uint local_110;
  undefined2 local_10c;
  short local_108;
  short local_104;
  short local_100;
  undefined4 local_fc;
  short local_f8;
  short local_f4;
  short local_f0;
  undefined4 local_ec;
  undefined4 local_e8;
  short local_e4;
  short local_e0;
  short local_dc;
  short local_d8;
  uint local_d4;
  uint local_d0;
  short local_cc;
  short local_c8;
  undefined2 local_c4;
  undefined2 local_c0;
  short local_bc;
  undefined2 uStack_ba;
  undefined *local_b8;
  short local_b4;
  undefined2 uStack_b2;
  undefined4 local_b0;
  undefined2 local_ac;
  uint local_a8;
  uint local_a4;
  undefined4 local_a0;
  ushort local_9c;
  undefined2 uStack_9a;
  undefined2 local_98;
  short local_5c;
  short local_5a;
  ushort local_3c;
  undefined4 local_38;
  undefined4 local_34;
  undefined1 local_30;
  undefined1 local_2f;
  undefined1 local_2e;
  undefined1 local_2d;
  undefined2 local_24;
  undefined2 local_22;
  undefined2 local_20;
  undefined2 local_1e;
  short local_1c;
  short sStack_1a;
  short local_18;
  short local_16;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB__text__005902fc;
  local_10 = ExceptionList;
  iVar1 = 0x51;
  puVar4 = local_154;
  while( true ) {
    if (iVar1 == 0) break;
    iVar1 = iVar1 + -1;
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  ExceptionList = &local_10;
  FUN__text__004075e0();
  local_8 = 0;
  FUN__text__004077c0(DAT_007a49fc);
  uVar2 = local_b0._2_2_;
  local_3c = local_3c | 0x40;
  local_24 = 100;
  local_22 = 100;
  local_20 = 0;
  local_34 = 0;
  local_38 = 1;
  local_2d = 0xff;
  local_2e = 0x80;
  local_2f = 0x80;
  local_30 = 0x80;
  local_1e = param_6;
  local_98 = 0;
  local_ac = 0;
  local_b0 = (uint)local_b0._2_2_ << 0x10;
  iVar1 = (param_7 & 0xffff) * 0x10;
  local_b8 = &DAT_0061bae0 + iVar1;
  _local_bc = CONCAT22(uStack_ba,param_9);
  local_c0 = 0;
  local_c4 = 0;
  local_d8 = 0;
  local_110 = param_12 & 0xff;
  switch(local_110) {
  case 0:
    local_e8 = (uint)local_e8._2_2_ << 0x10;
    local_ec = (uint)local_ec._2_2_ << 0x10;
    local_f0 = 0;
    break;
  case 1:
    local_e8 = CONCAT22(local_e8._2_2_,1);
    local_ec = (uint)local_ec._2_2_ << 0x10;
    local_f0 = 0;
    break;
  case 2:
    local_e8 = (uint)local_e8._2_2_ << 0x10;
    local_ec = CONCAT22(local_ec._2_2_,1);
    local_f0 = 0;
    break;
  case 3:
    local_e8 = CONCAT22(local_e8._2_2_,1);
    local_ec = CONCAT22(local_ec._2_2_,1);
    local_f0 = 0;
    break;
  case 4:
    local_e8 = (uint)local_e8._2_2_ << 0x10;
    local_ec = (uint)local_ec._2_2_ << 0x10;
    local_f0 = 1;
    break;
  case 5:
    local_e8 = CONCAT22(local_e8._2_2_,1);
    local_ec = (uint)local_ec._2_2_ << 0x10;
    local_f0 = 1;
    break;
  case 6:
    local_e8 = (uint)local_e8._2_2_ << 0x10;
    local_ec = CONCAT22(local_ec._2_2_,1);
    local_f0 = 1;
    break;
  case 7:
    local_e8 = CONCAT22(local_e8._2_2_,1);
    local_ec = CONCAT22(local_ec._2_2_,1);
    local_f0 = 1;
  }
  local_b4 = 0;
  if ((param_5 & 0xffff) != 0) {
    local_b4 = ((short)param_5 + -1) * param_10;
  }
  local_b4 = local_b4 + (short)param_5 * param_9;
  if ((local_ec & 0xffff) != 0) {
    sVar3 = (short)((ulonglong)(param_5 & 0xffff) / 3);
    local_b0 = CONCAT22(uVar2,sVar3);
    if (sVar3 != 0) {
      _local_b4 = CONCAT22(uStack_b2,local_b4 + sVar3 * param_11 + sVar3 * param_10);
    }
  }
  if (local_f0 != 0) {
    local_f0 = -(short)_local_b4;
  }
  local_f4 = param_1 + local_f0;
  local_f8 = param_2;
  local_fc = (uint)local_fc._2_2_ << 0x10;
  local_100 = param_2 + -8 + *(short *)(&DAT_0061baea + iVar1);
  local_a0 = (uint)local_a0._2_2_ << 0x10;
  while ((local_a0 & 0xffff) < (param_5 & 0xffff)) {
    if ((local_a0 & 0xffff) + 1 == (param_5 & 0xffff)) {
      uVar2 = (ushort)((ulonglong)param_8 % 10);
      local_e8 = local_e8 & 0xffff0000;
      local_fc = CONCAT22(local_fc._2_2_,1);
    }
    else {
      local_a8 = 1;
      local_a4 = local_a4 & 0xffff0000;
      while ((int)(local_a4 & 0xffff) < (int)(((param_5 & 0xffff) - 1) - (local_a0 & 0xffff))) {
        local_a8 = local_a8 * 10;
        local_a4 = CONCAT22(local_a4._2_2_,(short)local_a4 + 1);
      }
      uVar2 = (ushort)((longlong)(int)(param_8 / local_a8) % 10);
    }
    uVar2 = uVar2 % 10;
    _local_9c = CONCAT22(uStack_9a,uVar2);
    if (uVar2 != 0) {
      local_e8 = local_e8 & 0xffff0000;
    }
    if ((local_e8 & 0xffff) == 0) {
      local_c8 = param_3 + *(short *)(local_b8 + 4) + *(short *)(local_b8 + 0xe) * uVar2;
      local_cc = param_4 + *(short *)(local_b8 + 6);
      local_d0 = CONCAT22(local_d0._2_2_,local_f4);
      local_d4 = CONCAT22(local_d4._2_2_,local_f8);
      FUN__text__00407870(*local_b8,*(undefined2 *)(local_b8 + 2));
      local_5c = *(short *)(local_b8 + 8);
      local_5a = *(short *)(local_b8 + 10);
      local_1c = local_c8;
      sStack_1a = local_cc;
      local_18 = local_c8 + local_5c;
      local_16 = local_cc + local_5a;
      if (local_d8 == 0) {
        local_d8 = 1;
        local_dc = (short)local_d0;
        local_e0 = (short)local_d4;
        local_e4 = local_5a;
      }
      FUN__text__004079c0(local_d0 & 0xffff,local_d4 & 0xffff);
    }
    sVar3 = local_f4 + param_10 + (short)_local_bc;
    local_f4 = sVar3;
    if ((((int)((param_5 & 0xffff) - ((local_a0 & 0xffff) + 1)) % 3 == 0) &&
        (local_f4 = sVar3 + param_10 + param_11, local_104 = sVar3, (local_fc & 0xffff) == 0)) &&
       ((local_e8 & 0xffff) == 0)) {
      FUN__text__004d29e0(0xd,7,1,param_6,sVar3,local_100,0x291,param_4 + 0x7b,6,6,100,100,0xff,0x80
                          ,0x80,0x80);
    }
    local_a0 = CONCAT22(local_a0._2_2_,(short)local_a0 + 1);
  }
  local_114 = param_13;
  if (param_13 == '\x01') {
    local_108 = local_dc - (param_10 + 10);
    iVar1 = local_e0 + -5 + (int)local_e4 / 2;
    local_10c = (undefined2)iVar1;
    FUN__text__004d29e0(0xd,7,1,param_6,CONCAT22((short)((uint)iVar1 >> 0x10),local_108),
                        CONCAT22(local_e0 >> 0xf,local_10c),0x29d,param_4 + 0x74,10,10,100,100,0xff,
                        0x80,0x80,0x80);
  }
  local_8 = 0xffffffff;
  FUN__text__00407710();
  ExceptionList = local_10;
  local_8 = 0x4b7d98;
  FUN__text__0056ce80();
  return;
}

