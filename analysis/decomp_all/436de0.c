
void FUN__text__00436de0(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_58 [16];
  int local_18;
  undefined4 local_14;
  undefined4 local_10;
  undefined4 local_c;
  int local_8;
  
  puVar2 = local_58;
  for (iVar1 = 0x15; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_10 = FUN__text__00431d40(0x2d);
  local_14 = FUN__text__00431d40(0x2e);
  iVar1 = FUN__text__00468d80(local_10);
  if ((iVar1 == 0) || (iVar1 = FUN__text__00468d80(local_14), iVar1 == 0)) {
    iVar1 = FUN__text__00469220(local_10);
    if (((iVar1 != 0) || (iVar1 = FUN__text__00469220(local_14), iVar1 != 0)) &&
       (iVar1 = FUN__text__004e2720(3,0), iVar1 == 0)) {
      *(undefined4 *)(*(int *)(local_8 + 0x117c38) + 0x174) = 4;
      FUN__text__004549d0(0,0,0,1,0,0,1);
      goto LAB__text__004370bb;
    }
  }
  else {
    iVar1 = FUN__text__00469220(local_10);
    if (((iVar1 == 0) && (iVar1 = FUN__text__00469220(local_14), iVar1 == 0)) &&
       (iVar1 = FUN__text__004e2720(3,0), iVar1 == 0)) {
      FUN__text__004e29a0(3,0,1);
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
      goto LAB__text__004370bb;
    }
  }
  local_c = FUN__text__00431d40(0x2f);
  iVar1 = FUN__text__00469170(local_c);
  if (iVar1 == 0) {
    iVar1 = FUN__text__00430f60();
    if (iVar1 == 0) {
      if (*(int *)(local_8 + 0x2e6f4) == 0) {
        *(undefined4 *)(*(int *)(local_8 + 0x117c38) + 0x174) = 4;
        FUN__text__004549d0(0,0,0,1,0,0,1);
      }
    }
    else {
      *(undefined4 *)(*(int *)(local_8 + 0x117c38) + 0x174) = 5;
      FUN__text__004549d0(0,0,0,1,0,0,1);
    }
  }
  else {
    local_18 = FUN__text__00431e90(&DAT_005ff8d0);
    if (local_18 == 4) {
      iVar1 = FUN__text__00430c30();
      if (iVar1 == 0) {
        *(undefined4 *)(*(int *)(local_8 + 0x117c38) + 0x174) = 2;
      }
      else {
        *(undefined4 *)(*(int *)(local_8 + 0x117c38) + 0x174) = 1;
      }
    }
    else {
      *(undefined4 *)(*(int *)(local_8 + 0x117c38) + 0x174) = 3;
    }
    FUN__text__004549d0(0,0,0,1,0,0,1);
  }
LAB__text__004370bb:
  local_8 = 0x4370c8;
  FUN__text__0056ce80();
  return;
}

