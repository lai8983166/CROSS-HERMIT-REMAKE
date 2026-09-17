
/* WARNING: Removing unreachable block (ram,0x00535189) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __thiscall FUN__text__005350ef(int param_1,int param_2,int param_3,float *param_4)

{
  uint *puVar1;
  uint uVar2;
  float fVar3;
  uint *puVar4;
  
  fVar3 = _DAT_005d0e98;
  puVar4 = (uint *)(*(int *)(param_1 + 0x1050) * param_2 + *(int *)(param_1 + 0x1054) * param_3 +
                   *(int *)(param_1 + 0x18));
  puVar1 = puVar4 + *(int *)(param_1 + 0x1058);
  for (; puVar4 < puVar1; puVar4 = puVar4 + 1) {
    uVar2 = *puVar4;
    *param_4 = (float)(int)((short)((short)*puVar4 << 6) >> 6) * fVar3;
    param_4[1] = (float)(int)((short)((short)(uVar2 >> 10) << 6) >> 6) * fVar3;
    param_4[2] = (float)(int)((short)((ushort)(uVar2 >> 0x14) << 6) >> 6) * fVar3;
    param_4[3] = (float)(*puVar4 >> 0x1e) * _DAT_005d0e7c;
    param_4 = param_4 + 4;
  }
  if (*(int *)(param_1 + 0x10) != 0) {
    FUN__text__005324ac(param_4 + *(int *)(param_1 + 0x1058) * -4);
  }
  return;
}

