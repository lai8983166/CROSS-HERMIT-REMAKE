
void __thiscall
FUN__text__004d1cf0(undefined4 param_1,int param_2,short param_3,undefined2 param_4,uint param_5,
                   undefined2 param_6,uint param_7,byte param_8)

{
  int iVar1;
  ushort uVar2;
  undefined4 *puVar3;
  undefined4 local_6c [16];
  uint local_2c;
  uint local_28;
  uint local_24;
  ushort local_20;
  undefined2 uStack_1e;
  undefined2 local_1c;
  short local_18;
  undefined2 local_14;
  short local_10;
  uint local_c;
  undefined4 local_8;
  
  puVar3 = local_6c;
  for (iVar1 = 0x1a; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = CONCAT22(local_c._2_2_,(ushort)param_8);
  local_2c = local_2c & 0xffff0000;
  local_8 = param_1;
  while ((local_2c & 0xffff) != (param_5 & 0xffff)) {
    if ((local_2c & 0xffff) + 1 == (param_5 & 0xffff)) {
      local_c = local_c & 0xffff0000;
      uVar2 = (ushort)param_7;
    }
    else {
      local_24 = 1;
      local_28 = local_28 & 0xffff0000;
      while ((int)(local_28 & 0xffff) < (int)(((param_5 & 0xffff) - 1) - (local_2c & 0xffff))) {
        local_24 = local_24 * 10;
        local_28 = CONCAT22(local_28._2_2_,(short)local_28 + 1);
      }
      uVar2 = (ushort)(param_7 / local_24);
    }
    uVar2 = uVar2 % 10;
    _local_20 = CONCAT22(uStack_1e,uVar2);
    if (uVar2 != 0) {
      local_c = local_c & 0xffff0000;
    }
    if ((local_c & 0xffff) == 0) {
      local_10 = *(short *)(param_2 + 4) + *(short *)(param_2 + 8) * uVar2;
      local_14 = *(undefined2 *)(param_2 + 6);
      local_18 = param_3 + *(short *)(param_2 + 0xc) * (short)local_2c;
      local_1c = param_4;
      FUN__text__004d28c0(param_2,1,param_6,local_18,param_4,local_10,local_14,
                          *(undefined2 *)(param_2 + 8),*(undefined2 *)(param_2 + 10),0xff);
    }
    local_2c = CONCAT22(local_2c._2_2_,(short)local_2c + 1);
  }
  local_8 = 0x4d1ead;
  FUN__text__0056ce80();
  return;
}

