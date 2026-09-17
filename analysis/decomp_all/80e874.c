
bool FUN__text1__0080e874(char *param_1,byte *param_2,int *param_3,int param_4)

{
  int iVar1;
  byte *pbVar2;
  byte *pbVar3;
  int local_1c;
  byte *local_18;
  byte *local_14;
  byte local_8;
  
  local_14 = (byte *)(param_1 + 1);
  local_18 = param_2;
  iVar1 = *param_3;
  local_8 = 0xff;
  if (*param_1 == '\0') {
    *param_3 = *param_3 + -1;
    FUN__text1__00848490(param_2,param_1 + 1,*param_3);
    return true;
  }
  while ((pbVar2 = local_14, local_14 < param_1 + iVar1 && (local_18 < param_2 + param_4))) {
    if (*local_14 == 0xff) {
      pbVar3 = local_14 + 1;
      if (*pbVar3 == 0xff) {
        *local_18 = *pbVar3;
        local_8 = *local_18;
        local_18 = local_18 + 1;
      }
      else {
        local_1c = *pbVar3 + 3;
        pbVar2 = local_14 + 2;
        if (param_2 + param_4 <= local_18 + *pbVar3 + 3) break;
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
  local_14 = pbVar2;
  *param_3 = (int)local_18 - (int)param_2;
  return local_14 == (byte *)(param_1 + iVar1);
}

