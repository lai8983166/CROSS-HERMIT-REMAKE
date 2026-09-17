
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN__text__0040b590(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  undefined4 local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  _DAT_00791728 = 0;
  _memset(&DAT_00765728,0,0x2c000);
  local_8 = 0x40b5d7;
  FUN__text__0056ce80();
  return;
}

