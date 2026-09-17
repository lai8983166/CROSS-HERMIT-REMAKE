
void FUN__text__004b7230(short param_1,undefined2 param_2,short param_3,short param_4,uint param_5,
                        undefined2 param_6,uint param_7,uint param_8,byte param_9)

{
  int iVar1;
  ushort uVar2;
  undefined4 *puVar3;
  undefined4 local_fc [16];
  uint local_bc;
  uint local_b8;
  ushort local_b4;
  undefined2 uStack_b2;
  undefined4 local_b0;
  uint local_ac;
  uint local_a8;
  short local_a4;
  short local_a0;
  uint local_9c;
  short local_60;
  short local_5e;
  ushort local_40;
  undefined4 local_3c;
  undefined4 local_38;
  undefined1 local_34;
  undefined1 local_33;
  undefined1 local_32;
  undefined1 local_31;
  undefined2 local_28;
  undefined2 local_26;
  undefined2 local_24;
  undefined2 local_22;
  short local_20;
  short sStack_1e;
  short local_1c;
  short local_1a;
  undefined *local_18;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB__text__005902dc;
  local_10 = ExceptionList;
  iVar1 = 0x3b;
  puVar3 = local_fc;
  while( true ) {
    if (iVar1 == 0) break;
    iVar1 = iVar1 + -1;
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_18 = &DAT_0061bae0 + (param_7 & 0xffff) * 0x10;
  ExceptionList = &local_10;
  FUN__text__004075e0();
  local_8 = 0;
  FUN__text__004077c0(DAT_007a49fc);
  local_40 = local_40 | 0x40;
  local_28 = 100;
  local_26 = 100;
  local_24 = 0;
  local_38 = 0;
  local_3c = 1;
  local_31 = 0xff;
  local_32 = 0x80;
  local_33 = 0x80;
  local_34 = 0x80;
  local_22 = param_6;
  local_9c = CONCAT22(local_9c._2_2_,(ushort)param_9);
  local_b0 = (uint)local_b0._2_2_ << 0x10;
  while ((local_b0 & 0xffff) != (param_5 & 0xffff)) {
    if ((local_b0 & 0xffff) + 1 == (param_5 & 0xffff)) {
      uVar2 = (ushort)((ulonglong)param_8 % 10);
      local_9c = local_9c & 0xffff0000;
    }
    else {
      local_b8 = 1;
      local_bc = local_bc & 0xffff0000;
      while ((int)(local_bc & 0xffff) < (int)(((param_5 & 0xffff) - 1) - (local_b0 & 0xffff))) {
        local_b8 = local_b8 * 10;
        local_bc = CONCAT22(local_bc._2_2_,(short)local_bc + 1);
      }
      uVar2 = (short)(param_8 / local_b8) % 10;
    }
    uVar2 = uVar2 % 10;
    _local_b4 = CONCAT22(uStack_b2,uVar2);
    if (uVar2 != 0) {
      local_9c = local_9c & 0xffff0000;
    }
    if ((local_9c & 0xffff) == 0) {
      local_a0 = param_3 + *(short *)(local_18 + 4) + *(short *)(local_18 + 0xe) * uVar2;
      local_a4 = param_4 + *(short *)(local_18 + 6);
      local_a8 = CONCAT22(local_a8._2_2_,param_1 + *(short *)(local_18 + 0xc) * (short)local_b0);
      local_ac = CONCAT22(local_ac._2_2_,param_2);
      FUN__text__00407870(*local_18,*(undefined2 *)(local_18 + 2));
      local_60 = *(short *)(local_18 + 8);
      local_5e = *(short *)(local_18 + 10);
      local_20 = local_a0;
      sStack_1e = local_a4;
      local_1c = local_a0 + local_60;
      local_1a = local_a4 + local_5e;
      FUN__text__004079c0(local_a8 & 0xffff,local_ac & 0xffff);
    }
    local_b0 = CONCAT22(local_b0._2_2_,(short)local_b0 + 1);
  }
  local_8 = 0xffffffff;
  FUN__text__00407710();
  ExceptionList = local_10;
  local_8 = 0x4b757d;
  FUN__text__0056ce80();
  return;
}

