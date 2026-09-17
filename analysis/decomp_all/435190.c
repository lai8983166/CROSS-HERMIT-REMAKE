
void FUN__text__00435190(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_58 [16];
  int local_18;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_58;
  for (iVar1 = 0x15; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_18 = 0;
  local_c = FUN__text__00431dd0(&DAT_005ff810);
  local_10 = FUN__text__00431dd0(&DAT_005ff81c);
  if ((local_c < 2) || (local_10 < 4)) {
    FUN__text__004e29a0(0,0,0);
    FUN__text__004e29a0(3,0,0);
  }
  else {
    local_14 = FUN__text__004e2720(0,0);
    local_14 = local_14 + 1;
    if (local_14 < 54000) {
      FUN__text__004e29a0(0,0,local_14);
    }
    else {
      local_18 = 1;
    }
    FUN__text__004e29a0(3,0,1);
  }
  if (local_18 == 0) {
    iVar1 = FUN__text__00430df0();
    if (iVar1 != 0) {
      if (*(int *)(local_8 + 0x2e6f8) < 54000) {
        FUN__text__00454ab0(0xe);
      }
      else {
        FUN__text__00454ab0(0xb);
      }
    }
  }
  else if ((local_c < 4) || (local_10 < 0xd)) {
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
  local_8 = 0x4352ec;
  FUN__text__0056ce80();
  return;
}

