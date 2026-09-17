
uint __thiscall FUN__text1__0080ea40(int *param_1,byte *param_2,uint param_3)

{
  byte *pbVar1;
  int local_c;
  uint local_8;
  
  if (param_3 == 0) {
    local_8 = 0;
    for (local_c = 0; local_c < 4; local_c = local_c + 1) {
      local_8 = local_8 << 8 | (uint)*param_2;
      param_2 = param_2 + 1;
      if ((byte *)param_1[1] <= param_2) {
        param_2 = (byte *)*param_1;
      }
    }
  }
  else if (param_3 < (uint)(param_1[1] - (int)param_2)) {
    param_2 = param_2 + param_3;
    if (param_2 < (byte *)param_1[2]) {
      local_8 = (uint)*param_2 << 0x18 | (uint)param_2[1] << 0x10 | (uint)param_2[2] << 8 |
                (uint)param_2[3];
    }
    else {
      local_8 = FUN__text1__0080ea40(param_2,0);
    }
  }
  else {
    pbVar1 = (byte *)(*param_1 + (param_3 - (param_1[1] - (int)param_2)));
    if (pbVar1 < (byte *)param_1[2]) {
      local_8 = (uint)*pbVar1 << 0x18 | (uint)pbVar1[1] << 0x10 | (uint)pbVar1[2] << 8 |
                (uint)pbVar1[3];
    }
    else {
      local_8 = FUN__text1__0080ea40(pbVar1,0);
    }
  }
  return local_8;
}

