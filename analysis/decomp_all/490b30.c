
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN__text__00490b30(int param_1,float *param_2,float *param_3)

{
  float fVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_64 [24];
  
  puVar3 = local_64;
  for (iVar2 = 0x18; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (*(char *)(param_1 + 0x14) == '\a') {
    *param_2 = *param_2 * _DAT_005924c4;
    *param_3 = *param_3 * _DAT_005924c4;
  }
  else if (*(char *)(param_1 + 0x14) == '\r') {
    fVar1 = (float)((int)DAT_006c3e38 +
                   (int)((uint)*(byte *)(*(int *)(param_1 + 600) + 7) * (int)(short)PTR_DAT_006c3e3a
                        ) / 100) / _DAT_00592770;
    *param_2 = fVar1 * *param_2;
    *param_3 = fVar1 * *param_3;
  }
  if (*(char *)(param_1 + 0x34) == '4') {
    fVar1 = (float)((int)DAT_006c4348 +
                   (int)((uint)*(byte *)(*(int *)(param_1 + 600) + 7) * (int)(short)PTR_DAT_006c434a
                        ) / 100) / _DAT_00592770;
    *param_2 = fVar1 * *param_2;
    *param_3 = fVar1 * *param_3;
  }
  else if (*(char *)(param_1 + 0x34) == '5') {
    fVar1 = (float)((int)DAT_006c3bf8 +
                   (int)((uint)*(byte *)(*(int *)(param_1 + 600) + 8) * (int)DAT_006c3bfa) / 100) /
            _DAT_00592770;
    *param_2 = fVar1 * *param_2;
    *param_3 = fVar1 * *param_3;
  }
  return;
}

