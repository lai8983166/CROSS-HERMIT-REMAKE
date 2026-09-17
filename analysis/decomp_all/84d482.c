
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined4 FUN__text1__0084d482(uint param_1)

{
  if ((param_1 < DAT_00876c60) &&
     ((*(byte *)((&DAT_00876b60)[(int)param_1 >> 5] + 4 + (param_1 & 0x1f) * 8) & 1) != 0)) {
    return *(undefined4 *)((&DAT_00876b60)[(int)param_1 >> 5] + (param_1 & 0x1f) * 8);
  }
  _DAT_00875650 = 0;
  _DAT_0087564c = 9;
  return 0xffffffff;
}

