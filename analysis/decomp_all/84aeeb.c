
uint FUN__text1__0084aeeb(int param_1)

{
  uint uVar1;
  
  uVar1 = DAT_00876b38;
  while( true ) {
    if (DAT_00876b38 + DAT_00876b34 * 0x14 <= uVar1) {
      return 0;
    }
    if ((uint)(param_1 - *(int *)(uVar1 + 0xc)) < 0x100000) break;
    uVar1 = uVar1 + 0x14;
  }
  return uVar1;
}

