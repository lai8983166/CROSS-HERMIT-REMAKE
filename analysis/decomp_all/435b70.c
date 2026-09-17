
void FUN__text__00435b70(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = FUN__text__004e2720(3,0);
  if (local_c == 0) {
    iVar1 = FUN__text__00430f60();
    if (iVar1 != 0) {
      FUN__text__00454ab0(0xe);
    }
  }
  else {
    local_c = FUN__text__004307b0();
    if (local_c == 0) {
      FUN__text__00454ab0(8);
    }
    else {
      iVar1 = FUN__text__00430c30();
      if (iVar1 == 0) {
        FUN__text__00454ab0(5);
      }
      else {
        FUN__text__00454ab0(2);
      }
    }
  }
  local_8 = 0x435c26;
  FUN__text__0056ce80();
  return;
}

