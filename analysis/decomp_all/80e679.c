
void FUN__text1__0080e679(int *param_1,byte *param_2,uint *param_3)

{
  byte *pbVar1;
  int local_820;
  int local_81c [257];
  byte *local_418;
  int local_414 [256];
  uint local_14;
  byte *local_10;
  void *local_c;
  byte *local_8;
  
  local_81c[0] = *param_1;
  pbVar1 = (byte *)(param_1 + 1);
  *param_3 = *param_3 - 4;
  local_c = operator_new(*param_3 << 2);
  for (local_14 = 0; local_14 < 0x100; local_14 = local_14 + 1) {
    local_81c[local_14 + 1] = 0;
    local_414[local_14] = 0;
  }
  local_8 = pbVar1;
  local_10 = pbVar1 + *param_3;
  for (; local_8 < local_10; local_8 = local_8 + 1) {
    local_81c[*local_8 + 1] = local_81c[*local_8 + 1] + 1;
  }
  for (local_14 = 1; local_14 < 0x100; local_14 = local_14 + 1) {
    local_414[local_14] = local_414[local_14 - 1] + local_81c[local_14];
  }
  local_418 = pbVar1;
  for (local_14 = 0; local_14 < *param_3; local_14 = local_14 + 1) {
    *(uint *)((int)local_c + local_414[*local_418] * 4) = local_14;
    local_414[*local_418] = local_414[*local_418] + 1;
    local_418 = local_418 + 1;
  }
  local_418 = param_2;
  local_820 = local_81c[0];
  for (local_14 = 0; local_14 < *param_3; local_14 = local_14 + 1) {
    *local_418 = pbVar1[local_820];
    local_418 = local_418 + 1;
    local_820 = *(int *)((int)local_c + local_820 * 4);
  }
  FUN__text1__00848476(local_c);
  return;
}

