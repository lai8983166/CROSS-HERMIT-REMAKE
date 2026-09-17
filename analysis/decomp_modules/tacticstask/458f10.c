
void FUN__text__00458f10(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  short local_10;
  short local_c;
  int local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = *(short *)(DAT_007a49fc + 0x196c);
  local_10 = *(short *)(DAT_007a49fc + 0x1970);
  FUN__text__004077c0(DAT_007a49fc);
  *(undefined2 *)(local_8 + 0x148) = 0x80;
  FUN__text__00407870(0x5a,0x1b3);
  *(undefined4 *)(local_8 + 0x14c) = 0;
  *(undefined1 *)(local_8 + 0x157) = 0xff;
  *(undefined1 *)(local_8 + 0x154) = 0x80;
  *(undefined1 *)(local_8 + 0x155) = 0x80;
  *(undefined1 *)(local_8 + 0x156) = 0x80;
  *(undefined2 *)(local_8 + 0x166) = 1;
  FUN__text__004079c0((int)local_c,(int)local_10);
  local_8 = 0x458fea;
  FUN__text__0056ce80();
  return;
}

