
void __thiscall FUN__text__004d56a0(undefined4 param_1,int *param_2,short param_3,int param_4)

{
  int iVar1;
  int *piVar2;
  undefined4 *puVar3;
  undefined4 local_80 [16];
  int local_40;
  int local_3c;
  int local_38;
  short local_34;
  short local_30;
  short local_2c;
  int local_28 [4];
  int local_18;
  int local_14;
  int local_10;
  short local_c;
  undefined4 local_8;
  
  puVar3 = local_80;
  for (iVar1 = 0x1f; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  local_30 = param_3 + 1;
  local_40 = (int)DAT_007a528c;
  if ((local_40 < 0) || (1 < local_40)) {
    local_34 = 0x87;
  }
  else {
    local_34 = 100;
  }
  local_28[0] = 0;
  local_18 = 0;
  local_14 = 0;
  for (local_2c = 0; (int)local_2c < local_34 + 1; local_2c = local_2c + 1) {
    local_14 = local_14 + *(int *)(&DAT_006e4308 + local_2c * 4);
  }
  local_10 = local_14 - param_4;
  for (local_2c = 0; local_2c < local_30; local_2c = local_2c + 1) {
    local_28[0] = local_28[0] + *(int *)(&DAT_006e4308 + local_2c * 4);
  }
  local_28[1] = local_28[0] + *(int *)(&DAT_006e4308 + local_30 * 4);
  local_28[2] = *(int *)(&DAT_006e4308 + local_2c * 4);
  local_28[3] = (local_28[0] + *(int *)(&DAT_006e4308 + local_30 * 4)) - param_4;
  local_c = 0;
  local_38 = param_4 - local_28[0];
  if (-1 < local_38) {
    local_3c = local_28[2];
    if (local_28[2] == 0) {
      local_3c = 1;
    }
    local_c = (short)((local_38 * 100) / local_3c);
    local_18 = local_38;
    local_c = FUN__text__004d1ba0((int)local_c,0,100);
  }
  piVar2 = local_28;
  for (iVar1 = 8; iVar1 != 0; iVar1 = iVar1 + -1) {
    *param_2 = *piVar2;
    piVar2 = piVar2 + 1;
    param_2 = param_2 + 1;
  }
  local_8 = 0x4d583f;
  FUN__text__0056ce80();
  return;
}

