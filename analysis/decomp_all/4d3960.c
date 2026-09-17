
void FUN__text__004d3960(short param_1,short param_2,short param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  short local_14;
  short local_10;
  short local_c;
  undefined4 local_8;
  
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
  local_c = param_1;
  local_10 = param_2;
  local_14 = (char)(&DAT_007d3d71)[(int)param_2 + param_1 * 0x44] + param_3;
  local_14 = FUN__text__004d1ba0((int)local_14,1,100);
  (&DAT_007d3d71)[(int)local_10 + local_c * 0x44] = (undefined1)local_14;
  local_8 = 0x4d3a18;
  FUN__text__0056ce80();
  return;
}

