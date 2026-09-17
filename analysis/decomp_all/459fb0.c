
void FUN__text__00459fb0(void)

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
  *(undefined2 *)(local_8 + 0xa4) = 0x80;
  *(undefined4 *)(local_8 + 0xa8) = 0;
  *(undefined1 *)(local_8 + 0xb3) = 0xff;
  *(undefined1 *)(local_8 + 0xb0) = 0x80;
  *(undefined1 *)(local_8 + 0xb1) = 0x80;
  *(undefined1 *)(local_8 + 0xb2) = 0x80;
  *(undefined2 *)(local_8 + 0xc2) = 100;
  FUN__text__00407870(0x5a,2);
  FUN__text__004079c0(0,0);
  FUN__text__00410310(*(undefined4 *)(DAT_007a49fc + 0x196c),*(undefined4 *)(DAT_007a49fc + 0x1970),
                      0x10,0x20,0,0xffffffff,0);
  local_8 = 0x45a08d;
  FUN__text__0056ce80();
  return;
}

