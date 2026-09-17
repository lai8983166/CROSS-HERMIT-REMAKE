
void FUN__text1__0081080b(int param_1,int param_2,int param_3,uint param_4)

{
  uint uVar1;
  uint uVar2;
  uint uVar3;
  uint local_68;
  int local_64;
  int local_60;
  int local_5c [21];
  undefined4 local_8;
  
  local_5c[0] = 0x243f6a88;
  local_5c[1] = 0x85a308d3;
  local_5c[2] = 0x13198a2e;
  local_5c[3] = 0x3707344;
  local_5c[4] = 0xa4093822;
  local_5c[5] = 0x299f31d0;
  local_5c[6] = 0x82efa98;
  local_5c[7] = 0xec4e6c89;
  local_5c[8] = 0x452821e6;
  local_5c[9] = 0x38d01377;
  local_5c[10] = 0xbe5466cf;
  local_5c[0xb] = 0x34e90c6c;
  local_5c[0xc] = 0xc0ac29b7;
  local_5c[0xd] = 0xc97c50dd;
  local_5c[0xe] = 0x3f84d5b5;
  local_5c[0xf] = 0xb5470917;
  local_5c[0x10] = 0x9216d5d9;
  local_5c[0x11] = 0x8979fb1b;
  for (local_5c[0x12] = 0; local_5c[0x12] < 0x12; local_5c[0x12] = local_5c[0x12] + 1) {
    *(int *)(param_1 + 0x1000 + local_5c[0x12] * 4) = local_5c[local_5c[0x12]];
  }
  local_5c[0x14] = param_4;
  for (local_5c[0x12] = 0; local_5c[0x12] < 4; local_5c[0x12] = local_5c[0x12] + 1) {
    for (local_60 = 0; local_60 < 0x100; local_60 = local_60 + 1) {
      uVar1 = ((((uint)((local_5c[0x14] % 10000) * 0xc45 + (local_5c[0x14] / 10000) * 0x16bd) %
                10000) * 10000 + (local_5c[0x14] % 10000) * 0x16bd) % 100000000 + 1) % 100000000;
      uVar2 = (((((uVar1 % 10000) * 0xc45 + (uVar1 / 10000) * 0x16bd) % 10000) * 10000 +
               (uVar1 % 10000) * 0x16bd) % 100000000 + 1) % 100000000;
      uVar3 = (((((uVar2 % 10000) * 0xc45 + (uVar2 / 10000) * 0x16bd) % 10000) * 10000 +
               (uVar2 % 10000) * 0x16bd) % 100000000 + 1) % 100000000;
      local_5c[0x14] =
           (((((uVar3 % 10000) * 0xc45 + (uVar3 / 10000) * 0x16bd) % 10000) * 10000 +
            (uVar3 % 10000) * 0x16bd) % 100000000 + 1) % 100000000;
      *(uint *)(param_1 + local_5c[0x12] * 0x400 + local_60 * 4) =
           ((uVar1 / 10000) * 0x100) / 10000 << 0x18 |
           (((uVar2 / 10000) * 0x100) / 10000 & 0xff) << 0x10 |
           (((uVar3 / 10000) * 0x100) / 10000 & 0xff) << 8 |
           (((uint)local_5c[0x14] / 10000) * 0x100) / 10000 & 0xff;
    }
  }
  local_60 = 0;
  for (local_5c[0x12] = 0; local_5c[0x12] < 0x12; local_5c[0x12] = local_5c[0x12] + 1) {
    local_68 = 0;
    for (local_64 = 0; local_64 < 4; local_64 = local_64 + 1) {
      local_68 = local_68 << 8 | (int)*(char *)(param_2 + local_60);
      local_60 = local_60 + 1;
      if (param_3 <= local_60) {
        local_60 = 0;
      }
    }
    *(uint *)(param_1 + 0x1000 + local_5c[0x12] * 4) =
         *(uint *)(param_1 + 0x1000 + local_5c[0x12] * 4) ^ local_68;
  }
  local_8 = 0;
  local_5c[0x13] = 0;
  for (local_5c[0x12] = 0; local_5c[0x12] < 0x12; local_5c[0x12] = local_5c[0x12] + 2) {
    FUN__text1__00810dae(param_1,&local_8,local_5c + 0x13);
    *(undefined4 *)(param_1 + 0x1000 + local_5c[0x12] * 4) = local_8;
    *(int *)(param_1 + 0x1004 + local_5c[0x12] * 4) = local_5c[0x13];
  }
  for (local_5c[0x12] = 0; local_5c[0x12] < 4; local_5c[0x12] = local_5c[0x12] + 1) {
    for (local_60 = 0; local_60 < 0x100; local_60 = local_60 + 2) {
      FUN__text1__00810dae(param_1,&local_8,local_5c + 0x13);
      *(undefined4 *)(param_1 + local_5c[0x12] * 0x400 + local_60 * 4) = local_8;
      *(int *)(param_1 + local_5c[0x12] * 0x400 + 4 + local_60 * 4) = local_5c[0x13];
    }
  }
  return;
}

