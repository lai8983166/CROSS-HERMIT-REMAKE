
int FUN__text__00541e46(int param_1)

{
  int iVar1;
  undefined **ppuVar2;
  undefined **ppuVar3;
  
  if (param_1 == 0) {
    DAT_0075ed94 = 0xffff;
    ppuVar2 = &PTR_DAT_0075e500;
    ppuVar3 = &PTR_DAT_0075e418;
    for (iVar1 = 0x39; iVar1 != 0; iVar1 = iVar1 + -1) {
      *ppuVar3 = *ppuVar2;
      ppuVar2 = ppuVar2 + 1;
      ppuVar3 = ppuVar3 + 1;
    }
  }
  else if (DAT_0075ed94 == 0xffff) {
    DAT_0075ed94 = 0;
    ppuVar2 = &PTR_DAT_0075e500;
    ppuVar3 = &PTR_DAT_0075e418;
    for (iVar1 = 0x39; iVar1 != 0; iVar1 = iVar1 + -1) {
      *ppuVar3 = *ppuVar2;
      ppuVar2 = ppuVar2 + 1;
      ppuVar3 = ppuVar3 + 1;
    }
    FUN__text__0054b56c(&PTR_DAT_0075e418);
    iVar1 = FUN__text__00541b9b(4,"DisableD3DXPSGP",&param_1,4);
    if (iVar1 == 0) {
      param_1 = 0;
    }
    if (param_1 != 1) {
      iVar1 = FUN__text__00541d92(7);
      if (iVar1 == 0) {
        iVar1 = FUN__text__00541d92(10);
        if (iVar1 == 0) {
          iVar1 = FUN__text__00541d92(6);
          if (iVar1 != 0) {
            FUN__text__0054abb0(&PTR_DAT_0075e418);
            DAT_0075ed94 = 3;
          }
        }
        else {
          FUN__text__0054acc0(&PTR_DAT_0075e418);
          DAT_0075ed94 = 2;
        }
      }
      else {
        FUN__text__0054aea5(&PTR_DAT_0075e418);
        DAT_0075ed94 = 1;
      }
    }
  }
  return DAT_0075ed94;
}

