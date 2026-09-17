
void __fastcall FUN__text__004b52f0(int param_1)

{
  ushort uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_7c [16];
  short local_3c;
  undefined2 local_38;
  ushort local_34;
  undefined2 uStack_32;
  undefined2 local_30;
  uint local_2c;
  undefined *local_28;
  undefined *local_24;
  undefined1 *local_20;
  undefined1 local_1c [4];
  uint local_18;
  uint local_10;
  uint local_c;
  int local_8;
  
  puVar3 = local_7c;
  for (iVar2 = 0x1e; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_24 = &DAT_006b2d88 + (uint)*(ushort *)(param_1 + 0x632) * 0x40;
  local_28 = &DAT_007e17e8 + *(short *)(param_1 + 0x596 + DAT_007d6a34 * 2) * 0x4a0;
  local_2c = CONCAT22(local_2c._2_2_,(short)*(char *)(param_1 + 0x582));
  local_30 = 1;
  *(undefined1 *)(param_1 + 0xc87) = 0;
  if (DAT_007d6a36 == 3) {
    *(char *)(param_1 + 0xc87) = *(char *)(param_1 + 0xc87) + '\x01';
  }
  local_c = local_c & 0xffff0000;
  local_8 = param_1;
  while ((local_c & 0xffff) < (local_2c & 0xffff)) {
    uVar1 = *(ushort *)(local_28 + (local_c & 0xffff) * 2 + 0x52);
    _local_34 = CONCAT22(uStack_32,uVar1);
    if (uVar1 != 0) {
      *(char *)(local_8 + 0xc87) = *(char *)(local_8 + 0xc87) + '\x01';
      local_38 = (undefined2)((byte)(&DAT_006c2dcc)[(uint)uVar1 * 0x48] - 1);
      local_3c = (byte)(&DAT_006c2dcf)[(uint)uVar1 * 0x48] - 1;
      FUN__text__004b4d70((local_c & 0xffff) * 0x24 + 0x16e,0x1be,
                          CONCAT22((short)((uint)uVar1 * 0x48 >> 0x10),local_38),
                          CONCAT22((short)((byte)(&DAT_006c2dcc)[(uint)uVar1 * 0x48] - 1 >> 0x10),
                                   local_3c),7,0x40);
      if ((((DAT_007d6a36 == 1) && (DAT_007d6a32 == '\0')) && (DAT_007d6a31 == '\0')) &&
         (FUN__text__004b10b0(local_1c,local_c & 0xffff), (local_10 & 0xffff) != 0)) {
        local_20 = &DAT_0061bc10;
        FUN__text__004d2ca0(0xd,0x35,DAT_0061bc12,(local_c & 0xffff) * 0x24 + 0x16e,0x1be,
                            DAT_0061bc14,DAT_0061bc16,DAT_0061bc18,DAT_0061bc1a);
        DAT_007d6a30 = 1;
        if ((local_18 & 1) != 0) {
          FUN__text__004db2b0(5);
          DAT_007d6a46 = local_38;
          DAT_007d6a48 = local_3c;
          DAT_007d6a44 = (short)local_c;
          DAT_007d6a36 = 3;
          DAT_007d6a3c = *(undefined2 *)(local_28 + (local_c & 0xffff) * 2 + 0x52);
          *(undefined2 *)(local_28 + (local_c & 0xffff) * 2 + 0x52) = 0;
        }
      }
    }
    local_c = CONCAT22(local_c._2_2_,(short)local_c + 1);
  }
  local_8 = 0x4b559c;
  FUN__text__0056ce80();
  return;
}

