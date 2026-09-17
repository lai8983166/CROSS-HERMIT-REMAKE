
undefined4 FUN__text__00470a50(int param_1)

{
  short sVar1;
  short sVar2;
  undefined4 uVar3;
  int iVar4;
  undefined4 *puVar5;
  undefined4 local_80 [16];
  short local_40;
  short local_3c;
  int local_38;
  short local_34;
  short local_30;
  short local_2c;
  short local_28;
  short local_24;
  
  puVar5 = local_80;
  for (iVar4 = 0x1f; iVar4 != 0; iVar4 = iVar4 + -1) {
    *puVar5 = 0xcccccccc;
    puVar5 = puVar5 + 1;
  }
  iVar4 = (int)(short)((uint)*(undefined4 *)(param_1 + 0x2ec) >> 0x10);
  sVar1 = (short)((int)(iVar4 + (iVar4 >> 0x1f & 0x1fU)) >> 5);
  iVar4 = (int)(short)((uint)*(undefined4 *)(param_1 + 0x2f0) >> 0x10);
  sVar2 = (short)((int)(iVar4 + (iVar4 >> 0x1f & 0xfU)) >> 4);
  local_2c = (short)((int)((int)*(short *)(param_1 + 0x4d4) +
                          ((int)*(short *)(param_1 + 0x4d4) >> 0x1f & 0x1fU)) >> 5);
  local_30 = (short)((int)((int)*(short *)(param_1 + 0x4d6) +
                          ((int)*(short *)(param_1 + 0x4d6) >> 0x1f & 0xfU)) >> 4);
  local_24 = (short)((int)((int)*(short *)(param_1 + 0x4d8) +
                          ((int)*(short *)(param_1 + 0x4d8) >> 0x1f & 0x1fU)) >> 5);
  local_28 = (short)((int)((int)*(short *)(param_1 + 0x4da) +
                          ((int)*(short *)(param_1 + 0x4da) >> 0x1f & 0xfU)) >> 4);
  if ((sVar1 == local_24) && (sVar2 == local_28)) {
    *(short *)(param_1 + 0x4dc) = local_24 * 0x20 + 0x10;
    *(short *)(param_1 + 0x4de) = local_28 * 0x10 + 8;
    uVar3 = 1;
  }
  else {
    local_24 = local_24 - local_2c;
    local_28 = local_28 - local_30;
    if (local_24 < 0) {
      local_3c = -1;
      local_24 = -local_24;
    }
    else {
      local_3c = 1;
    }
    if (local_28 < 0) {
      local_40 = -1;
      local_28 = -local_28;
    }
    else {
      local_40 = 1;
    }
    local_38 = 0;
    if (local_24 < local_28) {
      for (local_34 = 0; local_34 < local_28; local_34 = local_34 + 1) {
        if ((sVar1 == local_2c) && (sVar2 == local_30)) {
          local_30 = local_30 + local_40;
          if ((int)local_28 <= local_38 + local_24) {
            local_2c = local_2c + local_3c;
          }
          break;
        }
        local_30 = local_30 + local_40;
        local_38 = local_38 + local_24;
        if (local_28 <= local_38) {
          local_2c = local_2c + local_3c;
          local_38 = local_38 - local_28;
        }
      }
    }
    else {
      for (local_34 = 0; local_34 < local_24; local_34 = local_34 + 1) {
        if ((sVar1 == local_2c) && (sVar2 == local_30)) {
          local_2c = local_2c + local_3c;
          if ((int)local_24 <= local_38 + local_28) {
            local_30 = local_30 + local_40;
          }
          break;
        }
        local_2c = local_2c + local_3c;
        local_38 = local_38 + local_28;
        if (local_24 <= local_38) {
          local_30 = local_30 + local_40;
          local_38 = local_38 - local_24;
        }
      }
    }
    *(short *)(param_1 + 0x4dc) = local_2c * 0x20 + 0x10;
    *(short *)(param_1 + 0x4de) = local_30 * 0x10 + 8;
    uVar3 = 0;
  }
  return uVar3;
}

