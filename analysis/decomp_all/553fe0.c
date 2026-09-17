
undefined8 *
FUN__text__00553fe0(undefined8 *param_1,undefined8 *param_2,undefined8 *param_3,undefined8 *param_4,
                   float param_5,float param_6)

{
  float fVar1;
  float fVar2;
  
  fVar1 = (float)*param_2;
  fVar2 = (float)((ulonglong)*param_2 >> 0x20);
  *param_1 = CONCAT44(((float)((ulonglong)*param_3 >> 0x20) - fVar2) * param_5 + fVar2 +
                      ((float)((ulonglong)*param_4 >> 0x20) - fVar2) * param_6,
                      ((float)*param_3 - fVar1) * param_5 + fVar1 +
                      ((float)*param_4 - fVar1) * param_6);
  return param_1;
}

