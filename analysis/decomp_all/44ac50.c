
int __fastcall FUN__text__0044ac50(int param_1)

{
  char *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_54 [16];
  int local_14;
  int local_10;
  
  puVar3 = local_54;
  for (iVar2 = 0x14; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_14 = 0;
  for (local_10 = 0; local_10 != 0x1e; local_10 = local_10 + 1) {
    pcVar1 = (char *)(param_1 + 0x1ab0 + local_10 * 8);
    if ((*pcVar1 != '\0') && (pcVar1[1] != '\0')) {
      local_14 = local_14 + 1;
    }
  }
  return local_14;
}

