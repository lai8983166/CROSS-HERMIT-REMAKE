
int __fastcall FUN__text__0044abe0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  int local_14;
  int local_10;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_14 = 0;
  for (local_10 = 0; local_10 != 0x1e; local_10 = local_10 + 1) {
    if (*(char *)(param_1 + 0x1ab0 + local_10 * 8) != '\0') {
      local_14 = local_14 + 1;
    }
  }
  return local_14;
}

