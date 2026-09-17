
void FUN__text__00554de0(float *param_1,float *param_2)

{
  float fVar1;
  float fVar2;
  float fVar3;
  float fVar4;
  float fVar5;
  undefined1 auVar6 [16];
  
  fVar1 = *param_2;
  fVar2 = param_2[1];
  fVar3 = param_2[2];
  fVar4 = fVar1 * fVar1 + fVar2 * fVar2 + fVar3 * fVar3;
  if (fVar4 < DAT_0080c180) {
    *param_1 = 0.0;
    param_1[1] = 0.0;
    param_1[2] = 0.0;
    return;
  }
  auVar6 = rsqrtss(ZEXT416((uint)fVar4),ZEXT416((uint)fVar4));
  fVar5 = auVar6._0_4_;
  fVar4 = DAT_0080c184 * fVar5 * (DAT_0080c188 - fVar4 * fVar5 * fVar5);
  *param_1 = fVar4 * fVar1;
  param_1[1] = fVar4 * fVar2;
  param_1[2] = fVar4 * fVar3;
  return;
}

