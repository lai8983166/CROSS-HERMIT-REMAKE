
int FUN__text__0052ae11(int param_1,int param_2,int *param_3)

{
  int iVar1;
  int iVar2;
  
  if (((param_1 == 0) || (param_2 == 0)) || (param_3 == (int *)0x0)) {
    iVar1 = -0x7789f794;
  }
  else {
    iVar1 = FUN__text__00428a40(0x50);
    if (iVar1 == 0) {
      iVar2 = 0;
    }
    else {
      iVar2 = FUN__text__0053bb9e();
    }
    if (iVar2 == 0) {
      iVar1 = -0x7ff8fff2;
    }
    else {
      iVar1 = FUN__text__0053b9f8(param_1,param_2);
      if (iVar1 < 0) {
        FUN__text__0052a801(1);
      }
      else {
        *param_3 = iVar2;
        iVar1 = 0;
      }
    }
  }
  return iVar1;
}

