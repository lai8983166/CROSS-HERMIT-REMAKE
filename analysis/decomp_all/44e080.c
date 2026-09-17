
void FUN__text__0044e080(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  int local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  FUN__text__004077c0(DAT_007a49fc);
  *(undefined2 *)(local_8 + 0xac) = 0x80;
  *(undefined4 *)(local_8 + 0xb0) = 0;
  *(undefined1 *)(local_8 + 0xbb) = 0xff;
  *(undefined1 *)(local_8 + 0xb8) = 0x80;
  *(undefined1 *)(local_8 + 0xb9) = 0x80;
  *(undefined1 *)(local_8 + 0xba) = 0x80;
  *(undefined2 *)(local_8 + 0xca) = 1;
  FUN__text__00407870(0x5a,0);
  FUN__text__004079c0(*(undefined4 *)(DAT_007a49fc + 0x196c),*(undefined4 *)(DAT_007a49fc + 0x1970))
  ;
  local_8 = 0x44e13c;
  FUN__text__0056ce80();
  return;
}

