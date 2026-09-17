
undefined4
FUN__text1__00847cd0(int param_1,int param_2,int param_3,int param_4,int param_5,int *param_6)

{
  byte bVar1;
  uint uVar2;
  uint uVar3;
  uint uVar4;
  uint uVar5;
  uint local_4c;
  uint local_48;
  uint local_44;
  uint local_40;
  uint local_3c;
  uint local_38;
  uint local_30;
  uint local_2c;
  uint local_24;
  byte *local_20;
  int local_18;
  uint local_14;
  byte *local_10;
  byte *local_c;
  byte *local_8;
  
  local_8 = (byte *)*param_6;
  local_38 = param_6[1];
  local_14 = *(uint *)(param_5 + 0x20);
  local_2c = *(uint *)(param_5 + 0x1c);
  local_c = *(byte **)(param_5 + 0x34);
  if (local_c < *(byte **)(param_5 + 0x30)) {
    local_3c = (*(int *)(param_5 + 0x30) - (int)local_c) - 1;
  }
  else {
    local_3c = *(int *)(param_5 + 0x2c) - (int)local_c;
  }
  local_30 = local_3c;
  uVar2 = *(uint *)(&DAT_008701c8 + param_1 * 4);
  uVar3 = *(uint *)(&DAT_008701c8 + param_2 * 4);
LAB__text1__00847d4a:
  for (; local_2c < 0x14; local_2c = local_2c + 8) {
    local_38 = local_38 - 1;
    local_14 = local_14 | (uint)*local_8 << ((byte)local_2c & 0x1f);
    local_8 = local_8 + 1;
  }
  local_20 = (byte *)(param_3 + (local_14 & uVar2) * 8);
  local_24 = (uint)*local_20;
  if (local_24 != 0) {
LAB__text1__00847de4:
    local_14 = local_14 >> (local_20[1] & 0x1f);
    local_2c = local_2c - local_20[1];
    if ((local_24 & 0x10) == 0) goto LAB__text1__008481dc;
    local_24 = local_24 & 0xf;
    uVar5 = *(int *)(local_20 + 4) + (local_14 & *(uint *)(&DAT_008701c8 + local_24 * 4));
    local_14 = local_14 >> (sbyte)local_24;
    for (local_2c = local_2c - local_24; local_2c < 0xf; local_2c = local_2c + 8) {
      local_38 = local_38 - 1;
      local_14 = local_14 | (uint)*local_8 << ((byte)local_2c & 0x1f);
      local_8 = local_8 + 1;
    }
    local_20 = (byte *)(param_4 + (local_14 & uVar3) * 8);
    bVar1 = *local_20;
    while( true ) {
      local_24 = (uint)bVar1;
      local_14 = local_14 >> (local_20[1] & 0x1f);
      local_2c = local_2c - local_20[1];
      if ((bVar1 & 0x10) != 0) break;
      if ((bVar1 & 0x40) != 0) {
        param_6[6] = (int)"invalid distance code";
        local_40 = param_6[1] - local_38;
        if (local_2c >> 3 < local_40) {
          local_40 = local_2c >> 3;
        }
        *(uint *)(param_5 + 0x20) = local_14;
        *(uint *)(param_5 + 0x1c) = local_2c + local_40 * -8;
        param_6[1] = local_38 + local_40;
        param_6[2] = param_6[2] + (((int)local_8 - local_40) - *param_6);
        *param_6 = (int)local_8 - local_40;
        *(byte **)(param_5 + 0x34) = local_c;
        return 0xfffffffd;
      }
      local_20 = local_20 +
                 (local_14 & *(uint *)(&DAT_008701c8 + local_24 * 4)) * 8 +
                 *(int *)(local_20 + 4) * 8;
      bVar1 = *local_20;
    }
    local_24 = local_24 & 0xf;
    for (; local_2c < local_24; local_2c = local_2c + 8) {
      local_38 = local_38 - 1;
      local_14 = local_14 | (uint)*local_8 << ((byte)local_2c & 0x1f);
      local_8 = local_8 + 1;
    }
    uVar4 = local_14 & *(uint *)(&DAT_008701c8 + local_24 * 4);
    local_14 = local_14 >> (sbyte)local_24;
    local_2c = local_2c - local_24;
    local_30 = local_30 - uVar5;
    local_10 = local_c + -(*(int *)(local_20 + 4) + uVar4);
    if (local_10 < *(byte **)(param_5 + 0x28)) {
      do {
        local_10 = local_10 + (*(int *)(param_5 + 0x2c) - *(int *)(param_5 + 0x28));
      } while (local_10 < *(byte **)(param_5 + 0x28));
      local_24 = *(int *)(param_5 + 0x2c) - (int)local_10;
      if (local_24 < uVar5) {
        local_18 = uVar5 - local_24;
        do {
          *local_c = *local_10;
          local_c = local_c + 1;
          local_10 = local_10 + 1;
          local_24 = local_24 - 1;
        } while (local_24 != 0);
        local_10 = *(byte **)(param_5 + 0x28);
        do {
          *local_c = *local_10;
          local_c = local_c + 1;
          local_10 = local_10 + 1;
          local_18 = local_18 + -1;
        } while (local_18 != 0);
      }
      else {
        *local_c = *local_10;
        local_c[1] = local_10[1];
        local_c = local_c + 2;
        local_10 = local_10 + 2;
        local_18 = uVar5 - 2;
        do {
          *local_c = *local_10;
          local_c = local_c + 1;
          local_10 = local_10 + 1;
          local_18 = local_18 + -1;
        } while (local_18 != 0);
      }
    }
    else {
      *local_c = *local_10;
      local_c[1] = local_10[1];
      local_c = local_c + 2;
      local_10 = local_10 + 2;
      local_18 = uVar5 - 2;
      do {
        *local_c = *local_10;
        local_c = local_c + 1;
        local_10 = local_10 + 1;
        local_18 = local_18 + -1;
      } while (local_18 != 0);
    }
    goto LAB__text1__008483bb;
  }
  local_14 = local_14 >> (local_20[1] & 0x1f);
  local_2c = local_2c - local_20[1];
  *local_c = local_20[4];
  local_c = local_c + 1;
  local_30 = local_30 - 1;
  goto LAB__text1__008483bb;
LAB__text1__008481dc:
  if ((local_24 & 0x40) != 0) {
    if ((local_24 & 0x20) != 0) {
      local_44 = param_6[1] - local_38;
      if (local_2c >> 3 < local_44) {
        local_44 = local_2c >> 3;
      }
      *(uint *)(param_5 + 0x20) = local_14;
      *(uint *)(param_5 + 0x1c) = local_2c + local_44 * -8;
      param_6[1] = local_38 + local_44;
      param_6[2] = param_6[2] + (((int)local_8 - local_44) - *param_6);
      *param_6 = (int)local_8 - local_44;
      *(byte **)(param_5 + 0x34) = local_c;
      return 1;
    }
    param_6[6] = (int)"invalid literal/length code";
    local_48 = param_6[1] - local_38;
    if (local_2c >> 3 < local_48) {
      local_48 = local_2c >> 3;
    }
    *(uint *)(param_5 + 0x20) = local_14;
    *(uint *)(param_5 + 0x1c) = local_2c + local_48 * -8;
    param_6[1] = local_38 + local_48;
    param_6[2] = param_6[2] + (((int)local_8 - local_48) - *param_6);
    *param_6 = (int)local_8 - local_48;
    *(byte **)(param_5 + 0x34) = local_c;
    return 0xfffffffd;
  }
  local_20 = local_20 +
             (local_14 & *(uint *)(&DAT_008701c8 + local_24 * 4)) * 8 + *(int *)(local_20 + 4) * 8;
  local_24 = (uint)*local_20;
  if (local_24 == 0) goto code_r0x0084821b;
  goto LAB__text1__00847de4;
code_r0x0084821b:
  local_14 = local_14 >> (local_20[1] & 0x1f);
  local_2c = local_2c - local_20[1];
  *local_c = local_20[4];
  local_c = local_c + 1;
  local_30 = local_30 - 1;
LAB__text1__008483bb:
  if ((local_30 < 0x102) || (local_38 < 10)) {
    local_4c = param_6[1] - local_38;
    if (local_2c >> 3 < local_4c) {
      local_4c = local_2c >> 3;
    }
    *(uint *)(param_5 + 0x20) = local_14;
    *(uint *)(param_5 + 0x1c) = local_2c + local_4c * -8;
    param_6[1] = local_38 + local_4c;
    param_6[2] = param_6[2] + (((int)local_8 - local_4c) - *param_6);
    *param_6 = (int)local_8 - local_4c;
    *(byte **)(param_5 + 0x34) = local_c;
    return 0;
  }
  goto LAB__text1__00847d4a;
}

