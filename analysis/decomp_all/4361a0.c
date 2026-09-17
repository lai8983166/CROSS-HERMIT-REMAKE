
void FUN__text__004361a0(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  int local_14;
  undefined4 local_10;
  undefined4 local_c;
  undefined4 local_8;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = FUN__text__00431d40(1);
  local_10 = FUN__text__00431d40(2);
  iVar1 = FUN__text__004e2720(3,0);
  if (iVar1 == 0) {
    iVar1 = FUN__text__00469170(local_c);
    if (iVar1 != 0) {
      FUN__text__004e29a0(3,0,1);
      FUN__text__00480040(0,local_10,0xc,0x1b);
    }
  }
  else {
    iVar1 = FUN__text__00469170(local_10);
    if (iVar1 != 0) {
      local_14 = FUN__text__00431dd0(&DAT_005ff8a4);
      if (local_14 == 8) {
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
      goto LAB__text__004362c7;
    }
  }
  iVar1 = FUN__text__00430df0();
  if (iVar1 != 0) {
    iVar1 = FUN__text__00469170(local_c);
    if (iVar1 == 0) {
      FUN__text__00454ab0(0xe);
    }
    else {
      FUN__text__00454ab0(0xb);
    }
  }
LAB__text__004362c7:
  local_8 = 0x4362d4;
  FUN__text__0056ce80();
  return;
}

