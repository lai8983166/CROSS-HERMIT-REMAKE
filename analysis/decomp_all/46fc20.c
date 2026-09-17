
void __thiscall FUN__text__0046fc20(int param_1,int param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_58 [16];
  short local_18;
  short local_14;
  short local_10;
  short local_c;
  int local_8;
  
  puVar2 = local_58;
  for (iVar1 = 0x15; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = *(short *)(DAT_007a49fc + 0x196c);
  local_10 = *(short *)(DAT_007a49fc + 0x1970);
  if ((0x1d < local_10) && (local_10 < 600)) {
    local_14 = ((short)((uint)*(undefined4 *)(param_2 + 0x2ec) >> 0x10) -
               *(short *)(param_1 + 0x2a30e)) +
               (short)(char)(&DAT_00615e5c)[(uint)*(byte *)(param_2 + 0x502) * 4];
    local_18 = ((short)((uint)*(undefined4 *)(param_2 + 0x2f0) >> 0x10) -
               *(short *)(param_1 + 0x2a310)) + 0x1e +
               (short)(char)(&DAT_00615e5d)[(uint)*(byte *)(param_2 + 0x502) * 4];
    local_8 = param_1;
    iVar1 = FUN__text__0056db00((int)local_c - (int)local_14);
    if (iVar1 <= (char)(&DAT_00615e5e)[(uint)*(byte *)(param_2 + 0x502) * 4]) {
      FUN__text__0056db00((int)local_10 - (int)local_18);
    }
  }
  local_8 = 0x46fd6a;
  FUN__text__0056ce80();
  return;
}

