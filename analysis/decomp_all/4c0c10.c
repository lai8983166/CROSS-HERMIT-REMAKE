
void __thiscall FUN__text__004c0c10(int param_1,short param_2)

{
  undefined1 uVar1;
  int iVar2;
  undefined2 extraout_var;
  undefined4 *puVar3;
  undefined4 local_1ac [16];
  uint local_16c;
  byte local_168;
  short local_164;
  short local_160;
  short asStack_15c [10];
  short local_148;
  short local_144;
  short local_140;
  short local_13c;
  short local_138;
  short local_134;
  ushort local_130;
  short local_12c;
  undefined1 local_128 [16];
  undefined1 local_118;
  int local_30;
  undefined *local_2c;
  short local_28;
  short local_24;
  short local_20 [12];
  int local_8;
  
  puVar3 = local_1ac;
  for (iVar2 = 0x6a; iVar2 != 0; iVar2 = iVar2 + -1) {
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
  local_2c = &DAT_007e17e8 + param_2 * 0x4a0;
  local_30 = 0;
  local_8 = param_1;
  for (local_24 = 0; local_24 < 7; local_24 = local_24 + 1) {
    *(ushort *)(local_8 + param_2 * 0x44 + 0x3a + local_24 * 2) =
         (ushort)(byte)local_2c[local_24 * 8 + 0xc];
    *(ushort *)(local_8 + param_2 * 0x44 + 0x5c + local_24 * 2) =
         (ushort)(byte)local_2c[local_24 * 8 + 0xc];
    *(int *)(local_2c + local_24 * 8 + 0x10) =
         *(int *)(local_2c + local_24 * 8 + 0x10) +
         *(int *)(&DAT_007cf34c + local_24 * 4 + param_2 * 0x124);
    local_30 = local_30 + *(int *)(local_2c + local_24 * 8 + 0x10);
    uVar1 = FUN__text__004d5600(*(undefined4 *)(local_2c + local_24 * 8 + 0x10));
    local_2c[local_24 * 8 + 0xc] = uVar1;
    *(undefined2 *)(local_8 + param_2 * 0x44 + 0x4a + local_24 * 2) = 0;
    *(undefined2 *)(local_8 + param_2 * 0x44 + 0x6c + local_24 * 2) = 0;
  }
  *(ushort *)(local_8 + 0x38 + param_2 * 0x44) = (ushort)(byte)local_2c[0x50];
  *(undefined2 *)(local_8 + 0x5a + param_2 * 0x44) =
       *(undefined2 *)(local_8 + 0x38 + param_2 * 0x44);
  FUN__text__004d58e0(local_128,CONCAT22((short)((uint)(param_2 * 0x44) >> 0x10),param_2));
  local_2c[0x50] = local_118;
  local_12c = *(short *)(local_2c + 6);
  local_130 = 0;
  local_134 = 0;
  local_138 = 0;
  local_13c = 0;
  local_140 = 0;
  local_144 = 0;
  local_148 = 1;
  for (local_24 = 0; local_24 < 5; local_24 = local_24 + 1) {
    asStack_15c[local_24] = (short)(char)(&DAT_007cf424)[local_24 * 2 + param_2 * 0x124];
    asStack_15c[local_24] =
         asStack_15c[local_24] + (short)(char)(&DAT_007cf425)[local_24 * 2 + param_2 * 0x124];
    asStack_15c[local_24] =
         asStack_15c[local_24] + (short)(char)(&DAT_007cf42e)[local_24 * 2 + param_2 * 0x124];
    asStack_15c[local_24] =
         asStack_15c[local_24] + (short)(char)(&DAT_007cf42f)[local_24 * 2 + param_2 * 0x124];
    asStack_15c[local_24] =
         asStack_15c[local_24] + (short)(char)(&DAT_007cf438)[local_24 * 2 + param_2 * 0x124];
    asStack_15c[local_24] =
         asStack_15c[local_24] + (short)(char)(&DAT_007cf439)[local_24 * 2 + param_2 * 0x124];
  }
  local_24 = 0;
LAB__text__004c0f9c:
  if (10 < local_24) {
    local_8 = 0x4c132b;
    FUN__text__0056ce80();
    return;
  }
  iVar2 = (int)local_24;
  local_130 = (ushort)(byte)(&DAT_006e4159)[iVar2 + local_12c * 0xd];
  local_134 = 0;
  if (local_130 != 0) {
    local_13c = 0;
    local_28 = 0;
    while (local_28 < 7) {
      local_138 = FUN__text__004c0060(CONCAT22((short)((uint)iVar2 >> 0x10),local_24),local_28);
      local_168 = local_2c[(local_138 + -1) * 0xc + 0xb8];
      if ((local_168 == 3) || ((4 < local_168 && (local_168 < 7)))) {
        local_13c = local_28 + 1;
      }
      local_28 = local_28 + 1;
      iVar2 = CONCAT22(extraout_var,local_28);
    }
    for (local_28 = 0; local_28 < (short)local_130; local_28 = local_28 + 1) {
      local_138 = FUN__text__004c0060(CONCAT22(local_28 >> 0xf,local_24),local_28);
      local_16c = (uint)(byte)local_2c[(local_138 + -1) * 0xc + 0xb8];
      switch(local_16c) {
      case 0:
        local_134 = 1;
        break;
      default:
        local_134 = 2;
        break;
      case 3:
      case 5:
      case 6:
        local_134 = 0;
      }
      if (local_134 == 2) break;
      if (local_134 == 1) {
        local_140 = local_130 + local_13c * 5;
        if (local_140 != 100) {
          local_144 = FUN__text__004d1cb0();
          local_144 = local_144 % 0x65;
          if (local_140 < local_144) break;
        }
        local_164 = 0;
        local_148 = 1;
        local_160 = 0;
        goto LAB__text__004c11a5;
      }
    }
  }
  goto LAB__text__004c0f90;
LAB__text__004c11a5:
  if (6 < local_160) goto LAB__text__004c120c;
  local_164 = local_164 + (ushort)(byte)local_2c[local_160 * 8 + 0xc];
  if ((short)(ushort)(byte)local_2c[local_160 * 8 + 0xc] <
      *(short *)(&DAT_0074f686 + local_160 * 2 + local_138 * 0x32)) {
    local_148 = 0;
    goto LAB__text__004c120c;
  }
  local_160 = local_160 + 1;
  goto LAB__text__004c11a5;
LAB__text__004c120c:
  if (local_164 < *(short *)(&DAT_0074f694 + local_138 * 0x32)) {
    local_148 = 0;
  }
  else {
    for (local_160 = 0; local_160 < 5; local_160 = local_160 + 1) {
      if (asStack_15c[local_160] < *(short *)(&DAT_0074f696 + local_160 * 2 + local_138 * 0x32)) {
        local_148 = 0;
        break;
      }
    }
  }
  if (local_148 != 0) {
    local_2c[(local_138 + -1) * 0xc + 0xb8] = 2;
    *(undefined2 *)(local_8 + 0x142c) = 1;
    if (-1 < local_20[local_24]) {
      *(undefined2 *)(local_8 + param_2 * 0x44 + 0x4a + local_20[local_24] * 2) = 1;
    }
  }
LAB__text__004c0f90:
  local_24 = local_24 + 1;
  goto LAB__text__004c0f9c;
}

