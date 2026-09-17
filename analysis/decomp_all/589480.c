
uint FUN__text__00589480(uint param_1,int *param_2)

{
  code *pcVar1;
  int iVar2;
  uint uVar3;
  
  if ((param_2 == (int *)0x0) &&
     (iVar2 = FUN__text__00573780(2,"ungetc.c",0x60,0,"str != NULL"), iVar2 == 1)) {
    pcVar1 = (code *)swi(3);
    uVar3 = (*pcVar1)();
    return uVar3;
  }
  if ((param_1 == 0xffffffff) ||
     (((param_2[3] & 1U) == 0 && (((param_2[3] & 0x80U) == 0 || ((param_2[3] & 2U) != 0)))))) {
    param_1 = 0xffffffff;
  }
  else {
    if (param_2[2] == 0) {
      FUN__text__00585b90(param_2);
    }
    if (*param_2 == param_2[2]) {
      if (param_2[1] != 0) {
        return 0xffffffff;
      }
      *param_2 = *param_2 + 1;
    }
    if ((param_2[3] & 0x40U) == 0) {
      *param_2 = *param_2 + -1;
      *(char *)*param_2 = (char)param_1;
    }
    else {
      *param_2 = *param_2 + -1;
      if (*(char *)*param_2 != (char)param_1) {
        *param_2 = *param_2 + 1;
        return 0xffffffff;
      }
    }
    param_2[1] = param_2[1] + 1;
    param_2[3] = param_2[3] & 0xffffffef;
    param_2[3] = param_2[3] | 1;
    param_1 = param_1 & 0xff;
  }
  return param_1;
}

