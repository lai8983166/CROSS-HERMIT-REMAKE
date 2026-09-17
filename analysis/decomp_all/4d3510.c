
void FUN__text__004d3510(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  undefined2 local_10;
  short local_c;
  undefined4 local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  DAT_007a5290 = DAT_007a5290 + 1;
  if (5 < DAT_007a5290) {
    DAT_007a528e = DAT_007a528e + 1;
    DAT_007a5290 = 1;
  }
  DAT_007a55fa = 0;
  DAT_007a4e62 = 0;
  for (local_c = 0; local_c < DAT_007a5260; local_c = local_c + 1) {
    local_10 = *(undefined2 *)(&DAT_007a5210 + local_c * 2);
    FUN__text__004d3aa0(CONCAT22(DAT_007a5260 >> 0xf,local_10));
  }
  FUN__text__004d31f0();
  FUN__text__004d34a0();
  DAT_007a55f6 = 0xb;
  DAT_007e11a0 = 0;
  local_8 = 0x4d35f3;
  FUN__text__0056ce80();
  return;
}

