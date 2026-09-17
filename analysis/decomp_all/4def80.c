
void FUN__text__004def80(int param_1,int param_2,int param_3)

{
  short sVar1;
  ushort uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_50 [17];
  int local_c;
  
  puVar4 = local_50;
  for (iVar3 = 0x13; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  sVar1 = *(short *)(param_1 + 4);
  if (((sVar1 == 0x17) || (sVar1 == 0x2c)) || (sVar1 == 0x3f)) {
    uVar2 = *(ushort *)(param_1 + 4);
  }
  else {
    uVar2 = *(ushort *)(param_1 + 4);
  }
  iVar3 = (uint)uVar2 * 0x48;
  local_c = (uint)*(byte *)(param_3 + 0xb) + (int)*(short *)(&DAT_006c2df0 + iVar3) +
            (int)((uint)*(byte *)(*(int *)(param_2 + 600) + 8) *
                 (int)*(short *)(&DAT_006c2df2 + iVar3)) / 100;
  if (local_c < 0) {
    local_c = 0;
  }
  else if (0xff < local_c) {
    local_c = 0xff;
  }
  *(undefined1 *)(param_3 + 0xb) = (undefined1)local_c;
  local_c = (uint)*(byte *)(param_3 + 10) + (int)*(short *)(&DAT_006c2df4 + iVar3) +
            (int)((uint)*(byte *)(*(int *)(param_2 + 600) + 8) *
                 (int)*(short *)(&DAT_006c2df6 + iVar3)) / 100;
  if (local_c < 0) {
    local_c = 0;
  }
  else if (100 < local_c) {
    local_c = 100;
  }
  *(undefined1 *)(param_3 + 10) = (undefined1)local_c;
  return;
}

