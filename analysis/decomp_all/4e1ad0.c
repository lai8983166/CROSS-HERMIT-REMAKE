
void FUN__text__004e1ad0(void)

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
  _memset(&DAT_007f7c18,0,0x400);
  FUN__text__004e2c60(&DAT_00809320);
  uStack_8 = 0x4e1b18;
  FUN__text__0056ce80();
  return;
}

