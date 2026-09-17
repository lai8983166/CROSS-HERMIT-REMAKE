
void FUN__text__004362e0(void)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_58 [16];
  int local_18;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_58;
  for (iVar2 = 0x15; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  iVar2 = FUN__text__004e2720(2,0);
  local_14 = (int)*(short *)(&DAT_005ff8b8 + iVar2 * 2);
  local_c = 0;
  for (local_10 = 0; local_10 != local_14; local_10 = local_10 + 1) {
    uVar1 = FUN__text__00431d40(local_10 + 1);
    iVar2 = FUN__text__00469220(uVar1);
    if (iVar2 != 0) {
      local_c = local_c + 1;
    }
  }
  if (local_c == local_14) {
    local_18 = 0;
    for (local_10 = 0; local_10 != 4; local_10 = local_10 + 1) {
      iVar2 = FUN__text__00430c90(1,local_10);
      local_18 = local_18 + iVar2;
    }
    if (local_18 != 0) {
      if (*(int *)(local_8 + 0x2e6f8) < 0x4651) {
        iVar2 = FUN__text__00430c30();
        if (iVar2 == 0) {
          FUN__text__00454ab0(5);
        }
        else {
          FUN__text__00454ab0(2);
        }
      }
      else if (*(int *)(local_8 + 0x2e6f8) < 0xd2f1) {
        FUN__text__00454ab0(8);
      }
      else {
        FUN__text__00454ab0(0xb);
      }
      goto LAB__text__00436441;
    }
  }
  iVar2 = FUN__text__00430f60();
  if (iVar2 != 0) {
    FUN__text__00454ab0(0xe);
  }
LAB__text__00436441:
  local_8 = 0x43644e;
  FUN__text__0056ce80();
  return;
}

