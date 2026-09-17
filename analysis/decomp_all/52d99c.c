
undefined4 * __thiscall FUN__text__0052d99c(undefined4 *param_1,byte param_2)

{
  undefined4 *puVar1;
  
  if ((param_2 & 2) == 0) {
    FUN__text__00428ad0(*param_1);
    puVar1 = param_1;
    if ((param_2 & 1) != 0) {
      FUN__text__00428ad0(param_1);
    }
  }
  else {
    puVar1 = param_1 + -1;
    FUN__text__0056de40(param_1,0xc,*puVar1,&LAB__text__0052d6d6);
    if ((param_2 & 1) != 0) {
      FUN__text__00428ad0(puVar1);
    }
  }
  return puVar1;
}

