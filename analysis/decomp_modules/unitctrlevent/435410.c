
void FUN__text__00435410(void)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  int local_c;
  undefined4 local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  iVar2 = FUN__text__004e2760(3,0,0);
  if (iVar2 != 0) {
    uVar1 = FUN__text__00431d40(0x38);
    iVar2 = FUN__text__00469170(uVar1);
    if (iVar2 != 0) {
      uVar1 = FUN__text__00431d40(0x39);
      iVar2 = FUN__text__00469170(uVar1);
      if (iVar2 == 0) {
        FUN__text__004e29a0(1,0,0x39);
      }
      else {
        FUN__text__004e29a0(1,0,0x38);
      }
      FUN__text__004e29a0(3,0,1);
    }
  }
  uVar1 = FUN__text__00431d40(0x38);
  iVar2 = FUN__text__00469170(uVar1);
  if (iVar2 != 0) {
    uVar1 = FUN__text__00431d40(0x39);
    iVar2 = FUN__text__00469170(uVar1);
    if (iVar2 != 0) {
      local_c = FUN__text__00431dd0(&DAT_005ff83c);
      if (local_c == 5) {
        iVar2 = FUN__text__00430ba0();
        if (iVar2 == 0) {
          FUN__text__00454ab0(5);
        }
        else {
          FUN__text__00454ab0(2);
        }
      }
      else {
        FUN__text__00454ab0(8);
      }
      goto LAB__text__00435585;
    }
  }
  uVar1 = FUN__text__00431d40(9);
  iVar2 = FUN__text__00469170(uVar1);
  if (iVar2 == 0) {
    uVar1 = FUN__text__00431d40(10);
    iVar2 = FUN__text__00469170(uVar1);
    if (iVar2 == 0) {
      iVar2 = FUN__text__00430df0();
      if (iVar2 != 0) {
        FUN__text__00454ab0(0xe);
      }
      goto LAB__text__00435585;
    }
  }
  FUN__text__00454ab0(0xb);
LAB__text__00435585:
  local_8 = 0x435592;
  FUN__text__0056ce80();
  return;
}

