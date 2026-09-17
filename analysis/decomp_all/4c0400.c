
void FUN__text__004c0400(short param_1,short param_2)

{
  undefined1 uVar1;
  int iVar2;
  undefined2 extraout_var;
  undefined4 *puVar3;
  undefined4 local_1dc [16];
  uint local_19c;
  byte local_198;
  int local_194;
  undefined1 local_190 [16];
  undefined1 local_180;
  int local_98;
  short local_94;
  short local_90;
  short asStack_8c [10];
  short local_78;
  short local_74;
  ushort local_70;
  short local_6c;
  short local_68;
  short local_64;
  ushort local_60;
  short local_5c;
  undefined *local_58;
  int local_54 [8];
  undefined2 local_34;
  short local_30;
  short local_2c;
  short local_28;
  undefined *local_24;
  short local_20 [12];
  int local_8;
  
  puVar3 = local_1dc;
  for (iVar2 = 0x76; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_20[0] = 0;
  local_20[1] = 1;
  local_20[2] = 2;
  local_20[3] = 2;
  local_20[4] = 3;
  local_20[5] = 3;
  local_20[6] = 4;
  local_20[7] = 4;
  local_20[8] = 4;
  local_20[9] = 4;
  local_20[10] = 4;
  local_20[0xb] = 0xffff;
  local_24 = &DAT_007e17e8 + param_1 * 0x4a0;
  local_30 = *(short *)(&DAT_007a52a4 + param_2 * 0x70);
  local_34 = *(undefined2 *)(&DAT_007a529c + param_2 * 0x70);
  FUN__text__004d3600(local_54,CONCAT22((short)((uint)(param_2 * 0x70) >> 0x10),param_1),
                      CONCAT22((short)((uint)(param_2 * 0x70) >> 0x10),local_30),local_34);
  *(undefined4 *)(&DAT_007cf36c + param_1 * 0x124) = 0;
  for (local_28 = 0; local_28 < 8; local_28 = local_28 + 1) {
    local_194 = (int)local_28;
    if (local_194 == 7) {
      *(int *)(local_8 + 0x34) = *(int *)(local_8 + 0x34) + local_54[7];
    }
    else {
      *(int *)(&DAT_007e17f8 + local_28 * 8 + param_1 * 0x4a0) =
           *(int *)(&DAT_007e17f8 + local_28 * 8 + param_1 * 0x4a0) + local_54[local_28];
      *(int *)(&DAT_007cf36c + param_1 * 0x124) =
           *(int *)(&DAT_007cf36c + param_1 * 0x124) + local_54[local_28];
    }
  }
  local_58 = &DAT_007e17e8 + param_1 * 0x4a0;
  local_5c = *(short *)(&DAT_007e17ee + param_1 * 0x4a0);
  local_60 = 0;
  local_64 = 0;
  local_68 = 0;
  local_6c = 0;
  local_70 = 0;
  local_74 = 0;
  local_78 = 0;
  for (local_28 = 0; local_28 < 8; local_28 = local_28 + 1) {
    *(undefined2 *)(local_8 + param_1 * 0x44 + 0x4a + local_28 * 2) = 0;
  }
  for (local_28 = 0; local_28 < 5; local_28 = local_28 + 1) {
    asStack_8c[local_28] = (short)(char)(&DAT_007cf424)[local_28 * 2 + param_1 * 0x124];
    asStack_8c[local_28] =
         asStack_8c[local_28] + (short)(char)(&DAT_007cf425)[local_28 * 2 + param_1 * 0x124];
    asStack_8c[local_28] =
         asStack_8c[local_28] + (short)(char)(&DAT_007cf42e)[local_28 * 2 + param_1 * 0x124];
    asStack_8c[local_28] =
         asStack_8c[local_28] + (short)(char)(&DAT_007cf42f)[local_28 * 2 + param_1 * 0x124];
    asStack_8c[local_28] =
         asStack_8c[local_28] + (short)(char)(&DAT_007cf438)[local_28 * 2 + param_1 * 0x124];
    asStack_8c[local_28] =
         asStack_8c[local_28] + (short)(char)(&DAT_007cf439)[local_28 * 2 + param_1 * 0x124];
  }
  local_28 = 0;
LAB__text__004c0757:
  if (10 < local_28) {
    local_98 = 0;
    for (local_28 = 0; local_28 < 7; local_28 = local_28 + 1) {
      *(ushort *)(local_8 + param_1 * 0x44 + 0x3a + local_28 * 2) =
           (ushort)(byte)(&DAT_007e17f4)[local_28 * 8 + param_1 * 0x4a0];
      *(ushort *)(local_8 + param_1 * 0x44 + 0x5c + local_28 * 2) =
           (ushort)(byte)(&DAT_007e17f4)[local_28 * 8 + param_1 * 0x4a0];
      uVar1 = FUN__text__004d5600(*(undefined4 *)(&DAT_007e17f8 + local_28 * 8 + param_1 * 0x4a0));
      (&DAT_007e17f4)[local_28 * 8 + param_1 * 0x4a0] = uVar1;
      local_98 = local_98 + *(int *)(&DAT_007e17f8 + local_28 * 8 + param_1 * 0x4a0);
      *(undefined2 *)(local_8 + param_1 * 0x44 + 0x6c + local_28 * 2) = 0;
    }
    *(ushort *)(local_8 + 0x38 + param_1 * 0x44) = (ushort)(byte)(&DAT_007e1838)[param_1 * 0x4a0];
    *(ushort *)(local_8 + 0x5a + param_1 * 0x44) = (ushort)(byte)(&DAT_007e1838)[param_1 * 0x4a0];
    FUN__text__004d58e0(local_190,CONCAT22((short)((uint)(param_1 * 0x44) >> 0x10),param_1));
    (&DAT_007e1838)[param_1 * 0x4a0] = local_180;
    local_8 = 0x4c0be6;
    FUN__text__0056ce80();
    return;
  }
  iVar2 = (int)local_28;
  local_60 = (ushort)(byte)(&DAT_006e4159)[iVar2 + local_5c * 0xd];
  local_64 = 0;
  if (local_60 != 0) {
    local_68 = 0;
    local_2c = 0;
    while (local_2c < 7) {
      local_6c = FUN__text__004c0060(CONCAT22((short)((uint)iVar2 >> 0x10),local_28),local_2c);
      local_198 = local_58[(local_6c + -1) * 0xc + 0xb8];
      if ((local_198 == 3) || ((4 < local_198 && (local_198 < 7)))) {
        local_68 = local_2c + 1;
      }
      local_2c = local_2c + 1;
      iVar2 = CONCAT22(extraout_var,local_2c);
    }
    for (local_2c = 0; local_2c < (short)local_60; local_2c = local_2c + 1) {
      local_6c = FUN__text__004c0060(CONCAT22(local_2c >> 0xf,local_28),local_2c);
      local_19c = (uint)(byte)local_58[(local_6c + -1) * 0xc + 0xb8];
      switch(local_19c) {
      case 0:
        local_64 = 1;
        break;
      default:
        local_64 = 2;
        break;
      case 3:
      case 5:
      case 6:
        local_64 = 0;
      }
      if (local_64 == 1) {
        local_70 = (ushort)(byte)(&DAT_0074bf1e)[(int)local_28 + local_30 * 0x60];
        if (local_70 != 100) {
          local_74 = FUN__text__004d1cb0();
          local_74 = local_74 % 0x65;
          if ((short)local_70 < local_74) break;
        }
        local_94 = 0;
        local_78 = 1;
        local_90 = 0;
        goto LAB__text__004c0911;
      }
    }
  }
  goto LAB__text__004c074b;
LAB__text__004c0911:
  if (6 < local_90) goto LAB__text__004c0972;
  local_94 = local_94 + (ushort)(byte)local_58[local_90 * 8 + 0xc];
  if ((short)(ushort)(byte)local_58[local_90 * 8 + 0xc] <
      *(short *)(&DAT_0074f686 + local_90 * 2 + local_6c * 0x32)) {
    local_78 = 0;
    goto LAB__text__004c0972;
  }
  local_90 = local_90 + 1;
  goto LAB__text__004c0911;
LAB__text__004c0972:
  if (local_94 < *(short *)(&DAT_0074f694 + local_6c * 0x32)) {
    local_78 = 0;
  }
  for (local_90 = 0;
      (local_90 < 5 &&
      (*(short *)(&DAT_0074f696 + local_90 * 2 + local_6c * 0x32) <= asStack_8c[local_90]));
      local_90 = local_90 + 1) {
  }
  if (local_78 != 0) {
    local_58[(local_6c + -1) * 0xc + 0xb8] = 2;
    *(undefined2 *)(local_8 + 0x142c) = 1;
    if (-1 < local_20[local_28]) {
      *(undefined2 *)(local_8 + param_1 * 0x44 + 0x4a + local_20[local_28] * 2) = 1;
    }
  }
LAB__text__004c074b:
  local_28 = local_28 + 1;
  goto LAB__text__004c0757;
}

