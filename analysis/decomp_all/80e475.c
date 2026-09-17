
bool FUN__text1__0080e475(undefined4 param_1,undefined4 *param_2,uint param_3)

{
  undefined4 uVar1;
  char cVar2;
  void *pvVar3;
  bool local_10;
  
  uVar1 = *param_2;
  pvVar3 = operator_new(param_3);
  cVar2 = FUN__text1__0080e089(param_1,pvVar3,param_2);
  if (cVar2 == '\0') {
    *param_2 = uVar1;
  }
  else {
    FUN__text1__00848490(param_1,pvVar3,*param_2);
  }
  local_10 = cVar2 != '\0';
  FUN__text1__00848476(pvVar3);
  return local_10;
}

