
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN__text__0053d261(float *param_1,float *param_2,int param_3,int param_4)

{
  float fVar1;
  float fVar2;
  
  fVar1 = _DAT_005d0a3c;
  if (param_3 == 2) {
    fVar2 = SQRT(param_2[2] * _DAT_005d0a3c + _DAT_005d0a3c);
    param_1[2] = fVar2;
    fVar1 = fVar1 / fVar2;
    *param_1 = fVar1 * *param_2;
    param_1[1] = fVar1 * param_2[1];
    return;
  }
  if (param_3 == 3) {
    *param_1 = *param_2;
    param_1[1] = param_2[1];
    if (param_4 != 0) goto LAB__text__0053d2b4;
  }
  else {
    if (param_3 != 4) {
      return;
    }
    if (param_4 != 0) {
      fVar1 = _DAT_005d0a3c / (_DAT_005d0a3c - param_2[2] * _DAT_005d0a3c);
      *param_1 = fVar1 * *param_2;
      param_1[1] = fVar1 * param_2[1];
LAB__text__0053d2b4:
      param_1[2] = -param_2[2];
      return;
    }
    fVar1 = _DAT_005d0a3c / ((param_2[2] + _DAT_005d0a40) * _DAT_005d0a3c);
    *param_1 = fVar1 * *param_2;
    param_1[1] = fVar1 * param_2[1];
  }
  param_1[2] = param_2[2];
  return;
}

