
void __thiscall FUN__text__0046fd70(int param_1,int param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  short local_10;
  short local_c;
  int local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if ((*(int *)(param_1 + 0x2a340) == 1) && (*(int *)(DAT_007a49fc + 0x19b8) == 3)) {
    local_c = ((short)((uint)*(undefined4 *)(param_2 + 0x2ec) >> 0x10) -
              *(short *)(param_1 + 0x2a30e)) +
              (short)(char)(&DAT_00615e5c)[(uint)*(byte *)(param_2 + 0x502) * 4];
    local_10 = ((short)((uint)*(undefined4 *)(param_2 + 0x2f0) >> 0x10) -
               *(short *)(param_1 + 0x2a310)) + 0x1e +
               (short)(char)(&DAT_00615e5d)[(uint)*(byte *)(param_2 + 0x502) * 4];
    local_8 = param_1;
    iVar1 = FUN__text__0056db00((int)local_c - *(int *)(param_1 + 0x2a330));
    if (iVar1 <= *(int *)(local_8 + 0x2a338) +
                 (int)(char)(&DAT_00615e5e)[(uint)*(byte *)(param_2 + 0x502) * 4]) {
      FUN__text__0056db00((int)local_10 - *(int *)(local_8 + 0x2a334));
    }
  }
  local_8 = 0x46feb4;
  FUN__text__0056ce80();
  return;
}

