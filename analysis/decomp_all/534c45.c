
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __thiscall FUN__text__00534c45(int param_1,int param_2,int param_3,float *param_4)

{
  byte *pbVar1;
  float fVar2;
  float fVar3;
  byte *pbVar4;
  
  fVar3 = _DAT_005d0e24;
  pbVar4 = (byte *)(*(int *)(param_1 + 0x1050) * param_2 + *(int *)(param_1 + 0x1054) * param_3 +
                   *(int *)(param_1 + 0x18));
  pbVar1 = pbVar4 + *(int *)(param_1 + 0x1058) * 2;
  for (; pbVar4 < pbVar1; pbVar4 = pbVar4 + 2) {
    fVar2 = (float)*pbVar4 * fVar3;
    param_4[2] = fVar2;
    param_4[1] = fVar2;
    *param_4 = fVar2;
    param_4[3] = (float)pbVar4[1] * fVar3;
    param_4 = param_4 + 4;
  }
  if (*(int *)(param_1 + 0x10) != 0) {
    FUN__text__005324ac(param_4 + *(int *)(param_1 + 0x1058) * -4);
  }
  return;
}

