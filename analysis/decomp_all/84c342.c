
byte FUN__text1__0084c342(uint param_1)

{
  if (DAT_00876c60 <= param_1) {
    return 0;
  }
  return *(byte *)((&DAT_00876b60)[(int)param_1 >> 5] + 4 + (param_1 & 0x1f) * 8) & 0x40;
}

