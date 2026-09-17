
void FUN__text__004df880(int param_1,int param_2,int param_3)

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
  if ((*(short *)(param_1 + 4) == 0x31) || (*(short *)(param_1 + 4) == 0x37)) {
    uVar1 = *(ushort *)(param_1 + 4);
  }
  else {
    uVar1 = *(ushort *)(param_1 + 4);
  }
  iVar2 = (uint)uVar1 * 0x48;
  local_c = (uint)*(byte *)(param_3 + 0xb) + (int)*(short *)(&DAT_006c2de8 + iVar2) +
            (int)((uint)*(byte *)(*(int *)(param_2 + 600) + 8) *
                 (int)*(short *)(&DAT_006c2dea + iVar2)) / 100;
  if (local_c < 0) {
    local_c = 0;
  }
  else if (0xff < local_c) {
    local_c = 0xff;
  }
  *(undefined1 *)(param_3 + 0xb) = (undefined1)local_c;
  local_c = (uint)*(byte *)(param_3 + 10) + (int)*(short *)(&DAT_006c2dec + iVar2) +
            (int)((uint)*(byte *)(*(int *)(param_2 + 600) + 8) *
                 (int)*(short *)(&DAT_006c2dee + iVar2)) / 100;
  if (local_c < 0) {
    local_c = 0;
  }
  else if (100 < local_c) {
    local_c = 100;
  }
  *(undefined1 *)(param_3 + 10) = (undefined1)local_c;
  return;
}

