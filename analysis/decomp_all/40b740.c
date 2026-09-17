
int FUN__text__0040b740(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  int local_10;
  int local_c;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_10 = 0x800;
  for (local_c = 0; local_c != 0x800; local_c = local_c + 1) {
    if ((&DAT_00765728)[local_c * 0x58] != '\0') {
      local_10 = local_10 + -1;
    }
  }
  return local_10;
}

