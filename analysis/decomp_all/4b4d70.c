
void FUN__text__004b4d70(undefined2 param_1,undefined2 param_2,undefined2 param_3,undefined2 param_4
                        ,uint param_5,undefined2 param_6)

{
  uint uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_68 [16];
  uint local_28;
  undefined4 local_24;
  undefined2 local_20;
  undefined2 local_1c;
  undefined4 local_18;
  undefined4 local_14;
  undefined4 local_10;
  undefined *local_c;
  undefined4 local_8;
  
  puVar3 = local_68;
  for (iVar2 = 0x19; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  uVar1 = local_10 >> 0x10;
  local_10 = local_10 & 0xffff0000;
  local_14 = CONCAT22(local_14._2_2_,param_3);
  local_18 = CONCAT22(local_18._2_2_,param_4);
  local_1c = 0xff;
  local_20 = 0x80;
  local_24 = 1;
  local_28 = param_5 & 0xffff;
  switch(local_28) {
  case 0:
    local_10 = CONCAT22((short)uVar1,1);
    break;
  case 2:
    local_c = &DAT_0061bbd0;
    local_1c = 0x60;
    local_20 = 0x80;
    break;
  case 3:
  case 7:
    local_c = &DAT_0061bbd0;
    break;
  case 4:
    local_c = &DAT_0061bbe0;
    local_1c = 0x60;
    local_20 = 0x80;
    break;
  case 5:
    local_c = &DAT_0061bbe0;
    break;
  case 6:
    local_c = &DAT_0061bbd0;
    local_1c = 0xc0;
    local_20 = 0xb0;
    local_24 = 2;
    break;
  case 8:
    local_c = &DAT_0061bbc0;
    local_14 = (uint)local_14._2_2_ << 0x10;
    local_18 = (uint)local_18._2_2_ << 0x10;
  }
  if ((local_10 & 0xffff) == 0) {
    FUN__text__004d2f10(0xd,param_6,*(undefined2 *)(local_c + 2),param_1,param_2,
                        (uint)*(ushort *)(local_c + 4) +
                        (local_14 & 0xffff) * (uint)*(ushort *)(local_c + 8),
                        (uint)*(ushort *)(local_c + 6) +
                        (local_18 & 0xffff) * (uint)*(ushort *)(local_c + 10),
                        *(undefined2 *)(local_c + 8),*(undefined2 *)(local_c + 10),local_1c,local_20
                        ,local_20,local_20,local_24);
  }
  local_8 = 0x4b4f10;
  FUN__text__0056ce80();
  return;
}

