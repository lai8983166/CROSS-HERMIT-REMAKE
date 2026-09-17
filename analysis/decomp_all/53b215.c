
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN__text__0053b215(float *param_1,undefined4 param_2)

{
  float fVar1;
  float fVar2;
  float fVar3;
  float fVar4;
  float local_14;
  float local_10;
  float local_c;
  float local_8;
  
  thunk_FUN__text__00554eb0(&local_14,param_2);
  fVar4 = _DAT_005d0a40;
  fVar1 = local_14 * _DAT_005d114c;
  fVar3 = local_10 * _DAT_005d114c;
  fVar2 = local_c * _DAT_005d114c;
  *param_1 = local_14 * fVar1 + _DAT_005d0a40;
  param_1[1] = fVar3 * local_14;
  param_1[2] = fVar2 * local_14;
  param_1[3] = 0.0;
  param_1[4] = local_10 * fVar1;
  param_1[5] = local_10 * fVar3 + fVar4;
  param_1[6] = fVar2 * local_10;
  param_1[7] = 0.0;
  param_1[8] = local_c * fVar1;
  param_1[9] = local_c * fVar3;
  param_1[10] = local_c * fVar2 + fVar4;
  param_1[0xb] = 0.0;
  param_1[0xc] = local_8 * fVar1;
  param_1[0xd] = local_8 * fVar3;
  param_1[0xe] = local_8 * fVar2;
  param_1[0xf] = 1.0;
  return;
}

