
void FUN__text__0054ab15(int *param_1)

{
  int iVar1;
  int iVar2;
  
  iVar1 = param_1[0x5f];
  if (param_1[4] != 0xcf) {
    *(undefined4 *)(*param_1 + 0x14) = 0x12;
    *(int *)(*param_1 + 0x18) = param_1[4];
    (**(code **)*param_1)(param_1);
  }
  if (((*(char *)((int)param_1 + 0x4a) == '\0') || (*(char *)((int)param_1 + 0x59) == '\0')) ||
     (param_1[0x1d] == 0)) {
    *(undefined4 *)(*param_1 + 0x14) = 0x2d;
    (**(code **)*param_1)(param_1);
  }
  else {
    iVar2 = *(int *)(iVar1 + 0x18);
    param_1[0x69] = iVar2;
    (**(code **)(iVar2 + 0xc))(param_1);
    *(undefined1 *)(iVar1 + 8) = 0;
  }
  return;
}

