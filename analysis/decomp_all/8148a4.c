
uint FUN__text1__008148a4(uint param_1,int param_2,byte param_3)

{
  undefined4 local_18;
  undefined4 local_10;
  undefined4 local_c;
  undefined4 local_8;
  
  local_8 = param_1 & ~((1 << ((byte)param_2 & 0x1f)) + -1 << (param_3 & 0x1f));
  local_10 = 1 << (param_3 & 0x1f);
  local_18 = 1 << ((param_3 - 1) + (byte)param_2 & 0x1f);
  for (local_c = 0; local_c < param_2; local_c = local_c + 1) {
    if ((param_1 & local_10) != 0) {
      local_8 = local_8 | local_18;
    }
    local_10 = local_10 << 1;
    local_18 = local_18 >> 1;
  }
  return local_8;
}

