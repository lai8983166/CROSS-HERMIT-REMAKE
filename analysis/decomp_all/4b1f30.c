
void __fastcall FUN__text__004b1f30(int param_1)

{
  ushort uVar1;
  int iVar2;
  undefined2 extraout_var;
  undefined2 extraout_var_00;
  undefined4 *puVar3;
  undefined4 local_74 [16];
  short local_34;
  undefined2 local_30;
  uint local_2c;
  undefined2 local_28;
  undefined2 local_24;
  undefined2 local_20;
  uint local_1c;
  undefined *local_18;
  undefined *local_14;
  ushort local_10;
  undefined2 uStack_e;
  uint local_c;
  int local_8;
  
  puVar3 = local_74;
  for (iVar2 = 0x1c; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  uVar1 = *(ushort *)(param_1 + 0x596 + DAT_007d6a34 * 2);
  _local_10 = CONCAT22(uStack_e,uVar1);
  local_14 = &DAT_007e17e8 + (uint)uVar1 * 0x4a0;
  local_18 = &DAT_006b2d88 + (uint)*(ushort *)(param_1 + 0x632) * 0x40;
  local_1c = CONCAT22(local_1c._2_2_,(short)*(char *)(param_1 + 0x582));
  local_20 = 1;
  local_24 = 0;
  local_28 = 0;
  local_c = local_c & 0xffff0000;
  local_8 = param_1;
  while ((local_c & 0xffff) < (local_1c & 0xffff)) {
    uVar1 = *(ushort *)(local_14 + (local_c & 0xffff) * 2 + 0x52);
    local_2c = CONCAT22(local_2c._2_2_,uVar1);
    if (uVar1 != 0) {
      local_30 = (undefined2)((byte)(&DAT_006c2dcc)[(uint)uVar1 * 0x48] - 1);
      local_34 = (byte)(&DAT_006c2dcf)[(uint)uVar1 * 0x48] - 1;
      FUN__text__004b4d70(0x341,(local_c & 0xffff) * 0x26 + 0x46,
                          CONCAT22((short)((uint)uVar1 * 0x48 >> 0x10),local_30),
                          CONCAT22((short)((byte)(&DAT_006c2dcc)[(uint)uVar1 * 0x48] - 1 >> 0x10),
                                   local_34),3,0x40);
      FUN__text__004b4f40(0x365,(local_c & 0xffff) * 0x26 + 0x49,CONCAT22(extraout_var_00,local_30),
                          CONCAT22(extraout_var,local_34),0x40);
      FUN__text__004b7230(0x3ad,(local_c & 0xffff) * 0x26 + 0x59,0,0,3,0x4a,0x3f,
                          (int)*(short *)(&DAT_006c2dd0 + (local_2c & 0xffff) * 0x48),1);
    }
    local_c = CONCAT22(local_c._2_2_,(short)local_c + 1);
  }
  local_8 = 0x4b20f8;
  FUN__text__0056ce80();
  return;
}

