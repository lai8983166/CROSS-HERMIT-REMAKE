
/* WARNING: Switch with 1 destination removed at 0x00537816 */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

float * FUN__text__0053780b(float *param_1,undefined4 param_2,int *param_3,undefined4 *param_4,
                           undefined4 *param_5,undefined4 *param_6)

{
  float fVar1;
  float fVar2;
  undefined4 *puVar3;
  undefined4 uStack_50;
  undefined4 uStack_4c;
  undefined4 uStack_48;
  undefined4 uStack_44;
  undefined4 uStack_40;
  undefined4 uStack_3c;
  undefined4 uStack_38;
  undefined4 uStack_34;
  undefined4 uStack_30;
  undefined4 uStack_2c;
  undefined4 uStack_28;
  undefined4 uStack_24;
  undefined4 uStack_20;
  undefined4 uStack_1c;
  undefined4 uStack_18;
  undefined4 uStack_14;
  undefined4 uStack_c;
  undefined4 uStack_8;
  
  uStack_8 = 1;
  uStack_c = 0x537815;
  FUN__text__00541e46();
  puVar3 = &uStack_50;
  switch(((param_6 != (undefined4 *)0x0) << 1 | param_5 != (undefined4 *)0x0) << 1 |
         param_4 != (undefined4 *)0x0) {
  case '\0':
    uStack_18 = 0;
    uStack_1c = 0;
    uStack_20 = 0;
    uStack_24 = 0;
    uStack_2c = 0;
    uStack_30 = 0;
    uStack_34 = 0;
    uStack_38 = 0;
    uStack_40 = 0;
    uStack_44 = 0;
    uStack_48 = 0;
    uStack_4c = 0;
    uStack_14 = 0x3f800000;
    uStack_28 = 0x3f800000;
    uStack_3c = 0x3f800000;
    uStack_50 = 0x3f800000;
    break;
  case '\x01':
    puVar3 = param_4;
    break;
  case '\x02':
    puVar3 = param_5;
    break;
  case '\x03':
    param_6 = param_5;
    goto LAB__text__0053ab0c;
  case '\x04':
    puVar3 = param_6;
    break;
  case '\x05':
    goto LAB__text__0053ab0c;
  case '\x06':
    param_4 = param_5;
    goto LAB__text__0053ab0c;
  case '\a':
    thunk_FUN__text__00554c90(&uStack_50,param_6,param_5);
    param_6 = &uStack_50;
LAB__text__0053ab0c:
    thunk_FUN__text__00554c90(&uStack_50,param_6,param_4);
  }
  thunk_FUN__text__00554ad0(param_1,param_2,puVar3);
  if (param_3 != (int *)0x0) {
    fVar2 = (float)param_3[2];
    if (param_3[2] < 0) {
      fVar2 = fVar2 + _DAT_005d0a44;
    }
    fVar1 = (float)*param_3;
    if (*param_3 < 0) {
      fVar1 = fVar1 + _DAT_005d0a44;
    }
    *param_1 = fVar1 + fVar2 * (*param_1 + _DAT_005d0a40) * _DAT_005d0a3c;
    fVar2 = (float)param_3[3];
    if (param_3[3] < 0) {
      fVar2 = fVar2 + _DAT_005d0a44;
    }
    fVar1 = (float)param_3[1];
    if (param_3[1] < 0) {
      fVar1 = fVar1 + _DAT_005d0a44;
    }
    param_1[1] = fVar1 + fVar2 * (1.0 - param_1[1]) * _DAT_005d0a3c;
    param_1[2] = ((float)param_3[5] - (float)param_3[4]) * param_1[2] + (float)param_3[4];
  }
  return param_1;
}

