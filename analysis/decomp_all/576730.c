
void FUN_00576730(char *param_1,int param_2,undefined4 param_3,int *param_4)

{
  char cVar1;
  
  do {
    if (param_2 < 1) {
      return;
    }
    cVar1 = *param_1;
    param_1 = param_1 + 1;
    FUN_00576670((int)cVar1,param_3,param_4);
    param_2 = param_2 + -1;
  } while (*param_4 != -1);
  return;
}

