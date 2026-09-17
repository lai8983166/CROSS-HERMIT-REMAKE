
uint FUN__text__0043c920(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  uint local_c;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = 0;
  if (*(int *)(DAT_007a49fc + 0x1970) < 1) {
    local_c = 1;
  }
  else if (0x2fe < *(int *)(DAT_007a49fc + 0x1970)) {
    local_c = 2;
  }
  if (*(int *)(DAT_007a49fc + 0x196c) < 1) {
    local_c = local_c | 4;
  }
  else if (0x3fe < *(int *)(DAT_007a49fc + 0x196c)) {
    local_c = local_c | 8;
  }
  return local_c;
}

