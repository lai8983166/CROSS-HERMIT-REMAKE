
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN__text__00470250(int param_1,undefined4 *param_2,int *param_3)

{
  short sVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 *puVar4;
  float10 fVar5;
  undefined4 local_a4 [16];
  int local_64;
  int local_60;
  int local_5c;
  int local_58;
  int local_54;
  int local_50;
  int local_4c;
  int local_48;
  uint local_44;
  int local_40;
  int local_3c;
  int local_38;
  float local_34;
  float local_30;
  float local_2c;
  float local_28;
  float local_24;
  short local_20;
  short local_1c;
  short local_18;
  short local_14;
  short local_10;
  short local_c;
  undefined4 local_8;
  
  puVar4 = local_a4;
  for (iVar3 = 0x28; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_c = (short)((uint)*(undefined4 *)(param_1 + 0x2ec) >> 0x10);
  local_10 = (short)((uint)*(undefined4 *)(param_1 + 0x2f0) >> 0x10);
  local_14 = *(short *)(param_1 + 0x4dc);
  local_18 = *(short *)(param_1 + 0x4de);
  local_38 = FUN__text__0043b8b0((int)((int)local_c + ((int)local_c >> 0x1f & 0x1fU)) >> 5,
                                 (int)((int)local_10 + ((int)local_10 >> 0x1f & 0xfU)) >> 4,
                                 *(undefined1 *)(*(int *)(param_1 + 600) + 0x30),0);
  local_1c = local_14 - local_c;
  local_20 = local_18 - local_10;
  local_3c = (int)local_1c;
  local_40 = (int)local_20;
  fVar5 = (float10)FUN__text__005711b0((double)local_40,(double)local_3c);
  local_24 = (float)fVar5;
  local_28 = (float)(fVar5 / (float10)_DAT_00592778);
  if (local_28 < _DAT_005924c0) {
    local_28 = local_28 + _DAT_0059c670 + _DAT_0059c670;
  }
  sVar1 = __ftol();
  *(short *)(param_1 + 0x4ec) = sVar1 % 0x168;
  local_44 = (uint)*(ushort *)(*(int *)(param_1 + 600) + 0x2e);
  local_2c = (float)local_38 * _DAT_0059ac28 * (float)local_44 * _DAT_0059ac28;
  fVar5 = (float10)FUN__text__0056d9d4((double)local_24);
  local_30 = (float)fVar5;
  fVar5 = (float10)FUN__text__0056d924((double)local_24);
  local_30 = local_30 * _DAT_005924cc * local_2c * _DAT_005924cc;
  local_34 = (float)fVar5 * _DAT_005924cc * local_2c * _DAT_005924cc;
  FUN__text__00490b30();
  local_1c = FUN__text__0056db00();
  local_20 = FUN__text__0056db00();
  local_48 = (int)local_1c;
  if ((float)local_48 < local_30) {
    local_4c = (int)local_1c;
    local_30 = (float)local_4c;
  }
  local_50 = (int)local_20;
  if ((float)local_50 < local_34) {
    local_54 = (int)local_20;
    local_34 = (float)local_54;
  }
  local_30 = local_30 * _DAT_00592774;
  local_34 = local_34 * _DAT_00592774;
  __ftol();
  local_58 = FUN__text__00415040();
  local_30 = (float)local_58;
  __ftol();
  local_5c = FUN__text__00415040();
  local_34 = (float)local_5c;
  uVar2 = __ftol();
  *param_2 = uVar2;
  iVar3 = __ftol();
  *param_3 = iVar3;
  *param_3 = *param_3 / 2;
  local_c = (short)((int)((int)*(short *)(param_1 + 0x4d4) +
                         ((int)*(short *)(param_1 + 0x4d4) >> 0x1f & 0x1fU)) >> 5);
  local_10 = (short)((int)((int)*(short *)(param_1 + 0x4d6) +
                          ((int)*(short *)(param_1 + 0x4d6) >> 0x1f & 0xfU)) >> 4);
  local_14 = (short)((int)((int)*(short *)(param_1 + 0x4d8) +
                          ((int)*(short *)(param_1 + 0x4d8) >> 0x1f & 0x1fU)) >> 5);
  local_18 = (short)((int)((int)*(short *)(param_1 + 0x4da) +
                          ((int)*(short *)(param_1 + 0x4da) >> 0x1f & 0xfU)) >> 4);
  local_1c = local_14 - local_c;
  local_20 = local_18 - local_10;
  local_60 = (int)local_1c;
  local_64 = (int)local_20;
  fVar5 = (float10)FUN__text__005711b0((double)local_64,(double)local_60);
  local_24 = (float)fVar5;
  local_28 = (float)(fVar5 / (float10)_DAT_00592778);
  if (local_28 < _DAT_005924c0) {
    local_28 = local_28 + _DAT_0059c670 + _DAT_0059c670;
  }
  sVar1 = __ftol();
  *(short *)(param_1 + 0x4ec) = sVar1 % 0x168;
  local_8 = 0x470611;
  FUN__text__0056ce80();
  return;
}

