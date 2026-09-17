
void FUN__text__00434770(void)

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
  local_c = FUN__text__00431dd0(&DAT_005ff7b8);
  local_10 = FUN__text__00431dd0(&DAT_005ff7c4);
  if (local_c < 4) {
    if (*(int *)(local_8 + 0x2e6f4) == 0) {
      FUN__text__00454ab0(0xb);
    }
    else {
      iVar1 = FUN__text__00430df0();
      if (iVar1 != 0) {
        FUN__text__00454ab0(0xe);
      }
    }
  }
  else if (local_10 < 6) {
    FUN__text__00454ab0(8);
  }
  else {
    iVar1 = FUN__text__00430ba0();
    if (iVar1 == 0) {
      FUN__text__00454ab0(5);
    }
    else {
      FUN__text__00454ab0(2);
    }
  }
  local_8 = 0x43484c;
  FUN__text__0056ce80();
  return;
}

