
/* WARNING: Switch with 1 destination removed at 0x00539e37 */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

float * thunk_FUN__text__00539e3d(float *param_1,float *param_2)

{
  float fVar1;
  int iVar2;
  float *extraout_ECX;
  
  fVar1 = param_2[3] * param_2[3] +
          param_2[2] * param_2[2] + param_2[1] * param_2[1] + *param_2 * *param_2;
  if (fVar1 <= _DAT_005d1148) {
    *param_1 = 0.0;
    param_1[1] = 0.0;
    param_1[2] = 0.0;
    fVar1 = 0.0;
  }
  else {
    *param_1 = -*param_2;
    param_1[1] = -param_2[1];
    param_1[2] = -param_2[2];
    param_1[3] = param_2[3];
    iVar2 = FUN__text__0053717b(fVar1,0x3f800000);
    if (iVar2 != 0) {
      return extraout_ECX;
    }
    fVar1 = 1.0 / fVar1;
    *extraout_ECX = fVar1 * *extraout_ECX;
    extraout_ECX[1] = fVar1 * extraout_ECX[1];
    extraout_ECX[2] = fVar1 * extraout_ECX[2];
    fVar1 = fVar1 * extraout_ECX[3];
    param_1 = extraout_ECX;
  }
  param_1[3] = fVar1;
  return param_1;
}

