
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __thiscall FUN__text__00534a4d(int param_1,int param_2,int param_3,float *param_4)

{
  byte *pbVar1;
  float fVar2;
  byte *pbVar3;
  
  fVar2 = _DAT_005d0e78;
  pbVar3 = (byte *)(*(int *)(param_1 + 0x1050) * param_2 + *(int *)(param_1 + 0x1054) * param_3 +
                   *(int *)(param_1 + 0x18));
  pbVar1 = pbVar3 + *(int *)(param_1 + 0x1058) * 2;
  for (; pbVar3 < pbVar1; pbVar3 = pbVar3 + 2) {
    *param_4 = (float)(pbVar3[1] & 0xf) * fVar2;
    param_4[1] = (float)(*pbVar3 >> 4) * fVar2;
    param_4[2] = (float)(*pbVar3 & 0xf) * fVar2;
    param_4[3] = 1.0;
    param_4 = param_4 + 4;
  }
  if (*(int *)(param_1 + 0x10) != 0) {
    FUN__text__005324ac(param_4 + *(int *)(param_1 + 0x1058) * -4);
  }
  return;
}

