
void __fastcall FUN__text__0044be10(undefined4 param_1)

{
  char cVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_58 [16];
  char local_18;
  undefined3 uStack_17;
  uint local_14;
  int local_10;
  int local_c;
  undefined4 local_8;
  
  puVar3 = local_58;
  for (iVar2 = 0x15; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  for (local_10 = 0; local_10 != 2; local_10 = local_10 + 1) {
    for (local_c = 0; local_c != 0x40; local_c = local_c + 1) {
      local_14 = local_10 * 0x40 + local_c;
      cVar1 = FUN__text__004e3210(local_14 & 0xffff);
      _local_18 = CONCAT31(uStack_17,cVar1);
      if ((cVar1 != '\0') && (*(short *)(&DAT_007a2988 + local_c * 2 + local_10 * 0x80) == 0)) {
        *(undefined2 *)(&DAT_007a2988 + local_c * 2 + local_10 * 0x80) = 1;
      }
    }
  }
  local_8 = 0x44bebf;
  FUN__text__0056ce80();
  return;
}

