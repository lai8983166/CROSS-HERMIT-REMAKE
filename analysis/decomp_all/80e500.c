
bool FUN__text1__0080e500(undefined4 param_1,undefined4 *param_2,uint param_3)

{
  char cVar1;
  void *pvVar2;
  
  pvVar2 = operator_new(param_3);
  FUN__text1__008103c7(param_1,pvVar2,param_2,param_3);
  FUN__text1__0080e59a(pvVar2,param_1,*param_2);
  FUN__text1__0080e679(param_1,pvVar2,param_2);
  cVar1 = FUN__text1__0080e874(pvVar2,param_1,param_2,param_3);
  if (cVar1 != '\0') {
    FUN__text1__00848476(pvVar2);
  }
  return cVar1 != '\0';
}

