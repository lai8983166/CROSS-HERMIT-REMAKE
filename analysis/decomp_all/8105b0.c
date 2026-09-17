
undefined4 * __thiscall
FUN__text1__008105b0(undefined4 *param_1,undefined4 param_2,int param_3,undefined1 param_4)

{
  *(undefined1 *)((int)param_1 + 0x16) = param_4;
  param_1[3] = param_2;
  param_1[2] = param_2;
  if (*(char *)((int)param_1 + 0x16) != '\0') {
    *(undefined1 *)param_1[3] = 0;
  }
  param_1[4] = param_1[2] + param_3;
  *(undefined1 *)((int)param_1 + 0x15) = 0;
  *(undefined1 *)(param_1 + 5) = 0x80;
  *param_1 = param_1[3];
  *(undefined1 *)(param_1 + 1) = *(undefined1 *)(param_1 + 5);
  return param_1;
}

