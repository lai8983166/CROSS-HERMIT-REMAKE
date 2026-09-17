
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

float10 FUN__text__0053a65a(float param_1,float param_2)

{
  float fVar1;
  float fVar2;
  float fVar3;
  float10 fVar4;
  float10 fVar5;
  float10 fVar6;
  
  if ((float)PTR_DAT_005d1144 <= param_1) {
    fVar4 = (float10)param_1 * (float10)param_1;
    fVar5 = ABS(((float10)param_2 * (float10)param_2 - (float10)_DAT_005d0a40) + fVar4);
    fVar1 = (float)fVar5;
    fVar5 = SQRT(fVar5);
    fVar6 = fVar5 * (float10)param_1 * (float10)_DAT_005d0e20;
    fVar2 = (float)((((float10)fVar1 - fVar6) + fVar4) / (fVar6 + (float10)fVar1 + fVar4));
    fVar6 = (float10)1 - fVar4;
    fVar3 = (float)((fVar6 / (float10)param_1) * fVar5 * (float10)_DAT_005d0e20);
    fVar4 = (((((float10)fVar1 - (float10)fVar3) +
              (float10)(float)fVar6 * (float10)(float)fVar6 * ((float10)1 / fVar4)) * (float10)fVar2
             ) / ((float10)(float)fVar6 * (float10)(float)fVar6 * ((float10)1 / fVar4) +
                  (float10)fVar3 + (float10)fVar1) + (float10)fVar2) * (float10)_DAT_005d0a3c;
    if ((float10)_DAT_005d0a40 < fVar4) {
      fVar4 = (float10)1;
    }
    if (fVar4 < (float10)_DAT_005d0a54) {
      fVar4 = (float10)0;
    }
  }
  else {
    fVar4 = (float10)_DAT_005d0a40;
  }
  return fVar4;
}

