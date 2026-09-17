
int FUN__text__0052af68(int param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4,
                       undefined4 param_5,int *param_6)

{
  int iVar1;
  int iVar2;
  
  if (param_1 == 0) {
    iVar1 = -0x7789f794;
  }
  else if (param_6 == (int *)0x0) {
    iVar1 = -0x7789f794;
  }
  else {
    iVar2 = FUN__text__00428a40(0x494);
    if (iVar2 == 0) {
      iVar2 = 0;
    }
    else {
      iVar2 = FUN__text__0053e28f();
    }
    if (iVar2 == 0) {
      iVar1 = -0x7ff8fff2;
    }
    else {
      iVar1 = FUN__text__0053cb5f(param_1,param_2,1,param_3,param_4,param_5);
      if (iVar1 < 0) {
        FUN__text__0052a855(1);
      }
      else {
        *param_6 = iVar2;
        iVar1 = 0;
      }
    }
  }
  return iVar1;
}

