
undefined4 __thiscall
FUN__text__004ca130(int param_1,short param_2,short param_3,short param_4,short param_5)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [17];
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (param_2 != -1) {
    *(short *)(param_1 + 2) = param_2;
  }
  if (param_3 != -1) {
    *(short *)(param_1 + 6) = param_3;
  }
  if (param_4 != -1) {
    *(short *)(param_1 + 8) = param_4;
  }
  if (param_5 != -1) {
    *(short *)(param_1 + 10) = param_5;
  }
  return CONCAT31((int3)(char)((ushort)param_5 >> 8),1);
}

