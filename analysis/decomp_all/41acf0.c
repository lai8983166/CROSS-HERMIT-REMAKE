
int __fastcall FUN__text__0041acf0(int param_1)

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
  local_10 = 0;
  for (local_c = 0; local_c != 0x10; local_c = local_c + 1) {
    if (*(char *)(param_1 + 0x1780 + local_c * 0x88) != '\0') {
      local_10 = local_10 + 1;
    }
  }
  return local_10;
}

