
void __thiscall FUN__text__004d0790(int param_1,char param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  char local_10;
  uint local_c;
  int local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = local_c & 0xffff0000;
  local_8 = param_1;
  while ((local_c & 0xffff) == 0) {
    iVar1 = (local_c & 0xffff) * 0x1c8;
    if (*(char *)(local_8 + 4 + iVar1) != '\0') {
      FUN__text__004ce090(CONCAT22((short)((uint)iVar1 >> 0x10),(short)local_c));
    }
    local_c = CONCAT22(local_c._2_2_,(short)local_c + 1);
  }
  local_10 = *(char *)(local_8 + 0x92e1);
  if ((local_10 == '\0') && (param_2 == '\0')) {
    FUN__text__004cded0();
  }
  if (DAT_007a49fc != 0) {
    FUN__text__0040d120(2);
  }
  local_8 = 0x4d084e;
  FUN__text__0056ce80();
  return;
}

