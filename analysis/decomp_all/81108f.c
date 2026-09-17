
int FUN__text1__0081108f(byte *param_1,undefined1 *param_2,int param_3,int param_4)

{
  byte bVar1;
  int iVar2;
  uint local_64;
  byte *local_60;
  int local_5c;
  undefined1 *local_54;
  int local_50;
  uint local_28;
  uint local_24;
  byte *local_20;
  byte *local_1c;
  uint local_18;
  byte *local_14;
  byte *local_10;
  byte *local_c;
  uint local_8;
  
  if (DAT_0086e2c0 == 0) {
    local_14 = param_1;
    local_c = param_1 + param_3;
    local_10 = param_2 + param_4 + -2;
    local_8 = CONCAT31(local_8._1_3_,0xff);
    local_18 = CONCAT31(local_18._1_3_,1);
    *param_2 = 1;
    local_1c = param_2 + 1;
    do {
      while( true ) {
        if (local_c <= local_14) goto LAB__text1__00811265;
        if ((((local_c <= local_14 + 2) || ((uint)*local_14 != (local_8 & 0xff))) ||
            ((uint)local_14[1] != (local_8 & 0xff))) || ((uint)local_14[2] != (local_8 & 0xff)))
        break;
        local_24 = 3;
        for (local_20 = local_14 + 3; (local_20 < local_c && ((uint)*local_20 == (local_8 & 0xff)));
            local_20 = local_20 + 1) {
          local_24 = local_24 + 1;
        }
        do {
          if (local_24 < 3) goto LAB__text1__008111e3;
          if (local_24 < 0x102) {
            local_64 = local_24;
          }
          else {
            local_64 = 0x101;
          }
          local_28 = local_64;
          *local_1c = 0xff;
          local_1c[1] = (char)local_64 - 3;
          local_1c = local_1c + 2;
          local_24 = local_24 - local_64;
        } while (local_1c < local_10);
        local_18 = local_18 & 0xffffff00;
LAB__text1__008111e3:
        local_14 = local_20 + -local_24;
      }
      if (*local_14 == 0xff) {
        *local_1c = 0xff;
        local_1c[1] = 0xff;
        local_1c = local_1c + 2;
        bVar1 = *local_14;
      }
      else {
        *local_1c = *local_14;
        bVar1 = *local_1c;
        local_1c = local_1c + 1;
      }
      local_14 = local_14 + 1;
      local_8 = CONCAT31(local_8._1_3_,bVar1);
    } while (local_1c < local_10);
    local_18 = local_18 & 0xffffff00;
LAB__text1__00811265:
    if ((local_18 & 0xff) == 0) {
      *param_2 = 0;
      FUN__text1__00848490(param_2 + 1,param_1,param_3);
      param_3 = param_3 + 1;
    }
    else {
      param_3 = (int)local_1c - (int)param_2;
    }
  }
  else {
    _memset(&local_60,0,0x38);
    iVar2 = FUN__text1__0083e3b0(&local_60,DAT_0086e2c0,"1.1.4",0x38);
    if (iVar2 == 0) {
      local_5c = param_3;
      local_50 = param_4;
      local_60 = param_1;
      local_54 = param_2;
      iVar2 = FUN__text1__0083ea4e(&local_60,4);
      if (iVar2 == 1) {
        param_3 = (int)local_54 - (int)param_2;
      }
      else {
        param_3 = 0;
      }
    }
    else {
      param_3 = 0;
    }
    FUN__text1__0083eee5(&local_60);
  }
  return param_3;
}

