
void FUN__text__004707b0(int param_1)

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
  local_c = (short)((int)((int)*(short *)(param_1 + 0x4d0) +
                         ((int)*(short *)(param_1 + 0x4d0) >> 0x1f & 0x1fU)) >> 5);
  local_10 = (short)((int)((int)*(short *)(param_1 + 0x4d2) +
                          ((int)*(short *)(param_1 + 0x4d2) >> 0x1f & 0xfU)) >> 4);
  FUN__text__0043c0c0((int)local_c,(int)local_10);
  local_8 = 0x47082d;
  FUN__text__0056ce80();
  return;
}

