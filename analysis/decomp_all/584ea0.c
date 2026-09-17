
undefined4 FUN__text__00584ea0(ushort *param_1,uint *param_2,int *param_3)

{
  int iVar1;
  uint uVar2;
  undefined1 local_34 [16];
  uint local_24;
  undefined4 local_20;
  uint local_1c;
  uint local_18;
  int local_14;
  int local_c;
  int local_8;
  
  local_8 = (param_1[5] & 0x7fff) - 0x3fff;
  local_24 = param_1[5] & 0x8000;
  local_1c = *(uint *)(param_1 + 3);
  local_18 = *(uint *)(param_1 + 1);
  local_14 = (uint)*param_1 << 0x10;
  if (local_8 == -0x3fff) {
    local_c = 0;
    iVar1 = __IsZeroMan(&local_1c);
    if (iVar1 == 0) {
      __FillZeroMan(&local_1c);
      local_20 = 2;
    }
    else {
      local_20 = 0;
    }
  }
  else {
    __CopyMan(local_34,&local_1c);
    iVar1 = FUN__text__00584c10(&local_1c,param_3[2]);
    if (iVar1 != 0) {
      local_8 = local_8 + 1;
    }
    if (local_8 < param_3[1] - param_3[2]) {
      __FillZeroMan(&local_1c);
      local_c = 0;
      local_20 = 2;
    }
    else if (param_3[1] < local_8) {
      if (local_8 < *param_3) {
        local_c = local_8 + param_3[5];
        local_1c = local_1c & 0x7fffffff;
        __ShrMan(&local_1c,param_3[3]);
        local_20 = 0;
      }
      else {
        __FillZeroMan(&local_1c);
        local_1c = local_1c | 0x80000000;
        __ShrMan(&local_1c,param_3[3]);
        local_c = *param_3 + param_3[5];
        local_20 = 1;
      }
    }
    else {
      iVar1 = param_3[1] - local_8;
      __CopyMan(&local_1c,local_34,iVar1);
      __ShrMan(&local_1c,iVar1);
      FUN__text__00584c10(&local_1c,param_3[2]);
      __ShrMan(&local_1c,param_3[3] + 1);
      local_c = 0;
      local_20 = 2;
    }
  }
  uVar2 = local_1c | local_c << (0x20U - ((char)param_3[3] + '\x01') & 0x1f) |
          -(uint)(local_24 != 0) & 0x80000000;
  if (param_3[4] == 0x40) {
    param_2[1] = uVar2;
    *param_2 = local_18;
  }
  else if (param_3[4] == 0x20) {
    *param_2 = uVar2;
  }
  return local_20;
}

