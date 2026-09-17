
void FUN__text__004294c0(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [15];
  undefined4 uStack_10;
  uint local_c;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  _memset(&DAT_007a272c,0x20d,0);
  (*API_KERNEL32_DLL_GetTempPathA)(0x20d,&DAT_007a272c);
  local_c = FUN__text__0056ce80();
  if (local_c < 0x20e) {
    FUN__text__00429580(&DAT_007a272c);
  }
  uStack_10 = 0x429539;
  FUN__text__0056ce80();
  return;
}

