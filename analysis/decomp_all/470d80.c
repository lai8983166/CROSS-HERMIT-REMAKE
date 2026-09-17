
void __thiscall FUN__text__00470d80(int param_1,int param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_88 [16];
  short local_48;
  short local_44;
  short local_40;
  short local_3c;
  int local_38;
  short local_34;
  short local_30;
  short local_2c;
  short local_28;
  short local_24;
  short local_20;
  short local_1c;
  short local_18;
  short local_14;
  undefined2 local_10;
  undefined2 local_c;
  int local_8;
  
  puVar2 = local_88;
  for (iVar1 = 0x21; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  iVar1 = (int)(short)((uint)*(undefined4 *)(param_2 + 0x2ec) >> 0x10);
  local_c = (undefined2)((int)(iVar1 + (iVar1 >> 0x1f & 0x1fU)) >> 5);
  iVar1 = (int)(short)((uint)*(undefined4 *)(param_2 + 0x2f0) >> 0x10);
  local_10 = (undefined2)((int)(iVar1 + (iVar1 >> 0x1f & 0xfU)) >> 4);
  local_2c = (short)((int)((int)*(short *)(param_2 + 0x4d4) +
                          ((int)*(short *)(param_2 + 0x4d4) >> 0x1f & 0x1fU)) >> 5);
  local_30 = (short)((int)((int)*(short *)(param_2 + 0x4d6) +
                          ((int)*(short *)(param_2 + 0x4d6) >> 0x1f & 0xfU)) >> 4);
  local_14 = (short)((int)((int)*(short *)(param_2 + 0x4d8) +
                          ((int)*(short *)(param_2 + 0x4d8) >> 0x1f & 0x1fU)) >> 5);
  local_18 = (short)((int)((int)*(short *)(param_2 + 0x4da) +
                          ((int)*(short *)(param_2 + 0x4da) >> 0x1f & 0xfU)) >> 4);
  local_24 = local_14 - local_2c;
  local_28 = local_18 - local_30;
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
  local_20 = local_30;
  local_1c = local_2c;
  local_8 = param_1;
  if (local_24 < local_28) {
    for (local_34 = 0; local_34 < local_28; local_34 = local_34 + 1) {
      local_30 = local_30 + local_40;
      local_38 = local_38 + local_24;
      if (local_28 <= local_38) {
        local_2c = local_2c + local_3c;
        local_38 = local_38 - local_28;
      }
      local_44 = local_2c * 0x20 - *(short *)(local_8 + 0x2a30e);
      local_48 = (local_30 * 0x10 - *(short *)(local_8 + 0x2a310)) + 0x1e;
      FUN__text__00410310(local_44 + 4,local_48 + 2,0x18,0xc,900,0x800000ff,1);
    }
  }
  else {
    for (local_34 = 0; local_34 < local_24; local_34 = local_34 + 1) {
      local_2c = local_2c + local_3c;
      local_38 = local_38 + local_28;
      if (local_24 <= local_38) {
        local_30 = local_30 + local_40;
        local_38 = local_38 - local_24;
      }
      local_44 = local_2c * 0x20 - *(short *)(local_8 + 0x2a30e);
      local_48 = (local_30 * 0x10 - *(short *)(local_8 + 0x2a310)) + 0x1e;
      FUN__text__00410310(local_44 + 4,local_48 + 2,0x18,0xc,900,0x800000ff,1);
    }
  }
  local_8 = 0x47105b;
  FUN__text__0056ce80();
  return;
}

