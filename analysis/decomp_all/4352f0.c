
void FUN__text__004352f0(void)

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
  iVar1 = FUN__text__004307b0();
  if (iVar1 == 0) {
    if (*(int *)(local_8 + 0x2e6f4) == 0) {
      local_c = FUN__text__00431dd0(&DAT_005ff838);
      if (local_c == 1) {
        iVar1 = FUN__text__00430ba0();
        if (iVar1 == 0) {
          FUN__text__00454ab0(6);
        }
        else {
          FUN__text__00454ab0(3);
        }
      }
      else {
        FUN__text__00454ab0(0xb);
      }
    }
    else {
      iVar1 = FUN__text__00430df0();
      if (iVar1 != 0) {
        FUN__text__00454ab0(0xe);
      }
    }
  }
  else if (*(int *)(local_8 + 0x2e6f8) < 0x4651) {
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
  local_8 = 0x435404;
  FUN__text__0056ce80();
  return;
}

