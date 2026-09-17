
/* WARNING: Switch with 1 destination removed at 0x00539f8f */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

float * thunk_FUN__text__00539f95(float *param_1,float *param_2)

{
  float10 fVar1;
  float fVar2;
  int iVar3;
  float *extraout_ECX;
  float10 fVar4;
  
  fVar2 = SQRT(param_2[2] * param_2[2] + param_2[1] * param_2[1] + *param_2 * *param_2);
  fVar4 = (float10)fVar2;
  fVar1 = (float10)fcos(fVar4);
  fVar4 = (float10)fsin(fVar4);
  param_1[3] = (float)fVar1;
  iVar3 = FUN__text__0053717b((float)fVar4,0);
  if (iVar3 == 0) {
    fVar2 = (float)fVar4 / fVar2;
    *param_1 = fVar2 * *extraout_ECX;
    param_1[1] = fVar2 * extraout_ECX[1];
    param_1[2] = fVar2 * extraout_ECX[2];
  }
  else if (param_1 != extraout_ECX) {
    *param_1 = *extraout_ECX;
    param_1[1] = extraout_ECX[1];
    param_1[2] = extraout_ECX[2];
  }
  return param_1;
}

