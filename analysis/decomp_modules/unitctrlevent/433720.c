
void FUN__text__00433720(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  int local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  iVar1 = FUN__text__004307b0();
  if (iVar1 == 0) {
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
  else if (*(int *)(local_8 + 0x2e6f8) < 0x6271) {
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
  local_8 = 0x4337eb;
  FUN__text__0056ce80();
  return;
}

