
uint FUN__text1__0083f330(int *param_1,int param_2)

{
  uint uVar1;
  int local_18;
  int local_14;
  int local_10;
  int local_8;
  
  local_8 = 0xffff;
  if (param_1[3] - 5U < 0xffff) {
    local_8 = param_1[3] + -5;
  }
  do {
    if ((uint)param_1[0x1b] < 2) {
      FUN__text1__0083f570(param_1);
      if ((param_1[0x1b] == 0) && (param_2 == 0)) {
        return 0;
      }
      if (param_1[0x1b] == 0) {
        if (param_1[0x15] < 0) {
          local_18 = 0;
        }
        else {
          local_18 = param_1[0xc] + param_1[0x15];
        }
        FUN__text1__00841f92(param_1,local_18,param_1[0x19] - param_1[0x15],param_2 == 4);
        param_1[0x15] = param_1[0x19];
        FUN__text1__0083ee20(*param_1);
        if (*(int *)(*param_1 + 0x10) == 0) {
          return (param_2 != 4) - 1 & 2;
        }
        return (-(uint)(param_2 != 4) & 0xfffffffe) + 3;
      }
    }
    param_1[0x19] = param_1[0x19] + param_1[0x1b];
    param_1[0x1b] = 0;
    uVar1 = param_1[0x15] + local_8;
    if ((param_1[0x19] == 0) || (uVar1 <= (uint)param_1[0x19])) {
      param_1[0x1b] = param_1[0x19] - uVar1;
      param_1[0x19] = uVar1;
      if (param_1[0x15] < 0) {
        local_10 = 0;
      }
      else {
        local_10 = param_1[0xc] + param_1[0x15];
      }
      FUN__text1__00841f92(param_1,local_10,param_1[0x19] - param_1[0x15],0);
      param_1[0x15] = param_1[0x19];
      FUN__text1__0083ee20(*param_1);
      if (*(int *)(*param_1 + 0x10) == 0) {
        return 0;
      }
    }
    if (param_1[9] - 0x106U <= (uint)(param_1[0x19] - param_1[0x15])) {
      if (param_1[0x15] < 0) {
        local_14 = 0;
      }
      else {
        local_14 = param_1[0xc] + param_1[0x15];
      }
      FUN__text1__00841f92(param_1,local_14,param_1[0x19] - param_1[0x15],0);
      param_1[0x15] = param_1[0x19];
      FUN__text1__0083ee20(*param_1);
      if (*(int *)(*param_1 + 0x10) == 0) {
        return 0;
      }
    }
  } while( true );
}

