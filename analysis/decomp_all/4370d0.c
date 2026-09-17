
void FUN__text__004370d0(void)

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
  local_c = FUN__text__00431e90(&DAT_005ff8dc);
  local_10 = FUN__text__00431e90(&DAT_005ff8e8);
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
    iVar1 = FUN__text__00430f60();
    if (iVar1 != 0) {
      if (*(int *)(local_8 + 0x2e6f8) < 54000) {
        *(undefined4 *)(*(int *)(local_8 + 0x117c38) + 0x174) = 5;
      }
      else {
        *(undefined4 *)(*(int *)(local_8 + 0x117c38) + 0x174) = 4;
      }
      FUN__text__004549d0(0,0,0,1,0,0,1);
    }
  }
  else {
    if ((local_c < 4) || (local_10 < 0xd)) {
      *(undefined4 *)(*(int *)(local_8 + 0x117c38) + 0x174) = 3;
    }
    else {
      iVar1 = FUN__text__00430c30();
      if (iVar1 == 0) {
        *(undefined4 *)(*(int *)(local_8 + 0x117c38) + 0x174) = 2;
      }
      else {
        *(undefined4 *)(*(int *)(local_8 + 0x117c38) + 0x174) = 1;
      }
    }
    FUN__text__004549d0(0,0,0,1,0,0,1);
  }
  local_8 = 0x437273;
  FUN__text__0056ce80();
  return;
}

