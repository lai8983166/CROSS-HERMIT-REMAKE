
void FUN__text__00436c80(void)

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
  local_c = FUN__text__00431d40(1);
  iVar1 = FUN__text__00469170(local_c);
  if (iVar1 == 0) {
    if (*(int *)(local_8 + 0x2e6f4) == 0) {
      *(undefined4 *)(*(int *)(local_8 + 0x117c38) + 0x174) = 4;
      FUN__text__004549d0(0,0,0,1,0,0,1);
    }
    else {
      iVar1 = FUN__text__00430f60();
      if (iVar1 != 0) {
        *(undefined4 *)(*(int *)(local_8 + 0x117c38) + 0x174) = 5;
        FUN__text__004549d0(0,0,0,1,0,0,1);
      }
    }
  }
  else {
    local_10 = FUN__text__00431e90(&DAT_005ff8cc);
    if (local_10 == 1) {
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
  local_8 = 0x436dcd;
  FUN__text__0056ce80();
  return;
}

