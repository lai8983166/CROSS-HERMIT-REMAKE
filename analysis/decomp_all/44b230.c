
void FUN__text__0044b230(void)

{
  char cVar1;
  int iVar2;
  uint uVar3;
  undefined4 *puVar4;
  undefined4 local_58 [16];
  short local_18;
  short local_14;
  int local_10;
  uint local_c;
  int local_8;
  
  puVar4 = local_58;
  for (iVar2 = 0x15; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_10 = FUN__text__004283b0();
  local_10 = local_10 << 2;
  for (local_c = 0; local_c != 0x14; local_c = local_c + 1) {
    cVar1 = *(char *)(local_8 + 0x1ab0 + local_10 * 8);
    if (cVar1 != '\0') {
      uVar3 = local_c & 0x80000003;
      if ((int)uVar3 < 0) {
        uVar3 = (uVar3 - 1 | 0xfffffffc) + 1;
      }
      local_14 = (short)uVar3 * 0x48 + 0xdd;
      local_18 = (short)((int)(local_c + ((int)local_c >> 0x1f & 3U)) >> 2) * 0x48 + 0x49;
      FUN__text__0044b300(local_14,CONCAT22(cVar1 >> 7,local_18),local_10);
    }
    local_10 = local_10 + 1;
  }
  local_8 = 0x44b2f2;
  FUN__text__0056ce80();
  return;
}

