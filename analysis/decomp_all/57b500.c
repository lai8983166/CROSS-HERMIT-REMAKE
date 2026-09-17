
undefined4 FUN_0057b500(void)

{
  int iVar1;
  int iVar2;
  undefined4 uVar3;
  int local_2c;
  undefined *local_28;
  int local_24;
  undefined **local_20;
  int local_1c;
  int local_18;
  int local_14;
  int local_10;
  int local_c;
  int *local_8;
  
  local_c = 0;
  local_20 = &PTR_LOOP_00762138;
  do {
    if ((undefined **)PTR_LOOP_00764158 == local_20) {
      local_c = local_c + 1;
    }
    if (local_20[4] != (undefined *)0xffffffff) {
      local_10 = 0;
      local_2c = 0;
      local_8 = (int *)local_20[4];
      for (; local_10 < 0x400; local_10 = local_10 + 1) {
        if (local_20[local_10 * 2 + 6] == (undefined *)0xffffffff) {
          if ((local_2c == 0) && ((undefined **)local_20[3] != local_20 + local_10 * 2 + 6)) {
            return 0xffffffff;
          }
          local_2c = local_2c + 1;
        }
        else {
          if (local_8 + 0x3e <= (int *)*local_8) {
            return 0xfffffffe;
          }
          if ((char)local_8[0x3e] != -1) {
            return 0xfffffffd;
          }
          local_14 = 0;
          local_1c = 0;
          local_28 = (undefined *)0x0;
          local_24 = 0;
          while (local_14 < 0xf0) {
            if ((int)local_8 + local_14 + 8 == *local_8) {
              local_1c = local_1c + 1;
            }
            if (*(char *)((int)local_8 + local_14 + 8) == '\0') {
              local_28 = local_28 + 1;
              local_24 = local_24 + 1;
              local_14 = local_14 + 1;
            }
            else {
              if ((int)local_20[local_10 * 2 + 7] <= local_24) {
                return 0xfffffffc;
              }
              if (local_1c == 1) {
                if (local_24 < local_8[1]) {
                  return 0xfffffffb;
                }
                local_1c = 2;
              }
              local_24 = 0;
              iVar1 = local_14;
              while (local_18 = iVar1 + 1,
                    local_18 < (int)(local_14 + (uint)*(byte *)((int)local_8 + local_14 + 8))) {
                iVar2 = iVar1 + 9;
                iVar1 = local_18;
                if (*(char *)((int)local_8 + iVar2) != '\0') {
                  return 0xfffffffa;
                }
              }
              local_14 = local_18;
            }
          }
          if (local_28 != local_20[local_10 * 2 + 6]) {
            return 0xfffffff9;
          }
          if (local_1c == 0) {
            return 0xfffffff8;
          }
        }
        local_8 = local_8 + 0x400;
      }
    }
    local_20 = (undefined **)*local_20;
    if (local_20 == &PTR_LOOP_00762138) {
      if (local_c == 0) {
        uVar3 = 0xfffffff7;
      }
      else {
        uVar3 = 0;
      }
      return uVar3;
    }
  } while( true );
}

