
void FUN__text__004deca0(int param_1,int param_2,ushort *param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [17];
  int local_c;
  undefined *local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*(short *)(param_1 + 4) == 0x25) {
    local_8 = &DAT_006c2dc8 + (uint)*(ushort *)(param_1 + 4) * 0x48;
  }
  else if (*(short *)(param_1 + 4) == 0x2e) {
    local_8 = &DAT_006c2dc8 + (uint)*(ushort *)(param_1 + 4) * 0x48;
  }
  else {
    local_8 = &DAT_006c2dc8 + (uint)*(ushort *)(param_1 + 4) * 0x48;
  }
  local_c = (uint)*param_3 + (int)*(short *)(local_8 + 0x28) +
            (int)((uint)*(byte *)(*(int *)(param_2 + 600) + 8) * (int)*(short *)(local_8 + 0x2a)) /
            100;
  if (local_c < 0) {
    local_c = 0;
  }
  else if (999 < local_c) {
    local_c = 999;
  }
  *param_3 = (ushort)local_c;
  local_c = (uint)param_3[1] + (int)*(short *)(local_8 + 0x2c) +
            (int)((uint)*(byte *)(*(int *)(param_2 + 600) + 8) * (int)*(short *)(local_8 + 0x2e)) /
            100;
  if (local_c < 0) {
    local_c = 0;
  }
  else if (999 < local_c) {
    local_c = 999;
  }
  param_3[1] = (ushort)local_c;
  return;
}

