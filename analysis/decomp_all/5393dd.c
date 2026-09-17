
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN__text__005393dd(float *param_1,float param_2,float param_3,float param_4,float param_5)

{
  float10 fVar1;
  float10 fVar2;
  
  fVar1 = (float10)fcos((float10)(param_2 * _DAT_005d0a3c));
  fVar2 = (float10)fsin((float10)(param_2 * _DAT_005d0a3c));
  *param_1 = ((float)fVar1 / (float)fVar2) / param_3;
  param_1[1] = 0.0;
  param_1[2] = 0.0;
  param_1[3] = 0.0;
  param_1[4] = 0.0;
  param_1[5] = (float)fVar1 / (float)fVar2;
  param_1[6] = 0.0;
  param_1[7] = 0.0;
  param_1[8] = 0.0;
  param_1[9] = 0.0;
  param_5 = param_5 / (param_5 - param_4);
  param_1[10] = param_5;
  param_1[0xb] = 1.0;
  param_1[0xc] = 0.0;
  param_1[0xd] = 0.0;
  param_1[0xe] = -(param_5 * param_4);
  param_1[0xf] = 0.0;
  return;
}

