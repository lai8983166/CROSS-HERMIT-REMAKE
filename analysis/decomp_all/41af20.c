
void FUN__text__0041af20(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  int local_14;
  undefined4 local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_10 = FUN__text__0041aea0();
  local_14 = 0;
  for (local_c = 0; local_c != 0x10; local_c = local_c + 1) {
    if ((*(char *)(local_8 + 0x1780 + local_c * 0x88) != '\0') &&
       (*(char *)(local_8 + 0x1781 + local_c * 0x88) != '\0')) {
      local_14 = local_14 + 1;
    }
  }
  local_8 = 0x41afc0;
  FUN__text__0056ce80();
  return;
}

