
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __thiscall FUN__text__00533784(int param_1,uint param_2,uint param_3,int param_4)

{
  float fVar1;
  int iVar2;
  ushort *extraout_EDX;
  ushort *puVar3;
  uint uVar4;
  int iVar5;
  
  uVar4 = 0;
  if (*(int *)(param_1 + 0x1048) != 0) {
    param_4 = FUN__text__00531868(param_4);
  }
  iVar2 = *(int *)(param_1 + 0x2c);
  FUN__text__005320bb();
  if (*(int *)(param_1 + 0x1058) != 0) {
    iVar5 = 0;
    puVar3 = extraout_EDX;
    do {
      fVar1 = *(float *)(iVar2 + ((param_3 & 3) + (param_2 & 3) * 8) * 4 + (uVar4 & 3) * 4);
      *puVar3 = (ushort)(((int)ROUND(*(float *)(iVar5 + 4 + param_4) * _DAT_005d0e60 + fVar1) &
                          0x1fU | (int)ROUND(*(float *)(iVar5 + 0xc + param_4) * _DAT_005d0e3c +
                                             fVar1) << 5) << 5) |
                (ushort)(int)ROUND(*(float *)(iVar5 + param_4) * _DAT_005d0e60 + fVar1) & 0x1f;
      puVar3 = puVar3 + 1;
      uVar4 = uVar4 + 1;
      iVar5 = iVar5 + 0x10;
    } while (uVar4 < *(uint *)(param_1 + 0x1058));
  }
  return;
}

