
void FUN__text__00470900(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  short local_10;
  short local_c;
  undefined4 local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = (short)((int)((*(int *)(param_1 + 0x2ec) >> 0x10) +
                         (*(int *)(param_1 + 0x2ec) >> 0x1f & 0x1fU)) >> 5);
  local_10 = (short)((int)((*(int *)(param_1 + 0x2f0) >> 0x10) +
                          (*(int *)(param_1 + 0x2f0) >> 0x1f & 0xfU)) >> 4);
  iVar1 = FUN__text__0043c0c0((int)local_c,(int)local_10);
  if (1 < iVar1) {
    *(short *)(param_1 + 0x4cc) = (short)((uint)*(undefined4 *)(param_1 + 0x2ec) >> 0x10);
    *(short *)(param_1 + 0x4ce) = (short)((uint)*(undefined4 *)(param_1 + 0x2f0) >> 0x10);
    FUN__text__00470840(param_1);
  }
  local_8 = 0x4709be;
  FUN__text__0056ce80();
  return;
}

