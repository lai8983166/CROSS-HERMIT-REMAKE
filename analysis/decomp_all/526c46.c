
int * FUN__text__00526c46(int param_1)

{
  int *piVar1;
  
  piVar1 = &DAT_005d03c8;
  while( true ) {
    if (PTR_DAT_0075dda4 <= piVar1) {
      return &DAT_005d03a0;
    }
    if (param_1 == *piVar1) break;
    piVar1 = piVar1 + 9;
  }
  return piVar1;
}

