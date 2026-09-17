
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN__text__0053a5b9(float *param_1,float *param_2,float param_3)

{
  float fVar1;
  
  fVar1 = param_2[1] * _DAT_005d0a4c + param_2[2] * _DAT_005d0a50 + *param_2 * _DAT_005d0a48;
  *param_1 = (*param_2 - fVar1) * param_3 + fVar1;
  param_1[1] = (param_2[1] - fVar1) * param_3 + fVar1;
  param_1[2] = (param_2[2] - fVar1) * param_3 + fVar1;
  param_1[3] = param_2[3];
  return;
}

