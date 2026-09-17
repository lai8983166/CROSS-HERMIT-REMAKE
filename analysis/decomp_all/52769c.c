
int FUN__text__0052769c(int *param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4,
                       undefined4 param_5,int param_6,undefined4 param_7,undefined4 param_8,
                       int param_9)

{
  int iVar1;
  int iVar2;
  
  if ((param_1 == (int *)0x0) || (param_9 == 0)) {
    iVar1 = -0x7789f794;
  }
  else {
    iVar2 = param_6;
    if (param_6 == -1) {
      iVar2 = 0;
    }
    iVar1 = FUN__text__005275ae(param_1,&param_2,&param_3,&param_4,&param_5,iVar2,&param_7,param_8);
    if ((-1 < iVar1) &&
       (iVar1 = (**(code **)(*param_1 + 0x54))
                          (param_1,param_2,param_3,param_4,param_5,iVar2,param_7,param_8,param_9),
       -1 < iVar1)) {
      iVar1 = 0;
    }
  }
  return iVar1;
}

