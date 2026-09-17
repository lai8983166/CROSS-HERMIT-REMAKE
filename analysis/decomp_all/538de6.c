
/* WARNING: Switch with 1 destination removed at 0x00538de6 */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined4 *
thunk_FUN__text__0053ae87
          (undefined4 *param_1,float *param_2,int param_3,undefined4 *param_4,float *param_5,
          int param_6,float *param_7)

{
  undefined4 uVar1;
  undefined4 uStack_d0;
  undefined4 uStack_cc;
  undefined4 uStack_c8;
  undefined4 uStack_c4;
  undefined4 uStack_c0;
  undefined4 uStack_bc;
  undefined4 uStack_b8;
  undefined4 uStack_b4;
  undefined4 uStack_b0;
  undefined4 uStack_ac;
  undefined4 uStack_a8;
  undefined4 uStack_a4;
  undefined4 uStack_a0;
  undefined4 uStack_9c;
  undefined4 uStack_98;
  undefined4 uStack_94;
  undefined1 auStack_90 [64];
  undefined1 auStack_50 [76];
  
  if (param_4 == (undefined4 *)0x0) {
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
    param_1[0xf] = 0x3f800000;
    param_1[10] = 0x3f800000;
    param_1[5] = 0x3f800000;
    *param_1 = 0x3f800000;
  }
  else if (param_3 == 0) {
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
    *param_1 = *param_4;
    param_1[5] = param_4[1];
    uVar1 = param_4[2];
    param_1[0xf] = 0x3f800000;
    param_1[10] = uVar1;
  }
  else {
    uStack_98 = 0;
    uStack_d0 = *param_4;
    uStack_9c = 0;
    uStack_bc = param_4[1];
    uStack_a0 = 0;
    uStack_a8 = param_4[2];
    uStack_a4 = 0;
    uStack_ac = 0;
    uStack_b0 = 0;
    uStack_b4 = 0;
    uStack_b8 = 0;
    uStack_c0 = 0;
    uStack_c4 = 0;
    uStack_c8 = 0;
    uStack_cc = 0;
    uStack_94 = 0x3f800000;
    thunk_FUN__text__00538cbf(auStack_90,param_3);
    if (param_2 == (float *)0x0) {
      thunk_FUN__text__005380d5(param_1,auStack_90);
      thunk_FUN__text__00554c90(param_1,param_1,&uStack_d0);
      thunk_FUN__text__00554c90(param_1,param_1,auStack_90);
    }
    else {
      thunk_FUN__text__005380d5(auStack_50,auStack_90);
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
      param_1[0xf] = 0x3f800000;
      param_1[10] = 0x3f800000;
      param_1[5] = 0x3f800000;
      *param_1 = 0x3f800000;
      param_1[0xc] = -*param_2;
      param_1[0xd] = -param_2[1];
      param_1[0xe] = -param_2[2];
      thunk_FUN__text__00554c90(param_1,param_1,auStack_50);
      thunk_FUN__text__00554c90(param_1,param_1,&uStack_d0);
      thunk_FUN__text__00554c90(param_1,param_1,auStack_90);
      param_1[0xc] = (float)param_1[0xc] + *param_2;
      param_1[0xd] = param_2[1] + (float)param_1[0xd];
      param_1[0xe] = (float)param_1[0xe] + param_2[2];
    }
  }
  if (param_6 != 0) {
    thunk_FUN__text__00538cbf(auStack_90,param_6);
    if (param_5 == (float *)0x0) {
      thunk_FUN__text__00554c90(param_1,param_1,auStack_90);
    }
    else {
      param_1[0xc] = (float)param_1[0xc] - *param_5;
      param_1[0xd] = (float)param_1[0xd] - param_5[1];
      param_1[0xe] = (float)param_1[0xe] - param_5[2];
      thunk_FUN__text__00554c90(param_1,param_1,auStack_90);
      param_1[0xc] = (float)param_1[0xc] + *param_5;
      param_1[0xd] = (float)param_1[0xd] + param_5[1];
      param_1[0xe] = (float)param_1[0xe] + param_5[2];
    }
  }
  if (param_7 != (float *)0x0) {
    param_1[0xc] = (float)param_1[0xc] + *param_7;
    param_1[0xd] = param_7[1] + (float)param_1[0xd];
    param_1[0xe] = param_7[2] + (float)param_1[0xe];
  }
  return param_1;
}

