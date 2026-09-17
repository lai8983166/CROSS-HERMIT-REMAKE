
void FUN__text__004e1a10(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_44 [13];
  undefined4 uStack_10;
  
  puVar2 = local_44;
  for (iVar1 = 0x10; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  _memset(&DAT_007f7c18,0,0x11730);
  FUN__text__004e1ad0();
  FUN__text__004e3120();
  FUN__text__004e1b20();
  _memset(&DAT_007e17e8,0,0x12ca0);
  _memset(&DAT_007f4518,0,0x3700);
  _memset(&DAT_007f4488,0,0x8c);
  _memset("PlayerName ",0,0x100);
  (*API_KERNEL32_DLL_lstrcpyA)("PlayerName ","PlayerName ");
  FUN__text__0056ce80();
  uStack_10 = 0x4e1ac3;
  FUN__text__0056ce80();
  return;
}

