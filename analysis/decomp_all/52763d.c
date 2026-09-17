
int FUN__text__0052763d(int *param_1,undefined4 param_2,undefined4 param_3,int param_4,
                       undefined4 param_5,undefined4 param_6,int param_7)

{
  int iVar1;
  int iVar2;
  
  if ((param_1 == (int *)0x0) || (param_7 == 0)) {
    iVar1 = -0x7789f794;
  }
  else {
    iVar2 = param_4;
    if (param_4 == -1) {
      iVar2 = 0;
    }
    iVar1 = FUN__text__00527586(param_1,&param_2,&param_3,iVar2,&param_5,param_6);
    if ((-1 < iVar1) &&
       (iVar1 = (**(code **)(*param_1 + 0x58))
                          (param_1,param_2,param_3,iVar2,param_5,param_6,param_7), -1 < iVar1)) {
      iVar1 = 0;
    }
  }
  return iVar1;
}

