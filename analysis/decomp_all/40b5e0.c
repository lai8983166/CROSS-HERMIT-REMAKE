
void FUN__text__0040b5e0(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = 0;
  do {
    if (local_c == 0x800) {
LAB__text__0040b64f:
      local_8 = 0x40b65c;
      FUN__text__0056ce80();
      return;
    }
    if ((&DAT_00765728)[local_c * 0x58] == '\0') {
      FUN__text__00409ef0(&DAT_00765728 + local_c * 0x58);
      goto LAB__text__0040b64f;
    }
    local_c = local_c + 1;
  } while( true );
}

