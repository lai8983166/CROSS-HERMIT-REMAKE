
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __thiscall FUN__text__0053251c(int param_1,uint param_2,uint param_3,int param_4)

{
  float fVar1;
  int iVar2;
  int iVar3;
  undefined1 *extraout_EDX;
  undefined1 *puVar4;
  uint uVar5;
  
  if (*(int *)(param_1 + 0x1048) != 0) {
    param_4 = FUN__text__00531868(param_4);
  }
  iVar2 = *(int *)(param_1 + 0x2c);
  FUN__text__005320bb();
  iVar3 = 0;
  uVar5 = 0;
  puVar4 = extraout_EDX;
  if (*(int *)(param_1 + 0x1058) != 0) {
    do {
      fVar1 = *(float *)(iVar2 + ((param_3 & 3) + (param_2 & 3) * 8) * 4 + (uVar5 & 3) * 4);
      *puVar4 = (char)(int)ROUND(*(float *)(iVar3 + 8 + param_4) * _DAT_005d0e38 + fVar1);
      puVar4[1] = (char)(int)ROUND(*(float *)(iVar3 + 4 + param_4) * _DAT_005d0e38 + fVar1);
      puVar4[2] = (char)(int)ROUND(*(float *)(iVar3 + param_4) * _DAT_005d0e38 + fVar1);
      puVar4 = puVar4 + 3;
      uVar5 = uVar5 + 1;
      iVar3 = iVar3 + 0x10;
    } while (uVar5 < *(uint *)(param_1 + 0x1058));
  }
  return;
}

