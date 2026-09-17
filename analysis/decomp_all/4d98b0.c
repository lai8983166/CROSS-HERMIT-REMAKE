
void FUN__text__004d98b0(void)

{
  int iVar1;
  undefined2 extraout_var;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  int local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  FUN__text__004d62f0(0xb0,0xbe,0x59);
  if (*(short *)(local_8 + 0x2c726) == -1) {
    FUN__text__004d2620(0x13f,0x271,0x8d,0x1f,0x52,0xa0010101,1);
  }
  FUN__text__004d2700(&DAT_00625648,1,0x5d,0,0);
  FUN__text__004d2700(&DAT_00625618,1,0x50,*(undefined2 *)(DAT_007a49fc + 0x196c),
                      CONCAT22(extraout_var,*(undefined2 *)(DAT_007a49fc + 0x1970)));
  FUN__text__004d69e0();
  local_8 = 0x4d9980;
  FUN__text__0056ce80();
  return;
}

