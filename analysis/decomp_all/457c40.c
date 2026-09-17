
void FUN__text__00457c40(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  undefined4 local_10;
  undefined4 local_c;
  int local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  FUN__text__00457d00();
  FUN__text__00458280();
  FUN__text__00425620(0x1cc,0x2cd,0x13a,10,0xc4);
  iVar1 = FUN__text__004577f0();
  if (iVar1 != 0) {
    local_c = 0x1cc;
    local_10 = 0x2b9;
    FUN__text__00426820(DAT_007a49fc,0x1cc,0x2b9,10,0,local_8 + 0x117f28,local_8 + 0x117fb4,0xc4);
  }
  local_8 = 0x457cf6;
  FUN__text__0056ce80();
  return;
}

