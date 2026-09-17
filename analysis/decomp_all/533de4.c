
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __thiscall FUN__text__00533de4(int param_1,uint param_2,uint param_3,int param_4)

{
  int iVar1;
  float *pfVar2;
  uint uVar3;
  undefined2 *extraout_EDX;
  undefined2 *puVar4;
  int iVar5;
  
  iVar5 = 0;
  if (*(int *)(param_1 + 0x1048) != 0) {
    param_4 = FUN__text__00531868(param_4);
  }
  iVar1 = *(int *)(param_1 + 0x2c);
  FUN__text__005320bb();
  uVar3 = 0;
  puVar4 = extraout_EDX;
  if (*(int *)(param_1 + 0x1058) != 0) {
    do {
      pfVar2 = (float *)(param_4 + iVar5);
      *puVar4 = (short)(int)ROUND(*(float *)(iVar1 + ((param_3 & 3) + (param_2 & 3) * 8) * 4 +
                                            (uVar3 & 3) * 4) +
                                  (*pfVar2 * _DAT_005d0a48 +
                                  pfVar2[1] * _DAT_005d0a4c + pfVar2[2] * _DAT_005d0a50) *
                                  _DAT_005d0e54);
      puVar4 = puVar4 + 1;
      uVar3 = uVar3 + 1;
      iVar5 = iVar5 + 0x10;
    } while (uVar3 < *(uint *)(param_1 + 0x1058));
  }
  return;
}

