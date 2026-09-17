
int FUN__text__004d3a20(short param_1,short param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [20];
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (100 < param_1) {
    param_1 = param_1 + -0x37;
  }
  if (100 < param_2) {
    param_2 = param_2 + -0x37;
  }
  return (int)(short)(char)(&DAT_007d3d71)[(int)param_2 + param_1 * 0x44];
}

