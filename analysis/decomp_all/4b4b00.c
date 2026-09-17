
void __thiscall
FUN__text__004b4b00(int param_1,undefined2 param_2,undefined2 param_3,uint param_4,uint param_5,
                   undefined2 param_6)

{
  ushort uVar1;
  uint uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_70 [16];
  uint local_30;
  uint local_2c;
  ushort local_28;
  undefined2 uStack_26;
  undefined4 local_24;
  undefined4 local_20;
  undefined4 local_1c;
  undefined2 local_18;
  undefined2 local_14;
  undefined4 local_10;
  undefined *local_c;
  int local_8;
  
  puVar4 = local_70;
  for (iVar3 = 0x1b; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  uVar2 = local_10 >> 0x10;
  local_10 = local_10 & 0xffff0000;
  local_14 = 0xff;
  local_18 = 0x80;
  local_1c = 1;
  local_20 = CONCAT22(local_20._2_2_,(short)((ulonglong)(param_4 & 0xffff) % 0xc));
  local_24 = CONCAT22(local_24._2_2_,(short)((ulonglong)(param_4 & 0xffff) / 0xc));
  local_2c = param_5 & 0xffff;
  switch(local_2c) {
  case 0:
    local_10 = CONCAT22((short)uVar2,1);
    break;
  case 1:
    local_c = &DAT_0061bcb0;
    break;
  case 2:
    local_c = &DAT_0061bcc0;
    break;
  case 3:
  case 4:
    local_30 = param_5 & 0xffff;
    if (local_30 == 3) {
      local_c = &DAT_0061bcb0;
    }
    else if (local_30 == 4) {
      local_c = &DAT_0061bcc0;
    }
    uVar1 = *(ushort *)(param_1 + 0x596 + DAT_007d6a34 * 2);
    _local_28 = CONCAT22(uStack_26,uVar1);
    if ((*(ushort *)(&DAT_007aacac + (param_4 & 0xffff) * 2) >> 1 & 0x7f) == uVar1) {
      local_14 = 0xc0;
      local_18 = 0xb0;
      local_1c = 2;
    }
    else {
      local_14 = 0x60;
      local_18 = 0x80;
    }
    break;
  case 5:
    local_c = &DAT_0061bcb0;
    local_14 = 0x60;
    break;
  case 6:
    local_c = &DAT_0061bbc0;
    local_14 = 0xff;
    local_20 = (uint)local_20._2_2_ << 0x10;
    local_24 = (uint)local_24._2_2_ << 0x10;
  }
  if ((local_10 & 0xffff) == 0) {
    local_8 = param_1;
    FUN__text__004d2f10(0xd,param_6,*(undefined2 *)(local_c + 2),param_2,param_3,
                        (local_20 & 0xffff) * (uint)*(ushort *)(local_c + 8) +
                        (uint)*(ushort *)(local_c + 4),
                        (local_24 & 0xffff) * (uint)*(ushort *)(local_c + 10) +
                        (uint)*(ushort *)(local_c + 6),*(undefined2 *)(local_c + 8),
                        *(undefined2 *)(local_c + 10),local_14,local_18,local_18,local_18,local_1c);
  }
  local_8 = 0x4b4d42;
  FUN__text__0056ce80();
  return;
}

