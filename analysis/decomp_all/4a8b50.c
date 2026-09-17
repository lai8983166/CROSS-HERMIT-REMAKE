
void FUN__text__004a8b50(short param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  short local_c;
  undefined4 local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  DAT_007d57d8 = (undefined1)param_1;
  local_c = -1;
  if (-1 < param_1) {
    local_c = *(short *)(&DAT_007aaa12 + param_1 * 0x1c) + -0x65;
  }
  FUN__text__004a2980(CONCAT22(param_1 >> 0xf,local_c));
  local_8 = 0x4a8bba;
  FUN__text__0056ce80();
  return;
}

