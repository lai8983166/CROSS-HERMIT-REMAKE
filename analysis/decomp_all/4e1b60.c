
void FUN__text__004e1b60(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_44 [15];
  undefined4 uStack_8;
  
  puVar2 = local_44;
  for (iVar1 = 0x10; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  _memset(&DAT_007e17e8,0,0x12ca0);
  _memset(&DAT_007f4518,0,0x3700);
  _memset(&DAT_007f4488,0,0x8c);
  FUN__text__004e1be0();
  FUN__text__0049e8d0();
  uStack_8 = 0x4e1bcd;
  FUN__text__0056ce80();
  return;
}

