
undefined4 __thiscall FUN__text__004d6930(int param_1,undefined4 *param_2)

{
  int iVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  short local_10;
  short local_c;
  
  iVar1 = -0x33333334;
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_10 = -1;
  local_c = 0;
  while( true ) {
    if (99 < local_c) goto LAB__text__004d69ca;
    if (*(short *)(param_1 + 0x24 + local_c * 0x28) != 1) break;
    local_c = local_c + 1;
    iVar1 = CONCAT22((short)((uint)param_1 >> 0x10),local_c);
  }
  *(undefined2 *)(param_1 + 0x24 + local_c * 0x28) = 1;
  *(undefined2 *)(param_1 + 0x26 + local_c * 0x28) = 0;
  iVar1 = local_c * 0x28;
  puVar3 = (undefined4 *)(param_1 + 0x28 + iVar1);
  for (iVar2 = 9; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = *param_2;
    param_2 = param_2 + 1;
    puVar3 = puVar3 + 1;
  }
  local_10 = local_c;
LAB__text__004d69ca:
  return CONCAT22((short)((uint)iVar1 >> 0x10),local_10);
}

