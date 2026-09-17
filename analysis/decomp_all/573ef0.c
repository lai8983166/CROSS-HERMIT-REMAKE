
void FUN_00573ef0(char *param_1)

{
  char cVar1;
  int iVar2;
  uint uStack_10;
  char cStack_c;
  
  iVar2 = func_0x00584900((int)*param_1);
  if (iVar2 != 0x65) {
    do {
      param_1 = param_1 + 1;
      if (DAT_00764370 < 2) {
        uStack_10 = *(ushort *)(PTR_DAT_00764164 + *param_1 * 2) & 4;
      }
      else {
        uStack_10 = FUN_0057bb50((int)*param_1,4);
      }
    } while (uStack_10 != 0);
  }
  cStack_c = *param_1;
  *param_1 = DAT_00764374;
  do {
    param_1 = param_1 + 1;
    cVar1 = *param_1;
    *param_1 = cStack_c;
    cStack_c = cVar1;
  } while (*param_1 != '\0');
  return;
}

