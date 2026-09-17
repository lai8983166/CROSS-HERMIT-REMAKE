
void FUN__text__00466fc0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [18];
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  iVar1 = (uint)*(ushort *)(*(int *)(param_1 + 600) + 2) * 2;
  *(undefined *)(param_1 + 0x502) = (&DAT_00615eac)[iVar1];
  *(undefined *)(param_1 + 0x503) = (&DAT_00615ead)[iVar1];
  return;
}

