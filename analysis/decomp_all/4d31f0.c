
void __fastcall FUN__text__004d31f0(undefined4 param_1)

{
  short sVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_5c [16];
  uint local_1c;
  short local_18;
  short local_14;
  ushort local_10;
  short local_c;
  undefined4 local_8;
  
  puVar3 = local_5c;
  for (iVar2 = 0x16; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  for (local_c = 0; local_c < 0x168; local_c = local_c + 1) {
    if ((((*(ushort *)(&DAT_007aacac + local_c * 2) & 1) == 1) &&
        (local_1c = (uint)(*(ushort *)(&DAT_007aacac + local_c * 2) >> 8 & 0xf), 2 < local_1c)) &&
       (local_1c < 5)) {
      local_10 = *(ushort *)(&DAT_007aacac + local_c * 2) >> 1 & 0x7f;
      sVar1 = FUN__text__004d46e0(local_10);
      if (sVar1 == 0) {
        *(ushort *)(&DAT_007aacac + local_c * 2) =
             *(ushort *)(&DAT_007aacac + local_c * 2) & 0xf0ff | 0x100;
      }
      else {
        local_14 = 1;
        for (local_18 = 0; local_18 < 8; local_18 = local_18 + 1) {
          if ((int)*(short *)(&DAT_007e184a + local_18 * 2 + (short)local_10 * 0x4a0) == local_c + 1
             ) {
            local_14 = 0;
            *(ushort *)(&DAT_007aacac + local_c * 2) =
                 *(ushort *)(&DAT_007aacac + local_c * 2) & 0xff01 | (local_10 & 0x7f) << 1;
          }
        }
        if (local_14 != 0) {
          *(ushort *)(&DAT_007aacac + local_c * 2) =
               *(ushort *)(&DAT_007aacac + local_c * 2) & 0xf0ff | 0x100;
        }
      }
    }
  }
  local_8 = 0x4d3396;
  FUN__text__0056ce80();
  return;
}

