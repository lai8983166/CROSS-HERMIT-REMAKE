
void FUN__text__00457d00(void)

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
  iVar1 = FUN__text__00456b20();
  if (iVar1 != 0) {
    local_c = 0x3d2;
    local_10 = 0x298;
    FUN__text__004077c0(DAT_007a49fc);
    *(undefined2 *)(local_8 + 0x148) = 0x80;
    if (*(char *)(local_8 + 0x18c) == '\0') {
      FUN__text__00407870(0x5a,0x23f);
    }
    else {
      FUN__text__00407870(0x5a,0x23e);
    }
    *(undefined4 *)(local_8 + 0x14c) = 0;
    *(undefined1 *)(local_8 + 0x157) = 0xff;
    *(undefined1 *)(local_8 + 0x154) = 0x80;
    *(undefined1 *)(local_8 + 0x155) = 0x80;
    *(undefined1 *)(local_8 + 0x156) = 0x80;
    *(undefined2 *)(local_8 + 0x166) = 0xc6;
    FUN__text__004079c0((int)local_c,(int)local_10);
  }
  local_8 = 0x457dfa;
  FUN__text__0056ce80();
  return;
}

