
undefined4 __fastcall FUN_0053b8db(int *param_1)

{
  code *pcVar1;
  undefined4 in_EAX;
  
  if (*param_1 != -1) {
    if (param_1[2] != 0) {
      (*DAT_005922a8)(param_1[2]);
      param_1[2] = 0;
      param_1[3] = 0;
    }
    pcVar1 = DAT_00592270;
    if (param_1[1] != -1) {
      (*DAT_00592270)(param_1[1]);
      param_1[1] = -1;
    }
    if (*param_1 != -1) {
      (*pcVar1)(*param_1);
      *param_1 = -1;
    }
    return 0;
  }
  return in_EAX;
}

