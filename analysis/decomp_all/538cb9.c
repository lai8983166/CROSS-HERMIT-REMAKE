
/* WARNING: Switch with 1 destination removed at 0x00538cb9 */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void thunk_FUN__text__00538cbf(float *param_1,float *param_2)

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
  
  fVar10 = *param_2 * _DAT_005d0e20;
  fVar11 = param_2[1] * _DAT_005d0e20;
  fVar12 = _DAT_005d0e20 * param_2[2];
  fVar9 = fVar10 * param_2[3];
  fVar1 = param_2[3];
  fVar2 = param_2[3];
  fVar3 = *param_2;
  fVar4 = *param_2;
  fVar5 = *param_2;
  fVar6 = param_2[1];
  fVar7 = param_2[1];
  fVar8 = param_2[2];
  *param_1 = (1.0 - fVar11 * fVar6) - fVar12 * fVar8;
  param_1[1] = fVar11 * fVar4 + fVar12 * fVar2;
  param_1[2] = fVar12 * fVar5 - fVar11 * fVar1;
  param_1[3] = 0.0;
  param_1[4] = fVar11 * fVar4 - fVar12 * fVar2;
  fVar2 = 1.0 - fVar10 * fVar3;
  param_1[5] = fVar2 - fVar12 * fVar8;
  param_1[6] = fVar12 * fVar7 + fVar9;
  param_1[7] = 0.0;
  param_1[8] = fVar12 * fVar5 + fVar11 * fVar1;
  param_1[9] = fVar12 * fVar7 - fVar9;
  param_1[10] = fVar2 - fVar11 * fVar6;
  param_1[0xb] = 0.0;
  param_1[0xc] = 0.0;
  param_1[0xd] = 0.0;
  param_1[0xe] = 0.0;
  param_1[0xf] = 1.0;
  return;
}

