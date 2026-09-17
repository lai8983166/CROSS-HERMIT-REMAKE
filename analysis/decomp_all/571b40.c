
undefined4 FUN__text__00571b40(int param_1)

{
  undefined4 local_c;
  uint local_8;
  
  if (DAT_00764370 < 2) {
    local_8 = *(ushort *)(PTR_DAT_00764164 + param_1 * 2) & 0x107;
  }
  else {
    local_8 = FUN__text__0057bb50(param_1,0x107);
  }
  if ((local_8 == 0) && (param_1 != 0x5f)) {
    local_c = 0;
  }
  else {
    local_c = 1;
  }
  return local_c;
}

