
uint FUN__text1__00811bf4(int param_1)

{
  int iVar1;
  uint local_c;
  int local_8;
  
  local_c = 0;
  local_8 = param_1;
  while (iVar1 = local_8 + -1, local_8 != 0) {
    local_c = local_c << 1;
    if ((DAT_0087444c & DAT_00874440) != 0) {
      local_c = local_c | 1;
    }
    DAT_00874440 = DAT_00874440 >> 1;
    local_8 = iVar1;
    if (DAT_00874440 == 0) {
      if (DAT_00874438 < DAT_0087442c) {
        DAT_0087444c = *DAT_00874438;
        DAT_00874438 = DAT_00874438 + 1;
      }
      else {
        DAT_00874430 = 1;
        DAT_0087444c = 0;
      }
      DAT_00874440 = 0x80;
    }
  }
  return local_c;
}

