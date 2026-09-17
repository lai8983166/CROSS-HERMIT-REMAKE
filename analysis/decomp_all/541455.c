
void FUN__text__00541455(int *param_1,int param_2,undefined4 param_3)

{
  if (param_2 == 0xfe) {
    *(undefined4 *)(param_1[100] + 0xc) = param_3;
    return;
  }
  if ((0xdf < param_2) && (param_2 < 0xf0)) {
    *(undefined4 *)(param_1[100] + -0x370 + param_2 * 4) = param_3;
    return;
  }
  *(undefined4 *)(*param_1 + 0x14) = 0x43;
  *(int *)(*param_1 + 0x18) = param_2;
  (**(code **)*param_1)(param_1);
  return;
}

