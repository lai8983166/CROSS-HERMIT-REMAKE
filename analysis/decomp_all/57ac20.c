
int FUN_0057ac20(undefined *param_1,undefined4 *param_2,uint *param_3)

{
  uint uVar1;
  undefined **local_c;
  
  local_c = &PTR_LOOP_00762138;
  while ((param_1 <= local_c[4] || (local_c[5] <= param_1))) {
    local_c = (undefined **)*local_c;
    if (local_c == &PTR_LOOP_00762138) {
      return 0;
    }
  }
  if ((((uint)param_1 & 0xf) == 0) && (0xff < ((uint)param_1 & 0xfff))) {
    *param_2 = local_c;
    uVar1 = (uint)param_1 & 0xfffff000;
    *param_3 = uVar1;
    return uVar1 + 8 + ((int)((int)param_1 - (uVar1 + 0x100)) >> 4);
  }
  return 0;
}

