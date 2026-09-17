
void FUN__text__004337f0(void)

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
  local_c = FUN__text__00431d40(3);
  iVar1 = FUN__text__0046a430(local_c);
  if ((iVar1 == 0) || (iVar1 = FUN__text__004e2720(3,0), iVar1 != 0)) {
    local_c = FUN__text__00431d40(0xb);
    iVar1 = FUN__text__00469170(local_c);
    if ((iVar1 == 0) || (local_10 = FUN__text__00431dd0(&DAT_005ff76c), local_10 < 2)) {
      if (*(int *)(local_8 + 0x2e6f4) == 0) {
        iVar1 = FUN__text__004e2720(3,0);
        if (iVar1 == 0) {
          FUN__text__00454af0(0xb,0xb);
        }
        else {
          FUN__text__00454af0(8,8);
        }
      }
      else {
        iVar1 = FUN__text__00430df0();
        if (iVar1 != 0) {
          iVar1 = FUN__text__004e2720(3,0);
          if (iVar1 == 0) {
            FUN__text__00454af0(0xe,0xe);
          }
          else {
            FUN__text__00454af0(0xe,8);
          }
        }
      }
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
  }
  else {
    FUN__text__00454bb0(0,0,0x14);
    FUN__text__004e29a0(3,0,1);
  }
  local_8 = 0x433966;
  FUN__text__0056ce80();
  return;
}

