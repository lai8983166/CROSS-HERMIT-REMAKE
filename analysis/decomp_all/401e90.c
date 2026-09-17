
undefined4 __thiscall FUN__text__00401e90(int param_1,char *param_2,undefined4 *param_3)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_74 [16];
  int local_34;
  undefined4 local_30;
  int local_2c;
  undefined4 local_28;
  float local_24;
  float local_20;
  char local_1c;
  float local_18;
  float local_14;
  float local_10;
  float local_c;
  int local_8;
  
  puVar3 = local_74;
  for (iVar2 = 0x1c; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if ((param_2 == (char *)0x0) || (param_3 == (undefined4 *)0x0)) {
    uVar1 = 0x80004005;
  }
  else {
    local_c = 0.0;
    local_2c = *(int *)(param_1 + 0x68);
    local_28 = 0;
    local_10 = (*(float *)(param_1 + 0x7c) - *(float *)(param_1 + 0x74)) * (float)local_2c;
    local_14 = 0.0;
    local_18 = local_10;
    while (*param_2 != '\0') {
      local_1c = *param_2;
      param_2 = param_2 + 1;
      if (local_1c == '\n') {
        local_c = 0.0;
        local_18 = local_18 + local_10;
      }
      if ('\x1f' < local_1c) {
        local_20 = *(float *)(param_1 + 0x70 + (local_1c + -0x20) * 0x10);
        local_24 = *(float *)(param_1 + 0x78 + (local_1c + -0x20) * 0x10);
        local_34 = *(int *)(param_1 + 100);
        local_30 = 0;
        local_c = (local_24 - local_20) * (float)local_34 + local_c;
        if (local_14 < local_c) {
          local_14 = local_c;
        }
      }
    }
    local_8 = param_1;
    uVar1 = __ftol();
    *param_3 = uVar1;
    uVar1 = __ftol();
    param_3[1] = uVar1;
    uVar1 = 0;
  }
  return uVar1;
}

