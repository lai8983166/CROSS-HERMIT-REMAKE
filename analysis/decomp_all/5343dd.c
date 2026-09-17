
/* WARNING: Removing unreachable block (ram,0x00534440) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __thiscall FUN__text__005343dd(int param_1,int param_2,int param_3,float *param_4)

{
  uint *puVar1;
  float fVar2;
  uint *puVar3;
  
  fVar2 = _DAT_005d0e24;
  puVar3 = (uint *)(*(int *)(param_1 + 0x1050) * param_2 + *(int *)(param_1 + 0x1054) * param_3 +
                   *(int *)(param_1 + 0x18));
  puVar1 = puVar3 + *(int *)(param_1 + 0x1058);
  for (; puVar3 < puVar1; puVar3 = puVar3 + 1) {
    *param_4 = (float)*(byte *)((int)puVar3 + 2) * fVar2;
    param_4[1] = (float)*(byte *)((int)puVar3 + 1) * fVar2;
    param_4[2] = (float)(*puVar3 & 0xff) * fVar2;
    param_4[3] = 1.0;
    param_4 = param_4 + 4;
  }
  if (*(int *)(param_1 + 0x10) != 0) {
    FUN__text__005324ac(param_4 + *(int *)(param_1 + 0x1058) * -4);
  }
  return;
}

