
uint FUN__text__004aa2a0(short param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [17];
  ushort local_c;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = 0;
  while( true ) {
    if (DAT_007a5b62 <= (short)local_c) {
      return CONCAT22(DAT_007a5b62 >> 0xf,0xffff);
    }
    if (*(short *)(&DAT_007a5662 + (short)local_c * 0x10) == param_1) break;
    local_c = local_c + 1;
  }
  return (uint)local_c;
}

