
void FUN__text__00436500(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_64 [16];
  undefined4 local_24;
  int local_20;
  int local_1c;
  int local_18;
  undefined4 local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_64;
  for (iVar1 = 0x18; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_24 = FUN__text__00451d10();
  iVar1 = FUN__text__004e2760(local_24,3,0);
  if (iVar1 == 0) {
    local_20 = 0;
    for (local_1c = 0; local_1c != 5; local_1c = local_1c + 1) {
      local_18 = local_8 + 0x80aec + (0xfa - (local_1c + 1)) * 0x520;
      iVar1 = FUN__text__00469170(local_18);
      if (iVar1 != 0) {
        local_20 = local_20 + 1;
      }
    }
    if (4 < local_20) {
      FUN__text__004e29e0(local_24,3,0,1);
      iVar1 = FUN__text__004551c0(0,2);
      if (iVar1 != 0) {
        FUN__text__004549d0(0,0,2,0,0,1,1);
      }
    }
  }
  iVar1 = FUN__text__004e2760(local_24,3,1);
  if (iVar1 == 0) {
    local_20 = 0;
    for (local_1c = 0; local_1c != 5; local_1c = local_1c + 1) {
      local_18 = local_8 + 0x80aec + (0xfa - (local_1c + 6)) * 0x520;
      iVar1 = FUN__text__00469170(local_18);
      if (iVar1 != 0) {
        local_20 = local_20 + 1;
      }
    }
    if (4 < local_20) {
      local_c = FUN__text__00431d40(0xb);
      *(undefined1 *)(*(int *)(local_c + 600) + 0xa4) = 0;
      *(undefined4 *)(*(int *)(local_c + 600) + 0x20) = 0x7fffffff;
      *(undefined4 *)(*(int *)(local_c + 600) + 0x24) = 0x7fffffff;
      FUN__text__0046d970(local_c);
      FUN__text__00475140(local_c);
      FUN__text__004e29e0(local_24,3,1,1);
      iVar1 = FUN__text__004551c0(0,3);
      if (iVar1 != 0) {
        FUN__text__004549d0(0,0,3,0,0,1,1);
      }
    }
  }
  iVar1 = FUN__text__004e2760(local_24,3,1);
  if (iVar1 != 0) {
    iVar1 = FUN__text__004e2760(local_24,3,2);
    if (iVar1 == 0) {
      local_c = FUN__text__00431d40(0xb);
      iVar1 = FUN__text__00469480(local_c);
      if (iVar1 != 0) {
        FUN__text__004e29e0(local_24,3,2,1);
        iVar1 = FUN__text__004551c0(0,4);
        if (iVar1 != 0) {
          FUN__text__004549d0(0,0,4,0,0,1,1);
        }
      }
    }
    else {
      iVar1 = FUN__text__004e2760(local_24,3,3);
      if (iVar1 == 0) {
        local_10 = local_8 + 0x80aec;
        local_14 = FUN__text__00431d40(0xb);
        iVar1 = FUN__text__004695d0(local_10);
        if ((iVar1 != 0) || (iVar1 = FUN__text__004695d0(local_14), iVar1 != 0)) {
          FUN__text__004e29e0(local_24,3,3,1);
          iVar1 = FUN__text__004551c0(0,5);
          if (iVar1 != 0) {
            FUN__text__004549d0(0,0,5,1,0,1,1);
            *(undefined4 *)(*(int *)(local_8 + 0x117c38) + 0x174) = 0;
          }
        }
      }
    }
  }
  local_8 = 0x436848;
  FUN__text__0056ce80();
  return;
}

