
undefined4 __fastcall FUN__text__00430c30(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  int local_c;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = 0;
  while( true ) {
    if (local_c == 4) {
      return 1;
    }
    if (*(char *)(param_1 + local_c + 0x2ef34) != '\0') break;
    local_c = local_c + 1;
  }
  return 0;
}

