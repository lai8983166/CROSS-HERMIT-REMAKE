
int FUN__text__0052ae80(int param_1,int *param_2)

{
  int iVar1;
  int iVar2;
  
  if (param_1 == 0) {
    iVar1 = -0x7789f794;
  }
  else if (param_2 == (int *)0x0) {
    iVar1 = -0x7789f794;
  }
  else {
    iVar2 = FUN__text__00428a40(0x20);
    if (iVar2 == 0) {
      iVar2 = 0;
    }
    else {
      iVar2 = FUN__text__0053c665();
    }
    if (iVar2 == 0) {
      iVar1 = -0x7ff8fff2;
    }
    else {
      iVar1 = FUN__text__0053bc06(param_1);
      if (iVar1 < 0) {
        FUN__text__0052a81d(1);
      }
      else {
        *param_2 = iVar2;
        iVar1 = 0;
      }
    }
  }
  return iVar1;
}

