
void __thiscall FUN__text__004a8bf0(undefined4 param_1,short param_2,short param_3)

{
  int iVar1;
  undefined4 *puVar2;
  short asStack_10350 [70];
  short asStack_102c4 [70];
  short asStack_10238 [70];
  ushort auStack_101ac [70];
  ushort auStack_10120 [70];
  short asStack_10094 [32358];
  undefined4 local_3bc [16];
  int local_37c;
  int local_378;
  int local_374;
  undefined4 local_370;
  short local_36c;
  ushort local_368;
  undefined *local_364;
  ushort local_360;
  short local_35c;
  short local_358;
  short local_354;
  short asStack_350 [70];
  short asStack_2c4 [70];
  short asStack_238 [70];
  ushort auStack_1ac [70];
  ushort auStack_120 [70];
  short asStack_94 [70];
  undefined4 local_8;
  
  puVar2 = local_3bc;
  for (iVar1 = 0xee; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  local_354 = -1;
  for (local_358 = 0; local_358 < 0x46; local_358 = local_358 + 1) {
    asStack_2c4[local_358] = 0;
  }
  local_374 = (int)param_3;
  if (local_374 == 0) {
    local_354 = DAT_007d57de;
    for (local_358 = 0; local_358 < local_354; local_358 = local_358 + 1) {
      local_35c = *(short *)(&DAT_007d57e2 + local_358 * 2);
      asStack_94[local_358] = *(short *)(&DAT_007d57e2 + local_358 * 2);
      local_364 = &DAT_007e17e8 + local_35c * 0x4a0;
      auStack_120[local_358] = (ushort)(byte)(&DAT_007e1838)[local_35c * 0x4a0];
      auStack_1ac[local_358] = (ushort)(byte)(&DAT_006b2d8a)[*(short *)(local_364 + 6) * 0x40];
      asStack_238[local_358] = 0;
      asStack_238[local_358] = asStack_238[local_358] + (ushort)(byte)local_364[0xc];
      asStack_238[local_358] = asStack_238[local_358] + (ushort)(byte)local_364[0x14];
      asStack_238[local_358] = asStack_238[local_358] + (ushort)(byte)local_364[0x1c];
      asStack_238[local_358] = asStack_238[local_358] + (ushort)(byte)local_364[0x24];
      asStack_238[local_358] = asStack_238[local_358] + (ushort)(byte)local_364[0x2c];
      asStack_238[local_358] = asStack_238[local_358] + (ushort)(byte)local_364[0x34];
      asStack_238[local_358] = asStack_238[local_358] + (ushort)(byte)local_364[0x3c];
      asStack_2c4[local_358] = 1;
    }
  }
  else if (local_374 == 1) {
    local_354 = DAT_007d58b0;
    for (local_358 = 0; local_358 < local_354; local_358 = local_358 + 1) {
      local_35c = *(short *)(&DAT_007d58b4 + local_358 * 2);
      asStack_94[local_358] = *(short *)(&DAT_007d58b4 + local_358 * 2);
      local_364 = &DAT_006f5088 + local_35c * 0x4a0;
      auStack_120[local_358] = (ushort)(byte)(&DAT_006f50d8)[local_35c * 0x4a0];
      auStack_1ac[local_358] = (ushort)(byte)(&DAT_006b2d8a)[*(short *)(local_364 + 6) * 0x40];
      asStack_238[local_358] = 0;
      asStack_238[local_358] = asStack_238[local_358] + (ushort)(byte)local_364[0xc];
      asStack_238[local_358] = asStack_238[local_358] + (ushort)(byte)local_364[0x14];
      asStack_238[local_358] = asStack_238[local_358] + (ushort)(byte)local_364[0x1c];
      asStack_238[local_358] = asStack_238[local_358] + (ushort)(byte)local_364[0x24];
      asStack_238[local_358] = asStack_238[local_358] + (ushort)(byte)local_364[0x2c];
      asStack_238[local_358] = asStack_238[local_358] + (ushort)(byte)local_364[0x34];
      asStack_238[local_358] = asStack_238[local_358] + (ushort)(byte)local_364[0x3c];
      asStack_2c4[local_358] = 1;
    }
  }
  local_378 = (int)param_2;
  if (local_378 == 0) {
    for (local_368 = 0; (int)(short)local_368 < local_354 + -1; local_368 = local_368 + 1) {
      for (local_36c = local_368 + 1; local_36c < local_354; local_36c = local_36c + 1) {
        if ((short)auStack_120[(short)local_368] < (short)auStack_120[local_36c]) {
          local_360 = auStack_120[(short)local_368];
          auStack_120[(short)local_368] = auStack_120[local_36c];
          auStack_120[local_36c] = local_360;
          local_360 = asStack_94[(short)local_368];
          asStack_94[(short)local_368] = asStack_94[local_36c];
          asStack_94[local_36c] = local_360;
        }
      }
    }
    for (local_368 = 0; (short)local_368 < local_354; local_368 = local_368 + 1) {
      asStack_350[(short)local_368] = asStack_94[(short)local_368];
    }
  }
  else if (local_378 == 1) {
    local_370 = (uint)local_370._2_2_ << 0x10;
    for (local_368 = 0; (short)local_368 < 6; local_368 = local_368 + 1) {
      for (local_36c = 0; local_36c < local_354; local_36c = local_36c + 1) {
        if ((auStack_1ac[local_36c] == local_368) && (asStack_2c4[local_36c] != 0)) {
          asStack_350[local_370 & 0xffff] = asStack_94[local_36c];
          local_370 = CONCAT22(local_370._2_2_,(short)local_370 + 1);
          asStack_2c4[local_36c] = 0;
        }
      }
    }
  }
  else if (local_378 == 2) {
    for (local_368 = 0; (int)(short)local_368 < local_354 + -1; local_368 = local_368 + 1) {
      for (local_36c = local_368 + 1; local_36c < local_354; local_36c = local_36c + 1) {
        if (asStack_238[(short)local_368] < asStack_238[local_36c]) {
          local_360 = asStack_238[(short)local_368];
          asStack_238[(short)local_368] = asStack_238[local_36c];
          asStack_238[local_36c] = local_360;
          local_360 = asStack_94[(short)local_368];
          asStack_94[(short)local_368] = asStack_94[local_36c];
          asStack_94[local_36c] = local_360;
        }
      }
    }
    for (local_368 = 0; (short)local_368 < local_354; local_368 = local_368 + 1) {
      asStack_350[(short)local_368] = asStack_94[(short)local_368];
    }
  }
  local_37c = (int)param_3;
  if (local_37c == 0) {
    for (local_358 = 0; local_358 < local_354; local_358 = local_358 + 1) {
      *(short *)(&DAT_007d57e2 + local_358 * 2) = asStack_350[local_358];
    }
  }
  else if (local_37c == 1) {
    for (local_358 = 0; local_358 < local_354; local_358 = local_358 + 1) {
      *(short *)(&DAT_007d58b4 + local_358 * 2) = asStack_350[local_358];
    }
  }
  return;
}

