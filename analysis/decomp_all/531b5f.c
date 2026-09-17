
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __thiscall FUN__text__00531b5f(float *param_1,uint param_2)

{
  float fVar1;
  
  fVar1 = _DAT_005d0e24;
  *param_1 = (float)(param_2 >> 0x10 & 0xff) * _DAT_005d0e24;
  param_1[1] = (float)(param_2 >> 8 & 0xff) * fVar1;
  param_1[2] = (float)(param_2 & 0xff) * fVar1;
  param_1[3] = (float)(param_2 >> 0x18) * fVar1;
  return;
}

