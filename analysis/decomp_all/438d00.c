
void __thiscall
FUN__text__00438d00(int param_1,short param_2,short param_3,short param_4,short param_5,int param_6,
                   undefined4 param_7,int param_8)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_70 [16];
  int local_30;
  int local_2c;
  int local_28;
  int local_24;
  int local_20;
  int local_1c;
  int local_18;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_70;
  for (iVar1 = 0x1b; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_20 = (int)param_4 - (int)param_2;
  local_24 = (int)param_5 - (int)param_3;
  if (local_20 < 0) {
    local_2c = -1;
    local_20 = -local_20;
  }
  else {
    local_2c = 1;
  }
  if (local_24 < 0) {
    local_30 = -1;
    local_24 = -local_24;
  }
  else {
    local_30 = 1;
  }
  local_c = (int)param_2;
  local_10 = (int)param_3;
  local_28 = 0;
  local_8 = param_1;
  if (local_20 < local_24) {
    for (local_1c = 0; local_14 = local_c, local_18 = local_10, local_1c < local_24;
        local_1c = local_1c + 1) {
      local_10 = local_10 + local_30;
      local_28 = local_28 + local_20;
      if (local_24 <= local_28) {
        local_c = local_c + local_2c;
        local_28 = local_28 - local_24;
      }
      iVar1 = FUN__text__0043bfa0(local_c,local_10,*(undefined4 *)(local_8 + 0x14));
      if ((iVar1 == 0) ||
         ((param_8 != 0 && (iVar1 = FUN__text__0043c0c0(local_c,local_10), iVar1 != 0)))) break;
    }
  }
  else {
    for (local_1c = 0; local_18 = local_10, local_14 = local_c, local_1c < local_20;
        local_1c = local_1c + 1) {
      local_c = local_c + local_2c;
      local_28 = local_28 + local_24;
      if (local_20 <= local_28) {
        local_10 = local_10 + local_30;
        local_28 = local_28 - local_20;
      }
      iVar1 = FUN__text__0043bfa0(local_c,local_10,*(undefined4 *)(local_8 + 0x14));
      if ((iVar1 == 0) ||
         ((param_8 != 0 && (iVar1 = FUN__text__0043c0c0(local_c,local_10), iVar1 != 0)))) break;
    }
  }
  if ((param_2 != local_14) || (param_3 != local_18)) {
    *(ushort *)(param_6 + 0x18) = (ushort)(byte)local_14;
    *(ushort *)(param_6 + 0x1a) = (ushort)(byte)local_18;
    *(undefined1 *)(param_6 + 0x1c) = (undefined1)param_2;
    *(undefined1 *)(param_6 + 0x1d) = (undefined1)param_3;
    *(undefined2 *)(param_6 + 0x1e) = 0;
    *(undefined2 *)(param_6 + 0x20) = 1;
    *(byte *)(param_6 + 0x22) = (byte)local_14;
    *(byte *)(param_6 + 0x23) = (byte)local_18;
  }
  local_8 = 0x438f5d;
  FUN__text__0056ce80();
  return;
}

