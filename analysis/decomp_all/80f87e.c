
void __thiscall FUN__text1__0080f87e(int *param_1,int param_2,int param_3,int param_4)

{
  void *pvVar1;
  int local_810;
  uint local_80c [256];
  int aiStack_40c [256];
  int local_c;
  byte *local_8;
  
  param_1[4] = param_3;
  *param_1 = param_2;
  param_1[1] = *param_1 + param_1[4];
  param_1[2] = param_1[1] + -4;
  param_1[3] = param_4;
  param_1[5] = 0;
  pvVar1 = operator_new(param_1[4] << 2);
  param_1[6] = (int)pvVar1;
  _memset(local_80c,0,0x400);
  for (local_8 = (byte *)*param_1; local_8 < (byte *)param_1[1]; local_8 = local_8 + 1) {
    local_80c[*local_8] = local_80c[*local_8] + 1;
  }
  local_810 = 0;
  for (local_c = 0; local_c < 0x100; local_c = local_c + 1) {
    aiStack_40c[local_c] = local_810;
    local_810 = local_810 + local_80c[local_c];
  }
  for (local_8 = (byte *)*param_1; local_8 < (byte *)param_1[1]; local_8 = local_8 + 1) {
    *(byte **)(param_1[3] + aiStack_40c[*local_8] * 4) = local_8;
    aiStack_40c[*local_8] = aiStack_40c[*local_8] + 1;
  }
  for (local_c = 0; local_c < 0x100; local_c = local_c + 1) {
    if (1 < local_80c[local_c]) {
      FUN__text1__0080f24c(aiStack_40c[local_c] - local_80c[local_c],aiStack_40c[local_c],0);
    }
  }
  return;
}

