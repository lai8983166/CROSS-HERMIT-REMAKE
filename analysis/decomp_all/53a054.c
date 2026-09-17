
/* WARNING: Switch with 1 destination removed at 0x0053a054 */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void thunk_FUN__text__0053a05a(float *param_1,float *param_2,float *param_3,float param_4)

{
  float fVar1;
  float *pfVar2;
  float10 fVar3;
  float10 fVar4;
  float10 fVar5;
  
  pfVar2 = param_2;
  fVar3 = (float10)1 - (float10)param_4;
  fVar5 = (float10)param_3[3] * (float10)param_2[3] +
          (float10)param_3[1] * (float10)param_2[1] +
          (float10)param_3[2] * (float10)param_2[2] + (float10)*param_2 * (float10)*param_3;
  if (fVar5 < (float10)_DAT_005d0a54) {
    param_2 = (float *)0xbf800000;
  }
  else {
    param_2 = (float *)0x3f800000;
  }
  fVar5 = (float10)(float)param_2 * fVar5;
  if ((float10)1 - fVar5 <= (float10)_DAT_005d1134) {
    fVar5 = (float10)param_4;
  }
  else {
    fVar4 = SQRT((float10)_DAT_005d0a40 - fVar5 * fVar5);
    fVar5 = (float10)fpatan(fVar4,(float10)(float)fVar5);
    fVar1 = (float)((float10)1 / fVar4);
    fVar3 = (float10)fsin((float10)(float)fVar5 * fVar3);
    fVar3 = fVar3 * (float10)fVar1;
    fVar5 = (float10)fsin((float10)(float)fVar5 * (float10)param_4);
    fVar5 = fVar5 * (float10)fVar1;
  }
  fVar5 = fVar5 * (float10)(float)param_2;
  *param_1 = (float)(fVar5 * (float10)*param_3 + fVar3 * (float10)*pfVar2);
  param_1[1] = (float)(fVar3 * (float10)pfVar2[1] + fVar5 * (float10)param_3[1]);
  param_1[2] = (float)(fVar3 * (float10)pfVar2[2] + fVar5 * (float10)param_3[2]);
  param_1[3] = (float)(fVar3 * (float10)pfVar2[3] + fVar5 * (float10)param_3[3]);
  return;
}

