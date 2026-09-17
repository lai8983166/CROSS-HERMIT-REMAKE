
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN__text__00539865(float *param_1,float param_2,float param_3,float param_4,float param_5,
                        float param_6,float param_7)

{
  float fVar1;
  float fVar2;
  float fVar3;
  float fVar4;
  
  fVar4 = _DAT_005d0e20;
  fVar3 = _DAT_005d0a40;
  fVar1 = _DAT_005d0a40 / (param_3 - param_2);
  fVar2 = _DAT_005d0a40 / (param_5 - param_4);
  *param_1 = fVar1 * _DAT_005d0e20;
  param_1[1] = 0.0;
  param_1[2] = 0.0;
  param_1[3] = 0.0;
  param_1[4] = 0.0;
  param_1[5] = fVar2 * fVar4;
  param_1[6] = 0.0;
  param_1[7] = 0.0;
  param_1[8] = 0.0;
  param_1[9] = 0.0;
  fVar3 = fVar3 / (param_7 - param_6);
  param_1[10] = fVar3;
  param_1[0xb] = 0.0;
  param_1[0xc] = -((param_2 + param_3) * fVar1);
  param_1[0xd] = -((param_4 + param_5) * fVar2);
  param_1[0xe] = -(fVar3 * param_6);
  param_1[0xf] = 1.0;
  return;
}

