
void FUN__text__00433040(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  int local_c;
  int local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  iVar1 = FUN__text__004e2720(3,0);
  if (iVar1 == 0) {
    if (*(int *)(local_8 + 0x2e6f4) == 0) {
      FUN__text__00454af0(0xb,0xe);
    }
    else {
      iVar1 = FUN__text__00430df0();
      if (iVar1 != 0) {
        FUN__text__00454af0(0xe,0xe);
      }
    }
  }
  else {
    local_c = FUN__text__00431dd0(&DAT_005ff758);
    if (local_c == 3) {
      iVar1 = FUN__text__00430ba0();
      if (iVar1 == 0) {
        FUN__text__00454af0(5,5);
      }
      else {
        FUN__text__00454af0(2,5);
      }
    }
    else {
      FUN__text__00454af0(8,5);
    }
  }
  local_8 = 0x433120;
  FUN__text__0056ce80();
  return;
}

