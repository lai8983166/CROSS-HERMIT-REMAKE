
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined8 *
FUN__text__00553c00(undefined8 *param_1,undefined8 *param_2,undefined8 *param_3,undefined8 *param_4,
                   undefined8 *param_5,float param_6)

{
  float fVar1;
  float fVar2;
  float fVar3;
  float fVar4;
  float fVar5;
  
  fVar4 = param_6 * param_6;
  fVar5 = param_6 * fVar4;
  fVar1 = param_6 * _DAT_0075fe80 + _DAT_0075fe60 + fVar4 * _DAT_0075fe70 + fVar5 * _DAT_0075fe50;
  fVar2 = param_6 * _UNK_0075fe84 + _UNK_0075fe64 + fVar4 * _UNK_0075fe74 + fVar5 * _UNK_0075fe54;
  fVar3 = param_6 * _UNK_0075fe88 + _UNK_0075fe68 + fVar4 * _UNK_0075fe78 + fVar5 * _UNK_0075fe58;
  fVar4 = param_6 * _UNK_0075fe8c + _UNK_0075fe6c + fVar4 * _UNK_0075fe7c + fVar5 * _UNK_0075fe5c;
  *param_1 = CONCAT44((float)((ulonglong)*param_2 >> 0x20) * fVar1 +
                      (float)((ulonglong)*param_4 >> 0x20) * fVar3 +
                      (float)((ulonglong)*param_3 >> 0x20) * fVar2 +
                      (float)((ulonglong)*param_5 >> 0x20) * fVar4,
                      (float)*param_2 * fVar1 + (float)*param_4 * fVar3 +
                      (float)*param_3 * fVar2 + (float)*param_5 * fVar4);
  return param_1;
}

