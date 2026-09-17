
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined4 FUN__text__0057de80(int param_1,int param_2,int param_3,int param_4,undefined4 *param_5)

{
  int iVar1;
  undefined4 local_2c;
  undefined4 local_28;
  undefined8 local_24;
  undefined8 local_1c;
  undefined4 local_10;
  
  local_10 = 0;
  if (_DAT_00592d98 <= (double)CONCAT44(param_2,param_1)) {
    local_1c = (double)CONCAT44(param_2,param_1);
  }
  else {
    local_1c = -(double)CONCAT44(param_2,param_1);
  }
  if ((param_4 == 0x7ff00000) && (param_3 == 0)) {
    if (local_1c <= _DAT_005f9d58) {
      if (_DAT_005f9d58 <= local_1c) {
        *param_5 = DAT_007646d0;
        param_5[1] = DAT_007646d4;
        local_10 = 1;
      }
      else {
        *param_5 = 0;
        param_5[1] = 0;
      }
    }
    else {
      *param_5 = DAT_007646c8;
      param_5[1] = DAT_007646cc;
    }
  }
  else if ((param_4 == -0x100000) && (param_3 == 0)) {
    if (local_1c <= _DAT_005f9d58) {
      if (_DAT_005f9d58 <= local_1c) {
        *param_5 = DAT_007646d0;
        param_5[1] = DAT_007646d4;
        local_10 = 1;
      }
      else {
        *param_5 = DAT_007646c8;
        param_5[1] = DAT_007646cc;
      }
    }
    else {
      *param_5 = 0;
      param_5[1] = 0;
    }
  }
  else if ((param_2 == 0x7ff00000) && (param_1 == 0)) {
    if ((double)CONCAT44(param_4,param_3) <= _DAT_00592d98) {
      if (_DAT_00592d98 <= (double)CONCAT44(param_4,param_3)) {
        *param_5 = 0;
        param_5[1] = 0x3ff00000;
      }
      else {
        *param_5 = 0;
        param_5[1] = 0;
      }
    }
    else {
      *param_5 = DAT_007646c8;
      param_5[1] = DAT_007646cc;
    }
  }
  else if ((param_2 == -0x100000) && (param_1 == 0)) {
    iVar1 = FUN__text__0057e0f0(param_3,param_4);
    if ((double)CONCAT44(param_4,param_3) <= _DAT_00592d98) {
      if (_DAT_00592d98 <= (double)CONCAT44(param_4,param_3)) {
        *param_5 = 0;
        param_5[1] = 0x3ff00000;
      }
      else {
        if (iVar1 == 1) {
          local_2c = DAT_007646e8;
          local_28 = DAT_007646ec;
        }
        else {
          local_2c = 0;
          local_28 = 0;
        }
        *param_5 = local_2c;
        param_5[1] = local_28;
      }
    }
    else {
      if (iVar1 == 1) {
        local_24 = -(double)CONCAT44(DAT_007646cc,DAT_007646c8);
      }
      else {
        local_24 = (double)CONCAT44(DAT_007646cc,DAT_007646c8);
      }
      *param_5 = (undefined4)local_24;
      param_5[1] = local_24._4_4_;
    }
  }
  return local_10;
}

