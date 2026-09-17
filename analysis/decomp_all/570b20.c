
void FUN__text__00570b20(byte *param_1,undefined1 *param_2,undefined1 *param_3,int param_4,
                        undefined1 *param_5)

{
  size_t sVar1;
  int local_24;
  int local_20;
  int local_1c;
  int local_18;
  byte *local_10;
  byte *local_c;
  byte *local_8;
  
  local_c = (byte *)0x0;
  sVar1 = _strlen((char *)param_1);
  if ((sVar1 == 0) || (param_1[1] != 0x3a)) {
    if (param_2 != (undefined1 *)0x0) {
      *param_2 = 0;
    }
  }
  else {
    if (param_2 != (undefined1 *)0x0) {
      FUN__text__0057c420(param_2,param_1,2);
      param_2[2] = 0;
    }
    param_1 = param_1 + 2;
  }
  local_10 = (byte *)0x0;
  for (local_8 = param_1; *local_8 != 0; local_8 = local_8 + 1) {
    if (((&DAT_0080aa21)[*local_8] & 4) == 0) {
      if ((*local_8 == 0x2f) || (*local_8 == 0x5c)) {
        local_10 = local_8 + 1;
      }
      else if (*local_8 == 0x2e) {
        local_c = local_8;
      }
    }
    else {
      local_8 = local_8 + 1;
    }
  }
  if (local_10 == (byte *)0x0) {
    if (param_3 != (undefined1 *)0x0) {
      *param_3 = 0;
    }
  }
  else {
    if (param_3 != (undefined1 *)0x0) {
      if ((uint)((int)local_10 - (int)param_1) < 0xff) {
        local_18 = (int)local_10 - (int)param_1;
      }
      else {
        local_18 = 0xff;
      }
      FUN__text__0057c420(param_3,param_1,local_18);
      param_3[local_18] = 0;
    }
    param_1 = local_10;
  }
  if ((local_c == (byte *)0x0) || (local_c < param_1)) {
    if (param_4 != 0) {
      if ((uint)((int)local_8 - (int)param_1) < 0xff) {
        local_24 = (int)local_8 - (int)param_1;
      }
      else {
        local_24 = 0xff;
      }
      FUN__text__0057c420(param_4,param_1,local_24);
      *(undefined1 *)(param_4 + local_24) = 0;
    }
    if (param_5 != (undefined1 *)0x0) {
      *param_5 = 0;
    }
  }
  else {
    if (param_4 != 0) {
      if ((uint)((int)local_c - (int)param_1) < 0xff) {
        local_1c = (int)local_c - (int)param_1;
      }
      else {
        local_1c = 0xff;
      }
      FUN__text__0057c420(param_4,param_1,local_1c);
      *(undefined1 *)(param_4 + local_1c) = 0;
    }
    if (param_5 != (undefined1 *)0x0) {
      if ((uint)((int)local_8 - (int)local_c) < 0xff) {
        local_20 = (int)local_8 - (int)local_c;
      }
      else {
        local_20 = 0xff;
      }
      FUN__text__0057c420(param_5,local_c,local_20);
      param_5[local_20] = 0;
    }
  }
  return;
}

