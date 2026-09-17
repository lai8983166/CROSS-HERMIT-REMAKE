
void FUN__text__00434300(void)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_5c [16];
  int local_1c;
  short *local_18;
  uint local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_5c;
  for (iVar2 = 0x16; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_10 = 0;
  iVar2 = FUN__text__004e2720(3,0);
  if (((iVar2 != 0) && (iVar2 = FUN__text__004e2720(3,1), iVar2 != 0)) &&
     (iVar2 = FUN__text__004e2720(3,2), iVar2 != 0)) {
    local_14 = 0;
    if ((*(short *)(local_8 + 0x2e814) != 0) && ((*(byte *)(local_8 + 0x2e816) & 3) != 0)) {
      local_14 = 1;
    }
    if ((*(short *)(local_8 + 0x2e854) != 0) && ((*(byte *)(local_8 + 0x2e856) & 0x18) != 0)) {
      local_14 = local_14 + 1;
    }
    if ((*(short *)(local_8 + 0x2e894) != 0) && ((*(byte *)(local_8 + 0x2e896) & 0x18) != 0)) {
      local_14 = local_14 + 1;
    }
    if (*(short *)(local_8 + 0x2e8d4) != 0) {
      local_14 = local_14 + 1;
    }
    if (*(short *)(local_8 + 0x2e914) != 0) {
      local_14 = local_14 + 1;
    }
    local_18 = (short *)(local_8 + 0x2e954);
    if (*local_18 != 0) {
      local_14 = local_14 + 1;
    }
    if (local_14 < 6) {
      FUN__text__004e29a0(0,0,0);
    }
    else {
      local_1c = FUN__text__004e2720(0,0);
      local_1c = local_1c + 1;
      if (local_1c < 300) {
        FUN__text__004e29a0(0,0,local_1c);
      }
      else {
        local_10 = 1;
      }
    }
  }
  if (local_10 == 0) {
    if (*(int *)(local_8 + 0x2e6f4) == 0) {
      FUN__text__00454ab0(0xb);
    }
    else {
      iVar2 = FUN__text__00430df0();
      if (iVar2 != 0) {
        FUN__text__00454ab0(0xe);
      }
    }
  }
  else {
    local_c = 0;
    uVar1 = FUN__text__00431d40(1);
    iVar2 = FUN__text__00469220(uVar1);
    if (iVar2 != 0) {
      local_c = local_c + 1;
    }
    uVar1 = FUN__text__00431d40(2);
    iVar2 = FUN__text__00469220(uVar1);
    if (iVar2 != 0) {
      local_c = local_c + 1;
    }
    uVar1 = FUN__text__00431d40(3);
    iVar2 = FUN__text__00469220(uVar1);
    if (iVar2 != 0) {
      local_c = local_c + 1;
    }
    if (local_c < 3) {
      FUN__text__00454ab0(8);
    }
    else {
      iVar2 = FUN__text__00430ba0();
      if (iVar2 == 0) {
        FUN__text__00454ab0(5);
      }
      else {
        FUN__text__00454ab0(2);
      }
    }
  }
  local_8 = 0x4345a4;
  FUN__text__0056ce80();
  return;
}

