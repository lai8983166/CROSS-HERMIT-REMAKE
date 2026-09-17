
void __fastcall FUN__text__0046f170(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_14 = 0;
  local_10 = 0;
  local_8 = param_1;
  for (local_c = 0; local_c != 0xfa; local_c = local_c + 1) {
    iVar1 = FUN__text__00468d10(local_8 + 0x80aec + local_c * 0x520);
    if (iVar1 != 0) {
      iVar1 = FUN__text__0046a430(local_8 + 0x80aec + local_c * 0x520);
      if ((iVar1 == 0) || (*(char *)(local_8 + 0x80d78 + local_c * 0x520) == '\0')) {
        iVar1 = FUN__text__0046a430(local_8 + 0x80aec + local_c * 0x520);
        if ((iVar1 == 0) &&
           (iVar1 = FUN__text__004690a0(local_8 + 0x80aec + local_c * 0x520), iVar1 != 0)) {
          *(undefined1 *)(local_8 + 0x80d78 + local_c * 0x520) = 0;
        }
      }
      else {
        local_10 = local_10 + 1;
        iVar1 = FUN__text__00469480(local_8 + 0x80aec + local_c * 0x520);
        if (iVar1 != 0) {
          local_14 = local_14 + 1;
        }
      }
    }
  }
  *(undefined4 *)(local_8 + 0x108b50) = 0;
  for (local_c = 0; local_c != 0xfa; local_c = local_c + 1) {
    iVar1 = FUN__text__00468d10(local_8 + 0x80aec + local_c * 0x520);
    if (iVar1 != 0) {
      if ((local_10 == 0) ||
         (iVar1 = FUN__text__0046a430(local_8 + 0x80aec + local_c * 0x520), iVar1 != 0)) {
        if ((local_14 == 0) ||
           (iVar1 = FUN__text__00469480(local_8 + 0x80aec + local_c * 0x520), iVar1 != 0)) {
          if (*(char *)(local_8 + 0x80d78 + local_c * 0x520) != '\0') {
            *(int *)(local_8 + 0x108b60 + *(int *)(local_8 + 0x108b50) * 4) =
                 local_8 + 0x80aec + local_c * 0x520;
            *(int *)(local_8 + 0x108b50) = *(int *)(local_8 + 0x108b50) + 1;
          }
        }
        else {
          *(undefined1 *)(local_8 + 0x80d78 + local_c * 0x520) = 0;
        }
      }
      else {
        *(undefined1 *)(local_8 + 0x80d78 + local_c * 0x520) = 0;
      }
    }
  }
  if (*(int *)(local_8 + 0x108b50) == 0) {
    *(undefined4 *)(local_8 + 0x108b54) = 0;
  }
  else if ((local_10 == 0) || (local_14 == 0)) {
    if ((local_10 == 0) || (local_14 != 0)) {
      *(undefined4 *)(local_8 + 0x108b54) = 3;
    }
    else {
      *(undefined4 *)(local_8 + 0x108b54) = 2;
    }
  }
  else {
    *(undefined4 *)(local_8 + 0x108b54) = 1;
  }
  local_8 = 0x46f42e;
  FUN__text__0056ce80();
  return;
}

