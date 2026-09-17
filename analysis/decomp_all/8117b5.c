
bool FUN__text1__008117b5(uint param_1,char param_2)

{
  uint local_8;
  
  for (local_8 = 1 << (param_2 - 1U & 0x1f); local_8 != 0; local_8 = (int)local_8 >> 1) {
    if ((param_1 & local_8) != 0) {
      DAT_0087444c = DAT_0087444c | DAT_00874440;
    }
    DAT_00874440 = DAT_00874440 >> 1;
    if (DAT_00874440 == 0) {
      if (DAT_00874438 < DAT_0087442c) {
        *DAT_00874438 = DAT_0087444c;
        DAT_00874438 = DAT_00874438 + 1;
      }
      if (DAT_0087442c <= DAT_00874438) {
        DAT_00874430 = '\x01';
      }
      DAT_0087444c = 0;
      DAT_00874440 = 0x80;
    }
  }
  return DAT_00874430 == '\0';
}

