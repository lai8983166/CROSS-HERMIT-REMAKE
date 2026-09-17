
undefined1 FUN__text__0053ba56(int *param_1,int *param_2)

{
  int iVar1;
  int iVar2;
  int iVar3;
  
  iVar3 = 4;
  do {
    if (iVar3 == 0) {
      return 1;
    }
    iVar3 = iVar3 + -1;
    iVar2 = *param_2;
    iVar1 = *param_1;
    param_1 = param_1 + 1;
    param_2 = param_2 + 1;
  } while (iVar1 == iVar2);
  return 0;
}

