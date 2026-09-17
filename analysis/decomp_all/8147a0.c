
uint FUN__text1__008147a0(uint param_1,int param_2)

{
  if (param_2 < 0) {
    param_2 = param_2 + 0x20;
  }
  return param_1 >> ((byte)param_2 & 0x1f) | param_1 << (0x20 - (byte)param_2 & 0x1f);
}

