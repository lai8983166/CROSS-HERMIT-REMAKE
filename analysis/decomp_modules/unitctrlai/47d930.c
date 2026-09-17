
void FUN__text__0047d930(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  short local_10 [2];
  short local_c [2];
  undefined4 local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c[0] = (short)((int)((int)*(short *)(param_1 + 0x4d0) +
                            ((int)*(short *)(param_1 + 0x4d0) >> 0x1f & 0x1fU)) >> 5);
  local_10[0] = (short)((int)((int)*(short *)(param_1 + 0x4d2) +
                             ((int)*(short *)(param_1 + 0x4d2) >> 0x1f & 0xfU)) >> 4);
  *(undefined1 *)(param_1 + 0x28b) = 0xff;
  *(short *)(param_1 + 0x4d4) = (short)((uint)*(undefined4 *)(param_1 + 0x2ec) >> 0x10);
  *(short *)(param_1 + 0x4d6) = (short)((uint)*(undefined4 *)(param_1 + 0x2f0) >> 0x10);
  iVar1 = FUN__text__00438860(param_1 + 0x3e0,local_c,local_10);
  if (iVar1 != 0) {
    local_c[0] = *(short *)(param_1 + 0x4d4);
    local_10[0] = *(short *)(param_1 + 0x4d4);
  }
  *(short *)(param_1 + 0x4d8) = local_c[0] * 0x20 + 0x10;
  *(short *)(param_1 + 0x4da) = local_10[0] * 0x10 + 8;
  local_8 = 0x47da28;
  FUN__text__0056ce80();
  return;
}

