
void FUN__text__00435080(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  int local_10;
  undefined4 local_c;
  int local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_10 = FUN__text__00431dd0(&DAT_005ff804);
  local_c = FUN__text__00431d40(6);
  iVar1 = FUN__text__00469170(local_c);
  if (iVar1 == 0) {
    iVar1 = FUN__text__00430df0();
    if (iVar1 != 0) {
      if (*(int *)(local_8 + 0x2e6f8) < 36000) {
        FUN__text__00454ab0(0xe);
      }
      else {
        FUN__text__00454ab0(0xb);
      }
    }
  }
  else if ((local_10 == 5) && (local_10 = FUN__text__00432040(&DAT_005ff804), local_10 == 0)) {
    iVar1 = FUN__text__00430ba0();
    if (iVar1 == 0) {
      FUN__text__00454ab0(5);
    }
    else {
      FUN__text__00454ab0(2);
    }
  }
  else {
    FUN__text__00454ab0(8);
  }
  local_8 = 0x435183;
  FUN__text__0056ce80();
  return;
}

