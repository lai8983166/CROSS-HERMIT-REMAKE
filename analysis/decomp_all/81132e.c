
int FUN__text1__0081132e(char *param_1,byte *param_2,int param_3,int param_4)

{
  byte *pbVar1;
  int iVar2;
  byte *pbVar3;
  int local_60;
  char *local_58;
  int local_54;
  byte *local_4c;
  int local_48;
  int local_20;
  int local_1c;
  byte *local_18;
  byte *local_14;
  byte *local_10;
  byte *local_c;
  byte local_8;
  
  if (DAT_0086e2c0 == 0) {
    local_14 = (byte *)(param_1 + 1);
    local_18 = param_2;
    local_c = (byte *)(param_1 + param_3);
    local_10 = param_2 + param_4;
    local_8 = 0xff;
    if (*param_1 != '\0') {
      while ((pbVar1 = local_14, local_14 < local_c && (local_18 < local_10))) {
        if (*local_14 == 0xff) {
          pbVar3 = local_14 + 1;
          if (*pbVar3 == 0xff) {
            *local_18 = *pbVar3;
            local_8 = *local_18;
            local_18 = local_18 + 1;
          }
          else {
            local_1c = *pbVar3 + 3;
            pbVar1 = local_14 + 2;
            if (local_10 <= local_18 + *pbVar3 + 3) break;
            while (local_1c != 0) {
              *local_18 = local_8;
              local_18 = local_18 + 1;
              local_1c = local_1c + -1;
            }
          }
          local_14 = local_14 + 2;
        }
        else {
          *local_18 = *local_14;
          local_8 = *local_18;
          local_18 = local_18 + 1;
          local_14 = local_14 + 1;
        }
      }
      local_14 = pbVar1;
      if (local_14 == local_c) {
        local_60 = (int)local_18 - (int)param_2;
      }
      else {
        local_60 = 0;
      }
      return local_60;
    }
    param_3 = param_3 + -1;
    FUN__text1__00848490(param_2,param_1 + 1,param_3);
  }
  else {
    _memset(&local_58,0,0x38);
    local_54 = param_3;
    local_48 = param_4;
    local_58 = param_1;
    local_4c = param_2;
    local_20 = FUN__text1__008409fa(&local_58,"1.1.4",0x38);
    if (local_20 == 0) {
      iVar2 = FUN__text1__00840a15(&local_58,4);
      if (iVar2 == 1) {
        param_3 = (int)local_4c - (int)param_2;
      }
      else {
        param_3 = 0;
      }
      FUN__text1__0084082b(&local_58);
    }
    else {
      param_3 = 0;
    }
  }
  return param_3;
}

