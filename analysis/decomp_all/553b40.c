
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined8 *
FUN__text__00553b40(undefined8 *param_1,undefined8 *param_2,undefined8 *param_3,undefined8 *param_4,
                   undefined8 *param_5,float param_6)

{
  float fVar1;
  float fVar2;
  float fVar3;
  float fVar4;
  float fVar5;
  float fVar6;
  float fVar7;
  float fVar8;
  
  fVar7 = param_6 * param_6;
  fVar8 = param_6 * fVar7;
  fVar3 = param_6 * _DAT_0075fe80 + _DAT_0075fe60 + fVar7 * _DAT_0075fe70 + fVar8 * _DAT_0075fe50;
  fVar4 = param_6 * _UNK_0075fe84 + _UNK_0075fe64 + fVar7 * _UNK_0075fe74 + fVar8 * _UNK_0075fe54;
  fVar5 = param_6 * _UNK_0075fe88 + _UNK_0075fe68 + fVar7 * _UNK_0075fe78 + fVar8 * _UNK_0075fe58;
  fVar6 = param_6 * _UNK_0075fe8c + _UNK_0075fe6c + fVar7 * _UNK_0075fe7c + fVar8 * _UNK_0075fe5c;
  fVar7 = *(float *)(param_2 + 1);
  fVar8 = *(float *)(param_3 + 1);
  fVar1 = *(float *)(param_4 + 1);
  fVar2 = *(float *)(param_5 + 1);
  *param_1 = CONCAT44((float)((ulonglong)*param_2 >> 0x20) * fVar3 +
                      (float)((ulonglong)*param_3 >> 0x20) * fVar4 +
                      (float)((ulonglong)*param_4 >> 0x20) * fVar5 +
                      (float)((ulonglong)*param_5 >> 0x20) * fVar6,
                      (float)*param_2 * fVar3 + (float)*param_3 * fVar4 + (float)*param_4 * fVar5 +
                      (float)*param_5 * fVar6);
  *(float *)(param_1 + 1) = fVar7 * fVar3 + fVar8 * fVar4 + fVar1 * fVar5 + fVar2 * fVar6;
  return param_1;
}

