
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __thiscall FUN__text__00407ad0(int param_1,int param_2,int param_3)

{
  undefined4 uVar1;
  undefined4 uVar2;
  undefined2 extraout_var;
  int iVar3;
  undefined2 extraout_var_00;
  int iVar4;
  undefined2 extraout_var_01;
  undefined4 *puVar5;
  undefined4 local_d4 [16];
  int local_94;
  int local_90;
  int local_8c;
  int local_88;
  int local_84;
  int local_80;
  int local_7c;
  int local_78;
  int local_74;
  int local_70;
  int local_6c;
  uint local_68;
  int local_64;
  uint local_60;
  int local_5c;
  uint local_58;
  int local_54;
  uint local_50;
  int local_4c;
  int local_48;
  int local_44;
  int local_40;
  int local_3c;
  int local_38;
  short local_34;
  float local_2c;
  float local_28;
  float local_24;
  float local_20;
  float local_1c;
  float local_18;
  float local_14;
  float local_10;
  int local_c;
  int local_8;
  
  puVar5 = local_d4;
  for (iVar3 = 0x34; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar5 = 0xcccccccc;
    puVar5 = puVar5 + 1;
  }
  if ((*(int *)(param_1 + 0x4c) != 0) && (*(short *)(*(int *)(param_1 + 0x4c) + 0xb28e) != 0)) {
    local_8 = param_1;
    local_c = FUN__text__0040dcd0(1);
    if ((*(ushort *)(local_8 + 0x58) & 1) == 0) {
      local_48 = (int)*(short *)(local_8 + 0x38);
      local_18 = (float)local_48;
      local_4c = (int)*(short *)(local_8 + 0x3a);
      local_1c = (float)local_4c;
    }
    else {
      local_38 = (int)*(short *)(local_8 + 0x38);
      local_3c = (int)*(short *)(local_8 + 0x70);
      local_18 = ((float)local_38 * (float)local_3c) / _DAT_00592770;
      local_40 = (int)*(short *)(local_8 + 0x3a);
      local_44 = (int)*(short *)(local_8 + 0x72);
      local_1c = ((float)local_40 * (float)local_44) / _DAT_00592770;
    }
    if ((*(ushort *)(local_8 + 0x58) & 0x40) == 0) {
      local_70 = (int)*(short *)(local_8 + 0x3c);
      local_20 = _DAT_005924c0 / (float)local_70;
      local_74 = (int)*(short *)(local_8 + 0x3e);
      local_24 = _DAT_005924c0 / (float)local_74;
      local_78 = (int)*(short *)(local_8 + 0x38);
      local_7c = (int)*(short *)(local_8 + 0x3c);
      local_28 = ((float)local_78 + _DAT_005924c0) / (float)local_7c;
      local_80 = (int)*(short *)(local_8 + 0x3a);
      local_84 = (int)*(short *)(local_8 + 0x3e);
      local_2c = ((float)local_80 + _DAT_005924c0) / (float)local_84;
    }
    else {
      local_50 = (uint)*(ushort *)(local_8 + 0x78);
      local_54 = (int)*(short *)(local_8 + 0x3c);
      local_20 = ((float)local_50 + _DAT_005924c0) / (float)local_54;
      local_58 = (uint)*(ushort *)(local_8 + 0x7a);
      local_5c = (int)*(short *)(local_8 + 0x3e);
      local_24 = ((float)local_58 + _DAT_005924c0) / (float)local_5c;
      local_60 = (uint)*(ushort *)(local_8 + 0x7c);
      local_64 = (int)*(short *)(local_8 + 0x3c);
      local_28 = ((float)local_60 + _DAT_005924c0) / (float)local_64;
      local_68 = (uint)*(ushort *)(local_8 + 0x7e);
      local_6c = (int)*(short *)(local_8 + 0x3e);
      local_2c = ((float)local_68 + _DAT_005924c0) / (float)local_6c;
    }
    if ((*(ushort *)(local_8 + 0x58) & 8) == 0) {
      local_90 = *(int *)(local_8 + 0x68) + param_2;
      local_10 = (float)local_90;
      local_94 = *(int *)(local_8 + 0x6c) + param_3;
      local_14 = (float)local_94;
    }
    else {
      local_88 = *(int *)(local_8 + 0x68) + param_2;
      local_10 = (float)local_88 - local_18 / _DAT_005924c8;
      local_8c = *(int *)(local_8 + 0x6c) + param_3;
      local_14 = (float)local_8c - local_1c / _DAT_005924c8;
    }
    if ((*(ushort *)(local_8 + 0x58) & 1) == 0) {
      iVar4 = (int)*(short *)(local_8 + 0x3a);
      iVar3 = (int)*(short *)(local_8 + 0x38);
      uVar1 = __ftol(iVar3,iVar4);
      uVar2 = __ftol(uVar1);
      iVar3 = FUN__text__0040e2a0(uVar2,uVar1,iVar3,iVar4);
      if (iVar3 != 0) goto LAB__text__00408111;
    }
    *(float *)(local_c + 0xc) = local_10 - _DAT_005924c4;
    *(float *)(local_c + 0x1c) = local_14 - _DAT_005924c4;
    if ((*(ushort *)(local_8 + 0x58) & 0x10) == 0) {
      *(float *)(local_c + 0x2c) = local_20;
    }
    else {
      *(float *)(local_c + 0x2c) = local_28;
    }
    if ((*(ushort *)(local_8 + 0x58) & 0x20) == 0) {
      *(float *)(local_c + 0x3c) = local_24;
    }
    else {
      *(float *)(local_c + 0x3c) = local_2c;
    }
    *(float *)(local_c + 0x10) = (local_10 + local_18) - _DAT_005924c4;
    *(float *)(local_c + 0x20) = local_14 - _DAT_005924c4;
    if ((*(ushort *)(local_8 + 0x58) & 0x10) == 0) {
      *(float *)(local_c + 0x30) = local_28;
    }
    else {
      *(float *)(local_c + 0x30) = local_20;
    }
    if ((*(ushort *)(local_8 + 0x58) & 0x20) == 0) {
      *(float *)(local_c + 0x40) = local_24;
    }
    else {
      *(float *)(local_c + 0x40) = local_2c;
    }
    *(float *)(local_c + 0x14) = (local_10 + local_18) - _DAT_005924c4;
    *(float *)(local_c + 0x24) = (local_14 + local_1c) - _DAT_005924c4;
    if ((*(ushort *)(local_8 + 0x58) & 0x10) == 0) {
      *(float *)(local_c + 0x34) = local_28;
    }
    else {
      *(float *)(local_c + 0x34) = local_20;
    }
    if ((*(ushort *)(local_8 + 0x58) & 0x20) == 0) {
      *(float *)(local_c + 0x44) = local_2c;
    }
    else {
      *(float *)(local_c + 0x44) = local_24;
    }
    *(float *)(local_c + 0x18) = local_10 - _DAT_005924c4;
    *(float *)(local_c + 0x28) = (local_14 + local_1c) - _DAT_005924c4;
    if ((*(ushort *)(local_8 + 0x58) & 0x10) == 0) {
      *(float *)(local_c + 0x38) = local_20;
    }
    else {
      *(float *)(local_c + 0x38) = local_28;
    }
    if ((*(ushort *)(local_8 + 0x58) & 0x20) == 0) {
      *(float *)(local_c + 0x48) = local_2c;
    }
    else {
      *(float *)(local_c + 0x48) = local_24;
    }
    if (((*(ushort *)(local_8 + 0x58) & 2) != 0) &&
       (local_34 = *(short *)(local_8 + 0x74) % 0x168, local_34 != 0)) {
      if ((*(ushort *)(local_8 + 0x58) & 4) != 0) {
        *(float *)(local_8 + 0x50) = local_18 / _DAT_005924c8;
        *(float *)(local_8 + 0x54) = local_1c / _DAT_005924c8;
      }
      local_10 = local_10 + *(float *)(local_8 + 0x50);
      local_14 = local_14 + *(float *)(local_8 + 0x54);
      FUN__text__00408d30(local_c + 0xc,local_c + 0x1c,local_10,local_14,local_34);
      FUN__text__00408d30(local_c + 0x10,local_c + 0x20,local_10,local_14,
                          CONCAT22(extraout_var_01,local_34));
      FUN__text__00408d30(local_c + 0x14,local_c + 0x24,local_10,local_14,
                          CONCAT22(extraout_var_00,local_34));
      FUN__text__00408d30(local_c + 0x18,local_c + 0x28,local_10,local_14,
                          CONCAT22(extraout_var,local_34));
    }
    if ((*(ushort *)(local_8 + 0x58) & 0x80) == 0) {
      *(int *)(local_c + 0x50) = local_8;
    }
    else {
      *(undefined4 *)(local_c + 0x50) = *(undefined4 *)(local_8 + 0x48);
    }
    *(undefined4 *)(local_c + 4) = 1;
    *(undefined2 *)(local_c + 0x58) = *(undefined2 *)(local_8 + 0x76);
    *(uint *)(local_c + 0x4c) =
         (uint)*(byte *)(local_8 + 0x67) << 0x18 | (uint)*(byte *)(local_8 + 0x66) << 0x10 |
         (uint)*(byte *)(local_8 + 0x65) << 8 | (uint)*(byte *)(local_8 + 100);
    *(undefined1 *)(local_c + 8) = *(undefined1 *)(local_8 + 0x60);
    *(undefined1 *)(local_c + 9) = *(undefined1 *)(local_8 + 0x5c);
    FUN__text__0040df20(local_c,*(undefined2 *)(local_8 + 0x76));
  }
LAB__text__00408111:
  local_8 = 0x408121;
  FUN__text__0056ce80();
  return;
}

