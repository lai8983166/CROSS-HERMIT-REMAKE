
void FUN__text__0046e3d0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  short local_14;
  short local_10;
  ushort local_c;
  undefined4 local_8;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if ((*(char *)(param_1 + 0x501) != -1) && (*(int *)(*(int *)(param_1 + 600) + 0x24) < 0x7fffffff))
  {
    local_c = (ushort)*(byte *)(param_1 + 0x501);
    if (local_c < 10) {
      local_10 = *(short *)(&DAT_00617ef0 + (short)local_c * 4) + 0x36;
    }
    else {
      local_10 = *(short *)(&DAT_00617ef0 + (short)local_c * 4) + -0x28;
    }
    local_14 = *(short *)(&DAT_00617ef2 + (short)local_c * 4) + 0x20;
    FUN__text__0046e4c0(CONCAT22((short)((uint)*(int *)(param_1 + 600) >> 0x10),local_10),local_14,
                        *(undefined4 *)(*(int *)(param_1 + 600) + 0x24));
  }
  local_8 = 0x46e4b2;
  FUN__text__0056ce80();
  return;
}

