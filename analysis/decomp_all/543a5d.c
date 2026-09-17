
void FUN__text__00543a5d(int param_1,int param_2)

{
  int *piVar1;
  int iVar2;
  undefined4 uVar3;
  uint uVar4;
  int iVar5;
  char *pcVar6;
  
  iVar2 = param_1;
  if (*(byte *)(param_1 + 0x11c) < 8) {
    uVar4 = (uint)*(byte *)(param_1 + 0x11c);
    iVar5 = -uVar4 + 8;
    FUN__text__00546578(param_1,uVar4 + 0x20 + param_2,iVar5);
    *(undefined1 *)(iVar2 + 0x11c) = 8;
    iVar5 = FUN__text__00546612(param_2 + 0x20,uVar4,iVar5);
    if (iVar5 != 0) {
      if ((uVar4 < 4) && (iVar5 = FUN__text__00546612(param_2 + 0x20,uVar4,-uVar4 + 4), iVar5 != 0))
      {
        pcVar6 = "Not a PNG file";
      }
      else {
        pcVar6 = "PNG file corrupted by ASCII conversion";
      }
      FUN__text__0054381d(iVar2,pcVar6);
    }
  }
  piVar1 = (int *)(iVar2 + 0x10c);
  while( true ) {
    while( true ) {
      while( true ) {
        while( true ) {
          FUN__text__00546578(iVar2,&param_1,4);
          uVar3 = FUN__text__0054bcc3(&param_1);
          FUN__text__005466ca(iVar2);
          FUN__text__0054bcf9(iVar2,piVar1,4);
          if (*piVar1 != DAT_005d2c14) break;
          FUN__text__0054c655(iVar2,param_2,uVar3);
        }
        if (*piVar1 != DAT_005d2c2c) break;
        FUN__text__0054c84b(iVar2,param_2,uVar3);
      }
      if (*piVar1 != DAT_005d2c24) break;
      FUN__text__0054c975(iVar2,param_2,uVar3);
    }
    if (*piVar1 == DAT_005d2c1c) break;
    if (*piVar1 == DAT_005d2c34) {
      FUN__text__0054c9bf();
    }
    else if (*piVar1 == DAT_005d2c3c) {
      FUN__text__0054caca();
    }
    else if (*piVar1 == DAT_005d2c44) {
      FUN__text__0054cbb9();
    }
    else {
      FUN__text__0054cd70(iVar2,param_2,uVar3);
    }
  }
  if ((*(uint *)(iVar2 + 0x58) & 1) == 0) {
    pcVar6 = "Missing IHDR before IDAT";
  }
  else {
    if ((*(char *)(iVar2 + 0x116) != '\x03') || ((*(uint *)(iVar2 + 0x58) & 2) != 0))
    goto LAB__text__00543bc1;
    pcVar6 = "Missing PLTE before IDAT";
  }
  FUN__text__0054381d(iVar2,pcVar6);
LAB__text__00543bc1:
  *(uint *)(iVar2 + 0x58) = *(uint *)(iVar2 + 0x58) | 4;
  *(undefined4 *)(iVar2 + 0xfc) = uVar3;
  return;
}

