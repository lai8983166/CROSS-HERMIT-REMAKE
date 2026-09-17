
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __thiscall FUN__text__00532c6e(int param_1,uint param_2,uint param_3,int param_4)

{
  float *pfVar1;
  int iVar2;
  float fVar3;
  int iVar4;
  byte *extraout_EDX;
  byte *pbVar5;
  int iVar6;
  uint uVar7;
  byte local_20;
  
  uVar7 = 0;
  if (*(int *)(param_1 + 0x1048) != 0) {
    param_4 = FUN__text__00531868(param_4);
  }
  iVar4 = *(int *)(param_1 + 0x2c);
  FUN__text__005320bb();
  if (*(int *)(param_1 + 0x1058) != 0) {
    iVar6 = 0;
    pbVar5 = extraout_EDX;
    do {
      fVar3 = *(float *)(iVar4 + ((param_3 & 3) + (param_2 & 3) * 8) * 4 + (uVar7 & 3) * 4);
      pfVar1 = (float *)(iVar6 + param_4);
      iVar2 = iVar6 + 8;
      local_20 = (byte)(int)ROUND(*(float *)(iVar6 + 4 + param_4) * _DAT_005d0e4c + fVar3);
      iVar6 = iVar6 + 0x10;
      *pbVar5 = ((char)(int)ROUND(*pfVar1 * _DAT_005d0e4c + fVar3) << 3 | local_20) << 2 |
                (byte)(int)ROUND(*(float *)(iVar2 + param_4) * _DAT_005d0e48 + fVar3);
      pbVar5 = pbVar5 + 1;
      uVar7 = uVar7 + 1;
    } while (uVar7 < *(uint *)(param_1 + 0x1058));
  }
  return;
}

