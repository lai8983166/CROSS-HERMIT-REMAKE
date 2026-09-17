
void FUN__text__004327e0(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  undefined4 local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_14 = FUN__text__00451d10();
  local_c = local_8 + 0xc258c;
  local_10 = local_8 + 0xc206c;
  iVar1 = FUN__text__0046a430(local_c);
  if ((iVar1 == 0) || (iVar1 = FUN__text__0046a430(local_10), iVar1 == 0)) {
    iVar1 = FUN__text__00469220(local_c);
    if (((iVar1 != 0) || (iVar1 = FUN__text__00469220(local_10), iVar1 != 0)) &&
       ((iVar1 = FUN__text__004e2760(local_14,3,0), iVar1 == 0 &&
        (iVar1 = FUN__text__004551c0(0,5), iVar1 != 0)))) {
      FUN__text__004549d0(0,0,5,1,0,1,1);
      *(undefined4 *)(*(int *)(local_8 + 0x117c38) + 0x174) = 3;
    }
  }
  else {
    iVar1 = FUN__text__00469220(local_c);
    if (((iVar1 == 0) && (iVar1 = FUN__text__00469220(local_10), iVar1 == 0)) &&
       (iVar1 = FUN__text__004e2760(local_14,3,0), iVar1 == 0)) {
      FUN__text__004e29e0(local_14,3,0,1);
      iVar1 = FUN__text__004551c0(0,10);
      if (iVar1 != 0) {
        FUN__text__004549d0(0,0,10,0,0,1,1);
      }
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
      goto LAB__text__00432b5b;
    }
  }
  iVar1 = FUN__text__00469170(local_8 + 0xc1b4c);
  if (iVar1 == 0) {
    iVar1 = FUN__text__00430df0();
    if (iVar1 == 0) {
      if ((*(int *)(local_8 + 0x2e6f4) == 0) && (iVar1 = FUN__text__004551c0(0,6), iVar1 != 0)) {
        FUN__text__004549d0(0,0,6,1,0,1,1);
        *(undefined4 *)(*(int *)(local_8 + 0x117c38) + 0x174) = 4;
      }
    }
    else {
      iVar1 = FUN__text__004551c0(0,2);
      if (iVar1 != 0) {
        FUN__text__004549d0(0,0,2,1,0,1,1);
        *(undefined4 *)(*(int *)(local_8 + 0x117c38) + 0x174) = 5;
      }
    }
  }
  else if (*(short *)(local_8 + 0x115cce) == 4) {
    iVar1 = FUN__text__004551c0(0,3);
    if (iVar1 != 0) {
      FUN__text__004549d0(0,0,3,1,0,1,1);
      *(undefined4 *)(*(int *)(local_8 + 0x117c38) + 0x174) = 1;
    }
  }
  else {
    iVar1 = FUN__text__004551c0(0,4);
    if (iVar1 != 0) {
      FUN__text__004549d0(0,0,4,1,0,1,1);
      *(undefined4 *)(*(int *)(local_8 + 0x117c38) + 0x174) = 2;
    }
  }
LAB__text__00432b5b:
  local_8 = 0x432b68;
  FUN__text__0056ce80();
  return;
}

