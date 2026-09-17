
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN__text__00452cf0(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_60 [16];
  int local_20;
  int local_1c;
  int local_18;
  int local_14;
  undefined *local_10;
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_60;
  for (iVar1 = 0x17; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if ((((char)DAT_007f448c == '\0') && (local_1c = (int)DAT_007f4488, 0x4b < local_1c)) &&
     ((local_1c < 0x51 || (local_1c == 0x62)))) {
    local_20 = DAT_007f4488 + -0x4c;
    switch(local_20) {
    case 0:
      local_10 = &DAT_00606948;
      local_18 = 5;
      break;
    case 1:
      local_10 = &DAT_00606cb8;
      local_18 = 8;
      break;
    case 2:
      local_10 = &DAT_00607238;
      local_18 = 3;
      break;
    case 3:
      local_10 = &DAT_00607448;
      local_18 = 4;
      break;
    case 4:
      local_10 = &DAT_00607708;
      local_18 = 1;
      break;
    default:
      local_10 = &DAT_00607d38;
      local_18 = 0xc;
      DAT_007f44b8 = 0;
      break;
    case 10:
      local_10 = &DAT_00608578;
      local_18 = 0x50;
    }
    local_14 = 0;
    for (local_c = 0; local_c != local_18; local_c = local_c + 1) {
      if ((byte)local_10[local_c * 0xb0 + 0xa4] < 4) {
        local_14 = local_14 + 1;
      }
    }
    DAT_007f448c._1_1_ = (char)local_14;
    DAT_007f448c._2_1_ = 0;
    _DAT_007f4508 = 0;
    for (local_c = 0; local_c != DAT_007f448c._1_1_; local_c = local_c + 1) {
      FUN__text__0056d4d0(&DAT_007f4518 + local_c * 0xb0,local_10 + local_c * 0xb0,0xb0);
      if ((byte)(&DAT_007f45bc)[local_c * 0xb0] < 4) {
        (&DAT_007f45b3)[local_c * 0xb0] = (char)DAT_007f4492 + (char)(local_c % 5);
        (&DAT_007f45b4)[local_c * 0xb0] = (char)DAT_007f4494 + (char)(local_c / 5);
      }
    }
  }
  local_8 = 0x452eff;
  FUN__text__0056ce80();
  return;
}

