
int FUN__text__005858f0(int *param_1)

{
  int iVar1;
  
  if (((*(int *)*param_1 == -0x1f928c9d) && (*(int *)(*param_1 + 0x10) == 3)) &&
     (*(int *)(*param_1 + 0x14) == 0x19930520)) {
    FUN__text__00575580();
  }
  if ((DAT_0080a6ac != (_func_int *)0x0) && (iVar1 = _ValidateExecute(DAT_0080a6ac), iVar1 != 0)) {
    iVar1 = (*DAT_0080a6ac)(param_1);
    return iVar1;
  }
  return 0;
}

