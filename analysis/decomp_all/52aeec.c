
int FUN__text__0052aeec(int param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4,
                       undefined4 param_5,undefined4 param_6,int *param_7)

{
  int iVar1;
  int iVar2;
  
  if (param_1 == 0) {
    iVar1 = -0x7789f794;
  }
  else if (param_7 == (int *)0x0) {
    iVar1 = -0x7789f794;
  }
  else {
    iVar2 = FUN__text__00428a40(0x54);
    if (iVar2 == 0) {
      iVar2 = 0;
    }
    else {
      iVar2 = FUN__text__0053cb19();
    }
    if (iVar2 == 0) {
      iVar1 = -0x7ff8fff2;
    }
    else {
      iVar1 = FUN__text__0053c683(param_1,param_2,param_3,param_4,param_5,param_6);
      if (iVar1 < 0) {
        FUN__text__0052a839(1);
      }
      else {
        *param_7 = iVar2;
        iVar1 = 0;
      }
    }
  }
  return iVar1;
}

