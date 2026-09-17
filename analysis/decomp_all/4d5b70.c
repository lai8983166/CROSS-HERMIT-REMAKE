
undefined4
FUN__text__004d5b70(short param_1,short param_2,short param_3,short param_4,short param_5,
                   short param_6)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [18];
  undefined1 local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = 0;
  iVar1 = (int)param_4;
  if ((((-1 < (short)(param_1 - param_3)) && (-1 < (short)(param_2 - param_4))) &&
      (iVar1 = (int)(short)(param_1 - param_3), iVar1 <= param_5)) &&
     (iVar1 = (int)param_6, (short)(param_2 - param_4) <= iVar1)) {
    local_8 = 1;
  }
  return CONCAT31((int3)((uint)iVar1 >> 8),local_8);
}

