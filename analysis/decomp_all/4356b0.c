
void FUN__text__004356b0(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_64 [16];
  int local_24;
  short local_20;
  short local_1c;
  int local_18;
  int local_14;
  int local_10;
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_64;
  for (iVar1 = 0x18; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_14 = FUN__text__00432040(&DAT_005ff880);
  local_18 = 0;
  for (local_10 = 0; local_10 != 3; local_10 = local_10 + 1) {
    local_c = FUN__text__00431d40((int)*(short *)(&DAT_005ff880 + local_10 * 2));
    iVar1 = FUN__text__00469480(local_c);
    if (iVar1 != 0) {
      local_1c = (short)((int)((*(int *)(local_c + 0x2ec) >> 0x10) +
                              (*(int *)(local_c + 0x2ec) >> 0x1f & 0x1fU)) >> 5);
      local_20 = (short)((int)((*(int *)(local_c + 0x2f0) >> 0x10) +
                              (*(int *)(local_c + 0x2f0) >> 0x1f & 0xfU)) >> 4);
      iVar1 = FUN__text__0043bb90((int)local_1c,(int)local_20);
      if (iVar1 == 1) {
        local_18 = local_18 + 1;
      }
    }
  }
  local_24 = local_14;
  switch(local_14) {
  case 0:
    if (local_18 == 3) {
      iVar1 = FUN__text__00430ba0();
      if (iVar1 == 0) {
        FUN__text__00454ab0(5);
      }
      else {
        FUN__text__00454ab0(2);
      }
      goto LAB__text__0043582b;
    }
    break;
  case 1:
  case 2:
    if (3 - local_14 == local_18) {
      FUN__text__00454ab0(8);
      goto LAB__text__0043582b;
    }
    break;
  case 3:
    FUN__text__00454ab0(0xb);
    goto LAB__text__0043582b;
  }
  iVar1 = FUN__text__00430df0();
  if (iVar1 != 0) {
    FUN__text__00454ab0(0xe);
  }
LAB__text__0043582b:
  local_8 = 0x435838;
  FUN__text__0056ce80();
  return;
}

