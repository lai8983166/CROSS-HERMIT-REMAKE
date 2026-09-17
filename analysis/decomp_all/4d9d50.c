
void FUN__text__004d9d50(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_60 [16];
  uint local_20;
  uint local_1c;
  int local_18;
  uint local_14;
  uint local_10;
  undefined2 local_c;
  undefined4 local_8;
  
  puVar2 = local_60;
  for (iVar1 = 0x17; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = 0;
  FUN__text__004d7830();
  local_10 = (uint)DAT_007e11a8;
  switch(local_10) {
  case 0:
  case 1:
  case 5:
  case 6:
    FUN__text__004d7e80();
    break;
  case 2:
  case 3:
    FUN__text__004d8620();
  }
  FUN__text__00422360(0);
  local_14 = (uint)DAT_007e11aa;
  switch(local_14) {
  case 0:
    local_18 = DAT_007e11a8 - 1;
    switch(local_18) {
    case 0:
    case 1:
      FUN__text__00439e30(9);
      break;
    case 2:
      FUN__text__00439e30(0xf);
      break;
    default:
      FUN__text__00439e30(1);
      break;
    case 4:
      break;
    case 5:
      DAT_007e11ac = 0;
    }
    break;
  case 1:
    local_1c = (uint)DAT_007e11a8;
    FUN__text__00439e30(9);
    break;
  default:
    break;
  case 3:
    DAT_007e11ac = 1;
    break;
  case 4:
    local_20 = (uint)DAT_007e11a8;
    if (local_20 == 2) {
      FUN__text__00439e30(9);
    }
    else if (local_20 == 3) {
      FUN__text__00439e30(0xf);
    }
    else if (local_20 != 4) {
      FUN__text__00439e30(1);
    }
  }
  DAT_007e11ae = 0;
  local_8 = 0x4d9ed8;
  FUN__text__0056ce80();
  return;
}

