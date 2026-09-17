
void __fastcall FUN__text__004cded0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  uint local_c;
  int local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = local_c & 0xffff0000;
  local_8 = param_1;
  while ((local_c & 0xffff) < 0x38) {
    if (*(char *)(local_8 + 0x92a0 + (local_c & 0xffff)) == '\x01') {
      if (DAT_007a49fc != 0) {
        FUN__text__0041f4e0(local_c & 0xffff);
      }
      *(undefined1 *)(local_8 + 0x92a0 + (local_c & 0xffff)) = 0;
    }
    local_c = CONCAT22(local_c._2_2_,(short)local_c + 1);
  }
  local_8 = 0x4cdf6f;
  FUN__text__0056ce80();
  return;
}

