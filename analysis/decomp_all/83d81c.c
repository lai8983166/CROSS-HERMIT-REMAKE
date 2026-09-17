
int FUN__text1__0083d81c(uint param_1,char param_2)

{
  int iVar1;
  int local_c;
  int local_8;
  
  local_c = 0;
  local_8 = DAT_0087542c;
  iVar1 = local_8;
  while (local_8 = iVar1, local_c < local_8) {
    iVar1 = local_c + (local_8 - local_c) / 2;
    if (**(uint **)(DAT_008752c0 + iVar1 * 4) < param_1) {
      local_c = iVar1 + 1;
      iVar1 = local_8;
    }
  }
  if ((local_c < DAT_0087542c) && (param_1 == **(uint **)(DAT_008752c0 + local_c * 4))) {
    if (param_2 != '\0') {
      local_c = -1;
    }
  }
  else if (param_2 == '\0') {
    local_c = -1;
  }
  return local_c;
}

