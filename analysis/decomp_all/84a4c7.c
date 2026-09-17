
int * FUN__text1__0084a4c7(int param_1)

{
  int *piVar1;
  
  piVar1 = &DAT_00870480;
  if (DAT_00870480 != param_1) {
    do {
      piVar1 = piVar1 + 3;
      if (&DAT_00870480 + DAT_00870500 * 3 <= piVar1) break;
    } while (*piVar1 != param_1);
  }
  if ((&DAT_00870480 + DAT_00870500 * 3 <= piVar1) || (*piVar1 != param_1)) {
    piVar1 = (int *)0x0;
  }
  return piVar1;
}

