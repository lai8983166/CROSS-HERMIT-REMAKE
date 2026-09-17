
void FUN__text__00451670(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_68 [16];
  int local_28;
  int local_24;
  int local_20;
  char local_1c;
  undefined4 local_18;
  undefined4 local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_68;
  for (iVar1 = 0x19; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_14 = 0x78;
  FUN__text__00415480(1,5);
  DAT_007a4394 = DAT_007a4394 + 1;
  FUN__text__00415420();
  FUN__text__00451d40();
  FUN__text__00451e20();
  FUN__text__00422360(0);
  FUN__text__00496390(0);
  FUN__text__00452040();
  FUN__text__00451b10();
  FUN__text__00451bf0();
  while( true ) {
    FUN__text__004519c0();
    local_10 = FUN__text__00451a60();
    if (local_10 != 0) break;
    local_10 = 0;
  }
  FUN__text__00415420();
  for (local_c = 0; local_c != 10; local_c = local_c + 1) {
    FUN__text__00451f00();
    FUN__text__00422360(0);
  }
  FUN__text__0040d610();
  FUN__text__00465e60();
  FUN__text__004db230(0x3c);
  while (iVar1 = FUN__text__004db270(), iVar1 == 0) {
    FUN__text__00422360(0);
  }
  local_1c = *(char *)(local_8 + 0x31);
  if (local_1c == '\x01') {
    FUN__text__00419240();
    FUN__text__00417cc0();
    FUN__text__00439e30(1);
    goto LAB__text__00451990;
  }
  local_20 = DAT_007f4488 + -0x4c;
  switch(local_20) {
  case 0:
  case 1:
  case 3:
    FUN__text__00439e30(0x11);
    break;
  case 2:
  case 4:
    FUN__text__00439e30(1);
    break;
  default:
    local_18 = 0;
    if (DAT_007f448a != 0) {
      if (DAT_007f448a == -1) {
        FUN__text__00453890();
        local_18 = 1;
      }
      else {
        iVar1 = FUN__text__004536c0();
        if (iVar1 != 0) {
          FUN__text__00439e30(0x10);
          break;
        }
        FUN__text__00453890();
        local_18 = 1;
      }
    }
    iVar1 = FUN__text__00456b20();
    if (iVar1 == 0) {
      local_24 = (int)DAT_007f4488;
      if (((local_24 == 0x2d) && (local_28 = *(int *)(local_8 + 0x174), 3 < local_28)) &&
         (local_28 < 6)) {
        FUN__text__00439e30(1);
      }
      else {
        FUN__text__00439e30(0xb);
      }
    }
    else {
      iVar1 = FUN__text__004daae0((int)DAT_007f4488);
      if (iVar1 == 0) {
        FUN__text__00439e30(0xf);
      }
      else {
        FUN__text__00473dc0(local_18);
        FUN__text__00439e30(0xb);
      }
    }
    break;
  case 6:
    if (DAT_005ff720 == -1) {
      FUN__text__00439e30(2);
    }
    else {
      FUN__text__00439e30(0x11);
    }
  }
  FUN__text__00415480(1,10);
  FUN__text__00415420();
LAB__text__00451990:
  local_8 = 0x45199d;
  FUN__text__0056ce80();
  return;
}

