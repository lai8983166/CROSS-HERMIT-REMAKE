
void __fastcall FUN__text__004a9ab0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_d8 [17];
  short local_94;
  uint local_8c;
  uint local_88;
  uint local_80;
  uint local_7c;
  uint local_78;
  ushort auStack_6c [40];
  uint local_1c;
  uint local_18;
  uint local_14;
  undefined4 local_10;
  uint local_c;
  int local_8;
  
  puVar2 = local_d8;
  for (iVar1 = 0x35; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  local_c = local_c & 0xffff0000;
  while ((int)(local_c & 0xffff) < (int)DAT_007a5260) {
    local_78 = (uint)*(ushort *)(&DAT_007a5210 + (local_c & 0xffff) * 2);
    auStack_6c[local_c & 0xffff] = 0;
    local_10 = (uint)local_10._2_2_ << 0x10;
    while ((local_10 & 0xffff) < 7) {
      auStack_6c[local_c & 0xffff] =
           auStack_6c[local_c & 0xffff] +
           (ushort)(byte)(&DAT_007e17f4)[(local_10 & 0xffff) * 8 + local_78 * 0x4a0];
      local_10 = CONCAT22(local_10._2_2_,(short)local_10 + 1);
    }
    local_c = CONCAT22(local_c._2_2_,(short)local_c + 1);
  }
  local_14 = local_14 & 0xffff0000;
  while ((int)(local_14 & 0xffff) < (int)DAT_007a5260) {
    local_7c = (uint)*(ushort *)(&DAT_007a5210 + (local_14 & 0xffff) * 2);
    local_18 = local_18 & 0xffff0000;
    while ((local_18 & 0xffff) < 8) {
      local_94 = 1;
      local_1c = local_1c & 0xffff0000;
      while ((int)(local_1c & 0xffff) < (int)DAT_007a5260) {
        if ((local_14 & 0xffff) != (local_1c & 0xffff)) {
          local_88 = (uint)*(ushort *)(&DAT_007a5210 + (local_1c & 0xffff) * 2);
          if ((local_18 & 0xffff) < 7) {
            local_80 = (uint)(byte)(&DAT_007e17f4)[(local_18 & 0xffff) * 8 + local_7c * 0x4a0];
            local_8c = (uint)(byte)(&DAT_007e17f4)[(local_18 & 0xffff) * 8 + local_88 * 0x4a0];
          }
          else if ((local_18 & 0xffff) == 7) {
            local_80 = (uint)auStack_6c[local_14 & 0xffff];
            local_8c = (uint)auStack_6c[local_1c & 0xffff];
          }
          if ((local_80 & 0xffff) < (local_8c & 0xffff)) {
            local_94 = local_94 + 1;
          }
        }
        local_1c = CONCAT22(local_1c._2_2_,(short)local_1c + 1);
      }
      *(short *)(local_8 + 0x76ca + (local_14 & 0xffff) * 0x10 + (local_18 & 0xffff) * 2) = local_94
      ;
      local_18 = CONCAT22(local_18._2_2_,(short)local_18 + 1);
    }
    local_14 = CONCAT22(local_14._2_2_,(short)local_14 + 1);
  }
  return;
}

