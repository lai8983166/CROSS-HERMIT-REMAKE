
uint FUN__text__00570db0(char *param_1,uint param_2,uint param_3,int *param_4)

{
  int iVar1;
  uint uVar2;
  uint uVar3;
  uint local_2c;
  uint local_28;
  uint local_24;
  uint local_20;
  uint local_10;
  char *local_c;
  
  local_c = param_1;
  uVar3 = param_2 * param_3;
  if (uVar3 == 0) {
    param_2 = 0;
  }
  else {
    local_10 = uVar3;
    if ((param_4[3] & 0x10cU) == 0) {
      local_20 = 0x1000;
    }
    else {
      local_20 = param_4[6];
    }
    do {
      while( true ) {
        while( true ) {
          if (local_10 == 0) {
            return param_3;
          }
          if (((param_4[3] & 0x108U) == 0) || (param_4[1] == 0)) break;
          if (local_10 < (uint)param_4[1]) {
            local_24 = local_10;
          }
          else {
            local_24 = param_4[1];
          }
          FUN__text__0056d4d0(*param_4,local_c,local_24);
          local_10 = local_10 - local_24;
          param_4[1] = param_4[1] - local_24;
          *param_4 = *param_4 + local_24;
          local_c = local_c + local_24;
        }
        if (local_20 <= local_10) break;
        iVar1 = FUN__text__005756c0((int)*local_c,param_4);
        if (iVar1 == -1) {
          return (uVar3 - local_10) / param_2;
        }
        local_c = local_c + 1;
        local_10 = local_10 - 1;
        if (param_4[6] < 1) {
          local_2c = 1;
        }
        else {
          local_2c = param_4[6];
        }
        local_20 = local_2c;
      }
      if (((param_4[3] & 0x108U) != 0) && (iVar1 = FUN__text__005775c0(param_4), iVar1 != 0)) {
        return (uVar3 - local_10) / param_2;
      }
      if (local_20 == 0) {
        local_28 = local_10;
      }
      else {
        local_28 = local_10 - local_10 % local_20;
      }
      uVar2 = FUN__text__0057c550(param_4[4],local_c,local_28);
      if (uVar2 == 0xffffffff) {
        param_4[3] = param_4[3] | 0x20;
        return (uVar3 - local_10) / param_2;
      }
      local_10 = local_10 - uVar2;
      local_c = local_c + uVar2;
    } while (local_28 <= uVar2);
    param_4[3] = param_4[3] | 0x20;
    param_2 = (uVar3 - local_10) / param_2;
  }
  return param_2;
}

