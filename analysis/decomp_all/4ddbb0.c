
undefined4 FUN__text__004ddbb0(int param_1)

{
  char cVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_5c [16];
  int local_1c;
  char local_18;
  int local_14;
  char local_10;
  float local_c;
  char local_8;
  
  puVar3 = local_5c;
  for (iVar2 = 0x16; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = *(char *)(*(int *)(param_1 + 600) + 0x2c);
  local_10 = *(char *)(param_1 + 0x34);
  if (local_10 == '.') {
    local_14 = (int)local_8;
    local_c = (float)local_14;
    local_8 = __ftol();
  }
  else if (local_10 == '/') {
    local_8 = ' ';
  }
  local_18 = *(char *)(param_1 + 0x14);
  if (local_18 == '\x06') {
    local_1c = (int)local_8;
    local_c = (float)local_1c;
    local_8 = __ftol();
  }
  cVar1 = local_8;
  if (local_8 < '\0') {
    local_8 = '\0';
  }
  if ('\x1f' < local_8) {
    local_8 = ' ';
  }
  return CONCAT31(cVar1 >> 7,local_8);
}

