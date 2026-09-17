
bool FUN__text__00438860(int param_1,ushort *param_2,ushort *param_3)

{
  int iVar1;
  undefined4 *puVar2;
  bool bVar3;
  undefined4 local_48 [17];
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  bVar3 = *(short *)(param_1 + 0x1e) != *(short *)(param_1 + 0x20);
  if (bVar3) {
    *param_2 = (ushort)*(byte *)(param_1 + 0x22 + *(short *)(param_1 + 0x1e) * 2);
    *param_3 = (ushort)*(byte *)(param_1 + 0x23 + *(short *)(param_1 + 0x1e) * 2);
    *(short *)(param_1 + 0x1e) = *(short *)(param_1 + 0x1e) + 1;
  }
  return !bVar3;
}

