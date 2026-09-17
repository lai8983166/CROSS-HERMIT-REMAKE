
void FUN__text1__00811d10(int *param_1,uint *param_2,uint param_3,int param_4)

{
  int iVar1;
  int iVar2;
  uint uVar3;
  uint uVar4;
  int local_4c;
  uint local_48;
  uint local_44;
  int local_40;
  int local_38;
  uint local_30;
  uint local_2c;
  int local_28;
  uint local_18;
  uint local_10;
  uint *local_8;
  
  iVar1 = *param_1;
  local_10 = param_1[1];
  iVar2 = param_1[2];
  local_18 = param_1[3];
  local_8 = param_2;
  param_2 = (uint *)((int)param_2 + (param_3 & 0xfffffff8));
  if (param_4 < 1) {
    while (local_8 < param_2) {
      local_44 = *local_8;
      local_48 = local_8[1];
      local_40 = -0x3910c8e0;
      local_4c = 0x20;
      while (local_4c != 0) {
        local_48 = local_48 -
                   (local_44 * 0x10 + iVar2 ^ local_44 + local_40 ^ (local_44 >> 5) + local_18);
        local_44 = local_44 -
                   (local_48 * 0x10 + iVar1 ^ local_48 + local_40 ^ (local_48 >> 5) + local_10);
        local_40 = local_40 + 0x61c88647;
        local_4c = local_4c + -1;
      }
      *local_8 = local_44;
      local_8[1] = local_48;
      local_8 = local_8 + 2;
      if (param_4 < 0) {
        local_10 = local_44;
        local_18 = local_48;
      }
    }
  }
  else {
    while (local_8 < param_2) {
      uVar3 = *local_8;
      uVar4 = local_8[1];
      local_28 = 0;
      local_38 = 0x20;
      local_30 = uVar4;
      local_2c = uVar3;
      while (local_38 != 0) {
        local_28 = local_28 + -0x61c88647;
        local_2c = local_2c +
                   (local_30 * 0x10 + iVar1 ^ local_30 + local_28 ^ (local_30 >> 5) + local_10);
        local_30 = local_30 +
                   (local_2c * 0x10 + iVar2 ^ local_2c + local_28 ^ (local_2c >> 5) + local_18);
        local_38 = local_38 + -1;
      }
      *local_8 = local_2c;
      local_8[1] = local_30;
      local_8 = local_8 + 2;
      if (1 < param_4) {
        local_18 = uVar4;
        local_10 = uVar3;
      }
    }
  }
  return;
}

