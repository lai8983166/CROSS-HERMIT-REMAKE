
float * FUN__text__00553f90(float *param_1,float *param_2,float *param_3,float *param_4,
                           float param_5,float param_6)

{
  float fVar1;
  float fVar2;
  float fVar3;
  float fVar4;
  float fVar5;
  float fVar6;
  float fVar7;
  float fVar8;
  float fVar9;
  float fVar10;
  
  fVar1 = *param_2;
  fVar2 = param_2[1];
  fVar3 = param_2[2];
  fVar4 = param_2[3];
  fVar5 = param_3[1];
  fVar6 = param_3[2];
  fVar7 = param_3[3];
  fVar8 = param_4[1];
  fVar9 = param_4[2];
  fVar10 = param_4[3];
  *param_1 = (*param_3 - fVar1) * param_5 + fVar1 + (*param_4 - fVar1) * param_6;
  param_1[1] = (fVar5 - fVar2) * param_5 + fVar2 + (fVar8 - fVar2) * param_6;
  param_1[2] = (fVar6 - fVar3) * param_5 + fVar3 + (fVar9 - fVar3) * param_6;
  param_1[3] = (fVar7 - fVar4) * param_5 + fVar4 + (fVar10 - fVar4) * param_6;
  return param_1;
}

