
char __fastcall FUN__text__0041ad60(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  char local_c;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = '\0';
  while( true ) {
    if (local_c == '\x10') {
      return -1;
    }
    if ((*(char *)(param_1 + 0x1780 + local_c * 0x88) != '\0') &&
       (*(int *)(param_1 + 0x1804 + local_c * 0x88) == *(int *)(param_1 + 0x138))) break;
    local_c = local_c + '\x01';
  }
  return local_c;
}

