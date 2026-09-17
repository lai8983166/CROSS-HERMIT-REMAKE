
void FUN__text__004df0b0(int param_1,int param_2,ushort *param_3)

{
  ushort uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [17];
  int local_c;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (*(short *)(param_1 + 4) == 7) {
    uVar1 = *(ushort *)(param_1 + 4);
  }
  else {
    uVar1 = *(ushort *)(param_1 + 4);
  }
  iVar2 = (uint)uVar1 * 0x48;
  local_c = (uint)param_3[2] + (int)*(short *)(&DAT_006c2de8 + iVar2) +
            (int)((uint)*(byte *)(*(int *)(param_2 + 600) + 4) *
                 (int)*(short *)(&DAT_006c2dea + iVar2)) / 100;
  if (local_c < 0) {
    local_c = 0;
  }
  else if (999 < local_c) {
    local_c = 999;
  }
  param_3[2] = (ushort)local_c;
  local_c = (uint)*param_3 + (int)*(short *)(&DAT_006c2dec + iVar2) +
            (int)((uint)*(byte *)(*(int *)(param_2 + 600) + 4) *
                 (int)*(short *)(&DAT_006c2dee + iVar2)) / 100;
  if (local_c < 0) {
    local_c = 0;
  }
  else if (999 < local_c) {
    local_c = 999;
  }
  *param_3 = (ushort)local_c;
  local_c = (uint)param_3[1] + (int)*(short *)(&DAT_006c2df0 + iVar2) +
            (int)((uint)*(byte *)(*(int *)(param_2 + 600) + 4) *
                 (int)*(short *)(&DAT_006c2df2 + iVar2)) / 100;
  if (local_c < 0) {
    local_c = 0;
  }
  else if (999 < local_c) {
    local_c = 999;
  }
  param_3[1] = (ushort)local_c;
  return;
}

