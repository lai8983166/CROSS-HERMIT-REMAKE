
/* WARNING: Removing unreachable block (ram,0x004a2c2a) */

void __fastcall FUN__text__004a2ba0(undefined4 param_1)

{
  uint uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_60 [16];
  undefined4 local_20;
  short local_1c;
  short local_18;
  undefined2 local_14;
  undefined2 uStack_12;
  uint local_10;
  uint local_c;
  undefined4 local_8;
  
  puVar3 = local_60;
  for (iVar2 = 0x17; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_14 = 1;
  local_18 = 0;
  local_1c = DAT_007a528e * 6 + DAT_007a5290;
  local_c = CONCAT22(local_c._2_2_,1);
  local_8 = param_1;
  while ((local_c & 0xffff) < 0x65) {
    if ((&DAT_007a5b64)[local_c & 0xffff] == '\0') {
      local_14 = 1;
      local_18 = (ushort)(byte)(&DAT_0074bed2)[(local_c & 0xffff) * 0x60] * 6 +
                 (ushort)(byte)(&DAT_0074bed3)[(local_c & 0xffff) * 0x60];
      if (local_18 <= local_1c) {
        uVar1 = local_20 >> 0x10;
        local_20 = local_20 & 0xffff0000;
        if (*(short *)(&DAT_0074bed6 + (local_c & 0xffff) * 0x60) == 0) {
          local_20 = CONCAT22((short)uVar1,1);
        }
        if (*(short *)(&DAT_0074bed8 + (local_c & 0xffff) * 0x60) == 0) {
          local_20 = CONCAT22(local_20._2_2_,1);
        }
        if ((local_20 & 0xffff) == 0) {
          local_10 = local_10 & 0xffff0000;
          while ((local_10 & 0xffff) < 0x14) {
            iVar2 = (local_c & 0xffff) * 0x60;
            if ((&DAT_0074bf0a)[(local_10 & 0xffff) + iVar2] != '\0') {
              FUN__text__004a24a0(local_10 & 0xffff,
                                  CONCAT22((short)((uint)iVar2 >> 0x10),(short)local_c));
            }
            local_10 = CONCAT22(local_10._2_2_,(short)local_10 + 1);
          }
          (&DAT_007a5b64)[local_c & 0xffff] = 1;
        }
      }
    }
    local_c = CONCAT22(local_c._2_2_,(short)local_c + 1);
  }
  local_8 = 0x4a2d50;
  FUN__text__0056ce80();
  return;
}

