
void FUN_00573fa0(char *param_1)

{
  char *pcVar1;
  char *pcStack_8;
  
  for (; (*param_1 != '\0' && (*param_1 != DAT_00764374)); param_1 = param_1 + 1) {
  }
  if (*param_1 != '\0') {
    do {
      pcVar1 = param_1;
      param_1 = pcVar1 + 1;
      if ((*param_1 == '\0') || (*param_1 == 'e')) break;
    } while (*param_1 != 'E');
    pcStack_8 = param_1;
    for (param_1 = pcVar1; *param_1 == '0'; param_1 = param_1 + -1) {
    }
    if (*param_1 == DAT_00764374) {
      param_1 = param_1 + -1;
    }
    do {
      param_1 = param_1 + 1;
      *param_1 = *pcStack_8;
      pcStack_8 = pcStack_8 + 1;
    } while (*param_1 != '\0');
  }
  return;
}

