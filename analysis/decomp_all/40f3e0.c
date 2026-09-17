
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __thiscall FUN__text__0040f3e0(int param_1,int param_2,uint param_3)

{
  short sVar1;
  ushort uVar2;
  int iVar3;
  ushort uVar4;
  int iVar5;
  undefined4 *puVar6;
  undefined4 local_c4 [16];
  int local_84;
  int local_80;
  int local_7c;
  int local_78;
  int local_74;
  int local_70;
  uint local_6c;
  int local_68;
  int local_64;
  int local_60;
  uint local_5c;
  int local_58;
  uint local_54;
  int local_50;
  uint local_4c;
  int local_48;
  undefined4 local_44;
  char local_40;
  ushort local_3c;
  undefined2 uStack_3a;
  ushort local_38;
  undefined2 uStack_36;
  ushort local_34;
  undefined2 uStack_32;
  uint local_30;
  int local_2c;
  int local_28;
  int local_24;
  float local_20;
  float local_1c;
  float local_18;
  float local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar6 = local_c4;
  for (iVar3 = 0x30; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar6 = 0xcccccccc;
    puVar6 = puVar6 + 1;
  }
  local_c = param_2;
  local_8 = param_1;
  (**(code **)(**(int **)(param_1 + 4) + 200))(*(undefined4 *)(param_1 + 4),0x1d,0);
  FUN__text__0056ce80();
  (**(code **)(**(int **)(local_8 + 4) + 200))(*(undefined4 *)(local_8 + 4),0xf,1);
  FUN__text__0056ce80();
  (**(code **)(**(int **)(local_8 + 4) + 200))(*(undefined4 *)(local_8 + 4),0x18,8);
  FUN__text__0056ce80();
  (**(code **)(**(int **)(local_8 + 4) + 200))(*(undefined4 *)(local_8 + 4),0x19,5);
  FUN__text__0056ce80();
  local_40 = *(char *)(local_c + 9);
  if (local_40 == '\x01') {
    if ((*(uint *)(local_c + 0x1c) & 0xff000000) != 0xff000000) {
      (**(code **)(**(int **)(local_8 + 4) + 200))(*(undefined4 *)(local_8 + 4),0x1b,1);
      FUN__text__0056ce80();
      (**(code **)(**(int **)(local_8 + 4) + 200))(*(undefined4 *)(local_8 + 4),0x13,5);
      FUN__text__0056ce80();
      (**(code **)(**(int **)(local_8 + 4) + 200))(*(undefined4 *)(local_8 + 4),0x14,6);
      FUN__text__0056ce80();
      goto LAB__text__0040f5b5;
    }
  }
  else if (local_40 == '\x02') {
    (**(code **)(**(int **)(local_8 + 4) + 200))(*(undefined4 *)(local_8 + 4),0x1b,1);
    FUN__text__0056ce80();
    (**(code **)(**(int **)(local_8 + 4) + 200))(*(undefined4 *)(local_8 + 4),0x13,5);
    FUN__text__0056ce80();
    (**(code **)(**(int **)(local_8 + 4) + 200))(*(undefined4 *)(local_8 + 4),0x14,7);
    FUN__text__0056ce80();
    goto LAB__text__0040f5b5;
  }
  (**(code **)(**(int **)(local_8 + 4) + 200))(*(undefined4 *)(local_8 + 4),0x1b,0);
  FUN__text__0056ce80();
LAB__text__0040f5b5:
  local_10 = *(int *)(local_c + 0x20);
  FUN__text__0040e210(*(undefined4 *)(local_10 + 0x2c));
  (**(code **)(**(int **)(local_8 + 4) + 0x130))(*(undefined4 *)(local_8 + 4),0x1c4);
  FUN__text__0056ce80();
  if (DAT_00799a48 == 0) {
    for (local_28 = 0; local_28 != 0x40; local_28 = local_28 + 1) {
      *(short *)(&DAT_00797748 + local_28 * 0xc) = (short)(local_28 << 2);
      sVar1 = (short)local_28;
      *(short *)(&DAT_0079774a + local_28 * 0xc) = sVar1 * 4 + 1;
      *(short *)(&DAT_0079774c + local_28 * 0xc) = sVar1 * 4 + 2;
      *(short *)(&DAT_0079774e + local_28 * 0xc) = sVar1 * 4 + 1;
      *(short *)(&DAT_00797750 + local_28 * 0xc) = sVar1 * 4 + 3;
      *(short *)(&DAT_00797752 + local_28 * 0xc) = sVar1 * 4 + 2;
    }
    DAT_00799a48 = 1;
  }
  local_24 = ((int)((int)*(short *)(local_c + 0xe) +
                   ((int)*(short *)(local_c + 0xe) >> 0x1f & 0xffU)) >> 8) + 1;
  if ((int)(0x100 / (longlong)(int)*(short *)(local_c + 0x10)) < local_24) {
    local_24 = (int)(0x100 / (longlong)(int)*(short *)(local_c + 0x10));
  }
  for (local_28 = 0; local_28 != local_24; local_28 = local_28 + 1) {
    local_30 = local_30 & 0xffff0000;
    uVar4 = *(short *)(local_c + 0x10) * (short)local_28;
    _local_34 = CONCAT22(uStack_32,uVar4);
    _local_38 = CONCAT22(uStack_36,*(ushort *)(local_c + 0x16));
    uVar2 = *(short *)(local_c + 0x10) * ((short)local_28 + 1);
    _local_3c = CONCAT22(uStack_3a,uVar2);
    local_44 = 0;
    local_48 = (int)*(short *)(local_c + 0x12);
    local_14 = (_DAT_005924c0 + 0.0) / (float)local_48;
    local_4c = (uint)uVar4;
    local_50 = (int)*(short *)(local_c + 0x14);
    local_18 = ((float)local_4c + _DAT_005924c0) / (float)local_50;
    local_54 = (uint)*(ushort *)(local_c + 0x16);
    local_58 = (int)*(short *)(local_c + 0x12);
    local_1c = ((float)local_54 + _DAT_005924c0) / (float)local_58;
    local_5c = (uint)uVar2;
    local_60 = (int)*(short *)(local_c + 0x14);
    local_20 = ((float)local_5c + _DAT_005924c0) / (float)local_60;
    local_64 = (uint)*(ushort *)(local_c + 0x16) * local_28 + (int)*(short *)(local_c + 10);
    *(float *)(&DAT_00797a48 + local_28 * 0x80) = (float)local_64 - _DAT_005924c4;
    local_68 = (int)*(short *)(local_c + 0xc);
    *(float *)(&DAT_00797a4c + local_28 * 0x80) = (float)local_68 - _DAT_005924c4;
    local_6c = param_3 & 0xffff;
    (&DAT_00797a50)[local_28 * 0x20] = (float)local_6c / _DAT_00592774;
    *(undefined4 *)(&DAT_00797a54 + local_28 * 0x80) = 0x3f800000;
    (&DAT_00797a58)[local_28 * 0x20] = *(undefined4 *)(local_c + 0x1c);
    *(float *)(&DAT_00797a60 + local_28 * 0x80) = local_14;
    *(float *)(&DAT_00797a64 + local_28 * 0x80) = local_18;
    *(undefined4 *)(&DAT_00797a5c + local_28 * 0x80) = 0;
    local_70 = (uint)*(ushort *)(local_c + 0x16) * local_28 + (int)*(short *)(local_c + 10) +
               (uint)*(ushort *)(local_c + 0x16);
    *(float *)(&DAT_00797a48 + (local_28 * 4 + 1) * 0x20) = (float)local_70 - _DAT_005924c4;
    local_74 = (int)*(short *)(local_c + 0xc);
    *(float *)(&DAT_00797a4c + (local_28 * 4 + 1) * 0x20) = (float)local_74 - _DAT_005924c4;
    (&DAT_00797a50)[(local_28 * 4 + 1) * 8] = DAT_00797a50;
    *(undefined4 *)(&DAT_00797a54 + (local_28 * 4 + 1) * 0x20) = 0x3f800000;
    (&DAT_00797a58)[(local_28 * 4 + 1) * 8] = DAT_00797a58;
    *(float *)(&DAT_00797a60 + (local_28 * 4 + 1) * 0x20) = local_1c;
    *(float *)(&DAT_00797a64 + (local_28 * 4 + 1) * 0x20) = local_18;
    *(undefined4 *)(&DAT_00797a5c + (local_28 * 4 + 1) * 0x20) = 0;
    local_78 = (uint)*(ushort *)(local_c + 0x16) * local_28 + (int)*(short *)(local_c + 10);
    *(float *)(&DAT_00797a48 + (local_28 * 4 + 2) * 0x20) = (float)local_78 - _DAT_005924c4;
    local_7c = (int)*(short *)(local_c + 0xc) + (int)*(short *)(local_c + 0x10);
    *(float *)(&DAT_00797a4c + (local_28 * 4 + 2) * 0x20) = (float)local_7c - _DAT_005924c4;
    (&DAT_00797a50)[(local_28 * 4 + 2) * 8] = DAT_00797a50;
    *(undefined4 *)(&DAT_00797a54 + (local_28 * 4 + 2) * 0x20) = 0x3f800000;
    (&DAT_00797a58)[(local_28 * 4 + 2) * 8] = DAT_00797a58;
    *(float *)(&DAT_00797a60 + (local_28 * 4 + 2) * 0x20) = local_14;
    *(float *)(&DAT_00797a64 + (local_28 * 4 + 2) * 0x20) = local_20;
    *(undefined4 *)(&DAT_00797a5c + (local_28 * 4 + 2) * 0x20) = 0;
    local_80 = (uint)*(ushort *)(local_c + 0x16) * local_28 + (int)*(short *)(local_c + 10) +
               (uint)*(ushort *)(local_c + 0x16);
    *(float *)(&DAT_00797a48 + (local_28 * 4 + 3) * 0x20) = (float)local_80 - _DAT_005924c4;
    local_84 = (int)*(short *)(local_c + 0xc) + (int)*(short *)(local_c + 0x10);
    *(float *)(&DAT_00797a4c + (local_28 * 4 + 3) * 0x20) = (float)local_84 - _DAT_005924c4;
    (&DAT_00797a50)[(local_28 * 4 + 3) * 8] = DAT_00797a50;
    *(undefined4 *)(&DAT_00797a54 + (local_28 * 4 + 3) * 0x20) = 0x3f800000;
    (&DAT_00797a58)[(local_28 * 4 + 3) * 8] = DAT_00797a58;
    *(float *)(&DAT_00797a60 + (local_28 * 4 + 3) * 0x20) = local_1c;
    *(float *)(&DAT_00797a64 + (local_28 * 4 + 3) * 0x20) = local_20;
    *(undefined4 *)(&DAT_00797a5c + (local_28 * 4 + 3) * 0x20) = 0;
  }
  local_2c = local_24;
  iVar5 = local_24 << 1;
  iVar3 = local_24 << 2;
  local_24 = iVar5;
  (**(code **)(**(int **)(local_8 + 4) + 0x124))
            (*(undefined4 *)(local_8 + 4),4,0,iVar3,iVar5,&DAT_00797748,0x65,&DAT_00797a48,0x20);
  FUN__text__0056ce80();
  (**(code **)(**(int **)(local_8 + 4) + 200))(*(undefined4 *)(local_8 + 4),0x1d,1);
  FUN__text__0056ce80();
  local_7c = 0x40fc0b;
  FUN__text__0056ce80();
  return;
}

