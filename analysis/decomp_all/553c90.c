
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

float * FUN__text__00553c90(float *param_1,float *param_2,float *param_3,float *param_4,
                           float *param_5,float param_6)

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
  float fVar11;
  float fVar12;
  float fVar13;
  float fVar14;
  float fVar15;
  float fVar16;
  
  fVar15 = param_6 * param_6;
  fVar16 = param_6 * fVar15;
  fVar11 = param_6 * _DAT_0075fe80 + _DAT_0075fe60 + fVar15 * _DAT_0075fe70 + fVar16 * _DAT_0075fe50
  ;
  fVar12 = param_6 * _UNK_0075fe84 + _UNK_0075fe64 + fVar15 * _UNK_0075fe74 + fVar16 * _UNK_0075fe54
  ;
  fVar13 = param_6 * _UNK_0075fe88 + _UNK_0075fe68 + fVar15 * _UNK_0075fe78 + fVar16 * _UNK_0075fe58
  ;
  fVar14 = param_6 * _UNK_0075fe8c + _UNK_0075fe6c + fVar15 * _UNK_0075fe7c + fVar16 * _UNK_0075fe5c
  ;
  fVar15 = param_2[1];
  fVar16 = param_2[2];
  fVar1 = param_2[3];
  fVar2 = param_3[1];
  fVar3 = param_3[2];
  fVar4 = param_3[3];
  fVar5 = param_4[1];
  fVar6 = param_4[2];
  fVar7 = param_4[3];
  fVar8 = param_5[1];
  fVar9 = param_5[2];
  fVar10 = param_5[3];
  *param_1 = *param_2 * fVar11 + *param_3 * fVar12 + *param_4 * fVar13 + *param_5 * fVar14;
  param_1[1] = fVar15 * fVar11 + fVar2 * fVar12 + fVar5 * fVar13 + fVar8 * fVar14;
  param_1[2] = fVar16 * fVar11 + fVar3 * fVar12 + fVar6 * fVar13 + fVar9 * fVar14;
  param_1[3] = fVar1 * fVar11 + fVar4 * fVar12 + fVar7 * fVar13 + fVar10 * fVar14;
  return param_1;
}

