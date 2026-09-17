
undefined4 FUN__text__0057b390(int param_1,uint *param_2,byte *param_3,uint param_4)

{
  int *piVar1;
  uint uVar2;
  uint *local_1c;
  undefined4 local_18;
  uint *local_14;
  uint local_c;
  
  local_18 = 0;
  piVar1 = (int *)(param_1 + 0x18 + ((int)param_2 - *(int *)(param_1 + 0x10) >> 0xc) * 8);
  uVar2 = (uint)*param_3;
  if (param_4 < uVar2) {
    *param_3 = (byte)param_4;
    *piVar1 = *piVar1 + (uVar2 - param_4);
    piVar1[1] = 0xf1;
    local_18 = 1;
  }
  else if ((uVar2 < param_4) && (param_3 + param_4 <= param_2 + 0x3e)) {
    local_1c = (uint *)(param_3 + param_4);
    for (local_14 = (uint *)(param_3 + uVar2); (local_14 < local_1c && ((char)*local_14 == '\0'));
        local_14 = (uint *)((int)local_14 + 1)) {
    }
    if (local_14 == local_1c) {
      *param_3 = (byte)param_4;
      if ((param_3 <= (byte *)*param_2) && ((uint *)*param_2 < local_1c)) {
        if (local_1c < param_2 + 0x3e) {
          *param_2 = (uint)local_1c;
          local_c = 0;
          for (; (char)*local_1c == '\0'; local_1c = (uint *)((int)local_1c + 1)) {
            local_c = local_c + 1;
          }
          param_2[1] = local_c;
        }
        else {
          *param_2 = (uint)(param_2 + 2);
          param_2[1] = 0;
        }
      }
      *piVar1 = *piVar1 + (uVar2 - param_4);
      local_18 = 1;
    }
  }
  return local_18;
}

