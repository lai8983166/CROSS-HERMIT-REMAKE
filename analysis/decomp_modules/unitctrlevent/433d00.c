
void FUN__text__00433d00(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  undefined4 local_14;
  undefined4 local_10;
  undefined4 local_c;
  int local_8;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_10 = FUN__text__00431d40(0x2d);
  local_14 = FUN__text__00431d40(0x2e);
  iVar1 = FUN__text__0046a430(local_10);
  if ((iVar1 == 0) || (iVar1 = FUN__text__0046a430(local_14), iVar1 == 0)) {
    iVar1 = FUN__text__00469220(local_10);
    if (((iVar1 != 0) || (iVar1 = FUN__text__00469220(local_14), iVar1 != 0)) &&
       (iVar1 = FUN__text__004e2720(3,0), iVar1 == 0)) {
      FUN__text__00454ab0(0xc);
      goto LAB__text__00433f5f;
    }
  }
  else {
    iVar1 = FUN__text__00469220(local_10);
    if (((iVar1 == 0) && (iVar1 = FUN__text__00469220(local_14), iVar1 == 0)) &&
       (iVar1 = FUN__text__004e2720(3,0), iVar1 == 0)) {
      FUN__text__004e29a0(3,0,1);
      FUN__text__00454bb0(0,0,0x14);
      FUN__text__0047fc60(9,0x34,0x55,5);
      FUN__text__0047fc60(10,2,3,5);
      FUN__text__0047fc60(0xb,3,0x5b,5);
      FUN__text__0047f4b0(1,0,0);
      FUN__text__0047f4b0(1,1,0);
      FUN__text__0047f4b0(1,2,2);
      FUN__text__0047f4b0(1,3,1);
      FUN__text__0047f4b0(2,0,0);
      FUN__text__0047f4b0(2,1,0);
      FUN__text__0047f4b0(2,2,2);
      FUN__text__0047f4b0(2,3,1);
      goto LAB__text__00433f5f;
    }
  }
  local_c = FUN__text__00431d40(0x2f);
  iVar1 = FUN__text__00469170(local_c);
  if (iVar1 == 0) {
    iVar1 = FUN__text__00430df0();
    if (iVar1 == 0) {
      if (*(int *)(local_8 + 0x2e6f4) == 0) {
        FUN__text__00454ab0(0xb);
      }
    }
    else {
      FUN__text__00454ab0(0xe);
    }
  }
  else if (*(short *)(local_8 + 0x115cce) == 4) {
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
LAB__text__00433f5f:
  local_8 = 0x433f6c;
  FUN__text__0056ce80();
  return;
}

