
uint FUN__text__00580830(uint param_1)

{
  uint local_c;
  uint local_8;
  
  if (DAT_00764370 < 2) {
    local_8 = *(ushort *)(PTR_DAT_00764164 + param_1 * 2) & 4;
  }
  else {
    local_8 = FUN__text__0057bb50(param_1,4);
  }
  if (local_8 == 0) {
    local_c = (param_1 & 0xffffffdf) - 7;
  }
  else {
    local_c = param_1;
  }
  return local_c;
}

