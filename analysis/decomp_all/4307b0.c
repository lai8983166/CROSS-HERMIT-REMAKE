
void FUN__text__004307b0(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  int local_10;
  int *local_c;
  int local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  iVar1 = FUN__text__00456b20();
  if ((iVar1 == 0) || (iVar1 = FUN__text__004daae0((int)DAT_007f4488), iVar1 != 0)) {
    local_c = (int *)(local_8 + 0xdc8ec);
    for (local_10 = 0; local_10 != *local_c; local_10 = local_10 + 1) {
      iVar1 = FUN__text__0046a550(local_c[local_10 + 1]);
      if ((((iVar1 != 0) && (iVar1 = FUN__text__00469ad0(local_c[local_10 + 1]), iVar1 == 0)) &&
          (iVar1 = FUN__text__00469b90(local_c[local_10 + 1]), iVar1 == 0)) &&
         (iVar1 = FUN__text__00469c60(local_c[local_10 + 1]), iVar1 == 0)) goto LAB__text__00430967;
    }
    local_c = (int *)(local_8 + 0xdccd8);
    local_10 = 0;
    while ((local_10 != *local_c &&
           ((((iVar1 = FUN__text__0046a550(local_c[local_10 + 1]), iVar1 == 0 ||
              (iVar1 = FUN__text__00469ad0(local_c[local_10 + 1]), iVar1 != 0)) ||
             ((iVar1 = FUN__text__00469b90(local_c[local_10 + 1]), iVar1 != 0 ||
              ((iVar1 = FUN__text__00469c60(local_c[local_10 + 1]), iVar1 != 0 ||
               (*(char *)(*(int *)(local_c[local_10 + 1] + 600) + 0x96) == '\x03')))))) ||
            (*(char *)(*(int *)(local_c[local_10 + 1] + 600) + 0xf) != '\0'))))) {
      local_10 = local_10 + 1;
    }
  }
LAB__text__00430967:
  local_8 = 0x430974;
  FUN__text__0056ce80();
  return;
}

