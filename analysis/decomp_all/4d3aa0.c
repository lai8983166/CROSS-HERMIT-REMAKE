
void FUN__text__004d3aa0(short param_1)

{
  bool bVar1;
  short sVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_70 [22];
  short local_18;
  short local_10;
  short local_c;
  
  puVar4 = local_70;
  for (iVar3 = 0x1b; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  for (local_c = 0; local_c < 0x1e; local_c = local_c + 1) {
    sVar2 = local_c + 1;
    bVar1 = false;
    if (((&DAT_00738cd3)[sVar2 * 0x32] != '\0') && ((&DAT_00738cd4)[sVar2 * 0x32] != '\0')) {
      if ((&DAT_007cf424)[(int)local_c + param_1 * 0x124] == 'd') {
        bVar1 = true;
      }
      else if ((short)((ushort)(byte)(&DAT_00738cd3)[sVar2 * 0x32] * 6 +
                      (ushort)(byte)(&DAT_00738cd4)[sVar2 * 0x32]) <=
               (short)(DAT_007a528e * 6 + DAT_007a5290)) {
        bVar1 = true;
      }
    }
    if (bVar1) {
      bVar1 = true;
    }
    else {
      bVar1 = true;
      local_18 = 0;
      for (local_10 = 0; local_10 < 7; local_10 = local_10 + 1) {
        local_18 = local_18 + (ushort)(byte)(&DAT_007e17f4)[local_10 * 8 + param_1 * 0x4a0];
        if ((short)(ushort)(byte)(&DAT_007e17f4)[local_10 * 8 + param_1 * 0x4a0] <
            *(short *)(&DAT_00738cd6 + local_10 * 2 + sVar2 * 0x32)) {
          bVar1 = false;
        }
      }
      if (local_18 < *(short *)(&DAT_00738ce4 + sVar2 * 0x32)) {
        bVar1 = false;
      }
      for (local_10 = 0; local_10 < 3; local_10 = local_10 + 1) {
        if (((byte)(&DAT_00738ce6)[local_10 * 2 + sVar2 * 0x32] != 0) &&
           ((int)(char)(&DAT_007cf423)
                       [(int)(short)(ushort)(byte)(&DAT_00738ce6)[local_10 * 2 + sVar2 * 0x32] +
                        param_1 * 0x124] <
            (int)(short)(ushort)(byte)(&DAT_00738ce7)[local_10 * 2 + sVar2 * 0x32])) {
          bVar1 = false;
        }
      }
    }
    if (bVar1) {
      (&DAT_007cf445)[(int)local_c + param_1 * 0x124] = 1;
    }
  }
  return;
}

