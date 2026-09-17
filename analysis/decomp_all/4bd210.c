
void FUN__text__004bd210(void)

{
  short sVar1;
  int iVar2;
  undefined4 *puVar3;
  short asStackY_101f4 [32718];
  undefined4 local_240 [16];
  short local_200;
  short local_1fc;
  undefined *local_1f8;
  short asStack_1f4 [210];
  short asStack_50 [8];
  short local_40 [8];
  short local_30 [8];
  short local_20;
  short local_1c;
  short local_18;
  short local_14;
  short local_10;
  short local_c;
  undefined4 local_8;
  
  puVar3 = local_240;
  for (iVar2 = 0x8f; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_1c = DAT_007a5294;
  local_20 = FUN__text__004d1ba0((int)DAT_007f450c,1,5);
  sVar1 = local_20;
  local_30[6] = DAT_007a5296 + -1;
  if (local_20 < (short)(ushort)(byte)(&DAT_007a54ca)[local_1c]) {
    (&DAT_007a54ca)[local_1c] = (undefined1)local_20;
  }
  local_20 = sVar1;
  if (local_1c == 0x25) {
    local_30[0] = 0;
    local_30[1] = 10;
    local_30[2] = 5;
    local_30[3] = 3;
    local_30[4] = 1;
    local_30[5] = 0;
    local_40[0] = 0xd;
    local_40[1] = 0x4f;
    local_40[2] = 0x52;
    local_40[3] = 0x51;
    local_40[4] = 0x50;
    local_40[5] = 0x53;
    local_40[6] = 0x54;
    for (local_c = 0; local_c < 7; local_c = local_c + 1) {
      asStack_50[local_c] = 0;
    }
    for (local_c = 0; local_c < *(short *)(&DAT_007a52f8 + local_30[6] * 0x70);
        local_c = local_c + 1) {
      local_1f8 = &DAT_007f4518 + local_c * 0xb0;
      local_14 = *(short *)(&DAT_007a52d0 + local_c * 2 + local_30[6] * 0x70);
      for (local_10 = 0; local_10 < 7; local_10 = local_10 + 1) {
        local_18 = local_40[local_10] + -1;
        if ((&DAT_007e18a0)[(short)(local_40[local_10] + -1) * 0xc + local_14 * 0x4a0] == '\0') {
          asStack_1f4[local_10 * 0x1e + (int)asStack_50[local_10]] = local_14;
          asStack_50[local_10] = asStack_50[local_10] + 1;
        }
      }
    }
    FUN__text__004d1c60();
    for (local_c = 0; local_c < local_30[local_20]; local_c = local_c + 1) {
      sVar1 = FUN__text__004d1cb0();
      local_1fc = sVar1 % 7;
      if (asStack_50[sVar1 % 7] != 0) {
        sVar1 = FUN__text__004d1cb0();
        local_200 = sVar1 % asStack_50[local_1fc];
        local_14 = asStack_1f4[local_1fc * 0x1e + (int)(sVar1 % asStack_50[local_1fc])];
        local_18 = local_40[local_1fc] + -1;
        if ((&DAT_007e18a0)[local_18 * 0xc + local_14 * 0x4a0] == '\0') {
          (&DAT_007e18a0)[local_18 * 0xc + local_14 * 0x4a0] = 2;
        }
      }
    }
  }
  local_8 = 0x4bd508;
  FUN__text__0056ce80();
  return;
}

