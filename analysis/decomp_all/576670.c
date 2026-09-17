
void __thiscall FUN_00576670(undefined4 param_1,uint param_2,int *param_3,int *param_4)

{
  param_3[1] = param_3[1] + -1;
  if (param_3[1] < 0) {
    param_2 = FUN_005756c0(param_2,param_3,param_1);
  }
  else {
    *(undefined1 *)*param_3 = (undefined1)param_2;
    param_2 = param_2 & 0xff;
    *param_3 = *param_3 + 1;
  }
  if (param_2 == 0xffffffff) {
    *param_4 = -1;
  }
  else {
    *param_4 = *param_4 + 1;
  }
  return;
}

