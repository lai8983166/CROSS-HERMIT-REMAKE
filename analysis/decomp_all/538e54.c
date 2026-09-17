
undefined4 *
FUN__text__00538e54(undefined4 *param_1,undefined4 param_2,float *param_3,int param_4,float *param_5
                   )

{
  undefined1 local_50 [76];
  
  param_1[0xe] = 0;
  param_1[0xd] = 0;
  param_1[0xc] = 0;
  param_1[0xb] = 0;
  param_1[9] = 0;
  param_1[8] = 0;
  param_1[7] = 0;
  param_1[6] = 0;
  param_1[4] = 0;
  param_1[3] = 0;
  param_1[2] = 0;
  param_1[1] = 0;
  *param_1 = param_2;
  param_1[5] = param_2;
  param_1[10] = param_2;
  param_1[0xf] = 0x3f800000;
  if (param_4 != 0) {
    thunk_FUN__text__00538cbf(local_50,param_4);
    if (param_3 == (float *)0x0) {
      thunk_FUN__text__00554c90(param_1,param_1,local_50);
    }
    else {
      param_1[0xc] = (float)param_1[0xc] - *param_3;
      param_1[0xd] = (float)param_1[0xd] - param_3[1];
      param_1[0xe] = (float)param_1[0xe] - param_3[2];
      thunk_FUN__text__00554c90(param_1,param_1,local_50);
      param_1[0xc] = *param_3 + (float)param_1[0xc];
      param_1[0xd] = (float)param_1[0xd] + param_3[1];
      param_1[0xe] = param_3[2] + (float)param_1[0xe];
    }
  }
  if (param_5 != (float *)0x0) {
    param_1[0xc] = *param_5 + (float)param_1[0xc];
    param_1[0xd] = param_5[1] + (float)param_1[0xd];
    param_1[0xe] = param_5[2] + (float)param_1[0xe];
  }
  return param_1;
}

