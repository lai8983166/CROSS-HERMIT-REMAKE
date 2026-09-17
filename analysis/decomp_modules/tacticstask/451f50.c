
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN__text__00451f50(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  iVar1 = FUN__text__00467e70();
  local_c = (int)(char)(&DAT_007f44bb)[iVar1 % 3];
  FUN__text__004db010(local_c);
  if (DAT_007f44b8 != '\0') {
    iVar1 = FUN__text__00456b20();
    if (iVar1 == 0) {
      for (local_10 = 0; local_10 != DAT_007f448c._1_1_; local_10 = local_10 + 1) {
        (&DAT_007f45bc)[local_10 * 0xb0] = DAT_007f4490;
        (&DAT_007f4548)[local_10 * 0xb0] = (&DAT_0060c8f8)[(byte)(&DAT_007f4548)[local_10 * 0xb0]];
      }
      DAT_007f448c._2_1_ = 0;
      _DAT_007f4508 = 0;
    }
  }
  *(undefined4 *)(local_8 + 0x174) = 0xffffffff;
  local_8 = 0x452038;
  FUN__text__0056ce80();
  return;
}

