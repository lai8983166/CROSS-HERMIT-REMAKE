
void __fastcall FUN__text__004b5050(int param_1)

{
  int iVar1;
  ushort uVar2;
  undefined4 *puVar3;
  undefined4 local_78 [16];
  undefined2 local_38;
  uint local_34;
  uint local_30;
  short local_2c;
  undefined2 uStack_2a;
  undefined *local_28;
  undefined *local_24;
  undefined1 *local_20;
  undefined1 local_1c [4];
  uint local_18;
  uint local_10;
  uint local_c;
  int local_8;
  
  puVar3 = local_78;
  for (iVar1 = 0x1d; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_24 = &DAT_006b2d88 + (uint)*(ushort *)(param_1 + 0x632) * 0x40;
  local_28 = &DAT_007e17e8 + *(short *)(param_1 + 0x596 + DAT_007d6a34 * 2) * 0x4a0;
  _local_2c = CONCAT22(uStack_2a,(short)*(char *)(param_1 + 0x582));
  local_30 = CONCAT22(local_30._2_2_,(short)*(char *)(param_1 + 0x570));
  local_34 = local_34 & 0xffff0000;
  local_38 = 1;
  *(undefined1 *)(param_1 + 0xc86) = 0;
  if (DAT_007d6a50 == 3) {
    *(char *)(param_1 + 0xc86) = *(char *)(param_1 + 0xc86) + '\x01';
  }
  local_c = local_c & 0xffff0000;
  local_8 = param_1;
  while ((local_c & 0xffff) < (local_30 & 0xffff)) {
    uVar2 = (short)_local_2c + (short)local_c;
    local_34 = CONCAT22(local_34._2_2_,uVar2);
    if (*(short *)(local_28 + (local_c & 0xffff) * 2 + 0x62) != 0) {
      *(char *)(local_8 + 0xc86) = *(char *)(local_8 + 0xc86) + '\x01';
      FUN__text__004b4b00((uint)uVar2 * 0x24 + 0x16e,0x1be,
                          *(short *)(local_28 + (local_c & 0xffff) * 2 + 0x62) + -1,1,0x3f);
      if ((((DAT_007d6a50 == 1) && (DAT_007d6a32 == '\x01')) && (DAT_007d6a31 == '\0')) &&
         (FUN__text__004b10b0(local_1c,local_34 & 0xffff), (local_10 & 0xffff) != 0)) {
        local_20 = &DAT_0061bc10;
        FUN__text__004d2ca0(0xd,0x35,DAT_0061bc12,(local_34 & 0xffff) * 0x24 + 0x16e,0x1be,
                            DAT_0061bc14,DAT_0061bc16,DAT_0061bc18,DAT_0061bc1a);
        DAT_007d6a30 = 1;
        if ((local_18 & 1) != 0) {
          FUN__text__004db2b0(5);
          DAT_007d6a5e = (short)local_c;
          DAT_007d6a60 = (undefined2)local_34;
          DAT_007d6a50 = 3;
          DAT_007d6a56 = *(undefined2 *)(local_28 + (local_c & 0xffff) * 2 + 0x62);
          *(undefined2 *)(local_28 + (local_c & 0xffff) * 2 + 0x62) = 0;
        }
      }
    }
    local_c = CONCAT22(local_c._2_2_,(short)local_c + 1);
  }
  local_8 = 0x4b52e6;
  FUN__text__0056ce80();
  return;
}

