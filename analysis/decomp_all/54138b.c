
void FUN__text__0054138b(int *param_1,int param_2,int param_3)

{
  int *piVar1;
  int iVar2;
  int iVar3;
  
  param_1[1] = 0;
  if (param_2 != 0x3d) {
    *(undefined4 *)(*param_1 + 0x14) = 10;
    *(undefined4 *)(*param_1 + 0x18) = 0x3d;
    *(int *)(*param_1 + 0x1c) = param_2;
    (**(code **)*param_1)(param_1);
  }
  if (param_3 != 0x1a8) {
    *(undefined4 *)(*param_1 + 0x14) = 0x13;
    *(undefined4 *)(*param_1 + 0x18) = 0x1a8;
    *(int *)(*param_1 + 0x1c) = param_3;
    (**(code **)*param_1)(param_1);
  }
  iVar3 = *param_1;
  piVar1 = param_1;
  for (iVar2 = 0x6a; iVar2 != 0; iVar2 = iVar2 + -1) {
    *piVar1 = 0;
    piVar1 = piVar1 + 1;
  }
  *param_1 = iVar3;
  *(undefined1 *)(param_1 + 3) = 1;
  FUN__text__0054a422(param_1);
  param_1[2] = 0;
  param_1[5] = 0;
  param_1[0x24] = 0;
  param_1[0x25] = 0;
  param_1[0x26] = 0;
  param_1[0x27] = 0;
  iVar3 = 4;
  piVar1 = param_1 + 0x2c;
  do {
    piVar1[-4] = 0;
    *piVar1 = 0;
    piVar1 = piVar1 + 1;
    iVar3 = iVar3 + -1;
  } while (iVar3 != 0);
  FUN__text__0054358d(param_1);
  FUN__text__00549a6c(param_1);
  if (DAT_0075edd8 == '\x02') {
    DAT_0075edd8 = FUN__text__00549562();
  }
  param_1[4] = 200;
  return;
}

