
void FUN__text__00544070(int param_1,undefined4 param_2)

{
  int *piVar1;
  int iVar2;
  int iVar3;
  
  iVar2 = param_1;
  FUN__text__0054c5c9(param_1,0);
  piVar1 = (int *)(iVar2 + 0x10c);
  do {
    FUN__text__00546578(iVar2,&param_1,4);
    iVar3 = FUN__text__0054bcc3(&param_1);
    FUN__text__005466ca(iVar2);
    FUN__text__0054bcf9(iVar2,piVar1,4);
    if (*piVar1 == DAT_005d2c14) {
      FUN__text__0054c655(iVar2,param_2,iVar3);
    }
    else if (*piVar1 == DAT_005d2c1c) {
      if ((iVar3 == 0) && ((*(byte *)(iVar2 + 0x58) & 8) == 0)) {
        FUN__text__0054c5c9(iVar2,0);
      }
      else {
        FUN__text__0054381d(iVar2,"Too many IDAT\'s found");
      }
    }
    else if (*piVar1 == DAT_005d2c2c) {
      FUN__text__0054c84b();
    }
    else if (*piVar1 == DAT_005d2c24) {
      FUN__text__0054c975();
    }
    else if (*piVar1 == DAT_005d2c34) {
      FUN__text__0054c9bf();
    }
    else if (*piVar1 == DAT_005d2c3c) {
      FUN__text__0054caca();
    }
    else if (*piVar1 == DAT_005d2c44) {
      FUN__text__0054cbb9();
    }
    else {
      FUN__text__0054cd70(iVar2,param_2,iVar3);
    }
  } while ((*(byte *)(iVar2 + 0x58) & 0x10) == 0);
  return;
}

