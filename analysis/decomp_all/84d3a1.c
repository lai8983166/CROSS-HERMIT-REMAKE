
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN__text1__0084d3a1(uint param_1)

{
  uint *puVar1;
  int iVar2;
  
  iVar2 = 0;
  _DAT_00875650 = param_1;
  puVar1 = &DAT_00872a90;
  do {
    if (param_1 == *puVar1) {
      _DAT_0087564c = *(undefined4 *)(&UNK_00872a94 + iVar2 * 8);
      return;
    }
    puVar1 = puVar1 + 2;
    iVar2 = iVar2 + 1;
  } while ((int)puVar1 < 0x872bf8);
  if ((0x12 < param_1) && (param_1 < 0x25)) {
    _DAT_0087564c = 0xd;
    return;
  }
  if ((param_1 < 0xbc) || (_DAT_0087564c = 8, 0xca < param_1)) {
    _DAT_0087564c = 0x16;
  }
  return;
}

