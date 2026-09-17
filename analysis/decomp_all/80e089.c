
bool FUN__text1__0080e089(char *param_1,undefined1 *param_2,int *param_3)

{
  char cVar1;
  int iVar2;
  bool bVar3;
  char *pcVar4;
  uint local_2c;
  uint local_24;
  char *local_20;
  char *local_1c;
  char *local_14;
  
  local_14 = param_1;
  pcVar4 = param_1 + *param_3;
  iVar2 = *param_3;
  cVar1 = -1;
  bVar3 = true;
  *param_2 = 1;
  local_1c = param_2 + 1;
  do {
    while( true ) {
      if (pcVar4 <= local_14) goto LAB__text1__0080e259;
      if ((((pcVar4 <= local_14 + 2) || (*local_14 != cVar1)) || (local_14[1] != cVar1)) ||
         (local_14[2] != cVar1)) break;
      local_24 = 3;
      for (local_20 = local_14 + 3; (local_20 < pcVar4 && (*local_20 == cVar1));
          local_20 = local_20 + 1) {
        local_24 = local_24 + 1;
      }
      do {
        if (local_24 < 3) goto LAB__text1__0080e1d7;
        if (local_24 < 0x102) {
          local_2c = local_24;
        }
        else {
          local_2c = 0x101;
        }
        *local_1c = -1;
        local_1c[1] = (char)local_2c + -3;
        local_1c = local_1c + 2;
        local_24 = local_24 - local_2c;
      } while (local_1c < param_2 + iVar2 + -2);
      bVar3 = false;
LAB__text1__0080e1d7:
      local_14 = local_20 + -local_24;
    }
    if (*local_14 == -1) {
      *local_1c = -1;
      local_1c[1] = -1;
      local_1c = local_1c + 2;
      cVar1 = *local_14;
    }
    else {
      *local_1c = *local_14;
      cVar1 = *local_1c;
      local_1c = local_1c + 1;
    }
    local_14 = local_14 + 1;
  } while (local_1c < param_2 + iVar2 + -2);
  bVar3 = false;
LAB__text1__0080e259:
  if (bVar3) {
    *param_3 = (int)local_1c - (int)param_2;
  }
  else {
    *param_2 = 0;
    FUN__text1__00848490(param_2 + 1,param_1,*param_3);
    *param_3 = *param_3 + 1;
  }
  return bVar3;
}

