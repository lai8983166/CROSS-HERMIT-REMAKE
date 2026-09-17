
/* WARNING: Removing unreachable block (ram,0x004a5e44) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN__text__004a5ce0(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  short local_14;
  short local_10;
  uint local_c;
  undefined4 local_8;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_10 = DAT_007aab18;
  FUN__text__004a5a60();
  FUN__text__004a8b50(0xffffffff);
  FUN__text__004a1c70();
  FUN__text__004a5f40();
  if (DAT_007a55fa != 0) {
    local_c = local_c & 0xffff0000;
    while ((local_c & 0xffff) < 5) {
      if (*(short *)(&DAT_007aaa12 + (local_c & 0xffff) * 0x1c) == -1) {
        (&DAT_007aaa15)[(local_c & 0xffff) * 0x1c] = 1;
      }
      else {
        (&DAT_007aaa15)[(local_c & 0xffff) * 0x1c] = 0;
      }
      local_c = CONCAT22(local_c._2_2_,(ushort)local_c + 1);
    }
  }
  if ((DAT_007aab0a != 0) && (DAT_007a55fa == 0)) {
    DAT_007aab0a = 0;
    local_14 = local_10;
    local_c = local_c & 0xffff0000;
    while ((local_c & 0xffff) < (uint)*(ushort *)(&DAT_007d62fa + local_10 * 2)) {
      if ((uint)DAT_007aab16 ==
          (int)*(short *)(&DAT_007d599e + (local_c & 0xffff) * 10 + local_10 * 800)) {
        DAT_007aab0a = 1;
        _DAT_007aab0c = (ushort)local_c & 1;
        _DAT_007aab0e = (undefined2)((local_c & 0xffff) / 2);
        DAT_007aab10 = *(undefined2 *)(&DAT_007d599a + (local_c & 0xffff) * 10 + local_10 * 800);
        DAT_007aab12 = *(undefined2 *)(&DAT_007d599c + (local_c & 0xffff) * 10 + local_10 * 800);
        DAT_007aab16 = *(ushort *)(&DAT_007d599e + (local_c & 0xffff) * 10 + local_10 * 800);
        DAT_007aab18 = local_10;
        DAT_007aab14 = (ushort)local_c;
        break;
      }
      local_c = CONCAT22(local_c._2_2_,(ushort)local_c + 1);
    }
  }
  if (DAT_007e11a0 == 0) {
    FUN__text__004db010((int)DAT_007a55f6);
  }
  FUN__text__004a8bf0(0,1);
  FUN__text__004a8bf0(0,0);
  local_8 = 0x4a5f38;
  FUN__text__0056ce80();
  return;
}

