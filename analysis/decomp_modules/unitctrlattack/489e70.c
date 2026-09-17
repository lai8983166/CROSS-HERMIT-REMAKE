
void FUN__text__00489e70(int param_1,int param_2,int param_3,int *param_4,undefined4 param_5)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_64 [16];
  int local_24;
  int local_20;
  int local_1c;
  short local_18;
  short local_14;
  int local_10;
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_64;
  for (iVar1 = 0x18; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  FUN__text__00427b70(param_3 + 0xc);
  local_c = 0x7fffffff;
  local_20 = 0;
  while (local_1c = FUN__text__00427bf0(), local_1c != 0) {
    local_24 = *(int *)(local_1c + 8);
    local_14 = (short)((int)((*(int *)(local_24 + 0x2ec) >> 0x10) +
                            (*(int *)(local_24 + 0x2ec) >> 0x1f & 0x1fU)) >> 5);
    local_18 = (short)((int)((*(int *)(local_24 + 0x2f0) >> 0x10) +
                            (*(int *)(local_24 + 0x2f0) >> 0x1f & 0xfU)) >> 4);
    iVar1 = FUN__text__0043c1d0(param_1,param_2,(int)local_14,(int)local_18,param_5);
    if (iVar1 != 0) {
      iVar1 = FUN__text__0056db00(param_1 - local_14);
      local_10 = FUN__text__0056db00(param_2 - local_18);
      local_10 = iVar1 + local_10;
      if (local_10 < local_c) {
        local_20 = local_1c;
        local_c = local_10;
      }
    }
  }
  if (local_20 != 0) {
    param_4[*param_4 + 1] = *(int *)(local_20 + 8);
    *param_4 = *param_4 + 1;
    FUN__text__00427c90(local_20);
    FUN__text__00427e70(local_20);
  }
  local_8 = 0x489fc7;
  FUN__text__0056ce80();
  return;
}

