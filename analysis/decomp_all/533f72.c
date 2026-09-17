
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __thiscall FUN__text__00533f72(int param_1,uint param_2,uint param_3,int param_4)

{
  float fVar1;
  int iVar2;
  float *pfVar3;
  int iVar4;
  uint *extraout_EDX;
  uint *puVar5;
  uint uVar6;
  
  if (*(int *)(param_1 + 0x1048) != 0) {
    param_4 = FUN__text__00531868(param_4);
  }
  iVar2 = *(int *)(param_1 + 0x2c);
  FUN__text__005320bb();
  uVar6 = 0;
  if (*(int *)(param_1 + 0x1058) != 0) {
    iVar4 = 0;
    puVar5 = extraout_EDX;
    do {
      fVar1 = *(float *)(iVar2 + ((param_3 & 3) + (param_2 & 3) * 8) * 4 + (uVar6 & 3) * 4);
      pfVar3 = (float *)(param_4 + iVar4);
      *puVar5 = (int)ROUND(*(float *)(iVar4 + 0xc + param_4) * _DAT_005d0e54 + fVar1) << 0x10 |
                (int)ROUND((*pfVar3 * _DAT_005d0a48 +
                           pfVar3[1] * _DAT_005d0a4c + pfVar3[2] * _DAT_005d0a50) * _DAT_005d0e54 +
                           fVar1);
      puVar5 = puVar5 + 1;
      uVar6 = uVar6 + 1;
      iVar4 = iVar4 + 0x10;
    } while (uVar6 < *(uint *)(param_1 + 0x1058));
  }
  return;
}

