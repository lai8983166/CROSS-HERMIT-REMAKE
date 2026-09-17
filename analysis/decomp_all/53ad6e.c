
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN__text__0053ad6e(float *param_1,float *param_2)

{
  float *pfVar1;
  float fVar2;
  int iVar3;
  float local_14;
  float local_10;
  float local_c;
  float local_8;
  
  fVar2 = param_2[3] * param_2[3] +
          param_2[2] * param_2[2] + param_2[1] * param_2[1] + *param_2 * *param_2;
  iVar3 = FUN__text__0053717b(fVar2,0x3f800000);
  if (iVar3 == 0) {
    if (fVar2 <= (float)PTR_DAT_005d1144) {
      *param_1 = 0.0;
      param_1[1] = 0.0;
      param_1[2] = 0.0;
      param_1[3] = 0.0;
      return;
    }
    fVar2 = _DAT_005d0a40 / SQRT(fVar2);
    local_14 = fVar2 * *param_2;
    local_10 = fVar2 * param_2[1];
    local_c = fVar2 * param_2[2];
    pfVar1 = param_2 + 3;
    param_2 = &local_14;
    local_8 = fVar2 * *pfVar1;
  }
  else if (param_1 == param_2) {
    return;
  }
  *param_1 = *param_2;
  param_1[1] = param_2[1];
  param_1[2] = param_2[2];
  param_1[3] = param_2[3];
  return;
}

