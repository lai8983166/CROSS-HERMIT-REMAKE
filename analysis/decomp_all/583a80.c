
void FUN__text__00583a80(undefined2 *param_1,int param_2,undefined4 param_3,int *param_4)

{
  undefined2 uVar1;
  
  do {
    if (param_2 < 1) {
      return;
    }
    uVar1 = *param_1;
    param_1 = param_1 + 1;
    FUN__text__00583a00(uVar1,param_3,param_4);
    param_2 = param_2 + -1;
  } while (*param_4 != -1);
  return;
}

