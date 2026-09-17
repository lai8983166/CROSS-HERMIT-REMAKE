
bool FUN__text1__0080e9cd(undefined4 param_1,undefined4 *param_2,uint param_3)

{
  char cVar1;
  void *pvVar2;
  
  pvVar2 = operator_new(param_3);
  cVar1 = FUN__text1__0080e874(param_1,pvVar2,param_2,param_3);
  if (cVar1 != '\0') {
    FUN__text1__00848490(param_1,pvVar2,*param_2);
    FUN__text1__00848476(pvVar2);
  }
  return cVar1 != '\0';
}

