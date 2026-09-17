
void FUN__text__004355a0(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  int local_10;
  undefined4 local_c;
  undefined4 local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_10 = FUN__text__00432040(&DAT_005ff848);
  if (local_10 == 0) {
    local_10 = FUN__text__00431dd0(&DAT_005ff848);
    if (local_10 == 0xf) {
      iVar1 = FUN__text__00432040(&DAT_005ff868);
      if (iVar1 == 0) {
        iVar1 = FUN__text__00430ba0();
        if (iVar1 == 0) {
          FUN__text__00454ab0(5);
        }
        else {
          FUN__text__00454ab0(2);
        }
      }
      else {
        local_c = FUN__text__00431d40(0x13);
        iVar1 = FUN__text__00469220(local_c);
        if (iVar1 == 0) {
          FUN__text__00454ab0(8);
        }
        else {
          FUN__text__00454ab0(0xb);
        }
      }
      goto LAB__text__0043569e;
    }
    iVar1 = FUN__text__00430df0();
    if (iVar1 == 0) goto LAB__text__0043569e;
  }
  FUN__text__00454ab0(0xe);
LAB__text__0043569e:
  local_8 = 0x4356ab;
  FUN__text__0056ce80();
  return;
}

